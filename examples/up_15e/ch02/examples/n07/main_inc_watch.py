"""University Physics, 15th edition, Example 2.7, with the physics code.

A ball is thrown straight up at 15.0 m/s from level with a roof railing,
then falls freely (the book's Fig. 2.24; upward positive, origin at the
railing).

(a) Where is it, and how fast is it moving, 1.00 s and 4.00 s later?

(b) What is its velocity when it is 5.00 m above the railing?

(c) How high does it go?

(d) What is its acceleration at the top?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.7/up-example-2.7-v1-000.py`, without its
last part, Example 2.8, which is `n08/main.py`. Its two zero
equations, in its `eq_flat`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`, before any
values. (c)'s zero velocity is a value, set after that step, so
`b1.vel.y` stays a symbol in the formula, as in the old script.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n07/main_inc_watch.py
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Particle, Y
from examples.answers import Answer

b = Particle("b", 2, Y)  # the ball
#> particle b (y): b0, b1

b0, b1 = b.states
#> (b0, b1)

b01 = b.edge(0, 1)
#> b01: b0 → b1

ball = System()
#> knowns: none
#> wants: none
#> connected: none
#> ready: none

ball = ball.add(*b.kinematics())
#> * (1)  b01.dt     = -b0.t + b1.t
#> * (2)  b01.v_av.y = (-b0.pos.y + b1.pos.y)/b01.dt
#> * (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

# Free fall: a constant g.
ball = ball.add(*b01.constant_acceleration())
#>   (1)  b01.dt     = -b0.t + b1.t
#>   (2)  b01.v_av.y = (-b0.pos.y + b1.pos.y)/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#> * (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

# Thrown at t = 0, from the railing.
ball = ball.known({
    b0.t:     0 * second,
    b0.pos.y: 0 * meter
})
#>   (1)  b01.dt     = -b0.t + b1.t
#>   (2)  b01.v_av.y = (-b0.pos.y + b1.pos.y)/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#> * knowns: b0.t = 0, b0.pos.y = 0
#>   wants: none
#>   connected: none
#>   ready: none

ball = ball.eliminate_zeros()
#> * (1)  b01.dt     = b1.t
#> * (2)  b01.v_av.y = b1.pos.y/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#>   knowns: b0.t = 0, b0.pos.y = 0
#>   wants: none
#>   connected: none
#>   ready: none

ball = ball.known(b0.vel.y, 15.0 * meter / second)
#>   (1)  b01.dt     = b1.t
#>   (2)  b01.v_av.y = b1.pos.y/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#> * knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second
#>   wants: none
#>   connected: none
#>   ready: none

ball = ball.known(b01.a.y, -9.8 * meter / second**2)
#>   (1)  b01.dt     = b1.t
#>   (2)  b01.v_av.y = b1.pos.y/b01.dt
#>   (3)  b01.a.y    = (-b0.vel.y + b1.vel.y)/b01.dt
#>   (4)  b01.v_av.y = b0.vel.y/2 + b1.vel.y/2
#> * knowns: b0.t = 0, b0.pos.y = 0, b0.vel.y = 15.0*meter/second,
#> *         b01.a.y = -9.8*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: none

# (a) Position and velocity at 1.00 s and 4.00 s.
sol_a1 = ball.known(b1.t, 1.0 * second).solve(b1.pos.y, b1.vel.y)
#> b1.pos.y = b1.t*(2*b0.vel.y + b01.a.y*b1.t)/2
#> b1.pos.y = 10.1*meter
#> b1.vel.y = b0.vel.y + b01.a.y*b1.t
#> b1.vel.y = 5.2*meter/second

sol_a4 = ball.known(b1.t, 4.0 * second).solve(b1.pos.y, b1.vel.y)
#> b1.pos.y = b1.t*(2*b0.vel.y + b01.a.y*b1.t)/2
#> b1.pos.y = -18.4*meter
#> b1.vel.y = b0.vel.y + b01.a.y*b1.t
#> b1.vel.y = -24.2*meter/second

# (b) The velocity 5.00 m above the railing: two roots.
sol_b = ball.known(b1.pos.y, 5.0 * meter).solve(b1.vel.y)
#> root 1:
#>   b1.vel.y = -sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)
#>   b1.vel.y = -11.2694276695846*meter/second
#> root 2:
#>   b1.vel.y = sqrt(b0.vel.y**2 + 2*b01.a.y*b1.pos.y)
#>   b1.vel.y = 11.2694276695846*meter/second

# (c) The maximum height, where the velocity is zero.
sol_c = ball.known(b1.vel.y, 0 * meter / second).solve(b1.pos.y)
#> b1.pos.y = (-b0.vel.y**2 + b1.vel.y**2)/(2*b01.a.y)
#> b1.pos.y = 11.4795918367347*meter

# (d) The acceleration is constant, so at the top it is still -9.80 m/s².
# It's a known, not a want, so it has no Answer.

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a1, b1.pos.y,  "10.1",         unit=meter),
    Answer(sol_a1, b1.vel.y,   "5.2",         unit=meter / second),
    Answer(sol_a4, b1.pos.y, "-18.4",         unit=meter),
    Answer(sol_a4, b1.vel.y, "-24.2",         unit=meter / second),
    Answer(sol_b,  b1.vel.y, "-11.3", "11.3", unit=meter / second),
    Answer(sol_c,  b1.pos.y,  "11.5",         unit=meter),
]
#> [✓ b1.pos.y: book 10.1 meter, found 10.1*meter,
#>  ✓ b1.vel.y: book 5.2 meter/second, found 5.2*meter/second,
#>  ✓ b1.pos.y: book -18.4 meter, found -18.4*meter,
#>  ✓ b1.vel.y: book -24.2 meter/second, found -24.2*meter/second,
#>  ✓ b1.vel.y: book -11.3, 11.3 meter/second, found -11.2694276695846*meter/second, 11.2694276695846*meter/second,
#>  ✓ b1.pos.y: book 11.5 meter, found 11.4795918367347*meter]
