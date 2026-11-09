"""University Physics, 15th edition, Exercise 2.3, with the physics code,
both trips in one system.

The usual drive home averages 105 km/h and takes 1 h 50 min. One day
traffic holds the average to 70 km/h over the same distance. How much
longer does the trip take?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.3/up-exercise-2.3-002-one-step.py`, with its
`1 * h + 50/60 * h`, a Float. Its zeros are values, so they are zero
knowns here, never eliminated. The old script stops at the slow trip's
time, 2.75 h. The book's answer, `longer`, is added, with
`Eq(longer, cb1.t - ca1.t)`.

    uv run python -m examples.up_15e.ch02.exercises.n003.main
"""

import sympy as sp
from sympy.physics.units import hour, kilometer, minute

from equarium import System, eq_flat
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

ca = make_states_model("ca", 2)  # the usual trip
cb = make_states_model("cb", 2)  # the slow trip
ca0, ca1 = ca.states
cb0, cb1 = cb.states
ca01 = ca.edges[0]
cb01 = cb.edges[0]
assert ca01.v_av is not None and cb01.v_av is not None  # included by default

longer = sp.Symbol("longer")

trips = (
    System()
    .add(*kinematics_fundamental(ca, axes=["x"]))
    .add(*kinematics_fundamental(cb, axes=["x"]))
    .add(*eq_flat(ca1.pos.x, cb1.pos.x))  # the same distance
    .add(sp.Eq(longer, cb1.t - ca1.t))  # added: how much longer the slow trip takes
    .known(ca0.t, 0 * hour)
    .known(ca1.t, 1 * hour + 50 / 60 * hour)
    .known(ca0.pos.x, 0 * kilometer)
    .known(ca01.v_av.x, 105 * kilometer / hour)
    .known(cb0.t, 0 * hour)
    .known(cb0.pos.x, 0 * kilometer)
    .known(cb01.v_av.x, 70 * kilometer / hour)
)

sol = trips.solve(cb1.t, longer)
# cb_1_t = (-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1 + cb_0_t*v_av_x_cb_0_1
#           - cb_0_x)/v_av_x_cb_0_1   2.75*hour
# longer, in minutes                  55

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol.in_units(minute), longer, "55", unit=minute),
]

if __name__ == "__main__":
    trips.show()
    print()
    sol.show()
    print()
    sol.in_units(minute).show()
