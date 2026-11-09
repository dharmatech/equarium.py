"""A 2-axis vector's polar form, one way each: `from_polar` gives the
components from the magnitude and the angle, and `to_polar` the magnitude
and the angle from the components.

Two-way polar is both, added together. The methods `v.from_polar()` and
`v.to_polar()` call these.
"""

from typing import TYPE_CHECKING, cast

import sympy as sp

from equarium.physics.axes import XY

if TYPE_CHECKING:
    from equarium.physics.vectors import Vector


def from_polar(v: Vector[XY]) -> list[sp.Eq]:
    """`v.x = v.mag*cos(v.angle)`, `v.y = v.mag*sin(v.angle)`."""
    return [
        cast(sp.Eq, sp.Eq(v.x, v.mag * sp.cos(v.angle))),
        cast(sp.Eq, sp.Eq(v.y, v.mag * sp.sin(v.angle))),
    ]


def to_polar(v: Vector[XY]) -> list[sp.Eq]:
    """`v.mag = sqrt(v.x**2 + v.y**2)`, `v.angle = atan2(v.y, v.x)`."""
    return [
        cast(sp.Eq, sp.Eq(v.mag, sp.sqrt(v.x**2 + v.y**2))),
        cast(sp.Eq, sp.Eq(v.angle, sp.atan2(v.y, v.x))),
    ]
