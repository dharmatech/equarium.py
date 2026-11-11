"""University Physics, 15th edition, Exercise 2.3, with the physics code,
in two steps: the usual trip's distance feeds the slow trip's system.

The usual drive home averages 105 km/h and takes 1 h 50 min. One day
traffic holds the average to 70 km/h over the same distance. How much
longer does the trip take?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.3/up-exercise-2.3-000-two-steps.py`, with
its `1 * h + 50/60 * h`, a Float. Its zeros are values, so they are zero
knowns here, never eliminated. The old script stops at the slow trip's
time, 2.75 h. The book's answer, `longer`, is added to the second
system, with `Eq(longer, cb1.t - ca1.t)` and `ca1.t` a known there.

    uv run python -m examples.up_15e.ch02.exercises.n003.main_two_steps
"""

import sympy as sp
from sympy.physics.units import hour, kilometer, minute

from equarium import System
from equarium.physics import Particle, X
from examples.answers import Answer

ca = Particle("ca", 2, X)  # the usual trip
cb = Particle("cb", 2, X)  # the slow trip
ca0, ca1 = ca.states
cb0, cb1 = cb.states
ca01 = ca.edge(0, 1)
cb01 = cb.edge(0, 1)

usual_time = 1 * hour + 50 / 60 * hour

# Step 1: the usual trip's distance.
usual = (
    System()
    .add(*ca.kinematics())
    .add(*ca01.constant_acceleration())
    .known(ca0.t, 0 * hour)
    .known(ca1.t, usual_time)
    .known(ca0.pos.x, 0 * kilometer)
    .known(ca01.v_av.x, 105 * kilometer / hour)
)
distance = usual.solve(ca1.pos.x)
# ca1.pos.x = ca0.pos.x - ca0.t*ca01.v_av.x + ca01.v_av.x*ca1.t   192.5*kilometer

# Step 2: the slow trip, over that distance.
longer = sp.Symbol("longer")

slow_trip = (
    System()
    .add(*cb.kinematics())
    .add(*cb01.constant_acceleration())
    .add(sp.Eq(longer, cb1.t - ca1.t))  # added: how much longer the slow trip takes
    .known(cb0.t, 0 * hour)
    .known(cb0.pos.x, 0 * kilometer)
    .known(cb01.v_av.x, 70 * kilometer / hour)
    .known(cb1.pos.x, distance.number(ca1.pos.x))  # the distance from step 1
    .known(ca1.t, usual_time)
)
slow = slow_trip.solve(cb1.t, longer)
# cb1.t = (-cb0.pos.x + cb0.t*cb01.v_av.x + cb1.pos.x)/cb01.v_av.x   2.75*hour
# longer, in minutes                                               55

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(slow.in_units(minute), longer, "55", unit=minute),
]

if __name__ == "__main__":
    usual.show()
    print()
    distance.show()
    print()
    slow_trip.show()
    print()
    slow.show()
    print()
    slow.in_units(minute).show()
