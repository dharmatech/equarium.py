"""The steps: one structured value per operation on a `System`.

A step records the operation, its arguments and what it changed. Its
description is rendered by `equarium.display`, never stored.
"""

from dataclasses import dataclass

import sympy as sp

from equarium.equations import Equation


@dataclass(frozen=True)
class AddStep:
    equations: tuple[Equation, ...]  # the ones added


@dataclass(frozen=True)
class KnownStep:
    values: tuple[tuple[sp.Symbol, sp.Expr | None], ...]  # in the order given


@dataclass(frozen=True)
class ForgetStep:
    symbols: tuple[sp.Symbol, ...]


@dataclass(frozen=True)
class WantStep:
    symbols: tuple[sp.Symbol, ...]


@dataclass(frozen=True)
class EliminateZerosStep:
    zeros: tuple[sp.Symbol, ...]
    rewritten: tuple[str, ...]  # rewritten and still there, in equation order
    dropped: tuple[str, ...]


@dataclass(frozen=True)
class EliminateStep:
    symbol: sp.Symbol
    using: str  # the equation the root came from, given or chosen
    replacement: sp.Expr  # the root substituted for the symbol
    rewritten: tuple[str, ...]  # rewritten and still there, in equation order
    dropped: tuple[str, ...]


@dataclass(frozen=True)
class IsolateStep:
    symbol: sp.Symbol
    label: str


type Step = (
    AddStep
    | KnownStep
    | ForgetStep
    | WantStep
    | EliminateZerosStep
    | EliminateStep
    | IsolateStep
)
