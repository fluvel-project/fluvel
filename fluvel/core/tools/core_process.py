# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Any

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QWidget


def configure_process(obj: QWidget, mapping: dict[str, str], **kwargs: dict[str, Any]) -> None:
    """
    Configure properties, methods, and signals of a PySide6 object in a generic way.

    This function is a central component of Fluvel that allows dynamic configuration
    of widgets, decoupling the names of the arguments from their
    corresponding methods in PySide6.

    Args:
        obj (object): The PySide6 object instance to be configured (e.g. QWidget, QPushButton).
        mapping (dict): A dictionary that maps argument names to method or signal names.
        **kwargs (any): Configuration arguments that will be processed.
    """
    for key, value in kwargs.items():

        if method_name := mapping.get(key):
            # Obtaining the method through its name
            attr = getattr(obj, method_name)

            if isinstance(attr, SignalInstance):
                attr.connect(value)

            else:
                if isinstance(value, (tuple, list)):
                    try:
                        # Try this if the arguments need to be passed positionally
                        attr(*value)
                    except TypeError:
                        # Attempting to pass the tuple/list as a single argument
                        attr(value)

                else:
                    attr(value)
