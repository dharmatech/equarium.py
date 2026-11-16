"""University Physics, 15th edition, Example 2.7, with the physics code,
with a state for each moment the book asks about.

A ball is thrown straight up at 15.0 m/s from level with a roof railing,
then falls freely (the book's Fig. 2.24; upward positive, origin at the
railing).

(a) Where is it, and how fast is it moving, 1.00 s and 4.00 s later?

(b) What is its velocity when it is 5.00 m above the railing?

(c) How high does it go?

(d) What is its acceleration at the top?

Each moment is a state of the ball, joined straight to the throw, b0,
by an edge of its own: one constant acceleration covers the whole
flight, so no state needs the one before it. The states are numbered as
the parts bring them up, not in time order: b1 at 1.00 s, b2 at 4.00 s,
b3 at 5.00 m above the railing, b4 at the top. b3 has two roots, the
two moments the ball is there, going up and coming down; with their
times, the states can be put in time order afterwards.

`b.edge(0, 2)` is refused, since a particle's edges join consecutive
states, so the edges are built with `Edge(b0, b2)`, and
`edge_kinematics` writes the 2.2 and 2.4 that `b.kinematics()` writes
for consecutive edges.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n07/main_inc_watch_star.py
"""

import sympy as sp
from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Edge, Particle, Y
from examples.answers import Answer


def edge_kinematics(e: Edge[Y]) -> list[sp.Eq]:
    """2.2 and 2.4 for one edge, between any two states."""
    return [
        sp.Eq(e.dt, e.end.t - e.start.t),
        sp.Eq(e.v_av.y, (e.end.pos.y - e.start.pos.y) / e.dt),
        sp.Eq(e.a.y, (e.end.vel.y - e.start.vel.y) / e.dt),
    ]


def leg(e: Edge[Y]) -> list[sp.Eq]:
    """An edge with free fall over it: 2.2, 2.4 and 2.10."""
    return [*edge_kinematics(e), *e.constant_acceleration()]


b = Particle("b", 5, Y)  # the ball
#> particle b (y): b0, b1, b2, b3, b4

b0, b1, b2, b3, b4 = b.states;

g = -9.8 * meter / second**2;

# Thrown at t = 0, from the railing, at 15.0 m/s.
ball = System().known({
    b0.t:     0 * second,
    b0.pos.y: 0 * meter,
    b0.vel.y: 15.0 * meter / second
});

# (a) Position and velocity at 1.00 s and 4.00 s: b1 and b2.
b01 = Edge(b0, b1)
#> b01: b0 → b1

b02 = Edge(b0, b2)
#> b02: b0 → b2

ball = ball.add(*leg(b01), *leg(b02)).known({b01.a.y: g, b02.a.y: g}).eliminate_zeros()
#> (1)  b01.dt     = b1.t
#> (2)  b01.v_av.y = b1.pos.y/b01.dt
#> (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#> (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#> (5)  b02.dt     = b2.t
#> (6)  b02.v_av.y = b2.pos.y/b02.dt
#> (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#> (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#> knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>         b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2
#> wants: none
#> connected: none
#> ready: none

ball = ball.known({b1.t: 1.0 * second, b2.t: 4.0 * second})
#>   (1)  b01.dt     = b1.t
#>   (2)  b01.v_av.y = b1.pos.y/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>   (5)  b02.dt     = b2.t
#>   (6)  b02.v_av.y = b2.pos.y/b02.dt
#>   (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>   (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#> *         b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#> *         b1.t = 1.0*second, b2.t = 4.0*second
#>   wants: none
#>   connected: none
#> * ready: (1), (5)

sol_a1 = ball.solve(b1.pos.y, b1.vel.y)
#> b1.pos.y = b1.t*(2*b0.vel.y + b01.a.y*b1.t)/2
#> b1.pos.y = 10.1*meter
#> b1.vel.y = b0.vel.y + b01.a.y*b1.t
#> b1.vel.y = 5.2*meter/second

sol_a4 = ball.solve(b2.pos.y, b2.vel.y)
#> b2.pos.y = b2.t*(2*b0.vel.y + b02.a.y*b2.t)/2
#> b2.pos.y = -18.4*meter
#> b2.vel.y = b0.vel.y + b02.a.y*b2.t
#> b2.vel.y = -24.2*meter/second

# (b) 5.00 m above the railing: one state, b3, and the solver finds the
# two moments it's there.
b03 = Edge(b0, b3)
#> b03: b0 → b3

ball = ball.add(*leg(b03)).known(b03.a.y, g).eliminate_zeros()
#>    (1)  b01.dt     = b1.t
#>    (2)  b01.v_av.y = b1.pos.y/b01.dt
#>    (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>    (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>    (5)  b02.dt     = b2.t
#>    (6)  b02.v_av.y = b2.pos.y/b02.dt
#>    (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>    (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#> *  (9)  b03.dt     = b3.t
#> * (10)  b03.v_av.y = b3.pos.y/b03.dt
#> * (11)  b03.a.y    = (-b0.vel.y + b3.vel.y)/b03.dt
#> * (12)  b03.v_av.y = b0.vel.y/2 + b3.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>           b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#> *         b1.t = 1.0*second, b2.t = 4.0*second,
#> *         b03.a.y = -9.8*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: (1), (5)

ball = ball.known(b3.pos.y, 5.0 * meter)
#>    (1)  b01.dt     = b1.t
#>    (2)  b01.v_av.y = b1.pos.y/b01.dt
#>    (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>    (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>    (5)  b02.dt     = b2.t
#>    (6)  b02.v_av.y = b2.pos.y/b02.dt
#>    (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>    (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#>    (9)  b03.dt     = b3.t
#>   (10)  b03.v_av.y = b3.pos.y/b03.dt
#>   (11)  b03.a.y    = (-b0.vel.y + b3.vel.y)/b03.dt
#>   (12)  b03.v_av.y = b0.vel.y/2 + b3.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>           b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#>           b1.t = 1.0*second, b2.t = 4.0*second,
#> *         b03.a.y = -9.8*meter/second**2, b3.pos.y = 5.0*meter
#>   wants: none
#>   connected: none
#>   ready: (1), (5)

