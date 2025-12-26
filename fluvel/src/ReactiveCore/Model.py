# Copyright (C) 2025 J. F. Escobar
#
# This file is part of Fluvel.
#
# Fluvel is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Fluvel is distributed WITHOUT ANY WARRANTY, even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for details.
#
# See the file COPYING.LESSER for more details on the LGPLv3 license.

"""
Reactive Core Module
====================

Este módulo implementa el motor de reactividad de Fluvel.
Provee la clase base :class:`Model`, descriptores para átomos reactivos,
computados con caché, y soporte para colecciones reactivas.
"""

from __future__ import annotations
import inspect, threading, functools
from typing import get_type_hints, Dict, Any, Callable, List, Tuple, Set, Type, get_origin
from dataclasses import dataclass

# PySide6
from PySide6.QtCore import QObject, Signal

# =================
# CORE DEPENDENCIES
# =================

_thread_local = threading.local()

def _get_reactive_stack() -> Tuple[List["ReactiveComputedAtom"], Set[str]]:
    """
    Recupera la pila de ejecución reactiva del hilo actual.
    
    Se utiliza para detectar qué átomo computado se está evaluando actualmente
    y registrar sus dependencias automáticamente.

    :return: Una tupla conteniendo la pila (lista) y un set de claves para búsqueda O(1).
    :rtype: Tuple[List[ReactiveComputedAtom], Set[str]]
    """
    if not hasattr(_thread_local, "stack_list"):
        _thread_local.stack_list = []
        _thread_local.stack_keys = set()
    return _thread_local.stack_list, _thread_local.stack_keys

class ModelCreationError(Exception):
    """
    Excepción lanzada cuando hay errores en la definición o registro de un Modelo.
    """
    pass

class CycleError(RecursionError):
    """
    Excepción lanzada cuando se detecta un ciclo infinito de dependencia reactiva.
    """
    pass

# ========
# METADATA
# ========

@dataclass(slots=True)
class ComputedMetadata:
    """
    Contenedor de metadatos para funciones decoradas con @computed.
    """
    func: Callable

@dataclass(slots=True)
class SubscriptionMetadata:
    """
    Contenedor de metadatos para funciones decoradas con @subscribe.
    """
    func: Callable
    deps: List[str]

def computed(func) -> ComputedMetadata:
    """
    Decorador para marcar un método como una Propiedad Computada.
    
    Las propiedades computadas cachean su resultado y solo se recalculan
    cuando sus dependencias reactivas cambian.

    :param func: El método a decorar.
    :return: Metadatos para que el Modelo construya el descriptor.
    """
    return ComputedMetadata(func=func)

def subscribe(func) -> SubscriptionMetadata:
    """
    Decorador para marcar un método como un Suscriptor (Efecto secundario).
    
    La función se ejecutará automáticamente cuando cambien los argumentos
    definidos en su firma.

    :param func: El método a decorar.
    :return: Metadatos con las dependencias extraídas de la firma.
    """
    signature = inspect.signature(func)

    # Extraemos los nombres de los argumentos (excepto 'self') como dependencias
    dependencies = list(signature.parameters.keys())[1:]

    return SubscriptionMetadata(func=func, deps=dependencies)

# =============================
#  REACTIVE ATOMS - DESCRIPTORS
# =============================

@dataclass(slots=True)
class ReactiveAtom:
    """
    Descriptor de datos que gestiona el acceso y modificación de un atributo reactivo.
    
    Implementa la lógica de notificar cambios y permitir que los observadores
    se registren automáticamente al acceder al valor (Dependency Tracking).
    """
    key: str
    deep_key: str
    initial_value: Any
    value_type: type
    base_type: type

    def __get__(self, instance: "Model", owner) -> Any:
        """
        Accesor del descriptor. Registra la dependencia si hay un computado activo.
        """
        # TRACKING: Registro de dependencia automático
        stack, _ = _get_reactive_stack() # ignora el set
        
        # Si hay algo en la pila, significa que un computado está leyendo este valor
        if stack:
            observer: "ReactiveComputedAtom" = stack[-1]
            instance._register_dependency(self.key, observer.key_name)

        return getattr(instance, self.deep_key, self.initial_value)

    def __set__(self, instance: "Model", new_value: Any) -> None:
        """
        Mutador del descriptor. Notifica cambios solo si el valor es diferente.
        """
        current_value = getattr(instance, self.deep_key, self.initial_value)
        
        if new_value != current_value:
            setattr(instance, self.deep_key, new_value)
            instance._notify_change(self.key, new_value)

