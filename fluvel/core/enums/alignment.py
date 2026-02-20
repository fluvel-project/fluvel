# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtCore import Qt

AlignmentTypes = Literal[
    "none",
    "top",
    "bottom",
    "right",
    "left",
    "center",
    "h-center",
    "v-center",
    "justify",
    "baseline",
    "top-left",
    "top-right",
    "bottom-left",
    "bottom-right",
    "center-top",
    "center-right",
    "center-bottom",
    "center-left",
]


@final
class Alignment:
    NONE = Qt.AlignmentFlag(0)

    # Alingment Flags
    TOP = Qt.AlignmentFlag.AlignTop
    BOTTOM = Qt.AlignmentFlag.AlignBottom
    RIGHT = Qt.AlignmentFlag.AlignRight
    LEFT = Qt.AlignmentFlag.AlignLeft
    CENTER = Qt.AlignmentFlag.AlignCenter
    H_CENTER = Qt.AlignmentFlag.AlignHCenter
    V_CENTER = Qt.AlignmentFlag.AlignVCenter

    # Combinations
    TOP_LEFT = TOP | LEFT
    TOP_RIGHT = TOP | RIGHT
    BOTTOM_LEFT = BOTTOM | LEFT
    BOTTOM_RIGHT = BOTTOM | RIGHT
    CENTER_TOP = TOP | H_CENTER
    CENTER_RIGHT = RIGHT | V_CENTER
    CENTER_BOTTOM = BOTTOM | H_CENTER
    CENTER_LEFT = LEFT | V_CENTER

    # Others
    ABSOLUTE = Qt.AlignmentFlag.AlignAbsolute
    BASELINE = Qt.AlignmentFlag.AlignBaseline
    LEADING = Qt.AlignmentFlag.AlignLeading
    TRAILING = Qt.AlignmentFlag.AlignTrailing
    HORIZONTAL_MASK = Qt.AlignmentFlag.AlignHorizontal_Mask
    VERTICAL_MASK = Qt.AlignmentFlag.AlignVertical_Mask
    JUSTIFY = Qt.AlignmentFlag.AlignJustify

    __MAP__: dict[AlignmentTypes, Qt.AlignmentFlag] = {
        "none": NONE,
        "top": TOP,
        "bottom": BOTTOM,
        "right": RIGHT,
        "left": LEFT,
        "center": CENTER,
        "h-center": H_CENTER,
        "v-center": V_CENTER,
        "justify": JUSTIFY,
        "baseline": BASELINE,
        "top-left": TOP_LEFT,
        "top-right": TOP_RIGHT,
        "bottom-left": BOTTOM_LEFT,
        "bottom-right": BOTTOM_RIGHT,
        "center-top": CENTER_TOP,
        "center-right": CENTER_RIGHT,
        "center-bottom": CENTER_BOTTOM,
        "center-left": CENTER_LEFT,
    }

    @staticmethod
    def get(alignment: AlignmentTypes) -> Qt.AlignmentFlag:
        return Alignment.__MAP__.get(alignment, Alignment.NONE)
