# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QFrame

ShadowTypes = Literal[
    "sunken",
    "raised",
    "plain",
]


@final
class Shadow:
    SUNKEN = QFrame.Shadow.Sunken
    RAISED = QFrame.Shadow.Raised
    PLAIN = QFrame.Shadow.Plain

    __MAP__: dict[ShadowTypes, QFrame.Shadow] = {
        "sunken": SUNKEN,
        "raised": RAISED,
        "plain": PLAIN,
    }

    @staticmethod
    def get(shadow: ShadowTypes) -> QFrame.Shadow:
        return Shadow.__MAP__.get(shadow, Shadow.SUNKEN)
