<div align="center">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/brands/logo-dark.svg">
    <img src="./assets/brands/logo-light.svg" alt="Fluvel Logo">
  </picture>

  ![Current Version](https://img.shields.io/badge/Version-1.0.0b1-green)
  ![PyPI - License](https://img.shields.io/badge/License-LGPLv3--or--later-green)
  ![Python Version](https://img.shields.io/badge/Python-3.11+-blue)
  ![Platform Desktop](https://img.shields.io/badge/Platform-Desktop%20UI-blue)
  ![Integrated CLI](https://img.shields.io/badge/CLI-Integrated-C084FC)
  ![Hot Reloading](https://img.shields.io/badge/Hot--Reloading-Instantaneous-C084FC)
</div>

> [!TIP]
> **Stable API Architecture (Beta 1.0.0b1)**: Although Fluvel is currently in the testing phase, the class structure, the context handler system, and the PYRO state engine are definitive. Future updates will focus on internal optimization and component expansion, ensuring that your current code remains compatible with stable versions. Caution is recommended in critical production environments until the final 1.0 release.

# About Fluvel

**Fluvel** is a framework built on top of **PySide6**. It abstracts the complexity of Qt by replacing manual layout management with **declarative context handlers** and a **Tailwind-inspired styling processor**. Powered by the **PYRO reactive engine**, it enables **deterministic state-to-UI binding** and a **decoupled resource architecture** (i18n/theming), ensuring that large-scale Python applications remain performant and easy to refactor.

<p align="center">
  <img src="./assets/gifs/hot-reloader-demo.gif" alt="Fluvel Demo: Start Project & Hot-Reload" width="100%">
  <br>
  <i>Fluvel in action: Scaffolding a project and real-time UI updates via Hot-Reload.</i>
  <br>
  <a href="#1-installation"><b>Get started in 30 seconds →</b></a>
</p>

## Key Features

* **Declarative UI Architecture**: Interface definition via the `Page` abstract class, utilizing a **context-handler-based** syntax. This approach abstracts boilerplate layout logic, focusing on component hierarchy and structural intent. [Learn more →](docs/md/ui-design.md)

* **PYRO Reactive Engine**: A standalone, agnostic state engine (*Pyro Yields Reactive Objects*) featuring **automatic dependency tracking**. It supports reactive primitives and collections (lists/dicts), enabling fine-grained UI binding and deterministic state synchronization. [Learn more →](docs/md/reactivity.md)

* **Utility-First Styling & QSSProcessor**: High-performance styling via an integrated **token-based** system. The `QSSProcessor` parses inline utility classes and external QSS, facilitating rapid component skinning without manual stylesheet overhead. [Learn more →](docs/md/styling.md)
    * *Example*: `Button(style="primary fg[red] b[2px solid blue]")`

* **Structural i18n & Logic Decoupling**: Separation of concerns through `.fluml` **(Fluvel Markup Language)** and XML schemas. This architecture decouples static/dynamic content from the Python business logic, enabling independent translation workflows and resource management. [Learn more →](docs/md/i18n.md)

* **Stateful Routing System**: Centralized navigation management via the `Router` class, handling page lifecycle and transitions within a unified application state.

* **Integrated Dev-Tools CLI**: A dedicated command-line interface for automated project scaffolding, asset management, and deployment workflows.

* **Hot-Reloading Environment**: A development-time watcher that performs **runtime hot-patching** of pages. It allows for instantaneous UI and theme iterations without destroying the application process or losing current state. [Learn more →](docs/md/ui-design.md#24-the-hot-reloader)

## 🚀 Quick Start

### 1. Installation
To install this version, use the following command:

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Fluvel
pip install fluvel
```

### 2. Starting a Project
Create your first application with the integrated CLI:

```bash
fluvel startproject
fluvel run
```

## Documentation Guide

Once you have your first project up and running, you can delve deeper into Fluvel's fundamental pillars. Each of these modules is designed to cover a specific aspect of your application's lifecycle and development:

* [1. Architecture](docs/md/architecture.md)
* [2. UI Design](docs/md/ui-design.md)
* [3. Styling](docs/md/styling.md)
* [4. Reactivity](docs/md/reactivity.md)
* [5. Internationalization (i18n)](docs/md/i18n.md)
* [6. Deployment](docs/md/deployment.md)

## Project Roadmap
We have big plans for `Fluvel`, including AI-powered translations, Rust-core optimizations, and advanced IDE tooling.

[See the full Roadmap here →](docs/md/roadmap.md)

## License
Fluvel is an open-source project, licensed under the [GNU LGPL-3.0 Licence](https://www.gnu.org/licenses/lgpl-3.0.html) (or any later version).