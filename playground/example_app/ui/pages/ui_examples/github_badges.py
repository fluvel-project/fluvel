"""
Example Module: GitHub-Style Badges (Advanced Composition)

This module illustrates Fluvel's potential for modelling visually complex designs
(such as the status badges commonly seen on GitHub) in an
extremely easy, intuitive, and robust manner.

It demonstrates the key principles of Fluvel's architecture:
--------------------------------------------------------------
1.  Composition Pattern (@Prefab): Use of nested components (RowBadges calls Badge)
    to encapsulate layout, iteration, and styling logic. This promotes
    reusability and separation of responsibilities.
2.  Declarative Programming: The final canvas (github-badges-example) focuses solely on
    the data structure (the BADGES list) and the placement of the final component,
    without worrying about how each individual badge is rendered.
3.  Hybrid Styling System: Demonstrates the powerful combination of predefined classes
    (such as "bg-zinc-200" or "font-bold") with the QSS preprocessor for fine-grained styling
    (e.g., "br-left[5px]", "m-0", "p-1").
"""

import fluvel as fl


@fl.Prefab
def Badge(canvas: fl.Canvas, title: str, description: str, color: str) -> fl.Canvas:

    with canvas.Horizontal() as h:
        h.adjust(spacing=0, margins=0, alignment="center")

        h.Label(
            text=title,
            style="bg-gray-500 m[0px] p[2px] fg[white] br-l[5px]",
            alignment="right",
        )
        h.Label(
            text=description,
            style=f"bg-{color}-400 m-0 p-1 fg[white] br-r[5px]",
            alignment="left",
        )

    return canvas


@fl.Prefab
def RowOfBadges(canvas: fl.Canvas, badges: list[tuple[str, str, str]]) -> fl.Canvas:

    with canvas.Horizontal() as h:
        for title, description, color in badges:
            # Create and insert each Badge
            h.add(Badge(title=title, description=description, color=color))

    return canvas


@fl.route("/github-badges")
class GHubBadges(fl.Page):
    def build(self):
        with self.Vertical(style="bg-slate-200") as v:
            v.adjust(spacing=10, alignment="center")

            # Data
            BADGES = [
                ("licence", "MIT", "lime"),
                ("python", "3.10+", "blue"),
                ("pypi", "v1.4.0", "blue"),
                ("codecov", "75%", "orange"),
                ("status", "stable", "lime"),
                ("architecture", "MVVM", "purple"),
            ]

            # Example title with advanced text styles
            v.Label(text="Github Badges", style="text-3xl font-bold", align="center",)

            # High-level component (RowOfBadges), passing data
            v.add(RowOfBadges(badges=BADGES))
        