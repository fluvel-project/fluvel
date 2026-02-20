# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent

# PySide6
from PySide6.QtWidgets import QFrame

# Fluvel
from fluvel.core.abstract.FWidget import FWidget, FWidgetKwargs

class FContainerKwargs(FWidgetKwargs, total=False):
    drag_window: bool


class FContainer(QFrame, FWidget):
    _QT_PROPERTY_MAP = {}

    def __init__(self, **kwargs: Unpack[FContainerKwargs]):
        super().__init__()

        # FluvelWidget Defaults
        self._set_defaults()

        # Movable functionality
        self.isMovable = kwargs.pop("drag_window", False)
        self.dragging = False
        self.offset = QPoint()

        if kwargs:
            self.configure(**kwargs)

    def configure(self, **kwargs: Unpack[FContainerKwargs]) -> None:
        if drag_window := kwargs.get("drag_window"):
            self.isMovable = drag_window

        super().configure(**kwargs)

    def mousePressEvent(self, event: QMouseEvent):
        if self.isMovable and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True

            # Calcular la posición del cursor respecto a la ventana principal
            parent_window = self.window()  # Obtiene la QMainWindow principal

            self.offset = event.globalPosition().toPoint() - parent_window.frameGeometry().topLeft()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isMovable and self.dragging:
            parent_window = self.window()

            # Mueve la ventana principal (MainWindow)
            parent_window.move(event.globalPosition().toPoint() - self.offset)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.isMovable and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)
