"""The chapter 2 ports against the old scripts: every formula the catalog
quotes for a ported script's want, verbatim, and its number, by value.

The old output is as `docs/design/implementation/001-example-catalog/catalog.md`
quotes it, from the old scripts run on 2026-11-08. Two differences are
expected, as checkpoint 007 lists:

- the old scripts printed `formula.subs(values)`, so an exact number
  printed as `43`, where equarium's number is `sp.N` of it, `43.0000000000000`.
  So the numbers compare by value, within 1e-9 relative;
- the additions (2.6's velocities at 2.0 s and 3.0 s, 2.3's `longer`) have
  no old output. Their `BOOK`s check them.
"""

import importlib
import math
from typing import cast

import pytest
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.physics.units import Quantity, hour, kilometer, meter, second

from equarium import Solution

UNITS = {"meter": meter, "second": second, "kilometer": kilometer, "hour": hour}

# (module, solution, want, the old formula, the old number), as printed.
OLD: list[tuple[str, str, str, str, str]] = [
    # Example 2.4, v4-001
    ("example_2_4", "sol_a", "m_1_x", "a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x", "43"),
    ("example_2_4", "sol_a", "m_1_v_x", "a_x_m_0_1*m_1_t + m_0_v_x", "23"),
    (
        "example_2_4",
        "sol_b",
        "m_1_x",
        "(2*a_x_m_0_1*m_0_x - m_0_v_x**2 + m_1_v_x**2)/(2*a_x_m_0_1)",
        "55",
    ),
    # Example 2.5, v4-000
    ("example_2_5", "sol", "t_01", "2*m_v/a_x_p_0_1", "10"),
    ("example_2_5", "sol", "p_1_v_x", "2*m_v", "30"),
    ("example_2_5", "sol", "dist", "2*m_v**2/a_x_p_0_1", "150"),
    # Example 2.5, v4-002
    ("example_2_5_step_by_step", "sol", "t_01", "2*m_v/a_x_p_0_1", "10"),
    ("example_2_5_step_by_step", "sol", "p_1_v_x", "2*m_v", "30"),
    ("example_2_5_step_by_step", "sol", "dist", "2*m_v**2/a_x_p_0_1", "150"),
    # Example 2.6, v2-000
    ("example_2_6", "sol_1", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-4.90000000000000"),
    ("example_2_6", "sol_1", "c_1_v_y", "a_y_c_0_1*c_1_t", "-9.80000000000000"),
    ("example_2_6", "sol_2", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-19.6000000000000"),
    ("example_2_6", "sol_3", "c_1_y", "a_y_c_0_1*c_1_t**2/2", "-44.1000000000000"),
    # Example 2.7, v1-000
    ("example_2_7", "sol_a1", "b_1_y", "b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2", "10.1000000000000"),
    ("example_2_7", "sol_a1", "b_1_v_y", "a_y_b_0_1*b_1_t + b_0_v_y", "5.20000000000000"),
    ("example_2_7", "sol_a4", "b_1_y", "b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2", "-18.4000000000000"),
    ("example_2_7", "sol_a4", "b_1_v_y", "a_y_b_0_1*b_1_t + b_0_v_y", "-24.2000000000000"),
    ("example_2_7", "sol_b", "b_1_v_y", "-sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)", "-11.2694276695846"),
    ("example_2_7", "sol_b", "b_1_v_y", "sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)", "11.2694276695846"),
    ("example_2_7", "sol_c", "b_1_y", "(-b_0_v_y**2 + b_1_v_y**2)/(2*a_y_b_0_1)", "11.4795918367347"),
    # Example 2.8, the end of 2.7's v1-000
    (
        "example_2_8",
        "sol",
        "b_1_t",
        "(-b_0_v_y - sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1",
        "3.36451028118484",
    ),
    (
        "example_2_8",
        "sol",
        "b_1_t",
        "(-b_0_v_y + sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1",
        "-0.303285791388921",
    ),
    # Exercise 2.1, 000
    (
        "exercise_2_1",
        "sol",
        "c_1_x",
        "-c_0_t*v_av_x_c_0_1 + c_0_x + c_1_t*v_av_x_c_0_1",
        "25.0*meter",
    ),
    # Exercise 2.3, 002
    (
        "exercise_2_3",
        "sol",
        "cb_1_t",
        "(-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1 + cb_0_t*v_av_x_cb_0_1"
        " - cb_0_x)/v_av_x_cb_0_1",
        "2.75*hour",
    ),
    # Exercise 2.3, 000
    (
        "exercise_2_3_two_steps",
        "distance",
        "ca_1_x",
        "-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1",
        "192.5*kilometer",
    ),
    (
        "exercise_2_3_two_steps",
        "slow",
        "cb_1_t",
        "(cb_0_t*v_av_x_cb_0_1 - cb_0_x + cb_1_x)/v_av_x_cb_0_1",
        "2.75*hour",
    ),
    # Exercise 2.5, 001
    (
        "exercise_2_5",
        "sol",
        "avg_vel_02",
        "(dx_p_0_1 + dx_p_1_2)/(dt_p_0_1 + dt_p_1_2)",
        "0.3125*meter/second",
    ),
    (
        "exercise_2_5",
        "sol",
        "avg_speed_02",
        "(Abs(dx_p_0_1) + Abs(dx_p_1_2))/(dt_p_0_1 + dt_p_1_2)",
        "1.5625*meter/second",
    ),
    # Exercise 2.19, 000
    (
        "exercise_2_19",
        "sol_a",
        "o_0_v_x",
        "(-dt_o_0_1*o_1_v_x - 2*o_0_x + 2*o_1_x)/dt_o_0_1",
        "8.33333333333333*meter/second",
    ),
    (
        "exercise_2_19",
        "sol_b",
        "a_x_o_0_1",
        "(2*dt_o_0_1*o_1_v_x + 2*o_0_x - 2*o_1_x)/dt_o_0_1**2",
        "1.11111111111111*meter/second**2",
    ),
    # Exercise 2.21, 000
    (
        "exercise_2_21",
        "sol_a",
        "a_x_b_0_1",
        "(b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))",
        "675.0*meter/second**2",
    ),
    (
        "exercise_2_21",
        "sol_b",
        "dt_b_0_1",
        "2*(-b_0_x + b_1_x)/(b_0_v_x + b_1_v_x)",
        "0.0666666666666667*second",
    ),
    # Exercise 2.23, 000
    (
        "exercise_2_23",
        "sol",
        "b_1_x",
        "(2*a_x_b_0_1*b_0_x - b_0_v_x**2 + b_1_v_x**2)/(2*a_x_b_0_1)",
        "22.05*kilometer**2*second**2/(hour**2*meter)",
    ),
]


def test_every_quoted_formula_has_a_row() -> None:
    assert len(OLD) == 33


@pytest.mark.parametrize(("module", "solution", "want", "formula", "number"), OLD)
def test_old_output(module: str, solution: str, want: str, formula: str, number: str) -> None:
    sol = getattr(importlib.import_module(f"examples.up_15e.ch02.{module}"), solution)
    assert isinstance(sol, Solution)
    (symbol,) = [w for w in sol.system.wants if w.name == want]

    # The formula, verbatim. With several roots, SymPy's order doesn't
    # matter: the row's formula picks its root.
    formulas = [str(root.formula(symbol)) for root in sol.roots]
    assert formula in formulas
    root = sol.roots[formulas.index(formula)]

    # The number, by value, in the old number's unit.
    old = cast(sp.Expr, parse_expr(number, local_dict=UNITS))
    old_value, unit = old.as_coeff_Mul()
    ours = root.number(symbol) / unit
    assert not ours.has(Quantity), f"{root.number(symbol)} isn't in {unit}"
    assert math.isclose(float(ours), float(old_value), rel_tol=1e-9)
