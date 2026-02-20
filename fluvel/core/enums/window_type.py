# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtCore import Qt

WindowTypes = Literal[
    "widget",
    "normal",
    "dialog",
    "sheet",
    "drawer",
    "popup",
    "tool",
    "tooltip",
    "splash",
    "desktop",
    "sub",
    "foreign",
    "cover",
    "always-on-top",
    "always-on-bottom",
    "context-help",
    "bypass",
    "transparent-input",
    "no-focus",
    "overrides-gestures",
    "bypass-proxy",
    "frameless",
    "title-bar",
    "sys-menu",
    "maximize-button",
    "minimize-button",
    "min-max-buttons",
    "close-button",
    "shade-button",
    "fullscreen-button",
    "no-title-bar-bg",
    "customize",
    "no-shadow",
    "fixed-size",
    "own-dc",
    "expanded-client",
    "max-fullscreen-geometry",
]


@final
class WindowType:
    # --- Standard Window Types ---
    WIDGET = Qt.WindowType.Widget
    NORMAL = Qt.WindowType.Window
    DIALOG = Qt.WindowType.Dialog
    SHEET = Qt.WindowType.Sheet
    DRAWER = Qt.WindowType.Drawer
    POPUP = Qt.WindowType.Popup
    TOOL = Qt.WindowType.Tool
    TOOLTIP = Qt.WindowType.ToolTip
    SPLASH = Qt.WindowType.SplashScreen
    DESKTOP = Qt.WindowType.Desktop
    SUB = Qt.WindowType.SubWindow
    FOREIGN = Qt.WindowType.ForeignWindow
    COVER = Qt.WindowType.CoverWindow

    # --- Behavior and Positioning Flags ---
    ALWAYS_ON_TOP = Qt.WindowType.WindowStaysOnTopHint
    ALWAYS_ON_BOTTOM = Qt.WindowType.WindowStaysOnBottomHint
    CONTEXT_HELP = Qt.WindowType.WindowContextHelpButtonHint
    BYPASS = Qt.WindowType.BypassWindowManagerHint

    # --- Interaction and Focus Flags ---
    TRANSPARENT_INPUT = Qt.WindowType.WindowTransparentForInput
    NO_FOCUS = Qt.WindowType.WindowDoesNotAcceptFocus
    OVERRIDES_GESTURES = Qt.WindowType.WindowOverridesSystemGestures
    BYPASS_PROXY = Qt.WindowType.BypassGraphicsProxyWidget

    # --- Decoration and Frame Flags ---
    FRAMELESS = Qt.WindowType.FramelessWindowHint
    TITLE_BAR = Qt.WindowType.WindowTitleHint
    SYS_MENU = Qt.WindowType.WindowSystemMenuHint
    MAX_BUTTON = Qt.WindowType.WindowMaximizeButtonHint
    MIN_BUTTON = Qt.WindowType.WindowMinimizeButtonHint
    MIN_MAX_BUTTONS = Qt.WindowType.WindowMinMaxButtonsHint
    CLOSE_BUTTON = Qt.WindowType.WindowCloseButtonHint
    SHADE_BUTTON = Qt.WindowType.WindowShadeButtonHint
    FULLSCREEN_BUTTON = Qt.WindowType.WindowFullscreenButtonHint
    NO_TITLE_BAR_BG = Qt.WindowType.NoTitleBarBackgroundHint
    CUSTOMIZE = Qt.WindowType.CustomizeWindowHint
    NO_SHADOW = Qt.WindowType.NoDropShadowWindowHint

    # --- OS Specific Flags ---
    FIXED_SIZE = Qt.WindowType.MSWindowsFixedSizeDialogHint
    OWN_DC = Qt.WindowType.MSWindowsOwnDC
    EXPANDED_CLIENT = Qt.WindowType.ExpandedClientAreaHint
    MAX_FULLSCREEN_GEOMETRY = Qt.WindowType.MaximizeUsingFullscreenGeometryHint

    _BASE_QT_VALUES: set[Qt.WindowType] = {
        WIDGET,
        NORMAL,
        DIALOG,
        SHEET,
        DRAWER,
        POPUP,
        TOOL,
        TOOLTIP,
        SPLASH,
        DESKTOP,
        SUB,
        FOREIGN,
        COVER,
    }

    __MAP__: dict[WindowTypes, Qt.WindowType] = {
        "widget": WIDGET,
        "normal": NORMAL,
        "dialog": DIALOG,
        "sheet": SHEET,
        "drawer": DRAWER,
        "popup": POPUP,
        "tool": TOOL,
        "tooltip": TOOLTIP,
        "splash": SPLASH,
        "desktop": DESKTOP,
        "sub": SUB,
        "foreign": FOREIGN,
        "cover": COVER,
        "always-on-top": ALWAYS_ON_TOP,
        "always-on-bottom": ALWAYS_ON_BOTTOM,
        "context-help": CONTEXT_HELP,
        "bypass": BYPASS,
        "transparent-input": TRANSPARENT_INPUT,
        "no-focus": NO_FOCUS,
        "overrides-gestures": OVERRIDES_GESTURES,
        "bypass-proxy": BYPASS_PROXY,
        "frameless": FRAMELESS,
        "title-bar": TITLE_BAR,
        "sys-menu": SYS_MENU,
        "maximize-button": MAX_BUTTON,
        "minimize-button": MIN_BUTTON,
        "min-max-buttons": MIN_MAX_BUTTONS,
        "close-button": CLOSE_BUTTON,
        "shade-button": SHADE_BUTTON,
        "fullscreen-button": FULLSCREEN_BUTTON,
        "no-title-bar-bg": NO_TITLE_BAR_BG,
        "customize": CUSTOMIZE,
        "no-shadow": NO_SHADOW,
        "fixed-size": FIXED_SIZE,
        "own-dc": OWN_DC,
        "expanded-client": EXPANDED_CLIENT,
        "max-fullscreen-geometry": MAX_FULLSCREEN_GEOMETRY,
    }

    @staticmethod
    def get(types: WindowTypes | list[WindowTypes]) -> Qt.WindowType:
        if isinstance(types, str):
            return WindowType.__MAP__.get(types, WindowType.NORMAL)

        map_get = WindowType.__MAP__.get
        base_set = WindowType._BASE_QT_VALUES
        normal_type = WindowType.NORMAL

        final_flags = normal_type

        for item in types:
            qt_flag = map_get(item)
            if qt_flag is not None:
                # Si es un tipo base (Widget, Window, Dialog, etc), reemplaza el base anterior
                if qt_flag in base_set:
                    final_flags = qt_flag | (final_flags & ~Qt.WindowType.WindowType_Mask)
                else:
                    final_flags |= qt_flag

        return final_flags
