# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QGroupBox

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums.alignment import Alignment, AlignmentTypes


class FGroupBoxKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FGroupBox."""

    # Define the specific arguments for the widget here (e.g., text: str)
    title: str | list[str]
    checkable: bool
    checked: bool
    flat: bool
    align: AlignmentTypes

    # Signals
    on_click: Callable
    toggled: Callable


class FGroupBox(QGroupBox, FWidget, FTextWidget):
    """Fluvel Component Class GroupBox, wrapping QGroupBox."""

    _BINDABLE_PROPERTY = None
    _BINDABLE_SIGNAL = None

    _QT_PROPERTY_MAP = {
        "title": "setTitle",
        "checkable": "setCheckable",
        "checked": "setChecked",
        "flat": "setFlat",
        "align": "setAlignment",
        "on_click": "clicked",
        "on_toggled": "toggled",
    }

    def __init__(self, **kwargs: Unpack[FGroupBoxKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FGroupBoxKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if align := kwargs.pop("align", None):
            kwargs["align"] = Alignment.get(align)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # Specific Qt configuration (e.g., setFocusPolicy)
        # ...
