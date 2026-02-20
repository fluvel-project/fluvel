# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import html
import re
from typing import ClassVar


class FlumlParser:
    # Pattern to detect the start of a block: ".. id: fluml-content"
    BLOCK_PATTERN = re.compile(r"^\s*\.\.\s*(?P<id>[^:]+):\s*(?P<content>.*)$")

    # Compiled re.sub Patterns
    STYLE_RULES: ClassVar[list[tuple[str, str]]] = [
        # COLOR & OPACITY
        # Syntax: [ color | content ] -> [red|Alert] or [rgba(0,0,0,0.5)|Ghost]
        (r"\[\s*([#a-zA-Z0-9(),\.\s%]+)\s*\|\s*([^\]]+)\s*\]", r"<span style='color:\1;'>\2</span>"),

        # LINKS: { content | href }
        (r"(?<!\\)\{\s*([^\s|{}](?:[^|{}]*[^\s|{}])?)\s*\|\s*([^\s|{}]+)\s*\}", r"<a href='\2'>\1</a>"),

        # --- TYPOGRAPHY ---
        # Bold + Italic: ***content***
        (r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>"),
        # Bold: **content**
        (r"\*\*(.+?)\*\*", r"<b>\1</b>"),
        # Italic: *content*
        (r"\*(.+?)\*", r"<i>\1</i>"),
        
        # --- DECORATION ---
        # Underline: __content__
        (r"__(.+?)__", r"<u>\1</u>"),
        # Strike: --content--
        (r"(?<!-)--([^\s-].*?[^\s-])--(?!-)", r"<s>\1</s>"),
        # Super: ^^content^^
        (r"\^\^(.+?)\^\^", r"<sup>\1</sup>"),
        # Sub: ~~content~
        (r"~~(.+?)~~", r"<sub>\1</sub>"),

        # --- UTILS ---
        # Line break
        (r"\\n", r"<br>"),

        # Escapes
        (r"\\\{", "{"),
        (r"\\\}", "}"),
        (r"\\\[", "["),
        (r"\\\]", "]"),
    ]

    # Pre-compile patterns once
    COMPILED_STYLES = [(re.compile(p), r) for p, r in STYLE_RULES]

    @classmethod
    def _apply_styles(cls, text: str) -> str:
        text = html.escape(text, quote=False)
        for pattern, replacement in cls.COMPILED_STYLES:
            text = pattern.sub(replacement, text)
        return text

    @classmethod
    def parse(cls, text: str) -> dict[str, str]:
        blocks: dict[str, list[str]] = {}
        current_id: str = None

        for line in text.splitlines():
            # Ignore blank spaces and comments
            if not (clean_line := line.strip()) or clean_line.startswith("#"):
                continue

            if match := cls.BLOCK_PATTERN.match(line):
                current_id = match.group("id").strip()
                content = match.group("content").strip()
                # We created a list to accumulate lines of this ID
                blocks[current_id] = [content] if content else []

            elif current_id:
                # If it's not an ID match, it's text that belongs to the current ID
                blocks[current_id].append(clean_line)

        # Build and return the ID: html_content
        return {block_id: cls._apply_styles(" ".join(lines)) for block_id, lines in blocks.items()}


def convert_FLUML_to_HTML(fluml_content: str) -> dict[str, str]:
    """
    Processes a block of content written in the FLUML markup language,
    extracts all static text directives, and converts them into HTML
    with inline styles for use in PySide6/Qt widgets that
    support Rich Text.

    This function serves as the main interface for loading the application's
    internationalization (i18n) content.

    :param fluml_content: The full text string read from a ``.fluml`` file
                        (e.g., messages.fluml) within the active
                        language directory.
    :type fluml_content: str

    :returns: A dictionary (catalog) where the keys are the text IDs
            (e.g., 'win.home.title') and the values are the text strings
            already rendered in HTML format.
    :rtype: Dict[str, str]
    """
    return FlumlParser.parse(fluml_content)
