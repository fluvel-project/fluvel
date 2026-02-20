# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Any

# PySide6
from PySide6.QtCore import QObject, Signal

# Fluvel I18n
from fluvel.i18n.I18nProvider import I18nProvider


class I18nBaseTextBar(QObject):
    valueChanged = Signal(str)

    def __init__(self, id: str, placeholders: dict[str, Any] = None):
        super().__init__()
        self._id = id
        self._placeholders = placeholders
        self.refresh()

    def refresh(self) -> None:
        new_value = self.get_by_id()
        if self._placeholders:
            new_value = new_value.format_map(self._placeholders)
        self.value = new_value
        self.valueChanged.emit(new_value)

    def replace(self, **placeholders) -> None:
        self._placeholders = placeholders
        self.refresh()


class I18nTextVar(I18nBaseTextBar):
    def get_by_id(self) -> str:
        return I18nProvider.get_text(self._id, "")


class I18nMenuTextVar(I18nBaseTextBar):
    def get_by_id(self) -> str:
        return I18nProvider.get_menu(self._id, "")
