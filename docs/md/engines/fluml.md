
#### Source Code: [fluvel/engines/fluml.py](../../../fluvel/engines/fluml.py)

# Syntactic rules for declaring static text content application

* **`#`**: Inline comments
* **`.. text-id:`**: **Directive** that declares the start of a static text block (ID used as a reference for the `i18n` system).
* **Multiline Content:** Any line following a directive that does not start a new directive is considered a continuation of the previous block. **Indentation is optional** for multiline content, but recommended for readability.

## Style Rules
|Style            | Syntax                       | Result in RichText                       |
|:----------------|:-----------------------------|:-----------------------------------------|
| Italic          | **`* *`**                    | `<i>content</i>`                         |          
| Bold            | **`** **`**                  | `<b>content</b>`                         |           
| Bold and Italic | **`*** ***`**                | `<b><i>content</i></b>`                  |
| Underline       | **`__ __`**                  | `<u>content</u>`                         |  
| Line Through    | **`-- --`**                  | `<s>content</s>`                         |  
| Subscript       | **`~~ ~~`**                  | `<sub>content</sub>`                     |
| Superscript     | **`^^ ^^`**                  | `<sup>content</sup>`                     |
| Link            | **`{ text \| url }`**        | `<a href='url'>text</a>`                 |
| Color           | **`[ color \| text ]`**      | `<span style='color:color;'>text</span>` |
| Placeholders    | **`{name}, {age}, etc...`**  | `Dynamic variables replaced at runtime.` |
| Line Break      | **`\n`**                     | `<br>`                                   |

>![Important] 
> To ensure dynamic variable substitution works correctly, placeholder names (e.g., {user_age}) must follow Python's variable naming rules (start with a letter or underscore, contain only alphanumeric characters and underscores). This is necessary because the .format_map() method is used internally to replace values ​​at runtime.

 ## Demostration
```fluml
.. home.title: Title of the Home Page

.. txt.welcome: 
    **Hi!** {name}, this is *a* __demonstration__. 
    Check our *{ Youtube | https://www.youtube.com }* channel.
    
.. txt.description.long:
    This is the first line of a long description.
    The parser joins this with the next line using a space. \n
    But this marker forces a real break in the UI.
 ```