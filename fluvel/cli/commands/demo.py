import click
from fluvel.cli.templates.demostrations.demo_main import demo_app
from fluvel.cli.tools.ClickStyledMessage import echo


@click.command("demo")
@click.option("--theme", help="The name of the theme to use for the demo. If not provided, the application's default theme is used.")
def demo(theme: str | None) -> None:
    """
    Runs a complete application demo.

    This command initializes and runs a demonstration version of the application.
    It allows developers to quickly test the application's UI, functionality,
    or a specific visual theme before a full build.

    :param theme: The name of the theme to apply during the demo.
    :type theme: str or None
    :raises Exception: If the demo application fails to initialize or run.
    """

    try:

        echo(":green[demo in progress...]")

        demo_app(theme)

    except Exception as e:
        click.echo(f":red[The demo could not be run.] Error: {e}")
