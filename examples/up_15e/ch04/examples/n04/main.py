"""University Physics, 15th edition, Example 4.4, with the physics code.

A worker pushes a 40 kg box horizontally with a constant 20 N force
across a level floor with negligible friction. What is the box's
acceleration?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.4/up-example-4.4-000.py`, with the physics
code's lone vectors and Newton's second law on the box's edge,
`box01.newton(F, n, w)`, where it had local helpers for the forces and
the law. The box is a particle, so its mass is `box.mass` and its
acceleration is the edge's, `box01.a`, where the old script made its own
`m` and `a`. There are no kinematics here: the box has two states only
so that it has an edge. Its zeros are values, so they are zero knowns
here, never eliminated: the formula keeps `n.x` and `w.x`. Its
`eliminate_zero_eqs` call changes nothing, since it has no zero
equations, so it has no counterpart here.

    uv run python -m examples.up_15e.ch04.examples.n04.main
"""

from equarium import System
from equarium.physics import XY, Particle, Vector
from examples.answers import Answer

box = Particle("box", 2, XY)  # the box
box01 = box.edge(0, 1)

F = Vector("F", XY)  # the worker's force
n = Vector("n", XY)  # the normal force
w = Vector("w", XY)  # the weight

push = (
    System()
    .add(*box01.newton(F, n, w))  # (1), (2)
    .known(F.x, 20)  # N
    .known(F.y, 0)  # N
    .known(box01.a.y, 0)  # m/s²
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(box.mass, 40)  # kg
)

sol = push.solve(box01.a.x)
# box01.a.x = (F.x + n.x + w.x)/box.mass   0.5

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, box01.a.x, "0.50"),  # m/s²
]

if __name__ == "__main__":
    push.show()
    print()
    sol.show()
