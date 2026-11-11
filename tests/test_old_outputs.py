"""The ports against the old scripts: every formula the catalog quotes for
a ported script's want, verbatim, and its number, by value. The physics
layer's symbols are renamed back to the old names first, with `old_name`.
The names a script made itself, such as 3.6's `dist`, 2.5's `t_01` and
4.5's `m`, are renamed back through the module's map, `SCRIPT_NAMES`.

The old output is as `docs/design/implementation/001-example-catalog/catalog.md`
quotes it, from the old scripts run on 2026-11-08. The differences that
checkpoints 007 and 008 list are expected:

- the old scripts printed `formula.subs(values)`, so an exact number
  printed as `43`, where equarium's number is `sp.N` of it, `43.0000000000000`.
  So the numbers compare by value, within 1e-9 relative;
- 2.4's knowns have units since 2026-11-10, where the old script's were
  plain numbers. Its rows give the old numbers in the port's units,
  `43*meter` for the printed `43`;
- the additions (2.6's velocities at 2.0 s and 3.0 s, 2.3's `longer`, the
  new wants of chapters 3 and 4, 4.1's book step, 4.5's second step) have
  no old output. Their `BOOK`s check them;
- 3.7, 3.9 and 4.7 use the book's givens. For their rows, the number is
  the port's formula with the old givens, `OLD_GIVENS`, in place of the
  port's, so every other given is still checked against the old script's;
- 3.8's range isn't a row: the old line is a bug, and the `BOOK`'s
  `Formula` checks the fixed one. 3.8 printed no numbers;
- displayed equations keep equarium's sides. 3.10's show-that, the old
  last line, has its sides the other way round, and its test says so;
- 3.6's five rows that the projectile setup changed, in increment 005 of
  the 004 series. The port derives v1x, which the old script gave.
  `RESHAPED` has their new formulas, and the numbers are the old ones.

The slow modules are imported only inside their tests.
"""

import importlib
import math
import re
from typing import cast

import pytest
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.physics.units import Quantity, hour, kilometer, meter, newton, second

from equarium import Solution, System
from equarium.physics import Var
from old_names import SCRIPT_NAMES, old_name, old_str
from slow_examples import SLOW_EXAMPLES

UNITS = {"meter": meter, "second": second, "kilometer": kilometer, "hour": hour}

# 4.1's |R| and angle, which two of its scripts print.
R_MAG_4_1 = (
    "sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle)"
    " + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2"
    " + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)"
)
R_ANGLE_4_1 = (
    "atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle),"
    " F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))"
)

# The old givens that differ from the port's, which uses the book's:
# a known's name and the old script's value.
OLD_GIVENS: dict[str, dict[str, sp.Expr | float]] = {
    "ch03.examples.n07.main": {"g": 9.81},
    "ch03.examples.n09.main": {"g": 9.81},
    "ch04.examples.n07.main": {"w": 2.45e4 * newton, "g": 9.81 * meter / second**2},
}

