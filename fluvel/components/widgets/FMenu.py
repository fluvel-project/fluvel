# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TypedDict, Unpack

from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QMenu, QMenuBar

# Fluvel
from fluvel.components.gui.FAction import FAction
from fluvel.i18n.I18nTextVar import I18nMenuTextVar
from fluvel.i18n.ResourceManager import er


class FMenuKwargs(TypedDict, total=False):
    parent: QMenu | QMenuBar | None
    menu_title: str | I18nMenuTextVar
    menu_structure: dict
    registry: dict[str, FAction]


class FMenu(QMenu):
    def __init__(self, **kwargs: Unpack[FMenuKwargs]) -> None:
        super().__init__(kwargs.get("parent"))

        self._registry = kwargs.get("registry", {})

        self.configure(**kwargs)

        if "menu_structure" in kwargs:
            self._create_menu(kwargs.get("parent"), kwargs.get("menu_structure"))

    def configure(self, **kwargs: Unpack[FMenuKwargs]) -> None:
        if menu_title := kwargs.get("menu_title"):
            if isinstance(menu_title, I18nMenuTextVar):
                menu_title.setParent(self)
                menu_title.valueChanged.connect(self.setTitle)
                menu_title = menu_title.value

            self.setTitle(menu_title)

    def _create_menu(self, parent, structure: dict):
        parent_menu = self if not isinstance(parent, QMenuBar) else parent
        self._structure_menu(parent_menu, structure, self._registry)

    def _structure_menu(self, parent_menu, structure, registry, prefix=""):
        for _id, element_dict in structure.items():
            if _id.startswith("sep_"):
                parent_menu.addSeparator()
                continue

            path = f"{prefix}.{_id}" if prefix else _id
            elements = element_dict.get("elements")

            if elements:
                new_menu = self._add_menu(parent_menu, _id, element_dict)
                registry[path] = new_menu

                self._structure_menu(new_menu, elements, registry, path)
            else:
                action = self._add_action(parent_menu, _id, element_dict)
                registry[path] = action

    def _add_menu(self, parent_menu: QMenu | QMenuBar, element_id, element_dict: dict) -> "FMenu":
        i18n_text = er[element_id]
        menu = FMenu(parent=parent_menu, menu_title=i18n_text, registry=self._registry)

        parent_menu.addMenu(menu)
        return menu

    def _add_action(self, parent_menu: QMenu, element_id: str, element_dict: dict) -> FAction:
        i18n_text = er[element_id]
        action = FAction(parent=parent_menu, text=i18n_text)

        if icon_path := element_dict.get("icon"):
            action.setIcon(QIcon(icon_path))

        if checkable := element_dict.get("checkable"):
            action.setCheckable(checkable)

        parent_menu.addAction(action)
        return action
