# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtWidgets import QSpinBox

StepTypes = Literal["default", "adaptative"]


@final
class StepType:
    DEFAULT = QSpinBox.StepType.DefaultStepType
    ADAPTATIVE = QSpinBox.StepType.AdaptiveDecimalStepType

    __MAP__: dict[StepTypes, QSpinBox.StepType] = {"default": DEFAULT, "adaptative": ADAPTATIVE}

    @staticmethod
    def get(step_type: StepTypes) -> QSpinBox.StepType:
        return StepType.__MAP__.get(step_type, StepType.DEFAULT)
