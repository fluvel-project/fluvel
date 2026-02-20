# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtCore import Qt

WindowStateTypes = Literal["normal", "minimized", "maximized", "fullscreen", "active"]


@final
class WindowState:
    NORMAL = Qt.WindowState.WindowNoState
    MINIMIZED = Qt.WindowState.WindowMinimized
    MAXIMIZED = Qt.WindowState.WindowMaximized
    FULLSCREEN = Qt.WindowState.WindowFullScreen
    ACTIVE = Qt.WindowState.WindowActive

    __MAP__: dict[WindowStateTypes, Qt.WindowState] = {
        "normal": NORMAL,
        "minimized": MINIMIZED,
        "maximized": MAXIMIZED,
        "fullscreen": FULLSCREEN,
        "active": ACTIVE,
    }

    @staticmethod
    def get(state: WindowStateTypes | list[WindowStateTypes]) -> Qt.WindowState:
        if isinstance(state, str):
            return WindowState.__MAP__.get(state, WindowState.NORMAL)

        # local binding
        map_get = WindowState.__MAP__.get
        normal_type = WindowState.NORMAL

        if isinstance(state, list):
            flags = normal_type

            for item in state:
                flags |= map_get(item, normal_type)

            return flags

        return normal_type
