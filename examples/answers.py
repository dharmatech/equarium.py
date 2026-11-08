"""The book's answers, written beside each example, and how they match.

An example module keeps a `BOOK: list[Answer]`, and `tests/test_examples.py`
checks every one.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

import sympy as sp

from equarium import Solution, UsageError


@dataclass(frozen=True, init=False)
class Answer:
    """The values a book prints for one symbol of a solution.

    `Answer(sol_a, x1, "43")`, or `Answer(sol, v1, "-11.3", "11.3")` for a
    solution with two roots. The printed values are strings, as the book
    prints them, since the last digit sets the tolerance.
    """

    solution: Solution
    symbol: sp.Symbol
    printed: tuple[str, ...]

    def __init__(self, solution: Solution, symbol: sp.Symbol, *printed: str) -> None:
        if symbol not in solution.system.wants:
            raise UsageError(f"{symbol} isn't a want of the solution", symbol=symbol)
        if not printed:
            raise UsageError(f"no printed value for {symbol}", symbol=symbol)
        for value in printed:
            _decimal(value)
        object.__setattr__(self, "solution", solution)
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "printed", printed)

    def mismatch(self) -> str | None:
        """None when the solution's numbers match the printed values, and
        otherwise what differs.

        They match when every root's number is real, and the numbers,
        sorted, pair one to one with the printed values, sorted, each
        within half a unit in the printed value's last digit.
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
