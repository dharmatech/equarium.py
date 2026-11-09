"""University Physics, 15th edition, Example 3.6, with the physics code.

A motorcycle rider leaves the edge of a cliff moving horizontally at
9.0 m/s, with the edge as the origin and no air resistance. At 0.50 s
after he leaves the edge, find his position, his distance from the edge,
and his velocity, as components and as magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.6-v1-000.py`. Its four zero equations, in
its `eq_flat` with `m01.a.y = -g`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`. Its
`m0.vel.y = 0.0` is a value, set after that step, so it stays a symbol in
the formulas. So is `m1.vel.x = 9.0`: the book's v_x is a given here. The
distance is the position's magnitude, from `m1.pos.to_polar()`, and the
speed and direction come from `m1.vel.to_polar()` and
`m1.vel.degrees()`. The old script wrote them by hand. Its six solves,
each of one want as its equations grew, are one here, with the
velocity's y-component added.

One step isn't in the old script: `eliminate(m01.dt)`. After the zeros,
equation (4) is `0 = (-m0.vel.x + m1.vel.x)/m01.dt`, with both
velocities known, so its only unknown is `m01.dt`, and SymPy can't
solve it for that: without the step, the solve finds no roots. The old
library's `clear_zero_denominators` turned it into
`-m0.vel.x + m1.vel.x = 0`, which has no unknown, so the old solve left it
out. Eliminating `m01.dt` does the same here.

    uv run python -m examples.up_15e.ch03.examples.n06.main
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Particle
from examples.answers import Answer

m = Particle("m", 2, XY)  # the motorcycle
m0, m1 = m.states
m01 = m.edge(0, 1)

g = sp.Symbol("g")

cliff = (
    System()
    .add(*m.kinematics())  # (1) to (7)
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
    .add(*m1.pos.to_polar())  # (9), (10): the distance, and the position's angle
    .add(*m1.vel.to_polar())  # (11), (12): the speed and direction
    .add(*m1.vel.degrees())  # (13)
)

sol = ride.solve(
    m1.pos.x, m1.pos.y, m1.pos.mag, m1.vel.y, m1.vel.mag, m1.vel.angle, m1.vel.angle_deg
)
# m1.pos.x = m1.t*(m0.vel.x + m1.vel.x)/2                                            4.5
# m1.pos.y = m1.t*(-g*m1.t + 2*m0.vel.y)/2                                           -1.225
# m1.pos.mag = sqrt(m1.t**2*((m0.vel.x + m1.vel.x)**2 + (g*m1.t - 2*m0.vel.y)**2))/2   4.66
# m1.vel.y = -g*m1.t + m0.vel.y                                                      -4.9
# m1.vel.mag = sqrt(m1.vel.x**2 + (g*m1.t - m0.vel.y)**2)                            10.25
# m1.vel.angle = atan2(-g*m1.t + m0.vel.y, m1.vel.x)                                 -0.499
# m1.vel.angle_deg = 180*atan2(-g*m1.t + m0.vel.y, m1.vel.x)/pi                      -28.6

# The book's v_x = 9.0 m/s is a given here, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, m1.pos.x, "4.5"),  # m
    Answer(sol, m1.pos.y, "-1.2"),  # m
    Answer(sol, m1.pos.mag, "4.7"),  # m
    Answer(sol, m1.vel.y, "-4.9"),  # m/s, a new want
    Answer(sol, m1.vel.mag, "10.2"),  # m/s
    Answer(sol, m1.vel.angle_deg, "-29"),  # degrees
]

if __name__ == "__main__":
    ride.show()
    print()
    sol.show()
