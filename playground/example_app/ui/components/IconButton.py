import qtawesome as qta

from fluvel.composer import Component


@Component("FButton")
def IconButton(
    icon_type: str = "s",
    icon_name: str = "times",
    color: str = "gray",
    on_click: callable = None,
):
    params: dict = {
        "style": "b[1px solid gray] rounded-2xl",
        "size": (45, 47),
        "icon_size": 19,
        "icon": qta.icon(
            f"fa5{icon_type}.{icon_name}", color=color, options=[{"scale_factor": 0.9}]
        ),
    }

    if on_click:
        params["on_click"] = on_click

    return params
