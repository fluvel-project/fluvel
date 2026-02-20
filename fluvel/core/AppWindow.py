# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TYPE_CHECKING, TypedDict, Unpack

# PySide6
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget

# Utils
from fluvel.core.enums import (
    WidgetAttributeTypes,
    WindowState,
    WindowStateTypes,
    WindowType,
    WindowTypes,
)
from fluvel.core.MenuBar import MenuBar

# Fluvel Controllers
from fluvel.i18n.I18nProvider import I18nProvider
from fluvel.i18n.I18nTextVar import I18nTextVar
from fluvel.user.UserSettings import Settings

if TYPE_CHECKING:
    from fluvel.core.App import App


class AppWindowKwargs(TypedDict, total=False):
    """
    Specifies the optional keyword arguments used to configure the main application window.
    """

    title: str | I18nTextVar
    geometry: tuple[int, int, int, int] | list[int]
    size: tuple[int, int]
    resizable: bool
    min_size: tuple[int, int]
    max_size: tuple[int, int]
    min_width: int
    min_height: int
    max_width: int
    max_height: int
    opacity: float
    state: WindowStateTypes
    flags: list[WindowTypes]
    attributes: list[WidgetAttributeTypes]


class AppWindow(QMainWindow, FWidget, FTextWidget):
    """
    The main window container for a Fluvel application.

    This class serves as the top-level "shell" for the entire user interface.
    It inherits from :class:`PySide6.QtWidgets.QMainWindow` and is responsible for
    managing core UI elements like the central widget area (a :class:`QStackedWidget`
    for the Router), the menu bar, and the overall window properties.

    The primary way to use this class is to subclass it in your project.

    :ivar app: The parent :class:`~fluvel.core.App.App` instance.
    :type app: :class:`~fluvel.core.App.App`

    **Example of Subclassing:**

    .. code-block:: python

        # In your project's window.py
        from fluvel import AppWindow

        class MainWindow(AppWindow):
            def init_ui(self) -> None:
                \"\"\"
                This method is called after the core UI is initialized.
                It's the perfect place for initial setup.
                \"\"\"
                # Configure window properties
                self.configure(title="My First Fluvel App", size=[1024, 768])
    """

    _QT_PROPERTY_MAP = {
        "title": "setWindowTitle",
        "geometry": "setGeometry",
        "size": "resize",
        "opacity": "setWindowOpacity",
        "flags": "setWindowFlags",
        "state": "setWindowState",
    }

    def __init__(self, app_instance: "App") -> None:
        """
        Initializes the AppWindow.

        It configures the window based on settings from :class:`~fluvel.user.UserSettings.Settings`,
        initializes the core UI components, and calls the user's :meth:`__post_init__` hook.

        :param app: The parent application instance (the :class:`~fluvel.core.App.App`).
        :type app: :class:`~fluvel.core.App.App`

        :rtype: None
        """
        super().__init__()
        FWidget._set_defaults(self)

        # The fluvel.core.App instance
        self.app: App = app_instance

        # Configured with the specifications from the .toml file
        if win_defaults := Settings.get("window"):
            self.configure(**vars(win_defaults))

        self._init_core_ui()

        # Initializes and displays the UI
        # Calls the optional __post_init__ hook
        self.__post_init__()

    def __post_init__(self) -> None:
        """
        An overridable method for initial user UI or Core configuration.

        This method is intended to be implemented in your subclass of :class:`AppWindow`.
        It is automatically called by Fluvel at the end of the initialization process,
        after the central widget and menu bar have been created.

        .. note::
           This is the designated "hook" for adding your application's initial
           setup logic, such as configuring menu actions or connecting signals.

        :rtype: None
        """
        pass

    def configure(self, **kwargs: Unpack[AppWindowKwargs]) -> None:
        """
        Configures multiple window properties from a single call.

        This high-level method allows setting various window attributes using
        keyword arguments, which are typically loaded from the ``config.toml``
        file but can also be set programmatically.

        :param title: Sets the window title.
        :type  title: str

        :param geometry: The initial position and size of the window as a four-element sequence: ``(x, y, width, height)``.
        :type geometry: Tuple[int, int, int, int] or List

        :param size: Sets the initial window size as ``(width, height)``.
        :type size: Tuple[int, int] or List

        :param resizable: Toggles whether the user can resize the window.
        :type resizable: bool

        :param min_size: Sets the minimum window size.
        :type min_size: Tuple[int, int] or List

        :param max_size: Sets the maximum window size.
        :type max_size: Tuple[int, int] or List

        :param min_width: Sets the minimum allowed width for the window.
        :type min_width: int

        :param min_height: Sets the minimum allowed height for the window.
        :type min_height: int

        :param max_width: Sets the maximum allowed width for the window.
        :type max_width: int

        :param max_height: Sets the maximum allowed height for the window.
        :type max_height: int

        :param show_mode: Sets the initial window state (e.g., "Normal", "Maximized").
        :type show_mode: str

        :param flags: A List of window flags to apply (e.g., "frameless").
        :type flags: List[:obj:`~fluvel.core.enums.WindowTypes`]

        :param attributes: A List of widget attributes to configure low-level behavior.
        :type attributes: List[:obj:`~fluvel.core.enums.WindowStateTypes`]

        :rtype: None
        """

        kwargs = self._apply_texts(**kwargs)

        if flags := kwargs.get("flags"):
            kwargs["flags"] = WindowType.get(flags)

        if mode := kwargs.get("state"):
            kwargs["state"] = WindowState.get(mode)

        super().configure(**kwargs)

        # The self.width() and self.height() propqerties will not be set yet.
        # If this is the first call to the method, it must be executed.
        # The "resizable" logic will ONLY be applied after the size has been set.
        if not kwargs.get("resizable", True):
            self.setFixedSize(self.width(), self.height())

    def _init_core_ui(self) -> None:
        """
        Initializes the core UI components of the window.

        This internal method orchestrates the setup of the central widget and
        the menu bar, and then calls the user-defined :meth:`init_ui` hook.

        :rtype: None
        """

        # Configuring the layout
        self._set_central_widget()

        # Configuring the Top Menu Bar
        self._set_menu_bar()

    def _set_menu_bar(self) -> None:
        """
        Initializes and sets up the main menu bar from the content configuration.
        """

        if menu := I18nProvider.raw_menus.get("main-menu", {}):
            # This is an instance of QMenuBar
            self.menu_bar = MenuBar(parent=self, structure=menu)

            # Adding the Menu Bar to the Window
            self.setMenuBar(self.menu_bar)

    def _set_central_widget(self) -> None:
        """
        Creates and configures the central :class:`PySide6.QtWidgets.QStackedWidget`.

        This widget serves as the container for all views managed by the
        :class:`~fluvel.core.Router.Router`.
        :rtype: None
        """
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

    def normalize(self) -> None:
        """
        Resets the window to its normal desktop state (with window decorations)
        and disables any special PySide6 attributes that may have been applied
        (e.g., frameless, always-on-top, translucent background).

        .. note:: The geometry (size and position) is not reset so as not to lose the position
            and size that has been adjusted.

        :rtype: None
        """

        self.configure(
            opacity=1.0,
            flags=[
                "title",
                "sys-menu",
                "minimize-button",
                "maximize-button",
                "close-button",
            ],
        )

        # Normalize the window state
        self.setWindowState(WindowState.NORMAL)

        self.show()

    def frameless(self) -> None:
        """
        Applies a clean, frameless window style, removing standard title bars, menu bar
        and decorations, and enables a translucent background.

        This is commonly used for custom UI designs where the application draws
        its own title bar or needs irregular shapes.

        :rtype: None
        """

        self.configure(flags=["frameless"], attributes=["translucent-background"])

        if hasattr(self, "menu_bar"):
            self.menu_bar.hide()

        self.show()

    def minimize(self) -> None:
        """
        Minimizes the window, hiding it and typically placing an icon
        in the system's taskbar or dock.

        :rtype: None
        """

        self.showMinimized()

    def maximize(self) -> None:
        """
        Toggles the window state between maximized and normal (restored) state.

        If the window is currently maximized, it is restored to its normal size
        and position; otherwise, it is maximized.

        :rtype: None
        """

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def fullscreen(self) -> None:
        """
        Toggles the window state between fullscreen and normal (restored) state.

        If the window is currently fullscreen, it is restored to its normal size
        and position; otherwise, it is fullscreen.

        :rtype: None
        """

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def kiosk(self, hide_menu: bool = True) -> None:
        """
        Toggles the application's Kiosk Mode.

        This method is designed for service applications (e.g., gas stations,
        information totems, ATMs) where the user's focus must be restricted
        entirely to the application.

        .. warning::
            **Exit Strategy Required:** Since Kiosk Mode removes window decorations
            (close/minimize buttons) and forces the window to stay on top, you **must** provide
            a programmatic way to exit (e.g., a hidden button, a password-protected
            exit, or a global keyboard shortcut). Failure to do so may require a
            system-level process termination.

        **Behavior:**
        - **Activation:** If the window is not in fullscreen, it applies
          a frameless style, forces the window to stay on top of all others,
          hides the system menu bar (optional), and expands to fill the entire screen.
        - **Deactivation:** If the window is already in fullscreen, it calls
          :meth:`normalize` to restore the standard window decorations,
          normal desktop state, and restores the menu bar visibility.

        :param hide_menu: Whether to hide the global :class:`~fluvel.core.MenuBar.MenuBar`
                          when entering Kiosk Mode. Defaults to ``True``.
        :type hide_menu: bool

        :rtype: None

        Example
        -------
        .. code-block:: python

            # Perfect for a "Start Service" button or an administrative hotkey
            self.kiosk(hide_menu=True)
        """

        if not self.isFullScreen():
            self.configure(
                flags=["frameless", "always-on-top"], attributes=["translucent-background"]
            )

            if hide_menu and hasattr(self, "menu_bar"):
                self.menu_bar.hide()

            self.showFullScreen()

        else:
            self.normalize()

            if hasattr(self, "menu_bar"):
                self.menu_bar.show()
