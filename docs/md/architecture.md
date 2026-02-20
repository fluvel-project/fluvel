# 1. Architecture & Lifecycle

This section explores the structural blueprint of **Fluvel**. Understanding how the framework orchestrates the application lifecycle, project hierarchy, and page routing is essential for building scalable and maintainable desktop applications.

## 1.1 Initialization

As with any project, our first step is to choose a directory of our preference and create a folder with the project name—in our case, `my_app/`—which will contain the files and directories necessary for our project, initiating the development lifecycle.

### 1.2 Initial Commands

Once the `my_app/` directory is created, we proceed with the initial configuration and installation of `Fluvel` from `PyPi` following the first part of the guide [Quick Start](../../README.md#-quick-start).

With our virtual environment active, it is time to write our first command in `Fluvel`:

```powershell
fluvel startproject
```

This will automatically generate the initial project structure.

Now, to ensure that our application runs correctly, copy the command below. You will see a default page where `Fluvel` welcomes you:

```powershell
fluvel run
```

> [!NOTE]
> If you encounter issues at this or any other point, feel free to send us a bug report or a support question directly in the [Issues section of our GitHub repository](https://github.com/fluvel-project/fluvel/issues).

### 1.3 Overview of the Project Structure

You likely noticed that when running the `fluvel startproject` command, a structure similar to this was printed in the console:

```bash
my_app/:
├───.fluvel                 # IDE Intelligence (Stubs & Schemas)
├───assets                  # (Optional) Binary resources (images, fonts, etc.)
├───static                  # Specialized directory for themes and languages -- (!)
│   ├───i18n                # Fluml and i18n content files -- (!)
│   │   └───en              # (Example) Language files for English
│   └───themes              # Directories for QSS styles/themes -- (!)
│       └───bootstrap/      # Initial theme (e.g., fluvel-bootstrap.min.qss)
├───ui                      # UI source code -- (!)
│   ├───components          # (Optional) Simple, reusable widgets @Component
│   ├───prefabs             # (Optional) Complex components decorated with @Prefab
│   ├───models              # (Optional) Reactive state models (Pyro)
│   └───pages               # Main application pages -- (!)
│       └───home/           # Dedicated directory for the composition of the home page
│           ├───components  # (Optional) Dedicated directory for specific home/ components
│           ├───prefabs     # (Optional) Dedicated directory for specific home/ prefabs
│           └───home.py     # Example page (Home)
│   config.toml             # Global application configuration file -- (!)
│   app.py                  # Application entry point -- (!)
│   window.py               # Custom AppWindow(QMainWindow) class -- (!)
```

If you look closely, you will see that some are marked with `(!)`, meaning that the file or directory is an **essential** component of `Fluvel`, containing critical configuration or the start of the application lifecycle.

Now we will briefly break down the intent of the most important files in `Fluvel`: 

| File/Directory | Purpose |
| -------------- | ------- |
| `app.py` | It is the main entry point. Here, the `Fluvel` application instance is initialized, and global configuration loading (`config.toml`) is managed. |
| `window.py` | Contains the `MainWindow` class, intended to customize the behavior of the main window. |
| `config.toml ` / `config.json` | Contains specifications for configuring application metadata, the main window, and Framework behavior. |

>[!Warning] 
> Renaming files/directories marked with `(!)` is not recommended due to the need for them to be automatically located by the framework.

Knowing that the entry point of a `Fluvel` application is the `./app.py` module, let's see how it is composed:

```python
import fluvel as fl

app = fl.App()
app.register(initial="/home")

if __name__ == "__main__":
    app.run()
```

The first thing we notice is the import of the `fluvel` package as a `namespace` (this is not a convention; you can use it this way or import classes and/or functions directly).

Then we instantiate the [App](core/app.md) class, which is "the application itself," and through its `register` method, we indicate which initial page to show (we will learn more about this in the [Page Composition](#13-page-composition) section).

Finally, we start the Qt loop (`exec()`) and show the window (`MainWindow`) through the `run` method.

> [!NOTE]
> The `fluvel run` command is not strictly necessary to start the application; it is also possible to do so by executing the `app.py` script via the Python interpreter (e.g., `python app.py`).

### 1.4 Page Composition

We have reached one of Fluvel's most unique features: **Interface Composition**.

Structurally, the central widget of the `MainWindow` is a `QStackedWidget`, meaning a widget capable of stacking other containers (your pages) in its interior **stack** and displaying them selectively. Thanks to this, interface composition can be seen as several SPAs (Single Page Applications) living within the stack and delegating their visualization to the [Router](#133-the-router-class) component.

#### 1.4.1 The `Page` Class

All application views must inherit from the `Page` class. This class provides the necessary environment to use Fluvel's ***Context Handlers*** and manage the interface lifecycle.

Each `Page` must implement the `build()` method:

```python
import fluvel as fl

class MyPage(fl.Page):
    def build(self): 

        # All UI construction logic resides here
        with self.Vertical() as v:
            v.Label(text="Hello World")
```

> [!IMPORTANT]
> In the `Page` inheritance tree, one of its bases is `QFrame`, which means that each page is not just a design canvas, but a **Qt Widget** with full access to the PySide6 API, allowing it to override native methods like `keyPressEvent` or `resizeEvent`.

#### 1.4.2 The `@route` Decorator

For a page to be accessible, it must be registered in the navigation system. This is achieved through the `@route` decorator, which binds a **unique path** to the page class.

```python
@fl.route("/home")
class HomePage(fl.Page):
    def build(self): ...
```

> [!IMPORTANT]
> Pages must reside in the `ui/pages/` directory. `Fluvel` uses this standard to organize code, allowing each page to have its own workspace (local components, prefabs, models, etc.).

#### 1.4.3 The `Router` Class

When a `Page` is created along with its `@route` decorator, the latter registers the assigned `path` in the `Router` class.

This static class is responsible for deciding which page to show at any given moment in the `MainWindow`. It can be imported from any module, and through its `show()` method, it can switch from one page to another.

```python
from fluvel import Router

# Switch to the test page with a fade-in animation
Router.show("/test", animation="fade_in")
```

> [!IMPORTANT]
> When executing the `show()` method, the `Router` checks its internal stack to see if the page has already been loaded; if not, it proceeds to instantiate the page and call its `build()` method. This results in the `build()` method only running once (Lazy Instantiation)—the first time the page is required by the Router—which optimizes memory usage and startup speed.

**Key Features:**
- **Lazy Instantiation**: Pages are not created until they are called for the first time. The `Router` instantiates the class, calls `build()`, and adds it to the main window stack automatically.
- **State Management**: The `Router` maintains a reference to the **page_instance** once created, allowing the page state to persist while the application is open.
- **Integrated Animations**: Thanks to the `Animator` module, switching between pages can be fluid using effects like `fade_in`, `slide_in`, among others.