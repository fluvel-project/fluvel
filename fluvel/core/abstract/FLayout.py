# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, TypedDict, TypeVar, Unpack, overload

# PySide6
from PySide6.QtWidgets import QLayout, QWidget

# Fluvel Composer (for typing)
from fluvel.core.abstract.FLayoutAPI import FLayoutAPI
from fluvel.core.enums import Alignment, AlignmentTypes, SizeConstraint, SizeConstraintTypes

# Flvuel Core
from fluvel.core.tools import configure_process

TWidget = TypeVar("TWidget", bound=QWidget)
TComponent = TypeVar("TComponent", bound=Callable)

if TYPE_CHECKING:
    from fluvel.composer.Prefab import Canvas

class FLayoutKwargs(TypedDict, total=False):
    """
    Keyword arguments for configuring the layout distribution.
    """

    alignment: AlignmentTypes
    spacing: int
    margins: int | tuple[int, int, int, int]
    size_constraint: SizeConstraintTypes

class FLayout(FLayoutAPI):
    """
    A class specific to `Fluvel` that provides methods for adding QWidgets to QLayouts.
    """

    _MAPPING_METHODS = {
        "alignment": "setAlignment",
        "spacing": "setSpacing",
        "margins": "setContentsMargins",
        "size_constraint": "setSizeConstraint",
    }

    def adjust(self, **kwargs: Unpack[FLayoutKwargs]) -> None:
        """
        Adjusts the main layout settings and size properties of its container.

        This method provides a single declarative interface for configuring various
        layout attributes and dimensions of the parent :class:`~fluvel.components.widgets.FContainer`
        in a single call.

        :param alignment: Alignment of elements within the layout.
                          Uses the text strings defined in :class:`~fluvel.core.enums.alignment.AlignmentTypes`.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :param spacing: Space in pixels between layout elements.
        :type spacing: int

        :param margins: Margins around the layout, in the order: (left, top, right, bottom).
        :type margins: int | tuple[int, int, int, int]

        :param size_constraint: Size constraint for the layout. Use one of the
                                constants predefined in :class:`~PySide6.QtWidgets.QLayout`.
        :type size_constraint: :class:`~fluvel.core.enums.size_constraint.SizeConstraintTypes`
        """

        if alignment := kwargs.get("alignment"):
            kwargs["alignment"] = Alignment.get(alignment)

        if size_constraint := kwargs.get("size_constraint"):
            kwargs["size_constraint"] = SizeConstraint.get(size_constraint)

        if isinstance(margin := kwargs.get("margins"), int):
            kwargs["margins"] = (margin, margin, margin, margin)

        configure_process(self, self._MAPPING_METHODS, **kwargs)

    def _create_widget(self, widget_class: type[TWidget], **kwargs) -> TWidget:
        """
        Internal utility method to instantiate a widget and immediately add it to the layout.

        :param widget_class: The Fluvel widget class to instantiate (e.g., FLabel).
        :type widget_class: Type[TWidget]
        :param kwargs: Keyword arguments for the widget constructor.
        :returns: The instance of the created widget.
        :rtype: TWidget
        """

        stretch = kwargs.pop("stretch", 0)
        alignment = kwargs.pop("alignment", Alignment.NONE)

        widget: TWidget = widget_class(**kwargs)
        self.add(widget, alignment, stretch)

        return widget

    # Usamos TComponent para transferir la firma de la función.
    def use(self, factory: TComponent, returns: bool = False) -> TComponent:
        """
        Registers a component or prefab factory as a local layout method.

        This method wraps a factory function (decorated with @Component or @Prefab)
        to automate its instantiation and addition to the current layout while
        preserving the original signature for IDE **autocompletion**.

        :param factory: The factory function to integrate.
        :type factory: TComponent (Callable)
        :param returns: If True, the wrapper returns the created widget instance.
        :type returns: bool
        :returns: A wrapper function with the same signature as the original factory.
        :rtype: TComponent (Callable)

        .. note::
            This is the idiomatic way in Fluvel to extend a Layout's capabilities
            locally without losing type safety.

        Usage
        -----
        .. code-block:: python

            with self.Vertical() as v:
                # Works with @Component
                v.Primary = v.use(PrimaryButton)
                v.Primary(text="Click me")

                # Also works with @Prefab
                v.Card = v.use(UserCard)
                v.Card(name="Robotid", role="BOT")
        """

        @functools.wraps(factory)
        def add_to_layout(*args, **kwargs) -> QWidget | None:
            stretch = kwargs.get("stretch", 0)
            alignment = kwargs.get("alignment", Alignment.NONE)

            item = factory(*args, **kwargs)
            self.add(item, alignment, stretch)

            return item if returns else None

        return add_to_layout

    def Gap(self, size: int) -> None:
        """
        Adds a fixed, non-stretchable space (gap) to the current layout.

        This method is used to create a precise separation between widgets
        without affecting how the layout redistributes remaining space.

        :param size: The fixed size of the gap in pixels.
        :type size: int

        Example
        -------
        .. code-block:: python
            with self.Vertical() as v:
                v.Label(text="Top Section")
                v.Gap(20)  # Fixed 20px breathing room
                v.Label(text="Bottom Section")
        """
        self.addSpacing(size)

    def Stretch(self, factor: int = 1) -> None:
        """
        Adds an elastic, stretchable space to the current layout.

        A Stretch acts like a spring that pushes widgets to occupy all
        available empty space. If multiple stretches are used, they will
        share the space according to their stretch factor.

        :param factor: The relative weight of this stretch compared to others.
        :type factor: int

        Example
        -------
        .. code-block:: python
            with self.Horizontal() as h:
                h.Button(text="Left")
                h.Stretch()  # Pushes the next button to the far right
                h.Button(text="Right")
        """
        self.addStretch(factor)

    @overload
    def add(self, canvas: 'Canvas', stretch: int = 0, alignment: AlignmentTypes = None) -> None:
        """
        Adds a Complex Component (@Prefab) to the current layout.

        This method integrates pre-fabricated components (functions decorated
        with `@Prefab`) into a Fluvel layout, extracting the component's
        main container and appending it to the parent widget hierarchy.

        :param canvas: The pre-fabricated component.
        :type canvas: :class:`~fluvel.core.abstract.AbstractPage.Page`

        :param alignment: Alignment of the prefab within the layout cell.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes` | None

        :param stretch: The **stretch factor** to assign to the widget. This value
                    determines how much extra space the widget receives relative
                    to other widgets in the same layout row or column.
                    A value of 0 means the widget will not receive extra space
                    when the window is resized. A higher number (e.g., 1, 2, 3)
                    means the widget will grow proportionally more.
        :type stretch: int
        """
        ...

    @overload
    def add(self, widget: QWidget, stretch: int = 0, alignment: AlignmentTypes = None) -> None:
        """
        Adds an existing widget to the layout, optionally applying an alignment.

        This is the low-level method used internally by all addition methods
        (e.g., :meth:`~FluvelLayout.Label`, :meth:`~FluvelLayout.Prefab`).

        :param widget: The widget to add to the layout.
        :type widget: :class:`~PySide6.QtWidgets.QWidget`

        :param alignment: Alignment of the widget within the layout cell.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes` | None

        :param stretch: The **stretch factor** to assign to the widget. This value
                        determines how much extra space the widget receives relative
                        to other widgets in the same layout row or column.
                        A value of 0 means the widget will not receive extra space
                        when the window is resized. A higher number (e.g., 1, 2, 3)
                        means the widget will grow proportionally more.
        :type stretch: int
        """
        ...

    def add(self, item: QWidget, alignment: AlignmentTypes = None, stretch: int = 0):
        self.addWidget(item, stretch, Alignment.get(alignment))
