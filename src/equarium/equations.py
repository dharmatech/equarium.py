"""Labeled equations, their origins, and `eq_flat`."""

from dataclasses import dataclass, field
from typing import Literal, cast

import sympy as sp
from sympy.logic.boolalg import BooleanAtom

from equarium.errors import UsageError

type Op = Literal["eliminate zeros"]


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
