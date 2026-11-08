"""What a system's symbols are, and which equations are ready to solve."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

import sympy as sp

from equarium.sympy_compat import free_symbols

if TYPE_CHECKING:
    from equarium.system import System


class Role(Enum):
    KNOWN = auto()
    WANT = auto()
    UNKNOWN = auto()


@dataclass(frozen=True)
class Analysis:
    """A system's knowns, wants and unknowns.

    `connected` holds the unknowns linked to the wants through the
    equations, wants included. `ready` and `connected_labels` are in
    equation order.
    """

    knowns: frozenset[sp.Symbol]  # including those with no number
    wants: tuple[sp.Symbol, ...]
    connected: frozenset[sp.Symbol]
    others: frozenset[sp.Symbol]  # the rest of the unknowns
    ready: tuple[str, ...]  # equations with exactly one unknown
    connected_labels: tuple[str, ...]  # equations with a connected unknown

    def role(self, sym: sp.Symbol) -> Role:
        if sym in self.knowns:
            return Role.KNOWN
        if sym in self.wants:
            return Role.WANT
        return Role.UNKNOWN


def analyze(system: System) -> Analysis:
    knowns = frozenset(system.knowns)
    unknowns = [
        (equation.label, free_symbols(equation.eq) - knowns)
        for equation in system.equations
    ]

    # Grow from the wants, as the old connected_unknowns did.
    connected = frozenset(system.wants)
    changed = True
    while changed:
        changed = False
        for _, syms in unknowns:
            if syms & connected and not syms <= connected:
                connected |= syms
                changed = True

    every_unknown = frozenset[sp.Symbol]().union(*(syms for _, syms in unknowns))
    return Analysis(
        knowns=knowns,
        wants=system.wants,
        connected=connected,
        others=every_unknown - connected,
        ready=tuple(label for label, syms in unknowns if len(syms) == 1),
        connected_labels=tuple(label for label, syms in unknowns if syms & connected),
    )
