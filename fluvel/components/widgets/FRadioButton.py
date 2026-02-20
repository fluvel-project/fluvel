# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QRadioButton

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.i18n.I18nTextVar import I18nTextVar


class FRadioButtonKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FRadioButton."""
    text: str | I18nTextVar
    checkable: bool
    checked: bool
    icon: QIcon
    icon_size: tuple[int, int]

    # Signals
    on_click: Callable[[], None]
    on_pressed: Callable[[], None]
    on_released: Callable[[], None]
    on_toggled: Callable[[bool], None]

class FRadioButton(QRadioButton, FWidget, FTextWidget):
    """Fluvel Component Class RadioButton, wrapping QRadioButton."""

    _BINDABLE_PROPERTY = "checked"
    _BINDABLE_SIGNAL = "toggled"

    _QT_PROPERTY_MAP = {
        "text": "setText",
        "checkable": "setCheckable",
        "checked": "setChecked",
        "icon": "setIcon",
        "icon_size": "setIconSize",
        # Signals
        "on_click": "clicked",
        "on_pressed": "pressed",
        "on_released": "released",
        "on_toggled": "toggled"
    }

    def __init__(self, **kwargs: Unpack[FRadioButtonKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FRadioButtonKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)
        kwargs = self._apply_texts(**kwargs)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # Specific Qt configuration (e.g., setFocusPolicy)
        # ...
