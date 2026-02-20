# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import threading
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ClassVar, Self, dataclass_transform, get_origin, get_type_hints
from fluvel.reactive.pyro.rules import Rule

local = threading.local()
local.stack = []


@dataclass(slots=True, frozen=True)
class ComputedData:
    func: Callable


@dataclass(slots=True, frozen=True)
class ReactionData:
    func: Callable
    deps: set[str]
    lazy: bool


@dataclass(slots=True, frozen=True)
class EffectData:
    func: Callable
    when: Rule


def computed(func):
    return ComputedData(func)

def reaction(*atoms: str, lazy: bool = False):
    def decorator(fn):
        return ReactionData(fn, set(atoms), lazy)
    return decorator

def effect(when: Rule):
    def decorator(fn):
        return EffectData(fn, when)
    return decorator


@dataclass(slots=True, frozen=True)
class Atom:
    name: str
    origin_key: str
    default: Any
    base_type: type

    def __get__(self, model, _) -> Any:
        if local.stack and not model._is_listening(self.name, local.stack[-1]):
            model._add_listener(self.name, local.stack[-1])

        return getattr(model, self.origin_key, self.default)

    def __set__(self, model, value) -> Any:
        if value == getattr(model, self.origin_key):
            return

        setattr(model, self.origin_key, value)
        model.notify(self.name, value)


@dataclass(slots=True, frozen=True)
class ComputedAtom:
    name: str
    func: Callable

    def __get__(self, model, _):
        local.stack.append(self.name)
        try:
            new_value = self.func(model)
        finally:
            local.stack.pop()
        return new_value

    def __set__(self, *_):
        raise AttributeError(f"Cannot overwrite computed '{self.name}'.")


@dataclass(slots=True, frozen=True)
class Effect:
    name: str
    func: Callable
    when: Rule

    def __get__(self, model, _):
        local.stack.append(self.name)
        try:
            should_run = self.when(model)
        finally:
            local.stack.pop()

        if should_run:
            self.func(model)

    def __set__(self, *_):
        raise AttributeError(f"Cannot set effect '{self.name}'.")


@dataclass(slots=True, frozen=True)
class Reaction:
    name: str
    func: Callable
    deps: set[str]
    lazy: bool

    def __get__(self, model, _):
        self.func(model)

    def __set__(self, *_):
        raise AttributeError(f"Cannot overwrite reaction '{self.name}'.")


@dataclass(slots=True, frozen=True)
class CollectionAtom(Atom):
    def make_reactive(self, model, value):
        if self.base_type is list:
            wrapper = PyroList
        elif self.base_type is dict:
            wrapper = PyroDict
        elif self.base_type is set:
            wrapper = PyroSet
        else:
            raise TypeError(
                f"Expected type (list, dict, set) for CollectionAtom '{self.name}', but got '{self.base_type.__name__}'. "
                f"Check the type annotation for this attribute."
            )

        return wrapper(model, self.name, value)

    def __set__(self, model, value):
        value = self.make_reactive(model, value)
        Atom.__set__(self, model, value)


