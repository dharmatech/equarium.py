"""University Physics, 15th edition, Example 2.5, with the equations
written out and eliminated by hand, a display after each stage.

A motorist at a constant 15 m/s passes a police officer on a motorcycle,
who starts after him from rest at that moment, with a constant 3.0 m/s².
(a) When does the officer catch up? At that time, (b) how fast is the
officer going, and (c) how far has each traveled?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.5/up-example-2.5-v3-001-step-by-step.py`,
with its symbol names and without its `Obj` and `Interval` helpers. Its
zero equations are zero knowns here, followed by `eliminate_zeros()` at
the point where the old script eliminated them.

    uv run python -m examples.up_15e.ch02.examples.n05.main_handwritten_step_by_step
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

start = (
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
    .known(m_v, 15)  # m/s
)

# (3) v_av_m_0_1 = m_v, and (2) m_a = 0.
speeds = start.eliminate(m_0_v, m_1_v)

# (1) m_v = (m_0_x - m_1_x)/(m_0_t - m_1_t)
motorist = speeds.eliminate(m_a, v_av_m_0_1)

# The officer starts from rest at the sign.
officer = motorist.known({p_0_v: 0, p_0_x: 0}).eliminate_zeros()

# Both clocks start at 0.
clocks = officer.known({m_0_t: 0, p_0_t: 0}).eliminate_zeros()

# The motorist starts at the sign too: (1) m_v = m_1_x/m_1_t.
origin = clocks.known(m_0_x, 0).eliminate_zeros()

# They meet at the same place, (9) and (10)...
place = (
    origin.known(p_a, 3)  # m/s²
    .add(*eq_flat(dist, m_1_x, dist, p_1_x))
    .eliminate(m_1_x, p_1_x)
)

# ...and at the same time, (11) and (12).
meet = place.add(*eq_flat(t_01, m_1_t, t_01, p_1_t)).eliminate(m_1_t, p_1_t)
# (1)  m_v = dist/t_01
# (4)  v_av_p_0_1 = dist/t_01
# (5)  p_a = p_1_v/t_01
# (6)  v_av_p_0_1 = p_1_v/2

sol = meet.want(t_01, p_1_v, dist).solve()  # t_01 = 2*m_v/p_a       10
#                                             p_1_v = 2*m_v          30
#                                             dist = 2*m_v**2/p_a    150

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, t_01, "10"),  # s
    Answer(sol, p_1_v, "30"),  # m/s
    Answer(sol, dist, "150"),  # m
]

STAGES: list[tuple[str, System]] = [
    ("start", start),
    ("speeds", speeds),
    ("motorist", motorist),
    ("officer", officer),
    ("clocks", clocks),
    ("origin", origin),
    ("place", place),
    ("meet", meet),
]

if __name__ == "__main__":
    for name, stage in STAGES:
        print(f"{name}:")
        stage.show()
        print()
    print("meet, with origins:")
    meet.show(origins=True)
    print()
    sol.show()
    print()
    meet.show_history()
