"""University Physics, 15th edition, Example 3.7, with the physics code.

A baseball leaves the bat at 37.0 m/s, 53.1° above the horizontal, from
ground level, with no air resistance. (a) Find its position and its
velocity (magnitude and direction) at t = 2.00 s. (b) When does it reach
its highest point, and how high is it then? (c) Find the horizontal
range R, and its velocity just before it lands.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.7-v1-000.py`, with the book's
g = 9.80 m/s², not the old 9.81: with 9.81 the speed at 2.00 s and the
height miss the book's answers. Its four zero equations are zero knowns
here, followed by `eliminate_zeros()` where it called its
`eliminate_zero_eqs`. (b)'s `b1.vel.y = 0` and (c)'s `b1.pos.y = 0` are
equations it added to a copy, so here each is a zero known on its
branch, eliminated there. The launch is polar one way, in the script's
own symbols, and the speed and angle at 2.00 s are written by hand.

The old script eliminates `b1_vel_angle` by hand before it solves for
the degrees, and so does this port: without the step, SymPy leaves
`b1_vel_angle_deg` undetermined. The old script solved the angle in
radians before the step, so that solve is `sol_a_radians` here. (b) and
(c) branch from after the step, as in the old script. Its solves, one
want or a few at a time, are one per part here. (c)'s landing time and
angle are added as wants.

    uv run python -m examples.up_15e.ch03.examples.n07.main
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics import XY, Particle
from examples.answers import Answer

b = Particle("b", 2, XY)  # the ball
b0, b1 = b.states
b01 = b.edge(0, 1)

g = sp.Symbol("g")
b0_vel_mag, b0_vel_angle = sp.symbols("b0_vel_mag b0_vel_angle")
b1_vel_mag, b1_vel_angle, b1_vel_angle_deg = sp.symbols(
    "b1_vel_mag b1_vel_angle b1_vel_angle_deg"
)

launch = (
    System()
    .add(*b.kinematics())  # (1) to (7)
    .add(*eq_flat(b01.a.y, -g, b0.vel.x, b1.vel.x))  # (8), (9): projectile motion
    .known({b0.pos.x: 0, b0.pos.y: 0, b01.a.x: 0, b0.t: 0})  # from the ground, at t = 0
    .eliminate_zeros()
    .known(g, 9.80)  # m/s²
    # The launch, polar one way: (10), (11).
    .add(
        *eq_flat(
            b0.vel.x, b0_vel_mag * sp.cos(b0_vel_angle),
            b0.vel.y, b0_vel_mag * sp.sin(b0_vel_angle),
        )
    )
    .known(b0_vel_mag, 37.0)  # m/s
    .known(b0_vel_angle, sp.N(sp.rad(53.1)))  # degrees to radians
)

# The speed and direction, by hand from the components: (12), (13).
speed = launch.add(
    *eq_flat(
        b1_vel_mag, sp.sqrt(b1.vel.x**2 + b1.vel.y**2),
        b1_vel_angle, sp.atan2(b1.vel.y, b1.vel.x),
    )
)
# The angle in degrees, (14), then the old script's by-hand step.
flight = speed.add(sp.Eq(b1_vel_angle_deg, sp.deg(b1_vel_angle))).eliminate(b1_vel_angle)

# (a) Position and velocity at t = 2.00 s.
sol_a = flight.known(b1.t, 2.00).solve(  # s
    b1.pos.x, b1.pos.y, b1.vel.x, b1.vel.y, b1_vel_mag, b1_vel_angle_deg
)
# b1.pos.x = b0_vel_mag*b1.t*cos(b0_vel_angle)                    44.4
# b1.pos.y = b1.t*(2*b0_vel_mag*sin(b0_vel_angle) - g*b1.t)/2     39.6
# b1.vel.x = b0_vel_mag*cos(b0_vel_angle)                         22.2
# b1.vel.y = b0_vel_mag*sin(b0_vel_angle) - g*b1.t                9.99
# b1_vel_mag = sqrt(b0_vel_mag**2 - 2*b0_vel_mag*g*b1.t*sin(b0_vel_angle) + g**2*b1.t**2)
#                                                                 24.36
# b1_vel_angle_deg = 180*atan2(b0_vel_mag*sin(b0_vel_angle) - g*b1.t,
#                              b0_vel_mag*cos(b0_vel_angle))/pi   24.2
sol_a_radians = speed.known(b1.t, 2.00).solve(b1_vel_angle)  # s; the old script's radians
# b1_vel_angle = atan2(b0_vel_mag*sin(b0_vel_angle) - g*b1.t,
#                      b0_vel_mag*cos(b0_vel_angle))              0.4225

# (b) The highest point, where the vertical velocity is zero.
sol_b = flight.known(b1.vel.y, 0).eliminate_zeros().solve(b1.t, b1.pos.y)  # m/s
# b1.t = b0_vel_mag*sin(b0_vel_angle)/g                           3.02
# b1.pos.y = b0_vel_mag**2*sin(b0_vel_angle)**2/(2*g)             44.7

# (c) Back at ground level. The time and the angle are added wants.
sol_c = (
    flight.known(b1.pos.y, 0)  # m
    .eliminate_zeros()
    .solve(b1.t, b1.pos.x, b1.vel.x, b1.vel.y, b1_vel_angle_deg)
)
# b1.t = 2*b0_vel_mag*sin(b0_vel_angle)/g                         6.04
# b1.pos.x = b0_vel_mag**2*sin(2*b0_vel_angle)/g                  134
# b1.vel.x = b0_vel_mag*cos(b0_vel_angle)                         22.2
# b1.vel.y = -b0_vel_mag*sin(b0_vel_angle)                        -29.6
# b1_vel_angle_deg = 180*atan2(-b0_vel_mag*sin(b0_vel_angle),
#                              b0_vel_mag*cos(b0_vel_angle))/pi   -53.1

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, b1.pos.x, "44.4"),  # m
    Answer(sol_a, b1.pos.y, "39.6"),  # m
    Answer(sol_a, b1.vel.x, "22.2"),  # m/s
    Answer(sol_a, b1.vel.y, "10.0"),  # m/s
    Answer(sol_a, b1_vel_mag, "24.4"),  # m/s
    Answer(sol_a, b1_vel_angle_deg, "24.2"),  # degrees
    Answer(sol_b, b1.t, "3.02"),  # s
    Answer(sol_b, b1.pos.y, "44.7"),  # m
    Answer(sol_c, b1.t, "6.04"),  # s, a new want
    Answer(sol_c, b1.pos.x, "134"),  # m
    Answer(sol_c, b1.vel.y, "-29.6"),  # m/s
    Answer(sol_c, b1_vel_angle_deg, "-53.1"),  # degrees, a new want
]

if __name__ == "__main__":
    flight.show()
    for sol in (sol_a, sol_a_radians, sol_b, sol_c):
        print()
        sol.show()
