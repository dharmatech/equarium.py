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
from sympy.core.relational import Relational
from sympy.logic.boolalg import BooleanFalse, BooleanFunction, BooleanTrue
from sympy.physics.units import Quantity, convert_to

from equarium import display
from equarium.analysis import analyze
from equarium.errors import UsageError
from equarium.sympy_compat import free_symbols
from equarium.text import listing, plural

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
                + listing(str(want) for want in self.formulas),
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

    def where(self, relation: sp.Basic) -> Solution:
        """The roots for which `relation` holds, such as `t1 > 0`.

        `relation` is a SymPy relation over the wants and the knowns, or
        relations joined with `&`, `|` and `~`. Each root's numbers are
        substituted for the wants, then the knowns' values, and the root
        is kept when the result is `true` and dropped when it's `false`.
        Anything else is a `UsageError`. The roots kept stay in their
        order, and when none are, the solution has no roots and a reason.
        """
        if not isinstance(relation, Relational | BooleanFunction):
            raise UsageError(
                f"where takes a SymPy relation, such as t1 > 0, not {relation!r}"
            )
        if not self.roots:
            return self
        values = _values(self.system)
        kept = tuple(root for root in self.roots if _holds(relation, root, values))
        if not kept:
            return Solution(self.system, (), self.elapsed, f"no root satisfies {relation}")
        return Solution(self.system, kept, self.elapsed)

    def in_units(self, *units: sp.Expr) -> Solution:
        """The solution with every number converted to `units`, such as
        `in_units(meter, second)`, by SymPy's `convert_to`.

        The system, the formulas, `elapsed` and the reason stay. A number
        with no units, or a known with no number left as a symbol, comes
        out as it went in. A solution with no roots is returned as it is.
        """
        if not units:
            raise UsageError("in_units needs units, such as in_units(meter, second)")
        for unit in units:
            if not is_unit(unit):
                raise UsageError(
                    f"in_units takes units, such as meter or kilometer/hour, not {unit!r}"
                )
        if not self.roots:
            return self
        targets = list(units)
        roots = tuple(
            Root(
                formulas=root.formulas,
                numbers=MappingProxyType(
                    {want: _convert(number, targets) for want, number in root.numbers.items()}
                ),
            )
            for root in self.roots
        )
        return Solution(self.system, roots, self.elapsed, self.reason)

    def show(self) -> None:
        print(display.render_solution(self))

    def _repr_pretty_(self, p: display.TextPrinter, cycle: bool) -> None:
        """The solution as IPython, and transcript mode, print it: as
        `show` prints it."""
        p.text(display.render_solution(self))

    def _only_root(self, call: str) -> Root:
        if len(self.roots) != 1:
            count = plural(len(self.roots), "root")
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
    for found_root in found:
        for want in system.wants:
            unknowns = sorted(
                free_symbols(found_root[want]) - system.knowns.keys(),
                key=lambda sym: sym.name,
            )
            if unknowns:
                return Solution(
                    system,
                    (),
                    elapsed,
                    f"sp.solve left {want} in terms of the"
                    f" {'unknown' if len(unknowns) == 1 else 'unknowns'}"
                    f" {listing(sym.name for sym in unknowns)}",
                )

    values = _values(system)
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


# Typed as `Expr.subs` takes them, so that it returns an `Expr`.
type Values = Mapping[sp.Basic | complex, sp.Expr | complex]


def _values(system: System) -> Values:
    """The knowns that have a number, with their numbers."""
    return {sym: value for sym, value in system.knowns.items() if value is not None}


def _number(formula: sp.Expr, values: Values) -> sp.Expr:
    """`sp.N` of the formula with the values substituted. A known with no
    number stays a symbol, and units stay as they come."""
    return cast(sp.Expr, sp.N(formula.subs(values)))  # sp.N is untyped


def is_unit(expr: object) -> bool:
    """Whether `expr` is a unit: a SymPy `Quantity` such as `meter`, or a
    product of their powers such as `kilometer/hour` or `meter/second**2`.
    A number, such as `3` or `3*meter`, isn't one."""
    if not isinstance(expr, sp.Expr):
        return False
    for factor in sp.Mul.make_args(expr):
        base, exponent = factor.as_base_exp()
        if not isinstance(base, Quantity) or not exponent.is_Rational:
            return False
    return True


def _convert(number: sp.Expr, units: list[sp.Expr]) -> sp.Expr:
    return cast(sp.Expr, convert_to(number, units))  # convert_to is untyped


def _holds(relation: sp.Basic, root: Root, values: Values) -> bool:
    """Whether `relation` is `true` for the root's numbers and the knowns'
    values, or `false`. Anything else is a `UsageError`."""
    numbers: Values = {want: number for want, number in root.numbers.items()}
    try:
        result = relation.subs(numbers).subs(values)
    except TypeError as e:  # a comparison with a number that isn't real
        raise UsageError(f"{relation} doesn't reduce to true or false: {e}") from e
    if isinstance(result, BooleanTrue):
        return True
    if isinstance(result, BooleanFalse):
        return False
    raise UsageError(f"{relation} became {result}, not true or false")
