"""University Physics, 15th edition, Example 2.5, with the physics code,
its links eliminated by hand, a display after each stage.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².
(a) When does the officer catch up? At that time, (b) how fast is the
officer going, and (c) how far has each traveled?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.5/up-example-2.5-v4-002-ks-eq-flat.py`.
Its five zero equations, in its `eq_flat` with the links, are zero
knowns here, followed by `eliminate_zeros()` where it called its
`eliminate_zero_eqs`, before the six link eliminations. The links are
the event `meet`'s equations, where the old script wrote them through
`t_01` and `dist`, and the same six eliminations remove them. Its three
solves are one here, with three wants.

    uv run python -m examples.up_15e.ch02.examples.n05.main_step_by_step
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics import Event, Particle, X
from examples.answers import Answer

m = Particle("m", 2, X)  # the motorist
p = Particle("p", 2, X)  # the police officer
m0, m1 = m.states
p0, p1 = p.states
m01 = m.edge(0, 1)
p01 = p.edge(0, 1)
meet = Event("meet", m1, p1)  # the same time and place

m_v = sp.Symbol("m_v")

start = (
    System()
    .add(*m.kinematics())  # (1) to (3)
    # The motorist at a constant 15 m/s: a constant zero acceleration.
    .add(*m01.constant_acceleration())  # (4)
    .add(*p.kinematics())  # (5) to (7)
    .add(*p01.constant_acceleration())  # (8): a constant 3.0 m/s²
)

links = (
    # The motorist's speed is constant: (9) and (10).
    start.add(*eq_flat(m_v, m0.vel.x, m_v, m1.vel.x))
    # The officer starts from rest, both at the sign, both at t = 0.
    .known({p0.vel.x: 0, m0.pos.x: 0, p0.pos.x: 0, m0.t: 0, p0.t: 0})
    # They meet at the same time and place: (11) to (14).
    .add(*meet.equations())
    .known(m_v, 15)  # m/s
    .known(p01.a.x, 3)  # m/s²
)

zeros = links.eliminate_zeros()  # as the old eliminate_zero_eqs

linked = zeros.eliminate(m0.vel.x, m1.vel.x, m1.pos.x, p1.pos.x, m1.t, p1.t)
# The eight equations the old script solves, each in the shape its
# eliminations leave here:
# (2)  m01.v_av.x = meet.pos.x/m01.dt
# (3)  m01.a.x = 0
# (4)  m01.v_av.x = m_v
# (6)  p01.v_av.x = meet.pos.x/p01.dt
# (7)  p01.a.x = p1.vel.x/p01.dt
# (8)  p01.v_av.x = p1.vel.x/2
# (11) m01.dt = meet.t
# (12) p01.dt = meet.t

sol = linked.want(meet.t, p1.vel.x, meet.pos.x).solve()
# meet.t = 2*m_v/p01.a.x          10
# p1.vel.x = 2*m_v                 30
# meet.pos.x = 2*m_v**2/p01.a.x    150

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, meet.t, "10"),  # s
    Answer(sol, p1.vel.x, "30"),  # m/s
    Answer(sol, meet.pos.x, "150"),  # m
]

STAGES: list[tuple[str, System]] = [
    ("start", start),
    ("links", links),
    ("zeros", zeros),
    ("linked", linked),
]

if __name__ == "__main__":
    for name, stage in STAGES:
        print(f"{name}:")
        stage.show()
        print()
    sol.show()
    print()
    linked.show_history()
