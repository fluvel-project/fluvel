# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from PySide6.QtCore import QEasingCurve, QObject, QPoint, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget


class Animator:
    # Lista para mantener las referencias a las animaciones y efectos
    _active_effects: list[QGraphicsOpacityEffect] = []
    _active_animations: list[QPropertyAnimation] = []

    @classmethod
    def animate(
        cls,
        target: QObject,
        property_name: bytes,
        start_value: float,
        end_value: float,
        duration: int = 400,
        easing: QEasingCurve = QEasingCurve.OutQuad,
    ) -> QPropertyAnimation:
        """
        Crea, configura e inicia un QPropertyAnimation para cualquier propiedad.
        """
        animation = QPropertyAnimation(target, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(easing)

        cls._active_animations.append(animation)

        animation.finished.connect(lambda: cls._active_animations.remove(animation))

        return animation

    @classmethod
    def fade_in(cls, widget: QWidget, duration: int = 800) -> QPropertyAnimation:
        """
        Aplica un efecto de opacidad y lo anima de 0.0 (invisible) a 1.0 (visible).
        """

        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        cls._active_effects.append(opacity_effect)

        animation = cls.animate(
            target=opacity_effect,
            property_name=b"opacity",
            start_value=0.8,
            end_value=1.0,
            duration=duration,
        )

        animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        animation.finished.connect(lambda: cls._active_effects.remove(opacity_effect))

        return animation

    @classmethod
    def fade_out(cls, widget: QWidget, duration: int = 400) -> QPropertyAnimation:
        """
        Anima la opacidad de un widget de 1.0 a 0.0 (desvanecerse).
        """
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        animation = cls.animate(
            target=opacity_effect,
            property_name=b"opacity",
            start_value=1.0,
            end_value=0.5,
            duration=duration,
        )

        # Una vez que la animación termina, ocultamos el widget saliente
        animation.finished.connect(lambda: widget.setHidden(True))
        animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        return animation

    @classmethod
    def slide_in(
        cls, widget: QWidget, direction: str = "right", duration: int = 300
    ) -> QPropertyAnimation:
        """
        Anima la posición (pos) del widget para que se deslice desde un borde
        del contenedor padre hasta su posición de layout final.

        :param direction: 'right' para deslizar desde la derecha, 'left' para deslizar desde la izquierda.
        """

        end_pos = widget.pos()
        parent = widget.parentWidget()

        if not parent:
            raise RuntimeError("slide_in requiere que el widget tenga un padre.")

        if direction == "right":
            start_pos_x = parent.width()
        elif direction == "left":
            start_pos_x = -widget.width()
        else:
            raise ValueError("La dirección debe ser 'right' o 'left'.")

        start_pos = QPoint(start_pos_x, end_pos.y())

        widget.setVisible(True)

        widget.move(start_pos)

        animation = cls.animate(
            target=widget,
            property_name=b"pos",
            start_value=start_pos,
            end_value=end_pos,
            duration=duration,
            easing=QEasingCurve.OutCubic,
        )

        return animation
