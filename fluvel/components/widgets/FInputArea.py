# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QTextEdit

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs

# Enums
from fluvel.core.enums import Alignment, AlignmentTypes
from fluvel.i18n.I18nTextVar import I18nTextVar


class FInputAreaKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FInputArea."""

    plain_text: str | I18nTextVar
    placeholder: str | I18nTextVar
    read_only: bool
    cursor_position: int
    align: AlignmentTypes

    # Signals
    on_text_changed: Callable[[], None]
    on_selection_changed: Callable[[], None]
    on_cursor_changed: Callable[[], None]
    on_undo: Callable[[bool], None]
    on_redo: Callable[[bool], None]

class FInputArea(QTextEdit, FWidget, FTextWidget):
    """Fluvel Component Class TextArea, wrapping QTextEdit."""

    _BINDABLE_PROPERTY = "plainText"
    _BINDABLE_SIGNAL = "textChanged"

    _QT_PROPERTY_MAP = {
        "plain_text": "setPlainText",
        "placeholder": "setPlaceholderText",
        "read_only": "setReadOnly",
        "cursor_position": "setCursorPosition",
        "align": "setAlignment",
        # Signals
        "on_text_changed": "textChanged",
        "on_undo": "undoAvailable",
        "on_redo": "redoAvailable",
    }

    def __init__(self, **kwargs: Unpack[FInputAreaKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FInputAreaKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)
        kwargs = self._apply_texts(**kwargs)

        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()