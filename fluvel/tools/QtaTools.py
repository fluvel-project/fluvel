# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict, Unpack

import qtawesome as qta
from PySide6.QtGui import QIcon

# PySide6
from PySide6.QtWidgets import QWidget


class QtaSpinKwargs(TypedDict, total=False):
    interval: int
    step: int
    autostart: bool


@dataclass(slots=True)
class QtaSpin:
    """qta.Spin Metadata."""

    spin_kwargs: QtaSpinKwargs = field(default_factory=dict)

    def __call__(self, widget: QWidget) -> qta.Spin:
        """Genera la instancia qta.Spin enlazada al widget."""
        return qta.Spin(widget, **self.spin_kwargs)


class Qta:
    class Options(TypedDict, total=False):
        color: str
        color_active: str
        color_disabled: str
        color_selected: str
        active: str
        disabled: str
        selected: str
        opacity: float
        scale_factor: float
        offset: tuple[float, float]
        hflip: bool
        vflip: bool
        rotated: int

    class Icon:
        __slots__ = ["src", "color", "options"]

        def __init__(self, src: str = "mdi", color: str = "black", **options: Unpack[Qta.Options]):
            self.src = src
            self.color = color
            self.options = options

        def __repr__(self) -> str:
            return f"{type(self).__name__}({', '.join([f'{v}={repr(getattr(self, v))}' for v in self.__slots__])})"

        def __call__(self, name: str, src: str = None, **options: Unpack[Qta.Options]) -> QIcon:
            """
            Genera un objeto QIcon de QtAwesome para un único icono.

            Este método encapsula la llamada a qtawesome.icon(), permitiendo configurar el
            glifo, los colores y el glifo de reemplazo para los diferentes modos del QIcon.

            :param name: Nombre del icono a generar (ej: 'house', 'spinner').
            :type name: str

            :param src: Prefijo de la fuente icónica (ej: 'fa6s', 'mdi'). Si es None, usa el valor de la instancia ('mdi' por defecto).
            :type src: str, opcional

            :param color: Color del icono en modo Normal. Sobrescribe el color de la instancia.
            :type color: str, opcional

            :param color_active: Color del icono en modo Activo. Si es None, usa 'color' o el valor de la instancia.
            :type color_active: str, opcional

            :param color_disabled: Color del icono en modo Deshabilitado. Si es None, usa 'gray' o el valor de la instancia.
            :type color_disabled: str, opcional

            :param color_selected: Color del icono en modo Seleccionado. Si es None, usa 'color' o el valor de la instancia.
            :type color_selected: str, opcional

            :param active: Nombre del glifo a usar en modo Activo (ej: si 'name' es 'lightbulb', 'active' podría ser 'lightbulb-on').
            :type active: str, opcional

            :param disabled: Nombre del glifo a usar en modo Deshabilitado.
            :type disabled: str, opcional

            :param selected: Nombre del glifo a usar en modo Seleccionado.
            :type selected: str, opcional

            :param opacity: Opacidad del glifo (entre 0.0 y 1.0).
            :type opacity: float, opcional

            :param scale: Factor de escala multiplicativo para el glifo (ej: 1.5 para 150% del tamaño).
            :type scale: float, opcional

            :param offset: Desplazamiento horizontal y vertical del glifo, 
                           especificado como una proporción del tamaño del icono (ej: (0.1, -0.2)).
            :type offset: Tuple[float, float], opcional

            :param hflip: Si es True, voltea el glifo horizontalmente.
            :type hflip: bool, opcional

            :param vflip: Si es True, voltea el glifo verticalmente.
            :type vflip: bool, opcional

            :returns: Un objeto QIcon configurado y listo para ser usado en un widget de Qt.
            :rtype: PySide6.QtGui.QIcon
            """

            src = src or self.src
            icon_name = f"{src}.{name}"
            options["color"] = options.pop("color", self.color)

            self.options.update(options)

            return qta.icon(icon_name, **self.options)

    def stack(self) -> QIcon: ...

    @classmethod
    def Spin(self, interval: int = 10, step: int = 1, autostart: bool = True) -> QtaSpin:
        return QtaSpin({"interval": interval, "step": step, "autostart": autostart})


icon: Qta.Icon = Qta.Icon()
