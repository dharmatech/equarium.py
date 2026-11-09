"""University Physics, 15th edition, Example 4.5, with the physics code.

A 0.45 kg ketchup bottle is pushed along a level counter. It leaves the
hand at 2.0 m/s and slides 1.0 m before stopping, slowed by a constant
horizontal friction force. What are the friction force's magnitude and
direction?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.5/up-example-4.5-001-one-step.py`: the
kinematics and Newton's second law in one system, linked through the
acceleration, solved all at once. Its zeros are values, so they are zero
knowns here, never eliminated: the formula keeps the book's general
form. The want is f_x, the friction's x-component, the book's
ΣF_x = -f; the book's f = 0.90 N is its magnitude, and the sign gives
its direction.

    uv run python -m examples.up_15e.ch04.examples.n05.main
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

n = make_point("n")  # the normal force
w = make_point("w")  # the weight
f = make_point("f")  # the friction force
m = sp.Symbol("m")  # the mass
a = make_point("a")  # the acceleration

counter = (
    System()
    .add(*kinematics_fundamental(b, axes=["x"]))  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
    .add(*newtons_second_law([n, w, f], m, a))  # (5), (6)
    .add(sp.Eq(a.x, b01.a.x))  # (7): Newton's acceleration is the kinematics'
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(m, 0.45)  # kg
)

sol = counter.solve(f.x)
# f_x = (b_0_v_x**2*m/2 - b_0_x*n_x - b_0_x*w_x - b_1_v_x**2*m/2 + b_1_x*n_x
#        + b_1_x*w_x)/(b_0_x - b_1_x)   -0.9

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, f.x, "-0.90"),  # N, the book's ΣF_x = -f
]

if __name__ == "__main__":
    counter.show()
    print()
    sol.show()
