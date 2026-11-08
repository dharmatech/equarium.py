"""University Physics, 15th edition, Example 2.5, with the equations
written out.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².
(a) When does the officer catch up? At that time, (b) how fast is the
officer going, and (c) how far has each traveled?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.5/up-example-2.5-v3-002-concise.py`, with
its symbol names and without its `Obj` and `Interval` helpers. Its five
zero equations are zero knowns here, followed by `eliminate_zeros()`.

    uv run python -m examples.up_15e.ch02.example_2_5_handwritten
"""

import sympy as sp

from equarium import System, eq_flat
from examples.answers import Answer

# The motorist (m) and the police officer (p), at the start (0) and when
# they meet (1).
m_0_x, m_0_t, m_0_v, m_1_x, m_1_t, m_1_v = sp.symbols("m_0_x m_0_t m_0_v m_1_x m_1_t m_1_v")
p_0_x, p_0_t, p_0_v, p_1_x, p_1_t, p_1_v = sp.symbols("p_0_x p_0_t p_0_v p_1_x p_1_t p_1_v")
m_a, v_av_m_0_1, p_a, v_av_p_0_1 = sp.symbols("m_a v_av_m_0_1 p_a v_av_p_0_1")
m_v, dist, t_01 = sp.symbols("m_v dist t_01")

setup = (
    System()
    # The motorist's 2.2, 2.7 and 2.10: (1) to (3).
    .add(
        sp.Eq(v_av_m_0_1, (m_1_x - m_0_x) / (m_1_t - m_0_t)),
        sp.Eq(m_a, (m_1_v - m_0_v) / (m_1_t - m_0_t)),
        sp.Eq(v_av_m_0_1, (m_0_v + m_1_v) / 2),
    )
    # The officer's: (4) to (6).
    .add(
        sp.Eq(v_av_p_0_1, (p_1_x - p_0_x) / (p_1_t - p_0_t)),
        sp.Eq(p_a, (p_1_v - p_0_v) / (p_1_t - p_0_t)),
        sp.Eq(v_av_p_0_1, (p_0_v + p_1_v) / 2),
    )
    # The motorist's speed is constant: (7) and (8).
    .add(*eq_flat(m_0_v, m_v, m_1_v, m_v))
    # They meet at the same place and time: (9) to (12).
    .add(*eq_flat(dist, m_1_x, dist, p_1_x, t_01, m_1_t, t_01, p_1_t))
    # Both start from the sign at t = 0, and the officer from rest.
    .known({p_0_v: 0, p_0_x: 0, m_0_t: 0, p_0_t: 0, m_0_x: 0})
    .known(m_v, 15)  # m/s
    .known(p_a, 3)  # m/s²
    .want(t_01, p_1_v, dist)
)

chase = setup.eliminate_zeros()  # as the old eliminate_zero_eqs
sol = chase.solve()  # t_01 = 2*m_v/p_a       10
#                      p_1_v = 2*m_v          30
#                      dist = 2*m_v**2/p_a    150

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, t_01, "10"),  # s
    Answer(sol, p_1_v, "30"),  # m/s
    Answer(sol, dist, "150"),  # m
]

if __name__ == "__main__":
    setup.show()  # the full set, the zeros among the knowns
    print()
    chase.show()  # the simpler set
    print()
    sol.show()
