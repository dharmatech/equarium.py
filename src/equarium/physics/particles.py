"""`Particle`, its `State`s and the `Edge`s between them.

All three are frozen dataclasses, equal by value. They hold names, never
symbols: states, edges, vectors and symbols are made on demand. So
`Particle("m", 2, X)` made twice is the same particle, with the same
symbols.
"""

from dataclasses import dataclass

import sympy as sp

from equarium.errors import UsageError
from equarium.physics.axes import XY, Axes
from equarium.physics.kinematics import kinematics_equations
from equarium.physics.newton import mass_of, newton_equations
from equarium.physics.projectile import Setup, projectile_setup
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vec, Vector

MAX_STATES = 10  # the most that keeps an edge's `m01` unambiguous


@dataclass(frozen=True)
class State[A: Axes]:
    """One instant of a particle: its position, velocity and time,
    `m0.pos`, `m0.vel` and `m0.t`."""

    owner: str
    index: int
    axes: type[A]

    @property
    def where(self) -> str:
        """The index, `"0"`."""
        return str(self.index)

    @property
    def pos(self) -> Vector[A]:
        return Vector(self.owner, self.axes, self.where, ("pos",))

    @property
    def vel(self) -> Vector[A]:
        return Vector(self.owner, self.axes, self.where, ("vel",))

    @property
    def t(self) -> Var:
        return Var(self.owner, self.where, "t")


@dataclass(frozen=True)
class Edge[A: Axes]:
    """The interval between two consecutive states: its time, average
    velocity and acceleration, `m01.dt`, `m01.v_av` and `m01.a`. An `XY`
    edge also has the projectile setup, `m01.projectile(g)`. Newton's
    second law on an edge is `m01.newton(n, w, f)`."""

    start: State[A]
    end: State[A]

    @property
    def owner(self) -> str:
        return self.start.owner

    @property
    def where(self) -> str:
        """The two indexes, `"01"`."""
        return self.start.where + self.end.where

    @property
    def axes(self) -> type[A]:
        return self.start.axes

    @property
    def dt(self) -> Var:
        return Var(self.owner, self.where, "dt")

    @property
    def a(self) -> Vector[A]:
        return Vector(self.owner, self.axes, self.where, ("a",))

    @property
    def v_av(self) -> Vector[A]:
        return Vector(self.owner, self.axes, self.where, ("v_av",))

    def projectile(self: Edge[XY], g: sp.Expr) -> Setup:
        """The projectile setup: `a.y = -g` and `v0x = v1x`, with `a.x`
        known zero."""
        return projectile_setup(self, g)

    def newton(self, *forces: Vector[A] | Vec[A]) -> list[sp.Eq]:
        """Newton's second law, ΣF = m a: for each axis, the forces' sum
        equals the particle's mass times this edge's acceleration."""
        return newton_equations(self, forces)


@dataclass(frozen=True, init=False)
class Particle[A: Axes]:
    """A particle with two to ten states in the axes `A`:
    `Particle("m", 2, X)`, with `m0, m1 = m.states` and
    `m01 = m.edge(0, 1)`.

    The name is a Python identifier that doesn't end in a digit, since
    `p2` with state 0 would print `p20.t`. Its mass is `m.mass`, which
    Newton's second law uses.
    """

    name: str
    count: int
    axes: type[A]

    def __init__(self, name: str, states: int, axes: type[A]) -> None:
        if not name.isidentifier() or name[-1].isdigit():
            raise UsageError(
                f"a particle's name is a Python identifier that doesn't end in a digit,"
                f" not {name!r}"
            )
        if not 2 <= states <= MAX_STATES:
            raise UsageError(f"a particle has 2 to {MAX_STATES} states, not {states}")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "count", states)
        object.__setattr__(self, "axes", axes)

    @property
    def states(self) -> tuple[State[A], ...]:
        return tuple(State(self.name, i, self.axes) for i in range(self.count))

    @property
    def edges(self) -> tuple[Edge[A], ...]:
        """One edge between each pair of consecutive states."""
        states = self.states
        return tuple(Edge(start, end) for start, end in zip(states, states[1:]))

    @property
    def mass(self) -> Var:
        """The particle's mass, `m.mass`."""
        return mass_of(self.name)

    def edge(self, i: int, j: int) -> Edge[A]:
        """The edge from state `i` to state `j`, which is `i + 1`."""
        if j != i + 1 or not (0 <= i and j < self.count):
            raise UsageError(
                f"{self.name} has edges between consecutive states 0 to {self.count - 1},"
                f" not from {i} to {j}"
            )
        return self.edges[i]

    def kinematics(self) -> list[sp.Eq]:
        """Every edge's Δt, then the book's 2.2, 2.7 and 2.10 for each
        edge and axis."""
        return kinematics_equations(self)
