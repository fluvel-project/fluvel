# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from PySide6.QtCore import QRectF
from PySide6.QtGui import QImage, QPainter, QPainterPath, QPaintEvent, QPixmap

# Fluvel
from fluvel.components.widgets.containers.FContainer import FContainer, FContainerKwargs


class FImageContainerKwargs(FContainerKwargs, total=False):
    """Argumentos específicos para el contenedor con imagen de fondo."""

    source: str | QPixmap | QImage
    rounded: int
    keep_aspect_ratio: bool
    cover: bool


class FImageContainer(FContainer):
    """
    Contenedor Fluvel que permite imágenes de fondo.
    Hereda de FContainer para soportar arrastre de ventana y estilos.
    """

    def __init__(self, **kwargs: Unpack[FImageContainerKwargs]):
        self._pixmap: QPixmap | None = None
        self._rounded = kwargs.pop("rounded", 0)
        self._keep_aspect = kwargs.pop("keep_aspect_ratio", True)
        self._cover = kwargs.pop("cover", True)
        source = kwargs.pop("source", None)

        super().__init__(**kwargs)

        if source:
            self.set_source(source)

    def set_source(self, source: str | QPixmap | QImage):
        """Cambia la imagen de fondo dinámicamente."""
        if isinstance(source, str):
            self._pixmap = QPixmap(source)
        elif isinstance(source, QImage):
            self._pixmap = QPixmap.fromImage(source)
        else:
            self._pixmap = source
        self.update()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        if not self._pixmap or self._pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )

        rect = QRectF(self.rect())

        if self._cover:
            target_rect = self._calculate_cover_rect(self._pixmap.size(), rect.size())
        else:
            target_rect = self._calculate_aspect_rect(self._pixmap.size(), rect.size())

        if self._rounded > 0:
            path = QPainterPath()
            radius = min(rect.width(), rect.height()) * (self._rounded / 100.0)
            path.addRoundedRect(rect, radius, radius)
            painter.setClipPath(path)

        painter.drawPixmap(target_rect.toRect(), self._pixmap)
        painter.end()

    def _calculate_cover_rect(self, img_size, widget_size) -> QRectF:
        w_ratio = widget_size.width() / img_size.width()
        h_ratio = widget_size.height() / img_size.height()
        ratio = max(w_ratio, h_ratio)
        new_w, new_h = img_size.width() * ratio, img_size.height() * ratio
        return QRectF(
            (widget_size.width() - new_w) / 2, (widget_size.height() - new_h) / 2, new_w, new_h
        )

    def _calculate_aspect_rect(self, img_size, widget_size) -> QRectF:
        w_ratio = widget_size.width() / img_size.width()
        h_ratio = widget_size.height() / img_size.height()
        ratio = min(w_ratio, h_ratio)
        new_w, new_h = img_size.width() * ratio, img_size.height() * ratio
        return QRectF(
            (widget_size.width() - new_w) / 2, (widget_size.height() - new_h) / 2, new_w, new_h
        )
