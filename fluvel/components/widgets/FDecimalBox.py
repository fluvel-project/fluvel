# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

# PySide6
from PySide6.QtWidgets import QDoubleSpinBox

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import Alignment, AlignmentTypes, StepType, StepTypes


class FDecimalBoxKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FDecimalBox."""

    value: float
    min: float
    max: float
    range: tuple[float, float]
    prefix: str
    suffix: str
    step: float
    step_type: StepTypes
    decimals: int
    align: AlignmentTypes

    # Signals
    on_text_changed: Callable[[str], None]
    on_value_changed: Callable[[int], None]


class FDecimalBox(QDoubleSpinBox, FWidget):
    """Fluvel Component Class DoubleSpinBox, wrapping QDoubleSpinBox."""

    _BINDABLE_PROPERTY = "value"
    _BINDABLE_SIGNAL = "valueChanged"

    _QT_PROPERTY_MAP = {
        "value": "setValue",
        "min": "setMinimum",
        "max": "setMaximum",
        "range": "setRange",
        "prefix": "setPrefix",
        "suffix": "setSuffix",
        "step": "setSingleStep",
        "step_type": "setStepType",
        "decimals": "setDecimals",
        "align": "setAlignment",
        # Signals
        "on_text_changed": "textChanged",
        "on_value_changed": "valueChanged",
    }

    def __init__(self, **kwargs: Unpack[FDecimalBoxKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FDecimalBoxKwargs]) -> None:
        # 1. Perform specific type conversions (e.g., Alignment.get)

        if step_type := kwargs.get("step_type"):
            kwargs["step_type"] = StepType.get(step_type)

        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()
        self.setRange(0.0, 100.0)
        self.setDecimals(2)
