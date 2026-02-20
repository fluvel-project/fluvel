# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QLineEdit

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs

# Fluvel core utils
from fluvel.core.enums import Alignment, AlignmentTypes, EchoMode, EchoModeTypes
from fluvel.i18n.I18nTextVar import I18nTextVar


class FInputKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FInput."""

    text: str | I18nTextVar
    placeholder: str | I18nTextVar
    align: AlignmentTypes
    frame: bool
    mode: EchoModeTypes
    read_only: bool
    clear_button: bool
    max_length: int
    mask: str

    # Signals
    on_returns: Callable[[], None]
    on_edit: Callable[[str], None]
    on_finish: Callable[[], None]
    on_text_changed: Callable[[str], None]

class FInput(QLineEdit, FWidget, FTextWidget):
    """Fluvel's Input component class, wrapping QLineEdit."""

    _BINDABLE_PROPERTY = "text"
    _BINDABLE_SIGNAL = "textChanged"

    _QT_PROPERTY_MAP = {
        "text": "setText",
        "placeholder": "setPlaceholderText",
        "align": "setAlignment",
        "frame": "setFrame",
        "mode": "setEchoMode",
        "read_only": "setReadOnly",
        "clear_button": "setClearButtonEnabled",
        "max_length": "setMaxLength",
        "mask": "setInputMask",
        "on_returns": "returnPressed",
        "on_edit": "textEdited",
        "on_finish": "editingFinished",
        "on_text_changed": "textChanged"
    }

    def __init__(self, **kwargs: Unpack[FInputKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FInputKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        if mode := kwargs.get("mode"):
            kwargs["mode"] = EchoMode.get(mode)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # Specific Qt configuration (e.g., setFocusPolicy)
        # ...
