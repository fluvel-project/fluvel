from typing import Literal

# PySide6
from PySide6.QtCore import Qt

AlignmentTypes = Literal[
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
    "center-left"
]

class Alignment:

    # Alingment Flags
    TOP             = Qt.AlignmentFlag.AlignTop
    BOTTOM          = Qt.AlignmentFlag.AlignBottom
    RIGHT           = Qt.AlignmentFlag.AlignRight
    LEFT            = Qt.AlignmentFlag.AlignLeft
    CENTER          = Qt.AlignmentFlag.AlignCenter
    H_CENTER        = Qt.AlignmentFlag.AlignHCenter
    V_CENTER        = Qt.AlignmentFlag.AlignVCenter
    JUSTIFY         = Qt.AlignmentFlag.AlignJustify
    BASELINE        = Qt.AlignmentFlag.AlignBaseline

    # Combinations
    TOP_LEFT        = TOP | LEFT
    TOP_RIGHT       = TOP | RIGHT
    BOTTOM_LEFT     = BOTTOM | LEFT
    BOTTOM_RIGHT    = BOTTOM | RIGHT
    CENTER_TOP      = TOP | H_CENTER
    CENTER_RIGHT    = RIGHT | V_CENTER
    CENTER_BOTTOM   = BOTTOM | H_CENTER
    CENTER_LEFT     = LEFT | V_CENTER

    ALIGNMENT_MAP: dict = {
        "top":  TOP,
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
        "center-left": CENTER_LEFT
    }

    @classmethod
    def get(cls, alignment: AlignmentTypes) -> Qt.AlignmentFlag:

        return cls.ALIGNMENT_MAP.get(alignment, cls.CENTER)