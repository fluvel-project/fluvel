# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import difflib
import re
from functools import lru_cache

# Fluvel
from fluvel.user.UserSettings import Settings


class QSSProcessor:
    """
    QSS style preprocessing engine for Fluvel Framework.

    This class is responsible for translating Fluvel's simplified and utilitarian syntax
    (e.g., ``bg[red]``, ``h::fs[14px]``) into native QSS stylesheets that are valid for Qt.

    It implements a system of tokens and regular expressions to parse standard properties,
    interactive pseudo-states (hover, pressed, etc.), and generate complex gradients.

    .. note::
        This class is heavily optimized using :func:`functools.lru_cache` on the
        parsing methods to guarantee O(1) time complexity for repetitive style patterns,
        significantly reducing startup and render latency in large UI applications.
    """

    BASE_PATTERN = re.compile(
        r"""
        (?:^|\s)                      # Start of string or space (Non-capturing)
        (?:                           # Start of Optional Interactive Prefix (Non-capturing)
            (?P<state>[a-z])          # ‘state’ group: Captures ‘h’, ‘p’, ‘d’, etc.
            ::                        # Literal ‘::’
        )?                            # End of Optional Interactive Prefix
        (?P<token>[a-z-]+)            # Group ‘token’: Captures ‘bg’, ‘f-size’, etc.                         
        \[(?P<value>[^\]]*)\]         # Group ‘value’: Captures the content.
        """,
        re.VERBOSE,
    )

    T_COMMON = "{class_name}#{id} {{\n\t{properties}\n}}\n"
    T_HOVER = "{class_name}#{id}:hover {{\n\t{properties}\n}}\n"
    T_PRESSED = "{class_name}#{id}:pressed {{\n\t{properties}\n}}\n"
    T_DIS = "{class_name}#{id}:disabled {{\n\t{properties}\n}}\n"
    T_CHECK = "{class_name}#{id}:checked {{\n\t{properties}\n}}\n"

    TEMPLATE_MAP = {"common": T_COMMON, "h": T_HOVER, "p": T_PRESSED, "d": T_DIS, "c": T_CHECK}

    STYLE_TOKENS: dict[str, str] = {
        # --- BACKGROUNDS ---
        "bg": "background-color: {value};",
        "bg-img": 'background-image: url("{value}");',
        "bg-repeat": "background-repeat: {value};",
        "bg-position": "background-position: {value};",
        "bg-origin": "background-origin: {value};",
        "bg-clip": "background-clip: {value};",
        # --- GRADIENTS ---
        "bg-lgrad-v": "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, {value});",
        "bg-lgrad-rv": "background-color: qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0, {value});",
        "bg-lgrad-h": "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, {value});",
        "bg-lgrad-rh": "background-color: qlineargradient(x1: 1, y1: 0, x2: 0, y2: 0, {value});",
        "bg-rgrad": "background-color: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5, {value});",
        # --- SELECTION ---
        "sel-bg": "selection-background-color: {value};",
        "sel-fg": "selection-color: {value};",
        # --- IMAGES & ICONS ---
        "b-img": 'border-image: url("{value}") 0 0 0 0 stretch stretch;',
        "img": 'image: url("{value}");',
        "img-pos": "image-position: {value};",
        # --- BORDERS ---
        "b": "border: {value};",
        "b-color": "border-color: {value};",
        "b-style": "border-style: {value};",
        "b-width": "border-width: {value};",
        "b-l": "border-left: {value};",
        "b-t": "border-top: {value};",
        "b-r": "border-right: {value};",
        "b-b": "border-bottom: {value};",
        "br": "border-radius: {value};",
        "br-t": "border-top-left-radius: {value};\n\tborder-top-right-radius: {value};",
        "br-b": "border-bottom-left-radius: {value};\n\tborder-bottom-right-radius: {value};",
        "br-l": "border-top-left-radius: {value};\n\tborder-bottom-left-radius: {value};",
        "br-r": "border-top-right-radius: {value};\n\tborder-bottom-right-radius: {value};",
        "br-tl": "border-top-left-radius: {value};",
        "br-tr": "border-top-right-radius: {value};",
        "br-bl": "border-bottom-left-radius: {value};",
        "br-br": "border-bottom-right-radius: {value};",
        # --- OUTLINE ---
        "o": "outline: {value};",
        "o-rad": "outline-radius: {value};",
        "o-style": "outline-style: {value};",
        "o-off": "outline-offset: {value};",
        # --- FONT/TEXT ---
        "fs": "font-size: {value};",
        "fg": "color: {value};",
        "f-weight": "font-weight: {value};",
        "f-align": "text-align: {value};",
        "f-family": "font-family: {value};",
        "f-style": "font-style: {value};",
        "f-decoration": "text-decoration: {value};",
        # --- LAYOUT/SPACING ---
        "m": "margin: {value};",
        "m-t": "margin-top: {value};",
        "m-b": "margin-bottom: {value};",
        "m-l": "margin-left: {value};",
        "m-r": "margin-right: {value};",
        "m-tl": "margin-top: {value}; margin-left: {value}",
        "m-tr": "margin-top: {value}; margin-right: {value}",
        "m-bl": "margin-bottom: {value}; margin-left: {value}",
        "m-br": "margin-bottom: {value}; margin-right: {value}",
        "m-v": "margin-top: {value};\n\tmargin-bottom: {value};",
        "m-h": "margin-left: {value};\n\tmargin-right: {value};",
        "p": "padding: {value};",
        "p-t": "padding-top: {value};",
        "p-b": "padding-bottom: {value};",
        "p-l": "padding-left: {value};",
        "p-r": "padding-right: {value};",
        "p-tl": "padding-top: {value}; padding-left: {value}",
        "p-tr": "padding-top: {value}; padding-right: {value}",
        "p-bl": "padding-bottom: {value}; padding-left: {value}",
        "p-br": "padding-bottom: {value}; padding-right: {value}",
        "p-v": "padding-top: {value};\n\tpadding-bottom: {value};",
        "p-h": "padding-left: {value};\n\tpadding-right: {value};",
        # --- SIZING ---
        "w": "width: {value};",
        "h": "height: {value};",
        "min-w": "min-width: {value};",
        "min-h": "min-height: {value};",
        "max-w": "max-width: {value};",
        "max-h": "max-height: {value};",
        # --- SUBCONTROLS ---
        "sc-org": "subcontrol-origin: {value};",
        "sc-pos": "subcontrol-position: {value};",
        # --- QT PROPERTIES ---
        "icon-s": "qproperty-iconSize: {value};"
    }

    @classmethod
    def lint(cls, styles: str, class_name: str = "Unknown") -> bool:
        """
        Syntax validator for Fluvel (Debug Mode).
        Analyzes the style string for tokens that don't exist in STYLE_TOKENS.
        If it finds errors, it prints warnings to the console with suggestions.

        :param styles: The style string to validate.
        :type styles: str
        :param class_name: Name of the widget to easily identify the error.
        :type class_name: str
        :return: True if the styles are valid, False if there were warnings.
        :rtype: bool
        """

        matches = cls.BASE_PATTERN.findall(styles)
        if not matches:
            return True

        valid_tokens = set(cls.STYLE_TOKENS.keys())
        has_errors = False

        # We filter unknown tokens
        for _state, token, _value in matches:
            if token not in valid_tokens:
                has_errors = True
                msg = f"Fluvel [SyntaxError] on '{class_name}': The token '{token}' does not exist."

                
                # We search for the closest matching token using difflib
                # and add it as a suggestion
                suggestions = difflib.get_close_matches(token, valid_tokens, n=1, cutoff=0.6)
                if suggestions:
                    msg += f" Did you mean '{suggestions[0]}'?"

                # TODO: Use print until you have
                # a logging configuration
                print(msg)

        return not has_errors

    @classmethod
    def process(cls, styles: str, class_name: str, widget_id: str) -> str:
        """
        Processes a Fluvel style string and generates the final QSS code.

        This method parses the input string for normal and interactive style patterns,
        resolves tokens using :attr:`STYLE_TOKENS`, and constructs the complete CSS style block
        applied to the specific widget ID.

        :param styles: The style string in Fluvel syntax (e.g., ``"bg[#333] :h:bg[#555]"``).
        :type styles: str
        :param class_name: The name of the widget class (e.g., ``"QPushButton"``).
        :type class_name: str
        :param widget_id: The unique ID of the object (e.g., ``"12345678"``) used as the ID selector in QSS.
        :type widget_id: str
        :return: The complete, formatted QSS code ready for use in ``setStyleSheet``.
        :rtype: str
        """

        # We use difflib to validate the syntax before
        # processing (validation is only performed in production)
        if not Settings.get("fluvel.production", False):
            cls.lint(styles, class_name)

        parsed_blocks = cls._parse_styles(styles)

        if not parsed_blocks:
            return ""

        final_parts = []

        # Micro-optimization: Bring the .format method local
        # Avoid attribute lookups in the loop
        get_template = cls.TEMPLATE_MAP.get

        for state, properties_block in parsed_blocks:
            template = get_template(state)
            if template:
                final_parts.append(
                    template.format(
                        class_name=class_name, id=widget_id, properties=properties_block
                    )
                )

        return "".join(final_parts)

    @classmethod
    @lru_cache(maxsize=2048)
    def _parse_styles(cls, styles: str) -> list[tuple[str, str]]:
        """
        Performs the heavy lifting of Regex matching, token resolution, and property grouping.

        This method is decorated with :func:`functools.lru_cache` to ensure that
        the expensive parsing process is executed only once per unique style string.

        The properties for each state are pre-joined to minimize string concatenation
        work in the main ``process`` method.

        :param styles: The raw style string from the user.
        :type styles: str
        :returns: A list of tuples, where each tuple is (state, properties_block).
                  Example: ``[('common', 'color: #fff;\\n\\tfont-size: 12px;'), ('h', 'background-color: #333;')]``
        :rtype: List[Tuple[str, str]]
        """

        matches = cls.BASE_PATTERN.findall(styles)

        if not matches:
            return []

        # Usamos un dict temporal para agrupar
        temp_groups = {}

        tokens_map = cls.STYLE_TOKENS

        for state, token, value in matches:
            state = state if state else "common"

            token_template = tokens_map.get(token)
            if not token_template:
                continue

            # Gradient processing only if necessary
            if token.startswith(("bg-lgrad", "bg-rgrad")):
                value = cls._generate_stops(value)

            qss_line = token_template.format(value=value)

            if state not in temp_groups:
                temp_groups[state] = []

            temp_groups[state].append(qss_line)
        
        # We convert to an immutable structure (List of tuples)
        # and pre-join the properties with \n\t to save work in the rendering step
        result = []
        for state, lines in temp_groups.items():
            result.append((state, "\n\t".join(lines)))

        return result

    @staticmethod
    @lru_cache(maxsize=128)
    def _generate_stops(colors: str) -> str:
        """
        Generates the QSS 'stop' string for a gradient.

        This method is cached to avoid recalculating the floating-point stop positions
        for repeated color sequences (e.g., using the same gradient on many widgets).

        :param colors: String with color codes separated by ``-`` (e.g., ``"#f00-#0f0-#00f"``).
        :type colors: str
        :returns: Formatted string of stops for QSS (e.g., ``"stop: 0.00 #f00, stop: 0.50 #0f0, stop: 1.00 #00f"``).
        :rtype: str
        """

        colors_list = colors.split("-")
        count = len(colors_list)

        if count <= 1:
            if count == 0:
                return ""
            c = colors_list[0]
            return f"stop: 0 {c}, stop: 1 {c}"

        step = 1.0 / (count - 1)

        return ", ".join([f"stop: {i * step:.3f} {c}" for i, c in enumerate(colors_list)])
