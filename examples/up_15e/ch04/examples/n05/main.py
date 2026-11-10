"""University Physics, 15th edition, Example 4.5, with the physics code.

A 0.45 kg ketchup bottle is pushed along a level counter. It leaves the
hand at 2.0 m/s and slides 1.0 m before stopping, slowed by a constant
horizontal friction force. What are the friction force's magnitude and
direction?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.5/up-example-4.5-001-one-step.py`: the
kinematics and Newton's second law in one system, solved all at once.
Newton's second law is on the bottle's edge, `b01.newton(n, w, f)`, so
its acceleration is the kinematics', `b01.a.x`, and its mass is the
bottle's, `b.mass`. The old script made its own `a` and `m`, and linked
the two accelerations with an equation, `a.x = b01.a.x`. The forces are
in x only, as the bottle is, so the old script's y equation, which no
want needs, has no counterpart here. Its zeros are values, so they are
zero knowns here, never eliminated: the formula keeps the book's general
form. The want is `f.x`, the friction's x-component, the book's
ΣF_x = -f; the book's f = 0.90 N is its magnitude, and the sign gives
its direction.

    uv run python -m examples.up_15e.ch04.examples.n05.main
"""

from equarium import System
from equarium.physics import Particle, Vector, X
from examples.answers import Answer

b = Particle("b", 2, X)  # the bottle
b0, b1 = b.states
b01 = b.edge(0, 1)

n = Vector("n", X)  # the normal force
w = Vector("w", X)  # the weight
f = Vector("f", X)  # the friction force

counter = (
    System()
    .add(*b.kinematics())  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
    .add(*b01.newton(n, w, f))  # (5): Newton's acceleration is the kinematics'
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(b.mass, 0.45)  # kg
)

sol = counter.solve(f.x)
# f.x = (b.mass*b0.vel.x**2/2 - b.mass*b1.vel.x**2/2 - b0.pos.x*n.x - b0.pos.x*w.x
#        + b1.pos.x*n.x + b1.pos.x*w.x)/(b0.pos.x - b1.pos.x)   -0.9

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, f.x, "-0.90"),  # N, the book's ΣF_x = -f
]

if __name__ == "__main__":
    counter.show()
    print()
    sol.show()
