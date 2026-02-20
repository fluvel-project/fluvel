# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This module implements the `fluvel startproject` command to initialize a new Fluvel project.

The command generates the essential folder and file architecture, providing a
functional starting point that includes a main window, TOML configuration,
a welcome view, and the default QSS theme.

Proposed architecture generated:

root:
├───assets                      # (Optional) Binary resources (images, fonts, etc.)
├───static                      # Specialized directory for themes and languages -- (!)
│   ├───i18n                    # Fluml and i18n content files -- (!)
│   │   └───en                  # (Example) Language files for English
│   └───themes                  # Directories for QSS styles/themes -- (!)
│       └───bootstrap/          # Initial theme (e.g., fluvel-bootstrap.min.qss)
├───ui                          # UI source code -- (!)
│   ├───components              # (Optional) Simple, reusable widgets @Component
│   ├───prefabs                 # (Optional) Complex components decorated with @Prefab
│   ├───models                  # (Optional) Reactive state models (Pyro)
│   └───pages                   # Main application pages -- (!)
│       └───home/               # Dedicated directory for the composition of the home page
│           ├───components      # (Optional) Dedicated directory for specific home/ components
│           ├───prefabs         # (Optional) Dedicated directory for specific home/ prefabs
│           └───home.py         # Example page (Home)
│   config.toml                 # Global application configuration file -- (!)
│   app.py                      # Application entry point -- (!)
│   window.py                   # Custom AppWindow(QMainWindow) class -- (!)
"""

import os
import sys

import click

from fluvel import __version__, __repo__

# File Templates
from fluvel.cli.templates import (
    CONFIG_SCHEMA,
    CONFIG_TEMPLATE,
    FLUML_TEMPLATE,
    GITIGNORE_TEMPLATE,
    MAINPY_TEMPLATE,
    PAGE_TEMPLATE,
    THEME_TEMPLATE,
    WINDOW_TEMPLATE,
    XML_SCHEMA,
    README_TEMPLATE
)

# Tools for stylized click messages
from fluvel.cli.tools.ClickStyled import ClickStyled, click_confirm, echo

# Main Paths
from fluvel.utils.paths import (
    CONFIG_PATH,
    CONFIG_SCHEMA_PATH,
    FLUVEL_DIR,
    I18N_DIR,
    MAINPY_ROOT,
    PAGES_DIR,
    PROJECT_ROOT,
    SCHEMA_DIR,
    STATIC_DIR,
    THEMES_DIR,
    UI_DIR,
    WINDOW_PATH,
    XML_SCHEMA_PATH
)

FOLDERS = [
    # .fluvel Folder
    FLUVEL_DIR,
    SCHEMA_DIR,
    # Static Section
    STATIC_DIR,
    I18N_DIR,
    I18N_DIR / "en",
    THEMES_DIR,
    THEMES_DIR / "bootstrap",
    # UI Section
    UI_DIR,
    PAGES_DIR,
    PAGES_DIR / "home",
]

FILE_TEMPLATES = [
    # .fluvel Folder
    (CONFIG_SCHEMA_PATH, CONFIG_SCHEMA),
    (XML_SCHEMA_PATH, XML_SCHEMA),
    (FLUVEL_DIR / "README.md", README_TEMPLATE),
    # Root Dir
    (MAINPY_ROOT, MAINPY_TEMPLATE),
    (CONFIG_PATH, CONFIG_TEMPLATE),
    (WINDOW_PATH, WINDOW_TEMPLATE),
    # Static Folder
    (I18N_DIR / "en" / "messages.fluml", FLUML_TEMPLATE),
    (THEMES_DIR / "bootstrap" / "fluvel-bootstrap.min.qss", THEME_TEMPLATE),
    # UI Folder
    (PAGES_DIR / "home" / "home.py", PAGE_TEMPLATE),
]


def create_folders() -> None:
    """
    Create all necessary folders for the Fluvel architecture.

    Use `Path.mkdir` with `parents=True` to create nested directories
    and `exist_ok=True` to avoid failure if the folder already exists.
    """

    for folder in FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)


def create_files() -> None:
    """
    Generates the initial code and configuration files from templates.

    This includes the entry point (main.py), the example view (home.py),
    and the initial styles file. If the file already exists, it will be overwritten.
    """

    existing_files = [file[0].name for file in FILE_TEMPLATES if file[0].exists()]

    if existing_files:
        echo(
            f"[yellow]([WARNING] The following files already exist:) {', '.join([f'[blue]({f})' for f in existing_files])}"
        )

        overwrite: bool = click_confirm(
            "[yellow](Do you want to overwite them and restart the project?)", default=False
        )

        if not overwrite:
            echo("[red](Operation cancelled. No files were modified.)")
            sys.exit(0)

    for file in FILE_TEMPLATES:
        try:
            with open(file[0], "w", encoding="utf-8") as f:
                f.write(file[1])

        except FileNotFoundError as e:
            click.echo(e)


def get_short_path(path, levels=3):
    parts = path.parts
    if len(parts) <= levels:
        return str(path)

    short_path = os.path.join("...", *parts[-levels:])
    return short_path


def display_welcome_message() -> None:
    """
    Displays a stylized success message and the project architecture tree
    after a successful project initialization.
    """
    project_path = get_short_path(PROJECT_ROOT)
    project_name = PROJECT_ROOT.name

    TREE_STRUCTURE = f"""{project_name}:
├───.fluvel/           [+] IDE Intelligence: Stubs (.pyi) and Schemas (.xsd, .json)
├───assets/            [ ] Binary resources (images, fonts, etc.)
├───static/            [!] Themes and Languages
│   ├───i18n/          [!] Content files (Fluml/XML)
│   └───themes/        [!] QSS styles
├───ui/                [!] Source code
│   └───pages/         [!] Application views
│       └───home/      Example Home page
├───config.toml        [!] App configuration
├───app.py             [!] Entry point
└───window.py          [!] Main Window class
"""

    echo("\n[yellow!](Fluvel project initialized successfully!)")
    echo("─" * 40)
    echo(f"> [black+](Location :) [blue]({project_path})")
    echo(f"> [black+](Version  :) [cyan!]({__version__})")
    echo(f"> [black+](Docs     :) [blue]({__repo__})")

    echo("\n[yellow!](Project Architecture:)")
    echo("[black+](─────────────────────)")
    echo("[black+]([!] Required, [+] Recommended, [ ] Optional)\n")

    replacements = [
        (f"{project_name}:", "blue!"),
        ("├───", "blue"),
        ("└───", "blue"),
        ("│", "blue"),
        ("[!]", "cyan!"),
        ("[+]", "green"),
        ("[ ]", "black+"),
    ]
    styled_tree = ClickStyled.sub(TREE_STRUCTURE, replacements)
    click.echo(styled_tree)

    echo("[yellow!](Next steps:)")
    echo("[black+](───────────)")
    echo("  $ [white!](fluvel run) [black+](--debug)\n")
    
    # About .fluvel/
    echo("\n[cyan]([TIP]) [white](To enable IDE autocompletion and validation,)")
    echo("[white](please read the instructions in:) [blue](.fluvel/README.md)\n")


def setup_gitignore():
    gitignore_path = PROJECT_ROOT / ".gitignore"
    internal_marker = ".fluvel/"

    if not gitignore_path.exists():
        gitignore_path.write_text(GITIGNORE_TEMPLATE, encoding="utf-8")
    else:
        content = gitignore_path.read_text(encoding="utf-8")
        if internal_marker not in content:
            new_content = f"# Fluvel Internal\n{internal_marker}\n\n" + content
            gitignore_path.write_text(new_content)


@click.command
def startproject() -> None:
    """
    Main CLI command to initialize a new Fluvel project.

    This command is executed via `fluvel startproject`.
    """
    create_folders()
    create_files()

    # Post-creation
    setup_gitignore()
    display_welcome_message()
