from typing import Unpack

# Fluvel Widgets
from fluvel.components.widgets.FLabel import FLabel, FLabelKwargs
from fluvel.components.widgets.FButton import FButton, FButtonKwargs
from fluvel.components.widgets.FInput import FInput, FInputKwargs
from fluvel.components.widgets.FCheckBox import FCheckBox, FCheckBoxKwargs
from fluvel.components.widgets.FRadioButton import FRadioButton, FRadioButtonKwargs
from fluvel.components.widgets.FCircleButton import FCircleButton, FCircleButtonKwargs
from fluvel.components.widgets.FSwitch import FSwitch, FSwitchKwargs
from fluvel.components.widgets.FProgressBar import FProgressBar, FProgressBarKwargs
from fluvel.components.widgets.FSlider import FSlider, FSliderKwargs

class FLayoutAPI:

    def Label(self, **kwargs: Unpack[FLabelKwargs]) -> FLabel:
        """
        Creates and adds a SKLabel widget to the layout.
    
        This method creates a new instance of :py:class:`~fluvel.components.widgets.FLabel`
        based on the key arguments provided.
    
        :param text: The text to display on the label. Can be a string or a list
                     for i18n lookup.
        :type text: str | Stringvar | list[str]
        :param style: A string of space-separated QSS class names to apply to the label.
        :type style: str
        :param content_align: The alignment of the label's text.
        :type content_align: str
        
        .. seealso::
            :py:class:`~fluvel.components.widgets.FLabel` for all available parameters
            and signals.

        :returns: The created :class:`~fluvel.components.widgets.FLabel` instance.
        :rtype: FLabel
    
        Example
        -------
        .. code-block:: python
            ...
            with self.Vertical() as v:
                # Creates a new label
                my_label = v.Label(text="Hello!", style="text-2xl font-bold")
        """
        
        return self._create_widget(FLabel, **kwargs)

    def Button(self, **kwargs: Unpack[FButtonKwargs]) -> FButton:
        
        return self._create_widget(FButton, **kwargs)
    
    def CircleButton(self, **kwargs: Unpack[FCircleButtonKwargs]) -> FCircleButton:
        
        return self._create_widget(FCircleButton, **kwargs)
    
    def Switch(self, **kwargs: Unpack[FSwitchKwargs]) -> FSwitch:
        
        return self._create_widget(FSwitch, **kwargs)

    def Input(self, **kwargs: Unpack[FInputKwargs]) -> FInput:
        
        return self._create_widget(FInput, **kwargs)
    
    def CheckBox(self, **kwargs: Unpack[FCheckBoxKwargs]) -> FCheckBox:

        return self._create_widget(FCheckBox, **kwargs)
    
    def RadioButton(self, **kwargs: Unpack[FRadioButtonKwargs]) -> FRadioButton:
        
        return self._create_widget(FRadioButton, **kwargs)
    
    def ProgressBar(self, **kwargs: Unpack[FProgressBarKwargs]) -> FProgressBar:
        
        return self._create_widget(FProgressBar, **kwargs)
    
    def Slider(self, **kwargs: Unpack[FSliderKwargs]) -> FSlider:
        
        return self._create_widget(FSlider, **kwargs)