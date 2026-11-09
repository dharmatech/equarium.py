"""University Physics, 15th edition, Exercise 2.21, with the physics code.

A pitched ball leaves the hand at 45.0 m/s after being accelerated
uniformly from rest over 1.50 m. (a) What was its acceleration? (b) How
long did the pitch take?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.21/up-exercise-2.21-000.py`, without its
GUI calls. Its zeros are values, so they are zero knowns here, never
eliminated: the formulas keep `b_0_x` and `b_0_v_x`, as the old ones do.
Its elimination of the average velocity, only displayed, is the stage
`no_average`.

    uv run python -m examples.up_15e.ch02.exercises.n021.main
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

b = make_states_model("b", 2)  # the baseball
b0, b1 = b.states
b01 = b.edges[0]
assert b01.v_av is not None  # make_states_model includes v_av by default

pitch = (
    System()
    .add(*kinematics_fundamental(b, axes=["x"]))
    .known(b0.pos.x, 0 * meter)
    .known(b1.pos.x, 1.50 * meter)
    .known(b0.vel.x, 0 * meter / second)
    .known(b1.vel.x, 45.0 * meter / second)
    .known(b0.t, 0 * second)
)

# (a) The acceleration.
sol_a = pitch.solve(b01.a.x)
# a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))   675*meter/second**2

# (b) How long the pitch took.
sol_b = pitch.solve(b01.dt)
# dt_b_0_1 = 2*(-b_0_x + b_1_x)/(b_0_v_x + b_1_v_x)   0.0667*second

# The old script then eliminates the average velocity by hand, and only
# displays the result.
no_average = pitch.eliminate(b01.v_av.x)

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, b01.a.x, "675", unit=meter/second**2),
    Answer(sol_b, b01.dt, "0.0667", unit=second),
]

if __name__ == "__main__":
    pitch.show()
    print()
    sol_a.show()
    print()
    sol_b.show()
    print()
    no_average.want(b01.a.x).show()
