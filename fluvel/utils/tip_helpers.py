# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal

# ===============
# Used in Factory
# ===============

AllWidgetsTypes = Literal[
    "FLabel",
    "FInput",
    "FButton",
    "FLinkButton",
    "FCheckBox",
    "FRadioButton",
    "FSlider",
    "FProgressBar",
    "FSwitch",
    "IconButton",
]

# =================
# Used in MenuBar
# =================

ActionSignalTypes = Literal["triggered", "toggled", "changed", "hovered"]

ActionPropertyTypes = Literal[
    "Text",
    "Icon",
    "Shortcut",
    "StatusTip",
    "ToolTip",
    "Enabled",
    "Visible",
    "Checkable",
    "MenuRole",
    "Data",
]

StandardActionShortcut = Literal[
    "AddTab",
    "Back",
    "Bold",
    "Close",
    "Copy",
    ""  # Para la definición del Literal, se pone una cadena vacía en la línea anterior
    "Cut",
    "Delete",
    "Contents",  # Ayuda de contenido
    "Find",
    "FindNext",
    "FindPrevious",
    "Forward",
    "HelpContents",  # Lo mismo que Contents
    "Help",  # Ayuda general
    "InsertParagraphSeparator",
    "InsertLineSeparator",
    "Italic",
    "MoveToNextChar",
    "MoveToPreviousChar",
    "MoveToNextWord",
    "MoveToPreviousWord",
    "MoveToNextLine",
    "MoveToPreviousLine",
    "MoveToNextPage",
    "MoveToPreviousPage",
    "MoveToNextSection",
    "MoveToPreviousSection",
    "MoveToEndOfLine",
    "MoveToEndOfBlock",
    "MoveToEndOfDocument",
    "MoveToStartOfLine",
    "MoveToStartOfBlock",
    "MoveToStartOfDocument",
    "MoveByPage",  # Más general que Next/Previous Page
    "MoveToPreviousWord",
    "MoveToNextWord",
    "MoveMode",  # Para activar/desactivar modo de movimiento
    "NextChild",
    "New",
    "Open",
    "Paste",
    "Preferences",  # Preferencias/Opciones
    "PreviousChild",
    "Print",
    "PrintPreview",
    "Properties",  # Propiedades del elemento actual
    "Redo",
    "Refresh",  # Recargar/Actualizar
    "Replace",
    "Save",
    "SaveAs",
    "SelectAll",
    "SelectNextChar",
    "SelectPreviousChar",
    "SelectNextWord",
    "SelectPreviousWord",
    "SelectNextLine",
    "SelectPreviousLine",
    "SelectNextPage",
    "SelectPreviousPage",
    "SelectNextSection",
    "SelectPreviousSection",
    "SelectToEndOfLine",
    "SelectToEndOfBlock",
    "SelectToEndOfDocument",
    "SelectToStartOfLine",
    "SelectToStartOfBlock",
    "SelectToStartOfDocument",
    "SelectTrailingSpaces",
    "Deselect",  # Deseleccionar todo
    "SetTextDirection",  # Establecer dirección del texto (RTL/LTR)
    "StrikeOut",  # Tachado
    "Subscript",
    "Superscript",
    "Underline",
    "Undo",
    "WhatsThis",  # Qué es esto? (para ayuda contextual)
    "ZoomIn",
    "ZoomOut",
    "Zoom",  # Restablecer zoom
    "DeleteStartOfWord",
    "DeleteEndOfWord",
    "DeleteStartOfLine",
    "DeleteEndOfLine",
    "Copy",  # Duplicado por si acaso, eliminar si ya está
    "Paste",  # Duplicado por si acaso, eliminar si ya está
]
