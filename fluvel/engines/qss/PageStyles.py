# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

class PageStyles:
    _styles: list[str] = []

    @classmethod
    def add(cls, style: str) -> None:
        cls._styles.append(style)

    @classmethod
    def getall(cls) -> str:
        styles = "".join(cls._styles)
        cls._styles.clear()
        return styles