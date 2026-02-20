# 6. Build Your App

> [!IMPORTANT]
> **Production & Deployment (Beta 1.0.0b1)**: Currently, `Fluvel` is optimized for development workflows and rapid prototyping. While the framework is designed to be compatible with [Nuitka](https://github.com/Nuitka) (our recommended distribution tool due to its native compilation capabilities), full automation of the `build` process is still under development.
>
> For now, we recommend using `Fluvel` to create interfaces and reactive logic. Official support for executable creation via the CLI will arrive in upcoming stable versions.

If you still wish to bundle the application, you can use Nuitka manually by ensuring that you include the UI packages and resources.

**IMPORTANT NOTE**: For this to work, you must add your application pages manually in `app.py`:

```python
# app.py
import fluvel as fl

app = fl.App()
app.register(
    initial="/home", 
    pages=[
        "ui.pages.home.home_page",
        "ui.pages.settings.settings_page"
    ]
)

if __name__ == "__main__":
    app.run()
```

## 6.1 The `fluvel build` Command
Once the manual configuration in `app.py` is done, you must execute the `fluvel build` command. This early-stage command bundles all your resources from `static/` into a single distributable `rsrc/` folder that will be used in production. Then, it automatically modifies your `config.toml` file to set the `production = true` flag.

```toml
[fluvel]
production = true # IMPORTANT so the frozen application looks for resources in rsrc/
```

> [!TIP]
> At this point, try running `fluvel run` to see if your application works correctly in production mode and that the files in `rsrc/` are loaded properly.

## 6.2 Bundling with Nuitka

Once Nuitka is installed in the virtual environment, the next step is to run the following command to generate a compiled version.

```powershell
nuitka --standalone --plugin-enable=pyside6 --windows-console-mode=disable --include-data-dir=rsrc=rsrc --include-data-files=config.toml=config.toml --follow-imports --include-module=window --include-package=ui --output-dir=dist app.py
```

> [!NOTE]
> If this didn't work for you, remember that **Nuitka** is highly sensitive to the virtual environment structure and relative paths. Make sure to run the command from the project root (at the same level as `app.py`) and have all dependencies installed in the same `venv`.
> If you encounter a persistent error, we invite you to open an Issue in our repository detailing your operating system and console output. Your feedback is vital to perfecting the `fluvel build` command and bundling systems in the next stable version.