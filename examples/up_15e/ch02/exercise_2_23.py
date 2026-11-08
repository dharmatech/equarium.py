"""University Physics, 15th edition, Exercise 2.23, with the physics code.

A body survives a sudden stop if the deceleration stays under 250 m/s².
In a crash at 105 km/h, an airbag stops you. Over what minimum distance
must it stop you?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.23/up-exercise-2.23-000.py`. Its zeros are
values, so they are zero knowns here, never eliminated: the formula
keeps `b_0_x` and `b_1_v_x`, as the old one does. The old script ends at
the unconverted number, and `in_units(meter, second)` converts it.

    uv run python -m examples.up_15e.ch02.exercise_2_23
"""

from sympy.physics.units import hour, kilometer, meter, second

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

b = make_states_model("b", 2)  # the body
b0, b1 = b.states
b01 = b.edges[0]

airbag = (
    System()
    .add(*kinematics_fundamental(b, axes=["x"]))
    .known(b01.a.x, -250 * meter / second**2)
    .known(b0.vel.x, 105 * kilometer / hour)
    .known(b1.vel.x, 0 * meter / second)
    .known(b0.t, 0 * second)
    .known(b0.pos.x, 0 * meter)
)

sol = airbag.solve(b1.pos.x)
# b_1_x = (2*a_x_b_0_1*b_0_x - b_0_v_x**2 + b_1_v_x**2)/(2*a_x_b_0_1)
#         22.05*kilometer**2*second**2/(hour**2*meter), which is 1.70 m

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol.in_units(meter, second), b1.pos.x, "1.70", unit=meter),
]

if __name__ == "__main__":
    airbag.show()
    print()
    sol.show()
    print()
    sol.in_units(meter, second).show()
