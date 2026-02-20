# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from .config_schema import CONFIG_SCHEMA
from .config_template import CONFIG_TEMPLATE
from .fluml_template import FLUML_TEMPLATE
from .gitignore_template import GITIGNORE_TEMPLATE
from .mainpy_template import MAINPY_TEMPLATE
from .page_template import PAGE_TEMPLATE
from .readme_template import README_TEMPLATE
from .theme_template import THEME_TEMPLATE
from .window_template import WINDOW_TEMPLATE
from .xml_schema import XML_SCHEMA

__all__ = [
    "MAINPY_TEMPLATE",
    "PAGE_TEMPLATE",
    "WINDOW_TEMPLATE",
    "FLUML_TEMPLATE",
    "CONFIG_TEMPLATE",
    "XML_SCHEMA",
    "THEME_TEMPLATE",
    "README_TEMPLATE",
    "GITIGNORE_TEMPLATE",
    "CONFIG_SCHEMA",
]
