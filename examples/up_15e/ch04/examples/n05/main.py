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
form. The want is `f.x`, the friction's x-component, the book's
ΣF_x = -f; the book's f = 0.90 N is its magnitude, and the sign gives
its direction.

    uv run python -m examples.up_15e.ch04.examples.n05.main
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Particle, Vector, X
from examples.answers import Answer

b = Particle("b", 2, X)  # the bottle
b0, b1 = b.states
b01 = b.edge(0, 1)

n = Vector("n", XY)  # the normal force
w = Vector("w", XY)  # the weight
f = Vector("f", XY)  # the friction force
m = sp.Symbol("m")  # the mass
a = Vector("a", XY)  # the acceleration

counter = (
    System()
    .add(*b.kinematics())  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
    .add(*(n + w + f).eq(a * m))  # (5), (6)
    .add(sp.Eq(a.x, b01.a.x))  # (7): Newton's acceleration is the kinematics'
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(m, 0.45)  # kg
)

sol = counter.solve(f.x)
# f.x = (m*b0.vel.x**2/2 - m*b1.vel.x**2/2 - b0.pos.x*n.x - b0.pos.x*w.x + b1.pos.x*n.x
#        + b1.pos.x*w.x)/(b0.pos.x - b1.pos.x)   -0.9

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, f.x, "-0.90"),  # N, the book's ΣF_x = -f
]

if __name__ == "__main__":
    counter.show()
    print()
    sol.show()
