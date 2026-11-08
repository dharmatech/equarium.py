"""Roots and filters: 2.7's four parts from one base, 2.8's two roots
and their pairs, 3.9's two roots, the refusals of `where`, and the
three small changes from the reviews of 001 to 003."""

from typing import Any

import pytest
import sympy as sp

from equarium import Solution, System, UsageError, eq_flat
from equarium.display import plain, render_history
from equarium.steps import EliminateZerosStep
from examples.answers import Answer
from examples.up_15e.ch02 import example_2_5_handwritten_step_by_step as ex_2_5_steps

import example_2_4


def matches(*answers: Answer) -> None:
    mismatches = [message for answer in answers if (message := answer.mismatch()) is not None]
    assert not mismatches, "\n".join(mismatches)


def formulas(solution: Solution, sym: sp.Symbol) -> set[str]:
    return {str(root.formula(sym)) for root in solution.roots}


def pairs(solution: Solution, first: sp.Symbol, second: sp.Symbol) -> set[tuple[float, float]]:
    return {
        (round(float(root.number(first)), 2), round(float(root.number(second)), 2))
        for root in solution.roots
    }


# 2.7: a ball thrown upward at 15.0 m/s from a roof railing, written out
# like 2.4. Its four parts branch from one base.

y0, y1, v0, v1, t0, t1, v_av, a = sp.symbols("y0 y1 v0 v1 t0 t1 v_av a")
D, x, y, z = sp.symbols("D x y z")

ball = (
    System()
    .add(sp.Eq(v_av, (y1 - y0) / (t1 - t0)), label="2.2")
    .add(sp.Eq(a, (v1 - v0) / (t1 - t0)), label="2.7")
    .add(sp.Eq(v_av, (v0 + v1) / 2), label="2.10")
    .known(t0, 0)  # s
    .known(y0, 0)  # m
    .eliminate_zeros()  # as the old script's zero equations
    .known(v0, 15.0)  # m/s
    .known(a, -9.8)  # m/s²
)
part_a = ball.known(t1, 1.0).want(y1, v1)


def test_2_7_a_at_1_s() -> None:
    sol = part_a.solve()
    assert formulas(sol, y1) == {"a*t1**2/2 + t1*v0"}
    assert formulas(sol, v1) == {"a*t1 + v0"}
    matches(Answer(sol, y1, "10.1"), Answer(sol, v1, "5.2"))  # m, m/s


def test_2_7_a_at_4_s_replaces_t1() -> None:
    sol = part_a.known(t1, 4.0).solve()
    matches(Answer(sol, y1, "-18.4"), Answer(sol, v1, "-24.2"))  # m, m/s
    assert part_a.knowns[t1] == 1.0


def test_2_7_b_two_roots() -> None:
    sol = ball.known(y1, 5.0).solve(v1)
    assert len(sol.roots) == 2
    assert formulas(sol, v1) == {"-sqrt(2*a*y1 + v0**2)", "sqrt(2*a*y1 + v0**2)"}
    matches(Answer(sol, v1, "-11.3", "11.3"))  # m/s


def test_2_7_c_maximum_height() -> None:
    sol = ball.known(v1, 0.0).solve(y1)
    # v1 became zero after eliminate_zeros(), so it stays a symbol.
    assert str(sol.formula(y1)) == "(-v0**2 + v1**2)/(2*a)"
    assert v1 in sol.formula(y1).free_symbols
    matches(Answer(sol, y1, "11.5"))  # m


def test_2_7_d_acceleration_at_the_top() -> None:
    assert ball.knowns[a] == -9.8  # m/s², the known a


# 2.8: when has the ball fallen 5.00 m below the railing?

fallen = ball.known(y1, -5.0)


def test_2_8_two_roots() -> None:
    sol = fallen.solve(t1)
    assert len(sol.roots) == 2
    matches(Answer(sol, t1, "3.36", "-0.30"))  # s
    with pytest.raises(UsageError, match="2 roots"):
        sol.number(t1)


def test_2_8_the_filter_keeps_the_positive_time() -> None:
    sol = fallen.solve(t1).where(t1 > 0)
    assert len(sol.roots) == 1
    matches(Answer(sol, t1, "3.36"))  # s
    assert abs(float(sol.number(t1)) - 3.3645) < 1e-4


def test_2_8_pairs() -> None:
    sol = fallen.solve(t1, v1)
    assert pairs(sol, t1, v1) == {(3.36, -17.97), (-0.3, 17.97)}
    assert pairs(sol.where((t1 > 0) & (v1 < 0)), t1, v1) == {(3.36, -17.97)}
    assert pairs(sol.where((t1 > 10) | (v1 > 0)), t1, v1) == {(-0.3, 17.97)}


def test_2_8_nothing_kept() -> None:
    sol = fallen.solve(t1).where(t1 > 10)
    assert sol.roots == ()
    assert sol.reason == "no root satisfies t1 > 10"


def test_where_keeps_the_system_the_time_and_the_order() -> None:
    sol = fallen.solve(t1, v1)
    kept = sol.where(v1 < 100)
    assert kept.roots == sol.roots
    assert kept.system is sol.system
    assert kept.elapsed == sol.elapsed
    assert kept.reason is None


def test_where_on_no_roots_returns_the_solution() -> None:
    sol = fallen.solve(t1).where(t1 > 10)
    assert sol.where(t1 > 0) is sol


# 3.9: a ball thrown from a window 8.0 m up, at 10.0 m/s and 20° below
# the horizontal, written out with polar to components only.

