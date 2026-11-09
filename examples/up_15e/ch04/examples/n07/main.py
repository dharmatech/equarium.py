"""University Physics, 15th edition, Example 4.7, written out, with units.

A truck moving in the +x direction brakes hard; the x-component of the
net external force on it is -1.83 × 10⁴ N. What is its acceleration?
The book first finds the mass from the weight.

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.7/up-example-4.7-000.py`, with the book's
weight and g. The book contradicts itself: its statement gives the
weight as 2.45 × 10⁴ N, but its solution's 2540 kg and -7.20 m/s²
follow from 2.49 × 10⁴ N, its SET UP's number, with g = 9.80 m/s². The
old script uses 2.45 × 10⁴ N and 9.81, and gets -7.33 m/s². The mass is
added as a want.

    uv run python -m examples.up_15e.ch04.examples.n07.main
"""

import sympy as sp
from sympy.physics.units import kilogram, meter, newton, second

from equarium import System, eq_flat
from examples.answers import Answer

w = sp.Symbol("w")  # the weight
m = sp.Symbol("m")  # the mass
g = sp.Symbol("g")  # gravity
F_x = sp.Symbol("F_x")  # the net force
a_x = sp.Symbol("a_x")  # the acceleration

truck = (
    System()
    .add(*eq_flat(w, m * g, F_x, m * a_x))  # (1), (2)
    .known(w, 2.49e4 * newton)  # the book's SET UP; its statement says 2.45e4
    .known(F_x, -1.83e4 * newton)
    .known(g, 9.80 * meter / second**2)
)

sol = truck.solve(a_x, m)
# a_x = F_x*g/w   -7.20240963855422*meter/second**2
# m = w/g         2540.81632653061*newton*second**2/meter, which is 2540.8 kg

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol.in_units(meter, second), a_x, "-7.20", unit=meter / second**2),
    Answer(sol.in_units(kilogram), m, "2.54e3", unit=kilogram),  # the book's 2540 kg
]

if __name__ == "__main__":
    truck.show()
    print()
    sol.show()
    print()
    sol.in_units(meter, second).show()
    print()
    sol.in_units(kilogram).show()
