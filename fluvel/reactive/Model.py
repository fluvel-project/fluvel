# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Any

# PySide6
from PySide6.QtCore import QMetaMethod, QObject, Signal

from fluvel.reactive.pyro.exceptions import ModelCreationError

# Pyro
from fluvel.reactive.pyro.Origin import Origin


class ModelStore:
    __store__: dict[str, "Model"] = {}

    @classmethod
    def add_model(cls, model: "Model", ref: str) -> None:
        if ref in cls.__store__:
            old_model = cls.__store__[ref]

            model_name = type(model).__qualname__
            old_model_name = type(old_model).__qualname__

            if model_name == old_model_name:
                model.update(old_model.to_dict())
            else:
                model_path = f"{type(model).__module__}.{model_name}"
                old_path = f"{type(old_model).__module__}.{old_model_name}"
                raise ModelCreationError(
                    f"Alias Collision: '{ref}' is bound to <{old_path}>. "
                    f"Cannot reassign to <{model_path}>."
                )
        cls.__store__[ref] = model

    @classmethod
    def get_model(cls, ref: str) -> "Model":
        model = cls.__store__.get(ref)
        if model is None:
            raise ValueError(f"There is no model with the ref '{ref}' or it was destroyed.")
        return model

    @classmethod
    def remove_model(cls, ref: str) -> None:
        if ref in cls.__store__:
            del cls.__store__[ref]


class ModelEmitter(QObject):
    modelChanged = Signal(dict)
    

class Model(Origin, is_base=True):
    ref: str

    def __awake__(self):
        self.qt_emitter = ModelEmitter()
        ModelStore.add_model(self, self.__ref__)

    def __init__(self, *, ref: str, **kwargs):

        if type(ref) is not str:
            raise ModelCreationError(
                f"Invalid ref '{ref}: {type(ref).__name__}'. Expected 'str'."
            )

        self.__ref__: str = ref

        if ref in ModelStore.__store__:
            old_model = ModelStore.get_model(ref)
            kwargs = old_model.to_dict() | kwargs

        # Origin.__init__
        super().__init__(**kwargs)

    def clear(self):
        self._listeners.clear()

    def update(self, data: dict[str, Any] = None, **kwargs) -> None:
        update_data = (data or {}) | kwargs
        atoms = type(self)._atom_names
        
        with self.batch():
            for name, val in update_data.items():
                if name not in atoms:
                    continue

                if not hasattr(self, atoms[name]):
                    setattr(self, atoms[name], None)

                setattr(self, name, val)

    def unbind(self):
        method = QMetaMethod.fromSignal(self.qt_emitter.modelChanged)
        if self.qt_emitter.isSignalConnected(method):
            self.qt_emitter.modelChanged.disconnect()

    def destroy(self):
        self.clear()
        self.unbind()
        ModelStore.remove_model(self.__ref__)

    def emit(self, changes):
        self.qt_emitter.modelChanged.emit(changes)