@dataclass(slots=True)
class ReactiveComputedAtom:
    """
    Descriptor para propiedades computadas (derivadas).
    
    Gestiona el caché, la validación (lazy evaluation) y la detección de ciclos.
    """
    func: Callable
    key_name: str

    def __get__(self, instance: "Model" | None, owner) -> Any:
        """
        Calcula o devuelve el valor cacheado de la propiedad.
        """

        # Si el valor es válido, no es necesario recalcular,
        # por lo que solo lo retornamos desde la caché
        if instance._is_computed_valid(self.key_name):
            return instance._computed_cache[self.key_name]

        # Preparación para recálculo
        stack, stack_keys = _get_reactive_stack()
        
        # Detección de ciclos
        if self.key_name in stack_keys:
            raise CycleError(f"Circular dependency detected in '{self.key_name}'")

        # TRACKING: Inicio evaluación (hacemos un Push en la pila)
        stack.append(self)
        stack_keys.add(self.key_name) 

        # Se limpian las dependencias antiguas antes de re-evaluar
        # para soportar ramificaciones dinámicas (o sea los if/else en la función)
        # (testear)
        instance._reset_computed_dependencies(self.key_name)

        try:
            new_value = self.func(instance)
        finally:
            # limpiamos la pila
            stack.pop()
            stack_keys.remove(self.key_name)

        # Actualizar caché y notificar a sus propios observadores
        instance._update_computed_cache(self.key_name, new_value)
        return new_value

    def __set__(self, instance, value) -> None:
        """Impide la modificación directa de una propiedad computada."""
        raise AttributeError(f"The computed property '{self.key_name}' is read-only.")

@dataclass(slots=True)
class ReactiveCollectionAtom(ReactiveAtom):
    """
    Descriptor especializado que convierte listas y diccionarios estándar
    en sus variantes reactivas (`ReactiveList`, `ReactiveDict`) al inicializarse.
    """
    
    def get_reactive_collection(self, instance: "Model", init_value: Any) -> ReactiveList | ReactiveDict:
        """
        Factoría que decide qué tipo de colección reactiva crear.
        """
        if self.base_type is list:
            reactive_collection = ReactiveList

        elif self.base_type is dict:
            reactive_collection = ReactiveDict

        else:
            return init_value

        reactive_value = self._create_reactive_collection(instance, init_value, reactive_collection)

        return reactive_value

    def _create_reactive_collection(
        self,
        instance: "Model",
        reactive_value: Any,
        ReactiveCollection: Type[ReactiveList] | Type[ReactiveDict]
    ) -> ReactiveList | ReactiveDict:
        """Crea la instancia de la colección reactiva vinculada al modelo."""

        # Inicialización estándar
        if reactive_value is None or reactive_value is self.initial_value:
            # Usa el valor inicial si es el default, sino inicializa vacío
            value = self.initial_value if reactive_value is self.initial_value else self.base_type()
            coll_to_wrap = self.base_type(value)

        else:
            # Es un valor pasado por el usuario en el constructor
            coll_to_wrap = reactive_value
        
        # Crea la instancia reactiva pasando el owner y la key para notificaciones
        reactive_instance = ReactiveCollection(instance, self.key, coll_to_wrap)

        return reactive_instance

# =============================
#  SUBSCRIPTION
# =============================

@dataclass(slots=True)
class Subscription:
    """
    Representa una suscripción activa (Efecto) dentro de un Modelo.
    Vincula una función con sus dependencias y el contexto de ejecución.
    """
    instance: "Model"
    key_name: str
    func: Callable
    deps: List[str]

    def run(self):
        """Ejecuta la función suscrita inyectando los valores actuales de las dependencias."""
        values = {key: getattr(self.instance, key) for key in self.deps}
        self.func(self.instance, **values)

# ======================
#  COLECCIONES REACTIVAS
# ======================

