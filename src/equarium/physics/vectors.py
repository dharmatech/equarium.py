"""`Vector`, a named vector whose components are `Var`s: `m0.pos`, `m01.a`.

For now a vector has its components only. Arithmetic, `.eq` and the polar
parts come in later increments.
"""

from dataclasses import dataclass

from equarium.errors import UsageError
from equarium.physics.axes import XY, Axes, X, Y
from equarium.physics.symbols import Var


@dataclass(frozen=True)
class Vector[A: Axes]:
    """A vector in the axes `A`. Its component on an axis is
    `Var(owner, where, *quantity, axis)`: a state's position,
    `Vector("m", X, "0", ("pos",))`, has `m0.pos.x`.

    `x` needs `X` or `XY`, and `y` needs `Y` or `XY`. Pyright flags the
    others, and at run time they raise `UsageError`.
    """

    owner: str
    axes: type[A]
    where: str = ""
    quantity: tuple[str, ...] = ()

    @property
    def x(self: Vector[X] | Vector[XY]) -> Var:
        return self._component("x")

    @property
    def y(self: Vector[Y] | Vector[XY]) -> Var:
        return self._component("y")

    @property
    def components(self) -> tuple[Var, ...]:
        """One `Var` per axis, in the axes' order."""
        return tuple(self._component(axis) for axis in self.axes.names)

    def _component(self, axis: str) -> Var:
        if axis not in self.axes.names:
            name = ".".join((self.owner + self.where, *self.quantity))
            raise UsageError(f"{name} is in {self.axes.__name__}, so it has no {axis}")
        return Var(self.owner, self.where, *self.quantity, axis)
