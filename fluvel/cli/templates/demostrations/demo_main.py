# fluvel/cli/templates/demostrations/demo.py

from fluvel import App

def demo_app(theme: str | None):

    # App
    app = App(window_module_path="fluvel.cli.templates.demostrations.DemoWindow")
    app.register(
        initial="/demo-widgets",
        pages=["fluvel.cli.templates.demostrations.DemoPage"]
    )

    if theme:
        app.change_theme(theme)

    app.run()