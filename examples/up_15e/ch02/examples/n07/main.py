"""University Physics, 15th edition, Example 2.7, with the physics code.

A ball is thrown straight up at 15.0 m/s from level with a roof railing,
then falls freely (the book's Fig. 2.24; upward positive, origin at the
railing). (a) Where is it, and how fast is it moving, 1.00 s and 4.00 s
later? (b) What is its velocity when it is 5.00 m above the railing?
(c) How high does it go? (d) What is its acceleration at the top?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.7/up-example-2.7-v1-000.py`, without its
last part, Example 2.8, which is `n08/main.py`. Its two zero
equations, in its `eq_flat`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`, before any
values. (c)'s `b1.vel.y = 0.0` is a value, set after that step, so it
stays a symbol in the formula, as in the old script.

    uv run python -m examples.up_15e.ch02.examples.n07.main
"""

from equarium import System
from equarium.physics import Particle, Y
from examples.answers import Answer

b = Particle("b", 2, Y)  # the ball
b0, b1 = b.states
b01 = b.edge(0, 1)

ball = (
    System()
    .add(*b.kinematics())
    .add(*b01.constant_acceleration())  # free fall: a constant g
    .known({b0.t: 0, b0.pos.y: 0})  # thrown at t = 0, from the railing
    .eliminate_zeros()
    .known(b0.vel.y, 15.0)  # m/s
    .known(b01.a.y, -9.8)  # m/s², free fall
)

# (a) Position and velocity at 1.00 s and 4.00 s.
sol_a1 = ball.known(b1.t, 1.0).solve(b1.pos.y, b1.vel.y)  # s
# b1.pos.y = b1.t*(2*b0.vel.y + b01.a.y*b1.t)/2   10.1
# b1.vel.y = b0.vel.y + b01.a.y*b1.t               5.2
sol_a4 = ball.known(b1.t, 4.0).solve(b1.pos.y, b1.vel.y)  # s; -18.4 and -24.2

# (b) The velocity 5.00 m above the railing: two roots.
sol_b = ball.known(b1.pos.y, 5.0).solve(b1.vel.y)  # m
# b1.vel.y = -sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)   -11.3
# b1.vel.y = sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)    11.3

# (c) The maximum height, where the velocity is zero.
sol_c = ball.known(b1.vel.y, 0.0).solve(b1.pos.y)  # m/s
# b1.pos.y = (-b0.vel.y**2 + b1.vel.y**2)/(2*b01.a.y)   11.5

# (d) The acceleration is constant, so at the top it is still -9.80 m/s².
# It's a known, not a want, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a1, b1.pos.y, "10.1"),  # m
    Answer(sol_a1, b1.vel.y, "5.2"),  # m/s
    Answer(sol_a4, b1.pos.y, "-18.4"),  # m
    Answer(sol_a4, b1.vel.y, "-24.2"),  # m/s
    Answer(sol_b, b1.vel.y, "-11.3", "11.3"),  # m/s
    Answer(sol_c, b1.pos.y, "11.5"),  # m
]

if __name__ == "__main__":
    ball.show()
    for sol in (sol_a1, sol_a4, sol_b, sol_c):
        print()
        sol.show()
