"""The kinematics equations of a particle and of an edge.

`kinematics_equations` writes the definitions, which hold for any
motion, in the old physics code's order: every edge's Δt, then the
book's 2.2 for each edge and axis, then 2.4.

`constant_acceleration_equations` writes the book's 2.10 for one edge:
the constant-acceleration assumption. An example that adds each edge's
2.10 right after the kinematics has the old code's order, so the core's
automatic labels stay as they were.
"""

from typing import TYPE_CHECKING, cast

import sympy as sp

from equarium.physics.axes import Axes

if TYPE_CHECKING:
    from equarium.physics.particles import Edge, Particle


def kinematics_equations[A: Axes](particle: Particle[A]) -> list[sp.Eq]:
    """`m01.dt = m1.t - m0.t` for each edge, then, for each edge and axis:

    - 2.2, `m01.v_av.x = (m1.pos.x - m0.pos.x)/m01.dt`, the average
      velocity over the edge;
    - 2.4, `m01.a.x = (m1.vel.x - m0.vel.x)/m01.dt`, the average
      acceleration over the edge, which holds for any motion.
    """
    edges = particle.edges
    eqs: list[sp.Eq] = []
    for e in edges:
        eqs.append(cast(sp.Eq, sp.Eq(e.dt, e.end.t - e.start.t)))
    for e in edges:
        for v_av, x0, x1 in zip(
            e.v_av.components, e.start.pos.components, e.end.pos.components
        ):
            eqs.append(cast(sp.Eq, sp.Eq(v_av, (x1 - x0) / e.dt)))
    for e in edges:
        for a, v0, v1 in zip(e.a.components, e.start.vel.components, e.end.vel.components):
            eqs.append(cast(sp.Eq, sp.Eq(a, (v1 - v0) / e.dt)))
    return eqs


def constant_acceleration_equations[A: Axes](edge: Edge[A]) -> list[sp.Eq]:
    """For each axis of the edge, 2.10, `m01.v_av.x = (m0.vel.x + m1.vel.x)/2`,
    which holds only when the acceleration over the edge is constant."""
    return [
        cast(sp.Eq, sp.Eq(v_av, (v0 + v1) / 2))
        for v_av, v0, v1 in zip(
            edge.v_av.components, edge.start.vel.components, edge.end.vel.components
        )
    ]
