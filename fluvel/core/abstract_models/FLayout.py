import functools
from typing import Unpack, TypedDict, TypeVar, Callable, Tuple, Type

# Flvuel Core
from fluvel.core.tools import configure_process
from fluvel.core.enums.alignment import AlignmentTypes, Alignment
from fluvel.core.abstract_models.FLayoutAPI import FLayoutAPI

# PySide6
from PySide6.QtWidgets import QWidget, QLayout

TWidget = TypeVar("TWidget", bound=QWidget)
TFactory = TypeVar("TFactory", bound=Callable)

class FLayoutKwargs(TypedDict, total=False):
    """
    Keyword arguments for configuring the layout distribution.
    """

    alignment       : AlignmentTypes
    spacing         : int
    margins         : Tuple[int, int, int, int]
    size_constraint : QLayout.SizeConstraint

    # container size management
    min_size        : Tuple[int, int]
    max_size        : Tuple[int, int]
    fixed_size      : Tuple[int, int]
    fixed_width     : int
    fixed_height    : int
    min_width       : int
    min_height      : int
    max_width       : int
    max_height      : int
    
class FLayout(FLayoutAPI):
    """
    A class specific to `Fluvel` that provides methods for adding QWidgets to QLayouts.
    """

    # Size Contraints
    DEFAULT         = QLayout.SizeConstraint.SetDefaultConstraint
    FIXED           = QLayout.SizeConstraint.SetFixedSize
    MINIMUM         = QLayout.SizeConstraint.SetMinimumSize
    MAXIMUM         = QLayout.SizeConstraint.SetMaximumSize
    WITHOUT         = QLayout.SizeConstraint.SetNoConstraint
    MIN_AND_MAX     = QLayout.SizeConstraint.SetMinAndMaxSize

    _MAPPING_METHODS = {
        "alignment": "setAlignment",
        "spacing": "setSpacing",
        "margins": "setContentsMargins",
        "size_constraint": "setSizeConstraint",
    }

    _CONTAINER_MAPPING_METHODS = {
        "fixed_size": "setFixedSize",
        "fixed_width": "setFixedWidth",
        "fixed_height": "setFixedHeight",
        "min_width": "setMinimumWidth",
        "min_height": "setMinimumHeight",
        "max_width": "setMaximumWidth",
        "max_height": "setMaximumHeight",
        "min_size": "setMinimumSize",
        "max_size": "setMaximumSize",
    }

    def adjust(self, **kwargs: Unpack[FLayoutKwargs]) -> None:
        """
        Adjusts the main layout settings and size properties of its container.

        This method provides a single declarative interface for configuring various 
        layout attributes and dimensions of the parent :class:`~fluvel.components.widgets.FContainer` 
        in a single call.

        :param alignment: **(Layout)** Alignment of elements within the layout. 
                          Uses the text strings defined in :class:`~fluvel.core.enums.alignment.AlignmentTypes`.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`
        :param spacing: **(Layout)** Space in pixels between layout elements.
        :type spacing: int
        :param margins: **(Layout)** Margins around the layout, in the order: (left, top, right, bottom).
        :type margins: tuple[int, int, int, int]
        :param size_constraint: **(Layout)** Size constraint for the layout. Use one of the 
                                constants predefined in :class:`~PySide6.QtWidgets.QLayout`.
        :type size_constraint: :class:`~PySide6.QtWidgets.QLayout.SizeConstraint`

        :param min_size: **(Container)** Sets the minimum width and height of the container widget (width, height).
        :type min_size: tuple[int, int]
        :param max_size: **(Container)** Sets the maximum width and height of the container widget (width, height).
        :type max_size: tuple[int, int]
        :param fixed_size: **(Container)** Sets the fixed width and height of the container widget (width, height).
        :type fixed_size: tuple[int, int]
        :param fixed_width: **(Container)** Sets the fixed width of the container widget.
        :type fixed_width: int
        :param fixed_height: **(Container)** Sets the fixed height of the container widget.
        :type fixed_height: int
        :param min_width: **(Container)** Sets the minimum width of the container widget.
        :type min_width: int
        :param min_height: **(Container)** Sets the minimum height of the container widget.
        :type min_height: int
        :param max_width: **(Container)** Sets the maximum width of the container widget.
        :type max_width: int
        :param max_height: **(Container)** Sets the maximum height of the container widget.
        :type max_height: int

        .. note::
            Properties marked as **(Container)** are applied directly to the parent widget 
            :class:`~fluvel.components.widgets.FContainer.FContainer` (`self.parentWidget()`), while 
            those marked as **(Layout)** are applied to the layout object.
        """

        if alignment:=kwargs.get("alignment"):
            kwargs["alignment"] = Alignment.get(alignment)

        configure_process(self, self._MAPPING_METHODS, **kwargs)
        configure_process(self.parentWidget(), self._CONTAINER_MAPPING_METHODS, **kwargs)
    
    def add_widget(self, widget: QWidget, alignment: AlignmentTypes = None, stretch: int = 0) -> None:
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

        if alignment:
            self.addWidget(widget, alignment=Alignment.get(alignment), stretch=stretch)
        else:
            self.addWidget(widget, stretch=stretch)

    def _create_widget(self, widget_class: Type[TWidget], **kwargs) -> TWidget:
        """
        Internal utility method to instantiate a widget and immediately add it to the layout.

        :param widget_class: The Fluvel widget class to instantiate (e.g., FLabel).
        :type widget_class: Type[TWidget]
        :param kwargs: Keyword arguments for the widget constructor.
        :returns: The instance of the created widget.
        :rtype: TWidget
        """

        stretch = kwargs.pop("stretch", 0)
        alignment = kwargs.pop("alignment", None)

        widget: TWidget = widget_class(**kwargs)
        
        self.add_widget(widget, alignment, stretch)

        return widget
    
    # --------------------------------- API ----------------------------------------------

    # Usamos TFactory para transferir la firma de la función.
    def from_factory(self, factory_widget: TFactory, returns: bool = False) -> TFactory:
        """
        Converts a component factory function into a layout method.

        This method takes a factory function created with :meth:`~fluvel.composer.Factory.Factory.compose` 
        and returns a *wrapper* function that:

        1. Preserves the original signature of the factory function for IDE **autocompletion**.
        2. Creates the :class:`~PySide6.QtWidgets.QWidget` and automatically adds it to the layout.

        This allows custom components to be added to the layout with concise syntax (Builder Pattern).

        :param factory_widget: The widget factory function (already decorated by :meth:`~fluvel.composer.Factory.Factory.compose`).
        :type factory_widget: TFactory (Callable)
        :param returns: If :obj:`True`, the returned function will return the created :class:`~PySide6.QtWidgets.QWidget`. If :obj:`False` (default), it returns :obj:`None`.
        :type returns: bool
        :returns: A *wrapper* function with the same argument signature as ``factory_widget``, but which handles adding it to the layout.
        :rtype: TFactory (Callable)

        .. note::
            Using `TFactory` with :func:`~functools.wraps` is crucial for preserving argument information
            and code *tips* in environments such as VS Code.

        Usage
        -----
        .. code-block:: python

            # 1. Factory definition (e.g. PrimaryButton)
            @Factory.compose(target="FButton")
            def PrimaryButton(text: str, route: str):
                return {"text": text, "style": "primary font-bold"}

            # 2. Use in the View
            with self.Vertical() as v:
                # Create a new method “v.PrimaryButton” with the signature (text, route)
                v.PrimaryButton = v.from_factory(PrimaryButton) 

                # When this new method is called, the button is automatically created and added:
                v.PrimaryButton("Enter", route="login") 
        """
        
        @functools.wraps(factory_widget)
        def add_to_layout(*args, **kwargs) -> QWidget | None:

            widget = factory_widget(*args, **kwargs)

            self.add_widget(widget,kwargs.get("alignment"), kwargs.get("stretch", 0))

            if returns:
                return widget

            return None

        return add_to_layout

    def Prefab(self, prefab_component, alignment: AlignmentTypes | None = None,  stretch: int = 0):
        """
        Adds a Complex Component (@Prefab) to the current layout.

        This method integrates pre-fabricated components (functions decorated 
        with `@Prefab`) into a Fluvel layout, extracting the component's 
        main container and appending it to the parent widget hierarchy.

        :param prefab_component: The pre-fabricated component.
        :type prefab_component: :py:class:`~fluvel.core.abstract_models.ABCAbstractPage.Page` | Callable

        :param alignment: Alignment of the prefab within the layout cell.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes` | None

        :param stretch: The **stretch factor** to assign to the widget. This value 
                    determines how much extra space the widget receives relative 
                    to other widgets in the same layout row or column. 
                    A value of 0 means the widget will not receive extra space 
                    when the window is resized. A higher number (e.g., 1, 2, 3) 
                    means the widget will grow proportionally more.
        :type stretch: int

        Usage
        -----
        .. code-block:: python
        
            with self.Vertical() as v:
            
                v.Prefab(ComponentName(arg="value"))
                # or
                v.Prefab(ComponentName) # This component does not require any arguments.
        """

        container = None

        if isinstance(prefab_component, Callable):
            container = prefab_component()
        else:
            container = prefab_component

        self.add_widget(container, alignment, stretch)
