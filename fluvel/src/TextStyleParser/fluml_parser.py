import re
from collections import defaultdict
from typing import Optional, Dict

class FlumlParser:

    # Pattern to detect the start of a block: ".. id: fluml-content"
    PATTERN = re.compile(r"^\s*\.\.\s*(?P<id>.*?):\s*(?P<content>.*)\s*$")

    blocks = defaultdict(list)

    @classmethod
    def parse(cls, text: str) -> None:
        """
        Analyze the content line by line.
        If you find “.. id:”, set the current context.
        The following lines are added to that context until another ID is found.
        """

        cls.blocks.clear()

        # Status to know who the current line belongs to
        current_id: Optional[str] = None 

        for raw_line in text.splitlines():
            clean_line = raw_line.strip()
            
            # Ignore empty lines or comments
            if not clean_line or clean_line.startswith("#"):
                continue

            _match = cls.PATTERN.match(raw_line)
            
            if _match:
                # It is a definition line (e.g., “.. title: Hello”)
                current_id = _match.group("id").strip()
                content = _match.group("content").strip()
                
                # If there is content on the same line as the definition, we save it.
                if content:
                    cls.blocks[current_id].append(content)
            
            elif current_id:
                # If it is not a definition, it is a continuation of the previous text (multiline)
                # We only save it if we already have an active ID defined
                cls.blocks[current_id].append(clean_line)

    @classmethod
    def _apply_styles(cls, text: str) -> str:
        """
        This method finds and translates patterns written in FLUML to the corresponding HTML syntax.
        *If more than one pattern matches, the `<span>` tags are nested.*
        """

        # LINK -> {content | href}
        text = re.sub(r"\{(.*?)\s*\|\s*(.*?)\}", r"<a href='\2'>\1</a>", text)

        # UNDERLINE -> __content__
        text = re.sub(
            r"__([^_]+)__", r"<span style='text-decoration: underline;'>\1</span>", text
        )

        # LINE-THROUGH -> --content--
        text = re.sub(
            r"--([^-]+)--",
            r"<span style='text-decoration: line-through;'>\1</span>",
            text,
        )

        # BOLD AND ITALIC -> ***content***
        text = re.sub(
            r"\*\*\*([^\*]+)\*\*\*",
            r"<span style='font-weight: bold; font-style: italic;'>\1</span>",
            text,
        )

        # BOLD -> **content**
        text = re.sub(
            r"\*\*([^\*]+)\*\*", r"<span style='font-weight: bold;'>\1</span>", text
        )

        # ITALIC -> *content*
        text = re.sub(
            r"\*([^\*]+)\*", r"<span style='font-style: italic;'>\1</span>", text
        )

        # VERTICAL ALIGN SUPER -> <sup>content</sup>
        text = re.sub(
            r"\^\^([^^]+)\^\^", r"<span style='vertical-align: super;'>\1</span>", text
        )

        # VERTICAL ALIGN SUB -> <sub>content</sub>
        text = re.sub(
            r"~~([^\~].*?)~~", r"<span style='vertical-align: sub;'>\1</span>", text
        )

        return text

    @classmethod
    def render_html(cls) -> dict:
        """
        This method processes each block of text,
        applies styles, and returns the rendered content as HTML.

        :returns: A dictionary with IDs (keys) referencing their
        rendered HTML content (values).
        :rtype: dict
        """

        result: dict = {}

        for block_id, lines in cls.blocks.items():
            # We join the lines with a space to form a continuous paragraph.
            full_text = "\n".join(lines)
            rendered = cls._apply_styles(full_text)
            result[block_id] = rendered

        return result

def convert_FLUML_to_HTML(fluml_content: str) -> Dict[str, str]:
    """
    Processes a block of content written in the FLUML markup language,
    extracts all static text directives, and converts them into HTML
    with inline styles for use in PySide6/Qt widgets that
    support Rich Text.

    This function serves as the main interface for loading the application's
    internationalization (i18n) content.

    The process is carried out in two phases:
    1. Parsing: :py:meth:`~FlumlParser.parse` is used to identify
    the '..id: content' directives and group multiline text.
    2. Rendering: :py:meth:`~FlumlParser.render_html` is used to
    join the lines of each block (with a newline character '\\n' or a space),
    and convert the custom markup syntax (e.g., ** bold, * italics)
    to the corresponding HTML/CSS tags.

    :param fluml_content: The full text string read from a ``.fluml`` file
                        (e.g., messages.fluml) within the active
                        language directory.
    :type fluml_content: str

    :returns: A dictionary (catalog) where the keys are the text IDs
            (e.g., 'welcome-title') and the values are the text strings
            already rendered in HTML format.
    :rtype: Dict[str, str]
    """
    FlumlParser.parse(fluml_content)
    return FlumlParser.render_html()