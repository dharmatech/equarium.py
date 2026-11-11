"""`Event`, two or more states at the same time and place.

An event owns a time and a position, `meet.t` and `meet.pos`, as a state
does. Its links, each state's time and position equal to the event's,
stay equations: `meet.equations()` writes them, and the example adds
them to its system, so it can eliminate them by hand, as 2.5 step by
step does.
"""

from dataclasses import dataclass
from typing import cast

import sympy as sp

from equarium.display import TextPrinter
from equarium.errors import UsageError
from equarium.physics.axes import Axes
from equarium.physics.particles import State
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vector


@dataclass(frozen=True, init=False)
class Event[A: Axes]:
    """Two or more states in the axes `A`, at the same time and place:
    `Event("meet", m1, p1)`, with `meet.t` and `meet.pos`.

    It holds states, never symbols: an event made twice with one name
    has the same symbols. The name is a Python identifier that doesn't
    end in a digit, as a particle's is.
    """

    name: str
    states: tuple[State[A], ...]

    def __init__(self, name: str, *states: State[A]) -> None:
        if not name.isidentifier() or name[-1].isdigit():
            raise UsageError(
                f"an event's name is a Python identifier that doesn't end in a digit,"
                f" not {name!r}"
            )
        if len(states) < 2:
            raise UsageError(f"{name} needs two or more states, not {len(states)}")
        first = states[0]
        for state in states[1:]:
            if state.axes is not first.axes:
                raise UsageError(
                    f"{name}: {_name(first)} is in {first.axes.__name__},"
                    f" but {_name(state)} is in {state.axes.__name__}"
                )
        if len(set(states)) != len(states):
            raise UsageError(f"{name} has a state twice")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "states", states)

    @property
    def axes(self) -> type[A]:
        return self.states[0].axes

    @property
    def t(self) -> Var:
        return Var(self.name, "", "t")

    @property
    def pos(self) -> Vector[A]:
        return Vector(self.name, self.axes, "", ("pos",))

    def equations(self, axes: type[Axes] | None = None) -> list[sp.Eq]:
        """The links: each state's time equals the event's, then, for
        each axis of `axes`, each state's position equals the event's.
        `axes` defaults to the event's."""
        return event_equations(self, axes)

    def _repr_pretty_(self, p: TextPrinter, cycle: bool) -> None:
        """The event as IPython, and transcript mode, print it: its
        states, `event meet: m1, p1`."""
        p.text(f"event {self.name}: {', '.join(_name(state) for state in self.states)}")


def event_equations[A: Axes](event: Event[A], axes: type[Axes] | None = None) -> list[sp.Eq]:
    """`event.equations(axes)`: the times, in the states' order, then the
    positions, axis by axis, in `axes.names` order."""
    names = event.axes.names
    chosen = names if axes is None else axes.names
    for axis in chosen:
        if axis not in names:
            raise UsageError(f"{event.name} is in {event.axes.__name__}, so it has no {axis}")
    equations = [cast(sp.Eq, sp.Eq(state.t, event.t)) for state in event.states]
    for axis in chosen:
        i = names.index(axis)
        at = event.pos.components[i]
        equations += [cast(sp.Eq, sp.Eq(s.pos.components[i], at)) for s in event.states]
    return equations


def _name[A: Axes](state: State[A]) -> str:
    """How a state reads in a message, `m1`."""
    return state.owner + state.where
