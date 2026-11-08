"""kinematic-equations 005's first derivation, with its symbols.

`kinematics` holds (2.2), (2.7) and (2.10) with `dt` as its own symbol,
and `derived` is `kinematics` with `dt` eliminated using (2.7).
"""

import sympy as sp

from equarium import System

x_1, x_2, v_1x, v_2x, v_av_x, dt, a_x = sp.symbols("x_1 x_2 v_1x v_2x v_av_x dt a_x")

kinematics = (
    System()
    .add(sp.Eq(v_av_x, (x_2 - x_1) / dt), label="2.2")
    .add(sp.Eq(a_x, (v_2x - v_1x) / dt), label="2.7")
    .add(sp.Eq(v_av_x, (v_1x + v_2x) / 2), label="2.10")
)
derived = kinematics.eliminate(dt, using="2.7")
