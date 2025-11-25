# Fluvel
from fluvel.components.gui import StyledText, StringVar

class FTextWidget:
    """
    Base class for text widgets that centralizes the management of static and dynamic content.

    The class is responsible for:

    1. Obtaining content through Fluvel methods (such as :py:class:`fluvel.components.gui.StyledText` 
    or an instance of :py:class:`fluvel.components.gui.StringVar`).
    2. Connecting dynamic content to the widget's update methods (e.g., ``setText``).
    3. Modifying and returning the ``kwargs`` so that the widget initializes with the correct value.
    """

    def get_static_text(self, **kwargs) -> dict[str, any]:
        """
        Processes and returns widget arguments to handle static and dynamic content.

        Searches for the "text" and "placeholder" keys to determine whether the content should be
        managed by a :py:class:`fluvel.components.gui.StringVar`.

        :param kwargs: Widget constructor arguments.
        :type kwargs: dict
        :returns: A dictionary with the processed arguments (e.g., "text" or "placeholder"
                        updated with the string variable value).
        :rtype: dict
        """

        if text := kwargs.get("text"):

            kwargs = self.get_string_var(text, "text", "setText", **kwargs)

        if placeholder := kwargs.get("placeholder"):

            kwargs = self.get_string_var(
                placeholder, "placeholder", "setPlaceholderText", **kwargs
            )

        if "textvariable" in kwargs:

            kwargs = self._is_text_variable(**kwargs)

        return kwargs

    def _is_text_variable(self, **kwargs) -> dict[str, any]:
        """
        Connects a directly provided StringVar (key "textvariable") to a widget.

        Removes the "textvariable" key from the kwargs and connects the ``valueChanged`` signal
        of the variable to the ``setText`` method of the widget.

        :param kwargs: Widget constructor arguments, including "textvariable".
        :type kwargs: dict
        :returns: Updated arguments without the "textvariable" key.
        :rtype: dict
        """

        string_var: StringVar = kwargs.pop("textvariable")

        string_var.valueChanged.connect(self.setText)

        kwargs["text"] = string_var.value

        return kwargs

    def get_string_var(self, _id: str, flag: str, method: str, **kwargs) -> None:
        """
        Gets a StringVar for a content ID and connects it to a widget method.

        This method handles both simple content IDs and lists containing an ID
        and placeholders for text replacement ( StyledText ).

        :param _id: The content ID (:py:class:`str`) or a list containing the ID and placeholders.
        :type _id: str | list
        :param flag: The key of the argument to be updated ("text" or "placeholder").
        :type flag: str
        :param method: The name of the widget method to connect to (e.g., "setText").
        :type method: str
        :param kwargs: Widget constructor arguments.
        :type kwargs: dict
        :returns: Updated arguments with the initial value of the StringVar or unchanged if ``_id`` is a simple string.
        :rtype: dict
        """

        if isinstance(_id, list):

            content_id, *markers = _id

            string_var: StringVar = StyledText(content_id, *markers).var

            string_var.valueChanged.connect(getattr(self, method))

            kwargs[flag] = string_var.value

        # Si es un texto simple (una instancia de str), no ocurre nada

        return kwargs
