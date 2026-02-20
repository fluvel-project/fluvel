# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TYPE_CHECKING
from dataclasses import dataclass
from functools import partial
from collections.abc import Callable

# PySide6
from PySide6.QtWidgets import QStackedWidget

# Fluvel
from fluvel.core.abstract.AbstractPage import AbstractPage
from fluvel.core.AppWindow import AppWindow
from fluvel.engines import PageStyles
from fluvel.core.exceptions.exceptions import RouteNotFoundError

# Composer
from fluvel.composer.Animator import Animator

if TYPE_CHECKING:
    from fluvel.core.App import App


class Router:
    """
    Manages the navigation flow and registration of views (pages) within the application.

    The Router is a static utility class that uses the main main_window's central widget
    (:class:`PySide6.QtWidgets.QStackedWidget`) to display views. It handles
    lazy instantiation of views and provides methods for animation during transitions.
    """

    @dataclass(slots=True)
    class Route:
        """
        Data structure representing a registered application route

        :ivar path: A unique path for each route (e.g., "login")
        :type path: str

        :ivar page_class: The uninstantiated class of the view, decorated by :func:`route`.
        :type page_class: Type[:class:`~fluvel.core.abstract.AbstractPage.AbstractPage`]

        :ivar page_instance: The actual instance of the view after it has been shown for the first time.
        :type page_instance: :class:`~fluvel.core.abstract.AbstractPage.AbstractPage`
        """

        path: str
        page_class: type[AbstractPage]
        page_instance: AbstractPage = None

    _window: AppWindow
    _routes: dict[str, Route] = {}
    _current_route: Route = None

    @classmethod
    def init(cls, app: "App", main_window: AppWindow) -> None:
        """
        Initializes the router by linking it to the main application main_window.

        This method must be called before registering or showing any routes.
        It also sets global variables on the :class:`~fluvel.core.abstract.AbstractPage.AbstractPage`
        base class for access to the root main_window components.

        :param main_window: The main application main_window instance containing the central widget.
        :type main_window: :class:`~fluvel.core.AppWindow.AppWindow`
        :rtype: None
        """
        cls._window = main_window
        AbstractPage._set_globals(app, cls._window)

    @classmethod
    def show(cls, path: str, animation: str | None = "fade_in") -> None:
        """
        Displays the view assigned to the given route path in the central widget
        of the main main_window, optionally applying an animation.

        Views are instantiated **lazily**: the view's ``build()`` method is only called
        the first time the view is requested via this method.

        :param path: The path of the route assigned to the view (e.g., "home").
        :type path: str
        :param animation: The path of the animation to display during the transition (e.g., "fade_in").
                          If :obj:`None`, no animation is applied.
        :type animation: str or None

        :raises RouteNotFoundError: If the provided route ``path`` was not found in the registered routes.
        :rtype: None
        """

        # if a view with the route path does not exist
        if path not in Router._routes:
            raise RouteNotFoundError(
                f"The @route '{path}' is not associated with any page; it may be misspelled or may not exist."
            )

        # The route (Router.Route)
        route = Router._routes[path]

        # The central widget (QStackedWidget)
        central_widget: QStackedWidget = cls._window.central_widget

        if not route.page_instance:
            # Instantiate the view
            route.page_instance = route.page_class()
            route.page_instance.build()

            # Load styles after build()
            styles = PageStyles.getall()
            route.page_instance.setStyleSheet(styles)

            # Add view container to QStackedWidget stack
            central_widget.addWidget(route.page_instance)

        if cls._current_route != route:
            # Set current route
            cls._current_route = route

            # Show the view in the central widget
            target_widget = route.page_instance
            central_widget.setCurrentWidget(target_widget)

            # Initialize animation
            if animation:
                anim = getattr(Animator, animation)(target_widget)
                anim.start()

    @classmethod
    def as_show(cls, path: str, animation: str | None = "fade_in") -> Callable[[], None]:
        """
        Returns a partial object that, when called, 
        executes the Router.show method with the passed parameters

        :param path: The path of the route assigned to the view (e.g., "home").
        :type path: str
        :param animation: The path of the animation to display during the transition (e.g., "fade_in").
                          If :obj:`None`, no animation is applied.
        :type animation: str or None

        :returns: The :class:`functools.partial` object
        :rtype: Callable[[], None]
        """
        return partial(cls.show, path, animation)

def route(path: str):
    """
    Decorator used to register a view class with the :class:`Router`.

    The view class is linked to the provided route path, allowing it to be displayed
    via :meth:`Router.show`. This decorator ensures that if a view with the same
    path is decorated again, the view class is simply updated.

    :param path: The unique path used to identify the view in the router (e.g., "login").
    :type path: str
    :returns: A wrapper that accepts the view class.
    :rtype: callable

    Example
    -------
    .. code-block:: python

        from fluvel import Page, route

        @route("login")
        class LoginPage(Page):
            def build(self):
                # ... UI implementation ...
                pass
    """

    def wrapper(page_class: type[AbstractPage]):
        if path in Router._routes:
            Router._routes[path].page_class = page_class
        else:
            Router._routes[path] = Router.Route(path, page_class)
        return page_class

    return wrapper
