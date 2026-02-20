# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QCheckBox

# Fluvel
from fluvel.core.abstract.FTextWidget import FTextWidget
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import CheckState, CheckStateTypes, Cursor
from fluvel.i18n.I18nTextVar import I18nTextVar


class FCheckBoxKwargs(FWidgetKwargs, total=False):
    text: str | I18nTextVar
    size: tuple[int, int]
    checkable: bool
    checked: bool
    checkstate: CheckStateTypes

    on_click: Callable[[], None]
    on_toggled: Callable[[bool], None]
    on_pressed: Callable[[], None]
    on_released: Callable[[], None]
    on_changed: Callable[[int], None]

class FCheckBox(QCheckBox, FTextWidget, FWidget):
    _BINDABLE_PROPERTY = "checked"
    _BINDABLE_SIGNAL = "toggled"

    _QT_PROPERTY_MAP = {
        "text": "setText", 
        "size": "setFixedSize", 
        "checkable": "setCheckable",
        "checked": "setChecked",
        "checkstate": "setCheckState",
        "on_click": "clicked",
        "on_toggled": "toggled",
        "on_pressed": "pressed",
        "on_released": "released",
        "on_changed": "checkStateChanged"
    }

    def __init__(self, **kwargs: Unpack[FCheckBoxKwargs]):
        super().__init__()
        self._set_defaults()
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FCheckBoxKwargs]) -> None:
        kwargs = self._apply_texts(**kwargs)
        if checkstate := kwargs.get("checkstate"):
            kwargs["checkstate"] = CheckState.get(checkstate)
        super().configure(**kwargs)

    def _set_defaults(self):
        super()._set_defaults()
        self.setCursor(Cursor.POINTING_HAND)