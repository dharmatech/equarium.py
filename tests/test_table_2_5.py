"""Table 2.5's port against kinematic-equations 003, whose output the
catalog quotes: its five lines, in order."""

import sympy as sp

from equarium.sympy_compat import sides
from examples.up_15e.ch02.tables.n05.main import EQUATIONS, a_x, dt, v_1x, v_2x, v_av_x, x_1, x_2

# 003's output, all of it, printed and as SymPy objects.
OLD = [
    "v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)",
    "-x_1 + x_2 = dt*(v_1x + v_2x)/2",
    "v_2x = a_x*dt + v_1x",
    "2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2",
    "x_2 = a_x*dt**2/2 + dt*v_1x + x_1",
]


def equation(lhs: sp.Expr, rhs: sp.Expr) -> sp.Equality:
    eq = sp.Eq(lhs, rhs)
    assert isinstance(eq, sp.Equality)
    return eq


OLD_EQUATIONS = [
    equation(v_av_x, a_x * (-x_1 + x_2) / (-v_1x + v_2x)),
    equation(-x_1 + x_2, dt * (v_1x + v_2x) / 2),
    equation(v_2x, a_x * dt + v_1x),
    equation(2 * a_x * (-x_1 + x_2) + v_1x**2, v_2x**2),
    equation(x_2, a_x * dt**2 / 2 + dt * v_1x + x_1),
]


def printed(eq: sp.Equality) -> str:
    return f"{eq.lhs} = {eq.rhs}"


def test_the_old_lines_are_the_old_equations() -> None:
    assert [printed(eq) for eq in OLD_EQUATIONS] == OLD


def test_the_names_in_003s_order() -> None:
    assert [name for name, _ in EQUATIONS] == ["v_av_x without dt", "2.14", "2.8", "2.13", "2.12"]


def test_line_1_is_equivalent_in_equariums_form() -> None:
    # eliminate simplifies each side, so the signs come out the other way.
    _, eq = EQUATIONS[0]
    lhs, rhs = sides(eq)
    old_lhs, old_rhs = sides(OLD_EQUATIONS[0])
    assert lhs == old_lhs
    assert sp.simplify(rhs - old_rhs) == 0
    assert printed(eq) == "v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)"


def test_lines_2_to_5_are_003s() -> None:
    for (name, eq), line, old in zip(EQUATIONS[1:], OLD[1:], OLD_EQUATIONS[1:], strict=True):
        assert printed(eq) == line, name
        assert eq == old, name
