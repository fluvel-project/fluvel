# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from pathlib import Path

from fluvel.user.UserSettings import Settings

# This folder
USER_FOLDER = Path(__file__).parent

__all__ = ["Settings", "USER_FOLDER"]