# (module, solution, want, the old formula, the old number), as printed.
# The module is under `examples.up_15e`.
OLD: list[tuple[str, str, str, str, str | None]] = [
    # Example 2.4, v4-001
    ("ch02.examples.n04.main", "sol_a", "m_1_x", "a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x", "43*meter"),
    ("ch02.examples.n04.main", "sol_a", "m_1_v_x", "a_x_m_0_1*m_1_t + m_0_v_x", "23*meter/second"),
    (
        "ch02.examples.n04.main",
        "sol_b",
        "m_1_x",
        "(2*a_x_m_0_1*m_0_x - m_0_v_x**2 + m_1_v_x**2)/(2*a_x_m_0_1)",
        "55*meter",
    ),
    # Example 2.5, v4-000
    ("ch02.examples.n05.main", "sol", "t_01", "2*m_v/a_x_p_0_1", "10"),
    ("ch02.examples.n05.main", "sol", "p_1_v_x", "2*m_v", "30"),
    ("ch02.examples.n05.main", "sol", "dist", "2*m_v**2/a_x_p_0_1", "150"),
    # Example 2.5, v4-002
    ("ch02.examples.n05.main_step_by_step", "sol", "t_01", "2*m_v/a_x_p_0_1", "10"),
    ("ch02.examples.n05.main_step_by_step", "sol", "p_1_v_x", "2*m_v", "30"),
    ("ch02.examples.n05.main_step_by_step", "sol", "dist", "2*m_v**2/a_x_p_0_1", "150"),
    # Example 2.6, v2-000
    ("ch02.examples.n06.main", "sol_1", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-4.90000000000000"),
    ("ch02.examples.n06.main", "sol_1", "c_1_v_y", "a_y_c_0_1*c_1_t", "-9.80000000000000"),
    ("ch02.examples.n06.main", "sol_2", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-19.6000000000000"),
    ("ch02.examples.n06.main", "sol_3", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-44.1000000000000"),
    # Example 2.7, v1-000
    ("ch02.examples.n07.main", "sol_a1", "b_1_y", "b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2", "10.1000000000000"),
    ("ch02.examples.n07.main", "sol_a1", "b_1_v_y", "a_y_b_0_1*b_1_t + b_0_v_y", "5.20000000000000"),
    ("ch02.examples.n07.main", "sol_a4", "b_1_y", "b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2", "-18.4000000000000"),
    ("ch02.examples.n07.main", "sol_a4", "b_1_v_y", "a_y_b_0_1*b_1_t + b_0_v_y", "-24.2000000000000"),
    ("ch02.examples.n07.main", "sol_b", "b_1_v_y", "-sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)", "-11.2694276695846"),
    ("ch02.examples.n07.main", "sol_b", "b_1_v_y", "sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)", "11.2694276695846"),
    ("ch02.examples.n07.main", "sol_c", "b_1_y", "(-b_0_v_y**2 + b_1_v_y**2)/(2*a_y_b_0_1)", "11.4795918367347"),
    # Example 2.8, the end of 2.7's v1-000
    (
        "ch02.examples.n08.main",
        "sol",
        "b_1_t",
        "(-b_0_v_y - sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1",
        "3.36451028118484",
    ),
    (
        "ch02.examples.n08.main",
        "sol",
        "b_1_t",
        "(-b_0_v_y + sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1",
        "-0.303285791388921",
    ),
    # Exercise 2.1, 000
    (
        "ch02.exercises.n001.main",
        "sol",
        "c_1_x",
        "-c_0_t*v_av_x_c_0_1 + c_0_x + c_1_t*v_av_x_c_0_1",
        "25.0*meter",
    ),
    # Exercise 2.3, 002
    (
        "ch02.exercises.n003.main",
        "sol",
        "cb_1_t",
        "(-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1 + cb_0_t*v_av_x_cb_0_1"
        " - cb_0_x)/v_av_x_cb_0_1",
        "2.75*hour",
    ),
    # Exercise 2.3, 000
    (
        "ch02.exercises.n003.main_two_steps",
        "distance",
        "ca_1_x",
        "-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1",
        "192.5*kilometer",
    ),
    (
        "ch02.exercises.n003.main_two_steps",
        "slow",
        "cb_1_t",
        "(cb_0_t*v_av_x_cb_0_1 - cb_0_x + cb_1_x)/v_av_x_cb_0_1",
        "2.75*hour",
    ),
    # Exercise 2.5, 001
    (
        "ch02.exercises.n005.main",
        "sol",
        "avg_vel_02",
        "(dx_p_0_1 + dx_p_1_2)/(dt_p_0_1 + dt_p_1_2)",
        "0.3125*meter/second",
    ),
    (
        "ch02.exercises.n005.main",
        "sol",
        "avg_speed_02",
        "(Abs(dx_p_0_1) + Abs(dx_p_1_2))/(dt_p_0_1 + dt_p_1_2)",
        "1.5625*meter/second",
    ),
    # Exercise 2.19, 000
    (
        "ch02.exercises.n019.main",
        "sol_a",
        "o_0_v_x",
        "(-dt_o_0_1*o_1_v_x - 2*o_0_x + 2*o_1_x)/dt_o_0_1",
        "8.33333333333333*meter/second",
    ),
    (
        "ch02.exercises.n019.main",
        "sol_b",
        "a_x_o_0_1",
        "(2*dt_o_0_1*o_1_v_x + 2*o_0_x - 2*o_1_x)/dt_o_0_1**2",
        "1.11111111111111*meter/second**2",
    ),
    # Exercise 2.21, 000
    (
        "ch02.exercises.n021.main",
        "sol_a",
        "a_x_b_0_1",
        "(b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))",
        "675.0*meter/second**2",
    ),
    (
        "ch02.exercises.n021.main",
        "sol_b",
        "dt_b_0_1",
        "2*(-b_0_x + b_1_x)/(b_0_v_x + b_1_v_x)",
        "0.0666666666666667*second",
    ),
    # Exercise 2.23, 000
    (
        "ch02.exercises.n023.main",
        "sol",
        "b_1_x",
        "(2*a_x_b_0_1*b_0_x - b_0_v_x**2 + b_1_v_x**2)/(2*a_x_b_0_1)",
        "22.05*kilometer**2*second**2/(hour**2*meter)",
    ),
    # Example 3.6, v1-000
    ("ch03.examples.n06.main", "sol", "m_1_x", "m_1_t*(m_0_v_x + m_1_v_x)/2", "4.50000000000000"),
    ("ch03.examples.n06.main", "sol", "m_1_y", "m_1_t*(-g*m_1_t + 2*m_0_v_y)/2", "-1.22500000000000"),
    (
        "ch03.examples.n06.main",
        "sol",
        "dist",
        "sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2",
        "4.66375653309647",
    ),
    (
        "ch03.examples.n06.main",
        "sol",
        "vel_mag",
        "sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)",
        "10.2474387043788",
    ),
    (
        "ch03.examples.n06.main",
        "sol",
        "vel_angle",
        "atan2(-g*m_1_t + m_0_v_y, m_1_v_x)",
        "-0.498567905638218",
    ),
    (
        "ch03.examples.n06.main",
        "sol",
        "vel_angle_deg",
        "180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi",
        "-28.5658367937466",
    ),
    # Example 3.7, v1-000, with the old g
    (
        "ch03.examples.n07.main",
        "sol_a",
        "b_1_x",
        "b0_vel_mag*b_1_t*cos(b0_vel_angle)",
        "44.4310966741154",
    ),
    (
        "ch03.examples.n07.main",
        "sol_a",
        "b_1_y",
        "b_1_t*(2*b0_vel_mag*sin(b0_vel_angle) - b_1_t*g)/2",
        "39.5566647280447",
    ),
    ("ch03.examples.n07.main", "sol_a", "b_1_v_x", "b0_vel_mag*cos(b0_vel_angle)", "22.2155483370577"),
    (
        "ch03.examples.n07.main",
        "sol_a",
        "b_1_v_y",
        "b0_vel_mag*sin(b0_vel_angle) - b_1_t*g",
        "9.96833236402236",
    ),
    (
        "ch03.examples.n07.main",
        "sol_a",
        "b1_vel_mag",
        "sqrt(b0_vel_mag**2 - 2*b0_vel_mag*b_1_t*g*sin(b0_vel_angle) + b_1_t**2*g**2)",
        "24.3495018026193",
    ),
    (
        "ch03.examples.n07.main",
        "sol_a_radians",
        "b1_vel_angle",
        "atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))",
        "0.421780406158419",
    ),
    (
        "ch03.examples.n07.main",
        "sol_a",
        "b1_vel_angle_deg",
        "180*atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))/pi",
        "24.1662371541911",
    ),
    ("ch03.examples.n07.main", "sol_b", "b_1_t", "b0_vel_mag*sin(b0_vel_angle)/g", "3.01613989439575"),
    (
        "ch03.examples.n07.main",
        "sol_b",
        "b_1_y",
        "b0_vel_mag**2*sin(b0_vel_angle)**2/(2*g)",
        "44.6212748258844",
    ),
    (
        "ch03.examples.n07.main",
        "sol_c",
        "b_1_x",
        "b0_vel_mag**2*sin(2*b0_vel_angle)/g",
        "134.010403230554",
    ),
    ("ch03.examples.n07.main", "sol_c", "b_1_v_x", "b0_vel_mag*cos(b0_vel_angle)", "22.2155483370577"),
    ("ch03.examples.n07.main", "sol_c", "b_1_v_y", "-b0_vel_mag*sin(b0_vel_angle)", "-29.5883323640224"),
    # Example 3.8, v1-000, formulas only. Its range is the old bug: not a row.
    ("ch03.examples.n08.main", "sol_top", "p_1_y", "p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)", None),
    # Example 3.9, v2, with the old g
    (
        "ch03.examples.n09.main",
        "sol",
        "b_1_x",
        "b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2"
        " + 2*b_0_y*g))*cos(b_0_v_angle)/g",
        "-15.7161745661753",
    ),
    (
        "ch03.examples.n09.main",
        "sol",
        "b_1_x",
        "b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2"
        " + 2*b_0_y*g))*cos(b_0_v_angle)/g",
        "9.16380341748480",
    ),
    # Example 3.13, 001-eq
    ("ch03.examples.n13.main", "sol", "v_TY", "v_TE - v_YE", "-192.0*kilometer/hour"),
    ("ch03.examples.n13.main", "sol", "v_YT", "-v_TE + v_YE", "192.0*kilometer/hour"),
    # Example 4.1, v1-007
    ("ch04.examples.n01.main", "sol", "R_mag", R_MAG_4_1, "128.204889993952"),
    ("ch04.examples.n01.main", "sol", "R_angle", R_ANGLE_4_1, "2.47114041353915"),
    ("ch04.examples.n01.main", "sol", "R_angle_deg", f"180*{R_ANGLE_4_1}/pi", "141.585916280006"),
    # Example 4.1, v1-006
    ("ch04.examples.n01.main_step_by_step", "sol", "R_mag", R_MAG_4_1, "128.204889993952"),
    ("ch04.examples.n01.main_step_by_step", "sol", "R_angle", R_ANGLE_4_1, "2.47114041353915"),
    (
        "ch04.examples.n01.main_step_by_step",
        "sol_deg",
        "R_angle_deg",
        f"180*{R_ANGLE_4_1}/pi",
        "141.585916280006",
    ),
    # Example 4.4, 000
    ("ch04.examples.n04.main", "sol", "a_x", "(F_x + n_x + w_x)/m", "0.500000000000000"),
    # Example 4.5, 001
    (
        "ch04.examples.n05.main",
        "sol",
        "f_x",
        "(b_0_v_x**2*m/2 - b_0_x*n_x - b_0_x*w_x - b_1_v_x**2*m/2 + b_1_x*n_x + b_1_x*w_x)"
        "/(b_0_x - b_1_x)",
        "-0.900000000000000",
    ),
    # Example 4.5, 000, its first step
    (
        "ch04.examples.n05.main_two_steps",
        "sol_1",
        "a_x_b_0_1",
        "(b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))",
        "-2.00000000000000",
    ),
    # Example 4.7, 000, with the old weight and g
    ("ch04.examples.n07.main", "sol", "a_x", "F_x*g/w", "-7.3274693877551*meter/second**2"),
]

# The rows a reshape changed: (module, solution, the old formula) to the
# new formula, in the new names. The row keeps the old formula as the
# record.
#
# Increment 005 of the 004 series, the projectile setup: 3.6's v1x isn't
# a given any more. The setup's `m0.vel.x = m1.vel.x` gives it, so each
# formula has `m0.vel.x` where the old one had `m1.vel.x`.
N06 = "ch03.examples.n06.main"
RESHAPED: dict[tuple[str, str, str], str] = {
    (N06, "sol", "m_1_t*(m_0_v_x + m_1_v_x)/2"): "m0.vel.x*m1.t",
    (
        N06,
        "sol",
        "sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2",
    ): "sqrt(m1.t**2*(4*m0.vel.x**2 + (g*m1.t - 2*m0.vel.y)**2))/2",
    (
        N06,
        "sol",
        "sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)",
    ): "sqrt(m0.vel.x**2 + (g*m1.t - m0.vel.y)**2)",
    (
        N06,
        "sol",
        "atan2(-g*m_1_t + m_0_v_y, m_1_v_x)",
    ): "atan2(-g*m1.t + m0.vel.y, m0.vel.x)",
    (
        N06,
        "sol",
        "180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi",
    ): "180*atan2(-g*m1.t + m0.vel.y, m0.vel.x)/pi",
}


def test_every_quoted_formula_has_a_row() -> None:
    assert len(OLD) == 66


def test_every_reshaped_formula_is_a_row() -> None:
    assert set(RESHAPED) <= {(module, solution, formula) for module, solution, _, formula, _ in OLD}
    assert len(RESHAPED) == 5


def slow_if(module: str) -> list[pytest.MarkDecorator]:
    return [pytest.mark.slow] if f"examples.up_15e.{module}" in SLOW_EXAMPLES else []


@pytest.mark.parametrize(
    ("module", "solution", "want", "formula", "number"),
    [pytest.param(*row, marks=slow_if(row[0])) for row in OLD],
)
def test_old_output(
    module: str, solution: str, want: str, formula: str, number: str | None
) -> None:
    sol = getattr(importlib.import_module(f"examples.up_15e.{module}"), solution)
    assert isinstance(sol, Solution)
    (symbol,) = [w for w in sol.system.wants if old_name(w, module) == want]

    # The formula, verbatim: renamed back, or, for a row a reshape
    # changed, the new one, in the new names. With several roots, SymPy's
    # order doesn't matter: the formula picks its root.
    new = RESHAPED.get((module, solution, formula))
    if new is None:
        formulas = [old_str(root.formula(symbol), module) for root in sol.roots]
        expected = formula
    else:
        formulas = [str(root.formula(symbol)) for root in sol.roots]
        expected = new
    assert expected in formulas
    root = sol.roots[formulas.index(expected)]
    if number is None:
        return

    # The number, with the old givens where the port uses the book's.
    ours = root.number(symbol)
    if module in OLD_GIVENS:
        values: dict[sp.Basic | complex, sp.Expr | complex] = {
            sym: value for sym, value in sol.system.knowns.items() if value is not None
        }
        for name, value in OLD_GIVENS[module].items():
            (given,) = [sym for sym in sol.system.knowns if old_name(sym, module) == name]
            assert given in values, f"{given} has no number in the port"
            values[given] = value
        ours = cast(sp.Expr, sp.N(root.formula(symbol).subs(values)))  # sp.N is untyped

    # By value, in the old number's unit.
    old = cast(sp.Expr, parse_expr(number, local_dict=UNITS))
    old_value, unit = old.as_coeff_Mul()
    ours = ours / unit
    assert not ours.has(Quantity), f"{root.number(symbol)} isn't in {unit}"
    assert math.isclose(float(ours), float(old_value), rel_tol=1e-9)


def test_3_6_given_v1x_again_is_the_old_output() -> None:
    # The reshaped rows moved because 3.6's givens changed. With
    # m1.vel.x given again, as in the old script, the solve needs the
    # port's old by-hand step, and then every old row comes back verbatim.
    module = importlib.import_module(f"examples.up_15e.{N06}")
    ride, sol = getattr(module, "ride"), getattr(module, "sol")
    assert isinstance(ride, System) and isinstance(sol, Solution)
    m1_vel_x, m01_dt = Var("m", "1", "vel", "x"), Var("m", "01", "dt")
    wants = [w for w in sol.system.wants if w != m1_vel_x]
    given = ride.known(m1_vel_x, 9.0)
    assert given.solve(*wants).roots == ()  # 0 = (-m0.vel.x + m1.vel.x)/m01.dt

    old = given.eliminate(m01_dt).solve(*wants)
    rows = [row for row in OLD if row[0] == N06]
    assert len(rows) == 6
    for _, _, want, formula, number in rows:
        (symbol,) = [w for w in wants if old_name(w, N06) == want]
        assert old_str(old.formula(symbol), N06) == formula
        assert number is not None
        assert math.isclose(float(old.number(symbol)), float(number), rel_tol=1e-9)


def test_4_5_step_2_has_the_edges_acceleration() -> None:
    # Not a row: the old script never solved its step 2. The catalog's
    # scratch try gave `f_x = a_x*m - n_x - w_x`, with step 2's own `a_x`.
    # Since increment 006 of the 004 series, the acceleration is the
    # edge's, the one symbol step 1 solves for and step 2 knows.
    module = importlib.import_module("examples.up_15e.ch04.examples.n05.main_two_steps")
    sol_1, sol_2 = getattr(module, "sol_1"), getattr(module, "sol_2")
    assert isinstance(sol_1, Solution) and isinstance(sol_2, Solution)
    f_x, b_mass, b01_a_x = Var("f", "", "x"), Var("b", "", "mass"), Var("b", "01", "a", "x")
    formula = sol_2.formula(f_x)
    assert str(formula) == "b.mass*b01.a.x - n.x - w.x"
    old_names = {b_mass: sp.Symbol("m"), b01_a_x: sp.Symbol("a_x")}
    assert old_str(formula.xreplace(old_names)) == "a_x*m - n_x - w_x"
    assert b01_a_x in sol_1.system.wants
    assert sol_2.system.knowns[b01_a_x] == sol_1.number(b01_a_x)


# 3.10 v1-001's last line, the stated condition.
OLD_3_10 = ("d_0_v_mag*sin(d_0_v_angle)", "D*d_0_v_mag*sin(d_0_v_angle)/d_1_x")


def test_3_10_show_that() -> None:
    module = importlib.import_module("examples.up_15e.ch03.examples.n10.main")
    proved = getattr(module, "proved")
    reached = getattr(module, "reached")
    assert isinstance(proved, System) and isinstance(reached, System)

    # One equation is left, the old last line with its sides swapped.
    (equation,) = proved.equations
    lhs, rhs = equation.eq.lhs, equation.eq.rhs
    assert (old_str(rhs), old_str(lhs)) == OLD_3_10

    # It holds exactly when the dart reaches x = D.
    d1_x, D = Var("d", "1", "pos", "x"), sp.Symbol("D")
    assert equation.eq.subs(d1_x, D) is sp.true

    # With d1.pos.x = D added, nothing is left.
    assert reached.equations == ()


# old_name, the old rule


def test_old_name_of_a_state() -> None:
    assert old_name(Var("m", "0", "pos", "x")) == "m_0_x"
    assert old_name(Var("m", "0", "vel", "x")) == "m_0_v_x"
    assert old_name(Var("m", "0", "t")) == "m_0_t"


def test_old_name_of_a_states_velocity_in_polar() -> None:
    assert old_name(Var("m", "0", "vel", "mag")) == "m_0_v_mag"
    assert old_name(Var("m", "0", "vel", "angle")) == "m_0_v_angle"


def test_old_name_of_an_edge() -> None:
    assert old_name(Var("m", "01", "dt")) == "dt_m_0_1"
    assert old_name(Var("m", "01", "a", "x")) == "a_x_m_0_1"
    assert old_name(Var("m", "01", "v_av", "x")) == "v_av_x_m_0_1"


def test_old_name_of_a_lone_vector() -> None:
    assert old_name(Var("F1", "", "x")) == "F1_x"
    assert old_name(Var("F1", "", "y")) == "F1_y"
    assert old_name(Var("F1", "", "mag")) == "F1_mag"
    assert old_name(Var("F1", "", "angle")) == "F1_angle"
    assert old_name(Var("a", "", "x")) == "a_x"  # as the old 4.4's acceleration was


def test_old_name_of_a_plain_symbol() -> None:
    assert old_name(sp.Symbol("m_v")) == "m_v"


@pytest.mark.parametrize(
    "var",
    [
        Var("m", "0", "pos", "mag"),  # a position's polar parts
        Var("m", "0", "pos", "angle"),
        Var("m", "01", "a", "mag"),  # an edge's
        Var("m", "0", "vel", "angle_deg"),
        Var("F1", "", "angle_deg"),
        Var("b", "", "mass"),
        Var("meet", "", "t"),  # an event's, without a module
        Var("meet", "", "pos", "x"),
    ],
    ids=str,
)
def test_old_name_of_a_var_the_rule_doesnt_know(var: Var) -> None:
    with pytest.raises(ValueError, match=re.escape(var.name)):
        old_name(var)


# The per-module map, SCRIPT_NAMES


def test_old_name_in_its_module_is_the_scripts() -> None:
    m1 = (Var("m", "1", "pos", "mag"), Var("m", "1", "vel", "angle_deg"))
    assert [old_name(v, "ch03.examples.n06.main") for v in m1] == ["dist", "vel_angle_deg"]
    R_angle_deg = Var("R", "", "angle_deg")
    assert old_name(R_angle_deg, "ch04.examples.n01.main") == "R_angle_deg"
    assert old_name(R_angle_deg, "ch04.examples.n01.main_step_by_step") == "R_angle_deg"
    meet = (Var("meet", "", "t"), Var("meet", "", "pos", "x"))
    for module in ("ch02.examples.n05.main", "ch02.examples.n05.main_step_by_step"):
        assert [old_name(v, module) for v in meet] == ["t_01", "dist"]
    box = (Var("box", "", "mass"), Var("box", "01", "a", "x"))
    assert [old_name(v, "ch04.examples.n04.main") for v in box] == ["m", "a_x"]
    assert old_name(Var("b", "", "mass"), "ch04.examples.n05.main") == "m"


def test_old_name_the_map_wins_over_the_rule() -> None:
    b0_vel_mag = Var("b", "0", "vel", "mag")
    assert old_name(b0_vel_mag, "ch03.examples.n07.main") == "b0_vel_mag"
    assert old_name(b0_vel_mag) == "b_0_v_mag"
    assert old_name(b0_vel_mag, "ch03.examples.n09.main") == "b_0_v_mag"
    box01_a_x = Var("box", "01", "a", "x")  # 4.4's acceleration, the old script's own
    assert old_name(box01_a_x, "ch04.examples.n04.main") == "a_x"
    assert old_name(box01_a_x) == "a_x_box_0_1"


def test_old_name_the_map_applies_in_its_module_only() -> None:
    m1_pos_mag = Var("m", "1", "pos", "mag")
    with pytest.raises(ValueError, match=re.escape(m1_pos_mag.name)):
        old_name(m1_pos_mag, "ch03.examples.n08.main")


def test_every_mapped_module_has_rows() -> None:
    assert set(SCRIPT_NAMES) <= {row[0] for row in OLD}


def test_old_str_prints_the_old_order() -> None:
    m0_x, m0_v_x, m1_t, m01_a_x = (
        Var("m", "0", "pos", "x"),
        Var("m", "0", "vel", "x"),
        Var("m", "1", "t"),
        Var("m", "01", "a", "x"),
    )
    formula = m0_x + m0_v_x * m1_t + m01_a_x * m1_t**2 / 2
    assert str(formula) == "m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2"
    assert old_str(formula) == "a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x"
