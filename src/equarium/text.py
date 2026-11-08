"""Small helpers for the text of displays and error reasons.

They import nothing from the package, so any module can use them.
"""

from collections.abc import Iterable


def listing(items: Iterable[str]) -> str:
    """The items joined by commas, or `none`."""
    return ", ".join(items) or "none"


def labels(names: Iterable[str]) -> str:
    return listing(f"({name})" for name in names)


def plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"
