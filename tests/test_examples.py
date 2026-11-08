import importlib
import pkgutil

import pytest
import sympy as sp

import examples
from equarium import System, UsageError
from examples.answers import Answer
from examples.up_15e.ch02.example_2_4_handwritten import sol_a, v1, x1

x, D = sp.symbols("x D")


def example_modules() -> list[str]:
    """Every module under `examples/` named `example_…` or `exercise_…`."""
    return sorted(
        info.name
        for info in pkgutil.walk_packages(examples.__path__, prefix="examples.")
        if info.name.rsplit(".", 1)[-1].startswith(("example_", "exercise_"))
    )


@pytest.mark.parametrize("name", example_modules())
def test_book(name: str) -> None:
    module = importlib.import_module(name)
    book = getattr(module, "BOOK", None)
    assert book, f"{name} has no BOOK, or an empty one"
    assert all(isinstance(answer, Answer) for answer in book)
    mismatches = [message for answer in book if (message := answer.mismatch()) is not None]
    assert not mismatches, "\n".join(mismatches)


def test_the_examples_are_found() -> None:
    assert {
        "examples.up_15e.ch02.example_2_4_handwritten",
        "examples.up_15e.ch02.example_2_5_handwritten",
        "examples.up_15e.ch02.example_2_5_handwritten_step_by_step",
    } <= set(example_modules())
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
