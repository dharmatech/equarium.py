"""`BookNotation`, a display hook that prints the book's notation.

The debug form is the symbol's name, `m0.pos.x`, with the core's default
hook. The book's form is for reading: `x0`, `v0x`, `ax`, `Δt`.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

import sympy as sp

from equarium.analysis import Role
from equarium.display import GREEN, RED, RESET
from equarium.physics.symbols import Var

AXES = ("x", "y")


@dataclass(frozen=True)
class BookNotation:
    """The book's notation as plain text, glued, as the book's text reads,
    in the book's order: letter, owner, state, axis.

    - `owners` maps an owner's name to the book's subscript for it, such
      as `{"m": "M", "p": "P"}`, so `p0.vel.x` prints `vP0x`. An owner
      not in it gets none.
    - `edge_index` prints an edge's states, `Δt01` and `a01x`, for
      problems with several edges.
    - `color` colors knowns green and wants red, as the core's
      `display.terminal` does.

    A plain symbol, and a `Var` the notation doesn't know, print their
    names. The book's form can be ambiguous: two owners without
    subscripts both print `x0`.
    """

    owners: Mapping[str, str] = field(default_factory=dict[str, str])
    edge_index: bool = False
    color: bool = True

    def text(self, symbol: sp.Symbol) -> str:
        """The book's form, without color."""
        if not isinstance(symbol, Var) or not symbol.where.isdigit():
            return symbol.name
        who = self.owners.get(symbol.owner, "")
        where = symbol.where
        if len(where) == 1:  # a state
            match symbol.path:
                case ("pos", axis) if axis in AXES:
                    return f"{axis}{who}{where}"
                case ("vel", axis) if axis in AXES:
                    return f"v{who}{where}{axis}"
                case ("t",):
                    return f"t{who}{where}"
                case _:
                    pass
        elif len(where) == 2:  # an edge
            index = where if self.edge_index else ""
            match symbol.path:
                case ("dt",):
                    return f"Δt{who}{index}"
                case ("a", axis) if axis in AXES:
                    return f"a{who}{index}{axis}"
                case ("v_av", axis) if axis in AXES:
                    return f"vav{who}{index}{axis}"
                case _:
                    pass
        return symbol.name

    def __call__(self, symbol: sp.Symbol, role: Role) -> str:
        """The book's form, knowns green, wants red, other unknowns plain."""
        text = self.text(symbol)
        if not self.color:
            return text
        match role:
            case Role.KNOWN:
                return f"{GREEN}{text}{RESET}"
            case Role.WANT:
                return f"{RED}{text}{RESET}"
            case Role.UNKNOWN:
                return text
