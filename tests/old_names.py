"""The physics layer's symbols, renamed back to the old physics code's
names, so the tests can compare a formula with the old output verbatim.

`m0.pos.x` was `m_0_x`, and `m01.a.x` was `a_x_m_0_1`. A plain symbol
keeps its name. A `Var` the old rule doesn't cover raises, so a symbol the
rule misses is loud. The symbols the rule can't reach, such as an event's
or a lone vector's, come with the increments that add them.
"""

import sympy as sp

from equarium.physics import Var

AXES = ("x", "y")


def old_name(symbol: sp.Symbol) -> str:
    """The old name of a symbol: `m0.pos.x` → `m_0_x`, `m0.vel.x` →
    `m_0_v_x`, `m0.t` → `m_0_t`, `m01.dt` → `dt_m_0_1`, `m01.a.x` →
    `a_x_m_0_1`, `m01.v_av.x` → `v_av_x_m_0_1`."""
    if not isinstance(symbol, Var):
        return symbol.name
    owner, where = symbol.owner, symbol.where
    if len(where) == 1 and where.isdigit():  # a state
        match symbol.path:
            case ("pos", axis) if axis in AXES:
                return f"{owner}_{where}_{axis}"
            case ("vel", axis) if axis in AXES:
                return f"{owner}_{where}_v_{axis}"
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
