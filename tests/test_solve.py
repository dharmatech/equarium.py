from dataclasses import FrozenInstanceError
from typing import Any

import pytest
import sympy as sp

from equarium import Solution, System, UsageError, all_at_once
from equarium.steps import WantStep
from examples.up_15e.ch02.examples.n05 import main_handwritten as ex_2_5
from examples.up_15e.ch02.examples.n04.main_handwritten import (
    a,
    motorcycle,
    part_a,
    sol_a,
    sol_b,
    t1,
    v0,
    v1,
    x0,
    x1,
)

x, y = sp.symbols("x y")


def formulas(solution: Solution) -> list[str]:
    (root,) = solution.roots
    return [str(formula) for formula in root.formulas.values()]


def numbers(solution: Solution) -> list[float]:
    (root,) = solution.roots
    return [float(number) for number in root.numbers.values()]


def two_roots() -> Solution:
    return System().add(sp.Eq(x**2, 4)).want(x).solve()


# 2.4 and 2.5


def test_2_4_a() -> None:
    assert formulas(sol_a) == ["a*t1**2/2 + t1*v0 + x0", "a*t1 + v0"]
    assert numbers(sol_a) == [43.0, 23.0]
    assert sol_a.number(x1) == 43.0
    assert sol_a.number(v1) == 23.0
    assert str(sol_a.formula(x1)) == "a*t1**2/2 + t1*v0 + x0"
    assert sol_a.system is part_a
    assert sol_a.reason is None


def test_2_4_a_formulas_keep_the_knowns_as_symbols() -> None:
    (root,) = sol_a.roots
    assert list(root.formulas) == [x1, v1]
    assert root.formula(x1).free_symbols == {a, t1, v0, x0}


def test_2_4_b() -> None:
    assert formulas(sol_b) == ["(2*a*x0 - v0**2 + v1**2)/(2*a)"]
    assert numbers(sol_b) == [55.0]
    assert sol_b.system.wants == (x1,)
    assert sol_b.system.step == WantStep((x1,))
    assert sol_b.system.previous == motorcycle.known(v1, 25)


def test_2_5() -> None:
    assert formulas(ex_2_5.sol) == ["2*m_v/p_a", "2*m_v", "2*m_v**2/p_a"]
    assert numbers(ex_2_5.sol) == [10.0, 30.0, 150.0]
    assert ex_2_5.sol.system.wants == (ex_2_5.t_01, ex_2_5.p_1_v, ex_2_5.dist)


# Wants


def test_no_wants() -> None:
    with pytest.raises(UsageError):
        motorcycle.solve()


def test_no_wants_raises_before_the_strategy() -> None:
    def strategy(system: System) -> Solution:
        raise AssertionError("the strategy ran")

    with pytest.raises(UsageError):
        motorcycle.solve(strategy=strategy)


def test_wants_given_to_solve_replace_the_systems() -> None:
    solution = part_a.solve(v1)
    assert solution.system.wants == (v1,)
    assert solution.system.previous is part_a
    assert numbers(solution) == [23.0]


def test_a_known_given_as_a_want() -> None:
    with pytest.raises(UsageError):
        part_a.solve(t1)


def test_strategy() -> None:
    solved: list[System] = []

    def strategy(system: System) -> Solution:
        solved.append(system)
        return all_at_once(system)

    assert part_a.solve(strategy=strategy) == sol_a
    assert solved == [part_a]


# No roots


def test_no_roots() -> None:
    solution = System().add(sp.Eq(x + y, 1), sp.Eq(x + y, 2)).want(x).solve()
    assert solution.roots == ()
    assert solution.reason == "sp.solve found no roots"


def test_not_implemented() -> None:
    solution = System().add(sp.Eq(x, sp.cos(x))).want(x).solve()
    assert solution.roots == ()
    assert solution.reason == "sp.solve: could not solve x - cos(x)"


def test_undetermined() -> None:
    solution = motorcycle.want(x1, v1).solve()  # no t1
    assert solution.roots == ()
    assert solution.reason == "sp.solve left x1 undetermined"


def test_no_roots_number() -> None:
    solution = System().add(sp.Eq(x + y, 1), sp.Eq(x + y, 2)).want(x).solve()
    with pytest.raises(UsageError, match="0 roots"):
        solution.number(x)


# Several roots


def test_several_roots() -> None:
    solution = two_roots()
    assert len(solution.roots) == 2
    assert {float(root.number(x)) for root in solution.roots} == {-2.0, 2.0}
    with pytest.raises(UsageError, match="2 roots"):
        solution.number(x)
    with pytest.raises(UsageError, match="2 roots"):
        solution.formula(x)
    with pytest.raises(UsageError):
        solution.roots[0].formula(y)
    with pytest.raises(UsageError):
        solution.roots[0].number(y)
    assert isinstance(solution.elapsed, float)
    assert solution.elapsed >= 0


# Values


def test_a_known_with_no_number_stays_a_symbol() -> None:
    D = sp.Symbol("D")
    solution = System().add(sp.Eq(x, 2 * D + y), sp.Eq(y, 3)).known(D).want(x).solve()
    assert str(solution.formula(x)) == "2*D + 3"
    assert str(solution.number(x)) == "2.0*D + 3.0"


def test_solutions_are_immutable() -> None:
    solution: Any = sol_a
    with pytest.raises(FrozenInstanceError):
        solution.roots = ()
    root: Any = sol_a.roots[0]
    with pytest.raises(TypeError):
        root.formulas[x1] = x0
    with pytest.raises(TypeError):
        root.numbers[x1] = v0


def test_equality_leaves_out_the_time() -> None:
    assert part_a.solve() == sol_a


def test_reason_exactly_when_no_roots() -> None:
    with pytest.raises(UsageError):
        Solution(part_a, (), 0.0)
    with pytest.raises(UsageError):
        Solution(part_a, sol_a.roots, 0.0, "a reason")
