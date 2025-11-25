# fluvel.core.MenuBar
from typing import Callable, Any, TypedDict, Dict, Unpack

# Fluvel
from fluvel.core.abstract_models.FWidget import FWidget
from fluvel.components.gui.FAction import FAction
from fluvel.components.widgets.FMenu import FMenu
from fluvel._user.GlobalConfig import AppConfig

# PySide6
from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QIcon

# Utils
from fluvel._user.MenuOptions import MenuOptions
from fluvel.core.tools.generate_menu_options import set_dynamic_menu_keys
from fluvel.utils.tip_helpers import ActionProperties, ActionSignalTypes, StandardActionShortcut

ACTION_SIGNALS = ["hovered", "triggered", "changed", "toggled"]

class ActionProperties(TypedDict):

    # ActionProperties
    text            : str
    icon            : QIcon
    shortcut        : StandardActionShortcut
    statusTip       : str
    enabled         : bool
    visible         : bool
    checkable       : bool
    menuRole        : FAction.MenuRole
    data            : Any

    # Signals
    triggered       : Callable
    hovered         : Callable
    changed         : Callable
    toggled         : Callable

class MenuBarKwargs(TypedDict, total=False):

    style           : str
    controls        : Dict[MenuOptions, ActionProperties]

class MenuBar(QMenuBar, FWidget):
    """
    A high-level wrapper around :py:class:`PySide6.QtWidgets.QMenuBar` for Fluvel applications.

    This class simplifies the configuration of menu items by abstracting complex
    signal connections and property settings into simple, readable methods like 
    :py:meth:`bind`, :py:meth:`set_property`, and the centralized :py:meth:`config` method.

    The actual menu structure (menus, sub-menus, and actions) is built internally 
    by :py:class:`~fluvel.components.widgets.FMenu` based on content files.
    """

    def __init__(self, *, structure: Dict, **kwargs: Unpack[MenuBarKwargs]):
        """
        Initializes the MenuBar and builds its structure.

        :param parent: The parent window, typically an :py:class:`~fluvel.core.AppWindow` instance.
        :type parent: :py:class:`PySide6.QtWidgets.QWidget`
        
        :param structure: A dictionary representing the hierarchical structure of the menu 
                          (loaded from a configuration file).
        :type structure: dict
        """
        super().__init__()

        self._fwidget_defaults()

        self.menu = FMenu(parent=self, menu_structure=structure)

        self.configure(**kwargs)
        
        # Generate the literal that contains all menu options
        if AppConfig.fluvel.DEV_MODE:
            set_dynamic_menu_keys(self.menu.all_menu_options)

    def get_item(self, item_name: str) -> FAction | FMenu:
        """
        Retrieves a menu item (either a menu or an action) by its string name.

        The item is accessed as an attribute of the :py:class:`MenuBar` instance.

        :param item_name: The name of the menu item (action or submenu) to retrieve.
        :type item_name: :py:class:`~fluvel._user.MenuOptions`

        :returns: The corresponding :py:class:`~fluvel.components.gui.FAction` or :py:class:`~fluvel.components.widgets.FMenu` object.
        :rtype: :py:class:`~fluvel.components.gui.FAction` or :py:class:`~fluvel.components.widgets.FMenu`
        """
        return getattr(self, item_name)
    
    def bind(
        self, menu_option: MenuOptions, action: ActionSignalTypes, controller: Callable
    ) -> None:
        """
        Connects a controller (callback function) to a specific signal of a menu item.

        This is the low-level method used by all ``on_*`` and ``add_shortcut`` methods.

        :param menu_option: The name of the menu action.
        :type menu_option: :py:class:`~fluvel._user.MenuOptions`

        :param action: The name of the signal/action method to connect to (e.g., ``"triggered"``, ``"hovered"``).
        :type action: :py:class:`~fluvel.utils.tip_helpers.ActionTypes`

        :param controller: The callable function or method to execute when the action is fired.
        :type controller: :py:class:`typing.Callable`

        :rtype: None
        """
        menu_item = self.get_item(menu_option)

        getattr(menu_item, action).connect(controller)

    def set_property(
        self,
        menu_option: MenuOptions,
        property_to_change: ActionProperties,
        new_value: Any,
    ) -> None:
        """
        Sets a specific property (e.g., ``"Text"``, ``"Checked"``) for a menu item.

        The method constructs the appropriate setter method name (e.g., ``set + PropertyToChange``) 
        and calls it on the item.

        :param menu_option: The name of the menu action.
        :type menu_option: :py:class:`~fluvel._user.MenuOptions`

        :param property_to_change: The property to change (e.g., ``"Text"``, ``"Enabled"``).
        :type property_to_change: :py:class:`~fluvel.utils.tip_helpers.ActionProperties`

        :param new_value: The new value for the property.
        :type new_value: any

        :rtype: None
        """
        property_method = f"set{property_to_change.capitalize()}"
        menu_item = self.get_item(menu_option)
        getattr(menu_item, property_method)(new_value)
  
    def configure(
        self,
        **kwargs: Unpack[MenuBarKwargs]
    ) -> None:
        """
        Provides a unified, declarative interface for configuring menu actions
        and styling the menu bar.

        :param controls: A dictionary mapping menu action IDs to their
                         configuration. The configuration is a
                         `MenuBarProperties` dictionary defining properties
                         (e.g., "Text", "Icon", "Shortcut") and signals
                         (e.g., "triggered", "hovered").
        :type controls: dict[:py:class:`~fluvel._user.MenuOptions`, :py:class:`~fluvel.core.MenuBar.MenuBarProperties`]

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

        kwargs = super().configure(**kwargs)

        if controls := kwargs.get("controls"):
            for action, properties in controls.items():
                for prop_name, value in properties.items():
                    if prop_name in ACTION_SIGNALS:
                        self.bind(action, prop_name, value)
                    else:
                        self.set_property(action, prop_name, value)
