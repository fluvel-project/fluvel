# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QFrame

ShapeTypes = Literal[
    "box",
    "no_frame",
    "panel",
    "styled_panel",
    "win_panel",
    "h_line",
    "v_line",
]


@final
class Shape:
    BOX = QFrame.Shape.Box
    H_LINE = QFrame.Shape.HLine
    V_LINE = QFrame.Shape.VLine
    NO_FRAME = QFrame.Shape.NoFrame
    PANEL = QFrame.Shape.Panel
    STYLED_PANEL = QFrame.Shape.StyledPanel
    WIN_PANEL = QFrame.Shape.WinPanel

    __MAP__: dict[ShapeTypes, QFrame.Shape] = {
        "box": BOX,
        "no_frame": NO_FRAME,
        "panel": PANEL,
        "styled_panel": STYLED_PANEL,
        "win_panel": WIN_PANEL,
        "h_line": H_LINE,
        "v_line": V_LINE,
    }

    @staticmethod
    def get(shape: ShapeTypes) -> QFrame.Shape:
        return Shape.__MAP__.get(shape, Shape.V_LINE)
