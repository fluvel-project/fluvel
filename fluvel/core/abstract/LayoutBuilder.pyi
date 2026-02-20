from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    TypeVar,
    Unpack,
    overload,
)

# PySide6
from PySide6.QtWidgets import QLayout

from fluvel.components.widgets.containers import (
    FContainer, FContainerKwargs,
    FGroupBox,
    FGroupBoxKwargs,
    FImageContainerKwargs,
    FScrollAreaKwargs,
)

# Necessary to avoid circular imports of
# layouts inherited from Builder
if TYPE_CHECKING:
    from fluvel.components.layouts import GridLayout, HBoxLayout, VBoxLayout

# Define a type variable for layouts
TLayout = TypeVar("TLayout", bound=QLayout)
LayoutTypes = Literal["vertical", "horizontal", "grid"]

class GroupKwargs(FGroupBoxKwargs, FContainerKwargs): pass
class ScrollKwargs(FScrollAreaKwargs, FContainerKwargs): pass
class ImageAreaKwargs(FImageContainerKwargs, FContainerKwargs): pass

# Internal cache for layouts
_L_CACHE: dict[str, type[QLayout]]

def _get_layout(layout: str) -> type[QLayout]: ...

class CMLayoutBuilder(Generic[TLayout]):
    """
    Context manager for the declarative creation of PySide6 layouts.

    This class allows developers to build nested layouts intuitively using the
    :keyword:`with` syntax, automatically handling the addition of the new layout
    to an existing container (:class:`PySide6.QtWidgets.QLayout` or :class:`~fluvel.components.widgets.FContainer.FContainer`).

    :ivar layout: The instantiated :class:`PySide6.QtWidgets.QLayout`.
    :type layout: TLayout
    """
    layout: TLayout
    parent_widget: FContainer | None

    def __init__(
        self,
        container: QLayout | FContainer,
        type_layout: type[TLayout],
        **kwargs: Unpack[FContainerKwargs],
    ) -> None:
        """
        Initializes the :class:`~fluvel.core.abstract.AbstractPage.LayoutBuilder` instance.

        :param container: The layout or widget to which the new layout will be added.
        :type container: :class:`PySide6.QtWidgets.QLayout` or :class:`~fluvel.components.widgets.FContainer.FContainer`

        :param type_layout: The class of the layout to instantiate (e.g., :class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`).
        :type type_layout: type[TLayout]

        :param style: The QSS-style class name(s) to apply to the layout's parent container :class:`~fluvel.components.widgets.FContainer.FContainer`.
        :type style: str or None

        :param drag_window: Enable dragging of the Main Window.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :param alignment: Alignment to add the container widget to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`
        """
        ...

    def __enter__(self) -> TLayout:
        """
        Context manager entry method.

        Returns the layout instance so it can be used inside the :keyword:`with` block.

        :returns: The instantiated layout object.
        :rtype: TLayout
        """
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """
        Context manager exit method.

        :returns: Always returns :obj:`False` to avoid suppressing exceptions.
        :rtype: bool
        """
        ...

