"""University Physics, 15th edition, Example 3.13, written out, with units.

You drive north at a constant 88 km/h on a straight road; a truck in the
other lane comes toward you at a constant 104 km/h. In one dimension,
north positive, find (a) the truck's velocity relative to you and
(b) yours relative to the truck. (c) How do they change once you've
passed each other? They don't: the velocities are constant.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.13/up-example-3.13-001-eq.py`: the book's
equations 3.32 and 3.33, written out. Its two solves are one here, with
two wants.

    uv run python -m examples.up_15e.ch03.example_3_13
"""

import sympy as sp
from sympy.physics.units import hour, kilometer

from equarium import System
from examples.answers import Answer

v_YE = sp.Symbol("v_YE")  # your velocity relative to the earth
v_TE = sp.Symbol("v_TE")  # the truck's velocity relative to the earth
v_TY = sp.Symbol("v_TY")  # the truck's velocity relative to you
v_YT = sp.Symbol("v_YT")  # your velocity relative to the truck

road = (
    System()
    .add(sp.Eq(v_TE, v_TY + v_YE), label="3.32")
    .add(sp.Eq(v_YT, -v_TY), label="3.33")
    .known(v_YE, 88 * kilometer / hour)
    .known(v_TE, -104 * kilometer / hour)
)

sol = road.solve(v_TY, v_YT)
# v_TY = v_TE - v_YE    -192.0*kilometer/hour
# v_YT = -v_TE + v_YE   192.0*kilometer/hour

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, v_TY, "-192", unit=kilometer / hour),
    Answer(sol, v_YT, "192", unit=kilometer / hour),
]

if __name__ == "__main__":
    road.show()
    print()
    sol.show()
