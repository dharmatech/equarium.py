"""University Physics, 15th edition, Example 3.8, with the physics code.

A projectile is launched at speed v0 and angle α0 between 0 and 90°,
from and back to the same height, with no air resistance. As formulas in
v0, α0 and g, find (a) its maximum height h and (b) its horizontal range
R. For a given v0, (c) which α0 gives the greatest h, and (d) which
gives the greatest R?

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.8-v1-000.py`, with its bug fixed: it
solved the range from the top-of-flight system, which gives half of it.
Here the range comes from the range system. Its zero equations are zero
knowns here, followed by `eliminate_zeros()` where it called its
`eliminate_zero_eqs`: four in the base, `p_1_v_y` at the top and
`p_1_y` back at the launch height. The launch is polar both ways, on the
state's `vel.mag` and `vel.angle`. All the givens are symbols: knowns
with no number. The old script's g = 9.81 was never used.

The old script eliminates `p_0_v_x` by hand before it solves. Here that
isn't enough: with `p_0_v_x` eliminated through `p_0_v_x = p_1_v_x`, the
solve still finds no roots, since the two-way equations (12) and (13)
still hold unknowns. The old solve found its roots only because its
`values` gave the magnitude and the angle the symbols `v0` and `a0`,
which became two more unknowns. So this port eliminates `p_0_v_x` and
`p_0_v_y` through the polar equations (10) and (11). That leaves (12)
and (13) with knowns only, so the solve leaves them out.

    uv run python -m examples.up_15e.ch03.example_3_8
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Formula

p = make_states_model("p", 2)  # the projectile
p0, p1 = p.states
p01 = p.edges[0]
assert p0.vel.mag is not None and p0.vel.angle is not None  # make_states_model sets both

g = sp.Symbol("g")

launch = (
    System()
    .add(*kinematics_fundamental(p, axes=["x", "y"]))  # (1) to (7)
    .add(*eq_flat(p01.a.y, -g, p0.vel.x, p1.vel.x))  # (8), (9): projectile motion
    .known({p0.pos.x: 0, p0.pos.y: 0, p01.a.x: 0, p0.t: 0})  # from the origin, at t = 0
    .eliminate_zeros()
    # Launched at speed v0 and angle α0, polar both ways: (10) to (13).
    .add(
        *eq_flat(
            p0.vel.x, p0.vel.mag * sp.cos(p0.vel.angle),
            p0.vel.y, p0.vel.mag * sp.sin(p0.vel.angle),
            p0.vel.mag, sp.sqrt(p0.vel.x**2 + p0.vel.y**2),
            p0.vel.angle, sp.atan2(p0.vel.y, p0.vel.x),
        )
    )
    .known(g)
    .known(p0.vel.mag)  # v0
    .known(p0.vel.angle)  # α0
)

# (a) The highest point, where the vertical velocity is zero.
top = (
    launch.known(p1.vel.y, 0)
    .eliminate_zeros()
    .eliminate(p0.vel.x, using="10")  # see the docstring
    .eliminate(p0.vel.y, using="11")
)
sol_top = top.solve(p1.t, p1.pos.y)
# p_1_t = p_0_v_mag*sin(p_0_v_angle)/g
# p_1_y = p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)

# (b) Back at the launch height.
back = (
    launch.known(p1.pos.y, 0)
    .eliminate_zeros()
    .eliminate(p0.vel.x, using="10")
    .eliminate(p0.vel.y, using="11")
)
sol_range = back.solve(p1.t, p1.pos.x)
# p_1_t = 2*p_0_v_mag*sin(p_0_v_angle)/g
# p_1_x = p_0_v_mag**2*sin(2*p_0_v_angle)/g

# (c) and (d) need a maximization over α0, which the old script never
# had. The book's answers: h is greatest at α0 = 90°, and R at 45°.

BOOK: list[Formula] = [  # University Physics, 15th ed.
    Formula(sol_top, p1.t, "p_0_v_mag*sin(p_0_v_angle)/g"),
    Formula(sol_top, p1.pos.y, "p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)"),
    Formula(sol_range, p1.t, "2*p_0_v_mag*sin(p_0_v_angle)/g"),
    Formula(sol_range, p1.pos.x, "p_0_v_mag**2*sin(2*p_0_v_angle)/g"),
]

if __name__ == "__main__":
    top.show()
    print()
    sol_top.show()
    print()
    back.show()
    print()
    sol_range.show()
