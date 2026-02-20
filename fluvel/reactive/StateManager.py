# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import re
from collections.abc import Callable
from re import Pattern

from PySide6.QtCore import Slot

# PySide6
from PySide6.QtWidgets import QWidget

# Exceptions
from fluvel.core.exceptions.state_manager import FluvelBindingError, FluvelStateError

# Fluvel
from fluvel.reactive import Model, ModelStore


class Formatter:
    FORMATTER_PATTERN: Pattern[str] = re.compile(
        r"""
        ^\s*
        %.?(?P<filter>.*?)?         # Optional filter (%..2f)
        \s*
        ['\"](?P<template>.*?)['\"] # Optional template ('Temperature: %v')
        \s*$
        """,
        re.VERBOSE,
    )
    """
    RegEx to parse the format suffix:
    Example: % 'My value: %v'
    Capture: <My value: %v> in the 'template' group.
    """

    SINGLE_FILTER_PATTERN: Pattern[str] = re.compile(r"^\s*%\.(?P<filter>.*?)$")

    _FILTERS: dict[str, Callable] = {
        # Numeric Filters
        # The ".1f", ".2f", etc. are defined in Formatter.get_filter()
        "percent": lambda v: f"{v * 100:.0f}%",
        "int": int,
        "abs": abs,
        "round": round,
        # String Filters
        "lower": lambda v: str(v).lower(),
        "title": lambda v: str(v).title(),
        "upper": lambda v: str(v).upper(),
        "cap": lambda v: str(v).capitalize(),
        "strip": lambda v: str(v).strip(),
        "len": len,
        # Boolean Filters
        "invert": lambda v: not v,
    }

    @classmethod
    def decode(cls, format_string: str) -> tuple[Callable | None, str]:
        """
        Parses the format string (%filter 'template') and returns
        (template_string, filter_function).
        """

        if format_string.strip() == "%":
            return None, "%v"

        match = cls.FORMATTER_PATTERN.match(format_string)
        filter_match = cls.SINGLE_FILTER_PATTERN.match(format_string)

        if match:
            filter_name = match.group("filter") or ""
            template = match.group("template") or "%v"
            filter_fn = None

            if filter_name:
                filter_fn = cls.get_filter(filter_name)

            return filter_fn, template

        elif filter_match:
            filter_fn = cls.get_filter(filter_match.group("filter"))
            return filter_fn, "%v"

        raise FluvelBindingError(f"Invalid formatter syntax: '{format_string}'")

    @classmethod
    def get_filter(cls, filter_name: str) -> Callable:
        filter_fn = cls._FILTERS.get(filter_name)

        if filter_fn:
            return filter_fn

        # Dynamic Numeric Filter Check (e.g., .5f, .10f)
        match = re.match(r"(\.\d+f)", filter_name)
        if match:
            return lambda v: f"{v:{filter_name}}" if v is not None else ""

        raise FluvelBindingError(f"Unknown formatter filter: '{filter_name}'")


