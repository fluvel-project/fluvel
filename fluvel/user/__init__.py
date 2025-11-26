from pathlib import Path
from fluvel.user.UserSettings import Settings

# This folder
USER_FOLDER = Path(__file__).parent

__all__ = [
    "Settings",
    "USER_FOLDER"
]