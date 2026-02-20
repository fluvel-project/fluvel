# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import ABC, ABCMeta, abstractmethod
from typing import TYPE_CHECKING

# Fluvel
from fluvel.components.widgets.containers.FContainer import FContainer
from fluvel.core.abstract.LayoutBuilder import LayoutBuilder
from fluvel.core.AppWindow import AppWindow

if TYPE_CHECKING:
    from fluvel.core.App import App

# PySide6
from PySide6.QtCore import QObject, Qt


class VBMeta(type(QObject), ABCMeta):
    """
    Unified Metaclass that resolves conflicts when combining
    :class:`PySide6.QtCore.QObject` and :class:`abc.ABCMeta`.

    All :class:`~fluvel.core.abstract.AbstractPage.AbstractPage` subclasses inherit from this metaclass to ensure
    compatibility with both PySide6's signal/slot system and Python's abstract base classes.
    """

    pass


class AbstractPage(FContainer, ABC, metaclass=VBMeta):
    """
    Abstract base class for creating Pages (views) in Fluvel.

    This class provides the core declarative helper methods (context managers)
    for UI construction, such as :meth:`Vertical`, :meth:`Horizontal`, etc.

    All application pages must inherit from :class:`~fluvel.core.abstract.AbstractPage.AbstractPage` and implement
    the :meth:`build` method.

    :cvar app_root: The instance of the main application class (:class:`~fluvel.core.App.App`).
    :cvar main_window: The instance of the main window container (:class:`~fluvel.core.AppWindow.AppWindow`).
    """

    def __init__(self) -> None:
        """
        Initializes an instance of :class:`~fluvel.core.abstract.AbstractPage.AbstractPage`.
        """
        super().__init__()

        # Valor predeterminado para que las vistas principales
        # puedan recibir eventos de teclado y ratón cuando se muestran.
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    @classmethod
    def _set_globals(cls, app_root: "App", main_window: AppWindow) -> None:
        """
        Sets global references to the application root and main window.

        This is called internally by :class:`~fluvel.core.SKRouter.Router.init`.

        :param app_root: The root application instance.
        :type app_root: :class:`~fluvel.core.SKApp.App`
        :param main_window: The main application window instance.
        :type main_window: :class:`~fluvel.core.SKMainWindow.SKMainWindow`
        :rtype: None
        """
        # The SKApp instance
        cls.app = app_root

        # The AppWindow instance
        cls.main_window = main_window

    @abstractmethod
    def build(self) -> None:
        """
        Abstract method for building the user interface.

        This method **must** be implemented by all classes inheriting from
        :class:`~fluvel.core.abstract.AbstractPage.AbstractPage` and is where the entire UI construction logic resides.
        :rtype: None
        """
        pass


class Page(AbstractPage, LayoutBuilder):
    """
    Concrete class that inherits from :class:`~fluvel.core.abstract.AbstractPage.AbstractPage`
    used for user interface composition via context handlers.
    """

    pass
