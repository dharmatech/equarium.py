"""University Physics, 15th edition, Example 4.4, with the physics code.

A worker pushes a 40 kg box horizontally with a constant 20 N force
across a level floor with negligible friction. What is the box's
acceleration?

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.4/up-example-4.4-000.py`, with the physics
code's lone vectors and `.eq` where it had local helpers for the forces
and Newton's second law. Its zeros are values, so they are zero knowns
here, never eliminated: the formula keeps `n.x` and `w.x`. Its
`eliminate_zero_eqs` call changes nothing, since it has no zero
equations, so it has no counterpart here.

    uv run python -m examples.up_15e.ch04.examples.n04.main
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Vector
from examples.answers import Answer

F = Vector("F", XY)  # the worker's force
n = Vector("n", XY)  # the normal force
w = Vector("w", XY)  # the weight
m = sp.Symbol("m")  # the mass
a = Vector("a", XY)  # the acceleration

box = (
    System()
    .add(*(F + n + w).eq(a * m))  # (1), (2)
    .known(F.x, 20)  # N
    .known(F.y, 0)  # N
    .known(a.y, 0)  # m/s²
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(m, 40)  # kg
)

sol = box.solve(a.x)
# a.x = (F.x + n.x + w.x)/m   0.5

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, a.x, "0.50"),  # m/s²
]

if __name__ == "__main__":
    box.show()
    print()
    sol.show()
