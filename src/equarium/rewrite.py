"""The operations that rewrite a system's equations, and the cleanup
inside each of them."""

from dataclasses import replace
from typing import TYPE_CHECKING, cast

import sympy as sp
from sympy.logic.boolalg import BooleanFalse, BooleanTrue

from equarium.equations import Derived, Equation
from equarium.errors import Contradiction, EliminationError, IsolationError, UsageError
from equarium.steps import EliminateStep, EliminateZerosStep, IsolateStep
from equarium.sympy_compat import free_symbols, safe_simplify, sides
from equarium.text import plural

if TYPE_CHECKING:
    from equarium.system import System


def cleanup(lhs: sp.Expr, rhs: sp.Expr, label: str, symbol: sp.Symbol) -> sp.Equality | None:
    """The equation a rewrite made of equation `label`, from its two new
    sides, or None when it's to be dropped.

    A side with `zoo` or `nan` is undefined, a contradiction. The sides
    are checked before `Eq` sees them, since `Eq(a, zoo)` is `false`.
    `true`, or an `Eq` whose difference simplifies to 0, is dropped.
    `false`, or a difference that is a nonzero constant, is a
    contradiction. Anything else is kept as it is.
    """
    if lhs.has(sp.zoo, sp.nan) or rhs.has(sp.zoo, sp.nan):
        raise Contradiction(
            f"({label}) is undefined: {lhs} = {rhs}", symbol=symbol, labels=(label,)
        )
    result = sp.Eq(lhs, rhs)
    if isinstance(result, BooleanTrue):
        return None
    if isinstance(result, BooleanFalse):
        raise Contradiction(
            f"({label}) is false: {lhs} = {rhs}", symbol=symbol, labels=(label,)
        )
    if not isinstance(result, sp.Equality):
        raise TypeError(f"({label}) became {result!r}, not an equation")
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
    becomes fixed, whether it occurred in an equation or not. The step
    lists the zeros that weren't fixed before it, and the fixed ones
    that still changed an equation, such as one added since.
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
    changed: set[sp.Symbol] = set()  # the zeros that rewrote or dropped an equation
    for zero in zeros:
        kept: list[Equation] = []
        for before in equations:
            if zero not in free_symbols(before.eq):
                kept.append(before)
                continue
            changed.add(zero)
            lhs, rhs = sides(before.eq)
            after = cleanup(
                lhs.subs(zero, sp.S.Zero), rhs.subs(zero, sp.S.Zero), before.label, zero
            )
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
        zeros=tuple(zero for zero in zeros if zero not in system.fixed or zero in changed),
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


def roots(eq: sp.Equality, sym: sp.Symbol) -> list[sp.Expr]:
    """The roots of `eq` for `sym` that don't contain `sym`, each simplified.

    SymPy's `NotImplementedError` means no usable roots. Any other
    exception propagates, since it means a bug.
    """
    try:
        found = cast(list[sp.Expr], sp.solve(eq, sym))
    except NotImplementedError:
        return []
    return [safe_simplify(root) for root in found if sym not in free_symbols(root)]


def eliminate(system: System, sym: sp.Symbol, using: str | None = None) -> System:
    """Solve one equation for `sym`, substitute the root into every other
    equation that has `sym`, remove that equation, and clean up.

    With `using`, that equation must give exactly one root. Without it,
    the equation whose one root has the fewest operations is used, and a
    tie goes to the earlier equation. Each rewritten side is simplified
    on its own, never the `Eq` as a whole, so an equation keeps its shape.
    """
    if not isinstance(sym, sp.Symbol):
        raise UsageError(f"eliminate takes symbols, not {sym!r}")
    if sym in system.knowns:
        raise EliminationError(f"{sym} is known, so it can't be eliminated", symbol=sym)
    if sym in system.wants:
        raise EliminationError(f"{sym} is a want, so it can't be eliminated", symbol=sym)
    source, root = _given(system, sym, using) if using is not None else _chosen(system, sym)

    equations: list[Equation] = []
    rewritten: list[str] = []
    dropped: list[str] = []
    for before in system.equations:
        if before is source:
            continue
        if sym not in free_symbols(before.eq):
            equations.append(before)
            continue
        lhs, rhs = sides(before.eq)
        after = cleanup(
            safe_simplify(lhs.subs(sym, root)),
            safe_simplify(rhs.subs(sym, root)),
            before.label,
            sym,
        )
        if after is None:
            dropped.append(before.label)
        else:
            equations.append(
                Equation(before.label, after, Derived("eliminate", sym, (before, source)))
            )
            rewritten.append(before.label)

    step = EliminateStep(
        symbol=sym,
        using=source.label,
        replacement=root,
        rewritten=tuple(rewritten),
        dropped=tuple(dropped),
    )
    return replace(system, equations=tuple(equations), step=step, previous=system)


def _given(system: System, sym: sp.Symbol, label: str) -> tuple[Equation, sp.Expr]:
    """Equation `label` and its one root for `sym`."""
    source = system.equation(label)
    if sym not in free_symbols(source.eq):
        raise EliminationError(f"({label}) has no {sym}", symbol=sym, labels=(label,))
    found = roots(source.eq, sym)
    if len(found) != 1:
        raise EliminationError(
            f"({label}) gives {plural(len(found), 'root')} for {sym},"
            " and eliminating needs exactly one",
            symbol=sym,
            labels=(label,),
        )
    return source, found[0]


def _chosen(system: System, sym: sp.Symbol) -> tuple[Equation, sp.Expr]:
    """The equation whose one root for `sym` has the fewest operations,
    the earlier one on a tie, and that root."""
    containing = [e for e in system.equations if sym in free_symbols(e.eq)]
    if not containing:
        raise EliminationError(f"no equation has {sym}", symbol=sym)
    best: tuple[int, Equation, sp.Expr] | None = None
    counts: list[str] = []
    for e in containing:
        found = roots(e.eq, sym)
        counts.append(f"({e.label}) gives {plural(len(found), 'root')}")
        if len(found) == 1:
            ops = _count_ops(found[0])
            if best is None or ops < best[0]:
                best = (ops, e, found[0])
    if best is None:
        raise EliminationError(
            f"no equation gives exactly one root for {sym}: " + ", ".join(counts),
            symbol=sym,
            labels=tuple(e.label for e in containing),
        )
    _, source, root = best
    return source, root


def _count_ops(expr: sp.Expr) -> int:
    """`sp.count_ops`, which SymPy leaves untyped."""
    return cast(int, sp.count_ops(expr))


def isolate(system: System, sym: sp.Symbol, label: str) -> System:
    """Rewrite equation `label` as `sym = root`, from its one root."""
    if not isinstance(sym, sp.Symbol):
        raise UsageError(f"isolate takes a symbol, not {sym!r}")
    before = system.equation(label)
    if sym not in free_symbols(before.eq):
        raise IsolationError(f"({label}) has no {sym}", symbol=sym, labels=(label,))
    found = roots(before.eq, sym)
    if len(found) != 1:
        raise IsolationError(
            f"({label}) gives {plural(len(found), 'root')} for {sym},"
            " and isolating needs exactly one",
            symbol=sym,
            labels=(label,),
        )
    eq = sp.Eq(sym, found[0])
    if not isinstance(eq, sp.Equality):  # sym is free, and the root has no sym
        raise TypeError(f"{sym} = {found[0]} became {eq!r}, not an equation")
    after = Equation(label, eq, Derived("isolate", sym, (before,)))
    return replace(
        system,
        equations=tuple(after if e is before else e for e in system.equations),
        step=IsolateStep(sym, label),
        previous=system,
    )
