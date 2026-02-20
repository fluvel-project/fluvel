# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import importlib
from typing import TypeVar

from PySide6.QtWidgets import QWidget

# Tip-helpers
from fluvel.utils.tip_helpers import AllWidgetsTypes

TWidget = TypeVar(name="TWidget", bound=QWidget)

class Factory:
    """
    Manages the creation of reusable, customized TWidget components.

    This class provides a decorator-based system to define new, pre-configured
    component types from base SKWidgets.

    :cvar _stock: A cache dictionary to store imported widget classes.
    :type _stock: dict[str, Type[TWidget]]
    """

    _stock: dict[str, type[TWidget]] = {}

    class Target:
        """
        An internal helper class to manage the dynamic import of widgets.

        This class handles the logic for dynamic importing and caching of
        TWidget classes, ensuring that each widget module is loaded only once.

        :ivar WidgetClass: The imported TWidget class.
        :type WidgetClass: Type[TWidget]
        """

        def __init__(self, widget_target: str):
            """
            Initializes the Target and loads the target widget class into the cache.

            :param widget_target: The class name of the widget to import.
            :type widget_target: str
            """

            if widget_target not in Factory._stock:
                widget_module = importlib.import_module(
                    f"fluvel.components.widgets.{widget_target}"
                )

                Factory._stock[widget_target] = getattr(widget_module, widget_target)

            self.WidgetClass = Factory._stock[widget_target]


def Component(target: AllWidgetsTypes):
    """
    A decorator that turns a configuration function into a component factory.

    The decorated function becomes a new component that, when called, creates
    an instance of the target widget with the specified configuration.

    :param target: The class name of the base widget to create (e.g., "FButton").
    :type target: str
    :returns: A decorator that produces a TWidget component factory.
    :rtype: callable

    Example
    -------
    .. code-block:: python

        # In components/custom.py
        from fluvel.composer import Component

        @Component("FButton")
        def PrimaryButton(text: str):
            return {
                "text": text,
                "style": "primary font-bold"
            }

        # In a View
        from components.custom import PrimaryButton
        ...
        with self.Vertical() as v:

            # 1) Creates an FButton with text="Submit" and style="primary bold"
            v.add_widget(PrimaryButton(text="Submit"))

            # 2) or create a method to speed up adding the factory component to the layout
            v.PrimaryButton = v.from_factory(PrimaryButton)
            v.PrimaryButton(text="Submit")
    """

    object_target = Factory.Target(target)

    def decorator(func):
        @functools.wraps(func)
        def component_wrapper(*args, **user_kwargs) -> TWidget:
            base_config = func(*args, **user_kwargs)

            return object_target.WidgetClass(**base_config)

        return component_wrapper

    return decorator
