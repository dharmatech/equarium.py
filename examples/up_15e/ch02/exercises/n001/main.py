"""University Physics, 15th edition, Exercise 2.1, with the physics code.

A car moves in the +x direction on a straight, level road. Over its
first 4.00 s its average velocity is 6.25 m/s. How far does it travel
in those 4.00 s?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.1/up-exercise-2.1-000.py`. Its zeros are
values, so they are zero knowns here, never eliminated: the formula
keeps `c0.t` and `c0.pos.x`, as the old one does.

    uv run python -m examples.up_15e.ch02.exercises.n001.main
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Particle, X
from examples.answers import Answer

c = Particle("c", 2, X)  # the car
c0, c1 = c.states
c01 = c.edge(0, 1)

car = (
    System()
    .add(*c.kinematics())
    .add(*c01.constant_acceleration())
    .known(c0.pos.x, 0 * meter)
    .known(c0.t, 0 * second)
    .known(c1.t, 4.0 * second)
    .known(c01.v_av.x, 6.25 * meter / second)
)

sol = car.solve(c1.pos.x)
# c1.pos.x = c0.pos.x - c0.t*c01.v_av.x + c01.v_av.x*c1.t   25.0*meter

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, c1.pos.x, "25.0", unit=meter),
]

if __name__ == "__main__":
    car.show()
    print()
    sol.show()
