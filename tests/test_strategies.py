"""`eliminating`: 3.9 and 4.1 with the two-way polar equations, which
`all_at_once` alone can't solve, and the strategy's edges."""

import re

import pytest
import sympy as sp
from sympy.logic.boolalg import BooleanAtom

from equarium import System, UsageError, all_at_once, eliminating, eq_flat
from equarium.display import plain, render_history, render_solution
from equarium.steps import EliminateStep
from examples.answers import Answer
from examples.up_15e.ch02.example_2_4_handwritten import part_a, sol_a, v1, x1


def matches(*answers: Answer) -> None:
    mismatches = [message for answer in answers if (message := answer.mismatch()) is not None]
    assert not mismatches, "\n".join(mismatches)


def eliminated(system: System) -> list[sp.Symbol]:
    """The symbols the system's history eliminated, in order."""
    found: list[sp.Symbol] = []
    current: System | None = system
    while current is not None:
        if isinstance(current.step, EliminateStep):
            found.append(current.step.symbol)
        current = current.previous
    return found[::-1]


# 3.9: a ball thrown from a window 8.0 m up, at 10.0 m/s and 20° below
# the horizontal, written out as in test_roots.py, with the two-way polar
# equations: the old `magnitude_and_angle_equations`.

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
    # Its fall, (8) and (9), and its launch, both ways: (10) to (13).
    .add(*eq_flat(b_a_y, -g, b0vx, b1vx))
    .add(
        *eq_flat(
            b0vx, v_mag * sp.cos(angle),
            b0vy, v_mag * sp.sin(angle),
            v_mag, sp.sqrt(b0vx**2 + b0vy**2),
            angle, sp.atan2(b0vy, b0vx),
        )
    )
    .known({b0x: 0, b_a_x: 0, b0t: 0, b1y: 0})  # b1y: it hits the ground
    .eliminate_zeros()
    .known(g, 9.81)  # m/s²
    .known(b0y, 8.0)  # m
    .known(v_mag, 10.0)  # m/s
    .known(angle, sp.rad(-20))
    .want(b1x)
)


def test_3_9_all_at_once_finds_no_roots() -> None:
    sol = window.solve()
    assert sol.roots == ()
    assert sol.reason == "sp.solve found no roots"


@pytest.mark.slow
def test_3_9_eliminating() -> None:  # about 6 s
    sol = window.solve(strategy=eliminating())
    # The book prints 9.2 m, and the old script 9.16.
    matches(Answer(sol, b1x, "-15.7", "9.2"))  # m
    matches(Answer(sol.where(b1x > 0), b1x, "9.2"))  # m
    assert render_history(sol.system, symbol=plain).splitlines()[-7:] == [
        "11. eliminate b1t using (1)",
        "12. eliminate b1vy using (5): into (7)",
        "13. eliminate b_a_y using (8): into (7)",
        "14. eliminate b_vav_y using (3): into (7)",
        "15. eliminate b1vx using (4): into (6), dropped (9)",
        "16. eliminate b0vx using (6): into (10), (12), (13)",
        "17. eliminate b0vy using (11): into (7), (12), (13)",
    ]
    last = render_solution(sol, symbol=plain).splitlines()[-1]
    assert re.fullmatch(r"time: \d+\.\d\d s", last)


def test_3_9_giving_up() -> None:
    sol = window.solve(strategy=eliminating(max_eliminations=1))
    assert sol.roots == ()
    assert sol.reason == "sp.solve found no roots, after 1 elimination"
    assert render_history(sol.system, symbol=plain).splitlines()[-1] == (
        "11. eliminate b1t using (1)"
    )


def test_no_eliminations_is_all_at_once() -> None:
    none = eliminating(max_eliminations=0)
    assert window.solve(strategy=none) == window.solve(strategy=all_at_once)
    sol = part_a.solve(strategy=none)
    assert sol == part_a.solve(strategy=all_at_once)
    assert [sol.number(x1), sol.number(v1)] == [43.0, 23.0]


