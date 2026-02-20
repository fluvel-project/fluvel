# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

SETTINGS_TEMPLATE = """{header}
from typing import Literal, Dict, Any

{name} = {literal}

class Settings:
    @classmethod
    def get(cls, key: {name}, default: Any) -> Any: ...
    def __class_getitem__(cls, key: {name}) -> Any: ...
    @classmethod
    def set(cls, key: str, value: Any) -> None: ...
    @classmethod
    def to_dict(cls) -> Dict[str, Any]: ...
"""
