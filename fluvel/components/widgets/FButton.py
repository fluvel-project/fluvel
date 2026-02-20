# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QMenu, QPushButton

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.i18n.I18nTextVar import I18nTextVar


class FButtonKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FButton."""

    text: str | I18nTextVar
    checkable: bool
    icon: QIcon
    icon_size: int
    shortcut: str
    is_default: bool
    auto_default: bool
    flat: bool
    menu: QMenu

    # Signals
    on_click: Callable[[], None]
    on_pressed: Callable[[], None]
    on_released: Callable[[], None]
    on_toggled: Callable[[bool], None]


class FButton(QPushButton, FWidget, FTextWidget):
    """Fluvel's Button component class, wrapping QPushButton."""

    _BINDABLE_PROPERTY = None
    _BINDABLE_SIGNAL = "clicked"

    _QT_PROPERTY_MAP: dict = {
        "text": "setText",
        "checkable": "setCheckable",
        "icon": "setIcon",
        "icon_size": "setIconSize",
        "enabled": "setEnabled",
        "shortcut": "setShortcut",
        "is_default": "setDefault",
        "auto_default": "setAutoDefault",
        "flat": "setFlat",
        "menu": "setMenu",
        # Signals
        "on_click": "clicked",
        "on_pressed": "pressed",
        "on_released": "released",
        "on_toggled": "toggled",
    }

    def __init__(self, **kwargs: Unpack[FButtonKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FButtonKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if icon_size := kwargs.get("icon_size"):
            kwargs["icon_size"] = QSize(icon_size, icon_size)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # By default, the cursor is PointingHang
        self.setCursor(Qt.PointingHandCursor)
