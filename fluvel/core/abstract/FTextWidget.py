# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Any, Final

# Fluvel I18n
from fluvel.i18n.I18nTextVar import I18nTextVar

MAPPING: Final[dict[str, str]] = {
    "text": "setText",
    "plain_text": "setPlainText",
    "placeholder": "setPlaceholderText",
    "tooltip": "setToolTip",
    "menu_title": "setTitle",
    "title": "setWindowTitle",
    "format": "setFormat",
}

MAPPING_KEYS: Final[frozenset[str]] = frozenset(MAPPING)


class FTextWidget:
    """
    Base class for text widgets that centralizes the management of static and dynamic content.
    """

    def _apply_texts(self, **kwargs) -> dict[str, Any]:
        """
        Processes and returns widget arguments to handle static and dynamic content.

        Searches for text keys (`MAPPING`) to determine whether the content should be
        managed by a :class:`~fluvel.i18n.I18nTextVar.I18nTextVar`.

        :param kwargs: Widget constructor arguments.
        :type kwargs: dict
        :returns: A dictionary with the processed arguments (e.g., "text" or "placeholder"
                        updated with the string variable value).
        :rtype: dict
        """
        for key in kwargs.keys() & MAPPING_KEYS:
            kwargs[key] = self._link_to_string_var(kwargs[key], MAPPING[key])
        return kwargs

    def _link_to_string_var(self, text: str, method: str) -> str:
        """
        If the text is an I18nTextVar, connect its signal to the widget's 
        setter method and return the string value.
        """
        if isinstance(text, I18nTextVar):
            text.setParent(self)
            text.valueChanged.connect(getattr(self, method))
            return text.value
        return text
