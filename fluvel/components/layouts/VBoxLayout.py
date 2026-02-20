# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

# PySide6
from PySide6.QtWidgets import QVBoxLayout

# Fluvel
from fluvel.components.widgets.containers.FContainer import FContainer
from fluvel.core.abstract.FLayout import FLayout
from fluvel.core.abstract.LayoutBuilder import LayoutBuilder


class VBoxLayout(QVBoxLayout, FLayout, LayoutBuilder):
    def __init__(self, parent: FContainer | None = None):
        super().__init__(parent)

    def Separator(self, **kwargs):
        if "orientation" not in kwargs:
            kwargs["orientation"] = "horizontal"
        if "style" not in kwargs:
            kwargs["style"] = "bg[#797979]"
        return super().Separator(**kwargs)
