# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

class ContentNotFoundError(Exception):
    """
    Exception that is thrown when attempting to access content
    of the GlobalContent class with an incorrect or non-existent id.
    """

    pass


class ContentLoadingError(Exception):
    """
    Exception thrown when attempting to load .json files via ContentHandler
    """

    pass


class InvalidLayoutOperationError(Exception):
    """
    This is thrown when you try to call .add() on an FContainer instead of a FLayout.
    """
    pass

class RouteNotFoundError(Exception):
    """
    Exception thrown when attempting to display a route that is not registered by the Router
    """
    pass