# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from PySide6.QtWidgets import QLayout

# Fluvel
from fluvel.core.exceptions.exceptions import InvalidLayoutOperationError
from fluvel.components.widgets.containers import (
    FContainer,
    FGroupBox,
    FImageContainer,
    FScrollArea,
)

_L_CACHE = {}

def _get_layout(layout: str):
    """Gets the layout class and caches the import."""
    try:
        return _L_CACHE[layout]
    except KeyError:
        from fluvel.components.layouts import GridLayout, HBoxLayout, VBoxLayout
        _L_CACHE['grid'] = GridLayout
        _L_CACHE['horizontal'] = HBoxLayout
        _L_CACHE['vertical'] = VBoxLayout
        return _L_CACHE[layout]

class CMLayoutBuilder:
    __slots__ = ["layout"]

    def __init__(self,container, type_layout, **kwargs):
        stretch = kwargs.pop("stretch", 0)
        alignment = kwargs.pop("alignment", "none")

        # The container is a QLayout,
        # which means that an FContainer must be created and added
        # to the current QLayout (container parameter)
        # for it to function as a new container for the requested QLayout.
        if isinstance(container, QLayout):

            if kwargs:
                parent_widget = FContainer(**kwargs)
                
                # Add the widget to the layout
                container.add(parent_widget, alignment, stretch)

                # Finally, the requested layout is instantiated
                # as a child of the newly created FContainer.
                self.layout = type_layout(parent_widget)
            else:
                self.layout = type_layout()
                container.addLayout(self.layout, stretch)

        # The container is a FContainer
        else:
            self.layout = type_layout(container)
            container.configure(**kwargs)

    def __enter__(self):
        return self.layout

    def __exit__(self, *_):
        return False


class LayoutBuilder:
    """
    A Mixin that provides the declarative API ('Vertical','Horizontal', etc.)
    for building layouts using LayoutBuilder.
    """

    def _build_container_layout(self, container_type, **kwargs):

        alignment = kwargs.pop("alignment", "none")
        stretch = kwargs.pop("stretch", 0)

        container = container_type(**kwargs)
        layout_class = _get_layout(kwargs.pop("layout", "vertical"))

        try:
            self.add(container, alignment, stretch)
        except AttributeError:
            raise InvalidLayoutOperationError(
                f"You cannot insert a special container like <{type(container).__name__}> "
                "inside a Canvas object. Consider defining a main layout first."
            )
        
        return CMLayoutBuilder(container, layout_class)

    def Vertical(self, **kwargs):
        return CMLayoutBuilder(self, _get_layout("vertical"), **kwargs)

    def Horizontal(self, **kwargs):
        return CMLayoutBuilder(self, _get_layout("horizontal"), **kwargs)
    
    def Grid(self, **kwargs):
        return CMLayoutBuilder(self, _get_layout("grid"), **kwargs)

    def ImageArea(self, **kwargs):
        return self._build_container_layout(FImageContainer, **kwargs)

    def Group(self, **kwargs):
        return self._build_container_layout(FGroupBox, **kwargs)

    def Scroll(self, **kwargs):

        alignment = kwargs.pop("alignment", None)
        stretch = kwargs.pop("stretch", 0)
        drag_window = kwargs.pop("drag_window", False)

        layout_class = _get_layout(kwargs.pop("layout", "vertical"))

        scroll = FScrollArea(**kwargs)
        container = FContainer(drag_window=drag_window)

        scroll.setWidget(container)
        self.add(scroll, alignment=alignment, stretch=stretch)

        return CMLayoutBuilder(container=container, type_layout=layout_class)