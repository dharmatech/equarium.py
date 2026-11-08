"""The both-sides helpers, from the old `misc.py`."""

from typing import cast

import pytest
import sympy as sp

from equarium import UsageError
from equarium.equations import add_both_sides, multiply_both_sides

x, y = sp.symbols("x y")
x_is_y = cast(sp.Equality, sp.Eq(x, y))  # SymPy types Eq as a union


def test_add_both_sides() -> None:
    assert add_both_sides(x_is_y, 2) == sp.Eq(x + 2, y + 2)


def test_multiply_both_sides() -> None:
    assert multiply_both_sides(x_is_y, 3) == sp.Eq(3 * x, 3 * y)


def test_a_result_that_isnt_an_equation() -> None:
    # 0 = 0 evaluates to true, which misc.py returned.
    with pytest.raises(UsageError):
        multiply_both_sides(x_is_y, 0)
