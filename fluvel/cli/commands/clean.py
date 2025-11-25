import click
from fluvel.core.tools.generate_menu_options import (
    _DEFAULT_MENU_OPTIONS,
    USER_FOLDER,
)
from fluvel.cli.tools.ClickStyledMessage import echo


def reset_menu_options() -> None:
    """
    Resets the user's MenuOptions.py file.

    It overwrites the content of 'MenuOptions.py' located in the
    user folder with the default menu configuration defined in
    ``_DEFAULT_MENU_OPTIONS``.
    """

    file_path = USER_FOLDER / "MenuOptions.py"

    try:
        with open(file_path, "w") as f:
            f.write(_DEFAULT_MENU_OPTIONS)

        # Custom styled success message
        echo(":green[Clean: 'fluvel._user.MenuOptions' succesfully reset to default settings.]")

    except Exception as e:
        # Custom styled error message
        echo(f":red[Error: An error ocurred while resetting 'fluvel._user.MenuOptions']. Error: {e}")

@click.command(name="clean", hidden=True)
def clean() -> None:
    """
    Resets the internal configuration of files and directories.

    This command is primarily used internally or before a publication to
    ensure that user-configurable files (like MenuOptions) are set back
    to their default state.
    """
    # Reset menu options
    reset_menu_options()