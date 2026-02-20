# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPainterPath

# PySide6
from PySide6.QtWidgets import QWidget

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs


class FIconKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FIcon."""

    source: str | QIcon
    size: int
    rounded: int


class FIcon(QWidget, FWidget):
    """Fluvel Component Class Icon, wrapping QIcon."""

    _BINDABLE_PROPERTY = None
    _BINDABLE_SIGNAL = None
    _QT_PROPERTY_MAP = {}

    def __init__(self, **kwargs: Unpack[FIconKwargs]):
        super().__init__()

        # 1. Set default values for Fluvel and Qt
        self._set_defaults()

        # 2. Configure properties
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FIconKwargs]) -> None:
        if size := kwargs.pop("size", None):
            self.setFixedSize(size, size)

        if source := kwargs.pop("source", None):
            self.setSource(source)

        if rounded := kwargs.pop("rounded", None):
            self.setRounded(rounded)

        # 2. Manage generic properties (bind, style, size_policy, etc.)
        super().configure(**kwargs)

    def setSource(self, source: str | QIcon):
        self._source = QIcon(source) if isinstance(source, str) else source
        self.update()

    def setRounded(self, rounded: int):
        self._rounded = rounded
        self.update()

    def paintEvent(self, event):
        if not self._source:
            return
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )

        dpr = self.devicePixelRatioF()
        pixmap_size = self.size() * dpr

        pixmap = self._source.pixmap(pixmap_size)

        rect = QRectF(0, 0, self.width(), self.height())

        if self._rounded > 0:
            path = QPainterPath()
            rx = self.width() * (self._rounded / 100)
            ry = self.height() * (self._rounded / 100)
            path.addRoundedRect(rect, rx, ry)
            painter.setClipPath(path)

        painter.drawPixmap(rect.toRect(), pixmap)
        painter.end()

    def _set_defaults(self) -> None:
        # 1. Establish the generic properties of an F-Widget
        super()._set_defaults()
        self._source = QIcon()
        self._rounded = 0
        self.setFixedSize(24, 24)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
