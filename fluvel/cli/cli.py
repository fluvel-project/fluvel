# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import click
from fluvel import __version__

from .commands.build import build
from .commands.demo import demo
from .commands.generate_stubs import generate_stubs
from .commands.run import run
from .commands.startproject import startproject


@click.group()
@click.version_option(
    version=__version__,
    prog_name="Fluvel CLI",
    message="%(prog)s version %(version)s"
)
def main() -> None:
    """
    Fluvel Command Line Interface (CLI).

    This command group is the entry point for all Fluvel development and
    build operations.

    Available commands:

    - ``run``: Runs the application in development mode.

    - ``demo``: Runs a demonstration version of the application with an optional theme.

    - ``startproject``: Initializes a new Fluvel project structure.

    - ``build``: Prepares and optimizes the application for production use.
    """
    pass


# Agregar comandos
main.add_command(startproject)
main.add_command(run)
main.add_command(demo)
main.add_command(build)
main.add_command(generate_stubs, "generate-stubs")


if __name__ == "__main__":
    main()
