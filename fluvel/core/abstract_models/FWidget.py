from typing import Any, List, TypedDict, Tuple

# Fluvel
from fluvel.src.QSSProcessor.qss_processor import QSSProcessor
from fluvel.core.enums import AlignmentTypes, SizePolicyTypes, SizePolicy, WidgetAttributeTypes, WidgetAttributes

# State Manager
from fluvel.core.State import State

class FWidgetKwargs(TypedDict, total=False):
    """
    Keyword arguments for configuring FWidget.

    Defines optional parameters that can be passed to :py:class:`~fluvel.core.abstract_modes.FWidget.FWidget`
    and its subclasses to configure styles, state bindings,
    size policies, and other widget attributes.
    """

    # F-Widgets Base
    bind        : str | List[str]
    style       : str

    # QtWidgets Base
    size_policy : SizePolicyTypes | Tuple[SizePolicyTypes, SizePolicyTypes]
    attributes  : List[WidgetAttributeTypes]

    # Layout
    alignment   : AlignmentTypes
    stretch     : str

class FWidget:
    """
    Base class for all Fluvel user interface components.

    Provides essential methods for initial configuration, style management
    (QSS), state binding, and internal object configuration, acting
    as an abstraction layer over PySide6 widgets.
    """

    def configure(self, **kwargs) -> None:
        """
        Configures the base widget by applying keyword arguments.

        This method processes arguments such as ``bind``, ``style``, ``size_policy``, and
        ``attributes`` defined in :py:class:`~fluvel.core.abstract_models.FWidget.FWidgetKwargs`, applying the
        corresponding settings through the internal methods of
        this class and PySide6. Unused arguments are returned.

        .. note::
            Layout-related arguments (such as ``alignment`` and ``stretch``)
            are left in ``kwargs`` to be processed by the layout manager
            containing this widget.

        :param kwargs: Dictionary of configuration arguments (FWidgetKwargs).
        :type kwargs: dict
        :returns: A dictionary with the remaining arguments (not consumed by FWidget).
        :rtype: dict
        """
        
        # Set Bindng
        if bind := kwargs.get("bind"):

            self.bind(bind)
            kwargs.pop("bind")
        
        if style := kwargs.get("style"):
            self.set_style(style)
            kwargs.pop("style")
        elif hasattr(self, "_BASE_STYLE"):
            self.set_style(self._BASE_STYLE)

        if size_policy := kwargs.get("size_policy"):

            self.setSizePolicy(SizePolicy.get(size_policy))
            kwargs.pop("size_policy")

        if attributes := kwargs.get("attributes"):
            for attr in attributes:
                attribute = WidgetAttributes.get(attr)
                self.setAttribute(attribute, True)
            kwargs.pop("attributes")

        return kwargs

    def set_style(self, style: str) -> None:
        """
        Applies QSS (Qt Style Sheet) styles to the component.

        The style is configured by setting the object's ``class`` property (to
        handle multiple classes) and then processing the entire style string through
        :py:class:`QSSProcessor` to apply the visual style using
        :py:meth:`PySide6.QtWidgets.QWidget.setStyleSheet`.

        :param style: String of QSS classes to apply.
        :type style: str
        :rtype: None
        """

        if _property := self.property("class"):
            full_style_string = "{} {}".format(style, _property)
        else:
            full_style_string = style

        self.setProperty("class", full_style_string)
        
        self.setStyleSheet(
            QSSProcessor.process(full_style_string, self.WIDGET_TYPE, self.obj_name)
        )

    def bind(self, binding_string: str) -> None:
        """
        Creates a binding between the widget and Fluvel's State Manager.

        Allows the widget's state to be automatically synchronized with one or more
        variables within the application's :py:class:`~fluvel.core.State.State` object.

        If ``binding_string`` is a list, it binds to each of the keys.

        :param binding_string: A string with the key or a list of keys to bind.
        :type binding_string: str or list[str]
        :rtype: None
        """

        if isinstance(binding_string, str):
            State.bind(self, binding_string)

        elif isinstance(binding_string, list):
            for b in binding_string:
                State.bind(self, b)

    def _fwidget_defaults(self) -> None:
        """
        Sets the internal default settings for :py:class:`FWidget`.

        Initializes the ``WIDGET_TYPE`` attribute with the class name (useful for
        :py:class:`~fluvel.src.qss_processor.QSSProcessor`), and sets a unique object name (``obj_name``)
        based on the memory ID to facilitate the application of instance-specific QSS styles.

        :rtype: None
        """

        self.WIDGET_TYPE: str = type(self).__name__

        # Estableciendo el nombre del objeto para
        # aplicar los estilos QSS
        self.obj_name: str = str(id(self))
        self.setObjectName(self.obj_name)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Allows configuration of the widget using dictionary syntax.

        Acts as a shortcut for the method :py:meth:`~fluvel.core.abstract_models.FWidget.FWidget.configure`.

        Example: ``widget["style"] = "bg-slate-100"`` is equivalent to
        ``widget.configure(style="bg-slate-100")``.

        :param key: The name of the parameter to configure (e.g., "style", "bind").
        :type key: str
        :param value: The value to assign to the parameter.
        :type value: Any
        :rtype: None
        """

        self.configure(**{key: value})