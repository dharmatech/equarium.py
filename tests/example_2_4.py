"""Example 2.4's equations written out, as in the spec's sketch.

`pre` is the base before `eliminate_zeros()`, `base` after it, and
`part_a` is part (a): t1 = 2 s, with x1 and v1 wanted.
"""

import sympy as sp

from equarium import System

x0, x1, v0, v1, t0, t1, v_av, a = sp.symbols("x0 x1 v0 v1 t0 t1 v_av a")

eq_2_2 = sp.Eq(v_av, (x1 - x0) / (t1 - t0))
eq_2_7 = sp.Eq(a, (v1 - v0) / (t1 - t0))
eq_2_10 = sp.Eq(v_av, (v0 + v1) / 2)


def motorcycle(t0_value: sp.Expr | float = 0) -> System:
    """The base before `eliminate_zeros()`."""
    return (
        System()
        .add(eq_2_2, label="2.2")
        .add(eq_2_7, label="2.7")
        .add(eq_2_10, label="2.10")
        .known(t0, t0_value)  # s
        .known(x0, 5)  # m
        .known(v0, 15)  # m/s
        .known(a, 4)  # m/s²
    )


pre = motorcycle()
base = pre.eliminate_zeros()
part_a = base.known(t1, 2).want(x1, v1)
