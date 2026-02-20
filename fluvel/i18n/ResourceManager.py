# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from functools import partial
from typing import TYPE_CHECKING
from collections.abc import Callable

# PySide6
from PySide6.QtCore import QObject, Signal

# Fluvel Utils
from fluvel.core.tools import load_style_sheet, load_theme
from fluvel.i18n.data_structures import I18nSafeDict

# Fluvel I18n
from fluvel.i18n.I18nLoader import I18nLoader
from fluvel.i18n.I18nProvider import I18nProvider
from fluvel.i18n.I18nTextVar import I18nMenuTextVar, I18nTextVar
from fluvel.user.UserSettings import Settings
from fluvel.utils.paths import PROD_THEMES_DIR, THEMES_DIR

if TYPE_CHECKING:
    from fluvel.core.App import App


class LanguageEmitter(QObject):
    languageChanged: Signal = Signal()


class ResourceManager:
    app: "App"

    def __init__(self):
        self.lang_emitter = LanguageEmitter()

    def _load_static(self, lang: str):
        """
        Entry point for initializing or updating the application's content.

        Determines the execution mode (development/production) to define which file types
        (fluml/json) and folders (CONTENT_DIR/PROD_CONTENT_DIR) will be used.

        :param lang: The language code to load.
        :type lang: str
        """

        raw = I18nLoader.load(lang, Settings.get("fluvel.production", False))

        if raw:
            I18nProvider.save_content(raw)
            self.lang_emitter.languageChanged.emit()

    @staticmethod
    def _load_theme() -> str:
        if theme := Settings.get("ui.theme"):
            if Settings.get("fluvel.production", False):
                return load_style_sheet(PROD_THEMES_DIR / f"{theme}.qss")

            return load_theme(THEMES_DIR, theme)
        return ""

    def __call__(self, id: str, **placeholders) -> I18nTextVar | str:
        if id in I18nProvider.texts:
            text_var = I18nTextVar(id, I18nSafeDict(placeholders))
            self.lang_emitter.languageChanged.connect(text_var.refresh)
            return text_var

        return ""

    def __getitem__(self, id: str) -> I18nMenuTextVar | str:
        if id in I18nProvider.menus:
            menu_text_var = I18nMenuTextVar(id)
            self.lang_emitter.languageChanged.connect(menu_text_var.refresh)
            return menu_text_var

        return ""

    def set_lang(self, lang: str) -> None:
        self.app.change_language(lang)
    def set_theme(self, theme: str) -> None:
        self.app.change_theme(theme)

    def as_set_lang(self, lang: str) -> Callable[[], None]:
        return partial(self.set_lang, lang)

    def as_set_theme(self, theme: str):
        return partial(self.set_theme, theme)


er = ResourceManager()
