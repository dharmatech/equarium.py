"""University Physics, 15th edition, Exercise 2.1, with the physics code.

A car moves in the +x direction on a straight, level road. Over its
first 4.00 s its average velocity is 6.25 m/s. How far does it travel
in those 4.00 s?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.1/up-exercise-2.1-000.py`. Its zeros are
values, so they are zero knowns here, never eliminated: the formula
keeps `c_0_t` and `c_0_x`, as the old one does.

    uv run python -m examples.up_15e.ch02.exercise_2_1
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

c = make_states_model("c", 2)  # the car
c0, c1 = c.states
c01 = c.edges[0]
assert c01.v_av is not None  # make_states_model includes v_av by default

car = (
    System()
    .add(*kinematics_fundamental(c, axes=["x"]))
    .known(c0.pos.x, 0 * meter)
    .known(c0.t, 0 * second)
    .known(c1.t, 4.0 * second)
    .known(c01.v_av.x, 6.25 * meter / second)
)

sol = car.solve(c1.pos.x)
# c_1_x = -c_0_t*v_av_x_c_0_1 + c_0_x + c_1_t*v_av_x_c_0_1   25.0*meter

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, c1.pos.x, "25.0", unit=meter),
]

if __name__ == "__main__":
    car.show()
    print()
    sol.show()
