# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtCore import Qt

WidgetAttributeTypes = Literal[
    # --- Behavior and Events ---
    "mouse-tracking",
    "input-method-enabled",
    "transparent-for-mouse-events",
    "delete-on-close",
    "hover",
    "accept-drops",
    "input-method-transparent",
    "accept-touch-events",
    "tablet-tracking",
    # --- Appearance and Painting ---
    "opaque-paint-event",
    "no-system-background",
    "styled-background",
    "translucent-background",
    # --- Window and OS (Essential Settings) ---
    "show-without-activation",
    "always-show-tool-tips",
    "quit-on-close",
    "no-child-events-for-parent",
    "x11-net-wm-window-type-dialog",
    "x11-net-wm-window-type-tool-bar",
    "x11-net-wm-window-type-utility",
    "x11-net-wm-window-type-notification",
]


@final
class WidgetAttribute:
    __MAP__: dict[WidgetAttributeTypes, Qt.WidgetAttribute] = {
        # --- Behavior and Events ---
        "mouse-tracking": Qt.WidgetAttribute.WA_MouseTracking,
        "input-method-enabled": Qt.WidgetAttribute.WA_InputMethodEnabled,
        "transparent-for-mouse-events": Qt.WidgetAttribute.WA_TransparentForMouseEvents,
        "delete-on-close": Qt.WidgetAttribute.WA_DeleteOnClose,
        "hover": Qt.WidgetAttribute.WA_Hover,
        "accept-drops": Qt.WidgetAttribute.WA_AcceptDrops,
        "input-method-transparent": Qt.WidgetAttribute.WA_InputMethodTransparent,
        "accept-touch-events": Qt.WidgetAttribute.WA_AcceptTouchEvents,
        "tablet-tracking": Qt.WidgetAttribute.WA_TabletTracking,
        # --- Appearance and Painting ---
        "opaque-paint-event": Qt.WidgetAttribute.WA_OpaquePaintEvent,
        "no-system-background": Qt.WidgetAttribute.WA_NoSystemBackground,
        "styled-background": Qt.WidgetAttribute.WA_StyledBackground,
        "translucent-background": Qt.WidgetAttribute.WA_TranslucentBackground,
        # --- Window and OS (Essential Settings) ---
        "show-without-activation": Qt.WidgetAttribute.WA_ShowWithoutActivating,
        "quit-on-close": Qt.WidgetAttribute.WA_QuitOnClose,
        "always-show-tool-tips": Qt.WidgetAttribute.WA_AlwaysShowToolTips,
        # X11 (Linux) specific window types
        "x11-net-wm-window-type-dialog": Qt.WidgetAttribute.WA_X11NetWmWindowTypeDialog,
        "x11-net-wm-window-type-tool-bar": Qt.WidgetAttribute.WA_X11NetWmWindowTypeToolBar,
        "x11-net-wm-window-type-utility": Qt.WidgetAttribute.WA_X11NetWmWindowTypeUtility,
        "x11-net-wm-window-type-notification": Qt.WidgetAttribute.WA_X11NetWmWindowTypeNotification,
        # --- Internal Event Support ---
        "no-child-events-for-parent": Qt.WidgetAttribute.WA_NoChildEventsForParent,
    }

    @staticmethod
    def get(attribute: WidgetAttributeTypes) -> Qt.WidgetAttribute | None:
        return WidgetAttribute.__MAP__.get(attribute, None)
