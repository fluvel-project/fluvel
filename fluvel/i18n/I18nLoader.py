# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from pathlib import Path
from typing import Any

# Exceptions Handler
from fluvel.core.exceptions.exceptions import ContentLoadingError
from fluvel.core.tools import load_file, load_fluml
from fluvel.engines import XMLMenuParser, convert_FLUML_to_HTML

# Fluvel Utils
from fluvel.i18n.data_structures import I18nRawContent

# Fluvel Paths
from fluvel.utils.paths import I18N_DIR, PROD_STATIC_DIR


class I18nLoader:
    current_language: str = None

    @classmethod
    def load(cls, lang: str, in_production: bool) -> I18nRawContent | None:
        # Si el lenguaje es el mismo de la aplicación actualmente
        # no es necesario procesar y parsear los archivos de idioma nuevamente.
        if lang == cls.current_language:
            return

        # En caso contrario, el nuevo lenguaje se convierte en el
        # lenguaje actual y comienza el proceso de carga y
        # parseo de los archivos de idioma.
        cls.current_language = lang

        # Se define la ruta a la carpeta del idioma objetivo y las
        # extensiones de los mismos.
        folder_path: Path = (PROD_STATIC_DIR if in_production else I18N_DIR) / lang

        if not folder_path.exists():
            return

        file_extensions: tuple[str, str] = ("json", "json") if in_production else ("fluml", "xml")

        # Getting the list of files
        menu_files, text_files = cls.get_files(folder_path, file_extensions)

        # Obtaining the functions responsible for loading
        # the files and delivering the content dictionary
        process_menus, process_texts = cls.get_file_processors(in_production)

        menus_dict = process_menus(menu_files)
        text_dict = process_texts(text_files)

        return I18nRawContent(menus_dict, text_dict)

    @classmethod
    def get_file_processors(cls, in_production: bool) -> tuple[Callable, Callable]:
        if in_production:
            return cls._load_from_json, cls._load_from_json

        return cls._process_menus, cls._process_texts

    @staticmethod
    def _process_menus(files: list[Path]) -> dict[str, Any]:
        return {f.stem: XMLMenuParser.parse(f) for f in files}

    @staticmethod
    def _process_texts(files: list[Path]) -> dict[str, Any]:
        return convert_FLUML_to_HTML("\n".join(load_fluml(f) for f in files))

    @staticmethod
    def _load_from_json(files: list[Path]) -> dict[str, Any]:
        return load_file(files[0])

    @staticmethod
    def get_files(
        content_folder: Path, extensions: tuple[str, str]
    ) -> tuple[list[Path], list[Path]]:
        if not content_folder.exists():
            raise ContentLoadingError(f"non-existent folder: {content_folder}")

        # Unpacking the extensions for each file type
        ext_texts, ext_menus = extensions

        # Defining menu folder path
        menus_path = content_folder / "menus"

        # Creating the menu file list (.xml or .json)
        menu_files = list(menus_path.rglob(f"*.{ext_menus}")) if menus_path.exists() else []
        menu_files_set = set(menu_files)

        # Filtering the language text files (.fluml or .json)
        text_files = [f for f in content_folder.rglob(f"*.{ext_texts}") if f not in menu_files_set]

        return menu_files, text_files
