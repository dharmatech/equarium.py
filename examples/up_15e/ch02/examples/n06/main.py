"""University Physics, 15th edition, Example 2.6, with the physics code.

A coin is dropped from rest from a tower and falls freely, ignoring air
resistance (the book's Fig. 2.23). What are its position and velocity
after 1.0 s, 2.0 s and 3.0 s? Upward is positive, so a = -9.8 m/s².

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.6/up-example-2.6-v2-000.ks.py`. Its three
zero equations, in its `eq_flat`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`, before any
values. The old script solves only for the position at 2.0 s and 3.0 s;
the velocity is added as a want there, for the book's -20 m/s and
-29 m/s.

    uv run python -m examples.up_15e.ch02.examples.n06.main
"""

from equarium import System
from equarium.physics import Particle, Y
from examples.answers import Answer

c = Particle("c", 2, Y)  # the coin
c0, c1 = c.states
c01 = c.edge(0, 1)

coin = (
    System()
    .add(*c.kinematics())
    .add(*c01.constant_acceleration())  # free fall: a constant g
    .known({c0.t: 0, c0.vel.y: 0, c0.pos.y: 0})  # dropped from rest, at the origin
    .eliminate_zeros()
    .known(c01.a.y, -9.8)  # m/s²
)

sol_1 = coin.known(c1.t, 1.0).solve(c1.pos.y, c1.vel.y)  # s
# c1.pos.y = c01.a.y*c1.t**2/2   -4.9
# c1.vel.y = c01.a.y*c1.t        -9.8
sol_2 = coin.known(c1.t, 2.0).solve(c1.pos.y, c1.vel.y)  # s; -19.6 and -19.6
sol_3 = coin.known(c1.t, 3.0).solve(c1.pos.y, c1.vel.y)  # s; -44.1 and -29.4

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_1, c1.pos.y, "-4.9"),  # m
    Answer(sol_1, c1.vel.y, "-9.8"),  # m/s
    Answer(sol_2, c1.pos.y, "-20"),  # m
    Answer(sol_2, c1.vel.y, "-20"),  # m/s
    Answer(sol_3, c1.pos.y, "-44"),  # m
    Answer(sol_3, c1.vel.y, "-29"),  # m/s
]

if __name__ == "__main__":
    coin.show()
    for sol in (sol_1, sol_2, sol_3):
        print()
        sol.show()
