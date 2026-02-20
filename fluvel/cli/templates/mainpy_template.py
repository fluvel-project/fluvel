# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

MAINPY_TEMPLATE = """import fluvel as fl

app = fl.App()
app.register(initial="/home")

if __name__ == "__main__":
    app.run()
"""
