"""`System`: equations, knowns and wants, and the steps that made them."""

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import overload

import sympy as sp
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
from sympy.core.sympify import SympifyError

from equarium import analysis, display, rewrite
from equarium.equations import Equation, Given
from equarium.errors import Contradiction, UsageError
from equarium.solve import Solution, Strategy, all_at_once, solve_with
from equarium.steps import AddStep, ForgetStep, KnownStep, Step, WantStep

type Value = sp.Expr | float


def _no_knowns() -> Mapping[sp.Symbol, sp.Expr | None]:
    return MappingProxyType({})


@dataclass(frozen=True)
class System:
    """An immutable system of equations with its knowns and wants.

    `System()` is the empty root. Every method returns a new system whose
    `previous` is the receiver and whose `step` records the call. Two
    systems are equal when their equations, knowns and wants are.
    """

    equations: tuple[Equation, ...] = ()
    knowns: Mapping[sp.Symbol, sp.Expr | None] = field(default_factory=_no_knowns)
    wants: tuple[sp.Symbol, ...] = ()
    fixed: frozenset[sp.Symbol] = field(default=frozenset(), compare=False)
    next_label: int = field(default=1, compare=False)
    step: Step | None = field(default=None, compare=False)
    previous: System | None = field(default=None, compare=False, repr=False)

    def add(self, *eqs: sp.Basic | bool, label: str | None = None) -> System:
        """Add equations. `true` is dropped, and `false` is a contradiction.

        A label is allowed only with one equation. Without one, each
        equation gets the next number not in use.
        """
        if label is not None:
            if not isinstance(label, str):
                raise UsageError(f"a label is a string, not {label!r}")
            if len(eqs) > 1:
                raise UsageError(
                    f"label {label!r} given with {len(eqs)} equations", labels=(label,)
                )
        kept: list[sp.Equality] = []
        for item in eqs:
            if item is True or isinstance(item, BooleanTrue):
                continue
            if item is False or isinstance(item, BooleanFalse):
                raise Contradiction(
                    "added an equation that is false",
                    labels=(label,) if label is not None else (),
                )
            if not isinstance(item, sp.Equality):
                raise UsageError(f"add takes equations, not {item!r}")
            kept.append(item)

        in_use = {e.label for e in self.equations}
        counter = self.next_label
        added: list[Equation] = []
        for eq in kept:
            if label is not None:
                if label in in_use:
                    raise UsageError(f"label ({label}) is already in use", labels=(label,))
                name = label
            else:
                while str(counter) in in_use:
                    counter += 1
                name = str(counter)
                counter += 1
            in_use.add(name)
            added.append(Equation(name, eq, Given()))

        return replace(
            self,
            equations=self.equations + tuple(added),
            next_label=counter,
            step=AddStep(tuple(added)),
            previous=self,
        )

    @overload
    def known(self, sym: sp.Symbol, value: Value | None = None, /) -> System: ...
    @overload
    def known(self, values: Mapping[sp.Symbol, Value | None], /) -> System: ...
    def known(
        self,
        sym_or_values: sp.Symbol | Mapping[sp.Symbol, Value | None],
        value: Value | None = None,
        /,
    ) -> System:
        """Add or replace knowns. A value is a number, possibly with units,
        and no value means known with no number."""
        if isinstance(sym_or_values, Mapping):
            if value is not None:
                raise UsageError("known takes a mapping alone, or a symbol and a value")
            given = list(sym_or_values.items())
        else:
            given = [(sym_or_values, value)]

        values: list[tuple[sp.Symbol, sp.Expr | None]] = []
        knowns = dict(self.knowns)
        for sym, raw in given:
            if not isinstance(sym, sp.Symbol):
                raise UsageError(f"a known is a symbol, not {sym!r}")
            if sym in self.wants:
                raise UsageError(f"{sym} is a want, so it can't be known", symbol=sym)
            number = _number(sym, raw)
            if sym in self.fixed and number != self.knowns[sym]:
                raise UsageError(
                    f"{sym} = {self.knowns[sym]} was substituted by eliminate_zeros,"
                    " so it can't change; branch from before that step",
                    symbol=sym,
                )
            knowns[sym] = number
            values.append((sym, number))

        return replace(
            self,
            knowns=MappingProxyType(knowns),
            step=KnownStep(tuple(values)),
            previous=self,
        )

    def forget(self, *syms: sp.Symbol) -> System:
        """Remove knowns."""
        for sym in syms:
            if not isinstance(sym, sp.Symbol) or sym not in self.knowns:
                raise UsageError(f"{sym} isn't known", symbol=_symbol_or_none(sym))
            if sym in self.fixed:
                raise UsageError(
                    f"{sym} was substituted by eliminate_zeros, so it can't be"
                    " forgotten; branch from before that step",
                    symbol=sym,
                )
        knowns = {sym: v for sym, v in self.knowns.items() if sym not in syms}
        return replace(
            self,
            knowns=MappingProxyType(knowns),
            step=ForgetStep(syms),
            previous=self,
        )

    def want(self, *syms: sp.Symbol) -> System:
        """Replace the wants. `want()` clears them."""
        for i, sym in enumerate(syms):
            if not isinstance(sym, sp.Symbol):
                raise UsageError(f"a want is a symbol, not {sym!r}")
            if sym in self.knowns:
                raise UsageError(f"{sym} is known, so it can't be a want", symbol=sym)
            if sym in syms[:i]:
                raise UsageError(f"{sym} is wanted twice", symbol=sym)
        return replace(self, wants=syms, step=WantStep(syms), previous=self)

    def equation(self, label: str) -> Equation:
        """The equation with that label."""
        for e in self.equations:
            if e.label == label:
                return e
        raise UsageError(f"no equation ({label})", labels=(label,))

    def eliminate_zeros(self) -> System:
        """Substitute the knowns that are zero now into the equations."""
        return rewrite.eliminate_zeros(self)

    def analyze(self) -> analysis.Analysis:
        return analysis.analyze(self)

    def solve(self, *wants: sp.Symbol, strategy: Strategy = all_at_once) -> Solution:
        """Solve for the wants. Wants given here replace the system's first."""
        return solve_with(self, wants, strategy)

    def show(self) -> None:
        print(display.render(self))


def _number(sym: sp.Symbol, raw: object) -> sp.Expr | None:
    """A known's value: None, or an expression with no free symbols."""
    if raw is None:
        return None
    try:
        number = sp.sympify(raw, strict=True)
    except SympifyError:
        number = None
    if not isinstance(number, sp.Expr):
        raise UsageError(f"the value of {sym} must be a number, not {raw!r}", symbol=sym)
    if number.free_symbols:
        raise UsageError(
            f"the value of {sym} must be a number, not {number};"
            " a relationship between symbols is an equation",
            symbol=sym,
        )
    return number


def _symbol_or_none(sym: object) -> sp.Symbol | None:
    return sym if isinstance(sym, sp.Symbol) else None
