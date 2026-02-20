# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from PySide6.QtCore import Property, QEasingCurve, QPoint, QPropertyAnimation, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter

from fluvel.components.widgets.FCheckBox import FCheckBox, FCheckBoxKwargs


class FSwitchKwargs(FCheckBoxKwargs, total=False):
    bg_color: str
    circle_color: str
    active_color: str
    animation_curve: QEasingCurve
    icon_off: QIcon
    icon_on: QIcon
    icon_size: tuple[int, int]

class FSwitch(FCheckBox):
    """
    Fluvel's native Switch component. 
    A modern toggle with smooth color and position animations.
    """

    _BINDABLE_PROPERTY = "checked"
    _BINDABLE_SIGNAL = "stateChanged"
    
    CIRCLE_PADDING = 3

    def __init__(self, **kwargs: Unpack[FSwitchKwargs]):
        kwargs.setdefault("size", (45, 24))
        super().__init__(**kwargs)

        # Colores y estado
        self._bg_color = QColor(kwargs.get("bg_color", "#777777"))
        self._active_color = QColor(kwargs.get("active_color", "#2E94D8"))
        self._circle_color = QColor(kwargs.get("circle_color", "#FFFFFF"))
        
        # Animación de posición e interpolación de color
        self._circle_position = self.get_end_position(self.isChecked())
        self._color_progress = 1.0 if self.isChecked() else 0.0

        # Animación principal
        self.animation = QPropertyAnimation(self, b"anim_progress", self)
        self.animation.setEasingCurve(kwargs.get("animation_curve", QEasingCurve.Type.InOutCubic))

        self.animation.setDuration(250)

        # Iconos
        self._icon_off = kwargs.get("icon_off")
        self._icon_on = kwargs.get("icon_on")
        self._icon_size = kwargs.get("icon_size", (14, 14))

        self.stateChanged.connect(self._start_animation)
    
    @Property(float)
    def anim_progress(self):
        return self._color_progress

    @anim_progress.setter
    def anim_progress(self, value):
        self._color_progress = value
        start = self.get_end_position(False)
        end = self.get_end_position(True)
        self._circle_position = start + (end - start) * value
        self.update()

    def get_end_position(self, checked: bool) -> float:
        diameter = self.height() - (2 * self.CIRCLE_PADDING)
        if checked:
            return float(self.width() - diameter - self.CIRCLE_PADDING)
        return float(self.CIRCLE_PADDING)

    def _start_animation(self, state: int):
        self.animation.stop()
        self.animation.setEndValue(1.0 if state else 0.0)
        self.animation.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.width(), self.height()).adjusted(0.5, 0.5, -0.5, -0.5)
        
        if not self.isEnabled():
            bg = QColor("#D0D0D0")
        else:
            bg = self._interpolate_color(self._bg_color, self._active_color, self._color_progress)

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bg)
        p.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        diameter = self.height() - (2 * self.CIRCLE_PADDING)
        thumb_rect = QRectF(
            self._circle_position,
            self.CIRCLE_PADDING,
            diameter,
            diameter
        )
        
        p.setBrush(self._circle_color)
        p.drawEllipse(thumb_rect)

        current_icon = self._icon_on if self.isChecked() else self._icon_off
        if current_icon:
            icon_w, icon_h = self._icon_size
            icon_rect = QRectF(
                thumb_rect.center().x() - icon_w / 2,
                thumb_rect.center().y() - icon_h / 2,
                icon_w,
                icon_h
            ).toRect()
            current_icon.paint(p, icon_rect, Qt.AlignmentFlag.AlignCenter)

        p.end()

    @staticmethod
    def _interpolate_color(c1: QColor, c2: QColor, fraction: float) -> QColor:
        r = c1.red() + (c2.red() - c1.red()) * fraction
        g = c1.green() + (c2.green() - c1.green()) * fraction
        b = c1.blue() + (c2.blue() - c1.blue()) * fraction
        return QColor(int(r), int(g), int(b))

    def hitButton(self, pos: QPoint) -> bool:
        return self.rect().contains(pos)