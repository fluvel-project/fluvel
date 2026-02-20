# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Any, TypedDict, Unpack

from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QMenuBar

from fluvel.components.gui.FAction import FAction
from fluvel.components.widgets.FMenu import FMenu

# Fluvel
from fluvel.core.abstract.FWidget import FWidget

# Utils
from fluvel.utils.tip_helpers import (
    ActionPropertyTypes,
    ActionSignalTypes,
    StandardActionShortcut,
)

ACTION_SIGNALS = ["hovered", "triggered", "changed", "toggled"]


class ActionProperties(TypedDict):
    # ActionProperties
    Text: str
    Icon: QIcon
    Shortcut: StandardActionShortcut
    StatusTip: str
    Enabled: bool
    Visible: bool
    Checkable: bool
    MenuRole: FAction.MenuRole
    Data: Any

    # Signals
    triggered: Callable
    hovered: Callable
    changed: Callable
    toggled: Callable


class MenuBarKwargs(TypedDict, total=False):
    style: str
    controls: dict[str, ActionProperties]


class MenuBar(QMenuBar, FWidget):
    """
    A high-level wrapper around :class:`PySide6.QtWidgets.QMenuBar` for Fluvel applications.

    This class simplifies the configuration of menu items by abstracting complex
    signal connections and property settings into simple, readable methods like
    :meth:`bind_action`, :meth:`set_property`, and the centralized :meth:`config` method.

    The actual menu structure (menus, sub-menus, and actions) is built internally
    by :class:`~fluvel.components.widgets.FMenu` based on content files.
    """

    _QT_PROPERTY_MAP = {}

    def __init__(self, *, structure: dict, **kwargs: Unpack[MenuBarKwargs]):
        """
        Initializes the MenuBar and builds its structure.

        :param parent: The parent window, typically an :class:`~fluvel.core.AppWindow` instance.
        :type parent: :class:`PySide6.QtWidgets.QWidget`

        :param structure: A dictionary representing the hierarchical structure of the menu
                          (loaded from a configuration file).
        :type structure: dict
        """
        super().__init__()

        self._set_defaults()

        self._actions: dict[str, FAction] = {}

        self.menu = FMenu(parent=self, menu_structure=structure, registry=self._actions)

        self.configure(**kwargs)

    def get_item(self, item_name: str) -> FAction | FMenu:
        """
        Retrieves a menu item (either a menu or an action) by its string name.

        The item is accessed as an attribute of the :class:`MenuBar` instance.

        :param item_name: The name of the menu item (action or submenu) to retrieve.
        :type item_name: :class:`~fluvel.user.MenuOptions`

        :returns: The corresponding :class:`~fluvel.components.gui.FAction` or :class:`~fluvel.components.widgets.FMenu` object.
        :rtype: :class:`~fluvel.components.gui.FAction` or :class:`~fluvel.components.widgets.FMenu`
        """
        return self._actions.get(item_name)

    def bind_action(
        self, menu_option: str, signal: ActionSignalTypes, controller: Callable
    ) -> None:
        """
        Connects a controller (callback function) to a specific signal of a menu item.
        """
        action = self.get_item(menu_option)
        if action:
            getattr(action, signal).connect(controller)

    def set_property(
        self,
        menu_option: str,
        property_to_change: ActionPropertyTypes,
        new_value: Any,
    ) -> None:
        """
        Sets a specific property (e.g., ``"Text"``, ``"Checked"``) for a menu item.

        The method constructs the appropriate setter method name (e.g., ``set + PropertyToChange``)
        and calls it on the item.

        :param menu_option: The name of the menu action.
        :type menu_option: :class:`~fluvel.user.MenuOptions`

        :param property_to_change: The property to change (e.g., ``"Text"``, ``"Enabled"``).
        :type property_to_change: :class:`~fluvel.utils.tip_helpers.ActionProperties`

        :param new_value: The new value for the property.
        :type new_value: any

        :rtype: None
        """
        property_method = f"set{property_to_change}"
        action = self.get_item(menu_option)
        if action:
            getattr(action, property_method)(new_value)

    def configure(self, **kwargs: Unpack[MenuBarKwargs]) -> None:
        """
        Provides a unified, declarative interface for configuring menu actions
        and styling the menu bar.

        :param controls: A dictionary mapping menu action IDs to their
                         configuration. The configuration is a
                         `MenuBarProperties` dictionary defining properties
                         (e.g., "Text", "Icon", "Shortcut") and signals
                         (e.g., "triggered", "hovered").
        :type controls: dict[:class:`~fluvel.user.MenuOptions`, :class:`~fluvel.core.MenuBar.MenuBarProperties`]

        :param style: A string containing Fluvel style rules (e.g., "bg[white]")
                      to be applied to the MenuBar itself.
        :type style: str

        :rtype: None

        Example
        -------
        .. code-block:: python

            def on_open_file():
                print("Opening file...")

            def on_exit_app():
                self.main_window.close()

            # Get the menu_bar instance (e.g., self.main_window.menu_bar)
            menu_bar.configure(
                controls={
                    "file_open": {
                        "text": "Open...",
                        "shortcut": "Ctrl+O",
                        "statusTip": "Open a new file",
                        "triggered": on_open_file
                    },
                    "file_exit": {
                        "text": "Exit",
                        "shortcut": "Ctrl+Q",
                        "statusTip": "Exit the application",
                        "triggered": on_exit_app
                    }
                },
                style="bg[#333] f-color[white]"
            )
        """

        if controls := kwargs.pop("controls", None):
            for action, properties in controls.items():
                for prop_name, value in properties.items():
                    if prop_name in ACTION_SIGNALS:
                        self.bind_action(action, prop_name, value)
                    else:
                        self.set_property(action, prop_name, value)

        super().configure(**kwargs)
