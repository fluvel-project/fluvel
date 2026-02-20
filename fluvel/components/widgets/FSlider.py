# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QSlider

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import (
    Cursor,
    Orientation,
    OrientationTypes,
    TickPosition,
    TickPositionTypes,
)


class FSliderKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FSlider."""

    inverted_appearance: bool
    inverted_controls: bool
    range: tuple[int, int]
    max: int
    min: int
    orientation: OrientationTypes
    page_step: int
    single_step: int
    slider_down: int
    slider_position: int
    tracking: bool
    value: int
    tick_interval: int
    tick_position: TickPositionTypes

    on_changed: Callable[[int], None]
    on_range_changed: Callable[[int, int], None]
    on_moved: Callable[[int], None]
    on_released: Callable[[], None]

class FSlider(QSlider, FWidget):
    """Fluvel Component Class Slider, wrapping QSlider."""

    _BINDABLE_PROPERTY = "value"
    _BINDABLE_SIGNAL = "valueChanged"

    _QT_PROPERTY_MAP = {
        "inverted_appearance": "setInvertedAppearance",
        "inverted_controls": "setInvertedControls",
        "range": "setRange",
        "max": "setMaximum",
        "min": "setMinimum",
        "orientation": "setOrientation",
        "page_step": "setPageStep",
        "single_step": "setSingleStep",
        "slider_down": "setSliderDown",
        "slider_position": "setSliderPosition",
        "tracking": "setTracking",
        "value": "setValue",
        "tick_interval": "setTickInterval",
        "tick_position": "setTickPosition",
        # Signals
        "on_changed": "valueChanged",
        "on_range_changed": "rangeChanged",
        "on_moved": "sliderMoved",
        "on_released": "sliderReleased"
    }

    def __init__(self, **kwargs: Unpack[FSliderKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FSliderKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)
        if orientation := kwargs.get("orientation"):
            kwargs["orientation"] = Orientation.get(orientation)

        if tick_position := kwargs.get("tick_position"):
            kwargs["tick_position"] = TickPosition.get(tick_position)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # Specific Qt configuration (e.g., setFocusPolicy)
        self.setRange(0, 100)

        self.setCursor(Cursor.get("pointing_hand"))
