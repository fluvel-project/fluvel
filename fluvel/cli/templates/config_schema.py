# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

CONFIG_SCHEMA = """{
    "$schema": "https://json-schema.org/draft-07/schema#",
    "title": "Fluvel Config Schema",
    "type": "object",
    "properties": {
        "fluvel": {
            "type": "object",
            "description": "Controls the internal behavior of the framework.",
            "properties": {
                "production": {
                    "type": "boolean", 
                    "default": false,
                    "description": "When `true`, the app uses optimized assets from `rsrc/`. When `false`, it enables development features and uses `static/`."
                }
            }
        },
        "app": {
            "type": "object",
            "description": "Define the application's identity and metadata. These values are processed by the `configure` method of the `fl.App` class.",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Internal technical name (used for data file paths)."
                },
                "display_name": {
                    "type": "string",
                    "description": "The name visible to the user in the taskbar or menus."
                },
                "version": {
                    "type": "string",
                    "description": "Current application version."
                },
                "organization": {
                    "type": "string",
                    "description": "Name of the company or author."
                },
                "domain": {
                    "type": "string",
                    "description": "Organization domain (used to identify the app on Linux/maxOS)."
                },
                "desktop_filename": {
                    "type": "string",
                    "description": "Unique identifier for the operating system launcher."
                },
                "icon": {
                    "type": "string",
                    "description": "Relative path to the image file used as the global icon."
                },
                "licence": {
                    "type": "string",
                    "description": "Software licence type."
                }
            }
        },
        "ui": {
            "type": "object",
            "description": "Manage the visual appearance and language of the application.",
            "properties": {
                "theme": {
                    "type": "string", 
                    "description": "Name of the folder in `./static/themes/` containig QSS styles."
                },
                "language": {
                    "type": "string", 
                    "description": "Name of the language folder in `./static/i18n/` to use in the application."
                }
            }
        },
        "window": {
            "type": "object",
            "description": "Defines the initial properties of the main window. The values declared here feed the `configure` method of the window.",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title appearing in the window's top bar."
                },
                "geometry": {
                    "type": "array",
                    "description": "Defines position and size: `[x, y, width, height]`.",
                    "minItems": 4,
                    "maxItems": 4,
                    "items": {"type": "integer"}
                },
                "size": {
                    "type": "array",
                    "description": "Initial size: `[width, height]`.",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "integer"}
                },
                "min_size": {
                    "type": "array",
                    "description": "Sets the minimum size of the window: `[width, height]`.",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "integer"}
                },
                "max_size": {
                    "type": "array",
                    "description": "Sets the maximum size of the window: `[width, height]`.",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "integer"}
                },
                "min_width": {
                    "type": "integer",
                    "description": "Sets the minimum width of the window: `width`."
                },
                "max_width": {
                    "type": "integer",
                    "description": "Sets the maximum width of the window: `width`."
                },
                "min_height": {
                    "type": "integer",
                    "description": "Sets the minimum height of the window: `height`."
                },
                "max_height": {
                    "type": "integer",
                    "description": "Sets the maximum height of the window: `height`."
                },
                "opacity": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 1.0,
                    "description": "Window transparency level. From `0.0 to 1.0`."
                },
                "state": {
                    "type": "string",
                    "description": "Initial state of the window.",
                    "enum": ["normal", "minimized", "maximized", "fullscreen", "active"]
                },
                "flags": {   
                    "type": "array",
                    "description": "Special window behaviors.",
                    "uniqueItems": true,
                    "items": {
                        "type": "string",
                        "enum": [
                            "normal", "dialog", "sheet", "tooltip", "splash", "popup", "tool", "desktop",
                            "sub", "always-on-top", "always-on-bottom", "context-help", "bypass", "transparent-input",
                            "no-focus", "frameless", "title-bar", "maximize-button", "minimize-button", "close-button",
                            "sys-menu", "fixed-size"    
                        ]
                    }
                },
                "attributes": {
                    "type": "array",
                    "description": "Low-Level Qt attributes.",
                    "uniqueItems": true,
                    "items": {
                        "type": "string",
                        "enum": [
                            "mouse-tracking", "input-method-enabled", "transparent-for-mouse-events",
                            "delete-on-close", "hover", "accept-drops", "input-method-transparent",
                            "accept-touch-events", "opaque-paint-event", "no-system-background",
                            "styled-background", "translucent-background", "show-without-activation",
                            "always-show-tool-tips", "quit-on-close", "no-child-events-for-parent", 
                            "x11-net-vm-window-type-dialog", "x11-net-wm-window-type-tool-bar",
                            "x11-net-wm-window-type-utility", "x11-net-wm-window-type-notification"
                        ]
                    }
                }
            }
        }
    },
    "additionalProperties": true
}"""
