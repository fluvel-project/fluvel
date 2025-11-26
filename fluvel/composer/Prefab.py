import functools
from typing import TypeVar, Callable, Any

# Fluvel
from fluvel.components.widgets.FContainer import FContainer
from fluvel.core.abstract_models.LayoutBuilder import LayoutBuilder

class Canvas(FContainer, LayoutBuilder):
    """
    It represents the drawing area or base container for building composite or custom UI components.

    Canvas inherits the following functionalities:

    * :py:class:`~fluvel.components.widgets.FContainer`: To act as a widget container.
    * :py:class:`~fluvel.core.abstract_models.LayoutBuilder`: To provide layout management methods (Vertical, Horizontal, Label, etc.)

    This class is the primary argument of functions decorated with :py:func:`~fluvel.composer.Prefab`.    
    """
    pass

TFunc = TypeVar('TFunc', bound=Callable[..., Any])

def Prefab(func: TFunc) -> TFunc:
    """
    A decorator that turns a Python function into a **reusable UI component (a "Prefab")**.

    This pattern encapsulates layout logic and widget 
    composition within a function to create a *complex component* 
    that can be easily included in any other layout.

    The decorated function automatically receives an instance of `~fluvel.composer.Canvas` 
    as its first argument (although this isn't required when calling it, as the decorator provides it) 
    and should return the modified instance of `~fluvel.composer.Canvas`.

    The signature of the decorated function should be:
    `def ComponentName(canvas: Canvas, **kwargs) -> Canvas:`

    :param func: The function that defines the component's layout and widgets.
    :type func: :py:data:`~fluvel.composer.TFunc`

    :returns: The decorated function (:code:`decorator`), which, when called, executes
              the component's logic and returns a constructed :py:class:`~fluvel.composer.Canvas`,
              ready to be added to another layout.
    :rtype: :py:data:`~fluvel.composer.TFunc`

    .. warning::
        The decorated function **MUST** return the :py:class:`~fluvel.composer.Canvas` object
        at the end of its execution so that it can be correctly embedded in the
        parent layout.

    Example 
    ------- 
        .. code-block:: python 

            from fluvel import Page, route 
            from fluvel.composer import Prefab, Canvas 

            @Prefab 
            def Note(canvas: Canvas, message: str | list): 
            
                # Defines a component with a title and a message 
                with canvas.Vertical(style="border-1 border-gray-300 p-4") as v: 

                    v.Label(text="Note", style="font-bold text-lg") 

                    v.Label(text=message, word_wrap=True) 

                return canvas # IMPORTANT! Return the modified Canvas

            # In your pages (or any other LayoutBuilder)
            @route("example")
            class ExamplePage(Page):
            
                def build_ui(self):
                
                    with self.Vertical(spacing=10) as v:

                        v.Label(text="My Application")

                        # Direct call to the Prefab function as if it were a widget
                        v.Prefab(Note(message="This is a reusable notification component."))

                        v.Label(text="End of content.")
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        
        canvas = Canvas()
        
        return func(canvas, *args, **kwargs)
        
    return decorator