"""Rendering systems, their histories and solutions as text.

Every symbol goes through a hook, `(symbol, role) -> str`. The printer
calls it from `_print_Symbol`, so symbol names never change and neither
does SymPy's order of terms.
"""

import re
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Protocol, assert_never

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
from equarium.text import labels, listing, plural

if TYPE_CHECKING:
    from equarium.solve import Root, Solution
    from equarium.system import System

type SymbolHook = Callable[[sp.Symbol, Role], str]


class TextPrinter(Protocol):
    """The part of IPython's pretty printer that `_repr_pretty_` uses."""

    def text(self, obj: str) -> None: ...

GREEN = "\x1b[32m"
RED = "\x1b[31m"
RESET = "\x1b[0m"
ANSI = re.compile(r"\x1b\[[0-9;]*m")

WIDTH = 74
"""The widest a system's lists, such as its knowns, run before they wrap:
79 columns in a transcript, after its `#> ` and a two-character mark."""

ALIGN_LIMIT = 16
"""The widest left side that the `=` signs line up after. A wider one
isn't padded, and doesn't push the others' `=` to the right."""


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


def render(system: System, symbol: SymbolHook = terminal, origins: bool = False) -> str:
    """One line per equation, then the knowns, the wants, the connected
    unknowns and the equations ready to solve.

    The labels are right-aligned, so the equations start in one column,
    and their `=` signs line up, for left sides up to `ALIGN_LIMIT` wide.
    Each list wraps to stay within `WIDTH`, its later lines under its
    first item.

    With `origins`, each derived equation's line is followed by its
    origin, starting under the equation: `(2.2) ← (2.2) + (2.7),
    eliminate dt`. Only the origin itself is shown, not its parents'
    origins.
    """
    analysis = analyze(system)
    p = Printer(symbol, analysis)
    lines: list[str] = []
    tags = [f"({e.label})" for e in system.equations]
    tag_width = max(map(len, tags), default=0)
    sides = [(p.doprint(e.eq.lhs), p.doprint(e.eq.rhs)) for e in system.equations]
    column = max((w for lhs, _ in sides if (w := width(lhs)) <= ALIGN_LIMIT), default=0)
    for e, tag, (lhs, rhs) in zip(system.equations, tags, sides, strict=True):
        pad = " " * max(column - width(lhs), 0)
        lines.append(f"{tag.rjust(tag_width)}  {lhs}{pad} = {rhs}")
        if origins and isinstance(e.origin, Derived):
            lines.append(" " * (tag_width + 2) + render_origin(e, e.origin, p))
    lines += wrapped("knowns: ", [p.known(sym, value) for sym, value in system.knowns.items()])
    lines += wrapped("wants: ", [p.doprint(sym) for sym in system.wants])
    connected = sorted(analysis.connected, key=lambda sym: sym.name)
    if connected:
        counts = (
            f" ({plural(len(connected), 'unknown')} in"
            f" {plural(len(analysis.connected_labels), 'equation')})"
        )
        lines += wrapped("connected: ", [p.doprint(sym) for sym in connected], counts)
    else:
        lines.append("connected: none")
    lines += wrapped("ready: ", [f"({label})" for label in analysis.ready])
    return "\n".join(lines)


def width(text: str) -> int:
    """How many columns the text takes, without its colors."""
    return len(ANSI.sub("", text))


def wrapped(head: str, items: list[str], tail: str = "") -> list[str]:
    """`head`, then the items, separated by commas, over as many lines as
    keep each within `WIDTH`, the later ones indented under the first
    item. `tail` follows the last item. No items: `head` and `none`.
    An item too wide for any line gets one of its own."""
    if not items:
        return [f"{head}none"]
    pieces = [f"{item}," for item in items[:-1]] + [items[-1] + tail]
    lines = [head + pieces[0]]
    for piece in pieces[1:]:
        if width(lines[-1]) + 1 + width(piece) <= WIDTH:
            lines[-1] += " " + piece
        else:
            lines.append(" " * len(head) + piece)
    return lines


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
    numbered, and no roots gives the reason. A last line gives the time,
    `time: 6.02 s`, when it's at least 1 s."""
    lines: list[str] = []
    p = Printer(symbol, analyze(solution.system))
    if not solution.roots:
        lines.append(f"no roots: {solution.reason}")
    elif len(solution.roots) == 1:
        lines.extend(_root_lines(solution.roots[0], p))
    else:
        for i, root in enumerate(solution.roots, 1):
            lines.append(f"root {i}:")
            lines.extend("  " + line for line in _root_lines(root, p))
    if solution.elapsed >= 1:
        lines.append(f"time: {solution.elapsed:.2f} s")
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
