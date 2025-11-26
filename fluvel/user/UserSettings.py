from typing import Any
from pathlib import Path

# Fluvel utils
from fluvel.core.tools.config_loader import load_file

class DataSection:
    """
    A simple container object used to represent a nested section in the configuration file.

    This class is used internally by :py:class:`~fluvel.config.app_config.Settings`
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
    as :py:class:`~fluvel.config.app_config.DataSection` objects, allowing for
    structured and easy-to-read access via class attributes.

    All configuration values are accessible as class attributes, for example:

    .. code-block:: python

        from fluvel.config.app_config import Settings
        
        # Accessing values directly
        app_name = Settings.app.name

        # or this (return None if app.name does not exist)
        app_name = Settings["app.name"]

        # or if you want a custom default value
        app_name = Settings.get("app.name", None)
    """

    @classmethod
    def init_config(cls, filename: str) -> None:
        """
        Initializes the application configuration from a file.

        This class method is the entry point for loading the configuration file,
        resolving its absolute path, and then invoking the recursive
        structuring process :py:func:`~fluvel.config.app_config.structure_config`.

        .. note::
            This method is called only once at the beginning of the 
            application lifecycle, so it includes protection to ensure it.

        :param filename: The name of the configuration file (e.g. ``'config.toml'``).
        :type filename: :py:class:`str`
        :rtype: :py:obj:`None`
        """

        # Check if configuration has already been loaded.
        if hasattr(cls, '__is_initialized'):
            # Return silently if already initialized to maintain single-load mandate.
            return

        # Getting the abs path to the file
        filepath = Path(filename).resolve()
        
        # Loading the file
        config: dict = load_file(filepath)

        # Start auto-configuration process
        structure_config(cls, config)

        # Mark the class as initialized successfully
        setattr(cls, '__is_initialized', True)

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value using dot notation for nested access.

        This method traverses the nested :py:class:`~fluvel.config.app_config.DataSection`
        objects based on the dots in the key string.

        :param key: The key path to the value (e.g., ``'app.domain'`` or ``'window.title'``).
        :type key: :py:class:`str`
        :param default: The value to return if the key path is not found. Defaults to :py:obj:`None`.
        :type default: :py:class:`typing.Any`
        :returns: The configuration value found at the specified path, or the ``default`` value.
        :rtype: :py:class:`typing.Any`
        """

        attrs = key.split('.')

        obj = cls

        for attr in attrs:

            if hasattr(obj, attr):
                obj = getattr(obj, attr)

            else:
                return default
            
        return obj

    @classmethod
    def __class_getitem__(cls, key: str) -> Any:
        """
        Enables dictionary-style access to configuration values using bracket notation.

        This method allows developers to retrieve configuration values using
        the same dot notation path as the :py:meth:`~fluvel.config.app_config.Settings.get`
        method, but using the class slicing syntax (e.g., :code:`Settings["key"]`).

        .. note::
            If the key is not found, this method returns :py:obj:`None` by default.

        :param key: The key path to the value (e.g., ``'window.size'``).
        :type key: :py:class:`str`
        :returns: The configuration value found at the specified path, or :py:obj:`None` if not found.
        :rtype: :py:class:`typing.Any`
        """
        return cls.get(key)

def structure_config(obj: Settings | DataSection, config: dict) -> None:
    """
    Processes a configuration dictionary and structures it into object attributes.

    This is a recursive helper function that iterates over the configuration
    dictionary and dynamically creates attributes on the provided object.
    It is the core of Fluvel's configuration mechanism.

    - Key-value pairs (that are not dictionaries) are set directly as attributes
      of the current object.
    - Nested sections (dictionaries) are converted into new
      :py:class:`~fluvel.config.app_config.DataSection` instances, and the function
      is called recursively to process that sub-section.

    :param obj: The current object where attributes will be set. This can be
                the :py:class:`~fluvel.config.app_config.Settings` class or a
                nested :py:class:`~fluvel.config.app_config.DataSection` object.
    :type obj: :py:obj:`~fluvel.config.app_config.Settings` or :py:obj:`~fluvel.config.app_config.DataSection`
    :param config: The configuration dictionary to be processed (the content of the TOML/JSON file).
    :type config: :py:class:`dict`
    :rtype: :py:obj:`None`
    """
    for varname, value in config.items():

        if not isinstance(value, dict):
            setattr(obj, varname, value)
        else:
            data_sec = DataSection()
            setattr(obj, varname, data_sec)
            structure_config(data_sec, value)