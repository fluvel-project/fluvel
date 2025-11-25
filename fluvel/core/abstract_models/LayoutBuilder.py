from typing import TYPE_CHECKING, List, TypedDict, Unpack, TypeVar, Generic, Type

# Fluvel
from fluvel.components.widgets.FContainer import FContainer
from fluvel.core.enums.alignment import AlignmentTypes

# PySide6
from PySide6.QtWidgets import QLayout

# necessary to avoid circular imports of 
# layouts inherited from Builder
if TYPE_CHECKING:
    from fluvel.components.layouts import VBoxLayout, HBoxLayout, GridLayout, FormLayout

# Define a type variable for layouts
TLayout = TypeVar("TLayout", bound=QLayout)

class LayoutBuilderKwargs(TypedDict, total=False):

    bind        : str | List[str]
    style       : str
    drag_window : bool
    stretch     : int
    alignment   : AlignmentTypes

class CMLayoutBuilder(Generic[TLayout]):
    """
    Context manager for the declarative creation of PySide6 layouts.

    This class allows developers to build nested layouts intuitively using the 
    :keyword:`with` syntax, automatically handling the addition of the new layout 
    to an existing container (:py:class:`PySide6.QtWidgets.QLayout` or :py:class:`~fluvel.components.widgets.FContainer.FContainer`).

    :ivar layout: The instantiated :py:class:`PySide6.QtWidgets.QLayout`.
    :type layout: TLayout
    """

    def __init__(
        self,
        container: QLayout | FContainer, 
        type_layout: Type[TLayout],
        **kwargs: Unpack[LayoutBuilderKwargs]
    ):
        """
        Initializes the :py:class:`~fluvel.core.abstract_models.ABCAbstractView.LayoutBuilder` instance.

        :param container: The layout or widget to which the new layout will be added.
        :type container: :py:class:`PySide6.QtWidgets.QLayout` or :py:class:`~fluvel.components.widgets.FContainer.FContainer`

        :param type_layout: The class of the layout to instantiate (e.g., :py:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`).
        :type type_layout: type[TLayout]

        :param style: The QSS-style class name(s) to apply to the layout's parent container :py:class:`~fluvel.components.widgets.FContainer.FContainer`.
        :type style: str or None

        :param drag_window: Enable dragging of the Main Window.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int
        """

        stretch = kwargs.pop("stretch", 0)
        alignment = kwargs.pop("alignment", None)
        style = kwargs.pop("style", "bg-transparent")

        parent_widget = None
        
        # The container is a QLayout, 
        # which means that an FContainer must be created and added 
        # to the current QLayout (container parameter) 
        # for it to function as a new container for the requested QLayout.
        if isinstance(container, QLayout):
            
            # Based on the “drag_window” parameter, 
            # it decides whether the container is 
            # capable of dragging the main window.
            parent_widget = FContainer()

            # Then add the widget to the layout
            container.add_widget(parent_widget, stretch=stretch, alignment=alignment)

            # Finally, the requested layout is instantiated 
            # as a child of the newly created FContainer.
            self.layout: TLayout = type_layout(parent_widget)

        # The container is a FContainer
        elif isinstance(container, FContainer):

            parent_widget = container
            
            self.layout: TLayout = type_layout(parent_widget)

        else:
            raise TypeError("The container must be a QLayout or an FContainer.")

        parent_widget.configure(style=style, **kwargs)

            
    def __enter__(self) -> TLayout:
        """
        Context manager entry method.
        
        Returns the layout instance so it can be used inside the :keyword:`with` block.
        
        :returns: The instantiated layout object.
        :rtype: TLayout
        """
        return self.layout

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method.
        
        :returns: Always returns :py:obj:`False` to avoid suppressing exceptions.
        :rtype: bool
        """
        return False

class LayoutBuilder:
    """
    A Mixin that provides the declarative API ('Vertical','Horizontal', etc.)
    for building layouts using LayoutBuilder.
    """

    def build_layout(
        self, 
        type_layout: Type[TLayout], 
        **kwargs: Unpack[LayoutBuilderKwargs]
    ) -> CMLayoutBuilder[TLayout]:
        """
        Internal factory method for creating a :py:class:`LayoutBuilder`.

        :param type_layout: The class of the layout to instantiate.
        :type type_layout: type[TLayout]

        :param style: The QSS-style class name(s) for the layout's container.
        :type style: str

        :param drag_window: Enable dragging of the Main Window.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :returns: A configured :py:class:`LayoutBuilder`.
        :rtype: LayoutBuilder[TLayout]
        """

        return CMLayoutBuilder(self, type_layout, **kwargs)

    def Vertical(self, **kwargs: Unpack[LayoutBuilderKwargs]) -> "CMLayoutBuilder[VBoxLayout]":
        """
        Creates a vertical box layout (:py:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`) 
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str or None
        
        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int
        
        :returns: A :py:class:`LayoutBuilder` for :py:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`.
        :rtype: LayoutBuilder[VBoxLayout]
        
        Example:
        --------
        .. code-block:: python
            ...
            with self.Vertical() as v:
                v.Label(text="Hello")
        """
        from fluvel.components.layouts import VBoxLayout

        return self.build_layout(VBoxLayout, **kwargs)

    def Horizontal(self, **kwargs: Unpack[LayoutBuilderKwargs]) -> "CMLayoutBuilder[HBoxLayout]":
        """
        Creates a horizontal box layout (:py:class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`) 
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str or None
        
        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :returns: A :py:class:`LayoutBuilder` for :py:class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`.
        :rtype: LayoutBuilder[HBoxLayout]
        
        Example:
        --------
        .. code-block:: python
            ...
            with self.Horizontal() as h:
                h.Label(text="Hello")
        """
        from fluvel.components.layouts import HBoxLayout
        
        return self.build_layout(HBoxLayout, **kwargs)

    def Form(self, **kwargs: Unpack[LayoutBuilderKwargs]) -> "CMLayoutBuilder[FormLayout]":
        """
        Creates a form layout (:py:class:`~fluvel.components.layouts.FormLayout.FormLayout`) 
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str or None

        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :returns: A :py:class:`LayoutBuilder` for :py:class:`~fluvel.components.layouts.FormLayout.FormLayout`.
        :rtype: LayoutBuilder[FormLayout]
        """
        from fluvel.components.layouts import FormLayout

        return self.build_layout(FormLayout, **kwargs)

    def Grid(self, **kwargs: Unpack[LayoutBuilderKwargs]) -> "CMLayoutBuilder[GridLayout]":
        """
        Creates a grid layout (:py:class:`~fluvel.components.layouts.GridLayout.GridLayout`) 
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str or None

        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :returns: A :py:class:`LayoutBuilder` for :py:class:`~fluvel.components.layouts.GridLayout.GridLayout`.
        :rtype: LayoutBuilder[GridLayout]
        """
        from fluvel.components.layouts import GridLayout

        return self.build_layout(GridLayout, **kwargs)

    def Stacked(self): ... # TODO

    # TODO 
    def DockSection(
        self, 
        title: str,
        layout: str = "vertical",
        side: str = "left",
        style: str | None = None
    ) -> "CMLayoutBuilder[VBoxLayout | HBoxLayout]":
        """
        TODO: Esta es una funcionalidad aún no implementada
        """

        from PySide6.QtWidgets import QDockWidget
        from PySide6.QtCore import Qt
        from fluvel.components.layouts import VBoxLayout, HBoxLayout

        layouts: dict[str, Type[QLayout]] = {
            "vertical": VBoxLayout,
            "horizontal": HBoxLayout 
        }

        dock_areas = {
            "right": Qt.DockWidgetArea.RightDockWidgetArea,
            "left": Qt.DockWidgetArea.LeftDockWidgetArea,
            "top": Qt.DockWidgetArea.TopDockWidgetArea,
            "bottom": Qt.DockWidgetArea.BottomDockWidgetArea
        }

        dock_widget = QDockWidget(title, self.main_window) 
        dock_container = FContainer()
        dock_widget.setWidget(dock_container)
        dock_layout = layouts.get(layout)
        self.main_window.addDockWidget(dock_areas.get(side), dock_widget)

        return self.build_layout(dock_container, dock_layout, style, False, 0)