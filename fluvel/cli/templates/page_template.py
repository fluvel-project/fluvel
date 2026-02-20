# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

PAGE_TEMPLATE = """import fluvel as fl

@fl.route("/home")
class HomePage(fl.Page):

    def build(self):
    
        with self.Vertical(style="bg-slate-100") as v:
            v.adjust(alignment="center", spacing=0)

            v.Label(text=fl.er("msg.welcome"), style="fs[32px]")
            v.Label(text=fl.Settings["app.copyright"], style="fs[12px]", alignment="center")
"""
