# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from pathlib import Path
from typing import Any, Literal

# Fluvel utils
from fluvel.core.tools import load_file


class DataSection:
    """
    A simple container object used to represent a nested section in the configuration file.

    This class is used internally by :class:`~fluvel.config.app_config.Settings`
    to transform nested dictionaries from a configuration file (e.g., TOML or JSON)
    into objects that allow access to their values via attributes (dot notation),
    such as :code:`Settings.app.name`.
    """

    pass


class Settings:
    """
    A central utility class that loads, processes, and exposes the global
    application configuration from a file (e.g., ``config.toml``).

    The configuration is loaded recursively. Nested sections are represented
    as :class:`~fluvel.user.UserSettings.DataSection` objects, allowing for
    structured and easy-to-read access via class attributes.

    All configuration values are accessible as class attributes, for example:

    .. code-block:: python

        from fluvel import Settings

        # Accessing values directly
        app_name = Settings.app.copyright

        # or this (return None if app.copyright does not exist)
        app_name = Settings["app.copyright"]

        # or if you want a custom default value
        app_name = Settings.get("app.copyright", None)
    """

    dict_tree: dict[str, Any] = {}
    __is_initialized = False

    @classmethod
    def init_config(cls, file_path: Path) -> None:
        """
        Initializes the application configuration from a file.

        This class method is the entry point for loading the configuration file,
        resolving its absolute path, and then invoking the recursive
        structuring process :func:`~fluvel.config.app_config.structure_config`.

        .. note::
            This method is called only once at the beginning of the
            application lifecycle, so it includes protection to ensure it.

        :param filename: The name of the configuration file (e.g. ``'config.toml'``).
        :type filename: :class:`str`
        :rtype: :obj:`None`
        """

        # Check if configuration has already been loaded.
        if cls.__is_initialized or not file_path.exists():
            # Return silently if already initialized to maintain single-load mandate.
            return

        # Loading the file
        config: dict[str, Any] = load_file(file_path)

        # Start auto-configuration process
        cls.dict_tree = {}
        cls.structure_config(cls, config, cls.dict_tree)

        # Mark the class as initialized successfully
        cls.__is_initialized = True

    @classmethod
    def structure_config(cls, obj, config: dict, tree_node: dict) -> None:
        """
        Processes a configuration dictionary and structures it into object attributes.

        This is a recursive helper function that iterates over the configuration
        dictionary and dynamically creates attributes on the provided object.
        It is the core of Fluvel's configuration mechanism.

        - Key-value pairs (that are not dictionaries) are set directly as attributes
        of the current object.
        - Nested sections (dictionaries) are converted into new
        :class:`~fluvel.config.app_config.DataSection` instances, and the function
        is called recursively to process that sub-section.

        :param obj: The current object where attributes will be set. This can be
                    the :class:`~fluvel.config.app_config.Settings` class or a
                    nested :class:`~fluvel.config.app_config.DataSection` object.
        :type obj: :obj:`~fluvel.config.app_config.Settings` or :obj:`~fluvel.config.app_config.DataSection`
        
        :param config: The configuration dictionary to be processed 
                       (the content of the TOML/JSON file).
        :type config: :class:`dict`
        :rtype: :obj:`None`
        """
        for varname, value in config.items():
            if not isinstance(value, dict):
                # Seteamos en el objeto y en el árbol
                setattr(obj, varname, value)
                tree_node[varname] = value
            else:
                # Crear la sección
                data_sec = DataSection()
                setattr(obj, varname, data_sec)

                # Crear la rama en el árbol
                tree_node[varname] = {}

                # Recursión bajando un nivel en ambos
                cls.structure_config(data_sec, value, tree_node[varname])

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value using dot notation for nested access.

        This method traverses the nested :class:`~fluvel.config.app_config.DataSection`
        objects based on the dots in the key string.

        :param key: The key path to the value (e.g., ``'app.domain'`` or ``'window.title'``).
        :type key: :class:`str`
        :param default: The value to return if the key path is not found. Defaults to :obj:`None`.
        :type default: :class:`typing.Any`
        :returns: The configuration value found at the specified path, or the ``default`` value.
        :rtype: :class:`typing.Any`
        """

        parts = key.split(".")
        current_obj = cls

        for part in parts:
            if hasattr(current_obj, part):
                current_obj = getattr(current_obj, part)
            else:
                return default

        return current_obj

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Sets a configuration value using dot notation, dynamically creating
        the necessary hierarchy.

        This method traverses the path defined by the dots. If a section in
        the path does not exist, it automatically instantiates a
        :class:`~fluvel.user.UserSettings.DataSection` to bridge the gap.
        This allows for "safe" assignments even if the configuration
        topology hasn't been pre-defined in the source file.

        .. code-block:: python

            # Even if 'plugins' doesn't exist in config.toml:
            Settings.set("plugins.editor.theme", "dark")
            print(Settings.plugins.editor.theme) # Output: dark

        :param key: The dot-separated path to the attribute (e.g., 'app.version.patch').
        :type key: str
        :param value: The value to assign to the final attribute.
        :type value: Any
        :rtype: None
        """

        parts = key.split(".")
        obj = cls

        for part in parts[:-1]:
            if not hasattr(obj, part):
                setattr(obj, part, DataSection())
            obj = getattr(obj, part)

        setattr(obj, parts[-1], value)

    def __class_getitem__(cls, key: Literal["Hola"]) -> Any:
        """
        Enables dictionary-style access to configuration values using bracket notation.

        This method allows developers to retrieve configuration values using
        the same dot notation path as the :meth:`~fluvel.config.app_config.Settings.get`
        method, but using the class slicing syntax (e.g., :code:`Settings["key"]`).

        .. note::
            If the key is not found, this method returns :obj:`None` by default.

        :param key: The key path to the value (e.g., ``'window.size'``).
        :type key: :class:`str`
        :returns: The configuration value found at the specified path, or :obj:`None` if not found.
        :rtype: :class:`typing.Any`
        """
        return cls.get(key)

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        return cls.dict_tree
