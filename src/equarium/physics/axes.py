"""The dimension of a model, as a type: `X`, `Y` or `XY`.

An axes type is passed as the class, `Particle("m", 2, X)`, and the
particle, its states, edges and vectors are generic in it. So pyright
flags `m0.pos.y` in an `X` model. There is no `Z`.
"""

from typing import ClassVar


class Axes:
    """The base of the axes types. `names` are the axes, in order."""

    names: ClassVar[tuple[str, ...]]


class X(Axes):
    names = ("x",)


class Y(Axes):
    names = ("y",)


class XY(Axes):
    names = ("x", "y")
