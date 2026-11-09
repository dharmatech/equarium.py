"""University Physics, 15th edition, Example 3.6, with the physics code.

A motorcycle rider leaves the edge of a cliff moving horizontally at
9.0 m/s, with the edge as the origin and no air resistance. At 0.50 s
after he leaves the edge, find his position, his distance from the edge,
and his velocity, as components and as magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.6-v1-000.py`. Its four zero equations, in
its `eq_flat` with `a_y = -g`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`. Its
`m_0_v_y = 0.0` is a value, set after that step, so it stays a symbol in
the formulas. So is `m_1_v_x = 9.0`: the book's v_x is a given here. The
distance, speed and angle are written by hand from the components, as in
the old script. Its six solves, each of one want as its equations grew,
are one here, with the velocity's y-component added.

One step isn't in the old script: `eliminate(m01.dt)`. After the zeros,
equation (4) is `0 = (-m_0_v_x + m_1_v_x)/dt_m_0_1`, with both
velocities known, so its only unknown is `dt_m_0_1`, and SymPy can't
solve it for that: without the step, the solve finds no roots. The old
library's `clear_zero_denominators` turned it into
`-m_0_v_x + m_1_v_x = 0`, which has no unknown, so the old solve left it
out. Eliminating `dt_m_0_1` does the same here.

    uv run python -m examples.up_15e.ch03.examples.n06.main
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

m = make_states_model("m", 2)  # the motorcycle
m0, m1 = m.states
m01 = m.edges[0]

g = sp.Symbol("g")
dist, vel_mag, vel_angle, vel_angle_deg = sp.symbols("dist vel_mag vel_angle vel_angle_deg")

cliff = (
    System()
    .add(*kinematics_fundamental(m, axes=["x", "y"]))  # (1) to (7)
    .add(sp.Eq(m01.a.y, -g))  # (8), projectile motion
    .known({m0.pos.x: 0, m0.pos.y: 0, m01.a.x: 0, m0.t: 0})  # from the edge, at t = 0
    .eliminate_zeros()
    .eliminate(m01.dt)  # see the docstring
    .known(m0.vel.x, 9.0)  # m/s, horizontal
    .known(m0.vel.y, 0.0)  # m/s
    .known(m1.vel.x, 9.0)  # m/s
    .known(g, 9.8)  # m/s²
    .known(m1.t, 0.50)  # s
)

ride = (
    cliff
    # The distance from the edge.
    .add(sp.Eq(dist, sp.sqrt(m1.pos.x**2 + m1.pos.y**2)))
    # The speed and direction.
    .add(
        *eq_flat(
            vel_mag, sp.sqrt(m1.vel.x**2 + m1.vel.y**2),
            vel_angle, sp.atan2(m1.vel.y, m1.vel.x),
        )
    )
    .add(sp.Eq(vel_angle_deg, vel_angle * 180 / sp.pi))
)

sol = ride.solve(m1.pos.x, m1.pos.y, dist, m1.vel.y, vel_mag, vel_angle, vel_angle_deg)
# m_1_x = m_1_t*(m_0_v_x + m_1_v_x)/2                                           4.5
# m_1_y = m_1_t*(-g*m_1_t + 2*m_0_v_y)/2                                        -1.225
# dist = sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2   4.66
# m_1_v_y = -g*m_1_t + m_0_v_y                                                  -4.9
# vel_mag = sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)                           10.25
# vel_angle = atan2(-g*m_1_t + m_0_v_y, m_1_v_x)                                -0.499
# vel_angle_deg = 180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi                     -28.6

# The book's v_x = 9.0 m/s is a given here, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, m1.pos.x, "4.5"),  # m
    Answer(sol, m1.pos.y, "-1.2"),  # m
    Answer(sol, dist, "4.7"),  # m
    Answer(sol, m1.vel.y, "-4.9"),  # m/s, a new want
    Answer(sol, vel_mag, "10.2"),  # m/s
    Answer(sol, vel_angle_deg, "-29"),  # degrees
]

if __name__ == "__main__":
    ride.show()
    print()
    sol.show()
