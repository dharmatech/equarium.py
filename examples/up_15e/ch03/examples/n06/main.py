"""University Physics, 15th edition, Example 3.6, with the physics code.

A motorcycle rider leaves the edge of a cliff moving horizontally at
9.0 m/s, with the edge as the origin and no air resistance. At 0.50 s
after he leaves the edge, find his position, his distance from the edge,
and his velocity, as components and as magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.6-v1-000.py`. Projectile motion is the
projectile setup, `m01.projectile(g)`, which is `m01.a.y = -g` and
`m0.vel.x = m1.vel.x`, with `m01.a.x` known zero. The old script wrote
`m01.a.y = -g` itself, and gave both horizontal velocities. Its other
three zero equations, the origin and the clock, are zero knowns here,
followed by `eliminate_zeros()` where it called its
`eliminate_zero_eqs`. Its `m0.vel.y = 0.0` is a value, set after that
step, so it stays a symbol in the formulas. The distance is the
position's magnitude, from `m1.pos.to_polar()`, and the speed and
direction come from `m1.vel.to_polar()` and `m1.vel.degrees()`. The old
script wrote them by hand. Its six solves, each of one want as its
equations grew, are one here, with the velocity's components added.

The book's v_x = 9.0 m/s is an answer here, not a given. Only `m0.vel.x`
is given, and the setup's `m0.vel.x = m1.vel.x` gives `m1.vel.x`. So the
formulas have `m0.vel.x` where the old script's had `m1.vel.x`. With
`m1.vel.x` given too, as in the old script, the solve finds no roots.
Equation (4), `0 = (-m0.vel.x + m1.vel.x)/m01.dt`, then has `m01.dt` as
its only unknown, and SymPy can't solve it for that. The port had a step
for that, `eliminate(m01.dt)`, where the old library's
`clear_zero_denominators` did the work. It isn't needed any more.

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

flight = m01.projectile(g)

cliff = (
    System()
    .add(*m.kinematics())  # (1) to (5)
    .add(*m01.constant_acceleration())  # (6), (7)
    .add(*flight.equations)  # (8), (9): projectile motion
    .known(flight.knowns)  # m01.a.x = 0
    .known({m0.pos.x: 0, m0.pos.y: 0, m0.t: 0})  # from the edge, at t = 0
    .eliminate_zeros()
    .known(m0.vel.x, 9.0)  # m/s, horizontal
    .known(m0.vel.y, 0.0)  # m/s
    .known(g, 9.8)  # m/s²
    .known(m1.t, 0.50)  # s
)

ride = (
    cliff
    .add(*m1.pos.to_polar())  # (10), (11): the distance, and the position's angle
    .add(*m1.vel.to_polar())  # (12), (13): the speed and direction
    .add(*m1.vel.degrees())  # (14)
)

sol = ride.solve(  # about 1.8 s
    m1.pos.x,
    m1.pos.y,
    m1.pos.mag,
    m1.vel.x,
    m1.vel.y,
    m1.vel.mag,
    m1.vel.angle,
    m1.vel.angle_deg,
)
# m1.pos.x = m0.vel.x*m1.t                                                     4.5
# m1.pos.y = m1.t*(-g*m1.t + 2*m0.vel.y)/2                                     -1.225
# m1.pos.mag = sqrt(m1.t**2*(4*m0.vel.x**2 + (g*m1.t - 2*m0.vel.y)**2))/2      4.66
# m1.vel.x = m0.vel.x                                                          9.0
# m1.vel.y = -g*m1.t + m0.vel.y                                                -4.9
# m1.vel.mag = sqrt(m0.vel.x**2 + (g*m1.t - m0.vel.y)**2)                      10.25
# m1.vel.angle = atan2(-g*m1.t + m0.vel.y, m0.vel.x)                           -0.499
# m1.vel.angle_deg = 180*atan2(-g*m1.t + m0.vel.y, m0.vel.x)/pi                -28.6

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, m1.pos.x, "4.5"),  # m
    Answer(sol, m1.pos.y, "-1.2"),  # m
    Answer(sol, m1.pos.mag, "4.7"),  # m
    Answer(sol, m1.vel.x, "9.0"),  # m/s, a given in the old script
    Answer(sol, m1.vel.y, "-4.9"),  # m/s, a new want
    Answer(sol, m1.vel.mag, "10.2"),  # m/s
    Answer(sol, m1.vel.angle_deg, "-29"),  # degrees
]

if __name__ == "__main__":
    ride.show()
    print()
    sol.show()
