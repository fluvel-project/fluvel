# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

# PySide6
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

# Fluvel
from fluvel.components.widgets.FButton import FButton, FButtonKwargs


class FLinkButtonKwargs(FButtonKwargs, total=False):
    url: str

class FLinkButton(FButton):
    def __init__(self, **kwargs: Unpack[FLinkButtonKwargs]):
        super().__init__(**kwargs)

    def configure(self, **kwargs: Unpack[FLinkButtonKwargs]):
        
        if url := kwargs.pop("url", None):
            self._connect_url(url)

        return super().configure(**kwargs)
    
    def _connect_url(self, url: str) -> None:
        self.url = url
        self.clicked.connect(self.open_link)

    def open_link(self):
        QDesktopServices.openUrl(QUrl(self.url))
