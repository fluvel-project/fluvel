# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtCore import Qt

OrientationTypes = Literal["vertical", "horizontal"]


@final
class Orientation:
    VERTICAL = Qt.Orientation.Vertical
    HORIZONTAL = Qt.Orientation.Horizontal

    __MAP__: dict[OrientationTypes, Qt.Orientation] = {
        "vertical": VERTICAL,
        "horizontal": HORIZONTAL,
    }

    @staticmethod
    def get(orientation: OrientationTypes) -> Qt.Orientation:
        return Orientation.__MAP__.get(orientation, Orientation.HORIZONTAL)
