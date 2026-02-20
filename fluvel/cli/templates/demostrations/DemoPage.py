# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from fluvel import Page, route


@route("/demo-widgets")
class Demo(Page):
    def build(self):
        with self.Vertical(style="bg-slate-100") as hbody:
            hbody.adjust(margins=(20, 20, 20, 20), alignment="top-left")

            hbody.Label(text="Buttons", style="h1", alignment="left")

            with hbody.Grid() as grid:
                buttons = (
                    "primary",
                    "secondary",
                    "info",
                    "warning",
                    "success",
                    "danger",
                    "dark",
                    "light",
                )

                for i, button in enumerate(buttons, 1):
                    normal = button.capitalize() + " Button"
                    outlined = button.capitalize() + " Outlined"

                    column = grid.Column(i)

                    column.Button(text=normal, style=button)

                    if button == "primary":
                        column.Button(text=outlined, style="outlined")
                    else:
                        column.Button(text=outlined, style=f"{button}-outlined")

            hbody.Label(text="Labels", style="h1", alignment="left")

            with hbody.Horizontal() as h1:
                h1.Label(text="Info", style="info")
                h1.Label(text="Success", style="success")
                h1.Label(text="Warning", style="warning")
                h1.Label(text="Danger", style="danger")