def _create_reactive_wrapper(original_method):
    """
    Crea un wrapper alrededor de un método mutante (ej. append, pop)
    que notifica al sistema reactivo después de la ejecución.
    """
    
    @functools.wraps(original_method)
    def wrapped_method(self, *args, **kwargs):

        # Ejecuta la lógica original (e.g., list.append)
        # Se llama como función unida (bound) implícitamente por el descriptor
        result = original_method(self, *args, **kwargs) 
        
        # Se notifica al motor reactivo que la colección cambió
        self._notify()
        
        # Por último, se devuelve el resultado original (ej. el elemento de pop())
        return result

    return wrapped_method

class BaseReactiveCollection:
    """
    Mixin que dota de capacidades de notificación a las colecciones.
    """

    _MUTATOR_METHODS: List[str]

    def __init_subclass__(cls, **kwargs):
        """
        Intercepta la creación de subclases para envolver
        automáticamente los métodos mutantes definidos en _MUTATOR_METHODS.
        """
        super().__init_subclass__(**kwargs)

        mutators: List[str] = getattr(cls, '_MUTATOR_METHODS', [])
        
        for mutator_name in mutators:
            
            # Obtenemos el método original de la clase base (list o dict)
            original_method = getattr(cls, mutator_name)
            
            # Usamos la función externa para crear el nuevo método envuelto
            wrapped_method = _create_reactive_wrapper(original_method)
            
            # Sobrescribimos el método en la clase
            setattr(cls, mutator_name, wrapped_method)

    def __init__(self, owner: "Model", key: str):
        self._owner = owner
        self._key = key

    def _notify(self): 
        """
        Método de notificación que será llamado por el wrapper.
        """
        self._owner._notify_change(self._key, self)

class ReactiveList(list, BaseReactiveCollection):
    """Lista que notifica a su modelo propietario cuando su contenido cambia."""

    _MUTATOR_METHODS = [
        "__setitem__", "__delitem__", "__iadd__", "append", "extend", 
        "pop", "remove", "clear", "reverse", "sort","insert"
    ]

    def __init__(self, owner: "Model", key: str, iterable=()):
        # Llamada explícita a constructores para herencia múltiple segura con tipos builtin
        super().__init__(iterable)
        BaseReactiveCollection.__init__(self, owner, key)