def reactive_conversion(fn):
    def wrapped_method(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        self._notify()
        return result
    return wrapped_method


@dataclass
class PyroCollection:
    model: "Origin"
    name: str
    _MUTATORS: ClassVar[list[str]]

    def __init_subclass__(cls):
        for mutator in cls._MUTATORS:
            original_method = getattr(cls, mutator)
            wrapped_method = reactive_conversion(original_method)
            setattr(cls, mutator, wrapped_method)

    def _notify(self):
        self.model.notify(self.name, self)

class PyroList(list, PyroCollection):
    _MUTATORS = [
        "__setitem__",
        "__delitem__",
        "__iadd__",
        "append",
        "extend",
        "pop",
        "remove",
        "clear",
        "reverse",
        "sort",
        "insert",
    ]

    def __init__(self, model, name, iterable=()):
        super().__init__(iterable)
        PyroCollection.__init__(self, model, name)

class PyroDict(dict, PyroCollection):
    _MUTATORS = ["__setitem__", "__delitem__", "pop", "popitem", "clear", "update"]

    def __init__(self, model, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        PyroCollection.__init__(self, model, name)

    def setdefault(self, key: Any, default: Any = None):
        if key not in self:
            val = super().setdefault(key, default)
            self._notify()
            return val
        return super().setdefault(key, default)


class PyroSet(set, PyroCollection):
    _MUTATORS = [
        "clear",
        "pop",
        "remove",
        "update",
        "intersection_update",
        "difference_update",
        "symmetric_difference_update",
        "__ior__",
        "__iand__",
        "__isub__",
        "__ixor__",
    ]

    def __init__(self, model, name, iterable=()):
        super().__init__(iterable)
        PyroCollection.__init__(self, model, name)

    def add(self, element: Any):
        if element not in self:
            super().add(element)
            self._notify()

    def discard(self, element: Any):
        if element in self:
            super().discard(element)
            self._notify()

@dataclass_transform(kw_only_default=True)
class Origin:
    __batching: bool = False

    def __init_subclass__(cls, **kwargs):
        if kwargs.get("is_base"):
            return

        cls._atom_names: dict[str, str] = {}
        cls._computeds: list[str] = []
        cls._subscriptions: list[str] = []
        cls._effects: list[str] = []

        # We need the type annotations for each defined attribute
        # in the models to filter out what's useful in the next line of code
        annotations = get_type_hints(cls)

        # We filter only the names of public attributes, that is,
        # the atomic states declared in the class body,
        # the computed states, subscriptions, and public methods
        # (although the latter will not be processed)
        names = {n: None for n in annotations | vars(cls) if not n.startswith("_")}

        for name in names:
            value = getattr(cls, name, None)

            if callable(value):
                continue

            if isinstance(value, ComputedData):
                setattr(cls, name, ComputedAtom(name, value.func))
                cls._computeds.append(name)

            elif isinstance(value, ReactionData):
                setattr(cls, name, Reaction(name, value.func, value.deps, value.lazy))
                cls._subscriptions.append(name)

            elif isinstance(value, EffectData):
                setattr(cls, name, Effect(name, value.func, value.when))
                cls._effects.append(name)

            else:
                origin_key = f"_origin_{name}"
                var_type = annotations.get(name)
                base_type = get_origin(var_type) or var_type
                default = value or (base_type() if isinstance(base_type, type) else None)

                if base_type in (list, dict, set):
                    atom = CollectionAtom(name, origin_key, default, base_type)
                else:
                    atom = Atom(name, origin_key, default, base_type)

                setattr(cls, name, atom)
                cls._atom_names[name] = origin_key

    def __init__(self, **kwargs):

        self.__batching = False
        self._listeners: dict[str, set[str]] = {}

        # Optional hook to customize
        # storage mode, system
        # notifications, or anything else
        # on base models that inherit from Origin
        self.__awake__()

        for name, origin_key in type(self)._atom_names.items():
            atom = type(self).__dict__[name]
            initial_value = kwargs.get(name, atom.default)
            if isinstance(atom, CollectionAtom):
                initial_value = atom.make_reactive(self, initial_value)
            setattr(self, origin_key, initial_value)

        # Dependency registration for subscriptions
        for sub_name in type(self)._subscriptions:
            sub = type(self).__dict__[sub_name]
            for d in sub.deps:
                self._add_listener(d, sub.name)

        self.__post_init__()

    def _add_listener(self, atom_name: str, listener: str):
        self._listeners.setdefault(atom_name, set()).add(listener)

    def _is_listening(self, atom_name: str, listener: str) -> bool:
        return listener in self._listeners.get(atom_name, {})

    def sync(self) -> Self:

        for effect_name in type(self)._effects:
            getattr(self, effect_name)
        
        for computed_name in type(self)._computeds:
            getattr(self, computed_name)

        for sub_name in type(self)._subscriptions:
            sub = type(self).__dict__[sub_name]
            if not sub.lazy:
                getattr(self, sub_name)
                
        return self

    def to_dict(self) -> dict[str, Any]:
        return {n: getattr(self, n) for n in type(self)._atom_names}

    def update(self, data: dict[str, Any] = None, **kwargs) -> None:
        update_data = (data or {}) | kwargs

        with self.batch():
            for name, val in update_data.items():
                if name not in type(self)._atom_names:
                    continue
                setattr(self, name, val)

    def reset(self, *atoms: str) -> None:
        for atom in atoms:
            descriptor = type(self).__dict__.get(atom)
            if not isinstance(descriptor, Atom):
                continue
            setattr(self, atom, descriptor.default)

    def reset_all(self) -> None:
        self.reset(*type(self)._atom_names)

    def toggle(self, atom: str) -> None:
        attr_value = getattr(self, atom)
        if not isinstance(attr_value, bool):
            raise TypeError(
                f"The toggle() method is only valid for Boolean attributes."
                f"'{atom}' is type {type(attr_value).__name__}"
            )
        setattr(self, atom, not attr_value)

    def __repr__(self) -> str:
        params = [f"{n}={repr(getattr(self, n))}" for n in type(self)._atom_names]
        return f"{type(self).__name__}({', '.join(params)})"

    def notify(self, atom_name: str, new_value: Any):
        changes = {atom_name: new_value}
        if listeners := self._listeners.get(atom_name):
            changes.update({key: getattr(self, key) for key in listeners})

        self.emit(changes)

    @contextmanager
    def batch(self) -> Generator[None, None, None]:

        if self.__batching:
            yield
            return

        original_notify = self.notify
        atoms_changed: set[str] = set()

        def batch_notify(atom_name: str, _new_value: Any):
            atoms_changed.add(atom_name)

        def recalculate_and_emit():

            if not atoms_changed:
                return

            final_package = {}

            for atom_name in atoms_changed:
                final_package[atom_name] = getattr(self, atom_name)
                if listeners := self._listeners.get(atom_name):
                    final_package.update({key: getattr(self, key) for key in listeners})

            self.emit(final_package)

        # Monkey Patching
        self.notify = batch_notify
        self.__batching = True

        try:
            yield
        finally:
            self.notify = original_notify
            self.__batching = False
            recalculate_and_emit()

    def emit(self, changes: dict[str, Any]) -> None:
        pass

    def __awake__(self) -> None:
        pass

    def __post_init__(self) -> None:
        pass

# --- README ---

# [TODO's] Implementations scheduled for very soon versions.

# [NOTE] Author's note on this first version:
#   Most of the implementations mentioned below were already developed
#   in the initial (non-public) versions of Pyro, which I used as a basis for building
#   and optimizing Pyro and Origin. I didn't include them in the first official version
#   to keep the core "pure" (minimalist) and readable across all classes. Essentially, everything else
#   consists of optimization systems that inject conditional logic, validations, and new data structures
#   to guide the flow of the Reactive System toward optimal behavior.

# [TODO] (already developed)
# In later versions, a system for caching computed properties
# will be implemented to avoid recalculation caused by the descriptor protocol (__get__).

# [TODO] (not developed)
# Currently, methods decorated with @reaction execute synchronously.
# In the future, these could execute in a separate thread or using a
# dedicated system that provides an asynchronous execution context.
# For a Beta, executing the dependency synchronously is sufficient and ideal.

# [TODO] (already developed, but could be extended)
# Dynamic dependency tracking.
# A dynamic dependency tracking system is a system
# that automatically identifies the atoms dependent on a computed property
# to dynamically build dependency graphs linked to those atoms.
# Currently, Pyro already implements this automatic tracking system through
# local.stack and Origin._add_listener(); however, the graph is static
# throughout the model's lifecycle, meaning that no matter the number
# of base atoms used within a computed property, if they were read at least once,
# they will remain as fixed triggers for the computed property's reactivity
# To complete this system, an intelligent mechanism needs to be implemented
# that allows/prevents notifications from being passed to computed properties upon change.
# This could be a simple constant rebuild of the Set[str] Origin._listeners at runtime
# or experimental mechanisms.
# PS: This could become secondary, since for most use cases, a cumulative graph is perfectly acceptable
# and avoids the overhead of rebuilding the set on each access.

# More Future-Oriented TODO's
# * Deep Reactivity
# * Connectivity Between Models