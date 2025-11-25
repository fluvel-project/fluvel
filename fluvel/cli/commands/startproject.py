"""
This module implements the `fluvel startproject` command to initialize a new Fluvel project.

The command generates the essential folder and file architecture, providing a 
functional starting point that includes a main window, TOML configuration, 
a welcome view, and the default QSS theme.

Proposed architecture generated:

root:
├───assets                  # Binary resources (images, fonts, etc.)
├───static                  # Specialized directory for themes and languages
│   ├───content             # Fluml and i18n content files
│   │   └───en              # (Example) Language files for English
│   └───themes              # Directories for QSS styles/themes
│       └───bootstrap/      # Initial theme (e.g., fluvel-bootstrap.min.qss)
├───ui                      # UI source code
│   ├───components          # Simple, reusable widgets @Component
│   ├───prefabs             # Complex components decorated with @Prefab
│   └───pages               # Main application pages       
│       └───home/           # Dedicated directory for the composition of the home page
│           ├───components  # (Optional) Dedicated directory for specific home/ components
│           ├───prefabs     # (Optional) Dedicated directory for specific home/ prefabs
│           └───homepage.py # Example page (Home) 
│   config.toml             # Global application configuration file
│   app.py                  # Application entry point
│   window.py               # Custom AppWindow(QMainWindow) class
"""

from typing import List, Tuple
from pathlib import Path
import click

# Fluvel CLI/Utils Paths
from fluvel.cli.paths import PROJECT_ROOT, MAINPY_ROOT
from fluvel.cli.templates import MAINPY_TEMPLATE, WELCOME_VIEW, WINDOW_TEMPLATE, APPCONFIG_TEMPLATE, HOME_GREETING, COMPACT_BOOTSTRAP
from fluvel.cli.tools.ClickStyledMessage import echo, ClickStyledMessage

# Folders
from fluvel.utils.paths import CONTENT_DIR, THEMES_DIR, PAGES_DIR, STATIC_DIR, UI_DIR


FOLDERS: List[Path] = [
    STATIC_DIR,
    CONTENT_DIR / "en", 
    THEMES_DIR, 
    PROJECT_ROOT / "assets",
    UI_DIR,
    UI_DIR / "components",
    UI_DIR / "prefabs",
    PAGES_DIR,
    PAGES_DIR / "home",
    THEMES_DIR / "bootstrap"
]

FILE_TEMPLATES: List[Tuple[Path, str]] = [
    (MAINPY_ROOT, MAINPY_TEMPLATE),
    (PAGES_DIR / "home" / "homepage.py", WELCOME_VIEW),
    (PROJECT_ROOT / "window.py", WINDOW_TEMPLATE),
    (PROJECT_ROOT / "config.toml", APPCONFIG_TEMPLATE),
    (CONTENT_DIR / "en" / "homepage.fluml", HOME_GREETING),
    (THEMES_DIR / "bootstrap" / "fluvel-bootstrap.min.qss", COMPACT_BOOTSTRAP),
]

def create_project_structure() -> None:
    """
    Create all necessary folders for the Fluvel architecture.

    Use `Path.mkdir` with `parents=True` to create nested directories 
    and `exist_ok=True` to avoid failure if the folder already exists.
    """
    
    for folder in FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)

def create_file_templates():
    """
    Generates the initial code and configuration files from templates.

    This includes the entry point (main.py), the example view (home.py), 
    and the initial styles file. If the file already exists, it will be overwritten.
    """

    for file in FILE_TEMPLATES:
        
        try:

            with open(file[0], "w", encoding="utf-8") as f:

                f.write(file[1])

        except FileNotFoundError as e:
            click.echo(e)

def display_welcome_message() -> None:

    project_path = PROJECT_ROOT.resolve()
    TREE_STRUCTURE = """root:
├───assets                  # Binary resources (images, fonts, etc.)
├───static                  # Specialized directory for themes and languages
│   ├───content             # Fluml and i18n content files
│   │   └───en              # (Example) Language files for English
│   └───themes              # Directories for QSS styles/themes
│       └───bootstrap/      # Initial theme (e.g., fluvel-bootstrap.min.qss)
├───ui                      # UI source code
│   ├───components          # Simple, reusable widgets @Component
│   ├───prefabs             # Complex components decorated with @Prefab
│   └───pages               # Main application pages       
│       └───home/           # Dedicated directory for the composition of the home page
│           ├───components  # (Optional) Dedicated directory for specific home/ components
│           ├───prefabs     # (Optional) Dedicated directory for specific home/ prefabs
│           └───homepage.py # Example page (Home) 
│   config.toml             # Global application configuration file
│   app.py                  # Application entry point
│   window.py               # Custom AppWindow(QMainWindow) class
"""

    # Mensaje Final Estilizado

    echo("\n:bright_yellow[Welcome to Fluvel Framework (v0.1.2b1)]")
    click.echo("="*38)
    echo(f":bright_green[App succesfully created in:] :blue[{project_path}]")

    echo(
        ":bright_green[You can consult the documentation and tutorials at] "\
        ":blue[https://github.com/Robotid/Fluvel]"
    )

    
    # Project Structure (With color to highlight routes)
    echo("\n:yellow[Fluvel Architecture:]")
    click.echo(click.style("-"*20, fg='yellow'))
    
    
    # Print the structure tree with colors
    # We will use 'blue' for logical directories
    replacements = [
        ("root:", "blue", True),
        ("├───", "blue", False),
        ("└───", "blue", False),
        ("│", "blue", False)
    ]
    styled_tree = ClickStyledMessage.replace_with_style(TREE_STRUCTURE, replacements)

    click.echo(styled_tree)

@click.command
def startproject() -> None:
    """
    Main CLI command to initialize a new Fluvel project.

    This command is executed via `fluvel startproject`.

    Flow:
    1. Calls :py:func:`create_project_structure` to generate the folder hierarchy.
    2. Calls :py:func:`create_file_templates` to populate the initial files.
    """
    create_project_structure()
    create_file_templates()
    display_welcome_message()

