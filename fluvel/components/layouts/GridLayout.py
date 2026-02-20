# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TypeVar

# PySide6
from PySide6.QtWidgets import QGridLayout, QLayout, QWidget

from fluvel.components.widgets.containers.FContainer import FContainer
from fluvel.composer import Canvas

# Fluvel
from fluvel.core.abstract.FLayout import FLayout
from fluvel.core.abstract.FLayoutAPI import FLayoutAPI
from fluvel.core.abstract.LayoutBuilder import LayoutBuilder

# Enums
from fluvel.core.enums.alignment import Alignment, AlignmentTypes

TWidget = TypeVar("TWidget", bound=QWidget)


class ColumnIndex(FLayoutAPI):
    """
    Handler for managing a single column in a GridLayout.

    This class provides a declarative and intuitive way to add widgets
    sequentially to a specific column within a grid, emulating a vertical layout (VBoxLayout) for each one.

    :ivar _grid: The container GridLayout instance.
    :type _grid: QGridLayout
    :ivar column: The index of the column this handler manages.
    :type column: int
    :ivar _current_row: The integer indicating the current position of the row 'cursor' within a column.
    :type _current_row: int
    """

    def __init__(self, grid: "GridLayout", column: int):
        """
        Initializer for a ColumnIndex.

        :param grid: The container GridLayout instance.
        :type grid: QGridLayout
        :param column: The index of the column this handler manages.
        :type column: int
        """

        # Store the GridLayout instance
        self._grid = grid

        # Store the column index
        self._column_index = column

        # Instance variable used to indicate to the row cursor
        # that it should initially point to the first row (index 0)
        self._current_row: int = 0

    def _create_widget(self, widget_class: type[TWidget], **kwargs) -> TWidget:
        """
        Creates an instance of the specified widget and adds it to the column layout.

        This method acts as the central insertion point for all declarative methods
        of the :class:`~fluvel.core.abstract.SKLayoutAPI` (e.g., :meth:`~SKLayoutAPI.Label`, :meth:`~SKLayoutAPI.Button`).

        It is responsible for intercepting the grid control arguments
        (:code:`rspan` and :code:`cspan`) for the :meth:`~ColumnIndex.add` method
        before passing the rest of the arguments to the widget constructor.

        :param widget_class: The class of the widget to instantiate (e.g., :class:`~fluvel.components.widgets.FLabel`).
        :type widget_class: Type[TWidget]
        :param kwargs: Widget configuration arguments (e.g., 'text', 'style', 'bind')
                    and grid control arguments ('rspan', 'cspan').
        :type kwargs: dict

        :returns: The widget instance created and already added to the grid.
        :rtype: TWidget

        .. note::
            The :code:`rspan` and :code:`cspan` arguments are extracted and used
            for insertion. If not provided, the default value of 1 is used.
            These arguments are NOT passed to the widget constructor (:code:`widget_class`).
        """

        rspan = kwargs.pop("rspan", 1)
        cspan = kwargs.pop("cspan", 1)
        alignment = kwargs.pop("alignment", "none")

        widget: TWidget = widget_class(**kwargs)

        self.add(widget, rspan, cspan, alignment)

        return widget

    def add(
        self,
        item: QWidget | Canvas,
        rspan: int = 1,
        cspan: int = 1,
        alignment: AlignmentTypes = "none",
    ) -> None:
        """
        Adds a widget or canvas to the next available row in the column.

        This method automatically finds the next empty cell in the assigned
        column and adds the given object. The row cursor is then advanced
        by the ``rspan`` value.

        :param item: The :class:`QWidget` or :class:`Canvas` to add to the cell.
        :type item: QWidget or Canvas
        :param rspan: The number of rows the object will span. Defaults to 1.
        :type rspan: int
        :param cspan: The number of columns the object will span. Defaults to 1.
        :type cspan: int
        :param alignment: Alignment of the widget within the layout cell.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`
        """

        # If there is an element in the current cell
        while self._grid.itemAtPosition(self._current_row, self._column_index) is not None:
            # Increases the row cursor by 1
            # while the current cell is occupied by another Widget or Layout
            self._current_row += 1

        # Add the widget or layout with the row and column parameters of the class.
        self._grid.addCell(item, self._current_row, self._column_index, rspan, cspan, alignment)

        # The row cursor is increased according to the space occupied by the widget (rspan).
        self._current_row += rspan

    def stretch(self, factor: int = 1) -> None:
        """
        Sets the stretch factor for the column managed by this instance.

        This method allows the column to occupy excess space in the grid 
        when the window is resized. A stretch factor of 0 means the column 
        will not stretch.

        :param factor: The stretch factor. Defaults to 1.
        :type factor: int

        Example
        -------
        .. code-block:: python

            with self.Grid() as grid:
                c1, c2 = grid.Columns(2)

                # Make the second column occupy all available excess space
                c2.stretch(1)
                  
                c1.Label(text="Fixed width")
                c2.Button(text="Flexible width")
        """
        self._grid.setColumnStretch(self._column_index, factor)

    def _update_grid_cursor(self) -> None:
        self._grid._row = self._current_row
        self._grid._column = self._column_index

    def Vertical(self, **kwargs):
        self._update_grid_cursor()
        return LayoutBuilder.Vertical(self._grid, **kwargs)

    def Horizontal(self, **kwargs):
        self._update_grid_cursor()
        return LayoutBuilder.Horizontal(self._grid, **kwargs)

    def Grid(self, **kwargs):
        self._update_grid_cursor()
        return LayoutBuilder.Grid(self._grid, **kwargs)


