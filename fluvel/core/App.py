from typing import Optional, List, TypedDict, Unpack
import sys, importlib
from pathlib import Path

# Fluvel
from fluvel.controllers.main_controller import init_content
from fluvel._user.GlobalConfig import AppConfig
from fluvel.core.Router import Router
from fluvel.controllers.ContentHandler import ContentHandler
from fluvel.core.tools.core_process import configure_process

# Utils
from fluvel.utils.paths import PAGES_DIR

# PySide6
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Exception Handler
from fluvel.core.exceptions.expect_handler import expect

class AppRegisterKwargs(TypedDict, total=False):
    initial         : str
    pages           : Optional[List[str]]
    show_animation  : str

class AppKwargs(TypedDict, total=False):

    name                : str
    display_name        : str
    version             : str
    organization        : str
    domain              : str
    icon                : str
    desktop_file_name   : str

class App:
    """
    The main entry point and controller for a Fluvel application.

    This class define the entire application lifecycle. It is responsible
    for initializing the QApplication, loading the main configuration, creating
    the main window, registering views with the router, and starting the event loop.

    :param window_class: The user-defined subclass of :py:class:`~fluvel.core.AppWindow.AppWindow`
                         that will serve as the main window.
    :type window_class: Type[AppWindow]
    
    :param config_file: The path to the main application configuration file.
                        Defaults to "config.toml".
    :type config_file: str, optional

    Example
    -------
    .. code-block:: python

       # In your app.py
       from fluvel import App

       app = App()
       app.register(initial="home")
       
       if __name__ == "__main__":
           app.run()
    """

    _MAPPING_METHODS = {
        "name"              : "setApplicationName",
        "display_name"      : "setApplicationDisplayName",
        "version"           : "setApplicationVersion",
        "organization"      : "setOrganizationName",
        "domain"            : "setOrganizationDomain",
        "icon"              : "setWindowIcon",
        "desktop_file_name" : "setDesktopFileName",
    }

    def __init__(self, window_module_path: Optional[str] = None, config_file: str = "config.toml") -> None:
        
        # The instance of QApplication
        self._app = QApplication()

        # Start initial config
        self._load(config_file)

        # The instance of AppWindow(QMainWindow)
        self.main_window = self._create_main_window(window_module_path)

        # Start router config
        Router.init(self, self.main_window)

        self.configure(**vars(AppConfig.app))

    def configure(self, **kwargs: Unpack[AppKwargs]) -> None:
        """
        Applies the global application settings (metadata) to the QApplication instance.

        This method is the **central control point** for applying the application identity,
        whether the values come from the **external configuration file** ``config.toml``
        or directly from arguments passed in the **Python code**.
        
        Initializes Qt identity setters, such as the application name, organization,
        domain, and icon. Uses the internal mapping :py:attr:`~fluvel.App._MAPPING_METHODS`
        to dynamically call methods of the :py:class:`~PySide6.QtWidgets.QApplication`.
        
        :param name: The internal name of the application (:py:meth:`~PySide6.QtWidgets.QApplication.setApplicationName`).
        :type name: str
        :param display_name: The user-readable name (:py:meth:`~PySide6.QtWidgets.QApplication.setApplicationDisplayName`).
        :type display_name: str
        :param version: The version of the application (:py:meth:`~PySide6.QtWidgets.QApplication.setApplicationVersion`).
        :type version: str
        :param organization: The name of the organization (:py:meth:`~PySide6.QtWidgets.QApplication.setOrganizationName`).
        :type organization: str
        :param domain: The domain of the organization (:py:meth:`~PySide6.QtWidgets.QApplication.setOrganizationDomain`).
        :type domain: str
        :param icon: The path to the global icon file. Converted to :py:class:`~PySide6.QtGui.QIcon`.
        :type icon: str
        :param desktop_file_name: The identifier for the operating system launcher (:py:meth:`~PySide6.QtWidgets.QApplication.setDesktopFileName`).
        :type desktop_file_name: str
        
        :rtype: None
        """

        if icon_path := kwargs.get("icon"):

            kwargs["icon"] = QIcon(icon_path)

        configure_process(self._app, self._MAPPING_METHODS, **kwargs)

    def _load(self, filename: str) -> None:
        """
        Loads the global application configuration from a TOML or JSON file.
        
        .. note::
           This is an internal method called during initialization. It also
           triggers the initial loading of static content and themes.

        :param filename: The name of the configuration file.
        :type filename: str
        """
        AppConfig.init_config(filename)

        # Se cargan los contenidos estáticos de la ui
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
        sys.exit(self._app.exec())

    @expect.ErrorImportingModule(stop=True)
    def register(self, **kwargs: Unpack[AppRegisterKwargs]) -> None:
        """
        Registers application pages and initializes the :py:class:`~fluvel.core.Router.Router`.

        This method dynamically imports the specified view modules, which allows
        their ``@route`` decorators to register them with the router.

        If the ``pages`` keyword argument is not provided, the method will automatically
        scan the conventional ``ui/pages/`` directory for all Python files and import them.

        :param initial: **(Required)** The name of the route (e.g., ``"login"``) to display first when the application starts.
        :type initial: str

        :param pages: A list of view modules to import (e.g., ``["ui.pages.login.SignInPage", "ui.pages.home.Homepage"]``). 
                      If omitted, all pages in the conventional ``ui/pages/`` directory are automatically detected.
        :type pages: Optional[List[str]]

        :param show_animation: The name of a pre-configured animation to use when displaying the initial view.
        :type show_animation: Optional[str]

        :raises ValueError: If the required argument ``initial`` is not provided.
        """
        initial_view = kwargs.get("initial")
        page_modules = kwargs.get("pages", [])
        animation = kwargs.get("show_animation")

        if initial_view is None:
            raise ValueError("The 'initial' argument is required in register() to show a first view.")

        if not page_modules:
            
            # Creamos una lista para las rutas de cada página
            modules_to_import = []
            
            # Iteramos sobre las carpetas de características (ej. 'login', 'dashboard', 'home')
            page_folders: list[Path] = [page_folder for page_folder in PAGES_DIR.iterdir() if page_folder.is_dir()]

            for page_folder in page_folders:
                
                # Iteramos sobre los archivos .py dentro de cada carpeta, excluyendo __init__.py
                for module_file in page_folder.glob("[!_]*.py"):
                    
                    # Construcctión del path al módulo
                    module_path = f"ui.pages.{page_folder.name}.{module_file.stem}"

                    # Se añade a la lista de módulos a importar
                    modules_to_import.append(module_path)
            
            # Usamos la lista de módulos detectados
            page_modules = modules_to_import

        # Importando los módulos
        for module_path in page_modules:
            importlib.import_module(module_path)
            
        # Show initial view
        Router.show(initial_view, animation)

    def _create_main_window(self, window_module_path: Optional[str]):
        """
        Dynamically imports and instantiates the main window class.

        This internal method is responsible for loading the user-defined
        subclass of :py:class:`~fluvel.core.AppWindow.AppWindow`. By default, it looks
        for a ``MainWindow`` class inside a ``window.py`` module at the
        project root.

        :param window_module_path: The dot-separated path to the module
                                   containing the main window class.
                                   Defaults to "window".
        :type window_module_path: str, optional
        :returns: An instance of the user-defined main window.
        :rtype: fluvel.core.AppWindow.AppWindow
        :raises ImportError: If the specified module cannot be found.
        :raises AttributeError: If the ``MainWindow`` class is not found in the module.
        """
        
        # The default is "window" if no alternative module defining AppWindow is provided.
        window_module_path = "window" if not window_module_path else window_module_path
        
        # Loading module
        window_module = importlib.import_module(window_module_path)

        # Return an instance of MainWindow(AppWindow)
        return window_module.MainWindow()
   
    def _set_static_content(self) -> None:
        """
        Loads and applies all static content, including text and themes.

        This is an internal method that orchestrates the loading of all
        ``.fluml`` content files and the application of QSS stylesheets.
        """

        # Cargando el contenido de texto estático de las vistas
        self._set_content()

        # Aplicando los temas y estilos a los componentes
        self._set_theme()

    def _set_theme(self) -> None:
        """
        Loads and applies the global QSS theme to the application.
        
        It sets the "Fusion" style for consistency and then applies the
        theme specified in ``appconfig.toml``.
        """

        # Esto provee una apariencia consistente en todas las plataformas antes de aplicar los estilos QSS
        self._app.setStyle("Fusion")

        qss_content: str = ContentHandler.process_theme()

        # Cargando el tema a la ui
        self._app.setStyleSheet(qss_content)

    def change_theme(self, new_theme: str) -> None:
        """
        Dynamically changes the application's visual theme at runtime.

        :param new_theme: The name of the new theme to apply. This should
                          correspond to a theme folder in your project.
        :type new_theme: str
        """
        # Change theme
        AppConfig.ui.theme = new_theme

        # Update theme
        self._set_theme()

    def _set_content(self) -> None:
        """
        Loads all static text content based on the current language setting.
        """

        init_content(lang=AppConfig.ui.language)

    def change_language(self, new_language: str) -> None:
        """
        Dynamically changes the application's language at runtime.

        This will reload all text content from the ``.fluml`` files
        corresponding to the new language.

        :param new_language: The code for the new language (e.g., "en", "es").
        :type new_language: str
        """

        # Change language
        AppConfig.ui.language = new_language
        
        # Update text content
        self._set_content()