sol_b = ball.solve(b3.t, b3.vel.y)
#> root 1:
#>   b3.t = (-b0.vel.y - sqrt(b0.vel.y**2 + 2*b03.a.y*b3.pos.y))/b03.a.y
#>   b3.t = 2.68055384383517*second
#>   b3.vel.y = -sqrt(b0.vel.y**2 + 2*b03.a.y*b3.pos.y)
#>   b3.vel.y = -11.2694276695846*meter/second
#> root 2:
#>   b3.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b03.a.y*b3.pos.y))/b03.a.y
#>   b3.t = 0.380670645960751*second
#>   b3.vel.y = sqrt(b0.vel.y**2 + 2*b03.a.y*b3.pos.y)
#>   b3.vel.y = 11.2694276695846*meter/second

# (c) The top, b4, where the velocity is zero.
b04 = Edge(b0, b4)
#> b04: b0 → b4

ball = ball.add(*leg(b04)).known(b04.a.y, g).eliminate_zeros()
#>    (1)  b01.dt     = b1.t
#>    (2)  b01.v_av.y = b1.pos.y/b01.dt
#>    (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>    (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>    (5)  b02.dt     = b2.t
#>    (6)  b02.v_av.y = b2.pos.y/b02.dt
#>    (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>    (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#>    (9)  b03.dt     = b3.t
#>   (10)  b03.v_av.y = b3.pos.y/b03.dt
#>   (11)  b03.a.y    = (-b0.vel.y + b3.vel.y)/b03.dt
#>   (12)  b03.v_av.y = b0.vel.y/2 + b3.vel.y/2
#> * (13)  b04.dt     = b4.t
#> * (14)  b04.v_av.y = b4.pos.y/b04.dt
#> * (15)  b04.a.y    = (-b0.vel.y + b4.vel.y)/b04.dt
#> * (16)  b04.v_av.y = b0.vel.y/2 + b4.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>           b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#>           b1.t = 1.0*second, b2.t = 4.0*second,
#> *         b03.a.y = -9.8*meter/second**2, b3.pos.y = 5.0*meter,
#> *         b04.a.y = -9.8*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: (1), (5)

ball = ball.known(b4.vel.y, 0 * meter / second)
#>    (1)  b01.dt     = b1.t
#>    (2)  b01.v_av.y = b1.pos.y/b01.dt
#>    (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>    (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>    (5)  b02.dt     = b2.t
#>    (6)  b02.v_av.y = b2.pos.y/b02.dt
#>    (7)  b02.a.y    = (-b0.vel.y + b2.vel.y)/b02.dt
#>    (8)  b02.v_av.y = b0.vel.y/2 + b2.vel.y/2
#>    (9)  b03.dt     = b3.t
#>   (10)  b03.v_av.y = b3.pos.y/b03.dt
#>   (11)  b03.a.y    = (-b0.vel.y + b3.vel.y)/b03.dt
#>   (12)  b03.v_av.y = b0.vel.y/2 + b3.vel.y/2
#>   (13)  b04.dt     = b4.t
#>   (14)  b04.v_av.y = b4.pos.y/b04.dt
#>   (15)  b04.a.y    = (-b0.vel.y + b4.vel.y)/b04.dt
#>   (16)  b04.v_av.y = b0.vel.y/2 + b4.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#>           b01.a.y = -9.8*meter/second**2, b02.a.y = -9.8*meter/second**2,
#>           b1.t = 1.0*second, b2.t = 4.0*second,
#>           b03.a.y = -9.8*meter/second**2, b3.pos.y = 5.0*meter,
#> *         b04.a.y = -9.8*meter/second**2, b4.vel.y = 0
#>   wants: none
#>   connected: none
#> * ready: (1), (5), (15), (16)

sol_c = ball.solve(b4.t, b4.pos.y)
#> b4.t = (-b0.vel.y + b4.vel.y)/b04.a.y
#> b4.t = 1.53061224489796*second
#> b4.pos.y = (-b0.vel.y**2 + b4.vel.y**2)/(2*b04.a.y)
#> b4.pos.y = 11.4795918367347*meter

# (d) The acceleration is constant, so at the top it is still -9.80 m/s².
# It's a known, b04.a.y, not a want, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a1, b1.pos.y,  "10.1",         unit=meter),
    Answer(sol_a1, b1.vel.y,   "5.2",         unit=meter / second),
    Answer(sol_a4, b2.pos.y, "-18.4",         unit=meter),
    Answer(sol_a4, b2.vel.y, "-24.2",         unit=meter / second),
    Answer(sol_b,  b3.vel.y, "-11.3", "11.3", unit=meter / second),
    Answer(sol_c,  b4.pos.y,  "11.5",         unit=meter),
]
#> [✓ b1.pos.y: book 10.1 meter, found 10.1*meter,
#>  ✓ b1.vel.y: book 5.2 meter/second, found 5.2*meter/second,
#>  ✓ b2.pos.y: book -18.4 meter, found -18.4*meter,
#>  ✓ b2.vel.y: book -24.2 meter/second, found -24.2*meter/second,
#>  ✓ b3.vel.y: book -11.3, 11.3 meter/second, found -11.2694276695846*meter/second, 11.2694276695846*meter/second,
#>  ✓ b4.pos.y: book 11.5 meter, found 11.4795918367347*meter]
