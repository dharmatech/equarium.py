"""The book's answers, written beside each example, and how they match.

An example module keeps a `BOOK: list[Answer | Formula]`, and
`tests/test_examples.py` checks every one. An `Answer` is a number the
book prints, and a `Formula` is a formula it prints.
"""

import io
import keyword
import tokenize
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

import sympy as sp
from sympy.core.function import AppliedUndef
from sympy.parsing.sympy_parser import parse_expr
from sympy.physics.units import Quantity

from equarium import Solution, UsageError
from equarium.solve import is_unit
from equarium.sympy_compat import free_symbols, safe_simplify


@dataclass(frozen=True, init=False)
class Answer:
    """The values a book prints for one symbol of a solution.

    `Answer(sol_a, x1, "43")`, or `Answer(sol, v1, "-11.3", "11.3")` for a
    solution with two roots. The printed values are strings, as the book
    prints them, since the last digit sets the tolerance.

    For numbers with units, `unit` is the unit the book prints them in:
    `Answer(sol.in_units(meter, second), x1, "1.70", unit=meter)`.
    """

    solution: Solution
    symbol: sp.Symbol
    printed: tuple[str, ...]
    unit: sp.Expr | None

    def __init__(
        self,
        solution: Solution,
        symbol: sp.Symbol,
        *printed: str,
        unit: sp.Expr | None = None,
    ) -> None:
        if symbol not in solution.system.wants:
            raise UsageError(f"{symbol} isn't a want of the solution", symbol=symbol)
        if not printed:
            raise UsageError(f"no printed value for {symbol}", symbol=symbol)
        for value in printed:
            _decimal(value)
        if unit is not None and not is_unit(unit):
            raise UsageError(
                f"unit is a unit, such as meter or kilometer/hour, not {unit!r}",
                symbol=symbol,
            )
        object.__setattr__(self, "solution", solution)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "printed", printed)
        object.__setattr__(self, "unit", unit)

    def mismatch(self) -> str | None:
        """None when the solution's numbers match the printed values, and
        otherwise what differs.

        They match when every root's number is real, and the numbers,
        sorted, pair one to one with the printed values, sorted, each
        within half a unit in the printed value's last digit.

        With a `unit`, each number is divided by it first, without
        simplifying, and must have no units left. So a number in
        kilometers doesn't match `unit=meter`: convert it with
        `Solution.in_units` first. Without a `unit`, a number with units
        doesn't match.
        """
        printed = ", ".join(self.printed)
        if not self.solution.roots:
            return f"{self.symbol}: printed {printed}, found no roots ({self.solution.reason})"
        numbers = [root.number(self.symbol) for root in self.solution.roots]
        found = ", ".join(sp.sstr(number, full_prec=False) for number in numbers)
        where = f"{self.symbol}: printed {printed}, found {found}"

        for number in numbers:
            if number.free_symbols:
                return f"{where}, which has free symbols"
        if self.unit is None:
            if any(number.has(Quantity) for number in numbers):
                return f"{where}, which has units: give unit="
        else:
            # Not simplified: simplify cancels kilometer/meter.
            numbers = [number / self.unit for number in numbers]
            if any(number.has(Quantity) for number in numbers):
                return f"{where}, which isn't in {self.unit}"
        for number in numbers:
            if number.is_real is not True:
                return f"{where}, which isn't a real number"
        if len(numbers) != len(self.printed):
            return (
                f"{where}: {len(self.printed)} printed for"
                f" {len(numbers)} {'root' if len(numbers) == 1 else 'roots'}"
            )
        expected = sorted(_decimal(value) for value in self.printed)
        actual = sorted(Decimal(float(number)) for number in numbers)
        for book, ours in zip(expected, actual):
            tolerance = _half_unit(book)
            if abs(ours - book) > tolerance:
                return f"{where}: {book} allows ±{tolerance}"
        return None


def _decimal(value: str) -> Decimal:
    try:
        number = Decimal(value)
    except InvalidOperation:
        number = None
    if number is None or not number.is_finite():
        raise UsageError(f"{value!r} isn't a printed number")
    return number


def _half_unit(value: Decimal) -> Decimal:
    """Half a unit in the last printed digit: 0.5 for "43", 0.005 for "1.70"."""
    exponent = value.as_tuple().exponent
    assert isinstance(exponent, int)  # a finite value, not "NaN" or "Infinity"
    return Decimal(5).scaleb(exponent - 1)


