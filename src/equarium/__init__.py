"""equarium: solve physics problems from core equations with SymPy."""

from equarium.equations import eq_flat
from equarium.errors import (
    Contradiction,
    EliminationError,
    EquariumError,
    IsolationError,
    UsageError,
)
from equarium.solve import Root, Solution, all_at_once
from equarium.strategies import eliminating
from equarium.system import System

__all__ = [
    "System",
    "Solution",
    "Root",
    "eq_flat",
    "all_at_once",
    "eliminating",
    "EquariumError",
    "UsageError",
    "Contradiction",
    "EliminationError",
    "IsolationError",
]
