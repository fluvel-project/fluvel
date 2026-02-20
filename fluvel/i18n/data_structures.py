# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class I18nRawContent:
    MENUS: dict[str, dict[str, Any]]
    TEXTS: dict[str, str]


class I18nSafeDict(dict):
    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"
