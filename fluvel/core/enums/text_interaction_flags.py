# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

# PySide6
from PySide6.QtCore import Qt

TextInteractionTypes = Literal[
    "without", "selectable", "editable", "links-selectable", "links-clickable"
]


@final
class TextInteraction:
    WHITOUT = Qt.TextInteractionFlag.NoTextInteraction
    SELECTABLE = Qt.TextInteractionFlag.TextSelectableByMouse
    EDITABLE = Qt.TextInteractionFlag.TextEditable
    LINKS_SELECTABLE = Qt.TextInteractionFlag.LinksAccessibleByMouse
    LINKS_CLICKABLE = Qt.TextInteractionFlag.LinksAccessibleByKeyboard

    __MAP__: dict[TextInteractionTypes, Qt.TextInteractionFlag] = {
        "without": WHITOUT,
        "selectable": SELECTABLE,
        "editable": EDITABLE,
        "links-selectable": LINKS_SELECTABLE,
        "links-clickable": LINKS_CLICKABLE,
    }

    @staticmethod
    def get(
        interaction: TextInteractionTypes | list[TextInteractionTypes],
    ) -> Qt.TextInteractionFlag:
        if isinstance(interaction, str):
            return TextInteraction.__MAP__.get(interaction, TextInteraction.WHITOUT)

        # local binding
        map_get = TextInteraction.__MAP__.get
        whitout_type = TextInteraction.WHITOUT

        if isinstance(interaction, list):
            flags = whitout_type

            for item in interaction:
                flags |= map_get(item, whitout_type)

            return flags

        return whitout_type
