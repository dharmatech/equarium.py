"""equarium: solve physics problems from core equations with SymPy."""

from equarium.equations import eq_flat
from equarium.errors import Contradiction, EquariumError, UsageError
from equarium.system import System

__all__ = ["System", "eq_flat", "EquariumError", "UsageError", "Contradiction"]
