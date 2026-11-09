"""University Physics, 15th edition, Example 4.5, with the physics code,
in two steps: the acceleration from the kinematics feeds Newton's second
law.

A 0.45 kg ketchup bottle is pushed along a level counter. It leaves the
hand at 2.0 m/s and slides 1.0 m before stopping, slowed by a constant
horizontal friction force. What are the friction force's magnitude and
direction?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.5/up-example-4.5-000-two-steps.py`, with
the physics code's `make_point` and `newtons_second_law` for its local
copies. Its zeros are values, so they are zero knowns here, never
eliminated. The old script ends at step 2's display, without feeding in
the acceleration. Here step 2 takes step 1's acceleration as a known and
solves for f_x.

    uv run python -m examples.up_15e.ch04.example_4_5_two_steps
"""

import sympy as sp

from equarium import System
from equarium.physics.kinematics_states import (
    kinematics_fundamental,
    make_point,
    make_states_model,
)
from equarium.physics.newtons_laws import newtons_second_law
from examples.answers import Answer

b = make_states_model("b", 2)  # the bottle
b0, b1 = b.states
b01 = b.edges[0]

# Step 1: the acceleration, from the kinematics.
slide = (
    System()
    .add(*kinematics_fundamental(b, axes=["x"]))  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
)
sol_1 = slide.solve(b01.a.x)
# a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))   -2.0

# Step 2: the friction force, from Newton's second law.
n = make_point("n")  # the normal force
w = make_point("w")  # the weight
f = make_point("f")  # the friction force
m = sp.Symbol("m")  # the mass
a = make_point("a")  # the acceleration

push = (
    System()
    .add(*newtons_second_law([n, w, f], m, a))  # (1), (2)
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(m, 0.45)  # kg
    .known(a.x, sol_1.number(b01.a.x))  # m/s², from step 1
)
sol_2 = push.solve(f.x)
# f_x = a_x*m - n_x - w_x   -0.9

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
