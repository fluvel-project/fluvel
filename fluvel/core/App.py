# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import importlib
import sys
from pathlib import Path
from typing import TypedDict, Unpack

from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QApplication

# Fluvel
from fluvel.core.Router import Router
from fluvel.core.tools.core_process import configure_process
from fluvel.core.tools.expect_handler import expect

# I18n
from fluvel.i18n.ResourceManager import er
from fluvel.user.UserSettings import Settings

# Utils
from fluvel.utils.paths import CONFIG_PATH, PAGES_DIR


class AppRegisterKwargs(TypedDict, total=False):
    initial: str
    pages: list[str] | None
    animation: str


class AppKwargs(TypedDict, total=False):
    name: str
    display_name: str
    version: str
    organization: str
    domain: str
    icon: str
    desktop_filename: str


class App(QApplication):
    """
    The main entry point and controller for a Fluvel application.

    This class define the entire application lifecycle. It is responsible
    for initializing the QApplication, loading the main configuration, creating
    the main window, registering views with the router, and starting the event loop.

    :param window_module_path: The dot-separated path to the module
                                containing the main window class.
                                Defaults to "window".
    :type window_module_path: Optional[str]

    :param config_file: The path to the main application configuration file.
                        Defaults to "config.toml".
    :type config_file: Path | str | None

    Example
    -------
    .. code-block:: python
       # In your app.py
       import fluvel as fl # Import fluvel namespace

       app = fl.App()
       app.register(initial="/home")

       if __name__ == "__main__":
           app.run()
    """

    _QT_PROPERTY_MAP = {
        "name": "setApplicationName",
        "display_name": "setApplicationDisplayName",
        "version": "setApplicationVersion",
        "organization": "setOrganizationName",
        "domain": "setOrganizationDomain",
        "icon": "setWindowIcon",
        "desktop_filename": "setDesktopFileName",
    }

    def __init__(
        self, window_module_path: str | None = None, config_file: str | Path | None = CONFIG_PATH
    ) -> None:
        super().__init__()

        # Inject as a dependency into the instance of the ResourceManager class
        er.app = self

        # Start initial configuration
        # This allows the use of the Configuration class
        if config_file is not None:
            self._load(config_file)

        if app_defaults := Settings.get("app"):
            self.configure(**vars(app_defaults))
        
        self.main_window = self._create_main_window(window_module_path)

        # Start router initialization
        Router.init(self, self.main_window)

    def configure(self, **kwargs: Unpack[AppKwargs]) -> None:
        """
        Applies the global application settings (metadata) to the QApplication instance.

        This method is the **central control point** for applying the application identity,
        whether the values come from the **external configuration file** ``config.toml``
        or directly from arguments passed in the **Python code**.

        Initializes Qt identity setters, such as the application name, organization,
        domain, and icon. Uses the internal mapping :attr:`~fluvel.App._QT_PROPERTY_MAP`
        to dynamically call methods of the :class:`~PySide6.QtWidgets.QApplication`.

        :param name: The internal name of the application (:meth:`~PySide6.QtWidgets.QApplication.setApplicationName`).
        :type name: str
        :param display_name: The user-readable name (:meth:`~PySide6.QtWidgets.QApplication.setApplicationDisplayName`).
        :type display_name: str
        :param version: The version of the application (:meth:`~PySide6.QtWidgets.QApplication.setApplicationVersion`).
        :type version: str
        :param organization: The name of the organization (:meth:`~PySide6.QtWidgets.QApplication.setOrganizationName`).
        :type organization: str
        :param domain: The domain of the organization (:meth:`~PySide6.QtWidgets.QApplication.setOrganizationDomain`).
        :type domain: str
        :param icon: The path to the global icon file. Converted to :class:`~PySide6.QtGui.QIcon`.
        :type icon: str
        :param desktop_file_name: The identifier for the operating system launcher (:meth:`~PySide6.QtWidgets.QApplication.setDesktopFileName`).
        :type desktop_file_name: str

        :rtype: None
        """

        if icon_path := kwargs.get("icon"):
            kwargs["icon"] = QIcon(icon_path)

        configure_process(self, self._QT_PROPERTY_MAP, **kwargs)

    def _load(self, filename: str | Path) -> None:
        """
        Loads the global application configuration from a TOML or JSON file.

        .. note::
           This is an internal method called during initialization. It also
           triggers the initial loading of static content and themes.

        :param filename: The name of the configuration file.
        :type filename: str
        """

        if isinstance(filename, str):
            filename = Path(filename).resolve()

        # Build the data model of the Settings class according to the configuration file
        Settings.init_config(filename)

        # The loading of the static content of the application is initialized (i18n)
        self._set_static_content()

    def run(self) -> None:
        """
        Starts the application's event loop.

        This method shows the main window and begins processing events. It should
        be the final call in your main script.
        """

        # Display window
        self.main_window.show()

        # Init mainloop
        sys.exit(self.exec())

    @expect.ErrorImportingModule(stop=True)
    def register(self, **kwargs: Unpack[AppRegisterKwargs]) -> None:
        """
        Registers application pages and initializes the :class:`~fluvel.core.Router.Router`.

        This method dynamically imports the specified view modules, which allows
        their ``@route`` decorators to register them with the router.

        If the ``pages`` keyword argument is not provided, the method will automatically
        scan the conventional ``ui/pages/`` directory for all Python files and import them.

        :param initial: **(Required)** The name of the route (e.g., ``"login"``) to display first when the application starts.
        :type initial: str

        :param pages: A list of view modules to import (e.g., ``["ui.pages.login.SignInPage", "ui.pages.home.Homepage"]``).
                      If omitted, all pages in the conventional ``ui/pages/`` directory are automatically detected.
        :type pages: Optional[List[str]]

        :param animation: The name of a pre-configured animation to use when displaying the initial view.
        :type animation: Optional[str]

        :raises ValueError: If the required argument ``initial`` is not provided.
        """
        initial_view = kwargs.get("initial")
        page_modules = kwargs.get("pages", [])
        animation = kwargs.get("animation")

        if initial_view is None:
            raise ValueError(
                "The 'initial' argument is required in register() to show a first view."
            )

        if not page_modules:
            page_modules = App._get_pages_to_import()

        # Importando los módulos
        for module_path in page_modules:
            importlib.import_module(module_path)

        # Show initial view
        Router.show(initial_view, animation)

    @staticmethod
    def _get_pages_to_import() -> list[str]:
        """
        Scans the project structure to automatically discover and map view modules.

        This method implements the **Autodiscovery** pattern. It iterates through the
        standard directory defined by ``PAGES_DIR``, looking for Python modules
        within feature-based subfolders.

        **Discovery Logic:**
        1. It identifies all subdirectories within the ``ui/pages/`` folder.
        2. Within each folder, it non-recursively searches for ``.py`` files.
        3. It ignores files starting with an underscore (like ``__init__.py``).
        4. It converts the file system paths into Pythonic dot-notation
           import paths (e.g., ``ui.pages.home.login_page``).

        :returns: A list of absolute module paths ready to be imported by
                  :meth:`importlib.import_module`.
        :rtype: List[str]

        .. note::
            This method is called automatically by :meth:`register` if no
            explicit list of pages is provided by the user.
        """

        # We created a list for the routes of each page
        modules_to_import = []

        # We iterate over the feature folders (e.g., 'login', 'dashboard', 'home')
        page_folders: list[Path] = [
            page_folder for page_folder in PAGES_DIR.iterdir() if page_folder.is_dir()
        ]

        for folder in page_folders:
            # We iterate over the .py files within each folder, excluding __init__.py
            for module_file in folder.glob("[!_]*.py"):
                # Building the path to the module
                module_path = f"ui.pages.{folder.name}.{module_file.stem}"

                # Added to the list of modules to import
                modules_to_import.append(module_path)

        return modules_to_import

    def _create_main_window(self, window_module_path: str | None):
        """
        Dynamically imports and instantiates the main window class.

        This internal method is responsible for loading the user-defined
        subclass of :class:`~fluvel.core.AppWindow.AppWindow`. By default, it looks
        for a ``MainWindow`` class inside a ``window.py`` module at the
        project root.

        :param window_module_path: The dot-separated path to the module
                                   containing the main window class.
                                   Defaults to "window".
        :type window_module_path: str, optional
        :returns: An instance of the user-defined main window.
        :rtype: :class:`~fluvel.core.AppWindow.AppWindow`
        :raises ImportError: If the specified module cannot be found.
        :raises AttributeError: If the ``MainWindow`` class is not found in the module.
        """

        # The default is "window" if no alternative module defining AppWindow is provided.
        window_module_path = "window" if not window_module_path else window_module_path

        # Loading MainWindow module
        window_module = importlib.import_module(window_module_path)

        # Return an instance of MainWindow(AppWindow)
        return window_module.MainWindow(self)

    def _set_static_content(self) -> None:
        """
        Loads and applies all static content, including text and themes.

        This is an internal method that orchestrates the loading of all
        ``.fluml`` content files and the application of QSS stylesheets.
        """

        # Loading static text content from views
        self._set_content()

        # Applying themes and styles to components
        self._set_theme()

    def _set_theme(self) -> None:
        """
        Loads and applies the global QSS theme to the application.

        It sets the "Fusion" style for consistency and then applies the
        theme specified in ``appconfig.toml``.
        """

        # This provides a consistent appearance across all platforms before applying QSS styles.
        self.setStyle("Fusion")

        qss_content: str = er._load_theme()

        # Loading theme to UI
        self.setStyleSheet(qss_content)
        self.setPalette(self.style().standardPalette())

    def change_theme(self, new_theme: str) -> None:
        """
        Dynamically changes the application's visual theme at runtime.

        :param new_theme: The name of the new theme to apply. This should
                          correspond to a theme folder in your project.
        :type new_theme: str
        """

        if new_theme != Settings.get("ui.theme", None):

            Settings.set("ui.theme", new_theme)

            # Update theme
            self._set_theme()

    def _set_content(self) -> None:
        """
        Loads all static text content based on the current language setting.
        """

        if lang := Settings.get("ui.language"):
            er._load_static(lang)

    def change_language(self, new_language: str) -> None:
        """
        Dynamically changes the application's language at runtime.

        This will reload all text content from the ``.fluml`` files
        corresponding to the new language.

        :param new_language: The code for the new language (e.g., "en", "es").
        :type new_language: str
        """

        Settings.set("ui.language", new_language)

        # Update text content
        self._set_content()