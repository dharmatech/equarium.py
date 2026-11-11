"""University Physics, 15th edition, Example 2.4, with the physics code.

A motorcyclist accelerates at a constant 4.0 m/s²
from 5.0 m east of a signpost,
moving east at 15 m/s at t = 0.

(a) Where is he, and how fast is he going, at t = 2.0 s?

(b) Where is he when his speed is 25 m/s?


    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n04/main_incremental_watch.py

"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.display import render, render_solution
from equarium.physics import BookNotation, Particle, X
from examples.answers import Answer

m = Particle("m", 2, X)
#> particle m (x): m0, m1

m0, m1 = m.states
#> (m0, m1)

m01 = m.edge(0, 1)
#> m01: m0 → m1

motorcycle = System()
#> knowns: none
#> wants: none
#> connected: none
#> ready: none

motorcycle = motorcycle.add(*m.kinematics())
#> * (1)  m01.dt = -m0.t + m1.t
#> * (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#> * (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

motorcycle = motorcycle.add(*m01.constant_acceleration())
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#> * (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

motorcycle = motorcycle.known(m0.t, 0 * second)
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0
#>   wants: none
#>   connected: none
#>   ready: none

# from 5.0 m east of a signpost
motorcycle = motorcycle.known(m0.pos.x, 5 * meter)
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0, m0.pos.x = 5*meter
#>   wants: none
#>   connected: none
#>   ready: none

# moving east at 15 m/s
motorcycle = motorcycle.known(m0.vel.x, 15 * meter / second)
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second
#>   wants: none
#>   connected: none
#>   ready: none

# accelerates at a constant 4.0 m/s²
motorcycle = motorcycle.known(m01.a.x, 4 * meter / second**2)
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second, m01.a.x = 4*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: none

motorcycle = motorcycle.eliminate_zeros()
#> * (1)  m01.dt = m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second, m01.a.x = 4*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: none

# (a) Where is he, and how fast is he going, at t = 2.0 s?

part_a = motorcycle.known(m1.t, 2 * second)
#>   (1)  m01.dt = m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second, m01.a.x = 4*meter/second**2, m1.t = 2*second
#>   wants: none
#>   connected: none
#> * ready: (1)

part_a1 = part_a.want(m1.pos.x)
#>   (1)  m01.dt = m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second, m01.a.x = 4*meter/second**2, m1.t = 2*second
#> * wants: m1.pos.x
#> * connected: m01.dt, m01.v_av.x, m1.pos.x, m1.vel.x (4 unknowns in 4 equations)
#>   ready: (1)

sol_a1 = part_a1.solve()
#> m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2
#> m1.pos.x = 43.0*meter

# how fast is he going
part_a2 = part_a.want(m1.vel.x)
#>   (1)  m01.dt = m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   knowns: m0.t = 0, m0.pos.x = 5*meter, m0.vel.x = 15*meter/second, m01.a.x = 4*meter/second**2, m1.t = 2*second
#> * wants: m1.vel.x
#> * connected: m01.dt, m01.v_av.x, m1.pos.x, m1.vel.x (4 unknowns in 4 equations)
#>   ready: (1)

sol_a2 = part_a2.solve()
#> m1.vel.x = m0.vel.x + m01.a.x*m1.t
#> m1.vel.x = 23.0*meter/second

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a1, m1.pos.x, "43", unit=meter),
    Answer(sol_a2, m1.vel.x, "23", unit=meter / second),
]
#> [✓ m1.pos.x: book 43 meter, found 43.0*meter,
#>  ✓ m1.vel.x: book 23 meter/second, found 23.0*meter/second]
