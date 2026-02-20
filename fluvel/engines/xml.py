# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

# Expect Handler
from fluvel.core.tools.expect_handler import expect


class XMLMenuParser:
    @classmethod
    @expect.FileNotFound(stop=True)
    def parse(cls, file_path: Path) -> dict[str, Any]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        menu_structure: dict[str, Any] = {}
        build_from_element = cls._build_dict_from_element

        # Usamos enumerate para que los menús principales también tengan orden si fuera necesario
        for menu_element in root.findall("menu"):
            menu_id = menu_element.get("id")
            if menu_id:
                menu_structure[menu_id] = build_from_element(menu_element)

        return menu_structure

    @classmethod
    def _build_dict_from_element(cls, element: ET.Element) -> dict[str, Any]:
        # El caso base del separador ya no necesita generar su propio ID aquí,
        # lo hará el padre al iterar.
        if element.tag == "sep":
            return {"text": "---"}

        node_dict = {
            "id": element.get("id"),
            "text": element.get("text", element.text),
            "icon": element.get("icon"),
            "checkable": element.get("checkable") == "true",
            "elements": {} if len(element) > 0 else None,
        }

        if node_dict["elements"] is not None:
            # Aquí es donde ocurre la magia del ID predecible
            for i, child in enumerate(element):
                # Si el hijo tiene ID lo usamos, si no (como el sep), usamos el índice
                child_id = child.get("id") or f"sep_{i}"
                node_dict["elements"][child_id] = cls._build_dict_from_element(child)

        return node_dict
