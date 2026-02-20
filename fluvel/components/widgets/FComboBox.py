# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QComboBox

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.i18n.I18nTextVar import I18nTextVar


class FComboBoxKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FComboBox."""

    items: list[str]
    editable: bool
    max_visible: int
    placeholder: str | I18nTextVar
    current_index: int
    current_text: str

    # Signals
    on_select: Callable[[int], None]
    on_changed: Callable[[str], None]


class FComboBox(QComboBox, FWidget, FTextWidget):
    """Fluvel Component Class ComboBox, wrapping QComboBox."""

    _BINDABLE_PROPERTY = "currentText"
    _BINDABLE_SIGNAL = "currentTextChanged"

    _QT_PROPERTY_MAP = {
        "items": "addItems",
        "editable": "setEditable",
        "max_visible": "setMaxVisible",
        "placeholder": "setPlaceholderText",
        "current_index": "setCurrentIndex",
        "current_text": "setCurrentText",
        "on_select": "currentIndexChanged",
        "on_changed": "currentTextChanged",
    }

    def __init__(self, **kwargs: Unpack[FComboBoxKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FComboBoxKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if items := kwargs.pop("items", None):
            self.clear()
            self.addItems(items)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()
