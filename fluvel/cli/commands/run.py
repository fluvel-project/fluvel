import click, sys, importlib, traceback
from typing import Tuple, TYPE_CHECKING

# Fluvel
from fluvel.cli.paths import MAINPY_ROOT
from fluvel.cli.reloader.HReloader import HReloader
from fluvel.core.exceptions.expect_handler import expect
from fluvel.cli.tools.ClickStyledMessage import echo
from fluvel._user.GlobalConfig import AppConfig

if TYPE_CHECKING:
    from fluvel.core.App import App

@expect.ErrorImportingModule(stop=True)
@expect.MismatchedKey(
    msg="Reloader Error: The <FluvelApp> instance $e was not found. Make sure to name it 'app' in the 'app.py' module to use Hot-Reloader.",
    stop=True
)

def initialize_app(debug: bool) -> Tuple[HReloader, "App"] | Tuple["App", None]:

    # Dynamically import the user's main application module ('app.py')
    main_module = importlib.import_module("app")

    # Get the FluvelApp instance, expected to be named 'app'
    # MismatchedKey decorator handles the case if 'app' is missing
    app_root: "App" = main_module.__dict__["app"]

    if debug:
        # Initialize the Hot Reloader
        reloader = HReloader(app_root.main_window, app_root._app, app_root)

        return app_root, reloader

    return app_root, None


@click.command()
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    help="Enable hot-reloading for development mode."
)
def run(debug: bool) -> None:
    """
    Starts the Fluvel application by running 'app.py'.

    This is the primary command for development. It executes the user's
    main application script. Use the --debug flag to enable Hot Reloading.
    """

    # Check if the main application file exists
    if not MAINPY_ROOT.exists():

        echo(
            ":red[Error: 'app.py' not found.] :yellow[Make sure the main script exist in the project root.]"
        )

        sys.exit(1)

    # If initialized in debug/hot-reloading mode
    if debug:
        echo(":green[Hot Reloading Enabled]")
    else:
        echo(":blue[Initializing application in standard mode...]")

    # Execute the application logic
    try:
        app_and_reloader = initialize_app(debug)

        app = app_and_reloader[0]
        
        echo(f"  > Application Name: :green[{app._app.applicationName()} - {app._app.applicationVersion()}]")
        echo(f"  > Application PID: :red[{app._app.applicationPid()}] (Unique Process)")
        echo(f"  > Main script path: :cyan[{MAINPY_ROOT}]")

        if AppConfig.fluvel.DEV_MODE:
            echo(f"  > Development Mode: :blue[{AppConfig.fluvel.DEV_MODE}]")
        else:
            echo(f"  > Development Mode: :blue[{AppConfig.fluvel.DEV_MODE}] (working with :blue[build_resources/])")

        app.run()

    except Exception as e:
        echo(f"\n:red[CRITICAL ERROR]: An unexpected error occurred during application runtime.")
        echo(f"  > Error Type: :blue[{type(e).__name__}]")
        echo(f"  > Message: :blue[{e}]")
        
        # Traceback
        echo("\n:yellow[--- FULL TRACEBACK ---]")
        # Use traceback.format_exc() to get the entire call stack
        echo(f"\n{traceback.format_exc()}")
        sys.exit(1)