# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import Unpack

from PySide6.QtGui import QImage, QMovie, QPicture, QPixmap

# PySide6
from PySide6.QtWidgets import QLabel, QWidget

from fluvel.core.abstract.FTextWidget import FTextWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs

# Fluvel core utils
from fluvel.core.enums import (
    Alignment,
    AlignmentTypes,
    TextFormat,
    TextFormatTypes,
    TextInteraction,
    TextInteractionTypes,
)
from fluvel.i18n.I18nTextVar import I18nTextVar


class FLabelKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FLabel."""

    text: str | I18nTextVar
    wordwrap: bool
    align: AlignmentTypes
    indent: int
    margin: int
    pixmap: QPixmap | QImage
    movie: QMovie
    picture: QPicture
    open_links: bool
    scaled_contents: bool
    format: TextFormatTypes
    flags: TextInteractionTypes | list[TextInteractionTypes]
    buddy: QWidget

    # Signals
    on_link_hovered: Callable
    on_link_activated: Callable


class FLabel(QLabel, FWidget, FTextWidget):
    """Fluvel's Label component class, wrapping QLabel."""

    _BINDABLE_PROPERTY = "text"
    _BINDABLE_SIGNAL = None

    _QT_PROPERTY_MAP = {
        "text": "setText",
        "align": "setAlignment",
        "wordwrap": "setWordWrap",
        "indent": "setIndent",
        "margin": "setMargin",
        "open_links": "setOpenExternalLinks",
        "pixmap": "setPixmap",
        "movie": "setMovie",
        "picture": "setPicture",
        "scaled_contents": "setScaledContents",
        "format": "setTextFormat",
        "flags": "setTextInteractionFlags",
        "on_link_hovered": "linkHovered",
        "on_link_activated": "linkActivated",
    }

    def __init__(self, **kwargs: Unpack[FLabelKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FLabelKwargs]) -> None:
        # 1. Manage specific properties of FTextWidget subclasses
        kwargs = self._apply_texts(**kwargs)

        # 2. Perform specific type conversions (e.g., Alignment.get)
        if align := kwargs.get("align"):
            kwargs["align"] = Alignment.get(align)

        if format := kwargs.get("format"):
            kwargs["format"] = TextFormat.get(format)

        if flags := kwargs.get("flags"):
            kwargs["flags"] = TextInteraction.get(flags)

        # 3. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()

        # 2. Manage Specific Qt configuration (e.g., setFocusPolicy, setCursor)

        # By default, it accepts the opening of
        # external links
        self.setOpenExternalLinks(True)

        # By default, its text format is RichText.
        self.setTextFormat(TextFormat.RICH)
