"""Labeled equations, their origins, `eq_flat`, and the both-sides helpers."""

from dataclasses import dataclass, field
from typing import Literal, cast

import sympy as sp
from sympy.logic.boolalg import BooleanAtom

from equarium.errors import UsageError
from equarium.sympy_compat import sides

type Op = Literal["eliminate zeros", "eliminate", "isolate"]


@dataclass(frozen=True)
class Given:
    """An equation as it was added."""


@dataclass(frozen=True)
class Derived:
    """An equation an operation made from its parents."""

    op: Op
    symbol: sp.Symbol
    parents: tuple[Equation, ...]


type Origin = Given | Derived


@dataclass(frozen=True)
class Equation:
    """A label, a plain `sp.Eq`, and where it came from.

    Equations compare by label and `Eq` only, not by origin.
    """

    label: str
    eq: sp.Equality
    origin: Origin = field(compare=False)


def eq_flat(*items: sp.Expr | float) -> list[sp.Equality | BooleanAtom]:
    """Pair the items into equations: `eq_flat(a, b, c, d)` is
    `[Eq(a, b), Eq(c, d)]`.

    A pair that SymPy evaluates on construction comes back as `true` or
    `false`, which `System.add` accepts.
    """
    if len(items) % 2:
        raise UsageError(f"eq_flat needs an even number of items, got {len(items)}")
    return [
        cast(sp.Equality | BooleanAtom, sp.Eq(items[i], items[i + 1]))
        for i in range(0, len(items), 2)
    ]


def add_both_sides(eq: sp.Equality, addend: sp.Expr | float) -> sp.Equality:
    """`eq` with `addend` added to both sides: `add_both_sides(Eq(x, y), 2)`
    is `Eq(x + 2, y + 2)`."""
    lhs, rhs = sides(eq)
    return _still_an_equation(lhs + addend, rhs + addend)


def multiply_both_sides(eq: sp.Equality, factor: sp.Expr | float) -> sp.Equality:
    """`eq` with both sides multiplied by `factor`:
    `multiply_both_sides(Eq(x, y), 3)` is `Eq(3*x, 3*y)`."""
    lhs, rhs = sides(eq)
    return _still_an_equation(lhs * factor, rhs * factor)


def _still_an_equation(lhs: sp.Expr, rhs: sp.Expr) -> sp.Equality:
    """`sp.Eq(lhs, rhs)`, which must stay an equation. SymPy evaluates `Eq`
    on construction, so multiplying both sides by 0 gives `true`."""
    eq = sp.Eq(lhs, rhs)
    if not isinstance(eq, sp.Equality):
        raise UsageError(f"{lhs} = {rhs} became {eq}, not an equation")
    return eq
