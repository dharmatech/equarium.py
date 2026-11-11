"""University Physics, 15th edition, Example 3.8, with the physics code.

A projectile is launched at speed v0 and angle α0 between 0 and 90°,
from and back to the same height, with no air resistance. As formulas in
v0, α0 and g, find (a) its maximum height h and (b) its horizontal range
R. For a given v0, (c) which α0 gives the greatest h, and (d) which
gives the greatest R?

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.8-v1-000.py`, with its bug fixed: it
solved the range from the top-of-flight system, which gives half of it.
Here the range comes from the range system. Projectile motion is the
projectile setup, `p01.projectile(g)`, which is the old script's
`p01.a.y = -g` and `p0.vel.x = p1.vel.x`, with its zero `p01.a.x`. Its
zero equations are zero knowns here, followed by `eliminate_zeros()`
where it called its `eliminate_zero_eqs`: four in the base, `p1.vel.y`
at the top and `p1.pos.y` back at the launch height. The launch is
polar one way, with `p0.vel.from_polar()`, on `p0.vel.mag` and
`p0.vel.angle`. All the givens are symbols: knowns with no number. The
old script's g = 9.81 was never used.

Each part solves all at once. The old script eliminated `p0.vel.x` by
hand before it solved, and with the launch polar both ways this port
eliminated `p0.vel.x` and `p0.vel.y` through the polar equations, or
the solve found no roots: the equations back to polar still held
unknowns. One way, neither step is needed.

    uv run python -m examples.up_15e.ch03.examples.n08.main
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Particle
from examples.answers import Formula

p = Particle("p", 2, XY)  # the projectile
p0, p1 = p.states
p01 = p.edge(0, 1)

g = sp.Symbol("g")

flight = p01.projectile(g)

launch = (
    System()
    .add(*p.kinematics())  # (1) to (5)
    .add(*p01.constant_acceleration())  # (6), (7): projectile motion, only gravity
    .add(*flight.equations)  # (8), (9): projectile motion
    .known(flight.knowns)  # p01.a.x = 0
    .known({p0.pos.x: 0, p0.pos.y: 0, p0.t: 0})  # from the origin, at t = 0
    .eliminate_zeros()
    # Launched at speed v0 and angle α0, polar one way: (10), (11).
    .add(*p0.vel.from_polar())
    .known(g)
    .known(p0.vel.mag)  # v0
    .known(p0.vel.angle)  # α0
)

# (a) The highest point, where the vertical velocity is zero.
top = launch.known(p1.vel.y, 0).eliminate_zeros()
sol_top = top.solve(p1.t, p1.pos.y)
# p1.t = p0.vel.mag*sin(p0.vel.angle)/g
# p1.pos.y = p0.vel.mag**2*sin(p0.vel.angle)**2/(2*g)

# (b) Back at the launch height.
back = launch.known(p1.pos.y, 0).eliminate_zeros()
sol_range = back.solve(p1.t, p1.pos.x)
# p1.t = 2*p0.vel.mag*sin(p0.vel.angle)/g
# p1.pos.x = p0.vel.mag**2*sin(2*p0.vel.angle)/g

# (c) and (d) need a maximization over α0, which the old script never
# had. The book's answers: h is greatest at α0 = 90°, and R at 45°.

BOOK: list[Formula] = [  # University Physics, 15th ed.
    Formula(sol_top, p1.t, p0.vel.mag * sp.sin(p0.vel.angle) / g),
    Formula(sol_top, p1.pos.y, p0.vel.mag**2 * sp.sin(p0.vel.angle) ** 2 / (2 * g)),
    Formula(sol_range, p1.t, 2 * p0.vel.mag * sp.sin(p0.vel.angle) / g),
    Formula(sol_range, p1.pos.x, p0.vel.mag**2 * sp.sin(2 * p0.vel.angle) / g),
]

if __name__ == "__main__":
    top.show()
    print()
    sol_top.show()
    print()
    back.show()
    print()
    sol_range.show()
