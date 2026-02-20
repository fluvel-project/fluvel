"""
UI Composition Example: Predefined Color Palette
============================================================

This module exemplifies the construction of complex and visually rich interfaces
using Fluvel's declarative composition (@Component and @Prefab) together with
the utility style system (QSS).

It demonstrates:
1. Creation of stylized atomic components (@Component).
2. Encapsulation of complex layout logic in reusable modules (@Prefab).
3. Advanced use of Grid Layouts and the .adjust() method for dimension control.
4. Application of dynamic styles through f-strings (e.g., bg-color-weight).
"""

from typing import Literal

from fluvel import Page, route
from fluvel.composer import Canvas, Component, Prefab

# Definition of types for predefined qss colors
ColorName = Literal[
    "slate",
    "gray",
    "zinc",
    "neutral",
    "stone",
    "red",
    "orange",
    "amber",
    "yellow",
    "lime",
    "green",
    "emerald",
    "teal",
    "cyan",
    "blue",
    "sky",
    "violet",
    "purple",
    "fuchsia",
    "pink",
]


@Component("FLabel")
def ColorLabel(color: str, bg_weight: int):
    """
    Atomic Component component for a single color sample.

    Generates an empty FLabel and applies a dynamic background class
    based on color and weight (e.g., "g-red-500").

    :param color: Base name of the color (e.g., "red", "blue").
    :type color: ColorName
    :param bg_weight: Color weight (e.g., 100, 500, 900).
    :type bg_weight: int
    :returns: A dictionary of arguments to initialize FLabel.
    :rtype: dict
    """

    return {"text": "", "style": f"bg-{color}-{bg_weight} rounded-md"}


@Component("FLabel")
def Label(text: str):
    """
    Factory component to standardize the appearance of palette titles.
    """

    return {"text": text, "style": "text-lg font-light"}


@Prefab
def Palette(canvas: Canvas, color: ColorName):
    """
    Prefab component that builds a palette of 10 shades for a single color.

    Uses a Grid Layout to organize the 10 samples in a 3x4 arrangement.

    :param canvas: the Canvas instance to compose the user interface
    :type canvas: Canvas

    :param color: The base color of the palette to be built.
    :type color: ColorName

    :returns: the Canvas instance with the built design.
    :rtype: Canvas
    """

    with canvas.Grid() as grid:
        grid.adjust(min_width=125)

        c1, c2, c3 = grid.Columns(3)

        c1.add(Label(color.capitalize()), column_span=3)

        c1.add(ColorLabel(color, 100))
        c1.add(ColorLabel(color, 200))
        c1.add(ColorLabel(color, 300))

        c2.add(ColorLabel(color, 400))
        c2.add(ColorLabel(color, 500))
        c2.add(ColorLabel(color, 600))

        c3.add(ColorLabel(color, 700))
        c3.add(ColorLabel(color, 800))
        c3.add(ColorLabel(color, 900))

        c1.add(ColorLabel(color, 1000), column_span=3)

    return canvas


@Prefab
def ColorScaleBar(canvas: Canvas, color: ColorName) -> Canvas:
    """
    Prefab component that creates a solid vertical bar with a single color scale.

    :param canvas: the Canvas instance to compose the user interface
    :type canvas: Canvas

    :param color: The base color of the bar.
    :type color: ColorName

    :returns: the Canvas instance with the built design.
    :rtype: Canvas
    """

    with canvas.Vertical() as v:
        v.adjust(spacing=0, fixed_width=300)

        for i in range(1, 11):
            lbl = v.Label(style=f"bg-{color}-{i * 100} m-0")

            match i:
                case 1:
                    lbl.configure(style="rounded-t-2xl")
                case 10:
                    lbl.configure(style="rounded-b-2xl")

    return canvas


@Prefab
def GridOfPalettes(canvas: Canvas):
    """
    Prefab component that organizes twenty (20) instances of the Prefab Palette in a 5-column Grid Layout.
    This Prefab acts as the grid's main container, applying background styles and padding to the entire layout.

    :param canvas: the Canvas instance to compose the user interface
    :type canvas: Canvas

    :returns: the Canvas instance with the built design.
    :rtype: Canvas
    """

    with canvas.Grid(style="bg-zinc-200 rounded-4xl") as grid:
        grid.adjust(margins=(20, 20, 20, 20))

        c1, c2, c3, c4, c5 = grid.Columns(5)

        c1.add(Palette(color="slate"))
        c1.add(Palette(color="gray"))
        c1.add(Palette(color="zinc"))
        c1.add(Palette(color="neutral"))

        c2.add(Palette(color="stone"))
        c2.add(Palette(color="red"))
        c2.add(Palette(color="orange"))
        c2.add(Palette(color="amber"))

        c3.add(Palette(color="yellow"))
        c3.add(Palette(color="lime"))
        c3.add(Palette(color="green"))
        c3.add(Palette(color="emerald"))

        c4.add(Palette(color="teal"))
        c4.add(Palette(color="cyan"))
        c4.add(Palette(color="blue"))
        c4.add(Palette(color="sky"))

        c5.add(Palette(color="violet"))
        c5.add(Palette(color="purple"))
        c5.add(Palette(color="fuchsia"))
        c5.add(Palette(color="pink"))

    return canvas


@route("color-palette")
class ColorPaletteDemo(Page):
    """
    Main page comprising the different palettes and color bars.
    """

    def build(self):
        """
        Method of constructing the interface.
        """

        with self.Horizontal(style="bg-stone-300") as hbody:
            hbody.add(ColorScaleBar(color="lime"))

            hbody.add(GridOfPalettes)