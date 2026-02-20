The `config.toml` file is the core of customization for a `Fluvel` application. This file allows you to define the framework’s behavior, the application’s identity at the operating system level, interface preferences, and the physical properties of the main window without modifying the source code.

## File Structure

The file is organized into four main sections (tables):

### `[fluvel]` Section

Controls the internal behavior of the framework.

<table>
  <tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>DEV_MODE</code></td>
    <td><code>bool</code></td>
    <td>If `true`, enables debugging tools and extended development logs (e.g., <code>QSSProcessor.lint</code>).</td>
  </tr>
</table>

### `[app]` Section

Defines the application’s identity and metadata. These values are processed by the `configure` method of the `App` class (see `app.md`).

<table>
  <tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>name</code></td>
    <td><code>str</code></td>
    <td>Internal technical name (used for data file paths).</td>
  </tr>
  <tr>
    <td><code>display_name</code></td>
    <td><code>str</code></td>
    <td>The name the user sees in the taskbar or menus.</td>
  </tr>
  <tr>
    <td><code>version</code></td>
    <td><code>str</code></td>
    <td>Current version of the application.</td>
  </tr>
  <tr>
    <td><code>organization</code></td>
    <td><code>str</code></td>
    <td>Name of the company or author.</td>
  </tr>
  <tr>
    <td><code>domain</code></td>
    <td><code>str</code></td>
    <td>Organization domain (used to identify the app on Linux/macOS).</td>
  </tr>
  <tr>
    <td><code>desktop_filename</code></td>
    <td><code>str</code></td>
    <td>Unique identifier for the operating system launcher.</td>
  </tr>
  <tr>
    <td><code>icon</code></td>
    <td><code>str</code></td>
    <td>Relative path to the image file that will serve as the global icon.</td>
  </tr>
  <tr>
    <td><code>licence</code></td>
    <td><code>str</code></td>
    <td>Software license type.</td>
  </tr>
</table>

### `[ui]` Section

Manages the visual appearance and language of the application.

<table>
  <tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>theme</code></td>
    <td><code>str</code></td>
    <td>Name of the theme folder in <code>./static/themes/</code> that contains the QSS styles (e.g., "bootstrap", "modern-dark").</td>
  </tr>
  <tr>
    <td><code>language</code></td>
    <td><code>str</code></td>
    <td>Name of the language folder in <code>./static/themes/</code> used to load <code>.fluml</code> and <code>.xml</code> text files (e.g., "es", "en").</td>
  </tr>
</table>

### `[window]` Section

Defines the initial properties of the `MainWindow`. The values declared here are passed to its `configure` method.

<table>
  <tr>
    <th>Key</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>title</code></td>
    <td><code>str</code></td>
    <td>Title displayed in the top window bar.</td>
  </tr>
  <tr>
    <td><code>geometry</code></td>
    <td><code>array</code></td>
    <td>Defines position and size <code>[x, y, width, height]</code>.</td>
  </tr>
  <tr>
    <td><code>size</code></td>
    <td><code>array</code></td>
    <td>Initial size <code>[width, height]</code>.</td>
  </tr>
  <tr>
    <td><code>min_size</code> / <code>max_size</code></td>
    <td><code>array</code></td>
    <td>Resize limits <code>[width, height]</code>.</td>
  </tr>
  <tr>
    <td><code>min_width</code> / <code>max_width</code></td>
    <td><code>int</code></td>
    <td>Specific width limits.</td>
  </tr>
  <tr>
    <td><code>min_height</code> / <code>max_height</code></td>
    <td><code>int</code></td>
    <td>Specific height limits.</td>
  </tr>
  <tr>
    <td><code>opacity</code></td>
    <td><code>float</code></td>
    <td>Window transparency level <code>(0.0 to 1.0)</code>.</td>
  </tr>
  <tr>
    <td><code>show_mode</code></td>
    <td><code>str</code></td>
    <td>Initial state. Possible values defined in <code>~fluvel.core.enums.window_state</code>.</td>
  </tr>
  <tr>
    <td><code>flags</code></td>
    <td><code>array</code></td>
    <td>Special window behaviors. Possible values defined in <code>~fluvel.core.enums.window_type</code>.</td>
  </tr>
  <tr>
    <td><code>attributes</code></td>
    <td><code>array</code></td>
    <td>Low-level Qt attributes. Possible values defined in <code>~fluvel.core.enums.widget_attributes</code>.</td>
  </tr>
</table>

## Complete Configuration Example

```toml
[fluvel]
DEV_MODE = true

[app]
name = "MyFluvelApp"
display_name = "Fluvel Designer"
version = "0.1.0"
organization = "Robotid"
icon = "assets/logo.png"

[ui]
theme = "modern"
language = "es"

[window]
title = "Fluvel v0.1"
size = [800, 600]
min_size = [400, 300]
opacity = 0.95
show_mode = "normal"
flags = ["sys-menu", "title", "minimize-button", "close-button"]
```
