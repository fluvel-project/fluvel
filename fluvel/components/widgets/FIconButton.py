# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

from fluvel.components.widgets.FButton import FButton, FButtonKwargs


class FIconButtonKwargs(FButtonKwargs):
    size: int


class FIconButton(FButton):
    def __init__(self, **kwargs: Unpack[FIconButtonKwargs]):
        # Tamaño base para el botón circular
        if not kwargs.get("size"):
            kwargs["size"] = 24

        super().__init__(**kwargs)

    def configure(self, **kwargs: Unpack[FIconButtonKwargs]):
        if size := kwargs.pop("size", None):
            self.setFixedSize(size, size)

            b_radius = f" p[0px] br[{int(size / 2)}px]"
            kwargs["style"] = kwargs.get("style", "") + b_radius

        super().configure(**kwargs)
