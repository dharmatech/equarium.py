"""University Physics, 15th edition, Example 2.7, with the physics code,
with the states in time order, each joined to the one before it, solved
one segment at a time.

A ball is thrown straight up at 15.0 m/s from level with a roof railing,
then falls freely (the book's Fig. 2.24; upward positive, origin at the
railing).

(a) Where is it, and how fast is it moving, 1.00 s and 4.00 s later?

(b) What is its velocity when it is 5.00 m above the railing?

(c) How high does it go?

(d) What is its acceleration at the top?

b0 is the throw, b1 is 5.00 m up going up, b2 is at 1.00 s, b3 is the
top, b4 is 5.00 m up coming down, and b5 is at 4.00 s. Each segment
starts where the last one ended: its start state's numbers are knowns,
carried over from the solve before. Two solves have two roots, and
`where` keeps the one in time order: b1 going up, b4 after the top.
Solving the whole chain at once didn't finish in five minutes, since its
two quadratics are coupled through the chain.

Each segment's 2.2 and 2.4 come from `edge_kinematics`, since
`b.kinematics()` writes every edge's at once. The system steps end in
`;`, so only the solves print.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n07/main_inc_watch_chrono_segments.py
"""

import sympy as sp
from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Edge, Particle, Y
from examples.answers import Answer


def edge_kinematics(e: Edge[Y]) -> list[sp.Eq]:
    """2.2 and 2.4 for one edge."""
    return [
        sp.Eq(e.dt, e.end.t - e.start.t),
        sp.Eq(e.v_av.y, (e.end.pos.y - e.start.pos.y) / e.dt),
        sp.Eq(e.a.y, (e.end.vel.y - e.start.vel.y) / e.dt),
    ]


def leg(e: Edge[Y]) -> list[sp.Eq]:
    """An edge with free fall over it: 2.2, 2.4 and 2.10."""
    return [*edge_kinematics(e), *e.constant_acceleration()]


b = Particle("b", 6, Y)  # the ball
#> particle b (y): b0, b1, b2, b3, b4, b5

b0, b1, b2, b3, b4, b5 = b.states;

g = -9.8 * meter / second**2;

# Thrown at t = 0, from the railing, at 15.0 m/s.
ball = System().known({
    b0.t:     0 * second,
    b0.pos.y: 0 * meter,
    b0.vel.y: 15.0 * meter / second
});

# b1: 5.00 m up, going up.
b01 = b.edge(0, 1)
#> b01: b0 → b1

ball = ball.add(*leg(b01)).eliminate_zeros().known({b01.a.y: g, b1.pos.y: 5.0 * meter});

sol_1 = ball.solve(b1.t, b1.vel.y).where(b1.vel.y > 0)
#> b1.t = (-b0.vel.y + sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y))/b01.a.y
#> b1.t = 0.380670645960751*second
#> b1.vel.y = sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)
#> b1.vel.y = 11.2694276695846*meter/second

ball = ball.known({b1.t: sol_1.number(b1.t), b1.vel.y: sol_1.number(b1.vel.y)});

# b2: at 1.00 s.
b12 = b.edge(1, 2)
#> b12: b1 → b2

ball = ball.add(*leg(b12)).known({b12.a.y: g, b2.t: 1.0 * second});

sol_2 = ball.solve(b2.pos.y, b2.vel.y)
#> b2.pos.y = b1.pos.y + b1.t**2*b12.a.y/2 - b1.t*b1.vel.y - b1.t*b12.a.y*b2.t + b1.vel.y*b2.t + b12.a.y*b2.t**2/2
#> b2.pos.y = 10.1*meter
#> b2.vel.y = -b1.t*b12.a.y + b1.vel.y + b12.a.y*b2.t
#> b2.vel.y = 5.2*meter/second

ball = ball.known({b2.pos.y: sol_2.number(b2.pos.y), b2.vel.y: sol_2.number(b2.vel.y)});

