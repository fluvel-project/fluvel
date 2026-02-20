# 3. Styling

`Fluvel` offers a robust hybrid styling system. On one hand, it allows for Global Theme management through traditional `.qss` (Qt Style Sheets) files; on the other, it introduces its own Inline Style Processor (Utility-First) for fast, specific compositions at the component level.

> [!NOTE]
> In the public folder of this repository you can find the basic Tailwind-like utilities for each theme you create.

## 3.1 Global Themes

The theme architecture is directory-based. To create a new theme, simply add a folder in `static/themes/` with the desired name (e.g., `modern-dark`) and place your `.qss` files inside.

```powershell
├───static                      # Specialized directory for themes and languages
│   ├───themes                  # QSS Themes
│   │   ├───bootstrap           # Specific theme 'bootstrap'
│   │   └───modern-dark         # Specific theme 'modern-dark'
```

To define the default theme the application will use at startup, edit your `config.toml` file:

```toml
[ui]
theme = "modern-dark"
```

**Changing Theme at Runtime**: The standard method for changing themes is using the `set_theme()` method from the global manager `er` in any module of your application. This will immediately change your application's theme by loading all `.qss` files from the selected folder.

```python
from fluvel import er

# Change theme immediately
er.set_theme("bootstrap") 

# Returns a reference to the set_theme function that changes the theme when executed
# Useful for clickable elements
er.as_set_theme("bootstrap") 
```

> [!TIP]
> Another way to change an application's theme is through the `App` instance that lives within each `Page` class.
> ```python
> class TestPage(Page):
>   def build(self):
>       self.app.change_theme("bootstrap")
> ```

## 3.2 Utility-First Styling (Inline)
Inspired by modern web frameworks, `Fluvel` incorporates the `QSSProcessor`, a lexical preprocessing engine designed to write complex styles directly in Python.

Unlike simple string replacement, the `QSSProcessor` is an intelligent system that analyzes, validates, and compiles abbreviated tokens into optimized native QSS blocks.

### 3.2.1 Syntax & Tokens
The syntax follows the `token[value]` pattern. The processor translates these tokens using an internal property dictionary (`STYLE_TOKENS`), covering everything from backgrounds and borders to complex gradients.

```python
# A button with a red background, bold white text, and a hover effect that darkens the background
v.Button(text="Alert", style="bg[red] fg[white] h::bg[darkred] font-bold")
```

> [!TIP] 
> Consult the [full reference of available tokens](engines/qss.md) in the technical documentation.

### 3.2.2 State Modifiers (Interactive Styles)
Similarly, the engine supports **state prefix** (`::`) syntax to handle interactions.
* `h::` **Hover**: Applied when the cursor is over the widget.
* `p::` **Pressed**: Applied when the widget is pressed.
* `d::` **Disabled**: Applied when the widget is disabled.
* `c::` **Checked**: Applied when a toggleable element is active.

```python
# A button that is blue, turns light blue on hover, 
# and dark gray when pressed.
v.Button(text="Interact", style="bg[blue] h::bg[skyblue] p::bg[#222]")
```

### 3.2.3 Gradient Generator
The processor includes a mathematical gradient generator. Instead of writing `qlineargradient(...)` syntax, simply define the colors separated by hyphens. The engine will calculate the stops automatically.

```python
with v.Vertical(style="bg-lgrad-h[#f00-#0f0-#00f]") as v: ...
```

> [!TIP]
> **Smart Linting**: In Debug mode, the `QSSProcessor` uses `difflib` to analyze your styles. If you mistype a token (e.g., `backgound[red]`), the console will warn you: *"Fluvel [SyntaxError]: Token 'backgound' does not exist. Did you mean 'bg'?"*

> [!IMPORTANT]
> **Performance**: The engine uses `functools.lru_cache` with a capacity of `2048 slots` to memorize lexical analysis results. This ensures that if you use the same style in 1,000 table cells or many widgets, the computational processing cost is O(1) (constant time), eliminating any rendering latency.