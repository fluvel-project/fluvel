import fluvel as fl
from fluvel.composer import Component
from fluvel.tools import icon


@Component("FIconButton")
def CloseIcon(color: str = "black"):
    return {
        "icon": icon("close", color=color),
        "style": "b[none] icon-s[18px]",
        "alignment": "right",
        "on_click": fl.Page.main_window.close,
    }