# b3: the top, where the velocity is zero.
b23 = b.edge(2, 3)
#> b23: b2 → b3

ball = ball.add(*leg(b23)).known({b23.a.y: g, b3.vel.y: 0 * meter / second});

sol_3 = ball.solve(b3.t, b3.pos.y)
#> b3.t = (b2.t*b23.a.y - b2.vel.y + b3.vel.y)/b23.a.y
#> b3.t = 1.53061224489796*second
#> b3.pos.y = (2*b2.pos.y*b23.a.y - b2.vel.y**2 + b3.vel.y**2)/(2*b23.a.y)
#> b3.pos.y = 11.4795918367347*meter

ball = ball.known({b3.t: sol_3.number(b3.t), b3.pos.y: sol_3.number(b3.pos.y)});

# b4: 5.00 m up, coming down, so after the top.
b34 = b.edge(3, 4)
#> b34: b3 → b4

ball = ball.add(*leg(b34)).known({b34.a.y: g, b4.pos.y: 5.0 * meter});

sol_4 = ball.solve(b4.t, b4.vel.y).where(b4.t > b3.t)
#> b4.t = (b3.t*b34.a.y - b3.vel.y - sqrt(-2*b3.pos.y*b34.a.y + b3.vel.y**2 + 2*b34.a.y*b4.pos.y))/b34.a.y
#> b4.t = 2.68055384383517*second
#> b4.vel.y = -sqrt(-2*b3.pos.y*b34.a.y + b3.vel.y**2 + 2*b34.a.y*b4.pos.y)
#> b4.vel.y = -11.2694276695846*meter/second

ball = ball.known({b4.t: sol_4.number(b4.t), b4.vel.y: sol_4.number(b4.vel.y)});

# b5: at 4.00 s.
b45 = b.edge(4, 5)
#> b45: b4 → b5

ball = ball.add(*leg(b45)).known({b45.a.y: g, b5.t: 4.0 * second});

sol_5 = ball.solve(b5.pos.y, b5.vel.y)
#> b5.pos.y = b4.pos.y + b4.t**2*b45.a.y/2 - b4.t*b4.vel.y - b4.t*b45.a.y*b5.t + b4.vel.y*b5.t + b45.a.y*b5.t**2/2
#> b5.pos.y = -18.4*meter
#> b5.vel.y = -b4.t*b45.a.y + b4.vel.y + b45.a.y*b5.t
#> b5.vel.y = -24.2*meter/second

# (d) The acceleration is constant, so at the top it is still -9.80 m/s².
# It's a known, b23.a.y, not a want, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_2, b2.pos.y,  "10.1", unit=meter),           # (a) at 1.00 s
    Answer(sol_2, b2.vel.y,   "5.2", unit=meter / second),
    Answer(sol_5, b5.pos.y, "-18.4", unit=meter),           # (a) at 4.00 s
    Answer(sol_5, b5.vel.y, "-24.2", unit=meter / second),
    Answer(sol_1, b1.vel.y,  "11.3", unit=meter / second),  # (b) going up
    Answer(sol_4, b4.vel.y, "-11.3", unit=meter / second),  # (b) coming down
    Answer(sol_3, b3.pos.y,  "11.5", unit=meter),           # (c) the top
]
#> [✓ b2.pos.y: book 10.1 meter, found 10.1*meter,
#>  ✓ b2.vel.y: book 5.2 meter/second, found 5.2*meter/second,
#>  ✓ b5.pos.y: book -18.4 meter, found -18.4*meter,
#>  ✓ b5.vel.y: book -24.2 meter/second, found -24.2*meter/second,
#>  ✓ b1.vel.y: book 11.3 meter/second, found 11.2694276695846*meter/second,
#>  ✓ b4.vel.y: book -11.3 meter/second, found -11.2694276695846*meter/second,
#>  ✓ b3.pos.y: book 11.5 meter, found 11.4795918367347*meter]
