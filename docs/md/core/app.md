The `App` class is the main entry point and central controller for any application built with `Fluvel`. It inherits the responsibility of managing the application lifecycle, integrating `PySide6` with Fluvel’s routing, configuration, and content management system.

## Feature Summary

* **Lifecycle Management**: Initializes the QApplication and handles the event loop.
* **Dynamic Routing**: Registers and loads pages/views automatically or explicitly.
* **Configuration Management**: Loads global settings from the **config.toml** file (or similar).
* **Visual Identity**: Applies themes (QSS), icons, and organization metadata at the operating system level.
* **Internationalization**: Allows dynamic language switching and static content updates at runtime through the `App.change_language` method.

## Data Structures (TypedDict)

To ensure data integrity during configuration, the following typed dictionaries are used:

**`AppKwargs`**

Defines the application metadata for the operating system:

* `name`: Internal name.
* `display_name`: User-friendly name.
* `version`: App version.
* `organization` / `domain`: Organization data.
* `icon`: Path to the icon file.

**`AppRegisterKwargs`**

Defines the parameters for route registration:

* `initial`: Initial route to display.
* `pages`: Optional list of page modules to import.
* `animation`: Entry animation for the initial view.

## `App` Class Reference

`__init__(window_module_path: str = None, config_file: str = "config.toml")`

Initializes the base infrastructure.

1. Instantiates `QApplication`.
2. Loads configuration from the specified file.
3. Creates the main window (`MainWindow`).
4. Binds the `Router` to the application and the window.

`configure(**kwargs: Unpack[AppRegisterKwargs])`

Applies global settings to the `QApplication` instance. Uses an internal mapping to dynamically call Qt methods such as `setApplicationName` or `setWindowIcon`.

`register(initial: str, pages: list[str] = None, show_animation: str = None)`

* If `pages` are not provided, it automatically scans the `ui/pages/` directory for `.py` files.
* Imports the modules so that `@route` decorators are registered in the `Router`.
* Sets the initial view that the user will see.

`run()`

Displays the main window and starts the Qt execution loop (`exec()`).

`change_theme(new_theme: str)` / `change_language(new_language: str)`

Enable interface reactivity. They update the global configuration and trigger the reloading of QSS styles or `.fluml` content files respectively, without requiring the application to restart.

## Usage Example

```python
import fluvel as fl

# 1. Instantiate the application
app = fl.App(config_file="settings.toml")

# 2. Register pages and define initial routes
app.register(
    inicial="/dashboard",
    animation="fade_in"
)

# 3. Run
if __name__ == "__main__":
    app.run()
```

## Internal Methods

<table>
    <th>Method</th>
    <th>Description</th>
    <tr>
        <td><code>_load(filename: str)</code></td>
        <td>Initializes the <code>Settings</code> system and loads static content.</td>
    </tr>
    <tr>
        <td><code>_get_pages_to_import()</code></td>
        <td>Scans the file system for automatic page discovery.</td>
    </tr>
    <tr>
        <td><code>_create_main_window(path: str)</code></td>
        <td>Performs the dynamic import of the <code>MainWindow</code> class.</td>
    </tr>
    <tr>
        <td><code>_set_theme()</code></td>
        <td>Loads and applies the global QSS theme from <code>Settings.app.theme</code> to the application.</td>
    </tr>
</table>

## Special Internal Methods

`_get_pages_to_import()`

**Type**: `staticmethod`  
**Return**: `list[str]` (A list of module paths in dot-notation format).

This method implements automatic application page discovery. Its purpose is to dynamically locate all view modules within the project so that the `Router` can register routes defined using `@route` decorators.

**Operating Mechanism**

1. **Feature Scanning**: Accesses the directory defined in `PAGES_DIR` (by default `ui/pages/`) and identifies all subfolders. Each subfolder is considered a "feature" or interface section (e.g., `home`, `dashboard`, `auth`, `settings`).
2. **Module Filtering**: Within each subfolder, it searches for files with the `.py` extension using the exclusion pattern `[!_]*.py`.
    * **Includes**: View logic files (e.g., `login_page.py`).
    * **Ignores**: Private or package initialization files (e.g., `__init__.py`), preventing accidental execution or import errors.
3. **Python Path Mapping**: Transforms the file system path into a valid Python import path.

### Technical Importance

`Fluvel` is a decorator-based framework, meaning that the view code (the class decorated with `@route`) is not executed unless the module is explicitly imported.

Without `_get_pages_to_import`, each page would have to be manually imported in the `main.py` file. This method ensures that when calling `app.register()`, all application decorators are read, registered, and properly managed by the `Router`.

**Developer Note**: If you decide to organize your pages in a location different from `ui/pages/`, you must manually pass the list of modules to the `register(pages=[])` method to prevent this method from failing or not finding your views.
