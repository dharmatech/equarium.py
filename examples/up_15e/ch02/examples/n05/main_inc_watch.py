"""University Physics, 15th edition, Example 2.5, with the physics code,
solved all at once.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².

(a) When does the officer catch up?

At that time,

(b) how fast is the officer going

(c) how far has each traveled?

The meeting is an event, `Event("meet", m1, p1)`, whose four links are (11)
to (14): each state's time, then its position, equal to the event's.
The old script wrote them itself, through `t_01` and `dist`, positions
first. Its five zero equations, which `sp.solve` took with the rest,
are zero knowns here, followed by `eliminate_zeros()` before the solve.
Its three solves are one here, with three wants.

    uv run python -m equarium.transcript --watch examples/up_15e/ch02/examples/n05/main_inc_watch.py 
"""

import sympy as sp
from sympy.physics.units import meter, second

from equarium import System
from equarium.display import render, render_solution
from equarium.physics import BookNotation, Event, Particle, X
from examples.answers import Answer

m = Particle("m", 2, X)  # the motorist
#> particle m (x): m0, m1

p = Particle("p", 2, X)  # the police officer
#> particle p (x): p0, p1

m0, m1 = m.states
#> (m0, m1)

p0, p1 = p.states
#> (p0, p1)

m01 = m.edge(0, 1)
#> m01: m0 → m1

p01 = p.edge(0, 1)
#> p01: p0 → p1

meet = Event("meet", m1, p1)  # the same time and place
#> event meet: m1, p1

m_v = sp.Symbol("m_v")
#> m_v

setup = System()
#> knowns: none
#> wants: none
#> connected: none
#> ready: none

setup = setup.add(*m.kinematics())
#> * (1)  m01.dt     = -m0.t + m1.t
#> * (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#> * (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.add(*m01.constant_acceleration())
#>   (1)  m01.dt     = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#> * (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.add(*p.kinematics())
#>   (1)  m01.dt     = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * (5)  p01.dt     = -p0.t + p1.t
#> * (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#> * (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.add(*p01.constant_acceleration())
#>   (1)  m01.dt     = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   (5)  p01.dt     = -p0.t + p1.t
#>   (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>   (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#> * (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.add(sp.Eq(m0.vel.x, m_v))
#>   (1)  m01.dt     = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>   (5)  p01.dt     = -p0.t + p1.t
#>   (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>   (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>   (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#> * (9)  m0.vel.x   = m_v
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.add(sp.Eq(m1.vel.x, m_v))
#>    (1)  m01.dt     = -m0.t + m1.t
#>    (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = -p0.t + p1.t
#>    (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>    (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>    (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#> * (10)  m1.vel.x   = m_v
#>   knowns: none
#>   wants: none
#>   connected: none
#>   ready: none

setup = setup.known(m_v, 15 * meter / second)
#>    (1)  m01.dt     = -m0.t + m1.t
#>    (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = -p0.t + p1.t
#>    (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>    (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>    (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#> * knowns: m_v = 15*meter/second
#>   wants: none
#>   connected: none
#> * ready: (9), (10)

setup = setup.known({
    m0.pos.x: 0 * meter, m0.t: 0 * second,
    p0.pos.x: 0 * meter, p0.t: 0 * second, p0.vel.x: 0 * meter / second,
    p01.a.x: 3 * meter / second**2
})
#>    (1)  m01.dt     = -m0.t + m1.t
#>    (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = -p0.t + p1.t
#>    (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>    (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>    (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#> * knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#> *         p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: (9), (10)

setup = setup.add(*meet.equations())
#>    (1)  m01.dt     = -m0.t + m1.t
#>    (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = -p0.t + p1.t
#>    (6)  p01.v_av.x = (-p0.pos.x + p1.pos.x)/p01.dt
#>    (7)  p01.a.x    = (-p0.vel.x + p1.vel.x)/p01.dt
#>    (8)  p01.v_av.x = p0.vel.x/2 + p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#> * (11)  m1.t       = meet.t
#> * (12)  p1.t       = meet.t
#> * (13)  m1.pos.x   = meet.pos.x
#> * (14)  p1.pos.x   = meet.pos.x
#>   knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#>           p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: (9), (10)

setup = setup.eliminate_zeros()
#> *  (1)  m01.dt     = m1.t
#> *  (2)  m01.v_av.x = m1.pos.x/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> *  (5)  p01.dt     = p1.t
#> *  (6)  p01.v_av.x = p1.pos.x/p01.dt
#> *  (7)  p01.a.x    = p1.vel.x/p01.dt
#> *  (8)  p01.v_av.x = p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#>   (11)  m1.t       = meet.t
#>   (12)  p1.t       = meet.t
#>   (13)  m1.pos.x   = meet.pos.x
#>   (14)  p1.pos.x   = meet.pos.x
#>   knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#>           p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#>   wants: none
#>   connected: none
#>   ready: (9), (10)

