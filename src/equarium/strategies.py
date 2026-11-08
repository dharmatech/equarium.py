"""The strategies beyond `all_at_once`: `eliminating`, the old library's
version 2."""

import time
from dataclasses import replace
from typing import TYPE_CHECKING

import sympy as sp

from equarium.errors import EliminationError, UsageError
from equarium.solve import Solution, Strategy, all_at_once
from equarium.sympy_compat import free_symbols
from equarium.text import plural

if TYPE_CHECKING:
    from equarium.system import System


def eliminating(max_eliminations: int = 10) -> Strategy:
    """A strategy that runs `all_at_once`, and while that finds no roots,
    eliminates one connected unknown that isn't a want and tries again,
    up to `max_eliminations` eliminations in all.

    The candidates go in the old library's order: those that occur in no
    equation with a want first, then those in fewer equations, then by
    name. The first that can be eliminated is, with `System.eliminate`,
    so each elimination is a step in the solution's system's history. An
    `EliminationError` moves on to the next candidate, and a
    `Contradiction` propagates. `elapsed` covers the whole run.
    `eliminating(max_eliminations=0)` is `all_at_once`.
    """
    if max_eliminations < 0:
        raise UsageError(
            f"max_eliminations is a count, 0 or more, not {max_eliminations}"
        )

    def strategy(system: System) -> Solution:
        start = time.perf_counter()
        solution = all_at_once(system)
        made = 0
        while not solution.roots and made < max_eliminations:
            eliminated = _eliminate_one(system)
            if eliminated is None:
                break
            system = eliminated
            made += 1
            solution = all_at_once(system)
        reason = solution.reason
        if reason is not None and made:
            reason = f"{reason}, after {plural(made, 'elimination')}"
        return replace(solution, elapsed=time.perf_counter() - start, reason=reason)

    return strategy


def _eliminate_one(system: System) -> System | None:
    """The system with the first candidate that can be eliminated
    eliminated, or None when none can."""
    for sym in _candidates(system):
        try:
            return system.eliminate(sym)
        except EliminationError:
            continue
    return None


def _candidates(system: System) -> list[sp.Symbol]:
    """The connected unknowns that aren't wants, in the old order."""
    wants = set(system.wants)
    symbols = [free_symbols(e.eq) for e in system.equations]
    near_a_want = frozenset[sp.Symbol]().union(*(syms for syms in symbols if syms & wants))
    candidates = [sym for sym in system.analyze().connected if sym not in wants]
    return sorted(
        candidates,
        key=lambda sym: (
            sym in near_a_want,
            sum(sym in syms for syms in symbols),
            sym.name,
        ),
    )
