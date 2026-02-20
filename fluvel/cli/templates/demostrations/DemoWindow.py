# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from fluvel.core import AppWindow


class MainWindow(AppWindow):
    def init_ui(self):
        self.configure(title="Demo Widgets")
