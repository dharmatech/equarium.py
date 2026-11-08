"""The operations that rewrite a system's equations."""

from dataclasses import replace
from typing import TYPE_CHECKING

import sympy as sp
from sympy.logic.boolalg import BooleanFalse, BooleanTrue

from equarium.equations import Derived, Equation
from equarium.errors import Contradiction
from equarium.steps import EliminateZerosStep
from equarium.sympy_compat import free_symbols, safe_simplify, sides

if TYPE_CHECKING:
    from equarium.system import System


def cleanup(result: sp.Basic, label: str, symbol: sp.Symbol) -> sp.Equality | None:
    """What a rewrite made of equation `label`, or None when it's to be dropped.

    `true`, or an `Eq` whose difference simplifies to 0, is dropped.
    `false`, or a difference that is a nonzero constant, is a
    contradiction. Anything else is kept as it is.
    """
    if isinstance(result, BooleanTrue):
        return None
    if isinstance(result, BooleanFalse):
        raise Contradiction(f"({label}) is false", symbol=symbol, labels=(label,))
    if not isinstance(result, sp.Equality):
        raise TypeError(f"({label}) became {result!r}, not an equation")
    lhs, rhs = sides(result)
    difference = safe_simplify(lhs - rhs)
    if difference.is_zero:
        return None
    if not difference.free_symbols:
        raise Contradiction(
            f"({label}) became {lhs} = {rhs}", symbol=symbol, labels=(label,)
        )
    return result


def eliminate_zeros(system: System) -> System:
    """Substitute every known that is zero now into the equations.

    The zeros go in one at a time, each followed by cleanup. Every zero
    becomes fixed, whether it occurred in an equation or not.
    """
    zeros = tuple(
        sym
        for sym, value in system.knowns.items()
        if value is not None and value.is_zero is True
    )
    order = {equation.label: i for i, equation in enumerate(system.equations)}
    equations = list(system.equations)
    rewritten: set[str] = set()
    dropped: list[str] = []
    for zero in zeros:
        kept: list[Equation] = []
        for before in equations:
            if zero not in free_symbols(before.eq):
                kept.append(before)
                continue
            after = cleanup(before.eq.subs(zero, sp.S.Zero), before.label, zero)
            if after is None:
                dropped.append(before.label)
                rewritten.discard(before.label)
            else:
                kept.append(
                    Equation(before.label, after, Derived("eliminate zeros", zero, (before,)))
                )
                rewritten.add(before.label)
        equations = kept

    step = EliminateZerosStep(
        zeros=zeros,
        rewritten=tuple(e.label for e in equations if e.label in rewritten),
        dropped=tuple(sorted(dropped, key=order.__getitem__)),
    )
    return replace(
        system,
        equations=tuple(equations),
        fixed=system.fixed | frozenset(zeros),
        step=step,
        previous=system,
    )
