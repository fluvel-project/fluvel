from fluvel import route, Page

@route("/demo-widgets")
class Demo(Page):

    def build_ui(self):

        with self.Vertical(style="bg-slate-100") as hbody:
            hbody.adjust(margins=(20, 20, 20, 20), alignment="top-left")

            hbody.Label(text="Buttons", style="text-2xl", alignment="left")

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
                    column.Button(text=outlined, style=f"{button}-outlined")

            hbody.Label(text="Labels", style="text-2xl", alignment="left")

            with hbody.Horizontal() as h1:

                h1.Label(text="Info", style="info")
                h1.Label(text="Success", style="success")
                h1.Label(text="Warning", style="warning")
                h1.Label(text="Danger", style="danger")
