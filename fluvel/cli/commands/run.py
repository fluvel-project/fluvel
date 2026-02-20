# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import importlib
import sys
import traceback
from typing import TYPE_CHECKING

import click

from fluvel.cli.reloader.HReloader import HReloader
from fluvel.cli.tools.ClickStyled import echo
from fluvel.core.tools.expect_handler import expect
from fluvel.user.UserSettings import Settings

# Fluvel
from fluvel.utils.paths import MAINPY_ROOT

if TYPE_CHECKING:
    from fluvel.core.App import App


@expect.MismatchedKey(
    msg="The <fl.App> instance $e was not found. Make sure to name it 'app' in the 'app.py' module.",
    stop=True,
)
def initialize_app(debug: bool) -> tuple["App", HReloader] | tuple["App", None]:
    # Dynamically import the user's main application module ('app.py')
    main_module = importlib.import_module("app")

    # Get the App instance, expected to be named 'app'
    # MismatchedKey decorator handles the case if 'app' is missing
    app_root: App = main_module.__dict__["app"]

    if debug:
        # Initialize the Hot Reloader
        reloader = HReloader(app_root.main_window, app_root)

        return app_root, reloader

    return app_root, None


@click.command()
@click.option("--debug", "-d", is_flag=True, help="Enable hot-reloading for development mode.")
def run(debug: bool) -> None:
    """
    Starts the Fluvel application by running 'app.py'.

    This is the primary command for development. It executes the user's
    main application script. Use the --debug flag to enable Hot Reloading.
    """

    # Check if the main application file exists
    if not MAINPY_ROOT.exists():
        echo(
            "[red]([ERROR] Initialization failed:) [blue!](app.py) [red](missing or execution path is incorrect.)"
        )
        sys.exit(1)

    # Execute the application logic
    try:
        app, _reloader = initialize_app(debug)

        app_name = Settings.get("app.name", "App")
        app_version = Settings.get("app.version", "")
        in_production = Settings.get("fluvel.production", False)

        echo(f"\n🚀 [white](Running) [green]({app_name}) [cyan]({app_version})")
        echo("[black+](──────────────────────────────────────)")

        # Context info
        mode_label = "[red!](PRODUCTION)" if in_production else "[green!](DEVELOPMENT)"
        asset_label = (
            "[blue](rsrc/) [black+]( (Optimized))"
            if in_production
            else "[blue](static/) [black+]( (Source))"
        )

        echo(f"> [black+](Mode   :) {mode_label}")
        echo(f"> [black+](Assets :) {asset_label}")
        echo(
            f"> [black+](PID    :) [red]({app.applicationPid()}) [black+](| Script:) [cyan]({MAINPY_ROOT.name})"
        )

        if debug:
            echo("[white](────────────────────────────────)")
            echo("[blue]([HMR] Enabled. Monitoring:) [cyan](ui/) [blue](and) [cyan](static/)")

        app.run()

    except Exception as e:
        echo("\n[red]([CRITICAL] An unexpected error occurred during application runtime.)")
        echo(f"  > Error Type: [blue]({type(e).__name__})")
        echo(f"  > Message: [blue]({e})")

        # Traceback
        echo("\n[yellow](--- FULL TRACEBACK ---)")

        # Use traceback.format_exc() to get the entire call stack
        echo(f"\n{traceback.format_exc()}")

        sys.exit(1)
