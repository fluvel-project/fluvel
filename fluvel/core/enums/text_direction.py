# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QProgressBar

TextDirectionTypes = Literal["bottom-to-top", "top-to-bottom"]


@final
class TextDirection:
    BOTTOM_TO_TOP = QProgressBar.Direction.BottomToTop
    TOP_TO_BOTTOM = QProgressBar.Direction.TopToBottom

    __MAP__: dict[TextDirectionTypes, QProgressBar.Direction] = {
        "bottom-to-top": BOTTOM_TO_TOP,
        "top-to-bottom": TOP_TO_BOTTOM,
    }

    @staticmethod
    def get(text_direction: TextDirectionTypes) -> QProgressBar.Direction:
        return TextDirection.__MAP__.get(text_direction, TextDirection.BOTTOM_TO_TOP)
