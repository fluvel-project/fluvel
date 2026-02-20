# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

RMANAGER_TEMPLATE = """{header}
from typing import Literal
from collections.abc import Callable
from fluvel.i18n.I18nTextVar import I18nTextVar
from fluvel.i18n.I18nTextVar import I18nMenuTextVar

{name} = {literal}

class ResourceManager:
    def __call__(self, id: {name}, **placeholders) -> I18nTextVar | str: ...
    def __getitem__(self, id: str) -> I18nMenuTextVar | str: ...
    def set_lang(self, lang: str) -> None: ...
    def set_theme(self, theme: str) -> None: ...
    def as_set_lang(self, lang: str) -> Callable[[], None]: ...
    def as_set_theme(self, theme: str) -> Callable[[], None]: ...

er: ResourceManager
"""
