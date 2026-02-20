# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("fluvel")
except PackageNotFoundError:
    __version__ = "development"

__author__ = "J. F. Escobar"
__email__ = "robotid7@outlook.es"
__licence__ = "LGPL-3.0-or-later"
__repo__ = "https://github.com/fluvel-project/fluvel"

from fluvel.composer import Canvas, Component, Prefab
from fluvel.core import App, AppWindow, Router, route
from fluvel.core.abstract.AbstractPage import Page
from fluvel.i18n.ResourceManager import er
from fluvel.reactive import Model, ModelStore, StateManager, computed, reaction, effect
from fluvel.user.UserSettings import Settings

__all__ = [
    "App",
    "AppWindow",
    "Router",
    "Page",
    "route",
    "Settings",
    "Model",
    "ModelStore",
    "StateManager",
    "computed",
    "reaction",
    "effect",
    "er",
    "Component",
    "Prefab",
    "Canvas"
]
