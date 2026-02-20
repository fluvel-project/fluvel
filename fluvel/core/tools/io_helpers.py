# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import tomllib
from pathlib import Path
from typing import Any

# Expect Handler
from fluvel.core.tools.expect_handler import expect

try:
    import orjson

    HAS_ORJSON = True
except ImportError:
    import json

    HAS_ORJSON = False


@expect.IOError(default=None)
def load_file(file_path: Path) -> dict[str, Any]:
    """
    **IMPORTANT** Only supports TOML or JSON files.
    This function loads and returns the configuration provided by a JSON or TOML file.

    :param file_path: The :class:`~pathlib.Path` to the file
    :type file_path: :class:`~pathlib.Path`
    """

    extension = file_path.suffix

    if extension == ".json":
        if HAS_ORJSON:
            with open(file_path, "rb") as f:
                return orjson.loads(f.read())
        else:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)

    if extension == ".toml":
        with open(file_path, "rb") as f:
            return tomllib.load(f)

    raise ValueError(f"The configuration format '{extension}' is not supported.")


@expect.IOError(default=None)
def dump_json(file_path: Path, data: Any, indent: bool = False) -> bool:
    """
    Saves a dictionary or list to a JSON file.
    """
    if HAS_ORJSON:
        opts = orjson.OPT_INDENT_2 if indent else 0
        with open(file_path, "wb") as f:
            f.write(orjson.dumps(data, option=opts))
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2 if indent else None)

    return True


@expect.FileNotFound(stop=True, default="")
def load_fluml(file_path: Path) -> str:
    """
    Loads and returns the contents of a ``.fluml`` file.

    :param file_path: The path to the .fluml file
    :type file_path: :class:`~pathlib.Path`
    :returns: A string with fluml content.
    :rtype: str
    """

    with open(file_path, encoding="utf-8") as f:
        return f.read()


@expect.FileNotFound(stop=False, default="")
def load_style_sheet(file_path: Path) -> str:
    """
    Loads and returns the contents of a QSS stylesheet file.

    This function reads the contents of a specified stylesheet file (QSS)
    and returns it as a string. If the file is not found,
    the function does not stop execution (``stop=False``) and
    returns an empty string (``default=""``) due to the decorator
    :meth:`expect.FileNotFound`.

    :param file_path: Path to the QSS file. This can be a string or a Path object.
    :type file_path: :class:`~pathlib.Path`
    :returns: Contents of the QSS file as a string.
    :rtype: str
    """
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def load_theme(folder: Path, theme: str) -> str:
    """
    Loads and concatenates the contents of all QSS files for a theme.

    This function recursively scans a specific theme folder
    within the base directory (``folder``) for all files
    with the `.qss` extension and concatenates their contents into a single string.

    :param folder: Base directory where the theme folders are located.
    :type folder: :class:`pathlib.Path`
    :param theme: Name of the subfolder containing the theme's QSS files.
    :type theme: str
    :returns: Text string containing the combined QSS of all the theme's files.
    :rtype: str
    """

    if not folder.exists():
        return ""

    qss_files = (folder / theme).rglob("*.qss")

    return "\n".join(load_style_sheet(f) for f in qss_files)
