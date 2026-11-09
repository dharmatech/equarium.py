"""University Physics, 15th edition, Exercise 2.19, with the physics code.

An antelope with constant acceleration covers the 70.0 m between two
points in 6.00 s, passing the second at 15.0 m/s. What are (a) its speed
at the first point and (b) its acceleration?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.19/up-exercise-2.19-000.py`. Its zero is a
value, so it's a zero known here, never eliminated.

    uv run python -m examples.up_15e.ch02.exercises.n019.main
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

o = make_states_model("o", 2)  # the antelope
o0, o1 = o.states
o01 = o.edges[0]

antelope = (
    System()
    .add(*kinematics_fundamental(o, axes=["x"]))
    .known(o0.pos.x, 0 * meter)
    .known(o1.pos.x, 70.0 * meter)
    .known(o01.dt, 6.00 * second)
    .known(o1.vel.x, 15.0 * meter / second)
)

# (a) Its speed at the first point.
sol_a = antelope.solve(o0.vel.x)
# o_0_v_x = (-dt_o_0_1*o_1_v_x - 2*o_0_x + 2*o_1_x)/dt_o_0_1   8.33*meter/second

# (b) Its acceleration.
sol_b = antelope.solve(o01.a.x)
# a_x_o_0_1 = (2*dt_o_0_1*o_1_v_x + 2*o_0_x - 2*o_1_x)/dt_o_0_1**2   1.11*meter/second**2

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, o0.vel.x, "8.33", unit=meter/second),
    Answer(sol_b, o01.a.x, "1.11", unit=meter/second**2),
]

if __name__ == "__main__":
    antelope.show()
    print()
    sol_a.show()
    print()
    sol_b.show()
