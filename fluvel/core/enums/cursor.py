# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtCore import Qt

CursorTypes = Literal[
    "arrow",
    "up_arrow",
    "cross",
    "wait",
    "ibeam",
    "size_ver",
    "size_hor",
    "size_bdi",
    "size_fwd",
    "size_all",
    "blank",
    "pointing_hand",
    "open_hand",
    "closed_hand",
    "busy",
    "forbidden",
    "split_ver",
    "split_hor",
    "whats_this",
    "drag_copy",
    "drag_move",
    "drag_link",
]


@final
class Cursor:
    ARROW = Qt.CursorShape.ArrowCursor
    UP_ARROW = Qt.CursorShape.UpArrowCursor
    CROSS = Qt.CursorShape.CrossCursor
    WAIT = Qt.CursorShape.WaitCursor
    IBEAM = Qt.CursorShape.IBeamCursor
    SIZE_VER = Qt.CursorShape.SizeVerCursor
    SIZE_HOR = Qt.CursorShape.SizeHorCursor
    SIZE_BDI = Qt.CursorShape.SizeBDiagCursor
    SIZE_FWD = Qt.CursorShape.SizeFDiagCursor
    SIZE_ALL = Qt.CursorShape.SizeAllCursor
    BLANK = Qt.CursorShape.BlankCursor
    POINTING_HAND = Qt.CursorShape.PointingHandCursor
    OPEN_HAND = Qt.CursorShape.OpenHandCursor
    CLOSED_HAND = Qt.CursorShape.ClosedHandCursor
    BUSY = Qt.CursorShape.BusyCursor
    FORBIDDEN = Qt.CursorShape.ForbiddenCursor
    SPLIT_VER = Qt.CursorShape.SplitVCursor
    SPLIT_HOR = Qt.CursorShape.SplitHCursor
    WHATS_THIS = Qt.CursorShape.WhatsThisCursor
    DRAG_COPY = Qt.CursorShape.DragCopyCursor
    DRAG_MOVE = Qt.CursorShape.DragMoveCursor
    DRAG_LINK = Qt.CursorShape.DragLinkCursor

    __MAP__: dict[CursorTypes, Qt.CursorShape] = {
        "arrow": ARROW,
        "up_arrow": UP_ARROW,
        "cross": CROSS,
        "wait": WAIT,
        "ibeam": IBEAM,
        "size_ver": SIZE_VER,
        "size_hor": SIZE_HOR,
        "size_bdi": SIZE_BDI,
        "size_fwd": SIZE_FWD,
        "size_all": SIZE_ALL,
        "blank": BLANK,
        "pointing_hand": POINTING_HAND,
        "open_hand": OPEN_HAND,
        "closed_hand": CLOSED_HAND,
        "busy": BUSY,
        "forbidden": FORBIDDEN,
        "split_ver": SPLIT_VER,
        "split_hor": SPLIT_HOR,
        "whats_this": WHATS_THIS,
        "drag_copy": DRAG_COPY,
        "drag_move": DRAG_MOVE,
        "drag_link": DRAG_LINK,
        "hand": POINTING_HAND,
        "size_diag": SIZE_BDI,
    }

    @staticmethod
    def get(cursor: CursorTypes) -> Qt.CursorShape:
        return Cursor.__MAP__.get(cursor, Cursor.ARROW)
