import importlib
import pkgutil
from typing import Any, cast

import pytest
import sympy as sp

import examples
from equarium import System, UsageError
from examples.answers import Answer, Formula
from examples.up_15e.ch02.examples.n04.main_handwritten import sol_a, v1, x1
from slow_examples import SLOW_EXAMPLES

x, D, a, b = sp.symbols("x D a b")


def example_modules() -> list[str]:
    """Every module in a problem's folder: in a chapter's `examples/` or
    `exercises/`, such as `examples.up_15e.ch02.examples.n04.main`."""
    return sorted(
        info.name
        for info in pkgutil.walk_packages(examples.__path__, prefix="examples.")
        if not info.ispkg and info.name.split(".")[-3:-2] in (["examples"], ["exercises"])
    )


@pytest.mark.parametrize(
    "name",
    [
        pytest.param(name, marks=[pytest.mark.slow] if name in SLOW_EXAMPLES else [])
        for name in example_modules()
    ],
)
def test_book(name: str) -> None:
    module = importlib.import_module(name)
    book = getattr(module, "BOOK", None)
    assert book, f"{name} has no BOOK, or an empty one"
    assert all(isinstance(answer, Answer | Formula) for answer in book)
    mismatches = [message for answer in book if (message := answer.mismatch()) is not None]
    assert not mismatches, "\n".join(mismatches)


def test_the_examples_are_found() -> None:
    assert {
        "examples.up_15e.ch02.examples.n04.main_handwritten",
        "examples.up_15e.ch02.examples.n05.main_handwritten",
        "examples.up_15e.ch02.examples.n05.main_handwritten_step_by_step",
        "examples.up_15e.ch02.examples.n04.main",
        "examples.up_15e.ch02.examples.n05.main",
        "examples.up_15e.ch02.examples.n05.main_step_by_step",
        "examples.up_15e.ch02.examples.n06.main",
        "examples.up_15e.ch02.examples.n07.main",
        "examples.up_15e.ch02.examples.n08.main",
        "examples.up_15e.ch02.exercises.n001.main",
        "examples.up_15e.ch02.exercises.n003.main",
        "examples.up_15e.ch02.exercises.n003.main_two_steps",
        "examples.up_15e.ch02.exercises.n005.main",
        "examples.up_15e.ch02.exercises.n019.main",
        "examples.up_15e.ch02.exercises.n021.main",
        "examples.up_15e.ch02.exercises.n023.main",
        "examples.up_15e.ch03.examples.n06.main",
        "examples.up_15e.ch03.examples.n07.main",
        "examples.up_15e.ch03.examples.n08.main",
        "examples.up_15e.ch03.examples.n09.main",
        "examples.up_15e.ch03.examples.n10.main",
        "examples.up_15e.ch03.examples.n13.main",
        "examples.up_15e.ch04.examples.n01.main",
        "examples.up_15e.ch04.examples.n01.main_step_by_step",
        "examples.up_15e.ch04.examples.n04.main",
        "examples.up_15e.ch04.examples.n05.main",
        "examples.up_15e.ch04.examples.n05.main_two_steps",
        "examples.up_15e.ch04.examples.n07.main",
    } <= set(example_modules())
    assert SLOW_EXAMPLES <= set(example_modules())
    assert "examples.up_15e.ch02.tables.n05.main" not in example_modules()
    assert "examples.answers" not in example_modules()


# Answer


def solve_x(value: sp.Expr | float) -> System:
    return System().add(sp.Eq(x, value)).want(x)


def test_matches() -> None:
    assert Answer(sol_a, x1, "43").mismatch() is None
    assert Answer(sol_a, x1, "43.0").mismatch() is None
    assert Answer(sol_a, v1, "23").mismatch() is None


def test_wrong_value() -> None:
    message = Answer(sol_a, x1, "44").mismatch()
    assert message is not None
    assert "x1" in message and "44" in message and "43.0" in message


def test_wrong_count() -> None:
    message = Answer(sol_a, x1, "43", "1").mismatch()
    assert message is not None
    assert "x1" in message and "43, 1" in message and "43.0" in message


