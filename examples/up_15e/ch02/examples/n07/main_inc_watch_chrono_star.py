"""University Physics, 15th edition, Example 2.7, with the physics code,
with the states in time order, each joined straight to the throw.

A ball is thrown straight up at 15.0 m/s from level with a roof railing,
then falls freely (the book's Fig. 2.24; upward positive, origin at the
railing).

(a) Where is it, and how fast is it moving, 1.00 s and 4.00 s later?

(b) What is its velocity when it is 5.00 m above the railing?

(c) How high does it go?

(d) What is its acceleration at the top?

b0 is the throw, b1 is 5.00 m up going up, b2 is at 1.00 s, b3 is the
top, b4 is 5.00 m up coming down, and b5 is at 4.00 s. Each state is
given by what the book says about it. b1 and b4 are both 5.00 m up, and
the equations can't tell which comes first, so the solve finds four
roots. The time order, as a relation, keeps the one that fits; numbered
in an order that can't happen, it keeps none and says which relation
failed.

`b.edge(0, 2)` is refused, since a particle's edges join consecutive
states, so the edges are built with `Edge(b0, b2)`, and
`edge_kinematics` writes the 2.2 and 2.4 that `b.kinematics()` writes
for consecutive edges. The system steps end in `;`, so their 20
equations don't print at every step.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n07/main_inc_watch_chrono_star.py
"""

from typing import cast

import sympy as sp
from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Edge, Particle, Y
from examples.answers import Answer


def edge_kinematics(e: Edge[Y]) -> list[sp.Eq]:
    """2.2 and 2.4 for one edge, between any two states."""
    return [
        cast(sp.Eq, sp.Eq(e.dt, e.end.t - e.start.t)),
        cast(sp.Eq, sp.Eq(e.v_av.y, (e.end.pos.y - e.start.pos.y) / e.dt)),
        cast(sp.Eq, sp.Eq(e.a.y, (e.end.vel.y - e.start.vel.y) / e.dt)),
    ]


def leg(e: Edge[Y]) -> list[sp.Eq]:
    """An edge with free fall over it: 2.2, 2.4 and 2.10."""
    return [*edge_kinematics(e), *e.constant_acceleration()]


b = Particle("b", 6, Y)  # the ball
#> particle b (y): b0, b1, b2, b3, b4, b5

b0, b1, b2, b3, b4, b5 = b.states;

g = -9.8 * meter / second**2;

b01, b02, b03, b04, b05 = (Edge(b0, s) for s in (b1, b2, b3, b4, b5))
#> (b01: b0 → b1, b02: b0 → b2, b03: b0 → b3, b04: b0 → b4, b05: b0 → b5)

ball = System().add(*leg(b01), *leg(b02), *leg(b03), *leg(b04), *leg(b05));

# Thrown at t = 0, from the railing, at 15.0 m/s, then in free fall.
ball = ball.known({b0.t: 0 * second, b0.pos.y: 0 * meter}).eliminate_zeros();

ball = ball.known({
    b0.vel.y: 15.0 * meter / second,
    b01.a.y: g, b02.a.y: g, b03.a.y: g, b04.a.y: g, b05.a.y: g
});

# The moments, in the order they happen.
ball = ball.known({
    b1.pos.y: 5.0 * meter,         # 5.00 m up, going up
    b2.t:     1.0 * second,
    b3.vel.y: 0 * meter / second,  # the top
    b4.pos.y: 5.0 * meter,         # 5.00 m up, coming down
    b5.t:     4.0 * second
})
#>  (1)  b01.dt     = b1.t
#>  (2)  b01.v_av.y = b1.pos.y/b01.dt
#>  (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>  (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>  (5)  b02.dt     = b2.t
#>  (6)  b02.v_av.y = b2.pos.y/b02.dt
#>  (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>  (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#>  (9)  b03.dt     = b3.t
#> (10)  b03.v_av.y = b3.pos.y/b03.dt
#> (11)  b03.a.y    = (-b0.vel.y + b3.vel.y)/b03.dt
#> (12)  b03.v_av.y = b0.vel.y/2 + b3.vel.y/2
#> (13)  b04.dt     = b4.t
#> (14)  b04.v_av.y = b4.pos.y/b04.dt
#> (15)  b04.a.y    = (-b0.vel.y + b4.vel.y)/b04.dt
#> (16)  b04.v_av.y = b0.vel.y/2 + b4.vel.y/2
#> (17)  b05.dt     = b5.t
#> (18)  b05.v_av.y = b5.pos.y/b05.dt
#> (19)  b05.a.y    = (-b0.vel.y + b5.vel.y)/b05.dt
#> (20)  b05.v_av.y = b0.vel.y/2 + b5.vel.y/2
#> knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>         b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#>         b03.a.y = -9.8*meter/second**2, b04.a.y = -9.8*meter/second**2,
#>         b05.a.y = -9.8*meter/second**2, b1.pos.y = 5.0*meter,
#>         b2.t = 1.0*second, b3.vel.y = 0, b4.pos.y = 5.0*meter,
#>         b5.t = 4.0*second
#> wants: none
#> connected: none
#> ready: (5), (11), (12), (17)