b0x, b1x, b0y, b1y, b0vx, b1vx, b0vy, b1vy, b0t, b1t = sp.symbols(
    "b0x b1x b0y b1y b0vx b1vx b0vy b1vy b0t b1t"
)
b_dt, b_vav_x, b_vav_y, b_a_x, b_a_y = sp.symbols("b_dt b_vav_x b_vav_y b_a_x b_a_y")
g, v_mag, angle = sp.symbols("g v_mag angle")

window = (
    System()
    # The seven, in the old physics code's order: (1) to (7).
    .add(
        sp.Eq(b_dt, b1t - b0t),
        sp.Eq(b_vav_x, (b1x - b0x) / b_dt),  # 2.2
        sp.Eq(b_vav_y, (b1y - b0y) / b_dt),
        sp.Eq(b_a_x, (b1vx - b0vx) / b_dt),  # 2.7
        sp.Eq(b_a_y, (b1vy - b0vy) / b_dt),
        sp.Eq(b_vav_x, (b0vx + b1vx) / 2),  # 2.10
        sp.Eq(b_vav_y, (b0vy + b1vy) / 2),
    )
    # Its fall, (8) and (9), and its launch, polar to components: (10), (11).
    .add(*eq_flat(b_a_y, -g, b0vx, b1vx))
    .add(*eq_flat(b0vx, v_mag * sp.cos(angle), b0vy, v_mag * sp.sin(angle)))
    .known({b0x: 0, b_a_x: 0, b0t: 0, b1y: 0})  # b1y: it hits the ground
    .eliminate_zeros()
    .known(g, 9.81)  # m/s²
    .known(b0y, 8.0)  # m
    .known(v_mag, 10.0)  # m/s
    .known(angle, sp.rad(-20))
)


def test_3_9_two_roots_and_the_filter() -> None:
    sol = window.solve(b1x)
    # The book prints 9.2 m, and the old script 9.16.
    matches(Answer(sol, b1x, "-15.7", "9.2"))  # m
    ahead = sol.where(b1x > 0)
    assert len(ahead.roots) == 1
    matches(Answer(ahead, b1x, "9.2"))  # m


def test_3_9_with_the_time() -> None:
    sol = window.solve(b1x, b1t).where(b1t > 0)
    assert len(sol.roots) == 1
    matches(Answer(sol, b1x, "9.2"), Answer(sol, b1t, "0.98"))  # m, s


# The refusals of `where`


def test_where_a_known_with_no_number() -> None:
    sol = ball.known(D).known(y1, -5.0).solve(t1)
    with pytest.raises(UsageError, match=r"t1 > D became .* > D"):
        sol.where(t1 > D)


def test_where_an_unknown_that_isnt_a_want() -> None:
    with pytest.raises(UsageError, match="v_av > 0 became v_av > 0"):
        fallen.solve(t1).where(v_av > 0)


def test_where_complex_roots() -> None:
    sol = System().add(sp.Eq(x**2, -4)).want(x).solve()
    with pytest.raises(UsageError, match="x > 0"):
        sol.where(x > 0)


@pytest.mark.parametrize("relation", [True, sp.true, t1], ids=["True", "sp.true", "t1"])
def test_where_not_a_relation(relation: Any) -> None:
    with pytest.raises(UsageError, match="where takes a SymPy relation"):
        fallen.solve(t1).where(relation)


# A formula that still contains unknowns


def test_unknowns_left_in_a_formula() -> None:
    sol = System().add(sp.Eq(x, y + z)).want(x).solve()
    assert sol.roots == ()
    assert sol.reason == "sp.solve left x in terms of the unknowns y, z"
    one = System().add(sp.Eq(x, 2 * y)).want(x).solve()
    assert one.reason == "sp.solve left x in terms of the unknown y"


def test_a_known_with_no_number_isnt_an_unknown() -> None:
    sol = System().add(sp.Eq(x, 2 * D)).known(D).want(x).solve()
    assert str(sol.formula(x)) == "2*D"


# eliminate_zeros lists only the new zeros, or those that still changed
# an equation.


def test_eliminate_zeros_lists_the_new_zeros() -> None:
    again = example_2_4.base.known(example_2_4.x0, 0).eliminate_zeros()
    assert isinstance(again.step, EliminateZerosStep)
    assert again.step.zeros == (example_2_4.x0,)
    assert again.fixed == {example_2_4.t0, example_2_4.x0}


def test_eliminate_zeros_again_lists_none() -> None:
    again = example_2_4.base.eliminate_zeros()
    assert again.step == EliminateZerosStep((), (), ())
    assert render_history(again, symbol=plain).splitlines()[-1] == "9. eliminate zeros: none"


def test_eliminate_zeros_lists_a_fixed_zero_that_rewrote_a_new_equation() -> None:
    x0, x1, t0 = example_2_4.x0, example_2_4.x1, example_2_4.t0
    again = example_2_4.base.add(sp.Eq(x1, x0 + t0)).eliminate_zeros()
    assert again.step == EliminateZerosStep((t0,), ("1",), ())
    assert again.equation("1").eq == sp.Eq(x1, x0)


def test_eliminate_zeros_in_the_step_by_step_history() -> None:
    lines = render_history(ex_2_5_steps.meet, symbol=plain).splitlines()
    assert lines[11] == "12. eliminate zeros m_0_t, p_0_t: into (1), (4), (5)"
    assert lines[13] == "14. eliminate zeros m_0_x: into (1)"
