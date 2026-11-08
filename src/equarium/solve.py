"""Solving a system: `Root`, `Solution`, the strategies, and `solve_with`.

A strategy is a function from a `System` to a `Solution`. `solve_with`,
behind `System.solve`, sets the wants and calls one.
"""

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, cast

import sympy as sp

from equarium import display
from equarium.analysis import analyze
from equarium.errors import UsageError

if TYPE_CHECKING:
    from equarium.system import System


@dataclass(frozen=True)
class Root:
    """One root: a formula and a number for every want, in the wants' order.

    The formula is in terms of the knowns. The number is the formula with
    the knowns' values substituted, through `sp.N`.
    """

    formulas: Mapping[sp.Symbol, sp.Expr]
    numbers: Mapping[sp.Symbol, sp.Expr]

    def formula(self, sym: sp.Symbol) -> sp.Expr:
        return self.formulas[self._want(sym)]

    def number(self, sym: sp.Symbol) -> sp.Expr:
        return self.numbers[self._want(sym)]

    def _want(self, sym: sp.Symbol) -> sp.Symbol:
        if sym not in self.formulas:
            raise UsageError(
                f"{sym} isn't a want; the wants are "
                + display.listing(str(want) for want in self.formulas),
                symbol=sym,
            )
        return sym


@dataclass(frozen=True)
class Solution:
    """The roots a strategy found for a system's wants.

    `system` is the system solved, with its history. `reason` says why
    there are no roots, and is None exactly when there are some.
    `elapsed` is in seconds, and doesn't take part in equality.
    """

    system: System
    roots: tuple[Root, ...]
    elapsed: float = field(compare=False)
    reason: str | None = None

    def __post_init__(self) -> None:
        if (self.reason is None) != bool(self.roots):
            raise UsageError("a solution has a reason exactly when it has no roots")

    def formula(self, sym: sp.Symbol) -> sp.Expr:
        """The formula for `sym`, from the only root."""
        return self._only_root(f"formula({sym})").formula(sym)

    def number(self, sym: sp.Symbol) -> sp.Expr:
        """The number for `sym`, from the only root."""
        return self._only_root(f"number({sym})").number(sym)

    def show(self) -> None:
        print(display.render_solution(self))

    def _only_root(self, call: str) -> Root:
        if len(self.roots) != 1:
            count = display.plural(len(self.roots), "root")
            why = f" ({self.reason})" if self.reason is not None else ""
            raise UsageError(f"{call} needs exactly one root, and there are {count}{why}")
        return self.roots[0]


type Strategy = Callable[[System], Solution]


def solve_with(system: System, wants: tuple[sp.Symbol, ...], strategy: Strategy) -> Solution:
    """Solve `system` with `strategy`. Wants given here replace the
    system's wants first, as a recorded step."""
    if wants:
        system = system.want(*wants)
    if not system.wants:
        raise UsageError("solve needs wants: pass them to solve, or call want first")
    return strategy(system)


def all_at_once(system: System) -> Solution:
    """One `sp.solve` over the connected unknowns, with the knowns kept as
    symbols, and then the knowns' values substituted for the numbers."""
    analysis = analyze(system)
    connected = set(analysis.connected_labels)
    equations = [e.eq for e in system.equations if e.label in connected]
    unknowns = sorted(analysis.connected, key=lambda sym: sym.name)

    start = time.perf_counter()
    try:
        found = cast(
            list[dict[sp.Symbol, sp.Expr]], sp.solve(equations, unknowns, dict=True)
        )
    except NotImplementedError as e:
        return Solution(system, (), time.perf_counter() - start, f"sp.solve: {e}")
    elapsed = time.perf_counter() - start

    if not found:
        return Solution(system, (), elapsed, "sp.solve found no roots")
    for want in system.wants:
        if any(want not in found_root for found_root in found):
            return Solution(system, (), elapsed, f"sp.solve left {want} undetermined")

    # Typed as `Expr.subs` takes them, so that it returns an `Expr`.
    values: dict[sp.Basic | complex, sp.Expr | complex] = {
        sym: value for sym, value in system.knowns.items() if value is not None
    }
    roots = tuple(
        Root(
            formulas=MappingProxyType({want: found_root[want] for want in system.wants}),
            numbers=MappingProxyType(
                {want: _number(found_root[want], values) for want in system.wants}
            ),
        )
        for found_root in found
    )
    return Solution(system, roots, elapsed)


def _number(
    formula: sp.Expr, values: Mapping[sp.Basic | complex, sp.Expr | complex]
) -> sp.Expr:
    """`sp.N` of the formula with the values substituted. A known with no
    number stays a symbol, and units stay as they come."""
    return cast(sp.Expr, sp.N(formula.subs(values)))  # sp.N is untyped
