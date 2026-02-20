# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QSlider

TickPositionTypes = Literal["without", "above", "below", "both-sides", "left", "right"]


@final
class TickPosition:
    NO_TICKS = QSlider.TickPosition.NoTicks
    TICKS_ABOVE = QSlider.TickPosition.TicksAbove
    TICKS_BELOW = QSlider.TickPosition.TicksBelow
    TICKS_BOTH_SIDES = QSlider.TickPosition.TicksBothSides
    TICKS_LEFT = QSlider.TickPosition.TicksLeft
    TICKS_RIGHT = QSlider.TickPosition.TicksRight

    __MAP__: dict[TickPositionTypes, QSlider.TickPosition] = {
        "without": NO_TICKS,
        "above": TICKS_ABOVE,
        "below": TICKS_BELOW,
        "both-sides": TICKS_BOTH_SIDES,
        "left": TICKS_LEFT,
        "right": TICKS_RIGHT,
    }

    @staticmethod
    def get(position: TickPositionTypes) -> QSlider.TickPosition:
        return TickPosition.__MAP__.get(position, TickPosition.NO_TICKS)
