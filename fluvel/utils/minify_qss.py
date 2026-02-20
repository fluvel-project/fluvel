# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import re


def minify_qss(qss: str) -> str:
    """
    This function is used only in :func:`fluvel.cli.commands.build.generate_themes`.
    It removes comments, unnecessary whitespace, and line breaks
    to reduce file size and speed up parsing in Qt.
    """
    qss = re.sub(r"/\*.*?\*/", "", qss, flags=re.DOTALL)
    qss = re.sub(r"\s*([\{\}\:\;\,\>])\s*", r"\1", qss)
    qss = re.sub(r"\s+", " ", qss)
    return qss.strip()
