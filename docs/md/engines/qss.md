#### Source Code: [fluvel/engines/qss.py](../../../fluvel/engines/qss.py)

# API Reference: QSSProcessor
The `QSSProcessor` is the utility styling engine for `Fluvel`. It allows translating a concise and modern syntax into native **QSS (Qt Style Sheets)** code.

## Basic Syntax
---

`prefix::token[value]`

* **`prefix` (Optional)**: Defines the state of the widget (hover, pressed, etc.). If omitted, it applies to the normal state of the widget.
* **`token`**: The style property to apply (e.g., `bg`, `fs`).
* **`value`**: The corresponding value (e.g., `red`, `12px`, `#333`).

## Pseudo-states (Prefixes)
---
| Prefix | State | Description |
|--------|-----------|---------------------------------------------------------|
| `h::` | Hover | Applies when the mouse is over the widget. |
| `p::` | Pressed | Applies when the widget is pressed. |
| `d::` | Disabled | Applies when the widget is disabled. |
| `c::` | Checked | Applies when the widget (e.g., Checkbox) is checked. |

**Example**: `h::bg[red]` -> Applies red background on hover.

## Style Tokens
---

### Backgrounds
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `bg` | `background-color` | Background color. |
| `bg-img` | `background-image` | Background image URL. |
| `bg-repeat` | `background-repeat` | Image repetition. |
| `bg-position`| `background-position`| Image position. |
| `bg-origin` | `background-origin` | Background origin. |
| `bg-clip` | `background-clip` | Background clip. |

### Gradients
---
| Token | Value Syntax | Description |
| :--- | :--- | :--- |
| `bg-lgrad-v` | `color1-color2-...` | **Vertical** linear gradient. |
| `bg-lgrad-rv`| `color1-color2-...` | **Inverted** Vertical linear gradient. |
| `bg-lgrad-h` | `color1-color2-...` | **Horizontal** linear gradient. |
| `bg-lgrad-rh`| `color1-color2-...` | **Inverted** Horizontal linear gradient. |
| `bg-rgrad` | `color1-color2-...` | **Radial** gradient. |

* Note: Colors must be separated by hyphens (`-`).

### Selection & Images
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `sel-bg` | `selection-background-color` | Background color for selected items. |
| `sel-fg` | `selection-color` | Text color for selected items. |
| `b-img` | `border-image` | Border image (stretched). |
| `img` | `image` | Element image. |
| `img-pos` | `image-position` | Image position. |

### Borders & Radius
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `b` | `border` | Full border. |
| `b-color` | `border-color` | Border color. |
| `b-style` | `border-style` | Border style. |
| `b-width` | `border-width` | Border width. |
| `b-l`, `b-t`, `b-r`, `b-b` | `border-left/top/right/bottom` | Individual side border. |
| `br` | `border-radius` | Border radius (rounded corners). |
| `br-tl` | `border-top-left-radius` | Top-left corner radius. |
| `br-tr` | `border-top-right-radius` | Top-right corner radius. |
| `br-bl` | `border-bottom-left-radius`| Bottom-left corner radius. |
| `br-br` | `border-bottom-right-radius`| Bottom-right corner radius. |
| `br-t` | `border-top-left/right-radius`| Top corner radius (both). |
| `br-b` | `border-bottom-left/right-radius`| Bottom corner radius (both). |
| `br-l` | `border-top/bottom-left-radius`| Left corner radius (both). |
| `br-r` | `border-top/bottom-right-radius`| Right corner radius (both). |

### Outlines
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `o` | `outline` | Outline property. |
| `o-rad` | `outline-radius` | Outline radius. |
| `o-style` | `outline-style` | Outline style. |
| `o-off` | `outline-offset` | Outline offset. |

### Font/Text
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `fs` | `font-size` | Font size. |
| `fg` | `color` | Text color (Foreground). |
| `f-weight` | `font-weight` | Font weight (bold, etc.). |
| `f-align` | `text-align` | Text alignment. |
| `f-family` | `font-family` | Font family. |
| `f-style` | `font-style` | Font style (italic, etc.). |
| `f-decoration`| `text-decoration` | Text decoration (underline, etc.). |

### Spacing/Size
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `m` | `margin` | Full margin. |
| `m-t`, `m-b`, `m-l`, `m-r`| `margin-top/bottom/left/right` | Individual margin side. |
| `m-tl`, `m-tr`, `m-bl`, `m-br`| `margin-top/bottom-left/right` | Dual side margin (corner). |
| `m-v` | `margin-top` & `margin-bottom`| Vertical margin. |
| `m-h` | `margin-left` & `margin-right`| Horizontal margin. |
| `p` | `padding` | Full padding. |
| `p-t`, `p-b`, `p-l`, `p-r`| `padding-top/bottom/left/right` | Individual padding side. |
| `p-tl`, `p-tr`, `p-bl`, `p-br`| `padding-top/bottom-left/right` | Dual side padding (corner). |
| `p-v` | `padding-top` & `padding-bottom`| Vertical padding. |
| `p-h` | `padding-left` & `padding-right`| Horizontal padding. |
| `w` | `width` | Width. |
| `h` | `height` | Height. |
| `min-w`, `min-h` | `min-width/height` | Minimum size. |
| `max-w`, `max-h` | `max-width/height` | Maximum size. |

### Subcontrols & Qt Properties
---
| Token | QSS Property | Description |
| :--- | :--- | :--- |
| `sc-org` | `subcontrol-origin` | Subcontrol origin. |
| `sc-pos` | `subcontrol-position` | Subcontrol position. |
| `icon-s` | `qproperty-iconSize` | Icon size (for buttons/labels). |

---
Usage Examples

1. Simple style
`v.Button(style="bg[#3498db] fg[white] br[5px]")`

2. Style with pseudo-state (Hover)
`v.Button(style="bg[#3498db] h::bg[#2980b9] h::fg[black]")`

3. Gradient and border
`v.Vertical(style="bg-lgrad-v[#fff-#f0f0f0] b[1px solid #ccc] br[10px]")`