from typing import Dict, Literal
from PySide6.QtCore import Qt

WidgetAttributeTypes = Literal[
    # --- Comportamiento y Eventos ---
    "mouse-tracking",
    "input-method-enabled",
    "transparent-for-mouse-events",
    "delete-on-close",
    "hover",
    "accept-drops",
    "input-method-transparent",
    "accept-touch-events",
    "tablet-tracking",
    
    # --- Apariencia y Pintado (Custom Rendering) ---
    "opaque-paint-event",
    "no-system-background",
    "styled-background",
    "translucent-background",

    # --- Ventana y OS (Configuración Esencial) ---
    "show-without-activation",
    "quit-on-close",
    "no-child-events-for-parent",
    "x11-net-wm-window-type-dialog",
    "x11-net-wm-window-type-tool-bar",
    "x11-net-wm-window-type-utility",
    "x11-net-wm-window-type-notification",
    "always-show-tool-tips",
]

class WidgetAttributes:
    """
    Abstracción de Qt.WidgetAttribute que selecciona banderas aptas para la
    configuración manual mediante widget.setAttribute(flag, True/False).
    """

    _ATTRIBUTE_MAP: Dict[str, Qt.WidgetAttribute] = {

        # --- Comportamiento y Eventos ---
        "mouse-tracking": Qt.WidgetAttribute.WA_MouseTracking, 
        "input-method-enabled": Qt.WidgetAttribute.WA_InputMethodEnabled,
        "transparent-for-mouse-events": Qt.WidgetAttribute.WA_TransparentForMouseEvents,
        "delete-on-close": Qt.WidgetAttribute.WA_DeleteOnClose,
        "hover": Qt.WidgetAttribute.WA_Hover,
        "accept-drops": Qt.WidgetAttribute.WA_AcceptDrops,
        "input-method-transparent": Qt.WidgetAttribute.WA_InputMethodTransparent,
        "accept-touch-events": Qt.WidgetAttribute.WA_AcceptTouchEvents,
        "tablet-tracking": Qt.WidgetAttribute.WA_TabletTracking,
        
        # --- Apariencia y Pintado ---
        "opaque-paint-event": Qt.WidgetAttribute.WA_OpaquePaintEvent,
        "no-system-background": Qt.WidgetAttribute.WA_NoSystemBackground,
        "styled-background": Qt.WidgetAttribute.WA_StyledBackground, 
        "translucent-background": Qt.WidgetAttribute.WA_TranslucentBackground, 
        
        # --- Ventana y OS (Configuración Esencial) ---
        "show-without-activation": Qt.WidgetAttribute.WA_ShowWithoutActivating,
        "quit-on-close": Qt.WidgetAttribute.WA_QuitOnClose,
        "always-show-tool-tips": Qt.WidgetAttribute.WA_AlwaysShowToolTips,

        # Tipos de ventana específicos de X11 (Linux)
        "x11-net-wm-window-type-dialog": Qt.WidgetAttribute.WA_X11NetWmWindowTypeDialog,
        "x11-net-wm-window-type-tool-bar": Qt.WidgetAttribute.WA_X11NetWmWindowTypeToolBar,
        "x11-net-wm-window-type-utility": Qt.WidgetAttribute.WA_X11NetWmWindowTypeUtility,
        "x11-net-wm-window-type-notification": Qt.WidgetAttribute.WA_X11NetWmWindowTypeNotification,
        
        # --- Soporte Interno de Eventos ---
        "no-child-events-for-parent": Qt.WidgetAttribute.WA_NoChildEventsForParent,
    }

    @classmethod
    def get(cls, attribute: WidgetAttributeTypes) -> Qt.WidgetAttribute | None:
        """
        Método para obtener la bandera de Qt.WidgetAttribute a partir de una cadena.
        """
        return cls._ATTRIBUTE_MAP.get(attribute, None)