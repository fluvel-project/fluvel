# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import importlib
import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, QTimer, Signal

# PySide6
from PySide6.QtWidgets import QDockWidget
from watchdog.events import FileSystemEventHandler

# Watchdog
from watchdog.observers import Observer

from fluvel.cli.tools.ClickStyled import echo

# Fluvel
from fluvel.core.Router import Router

# Expect Handler
from fluvel.core.tools.expect_handler import expect

# I18n Fluvel
from fluvel.i18n import I18nLoader, er
from fluvel.reactive import ModelStore
from fluvel.user.UserSettings import Settings
from fluvel.utils.paths import STATIC_DIR, UI_DIR

if TYPE_CHECKING:
    from fluvel.core import App, AppWindow

class ReloaderSignalEmmiter(QObject):
    """
    Emisor de señales para la recarga
    """

    fileModified = Signal()


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, emitter: ReloaderSignalEmmiter):
        super().__init__()
        self.emitter = emitter

    def on_modified(self, event):
        """
        Este método se activa cuando se modifica un archivo.
        """
        if not event.is_directory and event.src_path.endswith(
            (".py", ".qss", ".fluml", ".json", ".xml")
        ):
            self.emitter.fileModified.emit()


class HReloader:
    def __init__(self, window: "AppWindow", root: "App"):
        # App Intances
        self.app_root = root
        self.main_window = window

        # Observer
        self.observer = Observer()
        self.signal_emitter = ReloaderSignalEmmiter()
        self.signal_emitter.fileModified.connect(self.manage_debounce)
        self.event_handler = FileChangeHandler(self.signal_emitter)

        # Timer
        self.reload_timer = QTimer()
        self.reload_timer.setSingleShot(True)
        self.reload_timer.setInterval(20)
        self.reload_timer.timeout.connect(self.on_file_changed)

        self.show_window()

    def show_window(self) -> None:
        """
        Instancia la ventana principal por primera vez y la muestra.
        """
        self.main_window.show()
        self.start_file_monitoring()

    @expect.FileNotFound(
        msg="Error: The 'ui/' or 'static/' directory does not exist. Cannot monitor."
    )
    def start_file_monitoring(self) -> None:
        """
        Inicia el monitoreo de archivos en el directorio 'views'.
        """

        self.observer.schedule(self.event_handler, UI_DIR, recursive=True)
        self.observer.schedule(self.event_handler, STATIC_DIR, recursive=True)
        self.observer.start()
        self.app_root.aboutToQuit.connect(self.stop_file_monitoring)

    def stop_file_monitoring(self) -> None:
        """
        Detiene el monitoreo de archivos de forma segura.
        """
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            echo("[magenta]([HMR] Observer stopped.)")

    def manage_debounce(self) -> None:
        """
        Este nuevo slot se activa con cada evento de archivo.
        En lugar de recargar inmediatamente, (re)inicia el temporizador.
        """
        self.reload_timer.start()

    def on_file_changed(self) -> None:
        """
        Slot que se llama cuando cambia un archivo.
        """
        echo("[yellow]([HMR] Change detected. Reloading UI...)")
        self.reload_and_update()

    @expect.ErrorImportingModule(stop=True)
    def reload_and_update(self) -> None:
        """
        Recarga los módulos de vistas y actualiza el contenido de la ventana.
        """

        self.remove_models()

        self.reload_ui_modules()

        self.update_ui()

    def remove_models(self) -> None:
        
        models = ModelStore.__store__.copy()
        for model in models.values():
            model.unbind()

    def reload_ui_modules(self) -> None:
        modules_to_reload = [m for m in sys.modules.keys() if m.startswith("ui")]

        for module in modules_to_reload:
            if module in sys.modules:
                importlib.reload(sys.modules[module])

    def update_ui(self) -> None:
        """
        Refreshes the entire UI during a hot-reload event.

        This method is called by the :class:`~fluvel.cli.reloader.HReloader` to destroy and recreate
        UI components, ensuring that code changes are reflected visually.

        :param router: The application's Router instance, needed to re-render the current view.
        :type router: :class:`~fluvel.core.Router.Router`
        :rtype: None
        """

        # Recargamos los qss, esto permite editar los
        # estilos en tiempo real
        self.app_root._set_theme()

        # Recargamos el contenido de texto estático
        self.app_root._set_content()

        # Actualizamos la UI
        self.restart_ui()

    def restart_ui(self) -> None:
        # Forzamos al Loader a olvidar el lenguaje actual
        # para que cargue los archivos actualizados
        I18nLoader.current_language = None

        # Recarga física de los diccionarios.
        # No se crearán nuevos objetos I18nVars
        er._load_static(Settings["ui.language"])

        # Limpiamos y volvemos a inicializar el
        # menú principal
        if hasattr(self.main_window, "menu_bar"):
            self.main_window.menu_bar.deleteLater()
            self.main_window._set_menu_bar()

        # Borramos los QDockWidgets
        main_window_children = self.main_window.children()
        for child in main_window_children:
            if isinstance(child, QDockWidget):
                child.deleteLater()

        # Reiniciar Router
        for route in Router._routes.values():
            if route.page_instance:
                # Destruimos el widget contenedor de la vista.
                route.page_instance.deleteLater()
                # Reseteamos la instancia a None.
                route.page_instance = None

        # Finalmente, mostramos la página actualizada
        Router.show(Router._current_route.path)