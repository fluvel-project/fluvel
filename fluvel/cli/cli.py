import click
from .commands.run import run
from .commands.demo import demo
from .commands.clean import clean
from .commands.startproject import startproject
from .commands.build import build


@click.group()
def main() -> None:
    """
    Fluvel Command Line Interface (CLI).

    This command group is the entry point for all Fluvel development and
    build operations.

    Available commands:

    - ``run``: Runs the application in development mode.

    - ``demo``: Runs a demonstration version of the application with an optional theme.

    - ``clean``: Clears cache and generated production files.

    - ``startproject``: Initializes a new Fluvel project structure.
    
    - ``build``: Prepares and optimizes the application for production use.
    """
    pass


# Agregar comandos
main.add_command(run)
main.add_command(demo)
main.add_command(clean)
main.add_command(startproject)
main.add_command(build)


if __name__ == "__main__":
    main()
