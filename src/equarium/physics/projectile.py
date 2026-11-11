"""The projectile setup: what projectile motion adds to an `XY` edge's
kinematics, with y up. Gravity is the only acceleration, so `a.y = -g`,
the horizontal velocity doesn't change, `v0x = v1x`, and `a.x` is zero.

`d01.projectile(g)` returns a `Setup`, the equations and the knowns, and
the example adds both. The origin and the clock stay the example's.
"""

from collections.abc import Mapping
from typing import TYPE_CHECKING, NamedTuple, cast

import sympy as sp

from equarium.errors import UsageError
from equarium.physics.axes import XY

if TYPE_CHECKING:
    from equarium.physics.particles import Edge


class Setup(NamedTuple):
    """Equations and knowns that go into a system together:
    `.add(*flight.equations).known(flight.knowns)`."""

    equations: list[sp.Eq]
    knowns: Mapping[sp.Symbol, sp.Expr]


def projectile_setup(edge: Edge[XY], g: sp.Expr) -> Setup:
    """`d01.a.y = -g` and `d0.vel.x = d1.vel.x`, with `d01.a.x` known
    zero."""
    if edge.axes.names != XY.names:
        raise UsageError(
            f"{edge.owner}{edge.where} is in {edge.axes.__name__},"
            " so it has no projectile setup"
        )
    return Setup(
        equations=[
            cast(sp.Eq, sp.Eq(edge.a.y, -g)),
            cast(sp.Eq, sp.Eq(edge.start.vel.x, edge.end.vel.x)),
        ],
        knowns={edge.a.x: sp.S.Zero},
    )
