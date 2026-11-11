"""University Physics, 15th edition, Example 2.5, with the physics code,
solved all at once.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².
(a) When does the officer catch up? At that time, (b) how fast is the
officer going, and (c) how far has each traveled?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.5/up-example-2.5-v4-000-ks.py`. The
meeting is an event, `Event("meet", m1, p1)`, whose four links are (11)
to (14): each state's time, then its position, equal to the event's.
The old script wrote them itself, through `t_01` and `dist`, positions
first. Its five zero equations, which `sp.solve` took with the rest,
are zero knowns here, followed by `eliminate_zeros()` before the solve.
Its three solves are one here, with three wants.

    uv run python -m examples.up_15e.ch02.examples.n05.main
"""

import sympy as sp

from equarium import System
from equarium.display import render, render_solution
from equarium.physics import BookNotation, Event, Particle, X
from examples.answers import Answer

m = Particle("m", 2, X)  # the motorist
p = Particle("p", 2, X)  # the police officer
m0, m1 = m.states
p0, p1 = p.states
m01 = m.edge(0, 1)
p01 = p.edge(0, 1)
meet = Event("meet", m1, p1)  # the same time and place

m_v = sp.Symbol("m_v")

setup = (
    System()
    .add(*m.kinematics())  # (1) to (3)
    .add(*m01.constant_acceleration())  # (4)
    .add(*p.kinematics())  # (5) to (7)
    .add(*p01.constant_acceleration())  # (8)
    # The motorist's speed is constant: (9) and (10).
    .add(sp.Eq(m0.vel.x, m_v), sp.Eq(m1.vel.x, m_v))
    .known(m_v, 15)  # m/s
    # The officer starts from rest at the sign, and both start there at t = 0.
    .known({p0.vel.x: 0, p0.pos.x: 0, m0.pos.x: 0, m0.t: 0, p0.t: 0})
    .known(p01.a.x, 3)  # m/s²
    # They meet at the same time and place: (11) to (14).
    .add(*meet.equations())
    .want(meet.t, p1.vel.x, meet.pos.x)
)

chase = setup.eliminate_zeros()
sol = chase.solve()
# meet.t = 2*m_v/p01.a.x          10
# p1.vel.x = 2*m_v                 30
# meet.pos.x = 2*m_v**2/p01.a.x    150

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, meet.t, "10"),  # s
    Answer(sol, p1.vel.x, "30"),  # m/s
    Answer(sol, meet.pos.x, "150"),  # m
]

if __name__ == "__main__":
    setup.show()  # the full set, the zeros among the knowns
    print()
    chase.show()  # the simpler set
    print()
    sol.show()
    print()
    print("In the book's notation:")
    print()
    book = BookNotation(owners={"m": "M", "p": "P"})
    print(render(setup, symbol=book))
    print()
    print(render(chase, symbol=book))
    print()
    print(render_solution(sol, symbol=book))
