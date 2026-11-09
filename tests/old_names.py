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
`angle_deg`, an event's. The old code had none of them.

`SCRIPT_NAMES` is a per-module map for the names an old script made
itself, which a reshape turned into `Var`s: 3.6's `dist` is
`m1.pos.mag` now. In its module, the map wins over the rules: 3.7's
`b0.vel.mag` is `b0_vel_mag`, where the rule says `b_0_v_mag`. 2.5's
`meet.t` and `meet.pos.x` are its `t_01` and `dist`. Increment 006 adds
4.5's `b.mass`.
"""

from collections.abc import Mapping

import sympy as sp

from equarium.physics import Var

AXES = ("x", "y")

# The names an old script made itself, by module under `examples.up_15e`,
# as `OLD` names it, and keyed by the `Var`, since a name can print alike.
SCRIPT_NAMES: Mapping[str, Mapping[Var, str]] = {
    "ch02.examples.n05.main": {
        Var("meet", "", "t"): "t_01",
        Var("meet", "", "pos", "x"): "dist",
    },
    "ch02.examples.n05.main_step_by_step": {
        Var("meet", "", "t"): "t_01",
        Var("meet", "", "pos", "x"): "dist",
    },
    "ch03.examples.n06.main": {
        Var("m", "1", "pos", "mag"): "dist",
        Var("m", "1", "vel", "mag"): "vel_mag",
        Var("m", "1", "vel", "angle"): "vel_angle",
        Var("m", "1", "vel", "angle_deg"): "vel_angle_deg",
    },
    "ch03.examples.n07.main": {
        Var("b", "0", "vel", "mag"): "b0_vel_mag",
        Var("b", "0", "vel", "angle"): "b0_vel_angle",
        Var("b", "1", "vel", "mag"): "b1_vel_mag",
        Var("b", "1", "vel", "angle"): "b1_vel_angle",
        Var("b", "1", "vel", "angle_deg"): "b1_vel_angle_deg",
    },
    "ch04.examples.n01.main": {Var("R", "", "angle_deg"): "R_angle_deg"},
    "ch04.examples.n01.main_step_by_step": {Var("R", "", "angle_deg"): "R_angle_deg"},
}


def old_name(symbol: sp.Symbol, module: str = "") -> str:
    """The old name of a symbol: the module's map first, then the rules
    above. Without a module, the rules alone."""
    if not isinstance(symbol, Var):
        return symbol.name
    script_name = SCRIPT_NAMES.get(module, {}).get(symbol)
    if script_name is not None:
        return script_name
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


def old_str(expr: sp.Basic, module: str = "") -> str:
    """`str()` of an expression with every `Var` replaced by a plain symbol
    of its old name, in the module's names. With plain symbols, SymPy
    prints the old order."""
    return str(
        expr.xreplace(
            {
                var: sp.Symbol(old_name(var, module))
                for var in expr.free_symbols
                if isinstance(var, Var)
            }
        )
    )