def test_two_roots_in_either_order() -> None:
    solution = System().add(sp.Eq(x**2, 4)).want(x).solve()
    assert Answer(solution, x, "2", "-2").mismatch() is None
    assert Answer(solution, x, "-2", "2").mismatch() is None
    assert Answer(solution, x, "2").mismatch() is not None


def test_free_symbol() -> None:
    solution = System().add(sp.Eq(x, 2 * D)).known(D).want(x).solve()
    message = Answer(solution, x, "2").mismatch()
    assert message is not None
    assert "2.0*D" in message


def test_complex() -> None:
    solution = System().add(sp.Eq(x**2, -4)).want(x).solve()
    assert Answer(solution, x, "2", "-2").mismatch() is not None


def test_no_roots() -> None:
    solution = System().add(sp.Eq(x + D, 1), sp.Eq(x + D, 2)).want(x).solve()
    message = Answer(solution, x, "1").mismatch()
    assert message is not None
    assert "no roots" in message


def test_half_a_unit_in_the_last_digit() -> None:
    assert Answer(solve_x(sp.Rational(87, 2)).solve(), x, "43").mismatch() is None  # 43.5
    assert Answer(solve_x(sp.Rational(87, 2)).solve(), x, "43.0").mismatch() is not None
    assert Answer(solve_x(1.704).solve(), x, "1.70").mismatch() is None
    assert Answer(solve_x(1.706).solve(), x, "1.70").mismatch() is not None
    # -11.25 is exact in binary, and so is the half unit as a Decimal,
    # so the boundary is inclusive exactly.
    assert Answer(solve_x(sp.Rational(-45, 4)).solve(), x, "-11.3").mismatch() is None
    assert Answer(solve_x(sp.Rational(-45, 4)).solve(), x, "-11.30").mismatch() is not None


def test_misuse() -> None:
    with pytest.raises(UsageError):
        Answer(sol_a, D, "43")  # not a want
    with pytest.raises(UsageError):
        Answer(sol_a, x1)  # nothing printed
    with pytest.raises(UsageError):
        Answer(sol_a, x1, "forty")
    with pytest.raises(UsageError):
        Answer(sol_a, x1, "NaN")


# Formula

# x = 2*sin(a)*cos(a), with a known and no number.
double = System().add(sp.Eq(x, 2 * sp.sin(a) * sp.cos(a))).known(a).want(x).solve()


def test_formula_matches() -> None:
    assert str(double.formula(x)) == "2*sin(a)*cos(a)"
    assert Formula(double, x, 2 * sp.sin(a) * sp.cos(a)).mismatch() is None  # verbatim
    assert Formula(double, x, sp.sin(2 * a)).mismatch() is None  # equivalent


def test_formula_differs() -> None:
    message = Formula(double, x, sp.cos(2 * a)).mismatch()
    assert message is not None
    assert "x" in message and "cos(2*a)" in message and "2*sin(a)*cos(a)" in message


def test_formula_several_roots() -> None:
    solution = System().add(sp.Eq(x**2, a)).known(a).want(x).solve()
    message = Formula(solution, x, sp.sqrt(a)).mismatch()
    assert message is not None
    assert "2 roots" in message and "-sqrt(a)" in message


def test_formula_no_roots() -> None:
    solution = System().add(sp.Eq(x + D, 1), sp.Eq(x + D, 2)).want(x).solve()
    message = Formula(solution, x, 1 - D).mismatch()
    assert message is not None
    assert "no roots" in message


def test_formula_a_printed_symbol_not_in_the_formula() -> None:
    solution = System().add(sp.Eq(x, 2 * a)).known(a).known(D).want(x).solve()
    message = Formula(solution, x, 2 * a * D).mismatch()
    assert message is not None
    assert "has no D" in message


def test_formula_misuse() -> None:
    with pytest.raises(UsageError, match="isn't a want"):
        Formula(double, a, a)  # a known, not a want
    with pytest.raises(UsageError, match="has b, which isn't a symbol of the solution"):
        Formula(double, x, sp.sin(2 * b))
    with pytest.raises(UsageError, match="an expression"):
        Formula(double, x, cast(Any, "sin(2*a)"))  # text
    with pytest.raises(UsageError, match="an expression"):
        Formula(double, x, cast(Any, a > 0))  # a relation
