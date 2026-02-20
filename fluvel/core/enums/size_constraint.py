# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtWidgets import QLayout

SizeConstraintTypes = Literal[
    "default",
    "none",
    "min-and-max",
    "fixed",
    "minimum",
    "maximum"
]


@final
class SizeConstraint:

    DEFAULT = QLayout.SizeConstraint.SetDefaultConstraint
    NONE = QLayout.SizeConstraint.SetNoConstraint
    MIN_AND_MAX = QLayout.SizeConstraint.SetMinAndMaxSize
    FIXED = QLayout.SizeConstraint.SetFixedSize
    MINIMUM = QLayout.SizeConstraint.SetMinimumSize
    MAXIMUM = QLayout.SizeConstraint.SetMaximumSize

    __MAP__: dict[SizeConstraintTypes, QLayout.SizeConstraint] = {
        "default": DEFAULT,
        "none": NONE,
        "min-and-max": MIN_AND_MAX,
        "fixed": FIXED,
        "minimum": MINIMUM,
        "maximum": MAXIMUM,
    }

    @staticmethod
    def get(constraint: SizeConstraintTypes) -> QLayout.SizeConstraint:
        return SizeConstraint.__MAP__.get(constraint, SizeConstraint.DEFAULT)