# When is each moment? b1 and b4 can each be the earlier or the later
# time at 5.00 m.
ball.solve(b1.t, b3.t, b4.t)
#> root 1:
#>   b1.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#>   b1.t = 2.68055384383517*second
#>   b3.t = (-b0.vel.y + b3.vel.y)/b03.a.y
#>   b3.t = 1.53061224489796*second
#>   b4.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y))/b04.a.y
#>   b4.t = 2.68055384383517*second
#> root 2:
#>   b1.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#>   b1.t = 2.68055384383517*second
#>   b3.t = (-b0.vel.y + b3.vel.y)/b03.a.y
#>   b3.t = 1.53061224489796*second
#>   b4.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y))/b04.a.y
#>   b4.t = 0.380670645960751*second
#> root 3:
#>   b1.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#>   b1.t = 0.380670645960751*second
#>   b3.t = (-b0.vel.y + b3.vel.y)/b03.a.y
#>   b3.t = 1.53061224489796*second
#>   b4.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y))/b04.a.y
#>   b4.t = 2.68055384383517*second
#> root 4:
#>   b1.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#>   b1.t = 0.380670645960751*second
#>   b3.t = (-b0.vel.y + b3.vel.y)/b03.a.y
#>   b3.t = 1.53061224489796*second
#>   b4.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y))/b04.a.y
#>   b4.t = 0.380670645960751*second

in_order = (b1.t < b2.t) & (b2.t < b3.t) & (b3.t < b4.t) & (b4.t < b5.t)
#> (b1.t < b2.t) & (b2.t < b3.t) & (b3.t < b4.t) & (b4.t < b5.t)

sol = ball.solve(
    b1.t, b1.vel.y,
    b2.pos.y, b2.vel.y,
    b3.t, b3.pos.y,
    b4.t, b4.vel.y,
    b5.pos.y, b5.vel.y,
).where(in_order)
#> b1.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#> b1.t = 0.380670645960751*second
#> b1.vel.y = sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)
#> b1.vel.y = 11.2694276695846*meter/second
#> b2.pos.y = b2.t*(2*b0.vel.y + b02.a.y*b2.t)/2
#> b2.pos.y = 10.1*meter
#> b2.vel.y = b0.vel.y + b02.a.y*b2.t
#> b2.vel.y = 5.2*meter/second
#> b3.t = (-b0.vel.y + b3.vel.y)/b03.a.y
#> b3.t = 1.53061224489796*second
#> b3.pos.y = (-b0.vel.y**2 + b3.vel.y**2)/(2*b03.a.y)
#> b3.pos.y = 11.4795918367347*meter
#> b4.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y))/b04.a.y
#> b4.t = 2.68055384383517*second
#> b4.vel.y = -sqrt(b0.vel.y**2 + 2*b04.a.y*b4.pos.y)
#> b4.vel.y = -11.2694276695846*meter/second
#> b5.pos.y = b5.t*(2*b0.vel.y + b05.a.y*b5.t)/2
#> b5.pos.y = -18.4*meter
#> b5.vel.y = b0.vel.y + b05.a.y*b5.t
#> b5.vel.y = -24.2*meter/second

# (d) The acceleration is constant, so at the top it is still -9.80 m/s².
# It's a known, b03.a.y, not a want, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, b2.pos.y,  "10.1", unit=meter),           # (a) at 1.00 s
    Answer(sol, b2.vel.y,   "5.2", unit=meter / second),
    Answer(sol, b5.pos.y, "-18.4", unit=meter),           # (a) at 4.00 s
    Answer(sol, b5.vel.y, "-24.2", unit=meter / second),
    Answer(sol, b1.vel.y,  "11.3", unit=meter / second),  # (b) going up
    Answer(sol, b4.vel.y, "-11.3", unit=meter / second),  # (b) coming down
    Answer(sol, b3.pos.y,  "11.5", unit=meter),           # (c) the top
]
#> [✓ b2.pos.y: book 10.1 meter, found 10.1*meter,
#>  ✓ b2.vel.y: book 5.2 meter/second, found 5.2*meter/second,
#>  ✓ b5.pos.y: book -18.4 meter, found -18.4*meter,
#>  ✓ b5.vel.y: book -24.2 meter/second, found -24.2*meter/second,
#>  ✓ b1.vel.y: book 11.3 meter/second, found 11.2694276695846*meter/second,
#>  ✓ b4.vel.y: book -11.3 meter/second, found -11.2694276695846*meter/second,
#>  ✓ b3.pos.y: book 11.5 meter, found 11.4795918367347*meter]
