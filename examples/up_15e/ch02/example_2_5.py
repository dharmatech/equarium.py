"""University Physics, 15th edition, Example 2.5, with the physics code,
solved all at once.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².
(a) When does the officer catch up? At that time, (b) how fast is the
officer going, and (c) how far has each traveled?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.5/up-example-2.5-v4-000-ks.py`, with its
links as it writes them. Its five zero equations, which `sp.solve` took
with the rest, are zero knowns here, followed by `eliminate_zeros()`
before the solve. Its three solves are one here, with three wants.

    uv run python -m examples.up_15e.ch02.example_2_5
"""

import sympy as sp

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

m = make_states_model("m", 2, include_v_av=True)  # the motorist
p = make_states_model("p", 2, include_v_av=True)  # the police officer
m0, m1 = m.states
p0, p1 = p.states
m01 = m.edges[0]
p01 = p.edges[0]

m_v, dist, t_01 = sp.symbols("m_v dist t_01")

setup = (
    System()
    .add(*kinematics_fundamental(m, axes=("x",), include_dt_defs=True))  # (1) to (4)
    .add(*kinematics_fundamental(p, axes=("x",), include_dt_defs=True))  # (5) to (8)
    # The motorist's speed is constant: (9) and (10).
    .add(sp.Eq(m0.vel.x, m_v), sp.Eq(m1.vel.x, m_v))
    .known(m_v, 15)  # m/s
    # The officer starts from rest at the sign, and both start there at t = 0.
    .known({p0.vel.x: 0, p0.pos.x: 0, m0.pos.x: 0, m0.t: 0, p0.t: 0})
    .known(p01.a.x, 3)  # m/s²
    # They meet at the same place and time: (11) to (14).
    .add(sp.Eq(dist, m1.pos.x), sp.Eq(dist, p1.pos.x))
    .add(sp.Eq(t_01, m1.t), sp.Eq(t_01, p1.t))
    .want(t_01, p1.vel.x, dist)
)

chase = setup.eliminate_zeros()
sol = chase.solve()
# t_01 = 2*m_v/a_x_p_0_1        10
# p_1_v_x = 2*m_v               30
# dist = 2*m_v**2/a_x_p_0_1     150

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, t_01, "10"),  # s
    Answer(sol, p1.vel.x, "30"),  # m/s
    Answer(sol, dist, "150"),  # m
]

if __name__ == "__main__":
    setup.show()  # the full set, the zeros among the knowns
    print()
    chase.show()  # the simpler set
    print()
    sol.show()
