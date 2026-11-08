"""The errors equarium raises, all sharing one base."""

import sympy as sp


class EquariumError(Exception):
    """A failure with the symbol and labels it concerns, for a GUI to show."""

    reason: str
    symbol: sp.Symbol | None
    labels: tuple[str, ...]

    def __init__(
        self,
        reason: str,
        *,
        symbol: sp.Symbol | None = None,
        labels: tuple[str, ...] = (),
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.symbol = symbol
        self.labels = labels

    def __str__(self) -> str:
        return self.reason


class UsageError(EquariumError):
    """A misuse: a duplicate or missing label, a known that is also a want, …"""


class Contradiction(EquariumError):
    """An equation that is false, such as one that became 0 = 3."""
