"""SymPy's rough edges, each handled in one place."""

from typing import cast

import sympy as sp


def safe_simplify(expr: sp.Expr) -> sp.Expr:
    """`sp.simplify(expr)`, or `expr` unchanged when SymPy raises."""
    # SymPy issue 28926 (https://github.com/sympy/sympy/issues/28926):
    # simplify can raise instead of returning a result. This is the
    # package's only `try` around `simplify`, so it's the one place to
    # change once the issue is fixed.
    try:
        return sp.simplify(expr)
    except Exception:
        return expr


def free_symbols(expr: sp.Basic) -> frozenset[sp.Symbol]:
    """The free symbols of `expr`, which SymPy types as `set[Basic]`."""
    return frozenset(cast(set[sp.Symbol], expr.free_symbols))


def sides(eq: sp.Equality) -> tuple[sp.Expr, sp.Expr]:
    """An equation's two sides, which SymPy types as `Basic`."""
    return cast(sp.Expr, eq.lhs), cast(sp.Expr, eq.rhs)
