# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TypedDict, Unpack

from PySide6.QtGui import QAction

# PySide6
from PySide6.QtWidgets import QWidget

# Fluvel
from fluvel.i18n.I18nTextVar import I18nMenuTextVar


class FActionKwargs(TypedDict, total=False):
    text: str | I18nMenuTextVar


class FAction(QAction):
    _MAPPING_METHODS = {"text": "setText"}

    def __init__(self, parent: QWidget, **kwargs: Unpack[FActionKwargs]) -> None:
        super().__init__(parent)

        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FActionKwargs]) -> None:
        if text := kwargs.get("text"):
            if isinstance(text, I18nMenuTextVar):
                text.setParent(self)
                text.valueChanged.connect(self.setText)
                text = text.value

            self.setText(text)
