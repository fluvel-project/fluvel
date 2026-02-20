# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Any, Final, TypedDict
import itertools

from fluvel.core.enums import (
    AlignmentTypes,
    Cursor,
    CursorTypes,
    SizePolicy,
    SizePolicyTypes,
    WidgetAttribute,
    WidgetAttributeTypes,
)

# Core process
from fluvel.core.tools.core_process import configure_process

# Fluvel
from fluvel.engines import PageStyles, QSSProcessor

# State Manager
from fluvel.reactive.StateManager import StateManager


class FWidgetKwargs(TypedDict, total=False):
    """
    Keyword arguments for configuring FWidget.

    Defines optional parameters that can be passed to :class:`~fluvel.core.abstract_modes.FWidget.FWidget`
    and its subclasses to configure styles, state bindings,
    size policies, and other widget attributes.
    """

    # Fluvel's own properties for F-Widgets
    bind: str | list[str]
    style: str

    # Layout
    alignment: AlignmentTypes
    stretch: int

    # --- QWidgets base properties ---
    property: tuple[str, Any]

    size_policy: SizePolicyTypes | tuple[SizePolicyTypes, SizePolicyTypes]
    attributes: list[WidgetAttributeTypes]

    # State/Interaction
    enabled: bool
    visible: bool

    # User Help
    tooltip: str | list[str]
    status_tip: str

    # Resize
    size: tuple[int, int] | list[int]
    min_size: tuple[int, int] | list[int]
    max_size: tuple[int, int] | list[int]
    width: int
    height: int
    min_w: int
    min_h: int
    max_w: int
    max_h: int

    # Interface Property
    cursor: CursorTypes


class FWidgetMixin:
    _id_counter = itertools.count(1)

    def set_size_policy(
        self, policy: SizePolicyTypes | tuple[SizePolicyTypes, SizePolicyTypes]
    ) -> None:
        self.setSizePolicy(SizePolicy.get(policy))

    def set_cursor(self, cursor: CursorTypes) -> None:
        self.setCursor(Cursor.get(cursor))

    def set_attributes(self, attrs: list[str]) -> None:
        for attr in attrs:
            self.setAttribute(WidgetAttribute.get(attr), True)

    def set_style(self, style: str) -> None:
        """
        Applies QSS (Qt Style Sheet) styles to the component.

        The style is configured by setting the object's ``class`` property (to
        handle multiple classes) and then processing the entire style string through
        :class:`QSSProcessor` to apply the visual style using
        :meth:`PySide6.QtWidgets.QWidget.setStyleSheet`.

        :param style: String of QSS classes to apply.
        :type style: str
        :rtype: None
        """
        current_class = self.property("class")

        if not current_class:
            full_style = style
        else:
            # Using sets to avoid duplicates
            classes = set(current_class.split())
            new_classes = style.split()
            classes.update(new_classes)
            full_style = " ".join(classes)

        if full_style:
            self.setProperty("class", full_style)
            parsed_styles = QSSProcessor.process(full_style, self.class_name, self.obj_name)
            PageStyles.add(parsed_styles)
            # self.setStyleSheet(parsed_styles)

    def bind(self, binding_string: str) -> None:
        """
        Creates a binding between the widget and Fluvel's State Manager.

        Allows the widget's state to be automatically synchronized with one or more
        variables within the application's :class:`~fluvel.core.State.State` object.

        If ``binding_string`` is a list, it binds to each of the keys.

        :param binding_string: A string with the key or a list of keys to bind.
        :type binding_string: str or list[str]
        :rtype: None
        """

        if isinstance(binding_string, str):
            StateManager.bind(self, binding_string)

        elif isinstance(binding_string, list):
            for b in binding_string:
                StateManager.bind(self, b)

        elif binding_string is None:
            return

        else:
            raise TypeError(
                f"Invalid binding type '{type(binding_string).__name__}'. The 'bind' method must accept a string (str) or a list of strings."
            )