class StateManager:
    """
    Static Core class that manages the binding
    of all :class:`"Model"` in the application.

    It is the entry point for Fluvel's reactive state system.
    """

    BIND_PATTERN: Pattern[str] = re.compile(
        r"""
        ^
        (?P<property>[~]?[\w]*)      # Widget property (text or ~text)
        :?                           # Optional property separator
        (?P<signal>[\w]*)            # Widget signal (textChanged)
        :?                           # Optional signal separator
        @(?P<ref>[\w]+)              # Model ref (@vm)
        \.                           # Dot separator
        (?P<key>[\w]+)               # Model key (volume)
        (?P<formatter>.*?)?          # Optional formatter
        $                            
        """,
        re.VERBOSE,
    )
    """
    Regular expression for analyzing Fluvel *binding* syntax.
    
    **Expected Format**
        [widget_property][:widget_signal]:@model_alias.status_key

    **Examples**
    * ``@testmodel.username`` (**Level 1**: Default unidirectional/bidirectional binding. Depends on the Widget)
    * ``text:@testmodel.username`` (**Level 2**: Explicit unidirectional binding 'Model -> View')
    * ``text:textChanged:@testmodel.username`` (**Level 3**: Explicit Bidirectional binding 'Model <-> View')
    * ``~text:textChanged:@testmodel.username`` (**Level 4**: Inverted unidirectional binding 'View -> Model')

    :type: :class:`~typing.Pattern`
    """

    @classmethod
    def bind(cls, widget: QWidget, bind_string: str) -> None:
        """
        Establishes the data binding between a widget property and a state.

        This is the central method that implements two-way and one-way reactivity.
        It analyzes the binding string and configures the signal connections.

        :param widget: The PySide6 widget instance to bind.
        :type widget: :class:`PySide6.QtWidgets.QWidget`
        :param bind_string: The binding string with the format ``[prop][:signal]:@ref.key``.
        :type bind_string: str

        :raises FluvelBindingError: If the syntax of the binding string is invalid.
        :raises FluvelStateError: If the ref or state key is not found.
        :rtype: None
        """

        _match = cls.BIND_PATTERN.match(bind_string)
        parsed_binding = _match.groupdict()

        if not _match:
            raise FluvelBindingError(
                f"Invalid binding syntax: '{bind_string}'. "
                "Expected format: 'property:signal:@ref.key'."
                "Ex: '@vm.volume' or 'text:@h.username' or 'value:rangeChanged:@global.theme'."
            )

        ref = parsed_binding.get("ref")
        key = parsed_binding.get("key")
        model = ModelStore.get_model(ref)

        filter_fn, template = cls.decode_formatter(parsed_binding)
        prop_name, signal_name, to_model_only = cls.decode_level(parsed_binding, widget)

        # Only use one-way binding if it's not a level 4 binding
        # (where the widget isn't required to listen to the model, but rather the other way around)
        if not to_model_only:
            cls.set_unidirectional_binding(widget, model, key, prop_name, filter_fn, template)

        # Perform bidirectional binding only if signal_name is provided
        if signal_name:
            if key in type(model)._computeds:
                raise FluvelBindingError(
                    f"The computed state '{key}' of the model '@{ref}' is read-only. "
                    "Two-way binding cannot be used (requires signal_name)."
                )

            cls.set_bidirectional_binding(widget, model, key, signal_name, prop_name)

    @classmethod
    def decode_formatter(cls, parsed_binding: dict[str, str]) -> tuple[Callable | None, str | None]:
        # In 99% of cases, there is no formatter.
        if parsed_binding["formatter"] == "":
            return None, None

        return Formatter.decode(parsed_binding["formatter"])

    @classmethod
    def decode_level(
        self, parsed_binding: dict[str, str], widget: QWidget
    ) -> tuple[str, str, bool]:
        # Obtaining the property and link signal of the widget
        prop_name = parsed_binding.get("property")
        signal_name = parsed_binding.get("signal")

        # Level 1 Binding
        if not prop_name and not signal_name:
            prop_name = widget._BINDABLE_PROPERTY
            signal_name = widget._BINDABLE_SIGNAL

        # Level 2 Binding
        elif prop_name and not signal_name:
            prop_name = prop_name
            signal_name = None

        # Level 3 Binding
        else:
            prop_name = prop_name
            signal_name = signal_name

        # Level 4 Binding
        if to_model_only := prop_name.startswith("~"):
            prop_name = prop_name.lstrip("~")

        return prop_name, signal_name, to_model_only

    @classmethod
    def set_unidirectional_binding(
        cls,
        widget: QWidget,
        model: Model,
        key: str,
        prop_name: str,
        filter_fn: Callable | None,
        template: str | None,
    ) -> None:
        """
        Establishes a unidirectional data link (Model -> View).

        This method connects the centralized model change signal (model.qt_emitter.model_changed)
        to a slot (update_widget) that is responsible for applying filters, template formats,
        and updating the widget property only if the modified key matches the linked key.

        :param widget: The PySide6 widget instance whose property will be updated.
        :type widget: :class:`~PySide6.QtWidgets.QWidget`

        :param model: The Model instance containing the state to be observed.
        :type model: :class:`~fluvel.parsers.ReactiveCore.Model.Model`

        :param key: The specific key of the state (property) within the Model being observed (e.g., 'volume').
        :type key: str

        :param prop_name: The name of the widget property to update (e.g., 'text', 'value').
        :type prop_name: str

        :param filter_fn: The filter function (Callable) to apply to the Model value, or None if there is no filter.
        :type filter_fn: :class:`~typing.Callable` | None

        :param template: The format template (str) to apply (e.g., 'Total: %v'), or None if there is no template.
                        The placeholder '%v' is replaced with the filtered value.
        :type template: str | None

        :rtype: None
        """

        def make_slot():
            if template is None:
                return lambda v: v

            has_filter = filter_fn is not None

            if template == "%v":
                target_type = type(widget.property(prop_name))
                if has_filter:
                    return lambda v: target_type(filter_fn(v))
                return lambda v: target_type(v)

            prefix, _, suffix = template.partition("%v")
            
            if has_filter:
                return lambda v: f"{prefix}{filter_fn(v)}{suffix}"

            return lambda v: f"{prefix}{v}{suffix}"

        transform = make_slot()

        # Inicial value
        widget[prop_name] = transform(getattr(model, key))

        # Reactive Update, the unique ‘modelChanged’ signal for each model is used
        @Slot(dict)
        def update_widget(changes):
            """Slot that updates the widget only if the key matches."""
            if key in changes:
                widget[prop_name] = transform(changes[key])

        model.qt_emitter.modelChanged.connect(update_widget)

    @classmethod
    def set_bidirectional_binding(
        cls, widget: QWidget, model: "Model", key: str, signal_name: str, prop_name: str
    ):
        """
        Establishes a bidirectional data link (Widget -> Model).

        This method connects a specific signal from the widget (e.g., 'textChanged') to a slot
        (update_model) that reads the value of the widget property and writes it back
        to the corresponding key in the Model, provided that the new value is different
        from the current value in the Model.

        .. note::
            The bidirectional link is only used for the 'View -> Model' part of the cycle.
            The 'Model -> View' (unidirectional) part must be set up separately
            using :meth:`~StateManager.set_unidirectional_binding`.

        :param widget: The PySide6 widget instance that emits the change signal.
        :type widget: :class:`PySide6.QtWidgets.QWidget`

        :param model: The Model instance to be modified with the new widget value.
        :type model: :class:`~fluvel.parsers.ReactiveCore.Model.Model`

        :param key: The key of the state within the Model that will be modified (e.g., 'volume').
        :type key: str

        :param signal_name: The name of the widget signal that triggers the change (e.g., 'valueChanged', 'textChanged').
        :type signal_name: str

        :param prop_name: The name of the widget property from which the value will be read (e.g., 'text', 'value').
        :type prop_name: str

        :raises FluvelStateError: If the widget does not have the specified signal.
        :rtype: None
        """

        # Widget signal connection
        try:
            widget_signal = getattr(widget, signal_name)
        except AttributeError:
            raise FluvelStateError(
                f"The widget '{type(widget).__name__}' does not have a signal '{signal_name}'."
            ) from None

        origin_key = f"_origin_{key}"

        def update_model(*args):
            if args:
                widget_value = args[0]
            else:
                widget_value = widget.property(prop_name)

            if widget_value != getattr(model, origin_key):
                setattr(model, key, widget_value)

        widget_signal.connect(update_model)