class LayoutBuilder:
    """
    A Mixin that provides the declarative API ('Vertical','Horizontal', etc.)
    for building layouts using LayoutBuilder.
    """

    def _build_container_layout(
        self, container_type: type[FGroupBox] | type[FContainer], **kwargs: Any
    ) -> CMLayoutBuilder[Any]:
        """
        Lógica centralizada para contenedores que envuelven un layout.
        """
        ...

    def Vertical(self, **kwargs: Unpack[FContainerKwargs]) -> CMLayoutBuilder[VBoxLayout]:
        """
        Creates a vertical box layout (:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`)
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str

        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :param alignment: Alignment to add the container widget to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :returns: A :class:`LayoutBuilder` for :class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`.
        :rtype: LayoutBuilder[VBoxLayout]

        Example:
        --------
        .. code-block:: python
            ...
            with self.Vertical() as v:
                v.Label(text="Hello")
        """
        ...

    def Horizontal(self, **kwargs: Unpack[FContainerKwargs]) -> CMLayoutBuilder[HBoxLayout]:
        """
        Creates a horizontal box layout (:class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`)
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str

        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :param alignment: Alignment to add the container widget to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :returns: A :class:`LayoutBuilder` for :class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`.
        :rtype: LayoutBuilder[HBoxLayout]

        Example:
        --------
        .. code-block:: python
            ...
            with self.Horizontal() as h:
                h.Label(text="Hello")
        """
        ...
    
    def Grid(self, **kwargs: Unpack[FContainerKwargs]) -> CMLayoutBuilder[GridLayout]:
        """
        Creates a grid layout (:class:`~fluvel.components.layouts.GridLayout.GridLayout`)
        using a context manager.

        :param style: The style for the layout's container.
        :type style: str

        :param drag_window: Enable dragging of the Main Window.
                            Allows you to drag the Main Window
                            from the design area.
        :type drag_window: bool

        :param stretch: The **stretch factor** to assign to the layout container.
        :type stretch: int

        :param alignment: Alignment to add the container widget to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :returns: A :class:`LayoutBuilder` for :class:`~fluvel.components.layouts.GridLayout.GridLayout`.
        :rtype: LayoutBuilder[GridLayout]
        """
        ...

    @overload
    def Scroll(
        self, *, layout: Literal["vertical"] = "vertical", **kwargs: Unpack[ScrollKwargs]
    ) -> CMLayoutBuilder[VBoxLayout]: ...

    @overload
    def Scroll(
        self, *, layout: Literal["horizontal"], **kwargs: Unpack[ScrollKwargs]
    ) -> CMLayoutBuilder[HBoxLayout]: ...

    @overload
    def Scroll(
        self, *, layout: Literal["grid"], **kwargs: Unpack[ScrollKwargs]
    ) -> CMLayoutBuilder[GridLayout]: ...

    def Scroll(self, **kwargs: Unpack[ScrollKwargs]) -> CMLayoutBuilder[Any]:
        """
        Creates a scroll area (:class:`~fluvel.components.widgets.FScrollArea.FScrollArea`)
        that wraps a new inner layout.

        :param layout: Type of inner layout ('vertical', 'horizontal', or 'grid').
        :type layout: str

        :param resizable: Determines whether the scroll area automatically adjusts to the size of the content.
        :type resizable: bool

        :param alignment: Alignment to add the scroll area to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :param stretch: Stretch factor to add the scroll area to the parent layout.
        :type stretch: int

        :param bind: A string with the key or a list of keys to bind.
        :type bind: str or List[str] or None

        :param style: QSS style classes for the **internal content container** (:class:`~fluvel.components.widgets.FContainer.FContainer`).
        :type style: str

        :param scroll_style: QSS style classes for the **scroll wrapper** (:class:`~fluvel.components.widgets.FScrollArea.FScrollArea`).
        :type scroll_style: str

        :param drag_window: Enables dragging the main window from the internal container.
        :type drag_window: bool

        :returns: A :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder` that provides the internal layout for adding widgets.
        :rtype: :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder`
                [:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`
                or :class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`
                or :class:`~fluvel.components.layouts.GridLayout.GridLayout`]
        """
        ...

    @overload
    def ImageArea(
        self, *, layout: Literal["vertical"] = "vertical", **kwargs: Unpack[ImageAreaKwargs]
    ) -> CMLayoutBuilder[VBoxLayout]: ...

    @overload
    def ImageArea(
        self, *, layout: Literal["horizontal"], **kwargs: Unpack[ImageAreaKwargs]
    ) -> CMLayoutBuilder[HBoxLayout]: ...

    @overload
    def ImageArea(
        self, *, layout: Literal["grid"], **kwargs: Unpack[ImageAreaKwargs]
    ) -> CMLayoutBuilder[GridLayout]: ...

    def ImageArea(self, **kwargs: Unpack[ImageAreaKwargs]) -> CMLayoutBuilder[Any]:
        """
        Creates a container with a background image (:class:`~fluvel.components.widgets.FImageContainer.FImageContainer`)
        that wraps a new inner layout.

        :param source: Path to the image file, a :class:`~PySide6.QtGui.QPixmap`, or a :class:`~PySide6.QtGui.QImage`.
        :type source: str or :class:`~PySide6.QtGui.QPixmap` or :class:`~PySide6.QtGui.QImage`

        :param rounded: Percentage (0-100) of corner rounding based on the smallest dimension. Defaults to 0.
        :type rounded: int

        :param keep_aspect_ratio: If True, scales the image to fit the container without distortion. Defaults to True.
        :type keep_aspect_ratio: bool

        :param cover: If True, the image covers the entire container area (may crop). If False, fits the image inside. Defaults to True.
        :type cover: bool

        :param layout: Type of inner layout ('vertical', 'horizontal', or 'grid'). Defaults to 'vertical'.
        :type layout: str

        :param alignment: Alignment to add the image container to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :param stretch: Stretch factor to add the image container to the parent layout.
        :type stretch: int

        :param bind: A string with the key or a list of keys to bind.
        :type bind: str or List[str] or None

        :param style: QSS style classes for the image container itself.
        :type style: str

        :param drag_window: Enables dragging the main window from the image container.
        :type drag_window: bool

        :returns: A :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder` that provides the internal layout for adding widgets.
        :rtype: :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder`
                [:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`
                or :class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`
                or :class:`~fluvel.components.layouts.GridLayout.GridLayout`]
        """
        ...

    @overload
    def Group(
        self, *, layout: Literal["vertical"] = "vertical", **kwargs: Unpack[GroupKwargs]
    ) -> CMLayoutBuilder[VBoxLayout]: ...

    @overload
    def Group(
        self, *, layout: Literal["horizontal"], **kwargs: Unpack[GroupKwargs]
    ) -> CMLayoutBuilder[HBoxLayout]: ...

    @overload
    def Group(
        self, *, layout: Literal["grid"], **kwargs: Unpack[GroupKwargs]
    ) -> CMLayoutBuilder[GridLayout]: ...

    def Group(self, **kwargs: Unpack[GroupKwargs]) -> CMLayoutBuilder[Any]:
        """
        Creates a titled group container (:class:`~fluvel.components.widgets.FGroupBox.FGroupBox`)
        ideal for logically grouping related widgets.

        :param title: The title text to display in the group box frame.
        :type title: str

        :param layout: Type of inner layout ('vertical', 'horizontal', or 'grid').
        :type layout: str

        :param align: Alignment of the group box title text. Defaults to 'center-left'.
        :type align: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :param alignment: Alignment for adding the Group to the parent layout.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`

        :param stretch: Stretch factor for adding the Group to the parent layout.
        :type stretch: int

        :param bind: A string with the key or a list of keys to bind.
        :type bind: str or List[str] or None

        :param style: QSS style classes for the Group container itself.
        :type style: str

        :param flat: If True, the Group will not draw the frame around the content.
        :type flat: bool

        :returns: A :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder` that provides the internal layout for adding widgets.
        :rtype: :class:`~fluvel.core.abstract.LayoutBuilder.CMLayoutBuilder`
                [:class:`~fluvel.components.layouts.VBoxLayout.VBoxLayout`
                or :class:`~fluvel.components.layouts.HBoxLayout.HBoxLayout`
                or :class:`~fluvel.components.layouts.GridLayout.GridLayout`]
        """
        ...