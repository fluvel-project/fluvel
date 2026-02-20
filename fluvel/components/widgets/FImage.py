# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from PySide6.QtCore import QRectF, QSize
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPaintEvent, QPixmap
from PySide6.QtWidgets import QFrame

# Fluvel Core
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs
from fluvel.core.enums import SizePolicy


class FImageKwargs(FWidgetKwargs, total=False):
    """Specific arguments for FImage."""

    source: str | QPixmap | QImage
    size: int | tuple[int, int]
    rounded: int
    keep_aspect_ratio: bool
    bg_color: str


class FImage(QFrame, FWidget):
    """
    Fluvel's Responsive Image component.
    Draws the image dynamically to allow shrinking and expanding
    while maintaining High-Quality Antialiasing and Rounded Corners.
    """

    _QT_PROPERTY_MAP = {"scaled_contents": "setScaledContents", "size": "setFixedSize"}

    def __init__(self, **kwargs: Unpack[FImageKwargs]):
        super().__init__()

        # Estado interno
        self._pixmap: QPixmap | None = None
        self._rounded: int = 0
        self._keep_aspect: bool = True
        self._bg_color: QColor | None = None

        self._set_defaults()
        self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FImageKwargs]) -> None:
        if "size" in kwargs:
            size = kwargs.pop("size")
            if isinstance(size, int):
                self.setFixedSize(size, size)
            elif isinstance(size, (tuple, list)):
                self.setFixedSize(*size)

        if "rounded" in kwargs:
            self._rounded = kwargs.pop("rounded")

        if "keep_aspect_ratio" in kwargs:
            self._keep_aspect = kwargs.pop("keep_aspect_ratio")

        if "source" in kwargs:
            source = kwargs.pop("source")
            self._pixmap = self._to_pixmap(source)
            self.update()  # Fuerza el repintado

        super().configure(**kwargs)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Dibuja la imagen dinámicamente adaptándose al tamaño actual del widget (self.size()).
        """
        if not self._pixmap or self._pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )

        rect = QRectF(self.rect())

        if self._keep_aspect:
            target_rect = self._calculate_aspect_rect(self._pixmap.size(), rect.size())
        else:
            target_rect = rect

        path = QPainterPath()
        if self._rounded > 0:
            shortest_side = min(target_rect.width(), target_rect.height())
            radius = shortest_side * (self._rounded / 100.0)
            path.addRoundedRect(target_rect, radius, radius)
        else:
            path.addRect(target_rect)

        painter.setClipPath(path)
        painter.drawPixmap(target_rect.toRect(), self._pixmap)

        painter.end()

    def _calculate_aspect_rect(self, img_size: QSize, widget_size: QSize) -> QRectF:
        """Calcula el rectángulo centrado manteniendo el aspect ratio."""
        img_ratio = img_size.width() / img_size.height()
        widget_ratio = widget_size.width() / widget_size.height()

        new_w, new_h = 0.0, 0.0

        if img_ratio > widget_ratio:
            new_w = widget_size.width()
            new_h = new_w / img_ratio
        else:
            new_h = widget_size.height()
            new_w = new_h * img_ratio

        # Centrar
        x = (widget_size.width() - new_w) / 2
        y = (widget_size.height() - new_h) / 2

        return QRectF(x, y, new_w, new_h)

    def _to_pixmap(self, source) -> QPixmap:
        if isinstance(source, str):
            return QPixmap(source)
        if isinstance(source, QImage):
            return QPixmap.fromImage(source)
        return source if isinstance(source, QPixmap) else QPixmap()

    def _set_defaults(self):
        super()._set_defaults()
        self.setMinimumSize(1, 1)
        self.setSizePolicy(SizePolicy.IGNORED, SizePolicy.IGNORED)
