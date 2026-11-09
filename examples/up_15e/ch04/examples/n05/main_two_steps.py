"""University Physics, 15th edition, Example 4.5, with the physics code,
in two steps: the acceleration from the kinematics feeds Newton's second
law.

A 0.45 kg ketchup bottle is pushed along a level counter. It leaves the
hand at 2.0 m/s and slides 1.0 m before stopping, slowed by a constant
horizontal friction force. What are the friction force's magnitude and
direction?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.5/up-example-4.5-000-two-steps.py`, with
the physics code's lone vectors and `.eq` where it had local helpers for
the forces and Newton's second law. Its zeros are values, so they are
zero knowns here, never eliminated. The old script ends at step 2's
display, without feeding in the acceleration. Here step 2 takes step 1's
acceleration as a known and solves for `f.x`.

    uv run python -m examples.up_15e.ch04.examples.n05.main_two_steps
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Particle, Vector, X
from examples.answers import Answer

b = Particle("b", 2, X)  # the bottle
b0, b1 = b.states
b01 = b.edge(0, 1)

# Step 1: the acceleration, from the kinematics.
slide = (
    System()
    .add(*b.kinematics())  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
)
sol_1 = slide.solve(b01.a.x)
# b01.a.x = (b0.vel.x - b1.vel.x)*(b0.vel.x + b1.vel.x)/(2*(b0.pos.x - b1.pos.x))   -2.0

# Step 2: the friction force, from Newton's second law.
n = Vector("n", XY)  # the normal force
w = Vector("w", XY)  # the weight
f = Vector("f", XY)  # the friction force
m = sp.Symbol("m")  # the mass
a = Vector("a", XY)  # the acceleration

push = (
    System()
    .add(*(n + w + f).eq(a * m))  # (1), (2)
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(m, 0.45)  # kg
    .known(a.x, sol_1.number(b01.a.x))  # m/s², from step 1
)
sol_2 = push.solve(f.x)
# f.x = m*a.x - n.x - w.x   -0.9

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_1, b01.a.x, "-2.0"),  # m/s²
    Answer(sol_2, f.x, "-0.90"),  # N
]

if __name__ == "__main__":
    slide.show()
    print()
    sol_1.show()
    print()
    push.show()
    print()
    sol_2.show()
