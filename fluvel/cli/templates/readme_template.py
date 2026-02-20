# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

README_TEMPLATE = """# Hi! Welcome to Fluvel Framework

Welcome to the internal core of your **Fluvel** project. Thank you for choosing this framework to build your desktop applications!

If you want to contribute, report bugs, or explore the source code, visit our [Official GitHub Repository](https://github.com/fluvel-project/fluvel) ⭐.

**What is this folder?**

The `.fluvel/` directory is designed to enhance your **Developer Experience (DX)**. It contains the technical metadata necessary for your IDE to understand the framework's internal logic, providing:
* **Real-time Validation**: JSON and XSD schemas for `config.toml` and `.xml` files.
* **Autocompletion**: Instant suggestions for window flags, attributes, and styles.
* **Structural Consistency**: Ensures your project configuration follows the Fluvel standard.
> [!Tip]
> Use the command `fluvel generate-stubs` whenever you update your `config.toml` or `.fluml` files. This will update the internal stubs and give you full autocompletion and type safety for your settings and translations!

## IDE Integration

To enable full support for autocompletion and validation, follow the instructions for your editor:

**Visual Studio Code**
Fluvel is optimized for VS Code. To enable all features, create or edit the file `.vscode/settings.json` in your project root and paste the following:
```json
{
    "python.analysis.include": [".fluvel/stubs"],
    "python.analysis.stubPath": ".fluvel/stubs",
    "python.analysis.extraPaths": ["./.fluvel/stubs"],
    "python.analysis.useLibraryCodeForTypes": true,
    "json.schemas": [
        {
            "fileMatch": ["config.json"],
            "url": "./.fluvel/schema/config.schema.json"
        }
    ],
    "evenBetterToml.schema.associations": {
        "config.toml": "./.fluvel/schema/config.schema.json"
    },
    "xml.fileAssociations": [
        {
            "pattern": "**/static/i18n/**/menus/*.xml",
            "systemId": "./.fluvel/schema/menu.schema.xsd"
        }
    ]
}
```

---
This directory is automatically excluded from your git history (via `.gitignore`) to keep your repository clean of IDE-specific configurations. Support for other IDEs like PyCharm is currently limited and planned for future releases.
"""
