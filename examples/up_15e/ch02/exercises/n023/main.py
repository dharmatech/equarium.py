"""University Physics, 15th edition, Exercise 2.23, with the physics code.

A body survives a sudden stop if the deceleration stays under 250 m/s².
In a crash at 105 km/h, an airbag stops you. Over what minimum distance
must it stop you?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.23/up-exercise-2.23-000.py`. Its zeros are
values, so they are zero knowns here, never eliminated: the formula
keeps `b0.pos.x` and `b1.vel.x`, as the old one does. The old script ends at
the unconverted number, and `in_units(meter, second)` converts it.

    uv run python -m examples.up_15e.ch02.exercises.n023.main
"""

from sympy.physics.units import hour, kilometer, meter, second

from equarium import System
from equarium.physics import Particle, X
from examples.answers import Answer

b = Particle("b", 2, X)  # the body
b0, b1 = b.states
b01 = b.edge(0, 1)

airbag = (
    System()
    .add(*b.kinematics())
    .known(b01.a.x, -250 * meter / second**2)
    .known(b0.vel.x, 105 * kilometer / hour)
    .known(b1.vel.x, 0 * meter / second)
    .known(b0.t, 0 * second)
    .known(b0.pos.x, 0 * meter)
)

sol = airbag.solve(b1.pos.x)
# b1.pos.x = (2*b0.pos.x*b01.a.x - b0.vel.x**2 + b1.vel.x**2)/(2*b01.a.x)
#            22.05*kilometer**2*second**2/(hour**2*meter), which is 1.70 m

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol.in_units(meter, second), b1.pos.x, "1.70", unit=meter),
]

if __name__ == "__main__":
    airbag.show()
    print()
    sol.show()
    print()
    sol.in_units(meter, second).show()
