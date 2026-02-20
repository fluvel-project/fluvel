# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import sys
from pathlib import Path


def get_root_path() -> Path:
    """
    Returns the project root.
    - In production: The folder containing the .exe or the Onefile temporary file.
    - In development: The directory where the user has their terminal open (CWD).
    """
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)
        return Path(sys.executable).parent
    return Path.cwd()


PROJECT_ROOT = get_root_path().resolve()

# Base File Paths (Used by CLI and Core)
MAINPY_ROOT = PROJECT_ROOT / "app.py"
WINDOW_PATH = PROJECT_ROOT / "window.py"
CONFIG_JSON_PATH = PROJECT_ROOT / "config.json"
CONFIG_TOML_PATH = PROJECT_ROOT / "config.toml"
CONFIG_PATH = CONFIG_JSON_PATH if CONFIG_JSON_PATH.exists() else CONFIG_TOML_PATH

# Internal Structure (.fluvel)
FLUVEL_DIR = PROJECT_ROOT / ".fluvel"
STUBS_DIR = FLUVEL_DIR / "stubs"
SCHEMA_DIR = FLUVEL_DIR / "schema"
CONFIG_SCHEMA_PATH = SCHEMA_DIR / "config.schema.json"
XML_SCHEMA_PATH = SCHEMA_DIR / "menu.schema.xsd"

# Resource Directories (Development)
STATIC_DIR = PROJECT_ROOT / "static"
I18N_DIR = STATIC_DIR / "i18n"
THEMES_DIR = STATIC_DIR / "themes"
UI_DIR = PROJECT_ROOT / "ui"
PAGES_DIR = UI_DIR / "pages"

# Resource Directories (Production/Packaging)
PROD_STATIC_DIR = PROJECT_ROOT / "rsrc"
PROD_THEMES_DIR = PROD_STATIC_DIR / "_themes"

# This gets the 'fluvel/' folder in the system installation
FRAMEWORK_ROOT = Path(__file__).resolve().parent.parent
CLI_TEMPLATES = FRAMEWORK_ROOT / "cli" / "templates"

# System Environment
if (root := str(PROJECT_ROOT)) not in sys.path:
    sys.path.insert(0, root)