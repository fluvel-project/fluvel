# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Any

# Fluvel
from fluvel.i18n.data_structures import I18nRawContent


class I18nProvider:
    texts: dict[str, str] = {}
    menus: dict[str, str] = {}
    raw_menus: dict[str, dict[str, Any]] = {}

    get_text: Callable[[str, str], str] = None
    get_menu: Callable[[str, str], str] = None

    @classmethod
    def save_content(cls, raw: I18nRawContent) -> None:
        cls.texts = raw.TEXTS
        cls.menus = cls._flatten_menus(raw.MENUS)
        cls.raw_menus = raw.MENUS

        cls.get_text = cls.texts.get
        cls.get_menu = cls.menus.get

    @staticmethod
    def _flatten_menus(raw_menus: dict[str, dict[str, Any]]) -> dict[str, str]:
        flat_map: dict[str, str] = {}

        stack = []

        for menu_structure in raw_menus.values():
            stack.append(menu_structure)

        while stack:
            current_items = stack.pop()

            for _id, data in current_items.items():
                text = data["text"]

                if text != "---":
                    flat_map[_id] = text

                if elements := data.get("elements"):
                    stack.append(elements)

        return flat_map
