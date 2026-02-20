# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QLineEdit

EchoModeTypes = Literal["no-echo", "normal", "password", "password-on-edit"]


@final
class EchoMode:
    NO_ECHO = QLineEdit.EchoMode.NoEcho
    NORMAL = QLineEdit.EchoMode.Normal
    PASSWORD = QLineEdit.EchoMode.Password
    PASSWORD_ON_EDIT = QLineEdit.EchoMode.PasswordEchoOnEdit

    __MAP__: dict[EchoModeTypes, QLineEdit.EchoMode] = {
        "no-echo": NO_ECHO,
        "normal": NORMAL,
        "password": PASSWORD,
        "password-on-edit": PASSWORD_ON_EDIT,
    }

    @staticmethod
    def get(echo_mode: EchoModeTypes) -> QLineEdit.EchoMode:
        return EchoMode.__MAP__.get(echo_mode, EchoMode.NO_ECHO)
