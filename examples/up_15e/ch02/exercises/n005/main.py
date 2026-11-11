"""University Physics, 15th edition, Exercise 2.5, with the physics code.

You walk 60.0 m east from a door to a windmill in 28.0 s, then 40.0 m
west to a bench in 36.0 s. For the whole trip, what are (a) your average
velocity and (b) your average speed?

Ported from combine-equations.py's
`examples/up/ch2/exercises/2.5/up-exercise-2.5-001.py`: three states,
two intervals, and its `eq_flat` of the displacements and the averages,
`Abs` included. Its zeros are values, so they are zero knowns here,
never eliminated. Its two solves are one here, with two wants.

    uv run python -m examples.up_15e.ch02.exercises.n005.main
"""

import sympy as sp
from sympy.physics.units import meter, second

from equarium import System, eq_flat
from equarium.physics import Particle, X
from examples.answers import Answer

dx_p_0_1 = sp.Symbol("dx_p_0_1")
dx_p_1_2 = sp.Symbol("dx_p_1_2")

avg_speed_02 = sp.Symbol("avg_speed_02")
avg_vel_02 = sp.Symbol("avg_vel_02")

p = Particle("p", 3, X)  # the person: at the door, the windmill, the bench
p0, p1, p2 = p.states
p01 = p.edge(0, 1)
p12 = p.edge(1, 2)

walk = (
    System()
    .add(*p.kinematics())
    .add(*p01.constant_acceleration())
    .add(*p12.constant_acceleration())
    .add(*eq_flat(
        dx_p_0_1, p1.pos.x - p0.pos.x,
        dx_p_1_2, p2.pos.x - p1.pos.x,

        avg_speed_02, (sp.Abs(dx_p_0_1) + sp.Abs(dx_p_1_2)) / (p2.t - p0.t),

        avg_vel_02,   (p2.pos.x - p0.pos.x) / (p2.t - p0.t),
    ))
    .known(p0.t, 0 * second)
    .known(p01.dt, 28.0 * second)
    .known(p12.dt, 36.0 * second)
    .known(dx_p_0_1, 60.0 * meter)
    .known(dx_p_1_2, -40.0 * meter)
    .known(p0.pos.x, 0 * meter)
)

sol = walk.solve(avg_vel_02, avg_speed_02)
# avg_vel_02 = (dx_p_0_1 + dx_p_1_2)/(p01.dt + p12.dt)               0.3125*meter/second
# avg_speed_02 = (Abs(dx_p_0_1) + Abs(dx_p_1_2))/(p01.dt + p12.dt)   1.5625*meter/second

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, avg_vel_02, "0.313", unit=meter/second),
    Answer(sol, avg_speed_02, "1.56", unit=meter/second),
]

if __name__ == "__main__":
    walk.show()
    print()
    sol.show()
