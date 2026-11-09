"""University Physics, 15th edition, Example 2.4, with the equations
written out.

A motorcyclist accelerates at a constant 4.0 m/s² from 5.0 m east of a
signpost, moving east at 15 m/s at t = 0. (a) Where is he, and how fast
is he going, at t = 2.0 s? (b) Where is he when his speed is 25 m/s?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.4/up-example-2.4-v3-001-step-by-step.py`.
Its `Eq(m_0.t, 0)` is `known(t0, 0)` here, followed by `eliminate_zeros()`.

    uv run python -m examples.up_15e.ch02.examples.n04.main_handwritten
"""

import sympy as sp

from equarium import System
from examples.answers import Answer

x0, x1, v0, v1, t0, t1, v_av, a = sp.symbols("x0 x1 v0 v1 t0 t1 v_av a")

motorcycle = (
    System()
    .add(sp.Eq(v_av, (x1 - x0) / (t1 - t0)), label="2.2")
    .add(sp.Eq(a, (v1 - v0) / (t1 - t0)), label="2.7")
    .add(sp.Eq(v_av, (v0 + v1) / 2), label="2.10")
    .known(t0, 0)  # s
    .known(x0, 5)  # m
    .known(v0, 15)  # m/s
    .known(a, 4)  # m/s²
    .eliminate_zeros()  # t0 drops out; x0 = 5 stays a symbol
)

# (a) Position and velocity at t = 2.0 s.
part_a = motorcycle.known(t1, 2).want(x1, v1)
sol_a = part_a.solve()  # x1 = a*t1**2/2 + t1*v0 + x0   43
#                         v1 = a*t1 + v0                23

# (b) Where is he when his speed is 25 m/s?
sol_b = motorcycle.known(v1, 25).solve(x1)
#                         x1 = (2*a*x0 - v0**2 + v1**2)/(2*a)   55

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, x1, "43"),  # m
    Answer(sol_a, v1, "23"),  # m/s
    Answer(sol_b, x1, "55"),  # m
]

if __name__ == "__main__":
    part_a.show()  # (2.2)  v_av = (-x0 + x1)/t1  … x0, t1 green; x1 red
    print()
    sol_a.show()
    print()
    sol_b.show()