class GridLayout(QGridLayout, FLayout, LayoutBuilder):
    """
    Base class for handling GridLayouts in Fluvel.

    This class provides the API to manage QGridLayouts, offering
    helper methods to simplify the addition of widgets and layouts.
    """

    def __init__(self, parent: FContainer | None = None):
        super().__init__(parent)
        self._row = -1
        self._column = -1

    def __next__(self) -> ColumnIndex:
        self._column += 1
        return ColumnIndex(self, self._column)

    def Column(self, column: int) -> ColumnIndex:
        """
        Obtains a handler for a specific column in the grid.

        This method returns a :class:`~fluvel.components.layouts.GridLayout.ColumnIndex` object that allows widgets to be added
        sequentially to a column, as if it were a vertical layout.

        .. seealso::
            :meth:`GridLayout.Columns` for the idiomatic way of managing multiple columns.

        :param column: The index of the column to be handled (starting at 0).
        :type column: int
        :returns: A handler object for the specified column.
        :rtype: ColumnIndex


        Example
        -------
        .. code-block:: python
            ...
            with self.Grid() as grid:
                c1 = grid.Column(0) # first column
                c2 = grid.Column(1) # second column

                # Add widgets to the first column
                c1.Label(text="Name:")
                c1.LineEdit()

                # Add widgets to the second column
                c2.Label(text="Surname:")
                c2.LineEdit()
        """

        return ColumnIndex(self, column)

    def Columns(self, n_cols: int) -> list[ColumnIndex]:
        """
        Preferred method for creating a list of 
        :class:`~fluvel.components.layouts.GridLayout.ColumnIndex` objects.

        This method allows for the idiomatic unpacking of column handlers
        in Python.

        :param n_cols: The number of columns to create in the grid.
        :type n_cols: int
        :returns: A list of :class:`~fluvel.components.layouts.GridLayout.ColumnIndex` objects.
        :rtype: list

        Example
        -------
        .. code-block:: python
            ...
            with self.Grid() as grid:

                c1, c2 = grid.Columns(2)

                # Add widgets to the first column
                c1.Label(text="Name:")
                c1.Input()

                # Add widgets to the second column
                c2.Label(text="Surname:")
                c2.Input()
        """

        return [next(self) for _ in range(n_cols)]

    def add(
        self, 
        item: QWidget | Canvas | QLayout, 
        alignment: AlignmentTypes = "none", 
        _: None = None,
        column: int = None,
        rspan: int = 1,
        cspan: int = 1
    ) -> None:
        """
        Adds an existing widget or prefab (:class:`~fluvel.composer.Prefab.Canvas`) in the last column that was worked.

        :param item: The instance of the widget or canvas.
        :type item: QWidget | Canvas | QLayout

        :param alignment: Alignment of the widget within the layout cell.
        :type alignment: :class:`~fluvel.core.enums.alignment.AlignmentTypes`
        :param column: The column of the column where to add the item
        :type column: int
        :param rspan: The number of rows the object will span. Defaults to 1.
        :type rspan: int
        :param cspan: The number of columns the object will span. Defaults to 1.
        :type cspan: int
        """
        column = column or self._column
        column_handler = ColumnIndex(self, column)
        column_handler.add(item, rspan, cspan, alignment)

    def addLayout(
        self, 
        layout: QLayout, 
        /,
        column: int = None,
        rspan: int = 1,
        cspan: int = 1,
        alignment: AlignmentTypes = "none"
    ):
        """
        Adds a layout to a grid cell.

        This method is used to manually place a :class:`QLayout`
        into a specific cell of the grid.

        :param item: The layout to add to the cell.
        :type item: QLayout
        :param row: The row index of the cell.
        :type row: int
        :param column: The column index of the cell.
        :type column: int
        :param rspan: The number of rows the object will span. Defaults to 1.
        :type rspan: int
        :param cspan: The number of columns the object will span. Defaults to 1.
        :type cspan: int
        """
        self.add(layout, alignment, None, column, rspan, cspan)

    def addCell(
        self,
        item: QWidget | Canvas | QLayout,
        /,
        row: int,
        column: int,
        rspan: int = 1,
        cspan: int = 1,
        alignment: AlignmentTypes = "none"
    ) -> None:
        """
        Adds a widget, layout or prefab to a grid cell.

        This method is used to manually place a :class:`QWidget` or :class:`Canvas`
        into a specific cell of the grid.

        :param item: The widget, layout or prefab to add to the cell.
        :type item: QWidget or Canvas or QLayout
        :param row: The row index of the cell.
        :type row: int
        :param column: The column index of the cell.
        :type column: int
        :param rspan: The number of rows the object will span. Defaults to 1.
        :type rspan: int
        :param cspan: The number of columns the object will span. Defaults to 1.
        :type cspan: int
        :raises TypeError: if the provided object is not a QWidget or Canvas.

        .. note::
            While this method exists for manual control, it's recommended to use the
            declarative methods :meth:`~Grid.Column` and :meth:`~Grid.Columns`
            for a cleaner and more organized layout structure.

        .. seealso::
            :meth:`~Grid.Column`
            :meth:`~Grid.Columns`

        Example:
        --------
        .. code-block:: python
            ...
            with my_view.Grid() as grid:
                # Adds a button to row 0, column 0
                grid.addCell(FButton(text="button"), 0, 0)

                # Adds a label to row 0, column 1
                grid.addCell(FLabel(text="label"), 0, 1)

                # Adds a button that spans 2 columns
                grid.addCell(FButton(text="Spanning Button"), 1, 0, 1, 2)
        """
        alignment = Alignment.get(alignment)
        args = (item, row, column, rspan, cspan, alignment)

        if isinstance(item, QWidget):
            self.addWidget(*args)

        elif isinstance(item, QLayout):
            super().addLayout(*args)

        else:
            raise TypeError("The 'item' argument must be an instance of QWidget, Canvas or View")