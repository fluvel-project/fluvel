# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Unpack

# Fluvel Widgets
import fluvel.components.widgets as w


class FLayoutAPI:

    def Label(self, **kwargs: Unpack[w.FLabelKwargs]) -> w.FLabel:
        """
        Creates and instantiates a label component (:class:`~fluvel.components.widgets.FLabel`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QLabel` that implements the Fluvel
        styling engine and support for internationalization.

        :param text: Text to display in the label.
        :type text: str | I18nTextVar
        :param wordwrap: If ``True``, the text will automatically wrap to the next line if it does not fit.
        :type wordwrap: bool
        :param align: Alignment of the text or image within the label.
        :type align: AlignmentTypes
        :param indent: Text indentation in pixels.
        :type indent: int
        :param margin: Internal margin of the label in pixels.
        :type margin: int
        :param pixmap: Image to display (QPixmap or QImage).
        :type pixmap: QPixmap | QImage
        :param movie: Animation to display (QMovie).
        :type movie: QMovie
        :param picture: Vector image to display (QPicture).
        :type picture: QPicture
        :param open_links: If ``True`` (default), HTTP links within RichText will open in the external browser.
        :type open_links: bool
        :param scaled_contents: If ``True``, the image pixmap will be scaled to fit the label size.
        :type scaled_contents: bool
        :param format: Defines how the text is interpreted (Plain, Markdown, HTML).
        :type format: TextFormatTypes
        :param flags: Defines how the user interacts with the text (selecting, clicking).
        :type flags: TextInteractionTypes | list[TextInteractionTypes]
        :param buddy: Widget to which this label is associated (for keyboard shortcuts).
        :type buddy: QWidget
        :param on_link_hovered: Callback ``Callable[[str], None]`` executed when the pointer hovers over a link.
        :type on_link_hovered: Callable
        :param on_link_activated: Callback ``Callable[[str], None]`` executed when a link is clicked.
        :type on_link_activated: Callable
        :return: A configured instance of FLabel.
        :rtype: fluvel.components.widgets.FLabel
        """
        return self._create_widget(w.FLabel, **kwargs)

    def Button(self, **kwargs: Unpack[w.FButtonKwargs]) -> w.FButton:
        """
        Creates and instantiates a button component (:class:`~fluvel.components.widgets.FButton`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QPushButton` that implements the Fluvel
        styling engine and support for internationalization.

        :param text: Text to display on the button.
        :type text: str | I18nTextVar
        :param checkable: If ``True``, the button can be toggled between checked and unchecked states.
        :type checkable: bool
        :param icon: Icon to display on the button.
        :type icon: QIcon
        :param icon_size: Size of the icon in pixels (width and height are equal).
        :type icon_size: int
        :param shortcut: Keyboard shortcut string (e.g., "Ctrl+S").
        :type shortcut: str
        :param is_default: If ``True``, the button is the default button in the dialog.
        :type is_default: bool
        :param auto_default: If ``True``, the button will become the default button when it receives focus.
        :type auto_default: bool
        :param flat: If ``True``, the button frame is not drawn (flat appearance).
        :type flat: bool
        :param menu: A context menu associated with the button.
        :type menu: QMenu
        :param on_click: Callback ``Callable[[], None]`` executed when the button is clicked.
        :type on_click: Callable
        :param on_pressed: Callback ``Callable[[], None]`` executed when the button is pressed.
        :type on_pressed: Callable
        :param on_released: Callback ``Callable[[], None]`` executed when the button is released.
        :type on_released: Callable
        :param on_toggled: Callback ``Callable[[bool], None]`` executed when the checkable state changes.
        :type on_toggled: Callable
        :return: A configured instance of FButton.
        :rtype: fluvel.components.widgets.FButton
        """
        return self._create_widget(w.FButton, **kwargs)

    def IconButton(self, **kwargs: Unpack[w.FIconButtonKwargs]) -> w.FIconButton:
        """
        Creates and instantiates a button component (:class:`~fluvel.components.widgets.FIconButton`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QPushButton` that implements the Fluvel
        styling engine and support for internationalization.
        
        :param size: The fixed size (width and height) of the button in pixels. Default is 24.
        :type size: int
        :param text: Text to display on the button.
        :type text: str | I18nTextVar
        :param checkable: If ``True``, the button can be toggled between checked and unchecked states.
        :type checkable: bool
        :param icon: Icon to display on the button.
        :type icon: QIcon
        :param icon_size: Size of the icon in pixels (width and height are equal).
        :type icon_size: int
        :param shortcut: Keyboard shortcut string (e.g., "Ctrl+S").
        :type shortcut: str
        :param is_default: If ``True``, the button is the default button in the dialog.
        :type is_default: bool
        :param auto_default: If ``True``, the button will become the default button when it receives focus.
        :type auto_default: bool
        :param flat: If ``True``, the button frame is not drawn (flat appearance).
        :type flat: bool
        :param menu: A context menu associated with the button.
        :type menu: QMenu
        :param on_click: Callback ``Callable[[], None]`` executed when the button is clicked.
        :type on_click: Callable
        :param on_pressed: Callback ``Callable[[], None]`` executed when the button is pressed.
        :type on_pressed: Callable
        :param on_released: Callback ``Callable[[], None]`` executed when the button is released.
        :type on_released: Callable
        :param on_toggled: Callback ``Callable[[bool], None]`` executed when the checkable state changes.
        :type on_toggled: Callable
        :return: A configured instance of FIconButton.
        :rtype: fluvel.components.widgets.FIconButton
        """
        return self._create_widget(w.FIconButton, **kwargs)

    def CheckBox(self, **kwargs: Unpack[w.FCheckBoxKwargs]) -> w.FCheckBox:
        """
        Creates and instantiates a checkbox component (:class:`~fluvel.components.widgets.FCheckBox`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QCheckBox` that implements the Fluvel
        styling engine and support for internationalization.

        :param text: Text to display next to the checkbox.
        :type text: str | I18nTextVar
        :param size: Fixed size (width, height) of the checkbox in pixels.
        :type size: tuple[int, int]
        :param checkable: If ``True`` (default), the checkbox can be checked or unchecked by the user.
        :type checkable: bool
        :param checked: If ``True``, the checkbox is initially checked.
        :type checked: bool
        :param checkstate: Initial check state of the checkbox. Can be "checked", "partial", or "unchecked".
        :type checkstate: CheckStateTypes
        :param on_click: Callback ``Callable[[], None]`` executed when the checkbox is clicked.
        :type on_click: Callable
        :param on_toggled: Callback ``Callable[[bool], None]`` executed when the checked state changes.
        :type on_toggled: Callable
        :param on_pressed: Callback ``Callable[[], None]`` executed when the checkbox is pressed.
        :type on_pressed: Callable
        :param on_released: Callback ``Callable[[], None]`` executed when the checkbox is released.
        :type on_released: Callable
        :param on_changed: Callback ``Callable[[int], None]`` executed when the check state changes, providing the raw Qt check state integer.
        :type on_changed: Callable
        :return: A configured instance of FCheckBox.
        :rtype: fluvel.components.widgets.FCheckBox
        """
        return self._create_widget(w.FCheckBox, **kwargs)

    def Switch(self, **kwargs: Unpack[w.FSwitchKwargs]) -> w.FSwitch:
        """
        Creates and instantiates a native Fluvel switch component (:class:`~fluvel.components.widgets.FSwitch`) 
        within the current context.

        This is a modern toggle switch wrapper of :class:`PySide6.QtWidgets.QCheckBox`
        featuring smooth color and position animations, and optional icons.
        Inherits behavior from :class:`~fluvel.components.widgets.FCheckBox`.

        :param bg_color: Hex color string for the inactive state background. Defaults to "#777777".
        :type bg_color: str
        :param circle_color: Hex color string for the moving thumb circle. Defaults to "#FFFFFF".
        :type circle_color: str
        :param active_color: Hex color string for the active state background. Defaults to "#2E94D8".
        :type active_color: str
        :param animation_curve: Easing curve for the animation. Defaults to :attr:`QEasingCurve.Type.InOutCubic`.
        :type animation_curve: QEasingCurve
        :param icon_off: Icon to display inside the thumb when off.
        :type icon_off: QIcon
        :param icon_on: Icon to display inside the thumb when on.
        :type icon_on: QIcon
        :param icon_size: Size (width, height) of the icons in pixels. Defaults to (14, 14).
        :type icon_size: tuple[int, int]
        :param checked: If ``True``, the switch is initially on.
        :type checked: bool
        :param on_toggled: Callback ``Callable[[bool], None]`` executed when the switch state changes.
        :type on_toggled: Callable
        :return: A configured instance of FSwitch.
        :rtype: fluvel.components.widgets.FSwitch
        """
        return self._create_widget(w.FSwitch, **kwargs)

    def RadioButton(self, **kwargs: Unpack[w.FRadioButtonKwargs]) -> w.FRadioButton:
        """
        Creates and instantiates a radio button component (:class:`~fluvel.components.widgets.FRadioButton`)  
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QRadioButton` that implements the Fluvel
        styling engine and support for internationalization.

        :param text: Text to display next to the radio button.
        :type text: str | I18nTextVar
        :param checkable: If ``True`` (default), the button can be toggled by the user.
        :type checkable: bool
        :param checked: If ``True``, the radio button is initially selected.
        :type checked: bool
        :param icon: Icon to display next to the text.
        :type icon: QIcon
        :param icon_size: Size (width, height) of the icon in pixels.
        :type icon_size: tuple[int, int]
        :param on_click: Callback ``Callable[[], None]`` executed when the button is clicked.
        :type on_click: Callable
        :param on_pressed: Callback ``Callable[[], None]`` executed when the button is pressed down.
        :type on_pressed: Callable
        :param on_released: Callback ``Callable[[], None]`` executed when the button is released.
        :type on_released: Callable
        :param on_toggled: Callback ``Callable[[bool], None]`` executed when the checked state changes.
        :type on_toggled: Callable
        :return: A configured instance of FRadioButton.
        :rtype: fluvel.components.widgets.FRadioButton
        """
        return self._create_widget(w.FRadioButton, **kwargs)

    def Input(self, **kwargs: Unpack[w.FInputKwargs]) -> w.FInput:
        """
        Creates and instantiates an input component (:class:`~fluvel.components.widgets.FInput`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QLineEdit` that implements the Fluvel
        styling engine and support for internationalization.

        :param text: Text content of the input.
        :type text: str | I18nTextVar
        :param placeholder: Placeholder text shown when the input is empty.
        :type placeholder: str | I18nTextVar
        :param align: Alignment of the text within the input.
        :type align: AlignmentTypes
        :param frame: If ``True`` (default), the input frame is drawn.
        :type frame: bool
        :param mode: How the text is displayed (e.g., normal, password).
        :type mode: EchoModeTypes
        :param read_only: If ``True``, the user cannot edit the text.
        :type read_only: bool
        :param clear_button: If ``True``, shows a button to clear the input content.
        :type clear_button: bool
        :param max_length: Maximum number of characters allowed.
        :type max_length: int
        :param mask: Input mask to restrict character input (e.g., for phone numbers or dates).
        :type mask: str
        :param on_returns: Callback ``Callable[[], None]`` executed when the user presses Enter/Return.
        :type on_returns: Callable
        :param on_edit: Callback ``Callable[[str], None]`` executed when the text is edited by the user.
        :type on_edit: Callable
        :param on_finish: Callback ``Callable[[], None]`` executed when the input loses focus or Enter is pressed.
        :type on_finish: Callable
        :param on_text_changed: Callback ``Callable[[str], None]`` executed whenever the text changes (programmatically or by user).
        :type on_text_changed: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FInput`.
        :rtype: fluvel.components.widgets.FInput
        """
        return self._create_widget(w.FInput, **kwargs)

    def ProgressBar(self, **kwargs: Unpack[w.FProgressBarKwargs]) -> w.FProgressBar:
        """
        Creates and instantiates a progress bar component (:class:`~fluvel.components.widgets.FProgressBar`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QProgressBar` that implements the Fluvel
        styling engine and support for internationalization.

        :param align: Alignment of the percentage text.
        :type align: AlignmentTypes
        :param format: Format string for the percentage text (e.g., "%p%").
        :type format: str | list[str]
        :param inverted_appearance: If ``True``, the progress bar fills from right-to-left or top-to-bottom.
        :type inverted_appearance: bool
        :param range: Set the minimum and maximum values as a tuple (min, max).
        :type range: tuple[int, int]
        :param max: Maximum value of the progress bar.
        :type max: int
        :param min: Minimum value of the progress bar.
        :type min: int
        :param orientation: Direction of the progress bar (horizontal or vertical).
        :type orientation: OrientationTypes
        :param text_direction: Direction of the text display.
        :type text_direction: TextDirectionTypes
        :param text_visible: If ``True`` (default), the percentage text is displayed.
        :type text_visible: bool
        :param value: Current value of the progress bar.
        :type value: int
        :param on_changed: Callback ``Callable[[int], None]`` executed when the value changes.
        :type on_changed: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FProgressBar`.
        :rtype: fluvel.components.widgets.FProgressBar
        """
        return self._create_widget(w.FProgressBar, **kwargs)

    def Slider(self, **kwargs: Unpack[w.FSliderKwargs]) -> w.FSlider:
        """
        Creates and instantiates a slider component (:class:`~fluvel.components.widgets.FSlider`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QSlider` that implements the Fluvel
        styling engine and support for internationalization.

        :param inverted_appearance: If ``True``, the slider values are inverted.
        :type inverted_appearance: bool
        :param inverted_controls: If ``True``, mouse wheel and keyboard controls are inverted.
        :type inverted_controls: bool
        :param range: Set the minimum and maximum values as a tuple (min, max).
        :type range: tuple[int, int]
        :param max: Maximum value of the slider.
        :type max: int
        :param min: Minimum value of the slider.
        :type min: int
        :param orientation: Direction of the slider (horizontal or vertical).
        :type orientation: OrientationTypes
        :param page_step: Size of the page step.
        :type page_step: int
        :param single_step: Size of the single step.
        :type single_step: int
        :param slider_down: Indicates if the slider handle is currently pressed.
        :type slider_down: bool
        :param slider_position: Current position of the slider handle.
        :type slider_position: int
        :param tracking: If ``True`` (default), valueChanged is emitted while dragging.
        :type tracking: bool
        :param value: Current value of the slider.
        :type value: int
        :param tick_interval: Interval for tick marks.
        :type tick_interval: int
        :param tick_position: Position of the tick marks.
        :type tick_position: TickPositionTypes
        :param on_changed: Callback ``Callable[[int], None]`` executed when the value changes.
        :type on_changed: Callable
        :param on_range_changed: Callback ``Callable[[int, int], None]`` executed when the range changes.
        :type on_range_changed: Callable
        :param on_moved: Callback ``Callable[[int], None]`` executed when the slider handle is moved.
        :type on_moved: Callable
        :param on_released: Callback ``Callable[[], None]`` executed when the slider handle is released.
        :type on_released: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FSlider`.
        :rtype: fluvel.components.widgets.FSlider
        """
        return self._create_widget(w.FSlider, **kwargs)

    def InputArea(self, **kwargs: Unpack[w.FInputAreaKwargs]) -> w.FInputArea:
        """
        Creates and instantiates a text area component (:class:`~fluvel.components.widgets.FInputArea`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QTextEdit` that implements the Fluvel
        styling engine and support for internationalization.

        :param plain_text: Plain text content.
        :type plain_text: str | I18nTextVar
        :param placeholder: Placeholder text shown when empty.
        :type placeholder: str | I18nTextVar
        :param read_only: If ``True``, the user cannot edit the text.
        :type read_only: bool
        :param cursor_position: Position of the text cursor.
        :type cursor_position: int
        :param align: Alignment of the text within the area.
        :type align: AlignmentTypes
        :param on_text_changed: Callback ``Callable[[], None]`` executed when the text changes.
        :type on_text_changed: Callable
        :param on_selection_changed: Callback ``Callable[[], None]`` executed when text selection changes.
        :type on_selection_changed: Callable
        :param on_cursor_changed: Callback ``Callable[[], None]`` executed when cursor position changes.
        :type on_cursor_changed: Callable
        :param on_undo: Callback ``Callable[[bool], None]`` executed when undo state changes.
        :type on_undo: Callable
        :param on_redo: Callback ``Callable[[bool], None]`` executed when redo state changes.
        :type on_redo: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FInputArea`.
        :rtype: fluvel.components.widgets.FInputArea
        """
        return self._create_widget(w.FInputArea, **kwargs)

    def ComboBox(self, **kwargs: Unpack[w.FComboBoxKwargs]) -> w.FComboBox:
        """
        Creates and instantiates a combo box component (:class:`~fluvel.components.widgets.FComboBox`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QComboBox` that implements the Fluvel
        styling engine and support for internationalization.

        :param items: List of string items to populate the combo box.
        :type items: list[str]
        :param editable: If ``True``, the combo box can be edited by the user.
        :type editable: bool
        :param max_visible: Maximum number of items visible in the dropdown list.
        :type max_visible: int
        :param placeholder: Placeholder text shown when no item is selected.
        :type placeholder: str | I18nTextVar
        :param current_index: Index of the currently selected item.
        :type current_index: int
        :param current_text: Text of the currently selected item.
        :type current_text: str
        :param on_select: Callback ``Callable[[int], None]`` executed when the selected index changes.
        :type on_select: Callable
        :param on_text_change: Callback ``Callable[[str], None]`` executed when the current text changes.
        :type on_text_change: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FComboBox`.
        :rtype: fluvel.components.widgets.FComboBox
        """
        return self._create_widget(w.FComboBox, **kwargs)

    def Separator(self, **kwargs: Unpack[w.FSeparatorKwargs]) -> w.FSeparator:
        """
        Creates and instantiates a separator component (:class:`~fluvel.components.widgets.FSeparator`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QFrame` that implements the Fluvel
        styling engine and is configured as a horizontal or vertical line.

        :param orientation: Direction of the separator (horizontal or vertical).
        :type orientation: OrientationTypes
        :param shadow: Style of the line shadow (e.g., sunken, raised).
        :type shadow: ShadowTypes
        :param thickness: Width or height of the separator line in pixels.
        :type thickness: int
        :return: A configured instance of :class:`~fluvel.components.widgets.FSeparator`.
        :rtype: fluvel.components.widgets.FSeparator
        """
        return self._create_widget(w.FSeparator, **kwargs)

    def Image(self, **kwargs: Unpack[w.FImageKwargs]) -> w.FImage:
        """
        Creates and instantiates a responsive image component (:class:`~fluvel.components.widgets.FImage`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QFrame` that dynamically draws an image,
        allowing resizing, maintaining high-quality antialiasing, and applying rounded corners.

        :param source: Image source, can be a file path (str), :class:`QPixmap`, or :class:`QImage`.
        :type source: str | QPixmap | QImage
        :param size: Fixed size of the component (int for square, tuple for width, height).
        :type size: int | tuple[int, int]
        :param rounded: Corner radius percentage (0-100) for rounding the image corners.
        :type rounded: int
        :param keep_aspect_ratio: If ``True`` (default), the image maintains its aspect ratio while scaling.
        :type keep_aspect_ratio: bool
        :param bg_color: Background color for the image container (e.g., CSS color string).
        :type bg_color: str
        :return: A configured instance of :class:`~fluvel.components.widgets.FImage`.
        :rtype: fluvel.components.widgets.FImage
        """
        return self._create_widget(w.FImage, **kwargs)

    def Icon(self, **kwargs: Unpack[w.FIconKwargs]) -> w.FIcon:
        """
        Creates and instantiates an icon component (:class:`~fluvel.components.widgets.FIcon`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QWidget` that dynamically renders a :class:`QIcon`,
        allowing resizing and applying rounded corners using `QPainter`.

        :param source: Icon source, can be a file path (str) or a :class:`QIcon`.
        :type source: str | QIcon
        :param size: Fixed width and height of the component in pixels.
        :type size: int
        :param rounded: Corner radius percentage (0-100) for rounding the icon corners.
        :type rounded: int
        :return: A configured instance of :class:`~fluvel.components.widgets.FIcon`.
        :rtype: fluvel.components.widgets.FIcon
        """
        return self._create_widget(w.FIcon, **kwargs)

    def IntBox(self, **kwargs: Unpack[w.FIntBoxKwargs]) -> w.FIntBox:
        """
        Creates and instantiates an integer input component (:class:`~fluvel.components.widgets.FIntBox`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QSpinBox` that implements the Fluvel
        styling engine and support for internationalization.

        :param value: Current integer value.
        :type value: int
        :param min: Minimum allowed value.
        :type min: int
        :param max: Maximum allowed value.
        :type max: int
        :param range: Set the minimum and maximum values as a tuple (min, max).
        :type range: tuple[int, int]
        :param prefix: String to display before the number (e.g., "$").
        :type prefix: str
        :param suffix: String to display after the number (e.g., " px").
        :type suffix: str
        :param step: Step size for increments/decrements.
        :type step: int
        :param step_type: Type of stepping (e.g., adaptive, default).
        :type step_type: StepTypes
        :param base: Base for integer display (e.g., 10 for decimal, 16 for hex).
        :type base: int
        :param align: Alignment of the text within the input.
        :type align: AlignmentTypes
        :param on_text_changed: Callback ``Callable[[str], None]`` executed when text changes (includes prefix/suffix).
        :type on_text_changed: Callable
        :param on_value_changed: Callback ``Callable[[int], None]`` executed when the integer value changes.
        :type on_value_changed: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FIntBox`.
        :rtype: fluvel.components.widgets.FIntBox
        """
        return self._create_widget(w.FIntBox, **kwargs)

    def DecimalBox(self, **kwargs: Unpack[w.FDecimalBoxKwargs]) -> w.FDecimalBox:
        """
        Creates and instantiates a decimal input component (:class:`~fluvel.components.widgets.FDecimalBox`) 
        within the current context.

        Wrapper of :class:`PySide6.QtWidgets.QDoubleSpinBox` that implements the Fluvel
        styling engine and support for internationalization.

        :param value: Current decimal value.
        :type value: float
        :param min: Minimum allowed value.
        :type min: float
        :param max: Maximum allowed value.
        :type max: float
        :param range: Set the minimum and maximum values as a tuple (min, max).
        :type range: tuple[float, float]
        :param prefix: String to display before the number (e.g., "$").
        :type prefix: str
        :param suffix: String to display after the number (e.g., " kg").
        :type suffix: str
        :param step: Step size for increments/decrements.
        :type step: float
        :param step_type: Type of stepping (e.g., adaptive, default).
        :type step_type: StepTypes
        :param decimals: Number of decimal places to display.
        :type decimals: int
        :param align: Alignment of the text within the input.
        :type align: AlignmentTypes
        :param on_text_changed: Callback ``Callable[[str], None]`` executed when text changes (includes prefix/suffix).
        :type on_text_changed: Callable
        :param on_value_changed: Callback ``Callable[[float], None]`` executed when the decimal value changes.
        :type on_value_changed: Callable
        :return: A configured instance of :class:`~fluvel.components.widgets.FDecimalBox`.
        :rtype: fluvel.components.widgets.FDecimalBox
        """
        return self._create_widget(w.FDecimalBox, **kwargs)

    def Link(self, **kwargs: Unpack[w.FLinkButtonKwargs]) -> w.FLinkButton:
        """
        Creates and instantiates a link button component (:class:`~fluvel.components.widgets.FLinkButton`) 
        within the current context.

        Wrapper of :class:`~fluvel.components.widgets.FButton` that opens a specified
        URL in the system's default browser when clicked.

        :param url: The web address (URL) to open.
        :type url: str
        :param text: Text to display on the button (e.g., the link name).
        :type text: str | I18nTextVar
        :param icon: Optional icon to display next to the text.
        :type icon: QIcon
        :param checkable: If ``True``, the button can be toggled.
        :type checkable: bool
        :return: A configured instance of :class:`~fluvel.components.widgets.FLinkButton`.
        :rtype: fluvel.components.widgets.FLinkButton
        """
        return self._create_widget(w.FLinkButton, **kwargs)