# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import logging
import sys
from collections.abc import Callable
from typing import Any, TypedDict, Unpack

# Exceptions
from fluvel.core.exceptions.exceptions import ContentLoadingError, ContentNotFoundError


class ExpectKwargs(TypedDict, total=False):
    """
    Specifies optional key arguments for exception handling decorators.

    :param msg: Custom error message to display. You can use ``$e`` as a placeholder for the original exception message.
    :type msg: str
    :param default: Value to return if the exception is caught and the flow does not stop.
    :type default: any
    :param stop: If ``True``, stops the application execution (via ``sys.exit(1)``) after catching the exception. Default is ``True``.
    :type stop: bool
    """

    msg: str
    default: Any
    stop: bool


class expect:
    """
    Static utility class that groups decorators for handling common exceptions
    within the Fluvel framework.

    Provides a declarative way (``@expect.Exception(...)``) to wrap
    functions, centralising the logging and output logic (``sys.exit``).
    """

    @classmethod
    def Handle(
        cls,
        function: Callable,
        exception: type[Exception],
        args: tuple,
        kwargs: dict[str, Any],
        msg: str = None,
        default: Any = None,
        stop: bool = True,
    ):
        """
        Central function that executes the ``try...except`` logic, handles logging,
        and controls the flow of the application (stopping or returning a value).

        :param function: The original function to execute.
        :type function: callable
        :param exception: The type of exception to catch (e.g., ``ImportError``).
        :type exception: Exception
        :param args: Positional arguments passed to the original function.
        :type args: tuple
        :param kwargs: Key arguments passed to the original function.
        :type kwargs: dict[str, any]
        :param msg: Custom error message for logging.
        :type msg: str
        :param default: Value to return in case of exception, if stop is False.
        :type default: any
        :param stop: If ``True``, call ``sys.exit(1)`` after catching the exception.
        :type stop: bool
        :returns: The result of the original function, or ``default`` if an exception occurs and the flow does not stop.
        :rtype: any
        """
        try:
            return function(*args, **kwargs)
        except exception as e:
            msg = msg.replace("$e", str(e)) if msg else f"{type(e).__name__}: {e}"

            logging.error(msg)

            if stop:
                sys.exit(1)

            return default

    @classmethod
    def _make_handler(cls, exception: Exception, **eparams):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return cls.Handle(func, exception, args, kwargs, **eparams)

            return wrapper

        return decorator

    @classmethod
    def Any(cls, exception: type[Exception], **eparams: Unpack[ExpectKwargs]):
        """Decorator to handle any type of specified exception."""
        return cls._make_handler(exception, **eparams)

    @classmethod
    def FileNotFound(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`FileNotFoundError`.
        """

        return cls._make_handler(FileNotFoundError, **eparams)

    @classmethod
    def ContentNotFound(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`~fluvel.core.exceptions.exceptions.ContentNotFoundError`.
        """

        return cls._make_handler(ContentNotFoundError, **eparams)

    @classmethod
    def ErrorLoadingContent(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`~fluvel.core.exceptions.exceptions.ContentLoadingError`.
        """

        return cls._make_handler(ContentLoadingError, **eparams)

    @classmethod
    def ErrorImportingModule(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`ImportError` (incluyendo ``ModuleNotFoundError``).
        """

        return cls._make_handler(ImportError, **eparams)

    @classmethod
    def RouteNotFound(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`ValueError` (usada para rutas no encontradas).
        """

        return cls._make_handler(ValueError, **eparams)

    @classmethod
    def MismatchedKey(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`KeyError`.
        """

        return cls._make_handler(KeyError, **eparams)

    @classmethod
    def IOError(cls, **eparams: Unpack[ExpectKwargs]):
        """
        Decorator to handle the exception :exc:`IOError`.
        """

        return cls._make_handler(IOError, **eparams)