class ReactiveDict(dict, BaseReactiveCollection):
    """Diccionario que notifica a su modelo propietario cuando su contenido cambia."""

    _MUTATOR_METHODS = [
        "__setitem__", "__delitem__", "pop", 
        "popitem", "clear", "update"
    ]
    
    def __init__(self, owner: "Model", key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        BaseReactiveCollection.__init__(self, owner, key)
    
    def setdefault(self, key, default=None):
        """
        Sobrescrutura manual de setdefault porque su notificación es condicional.
        Solo notifica si la clave NO existía.
        """
        if key not in self:
            val = super().setdefault(key, default)
            self._notify()
            return val
        return super().setdefault(key, default)

# =============
#  GLOBAL STORE
# =============

class ModelStore:
    """
    Almacén global de Modelos activos utilizando referencias fuertes.
    Permite recuperar modelos por su alias en cualquier parte de la app.
    """
    __store__: Dict[str, "Model"] = {}

    @classmethod
    def add_model(cls, model: "Model", alias: str) -> None:
        if alias in cls.__store__: 
            raise ModelCreationError(f"Alias '{alias}' already in use.")
        cls.__store__[alias] = model

    @classmethod
    def get_model(cls, alias: str) -> "Model":
        """
        Recupera una instancia de modelo por su alias.

        :raises ValueError: Si el modelo no existe o fue recolectado por el GC.
        """
        model = cls.__store__.get(alias) 
        if model is None:
            raise ValueError(f"There is no model with the alias '{alias}' or it was destroyed.")
        return model

    @classmethod
    def remove_model(cls, alias: str) -> None:
        if alias in cls.__store__:
            del cls.__store__[alias]

# =======
# EMITTER
# =======

class ModelEmitter(QObject):
    """
    Puente de señales Qt para integrar el modelo reactivo con la UI.
    """
    model_changed = Signal(str, object)

# ========================
#  CORE - MODEL
# ========================

class Model:
    """        
    Base class for creating reactive ViewModels.

    Uses type introspection to convert annotated attributes into reactive atoms. 
    Supports computed properties, subscriptions, and linking with PySide6.
    """

    def __init_subclass__(cls, **kwargs):
        """            
        Analyze the type annotations and decorators of the subclass
        to construct the reactive descriptors.
        """
        super().__init_subclass__(**kwargs)

        cls._atom_names             : Dict[str, str]                    = {}    # Map: Atom -> AtomDeepKey
        cls._computed_names         : Set[str]                          = set()
        cls._subscription_metadata  : Dict[str, SubscriptionMetadata]   = {}

        model_annotations = get_type_hints(cls)

        for name, attr_value in vars(cls).items():
            
            # Ignora los atributos privados, métodos dunder o métodos comunes
            if name.startswith("_") or callable(attr_value): continue

            if isinstance(attr_value, ComputedMetadata):
                # Convierte métodos @computed en descriptores ReactiveComputedAtom
                setattr(cls, name, ReactiveComputedAtom(attr_value.func, name))
                cls._computed_names.add(name)

            elif isinstance(attr_value, SubscriptionMetadata):
                # Guarda metadatos de suscripción para instanciar en __init__
                cls._subscription_metadata[name] = attr_value

            else:
                # Procesa atributos de clase como Átomos de Estado
                default_value = getattr(cls, name, None)
                deep_key = f"_deep_{name}" # Nombre interno de almacenamiento
                var_type = model_annotations.get(name)
                base_type = get_origin(var_type)

                # Decide si usar átomo simple o colección reactiva
                if base_type in (list, dict):
                    descriptor = ReactiveCollectionAtom(name, deep_key, default_value, var_type, base_type)
                else:
                    descriptor = ReactiveAtom(name, deep_key, default_value, var_type, base_type)

                setattr(cls, name, descriptor)
                cls._atom_names[name] = deep_key

    def __init__(self, *, alias: str, **kwargs):
        """
        Inicializa una nueva instancia del Modelo.

        :param alias: Identificador único para el almacén global.
        :param kwargs: Valores iniciales para sobrescribir los defaults de la clase.
        """
        self.__alias__: str = alias
        self.qt_emitter: ModelEmitter = ModelEmitter()

        # Estructuras internas del grafo de dependencia por modelo
        self._computed_cache    : Dict[str, Any]            = {} # Map: ComputedAtom -> Any
        self._computed_validity : Dict[str, bool]           = {} # Map: ComputedAtom -> bool
        self._dep_listeners     : Dict[str, str]            = {} # Map: Atom -> Set[Observers]
        self._observing         : Dict[str, Set[str]]       = {} # Map: Observer -> Set[Atoms]
        self._subscriptions     : Dict[str, Subscription]   = {} # Map: str -> Subscribers
        
        # Inicializar Atoms de acuerdo al Map: 'Atom -> AtomDeepKey'
        for name, deep_key in self.__class__._atom_names.items():
            
            descriptor: ReactiveAtom | ReactiveCollectionAtom = self.__class__.__dict__.get(name)

            init_value = kwargs.pop(name, descriptor.initial_value)

            if isinstance(descriptor, ReactiveCollectionAtom):
                init_value = descriptor.get_reactive_collection(self, init_value)

            setattr(self, deep_key, init_value)

        # Inicializar Computadas (Marcar como inválidas inicialmente)
        for computed_key in self.__class__._computed_names:
            self._computed_validity[computed_key] = False

        # Inicializar Suscripciones (Registro)
        for name, metadata in self.__class__._subscription_metadata.items():
            sub = Subscription(self, name, metadata.func, metadata.deps)
            self._subscriptions[name] = sub
            # Registro estático de dependencias (se conocen por la firma)
            for atom_key in metadata.deps:
                self._dep_listeners.setdefault(atom_key, set()).add(name)

        ModelStore.add_model(self, alias)

        # Ejecución Inicial de Suscripciones
        for sub in self._subscriptions.values():
            sub.run()

    def _register_dependency(self, atom_key: str, observer_key: str) -> None:
        """
        Registra una relación de dependencia en el grafo.
        """
        self._dep_listeners.setdefault(atom_key, set()).add(observer_key)
        self._observing.setdefault(observer_key, set()).add(atom_key)

    def _is_computed_valid(self, key: str) -> bool:
        return self._computed_validity.get(key, False)

    def _invalidate_computed(self, key: str):
        self._computed_validity[key] = False

    def _reset_computed_dependencies(self, computed_key: str) -> None:
        """
        Elimina las dependencias previas de un computado.
        Esencial para que el grafo se adapte a lógica condicional (if/else).
        """
        observed_atoms = self._observing.get(computed_key) 

        if observed_atoms: 
            # Limpieza del mapa inverso (_dep_listeners)
            for atom_key in observed_atoms:
                if atom_key in self._dep_listeners:
                    self._dep_listeners[atom_key].discard(computed_key)
                    # Limpieza opcional de claves vacías
                    if not self._dep_listeners[atom_key]:
                        del self._dep_listeners[atom_key]

            # Limpieza final y explícita del mapa de observación
            del self._observing[computed_key]

    def _update_computed_cache(self, key: str, value: Any):
        """
        Actualiza el caché y notifica a los que dependen de este computado.
        """
        old_value = self._computed_cache.get(key)
        self._computed_cache[key] = value
        self._computed_validity[key] = True

        if old_value != value:
            self._notify_change(key, value)

    def _notify_change(self, key: str, new_value: Any) -> None:
        """
        Núcleo de la propagación de cambios.

        1. Emite señal Qt para notificar a los widgets asociados.
        2. Ejecuta suscriptores.
        3. Invalida y recalcula propiedades computadas dependientes.
        """
        self.qt_emitter.model_changed.emit(key, new_value)

        if key in self._dep_listeners:

            # Obtenemos el grafo de dependencias, es decir,
            # las computed o suscripciones asociadas al atom
            listeners = self._dep_listeners[key].copy()
            
            for observer_key in listeners:

                if observer_key in self._subscriptions:
                    self._subscriptions[observer_key].run()

                elif observer_key in self.__class__._computed_names:
                    # Eager Propagation: Invalida y fuerza recálculo
                    self._invalidate_computed(observer_key)
                    getattr(self, observer_key) # Trigger __get__

    def __repr__(self) -> str:
        params = [f"{name}={repr(getattr(self, name))}" for name in self._atom_names.keys()]
        return f"{type(self).__name__}({', '.join(params)})"

    def dispose(self) -> None:
        """
        Libera recursos internos y limpia el grafo de dependencias.
        """
        self._dep_listeners.clear()
        self._observing.clear()
        self._subscriptions.clear()
        self._computed_cache.clear()

    def destroy(self) -> None:
        """
        Elimina el modelo del Store global y libera recursos.
        """
        self.dispose()
        ModelStore.remove_model(self.__alias__)

    def to_dict(self) -> Dict[str, Any]:
        """
        Devuelve la representación de solo los átomos de datos reactivos
        en forma de diccionario.

        :return: Dict con {nombre_atomo: valor_actual}.
        """
        data = {}
        for name in self.__class__._atom_names.keys():
            data[name] = getattr(self, name) 
        return data

    def toggle(self, attr: str) -> None:
        """
        Alterna (invierte) el valor de un atributo booleano reactivo.

        :param attr: Nombre del atributo a alternar.
        :raises TypeError: Si el atributo no es booleano.

        Example
        -------
        .. code-block:: python
            vm.toggle("is_playing") 
            # is equal to:
            vm.is_playing = not vm.is_playing
        """
        attr_value = getattr(self, attr)

        # Verificación de Tipo
        if not isinstance(attr_value, bool):
            raise TypeError(
                f"The toggle() method is only valid for Boolean attributes."
                f"'{attr}' is of type {type(attr_value).__name__}."
            )

        setattr(self, attr, not attr_value)

    def reset(self, *attrs: str) -> None:
        """
        Restablece uno o más atributos reactivos a sus valores iniciales
        definidos en la clase.

        :param attrs: Nombres de los atributos a resetear.
        """
        for attr in attrs:
            descriptor = self.__class__.__dict__.get(attr)
            
            if not isinstance(descriptor, ReactiveAtom):
                 # Ignorar computed o métodos regulares
                 continue

            initial_value = descriptor.initial_value
            
            # Usar setattr para forzar la reactividad y notificación
            setattr(self, attr, initial_value)

    def reset_all(self) -> None:
        """
        Restablece todos los átomos reactivos del modelo a su valor inicial.
        """
        attrs = list(self.__class__._atom_names.keys())
        self.reset(*attrs)
