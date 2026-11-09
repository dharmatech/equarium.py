"""`Var`, the physics layer's symbol: a SymPy symbol whose identity is
its structure.

Its name is its access path: the owner and where, then the path, joined
by dots. `Var("m", "0", "pos", "x")` is `m0.pos.x`, and
`Var("m", "01", "a", "x")` is `m01.a.x`.
"""

from typing import Any, Self, SupportsIndex

import sympy as sp


class Var(sp.Symbol):
    """A symbol with three plain fields: `owner` (`"m"`), `where` (`""`, a
    state `"0"` or an edge `"01"`) and `path` (`("pos", "x")`).

    Two `Var`s are equal when their fields are. A plain
    `sp.Symbol("m0.pos.x")` is a different symbol, and so is
    `Var("m0", "", "pos", "x")`, though both print the same. A `Var`
    carries no SymPy assumptions, and checks nothing: the owners check
    their names.
    """

    owner: str
    where: str
    path: tuple[str, ...]

    def __new__(cls, owner: str, where: str, *path: str) -> Self:
        # __xnew__ skips SymPy's name cache, which would hand back a symbol
        # made earlier with the same name.
        obj = sp.Symbol.__xnew__(cls, ".".join((owner + where, *path)))
        obj.owner, obj.where, obj.path = owner, where, path
        return obj

    def _hashable_content(self) -> tuple[str, ...]:
        # Strings only, in fixed positions: SymPy compares these element
        # by element to sort terms.
        return (self.name, self.owner, self.where, *self.path)

    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]:
        return (type(self), (self.owner, self.where, *self.path))
