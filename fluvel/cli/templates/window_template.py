# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

WINDOW_TEMPLATE = """from fluvel import AppWindow

class MainWindow(AppWindow):

    def __post_init__(self):
        \"\"\"
        This method is called after the core UI (CentralWidget, MenuBar) 
        is initialized. It is the perfect place for initial window setup.
        \"\"\"

        # These settings replace those made in 'config.toml'
        self.configure(
            title="FluvelApp",
            size=[720, 500]
        )
"""