@dataclass(frozen=True, init=False)
class Formula:
    """The formula a book prints for one symbol of a solution.

    `Formula(sol_top, p1.pos.y, "p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)")`.
    The printed formula is in SymPy's syntax and the solution's symbols,
    by name: those of its equations, knowns, wants and formulas. Every
    other name in it must be a SymPy function or constant, such as `sin`,
    `sqrt` or `pi`, so a typo is an error rather than a new symbol.

    A name SymPy defines, such as `E` or `I`, means SymPy's constant,
    unless the solution has a symbol of that name.
    """

    solution: Solution
    symbol: sp.Symbol
    printed: str
    expr: sp.Expr = field(compare=False, repr=False)

    def __init__(self, solution: Solution, symbol: sp.Symbol, printed: str) -> None:
        if symbol not in solution.system.wants:
            raise UsageError(f"{symbol} isn't a want of the solution", symbol=symbol)
        if not isinstance(printed, str):
            raise UsageError(
                f"the printed formula for {symbol} is text, not {printed!r}", symbol=symbol
            )
        object.__setattr__(self, "solution", solution)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "printed", printed)
        object.__setattr__(self, "expr", _parse(printed, _symbols_by_name(solution), symbol))

    def mismatch(self) -> str | None:
        """None when the solution has one root, and its formula for the
        symbol is the printed one, and otherwise what differs.

        They are the same when their difference simplifies to 0, so an
        equivalent form matches: `"sin(2*a)"` for `2*sin(a)*cos(a)`. Every
        symbol in the printed formula must be in the root's formula.
        """
        where = f"{self.symbol}: printed {self.printed}"
        roots = self.solution.roots
        if not roots:
            return f"{where}, found no roots ({self.solution.reason})"
        if len(roots) > 1:
            found = "; ".join(str(root.formula(self.symbol)) for root in roots)
            return f"{where}, found {len(roots)} roots: {found}"
        formula = self.solution.formula(self.symbol)
        present = free_symbols(formula)
        missing = sorted(sym.name for sym in free_symbols(self.expr) - present)
        if missing:
            return f"{where}, found {formula}, which has no {', '.join(missing)}"
        if safe_simplify(formula - self.expr).is_zero is not True:
            return f"{where}, found {formula}"
        return None


def _symbols_by_name(solution: Solution) -> dict[str, sp.Symbol]:
    """The solution's symbols by name: its equations', knowns', wants' and
    formulas'."""
    system = solution.system
    symbols: set[sp.Symbol] = set(system.knowns) | set(system.wants)
    for equation in system.equations:
        symbols |= free_symbols(equation.eq)
    for root in solution.roots:
        for formula in root.formulas.values():
            symbols |= free_symbols(formula)
    return {sym.name: sym for sym in symbols}


def _parse(printed: str, symbols: dict[str, sp.Symbol], symbol: sp.Symbol) -> sp.Expr:
    """The printed formula as an expression, its names bound to the
    solution's symbols."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(printed).readline))
    except (tokenize.TokenError, SyntaxError) as e:
        raise UsageError(f"can't read the printed formula for {symbol}: {e}", symbol=symbol) from e
    for name in (token.string for token in tokens if token.type == tokenize.NAME):
        if name not in symbols and not _sympy_name(name):
            raise UsageError(
                f"the printed formula for {symbol} names {name},"
                " which isn't a symbol of the solution or a SymPy function or constant",
                symbol=symbol,
            )
    try:
        expr = parse_expr(printed, local_dict=dict(symbols))
    except (SyntaxError, tokenize.TokenError, TypeError, ValueError, AttributeError) as e:
        raise UsageError(f"can't read the printed formula for {symbol}: {e}", symbol=symbol) from e
    if not isinstance(expr, sp.Expr):
        raise UsageError(
            f"the printed formula for {symbol} is {expr!r}, not an expression", symbol=symbol
        )
    # A name can still make a symbol, as `Symbol("q")` would.
    strays = sorted(sym.name for sym in free_symbols(expr) if symbols.get(sym.name) != sym)
    strays += sorted(str(f.func) for f in expr.atoms(AppliedUndef))
    if strays:
        raise UsageError(
            f"the printed formula for {symbol} makes {', '.join(strays)},"
            " which isn't a symbol of the solution",
            symbol=symbol,
        )
    return expr


def _sympy_name(name: str) -> bool:
    """Whether SymPy defines `name` as a function, such as `sin` or `sqrt`,
    or as a constant, such as `pi`."""
    if keyword.iskeyword(name):
        return False
    value = getattr(sp, name, None)
    if isinstance(value, sp.Expr):
        return not value.free_symbols
    return callable(value)
