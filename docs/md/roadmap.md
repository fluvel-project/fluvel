# Roadmap
With the base of core systems already developed ([key features](../../README.md#key-features)), Fluvel now needs to expand them to encompass and expose the broad PySide6 ecosystem. Therefore, here are some of the goals in mind.

* **Utility and Frontend API**
  * **Expansion of the F-Widgets Library**: Fluvel needs to cover the broad spectrum of `QWidgets` and expose a simple API on them.
  * **Development of Systems for Coverage of the `QtGui` Module**: You can see a glimpse of this in the Animator, Factory, and Customizer modules in the fluvel/composer directory. The main concept is to centralize and simplify the graphic component design philosophy proposed by PySide6.

* **Core API**
  * **Native Tools for Freezing Applications**: Simplified integration with packagers like PyInstaller and Nuitka. The goal is to provide a predefined configuration that automatically handles the inclusion of critical directories (`ui/`, `static/`, `assets/`) and the `config.toml` file, allowing you to create executables with a single command from the Fluvel CLI.
  * **Reloader Manual Configuration**: Expose the `Hot-Reloader`  configuration API in the `config.toml` file to manage its behavior,  allow the addition of new folders and files to listen, etc.
  * **First-Class IDE Tooling & DX Expansion**: Development of dedicated tools and extensions for popular editors such as Visual Studio, VSCode, VSCodium, Code - OSS, PyCharm, etc. This includes a dedicated Language Server (LSP) for the .fluml language and the automatic generation of type-safe stubs (.pyi) for the i18n system.
  * **AI-Powered Automatic Translation System**: Leveraging GenAI APIs (like Google Gemini) or traditional translation services (DeepL/Google Translate), the translate command will automatically generate complete, ready-to-use translations from your `.fluml` and `.xml` content, transforming i18n into a near zero-effort task that understands contextual formatting.
  * **Continuous Structural Refinement & Testing:**: Development of a robust testing suite focused on:
    * **Structural Coherence**: Ensuring the **Fluvel-Pyro** connection remains **linear** and **deterministic** as new F-Widgets or features are added, preventing graph complexity bloat.
    * **Performance Benchmarking**: Stress testing Fluvel with complex UI compositions to ensure that hot-reloading and widget rendering remain instantaneous even in large-scale applications.
    * **High-performance Optimizations**: The possibility of integrating languages ​​like Rust or Cython into Fluvel to improve algorithms and optimize critical framework modules (like `QSSProcessor`, `StateManager`, etc.) is not ruled out.
* **Documentation**
  * **Comprehensive Documentation**: Implementation of Sphinx-rST documentation, built directly from high-quality Docstrings, covering API references, in-depth tutorials, and best practices for developing scalable applications with Fluvel.


