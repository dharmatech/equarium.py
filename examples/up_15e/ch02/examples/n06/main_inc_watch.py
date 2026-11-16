"""University Physics, 15th edition, Example 2.6, with the physics code.

A coin is dropped from rest from a tower and falls freely, ignoring air
resistance (the book's Fig. 2.23). What are its position and velocity
after 1.0 s, 2.0 s and 3.0 s? Upward is positive, so a = -9.8 m/s².

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.6/up-example-2.6-v2-000.ks.py`. Its three
zero equations, in its `eq_flat`, are zero knowns here, followed by
`eliminate_zeros()` where it called its `eliminate_zero_eqs`, before any
values. The old script solves only for the position at 2.0 s and 3.0 s;
the velocity is added as a want there, for the book's -20 m/s and
-29 m/s.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n06/main_inc_watch.py
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.physics import Particle, Y
from examples.answers import Answer

c = Particle("c", 2, Y)  # the coin
#> particle c (y): c0, c1

c0, c1 = c.states
#> (c0, c1)

c01 = c.edge(0, 1)
#> c01: c0 → c1

coin = System()
#> knowns: none
#> wants: none
#> connected: none
#> ready: none

coin = coin.add(*c.kinematics())
#> * (1)  c01.dt     = -c0.t + c1.t
#> * (2)  c01.v_av.y = (-c0.pos.y + c1.pos.y)/c01.dt
#> * (3)  c01.a.y    = (-c0.vel.y + c1.vel.y)/c01.dt
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

# Free fall: a constant g.
coin = coin.add(*c01.constant_acceleration())
#>   (1)  c01.dt     = -c0.t + c1.t
#>   (2)  c01.v_av.y = (-c0.pos.y + c1.pos.y)/c01.dt
#>   (3)  c01.a.y    = (-c0.vel.y + c1.vel.y)/c01.dt
#> * (4)  c01.v_av.y = c0.vel.y/2 + c1.vel.y/2
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

# Dropped from rest, at the origin.
coin = coin.known({
    c0.t:     0 * second,
    c0.pos.y: 0 * meter,
    c0.vel.y: 0 * meter / second
})
#>   (1)  c01.dt     = -c0.t + c1.t
#>   (2)  c01.v_av.y = (-c0.pos.y + c1.pos.y)/c01.dt
#>   (3)  c01.a.y    = (-c0.vel.y + c1.vel.y)/c01.dt
#>   (4)  c01.v_av.y = c0.vel.y/2 + c1.vel.y/2
#> * knowns: c0.t = 0, c0.pos.y = 0, c0.vel.y = 0
#>   wants: none
#>   connected: none
#>   ready: none

coin = coin.eliminate_zeros()
#> * (1)  c01.dt     = c1.t
#> * (2)  c01.v_av.y = c1.pos.y/c01.dt
#> * (3)  c01.a.y    = c1.vel.y/c01.dt
#> * (4)  c01.v_av.y = c1.vel.y/2
#>   knowns: c0.t = 0, c0.pos.y = 0, c0.vel.y = 0
#>   wants: none
#>   connected: none
#>   ready: none

coin = coin.known(c01.a.y, -9.8 * meter / second**2)
#>   (1)  c01.dt     = c1.t
#>   (2)  c01.v_av.y = c1.pos.y/c01.dt
#>   (3)  c01.a.y    = c1.vel.y/c01.dt
#>   (4)  c01.v_av.y = c1.vel.y/2
#> * knowns: c0.t = 0, c0.pos.y = 0, c0.vel.y = 0,
#> *         c01.a.y = -9.8*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: none

sol_1 = coin.known(c1.t, 1.0 * second).solve(c1.pos.y, c1.vel.y)
#> c1.pos.y = c01.a.y*c1.t**2/2
#> c1.pos.y = -4.9*meter
#> c1.vel.y = c01.a.y*c1.t
#> c1.vel.y = -9.8*meter/second

sol_2 = coin.known(c1.t, 2.0 * second).solve(c1.pos.y, c1.vel.y)
#> c1.pos.y = c01.a.y*c1.t**2/2
#> c1.pos.y = -19.6*meter
#> c1.vel.y = c01.a.y*c1.t
#> c1.vel.y = -19.6*meter/second

sol_3 = coin.known(c1.t, 3.0 * second).solve(c1.pos.y, c1.vel.y)
#> c1.pos.y = c01.a.y*c1.t**2/2
#> c1.pos.y = -44.1*meter
#> c1.vel.y = c01.a.y*c1.t
#> c1.vel.y = -29.4*meter/second

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_1, c1.pos.y,  "-4.9", unit=meter),
    Answer(sol_1, c1.vel.y,  "-9.8", unit=meter / second),
    Answer(sol_2, c1.pos.y, "-20",   unit=meter),
    Answer(sol_2, c1.vel.y, "-20",   unit=meter / second),
    Answer(sol_3, c1.pos.y, "-44",   unit=meter),
    Answer(sol_3, c1.vel.y, "-29",   unit=meter / second),
]
#> [✓ c1.pos.y: book -4.9 meter, found -4.9*meter,
#>  ✓ c1.vel.y: book -9.8 meter/second, found -9.8*meter/second,
#>  ✓ c1.pos.y: book -20 meter, found -19.6*meter,
#>  ✓ c1.vel.y: book -20 meter/second, found -19.6*meter/second,
#>  ✓ c1.pos.y: book -44 meter, found -44.1*meter,
#>  ✓ c1.vel.y: book -29 meter/second, found -29.4*meter/second]

