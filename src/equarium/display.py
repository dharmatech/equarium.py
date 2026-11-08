"""Rendering systems, their histories and solutions as text.

Every symbol goes through a hook, `(symbol, role) -> str`. The printer
calls it from `_print_Symbol`, so symbol names never change and neither
does SymPy's order of terms.
"""

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, assert_never

import sympy as sp
from sympy.printing.str import StrPrinter

from equarium.analysis import Analysis, Role, analyze
from equarium.equations import Derived, Equation
from equarium.steps import (
    AddStep,
    EliminateStep,
    EliminateZerosStep,
    ForgetStep,
    IsolateStep,
    KnownStep,
    Step,
    WantStep,
)

if TYPE_CHECKING:
    from equarium.solve import Root, Solution
    from equarium.system import System

type SymbolHook = Callable[[sp.Symbol, Role], str]

GREEN = "\x1b[32m"
RED = "\x1b[31m"
RESET = "\x1b[0m"


def plain(symbol: sp.Symbol, role: Role) -> str:
    """The name alone, whatever the role."""
    return symbol.name


def terminal(symbol: sp.Symbol, role: Role) -> str:
    """Knowns in green, wants in red, other unknowns plain, in ANSI codes."""
    match role:
        case Role.KNOWN:
            return f"{GREEN}{symbol.name}{RESET}"
        case Role.WANT:
            return f"{RED}{symbol.name}{RESET}"
        case Role.UNKNOWN:
            return symbol.name


class Printer(StrPrinter):
    """SymPy's string printer, with every symbol printed by the hook."""

    def __init__(self, symbol: SymbolHook, analysis: Analysis) -> None:
        super().__init__({"full_prec": False})
        self.hook = symbol
        self.analysis = analysis

    def _print_Symbol(self, expr: sp.Symbol) -> str:
        return self.hook(expr, self.analysis.role(expr))

    def equation(self, eq: sp.Equality) -> str:
        return f"{self.doprint(eq.lhs)} = {self.doprint(eq.rhs)}"

    def known(self, sym: sp.Symbol, value: sp.Expr | None) -> str:
        if value is None:
            return self.doprint(sym)
        return f"{self.doprint(sym)} = {self.doprint(value)}"

    def symbols(self, syms: Iterable[sp.Symbol]) -> str:
        return listing(self.doprint(sym) for sym in syms)


def listing(items: Iterable[str]) -> str:
    """The items joined by commas, or `none`."""
    return ", ".join(items) or "none"


def labels(names: Iterable[str]) -> str:
    return listing(f"({name})" for name in names)


def plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def render(system: System, symbol: SymbolHook = terminal, origins: bool = False) -> str:
    """One line per equation, then the knowns, the wants, the connected
    unknowns and the equations ready to solve.

    With `origins`, each derived equation's line is followed by its
    origin, indented: `  (2.2) ← (2.2) + (2.7), eliminate dt`. Only the
    origin itself is shown, not its parents' origins.
    """
    analysis = analyze(system)
    p = Printer(symbol, analysis)
    lines: list[str] = []
    for e in system.equations:
        lines.append(f"({e.label})  {p.equation(e.eq)}")
        if origins and isinstance(e.origin, Derived):
            lines.append("  " + render_origin(e, e.origin, p))
    lines.append(
        "knowns: " + listing(p.known(sym, value) for sym, value in system.knowns.items())
    )
    lines.append("wants: " + p.symbols(system.wants))
    connected = sorted(analysis.connected, key=lambda sym: sym.name)
    if connected:
        counts = (
            f"{plural(len(connected), 'unknown')} in"
            f" {plural(len(analysis.connected_labels), 'equation')}"
        )
        lines.append(f"connected: {p.symbols(connected)} ({counts})")
    else:
        lines.append("connected: none")
    lines.append("ready: " + labels(analysis.ready))
    return "\n".join(lines)


def render_origin(equation: Equation, origin: Derived, p: Printer) -> str:
    """`(2.2) ← (2.2) + (2.7), eliminate dt`: the equation's label, its
    parents' labels, and what was done."""
    parents = " + ".join(f"({parent.label})" for parent in origin.parents)
    match origin.op:
        case "eliminate zeros":
            what = f"{p.doprint(origin.symbol)} = 0"
        case "eliminate":
            what = f"eliminate {p.doprint(origin.symbol)}"
        case "isolate":
            what = f"isolate {p.doprint(origin.symbol)}"
        case _:
            assert_never(origin.op)
    return f"({equation.label}) ← {parents}, {what}"


def render_solution(solution: Solution, symbol: SymbolHook = terminal) -> str:
    """Each want's formula line, then its number line. Several roots come
    numbered, and no roots gives the reason."""
    if not solution.roots:
        return f"no roots: {solution.reason}"
    p = Printer(symbol, analyze(solution.system))
    if len(solution.roots) == 1:
        return "\n".join(_root_lines(solution.roots[0], p))
    lines: list[str] = []
    for i, root in enumerate(solution.roots, 1):
        lines.append(f"root {i}:")
        lines.extend("  " + line for line in _root_lines(root, p))
    return "\n".join(lines)


def _root_lines(root: Root, p: Printer) -> list[str]:
    lines: list[str] = []
    for want, formula in root.formulas.items():
        lines.append(f"{p.doprint(want)} = {p.doprint(formula)}")
        lines.append(f"{p.doprint(want)} = {p.doprint(root.numbers[want])}")
    return lines


def render_step(step: Step, p: Printer) -> str:
    match step:
        case AddStep(equations):
            return "add " + labels(e.label for e in equations)
        case KnownStep(values):
            return "known " + listing(p.known(sym, value) for sym, value in values)
        case ForgetStep(syms):
            return "forget " + p.symbols(syms)
        case WantStep(syms):
            return "want " + p.symbols(syms)
        case EliminateZerosStep(zeros, rewritten, dropped):
            if not zeros:
                return "eliminate zeros: none"
            changes = _changes(rewritten, dropped)
            return f"eliminate zeros {p.symbols(zeros)}: {changes or 'no change'}"
        case EliminateStep(sym, using, _, rewritten, dropped):
            done = f"eliminate {p.doprint(sym)} using ({using})"
            changes = _changes(rewritten, dropped)
            return f"{done}: {changes}" if changes else done
        case IsolateStep(sym, label):
            return f"isolate {p.doprint(sym)} in ({label})"
        case _:
            assert_never(step)


def _changes(rewritten: tuple[str, ...], dropped: tuple[str, ...]) -> str:
    """`into (1), (3), dropped (4)`, or empty when nothing changed."""
    changes: list[str] = []
    if rewritten:
        changes.append("into " + labels(rewritten))
    if dropped:
        changes.append("dropped " + labels(dropped))
    return ", ".join(changes)


def render_history(system: System, symbol: SymbolHook = terminal) -> str:
    """The steps from the first, numbered from 1, each with the roles of
    the system it produced."""
    made: list[tuple[Step, System]] = []
    current: System | None = system
    while current is not None:
        if current.step is not None:
            made.append((current.step, current))
        current = current.previous
    made.reverse()
    return "\n".join(
        f"{i}. {render_step(step, Printer(symbol, analyze(after)))}"
        for i, (step, after) in enumerate(made, 1)
    )