MAPPING: Final[dict[str, Callable]] = {
    "bind": FWidgetMixin.bind,
    "style": FWidgetMixin.set_style,
    "size_policy": FWidgetMixin.set_size_policy,
    "cursor": FWidgetMixin.set_cursor,
    "attributes": FWidgetMixin.set_attributes,
}

MAPPING_KEYS: Final[frozenset[str]] = frozenset(MAPPING)


class FWidget(FWidgetMixin):
    """
    Base class for all Fluvel user interface components.

    Provides essential methods for initial configuration, style management
    (QSS), state binding, and internal object configuration, acting
    as an abstraction layer over PySide6 widgets.
    """
    _BINDABLE_PROPERTY: str = None
    _BINDABLE_SIGNAL: str = None
    _QT_PROPERTY_MAP: dict[str, str] = {}

    _QT_PROPERTY_BASE_MAP = {
        "property": "setProperty",
        "size_policy": "setSizePolicy",
        "tooltip": "setToolTip",
        "enabled": "setEnabled",
        "visible": "setVisible",
        "size": "setFixedSize",
        "width": "setFixedWidth",
        "height": "setFixedHeight",
        "min_w": "setMinimumWidth",
        "min_h": "setMinimumHeight",
        "max_w": "setMaximumWidth",
        "max_h": "setMaximumHeight",
        "min_size": "setMinimumSize",
        "max_size": "setMaximumSize",
        "cursor": "setCursor",
    }

    def __init_subclass__(cls):
        # A map is created to configure the Widget's properties
        # This is done by combining the _QT_PROPERTY_BASE_MAP of FWidget
        # and the specific QT_PROPERTY_MAP of each Widget
        QT_MAP_TO_CONFIGURE = FWidget._QT_PROPERTY_BASE_MAP.copy()
        QT_MAP_TO_CONFIGURE.update(cls._QT_PROPERTY_MAP)
        cls.QT_MAP_TO_CONFIGURE = QT_MAP_TO_CONFIGURE

    def _set_defaults(self) -> None:
        """
        Sets the internal default settings for :class:`FWidget`.

        Initializes the ``class_name`` attribute with the class name (useful for
        :class:`~fluvel.parsers.qss_processor.QSSProcessor`), and sets a unique object name (``obj_name``)
        based on the memory ID to facilitate the application of instance-specific QSS styles.

        :rtype: None
        """
        self.class_name: str = type(self).__name__
        # Setting the object name to apply QSS styles
        self.obj_name: str = f"{self.class_name}_{next(self._id_counter)}"
        self.setObjectName(self.obj_name)

    def configure(self, **kwargs):
        """
        Configures the base widget by applying keyword arguments.

        This method processes arguments such as ``bind``, ``style``, ``size_policy``, and
        ``attributes`` defined in :class:`~fluvel.core.abstract.FWidget.FWidgetKwargs`, applying the
        corresponding settings through the internal methods of
        this class and PySide6. Unused arguments are returned.

        .. note::
            Layout-related arguments (such as ``alignment`` and ``stretch``)
            are left in ``kwargs`` to be processed by the layout manager
            containing this widget.

        :param kwargs: Dictionary of configuration arguments (FWidgetKwargs).
        :type kwargs: dict
        :returns: A dictionary with the remaining arguments (not consumed by FWidget).
        :rtype: dict
        """

        for key in kwargs.keys() & MAPPING_KEYS:
            MAPPING[key](self, kwargs.pop(key))

        if kwargs:
            configure_process(self, self.__class__.QT_MAP_TO_CONFIGURE, **kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Allows configuration of the widget using dictionary syntax.

        Acts as a shortcut for the method :meth:`~fluvel.core.abstract.FWidget.FWidget.configure`.

        Example: ``widget["style"] = "bg-slate-100"`` is equivalent to
        ``widget.configure(style="bg-slate-100")``.

        :param key: The name of the parameter to configure (e.g., "style", "bind").
        :type key: str
        :param value: The value to assign to the parameter.
        :type value: Any
        :rtype: None
        """
        self.configure(**{key: value})