part_a = setup.want(meet.t)
#>    (1)  m01.dt     = m1.t
#>    (2)  m01.v_av.x = m1.pos.x/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = p1.t
#>    (6)  p01.v_av.x = p1.pos.x/p01.dt
#>    (7)  p01.a.x    = p1.vel.x/p01.dt
#>    (8)  p01.v_av.x = p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#>   (11)  m1.t       = meet.t
#>   (12)  p1.t       = meet.t
#>   (13)  m1.pos.x   = meet.pos.x
#>   (14)  p1.pos.x   = meet.pos.x
#>   knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#>           p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#> * wants: meet.t
#> * connected: m0.vel.x, m01.a.x, m01.dt, m01.v_av.x, m1.pos.x, m1.t,
#> *            m1.vel.x, meet.pos.x, meet.t, p01.dt, p01.v_av.x, p1.pos.x,
#> *            p1.t, p1.vel.x (14 unknowns in 14 equations)
#>   ready: (9), (10)

sol_a = part_a.solve()
#> meet.t = 2*m_v/p01.a.x
#> meet.t = 10.0*second

part_b = setup.want(p1.vel.x)
#>    (1)  m01.dt     = m1.t
#>    (2)  m01.v_av.x = m1.pos.x/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = p1.t
#>    (6)  p01.v_av.x = p1.pos.x/p01.dt
#>    (7)  p01.a.x    = p1.vel.x/p01.dt
#>    (8)  p01.v_av.x = p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#>   (11)  m1.t       = meet.t
#>   (12)  p1.t       = meet.t
#>   (13)  m1.pos.x   = meet.pos.x
#>   (14)  p1.pos.x   = meet.pos.x
#>   knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#>           p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#> * wants: p1.vel.x
#> * connected: m0.vel.x, m01.a.x, m01.dt, m01.v_av.x, m1.pos.x, m1.t,
#> *            m1.vel.x, meet.pos.x, meet.t, p01.dt, p01.v_av.x, p1.pos.x,
#> *            p1.t, p1.vel.x (14 unknowns in 14 equations)
#>   ready: (9), (10)

sol_b = part_b.solve()
#> p1.vel.x = 2*m_v
#> p1.vel.x = 30.0*meter/second

part_c = setup.want(meet.pos.x)
#>    (1)  m01.dt     = m1.t
#>    (2)  m01.v_av.x = m1.pos.x/m01.dt
#>    (3)  m01.a.x    = (-m0.vel.x + m1.vel.x)/m01.dt
#>    (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#>    (5)  p01.dt     = p1.t
#>    (6)  p01.v_av.x = p1.pos.x/p01.dt
#>    (7)  p01.a.x    = p1.vel.x/p01.dt
#>    (8)  p01.v_av.x = p1.vel.x/2
#>    (9)  m0.vel.x   = m_v
#>   (10)  m1.vel.x   = m_v
#>   (11)  m1.t       = meet.t
#>   (12)  p1.t       = meet.t
#>   (13)  m1.pos.x   = meet.pos.x
#>   (14)  p1.pos.x   = meet.pos.x
#>   knowns: m_v = 15*meter/second, m0.pos.x = 0, m0.t = 0, p0.pos.x = 0,
#>           p0.t = 0, p0.vel.x = 0, p01.a.x = 3*meter/second**2
#> * wants: meet.pos.x
#> * connected: m0.vel.x, m01.a.x, m01.dt, m01.v_av.x, m1.pos.x, m1.t,
#> *            m1.vel.x, meet.pos.x, meet.t, p01.dt, p01.v_av.x, p1.pos.x,
#> *            p1.t, p1.vel.x (14 unknowns in 14 equations)
#>   ready: (9), (10)

sol_c = part_c.solve()
#> meet.pos.x = 2*m_v**2/p01.a.x
#> meet.pos.x = 150.0*meter

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, meet.t,      "10", unit=second),
    Answer(sol_b, p1.vel.x,    "30", unit=meter / second),
    Answer(sol_c, meet.pos.x, "150", unit=meter),
]
#> [✓ meet.t: book 10 second, found 10.0*second,
#>  ✓ p1.vel.x: book 30 meter/second, found 30.0*meter/second,
#>  ✓ meet.pos.x: book 150 meter, found 150.0*meter]

