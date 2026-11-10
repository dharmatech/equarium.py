"""Newton's second law on an edge, ΣF = m a: one equation per axis, with
the particle's mass, `b.mass`, and the edge's acceleration, `b01.a`.

The acceleration is the one the kinematics equations have. So a system
with both, such as Example 4.5's, needs no equation to link Newton's
acceleration to the kinematics'. `b01.newton(n, w, f)` calls this.
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING

import sympy as sp

from equarium.errors import UsageError
from equarium.physics.axes import Axes
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vec, Vector, describe

if TYPE_CHECKING:
    from equarium.physics.particles import Edge


def mass_of(owner: str) -> Var:
    """The mass of the particle named `owner`, `b.mass`."""
    return Var(owner, "", "mass")


def newton_equations[A: Axes](edge: Edge[A], forces: Sequence[Vector[A] | Vec[A]]) -> list[sp.Eq]:
    """`f.x + n.x + w.x = b.mass*b01.a.x`, for each axis of the edge: the
    forces' sum equals the particle's mass times the edge's acceleration."""
    name = edge.owner + edge.where
    call = f"{name}.newton({', '.join(describe(force) for force in forces)})"
    if not forces:
        raise UsageError(f"{call} needs one or more forces")
    for force in forces:
        if not isinstance(force, Vector | Vec):
            raise UsageError(f"{call}: {describe(force)} isn't a vector")
        if force.axes is not edge.axes:
            raise UsageError(
                f"{call}: {name} is in {edge.axes.__name__},"
                f" but {describe(force)} is in {force.axes.__name__}"
            )
    total = sum(forces[1:], start=forces[0])
    return total.eq(edge.a * mass_of(edge.owner))
