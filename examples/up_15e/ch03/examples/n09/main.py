"""University Physics, 15th edition, Example 3.9, with the physics code.

A ball is thrown from a window 8.0 m above the ground at 10.0 m/s,
20.0° below the horizontal, with no air resistance. How far from the
window, horizontally, does it land?

Ported from combine-equations.py's `examples/up/ch3/up-example-3.9-v2.py`,
with the book's g = 9.80 m/s², not the old 9.81. Its four zero
equations, `b_1_y` among them (it hits the ground), are zero knowns
here, followed by `eliminate_zeros()` where it called
`eliminate_zero_eqs`. The launch is polar both ways, through
`magnitude_and_angle_equations`, so `all_at_once` finds no roots, and
`eliminating()` solves it, as the old version 2 did. The origin is at
the ground, not at the hand as in the book: the same answer. The time
is added as a want, solved with x in no more time than x alone. The
book prints both roots, -1.7 s and 0.98 s, and the negative one is the
other root of x, -15.7 m.

    uv run python -m examples.up_15e.ch03.examples.n09.main
"""

import sympy as sp

from equarium import System, eliminating, eq_flat
from equarium.physics.kinematics_states import (
    kinematics_fundamental,
    magnitude_and_angle_equations,
    make_states_model,
)
from examples.answers import Answer

b = make_states_model("b", 2)  # the ball
b0, b1 = b.states
b01 = b.edges[0]
assert b0.vel.mag is not None and b0.vel.angle is not None  # make_states_model sets both

g = sp.Symbol("g")

window = (
    System()
    .add(*kinematics_fundamental(b, axes=["x", "y"]))  # (1) to (7)
    .add(*eq_flat(b01.a.y, -g, b0.vel.x, b1.vel.x))  # (8), (9): projectile motion
    .known({b0.pos.x: 0, b01.a.x: 0, b0.t: 0, b1.pos.y: 0})  # b_1_y: it hits the ground
    .eliminate_zeros()
    .known(g, 9.80)  # m/s²
    .known(b0.pos.y, 8.0)  # m
    .add(*magnitude_and_angle_equations(b0))  # (10) to (13)
    .known(b0.vel.mag, 10.0)  # m/s
    .known(b0.vel.angle, sp.N(sp.rad(-20.0)))  # degrees to radians
)

sol = window.solve(b1.pos.x, b1.t, strategy=eliminating())  # about 5 s
# Root 1:
# b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle)
#         - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g   -15.7
# b_1_t = (b_0_v_mag*sin(b_0_v_angle)
#         - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))/g                    -1.67
# Root 2: the same with +, 9.17 and 0.976.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol.where(b1.pos.x > 0), b1.pos.x, "9.2"),  # m
    Answer(sol, b1.t, "-1.7", "0.98"),  # s, a new want
]

if __name__ == "__main__":
    window.show()
    print()
    sol.show()
    print()
    sol.system.show_history()
    print()
    sol.where(b1.pos.x > 0).show()
