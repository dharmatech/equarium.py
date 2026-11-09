"""The physics layer's symbols, renamed back to the old physics code's
names, so the tests can compare a formula with the old output verbatim.

The rules:

- a state's, `make_states_model`'s names: `m0.pos.x` → `m_0_x`,
  `m0.vel.x` → `m_0_v_x`, `m0.t` → `m_0_t`, and its velocity in polar,
  `m0.vel.mag` → `m_0_v_mag` and `m0.vel.angle` → `m_0_v_angle`;
- an edge's: `m01.dt` → `dt_m_0_1`, `m01.a.x` → `a_x_m_0_1`,
  `m01.v_av.x` → `v_av_x_m_0_1`;
- a lone vector's, `make_point`'s names: `F1.x` → `F1_x`, `F1.mag` →
  `F1_mag`, `F1.angle` → `F1_angle`.

A plain symbol keeps its name. A `Var` the rules don't cover raises, so a
symbol they miss is loud: a position's or an edge's polar parts, any
`angle_deg`, an event's. The old code had none of them. There is no
per-module map yet: the symbols the rules can't reach come with the
increments that add them.
"""

import sympy as sp

from equarium.physics import Var

AXES = ("x", "y")


def old_name(symbol: sp.Symbol) -> str:
    """The old name of a symbol, by the rules above."""
    if not isinstance(symbol, Var):
        return symbol.name
    owner, where = symbol.owner, symbol.where
    if where == "":  # a lone vector
        match symbol.path:
            case (part,) if part in (*AXES, "mag", "angle"):
                return f"{owner}_{part}"
            case _:
                pass
    elif len(where) == 1 and where.isdigit():  # a state
        match symbol.path:
            case ("pos", axis) if axis in AXES:
                return f"{owner}_{where}_{axis}"
            case ("vel", part) if part in (*AXES, "mag", "angle"):
                return f"{owner}_{where}_v_{part}"
            case ("t",):
                return f"{owner}_{where}_t"
            case _:
                pass
    elif len(where) == 2 and where.isdigit():  # an edge
        i, j = where
        match symbol.path:
            case ("dt",):
                return f"dt_{owner}_{i}_{j}"
            case ("a", axis) if axis in AXES:
                return f"a_{axis}_{owner}_{i}_{j}"
            case ("v_av", axis) if axis in AXES:
                return f"v_av_{axis}_{owner}_{i}_{j}"
            case _:
                pass
    raise ValueError(f"no old name for {symbol.name}")


def old_str(expr: sp.Basic) -> str:
    """`str()` of an expression with every `Var` replaced by a plain symbol
    of its old name. With plain symbols, SymPy prints the old order."""
    return str(
        expr.xreplace(
            {var: sp.Symbol(old_name(var)) for var in expr.free_symbols if isinstance(var, Var)}
        )
    )
