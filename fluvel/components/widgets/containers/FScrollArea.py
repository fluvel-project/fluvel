# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

# PySide6
from PySide6.QtWidgets import QScrollArea

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums.alignment import Alignment, AlignmentTypes


class FScrollAreaKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FScrollArea."""

    # Define the specific arguments for the widget here (e.g., text: str)
    align: AlignmentTypes
    resizable: bool


class FScrollArea(QScrollArea, FWidget):
    """Fluvel Component Class ScrollArea, wrapping QScrollArea."""

    _BINDABLE_PROPERTY = None
    _BINDABLE_SIGNAL = None

    _QT_PROPERTY_MAP = {"align": "setAlignment", "resizable": "setWidgetResizable"}

    def __init__(self, **kwargs: Unpack[FScrollAreaKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FScrollAreaKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)
        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()
        self.setWidgetResizable(True)
