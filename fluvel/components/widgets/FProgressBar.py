# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QProgressBar

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import (
    Alignment,
    AlignmentTypes,
    Orientation,
    OrientationTypes,
    TextDirection,
    TextDirectionTypes,
)


class FProgressBarKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FProgressBar."""

    align: AlignmentTypes
    format: str | list[str]
    inverted_appearance: bool
    range: tuple[int, int]
    max: int
    min: int
    orientation: OrientationTypes
    text_direction: TextDirectionTypes
    text_visible: bool
    value: int

    # Signals
    on_changed: Callable[[int], None]


class FProgressBar(QProgressBar, FWidget, FTextWidget):
    """Fluvel Component Class ProgressBar, wrapping QProgressBar."""

    _BINDABLE_PROPERTY = "value"
    _BINDABLE_SIGNAL = "valueChanged"

    _QT_PROPERTY_MAP = {
        "align": "setAlignment",
        "format": "setFormat",
        "inverted_appearance": "setInvertedAppearance",
        "range": "setRange",
        "max": "setMaximum",
        "min": "setMinimum",
        "orientation": "setOrientation",
        "text_direction": "setTextDirection",
        "text_visible": "setTextVisible",
        "value": "setValue",
        # Signals
        "on_changed": "valueChanged"
    }

    def __init__(self, **kwargs: Unpack[FProgressBarKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FProgressBarKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        if orientation := kwargs.get("orientation"):
            kwargs["orientation"] = Orientation.get(orientation)

        if text_direction := kwargs.get("text_direction"):
            kwargs["text_direction"] = TextDirection.get(text_direction)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # Specific Qt configuration (e.g., setFocusPolicy)
        self.setRange(0, 100)
