# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtCore import Qt

CheckStateTypes = Literal["checked", "partial", "unchecked"]

@final
class CheckState:

    CHECKED = Qt.CheckState.Checked
    PARTIAL = Qt.CheckState.PartiallyChecked
    UNCHECKED = Qt.CheckState.Unchecked

    __MAP__ = {
        "checked": CHECKED,
        "partial": PARTIAL,
        "unchecked": UNCHECKED
    }

    @staticmethod
    def get(checkstate: CheckStateTypes) -> Qt.CheckState:
        return CheckState.__MAP__.get(checkstate, CheckState.UNCHECKED)