from fluvel import AppWindow, er


class MainWindow(AppWindow):
    def init_ui(self):
        """Display the `components` in the Main Window."""

        self.configure(size=(920, 605))

        # configure menu options
        # self.build_menu_bar()

    def build_menu_bar(self):
        change_theme = self.app.change_theme
        change_language = self.app.change_language

        self.menu_bar.configure(
            controls={
                # -------------- FILE --------------------
                "quit": {"triggered": self.close, "Shortcut": "Ctrl+Q"},
                # -------------- SETTINGS ----------------
                "bootstrap_theme": {"triggered": lambda: change_theme("bootstrap")},
                "modern_dark_theme": {"triggered": er.set_lang("modern-dark")},
                "es_language": {"triggered": er.set_lang("es")},
                "en_language": {"triggered": er.set_lang("en")},
            }
        )
