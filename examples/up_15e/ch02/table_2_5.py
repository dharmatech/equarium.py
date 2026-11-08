"""University Physics, 15th edition, Table 2.5: the constant-acceleration
equations 2.8, 2.12, 2.13 and 2.14, derived from 2.2, 2.7 and 2.10.

(2.2) defines the average velocity over an interval `dt`, (2.7) the
average acceleration over it, and (2.10) is the average velocity as the
mean of the end velocities, true for constant acceleration.

Ported from combine-equations.py's
`examples/up/ch2/kinematic-equations/kinematics-equations-003-book-equations.py`,
in its symbols. Each equation comes from a branch of one system: its
`solve_subs` is `eliminate` with `using`, its `isolate_variable` is
`isolate`, and `multiply_both_sides`, `sp.simplify` and `add_both_sides`
take the last steps of 2.13 and 2.14, as in 003.

Not an example or exercise, so it has no `BOOK`.

    uv run python -m examples.up_15e.ch02.table_2_5
"""

import sympy as sp

from equarium import System
from equarium.equations import add_both_sides, multiply_both_sides

x_1, x_2, v_1x, v_2x, v_av_x, dt, a_x = sp.symbols("x_1 x_2 v_1x v_2x v_av_x dt a_x")

kinematics = (
    System()
    .add(sp.Eq(v_av_x, (x_2 - x_1) / dt), label="2.2")
    .add(sp.Eq(a_x, (v_2x - v_1x) / dt), label="2.7")
    .add(sp.Eq(v_av_x, (v_1x + v_2x) / 2), label="2.10")
)


def simplified(eq: sp.Equality) -> sp.Equality:
    """`sp.simplify` of a whole equation, which pyright types as `Boolean`.
    It must stay an equation."""
    result = sp.simplify(eq)
    if not isinstance(result, sp.Equality):
        raise TypeError(f"{eq} simplified to {result}, not an equation")
    return result


# The average velocity without dt: (2.7) into (2.2) for dt.
no_dt = kinematics.eliminate(dt, using="2.7")
eq_v_av_x = no_dt.equation("2.2").eq

# 2.14: (2.10) into (2.2) for v_av_x, then both sides times dt,
# simplified, and both sides times -1.
no_v_av_x = kinematics.eliminate(v_av_x, using="2.10")
step = multiply_both_sides(no_v_av_x.equation("2.2").eq, dt)
step = simplified(step)
eq_2_14 = multiply_both_sides(step, -1)

# 2.8: (2.7) isolated for v_2x.
eq_2_8 = kinematics.isolate(v_2x, "2.7").equation("2.7").eq

# 2.13: (2.7) into (2.2) for dt, then (2.10) for v_av_x, then both sides
# times (-v_1x + v_2x) and times 2, simplified, and v_1x**2 added to
# both sides.
no_dt_or_v_av_x = no_dt.eliminate(v_av_x, using="2.10")
step = multiply_both_sides(no_dt_or_v_av_x.equation("2.2").eq, -v_1x + v_2x)
step = multiply_both_sides(step, 2)
step = simplified(step)
eq_2_13 = add_both_sides(step, v_1x**2)

# 2.12: (2.10) into (2.2) for v_av_x, then (2.7) for v_2x, then (2.2)
# isolated for x_2.
positions = no_v_av_x.eliminate(v_2x, using="2.7").isolate(x_2, "2.2")
eq_2_12 = positions.equation("2.2").eq

# In 003's order.
EQUATIONS: list[tuple[str, sp.Equality]] = [
    ("v_av_x without dt", eq_v_av_x),  # v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)
    ("2.14", eq_2_14),  # -x_1 + x_2 = dt*(v_1x + v_2x)/2
    ("2.8", eq_2_8),  # v_2x = a_x*dt + v_1x
    ("2.13", eq_2_13),  # 2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2
    ("2.12", eq_2_12),  # x_2 = a_x*dt**2/2 + dt*v_1x + x_1
]

if __name__ == "__main__":
    for _, eq in EQUATIONS:
        print(f"{eq.lhs} = {eq.rhs}")
