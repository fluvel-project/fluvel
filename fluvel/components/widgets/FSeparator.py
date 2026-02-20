# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

# PySide6
from PySide6.QtWidgets import QFrame

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import (
    Orientation,
    OrientationTypes,
    Shadow,
    ShadowTypes,
    Shape,
    SizePolicy,
)


class FSeparatorKwargs(FWidgetKwargs, total=False):
    """Argumentos específicos para FSeparator."""

    orientation: OrientationTypes
    shadow: ShadowTypes
    thickness: int


class FSeparator(QFrame, FWidget):
    """
    Componente Separador de Fluvel.
    Envuelve QFrame configurado como una línea de separación.
    """

    _QT_PROPERTY_MAP: dict[str, str] = {"shadow": "setFrameShadow", "thickness": "setLineWidth"}

    def __init__(self, **kwargs: Unpack[FSeparatorKwargs]):
        super().__init__()

        self.orientation = None
        kwargs["thickness"] = kwargs.get("thickness") or 1

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FSeparatorKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)
        if orientation := kwargs.pop("orientation", None):
            orientation = Orientation.get(orientation)

            if orientation == Orientation.HORIZONTAL:
                shape = Shape.get("h_line")
                policy = SizePolicy.get(("preferred", "fixed"))
                self.orientation = "horizontal"
            else:
                shape = Shape.get("v_line")
                policy = SizePolicy.get(("fixed", "preferred"))
                self.orientation = "vertical"

            self.setFrameShape(shape)
            self.setSizePolicy(policy)

        if shadow := kwargs.get("shadow"):
            kwargs["shadow"] = Shadow.get(shadow)

        if thickness := kwargs.pop("thickness", None):
            if self.orientation == "vertical":
                self.setFixedWidth(thickness)
            else:
                self.setFixedHeight(thickness)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        """Establece los valores predeterminados para el separador."""

        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # QFrame's default configuration to be a separator.
        self.setFrameShape(Shape.get("h_line"))
        self.setFrameShadow(Shadow.get("sunken"))
