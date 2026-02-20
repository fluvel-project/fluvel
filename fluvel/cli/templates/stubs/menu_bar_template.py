# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

MENU_BAR_TEMPLATE = """{header}
from typing import Literal, Dict, Any, Callable
from PySide6.QtWidgets import QMenuBar
from fluvel.core.abstract.FWidget import FWidget
from fluvel.components.gui.FAction import FAction
from fluvel.utils.tip_helpers import ActionPropertyTypes, ActionSignalTypes

{name} = {literal}

ActionProperties = Literal[
    "Text",
    "Icon",
    "Shortcut",
    "StatusTip",
    "Enabled",
    "Visible",
    "Checkable",
    "MenuRole",
    "Data",
    "triggered",
    "hovered",
    "changed",
    "toggled"
]
    
class MenuBar(QMenuBar, FWidget):
    def __getattr__(self, name: {name}) -> FAction: ...
    def get_item(self, item_name: {name}) -> FAction: ...
    def bind_action(
        self, 
        menu_option: {name}, 
        action: ActionSignalTypes,
        controller: Callable
    ) -> None: ...

    def set_property(
        self,
        menu_option: {name},
        property_to_change: ActionPropertyTypes,
        new_value: Any
    ) -> None: ...

    def configure(
        self, 
        *,
        style: str = ...,
        controls: Dict[{name}, Dict[ActionProperties, Any]] = ...
    ) -> None: ...
"""