def test_eliminating_when_all_at_once_succeeds() -> None:
    sol = part_a.solve(strategy=eliminating())
    assert sol == sol_a
    assert sol.system is part_a


def test_a_negative_count() -> None:
    with pytest.raises(UsageError, match="max_eliminations"):
        eliminating(-1)


# 4.1: three wrestlers pull on a belt, with 50 N at 0°, 120 N at 270° and
# 250 N at 127°. Written out as the old v1-003, with the two-way polar
# equations for every force and for the net force R: (1) to (19).

F1_x, F1_y, F1_mag, F1_angle = sp.symbols("F1_x F1_y F1_mag F1_angle")
F2_x, F2_y, F2_mag, F2_angle = sp.symbols("F2_x F2_y F2_mag F2_angle")
F3_x, F3_y, F3_mag, F3_angle = sp.symbols("F3_x F3_y F3_mag F3_angle")
R_x, R_y, R_mag, R_angle = sp.symbols("R_x R_y R_mag R_angle")
R_angle_deg = sp.Symbol("R_angle_deg")


def polar(
    x: sp.Symbol, y: sp.Symbol, mag: sp.Symbol, angle: sp.Symbol
) -> list[sp.Equality | BooleanAtom]:
    """The old `force_equations`: components to polar and back."""
    return eq_flat(
        x, mag * sp.cos(angle),
        y, mag * sp.sin(angle),
        mag, sp.sqrt(x**2 + y**2),
        angle, sp.atan2(y, x),
    )


belt = (
    System()
    .add(*eq_flat(R_x, F1_x + F2_x + F3_x, R_y, F1_y + F2_y + F3_y))
    .add(*polar(F1_x, F1_y, F1_mag, F1_angle))
    .add(*polar(F2_x, F2_y, F2_mag, F2_angle))
    .add(*polar(F3_x, F3_y, F3_mag, F3_angle))
    .add(*polar(R_x, R_y, R_mag, R_angle))
    .add(sp.Eq(R_angle_deg, sp.deg(R_angle)))
    .known({F1_mag: 50, F1_angle: 0})  # N
    .known({F2_mag: 120, F2_angle: 3 * sp.pi / 2})
    .known({F3_mag: 250, F3_angle: sp.rad(127)})
)

# Not tested: |R|, the angle, and all four wants at once. The old v1-003,
# run again on 2026-11-08, "solves" them as formulas in other unknowns,
# not numbers, and then fails:
#
#     R_mag = sqrt(R_x**2 + R_y**2)
#     R_angle = atan2(R_y, R_x)
#     R_angle_deg: ValueError: No solutions found.
#
# Its 128.2 N and 141.6° come from the one-way versions, v1-006 and
# v1-007. Here `all_at_once` refuses such a formula ("left R_mag in terms
# of the unknowns R_x, R_y"), so `eliminating` goes on, and `sp.solve`
# never returned: |R| ran 20 minutes, and all four wants 25 minutes.


@pytest.mark.slow
def test_4_1_R_x() -> None:  # about 90 s; the old run took 87 s
    sol = belt.solve(R_x, strategy=eliminating())
    assert eliminated(sol.system) == [R_angle_deg, F1_y, F2_y, F3_y]
    assert str(sol.formula(R_x)) == (
        "F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)"
    )
    matches(Answer(sol, R_x, "-100.45"))  # N, the old script's number


@pytest.mark.slow
def test_4_1_R_y() -> None:  # about 210 s; the old run took 224 s
    sol = belt.solve(R_y, strategy=eliminating())
    assert eliminated(sol.system) == [R_angle_deg, F1_x, F2_x, F3_x, R_angle, R_mag, R_x]
    assert str(sol.formula(R_y)) == (
        "F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)"
    )
    matches(Answer(sol, R_y, "79.66"))  # N, the old script's number
