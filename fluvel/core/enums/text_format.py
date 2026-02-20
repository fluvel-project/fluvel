# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtCore import Qt

TextFormatTypes = Literal["auto", "plain", "rich", "markdown"]


@final
class TextFormat:
    AUTO = Qt.TextFormat.AutoText
    PLAIN = Qt.TextFormat.PlainText
    RICH = Qt.TextFormat.RichText
    MARKDOWN = Qt.TextFormat.MarkdownText

    __MAP__: dict[TextFormatTypes, Qt.TextFormat] = {
        "auto": AUTO,
        "plain": PLAIN,
        "rich": RICH,
        "markdown": MARKDOWN,
    }

    @staticmethod
    def get(text_format: TextFormatTypes) -> Qt.TextFormat:
        return TextFormat.__MAP__.get(text_format, TextFormat.AUTO)
