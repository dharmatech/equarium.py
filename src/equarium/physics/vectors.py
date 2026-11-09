"""`Vector`, a named vector whose components are `Var`s, and `Vec`, a vector
expression.

A `Vector` is a state's or an edge's, `m0.pos` or `m01.a`, or a lone
vector, such as a force, `Vector("F1", XY)`. Vectors add, subtract and
scale, component by component, into a `Vec`, and `.eq` makes one equation
per axis: `R.eq(F1 + F2 + F3)`. An `XY` vector has the polar parts `mag`,
`angle` and `angle_deg`, with `from_polar`, `to_polar` and `degrees`.
"""

from dataclasses import dataclass
from typing import cast

import sympy as sp

from equarium.errors import UsageError
from equarium.physics import polar
from equarium.physics.axes import XY, Axes, X, Y
from equarium.physics.symbols import Var


@dataclass(frozen=True)
class Vector[A: Axes]:
    """A vector in the axes `A`. Its component on an axis is
    `Var(owner, where, *quantity, axis)`: a state's position,
    `Vector("m", X, "0", ("pos",))`, has `m0.pos.x`, and a lone vector,
    `Vector("F1", XY)`, has `F1.x`.

    `x` needs `X` or `XY`, `y` needs `Y` or `XY`, and the polar parts,
    `mag`, `angle` and `angle_deg`, need `XY`. Pyright flags the others,
    and at run time they raise `UsageError`.

    The name is a Python identifier, which may end in a digit, as `F1`
    does.
    """

    owner: str
    axes: type[A]
    where: str = ""
    quantity: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.owner.isidentifier():
            raise UsageError(f"a vector's name is a Python identifier, not {self.owner!r}")

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

    @property
    def mag(self: Vector[XY]) -> Var:
        """The magnitude, `m0.vel.mag`."""
        return self._polar("mag")

    @property
    def angle(self: Vector[XY]) -> Var:
        """The angle in radians, from the +x axis, `m0.vel.angle`."""
        return self._polar("angle")

    @property
    def angle_deg(self: Vector[XY]) -> Var:
        """The angle in degrees, `m0.vel.angle_deg`."""
        return self._polar("angle_deg")

    def from_polar(self: Vector[XY]) -> list[sp.Eq]:
        """The components from the magnitude and the angle."""
        return polar.from_polar(self)

    def to_polar(self: Vector[XY]) -> list[sp.Eq]:
        """The magnitude and the angle from the components."""
        return polar.to_polar(self)

    def degrees(self: Vector[XY]) -> list[sp.Eq]:
        """The angle in degrees from the angle in radians."""
        return polar.degrees(self)

    def __add__(self, other: Vector[A] | Vec[A]) -> Vec[A]:
        return _combine(self, other, "+")

    def __radd__(self, other: int) -> Vec[A]:
        return _start_sum(other, self)

    def __sub__(self, other: Vector[A] | Vec[A]) -> Vec[A]:
        return _combine(self, other, "-")

    def __neg__(self) -> Vec[A]:
        return -_as_vec(self)

    def __mul__(self, k: sp.Expr | float) -> Vec[A]:
        return _as_vec(self) * _scalar(k, self)

    def __rmul__(self, k: sp.Expr | float) -> Vec[A]:
        return _as_vec(self) * _scalar(k, self)

    def eq(self, other: Vector[A] | Vec[A]) -> list[sp.Eq]:
        """One equation per axis, x first: `self`'s component equals
        `other`'s."""
        return _equations(self, other)

    def _component(self, axis: str) -> Var:
        if axis not in self.axes.names:
            raise UsageError(f"{_name(self)} is in {self.axes.__name__}, so it has no {axis}")
        return Var(self.owner, self.where, *self.quantity, axis)

    def _polar(self, part: str) -> Var:
        if self.axes.names != XY.names:
            raise UsageError(f"{_name(self)} is in {self.axes.__name__}, so it has no {part}")
        return Var(self.owner, self.where, *self.quantity, part)


@dataclass(frozen=True)
class Vec[A: Axes]:
    """A vector expression in the axes `A`: one SymPy expression per axis,
    in the axes' order, such as `F1 + F2`'s `(F1.x + F2.x, F1.y + F2.y)`.
    It has no name, no `x` or `y`, and no polar parts.
    """

    axes: type[A]
    components: tuple[sp.Expr, ...]

    def __add__(self, other: Vector[A] | Vec[A]) -> Vec[A]:
        return _combine(self, other, "+")

    def __radd__(self, other: int) -> Vec[A]:
        return _start_sum(other, self)

    def __sub__(self, other: Vector[A] | Vec[A]) -> Vec[A]:
        return _combine(self, other, "-")

    def __neg__(self) -> Vec[A]:
        return Vec(self.axes, tuple(-c for c in self.components))

    def __mul__(self, k: sp.Expr | float) -> Vec[A]:
        k = _scalar(k, self)
        return Vec(self.axes, tuple(c * k for c in self.components))

    def __rmul__(self, k: sp.Expr | float) -> Vec[A]:
        return self * k

    def eq(self, other: Vector[A] | Vec[A]) -> list[sp.Eq]:
        """One equation per axis, x first: `self`'s component equals
        `other`'s."""
        return _equations(self, other)


def _name[A: Axes](v: Vector[A]) -> str:
    return ".".join((v.owner + v.where, *v.quantity))


def _describe(v: object) -> str:
    """How an operand reads in a message: a vector's name, a `Vec`'s
    components, or anything else's repr."""
    if isinstance(v, Vector):
        return _name(v)
    if isinstance(v, Vec):
        return "(" + ", ".join(str(c) for c in v.components) + ")"
    return repr(v)


def _as_vec[A: Axes](v: Vector[A] | Vec[A]) -> Vec[A]:
    if isinstance(v, Vector):
        return Vec(v.axes, v.components)
    return v


def _operand[A: Axes](left: Vector[A] | Vec[A], right: object, call: str) -> Vec[A]:
    """`right` as a `Vec`, once it's a vector in `left`'s axes. Pyright
    checks this, and so does the run time, since `zip` would drop an axis
    silently."""
    if not isinstance(right, Vector | Vec):
        raise UsageError(f"{call}: {_describe(right)} isn't a vector")
    if right.axes is not left.axes:
        raise UsageError(
            f"{call}: {_describe(left)} is in {left.axes.__name__},"
            f" but {_describe(right)} is in {right.axes.__name__}"
        )
    return _as_vec(cast(Vector[A] | Vec[A], right))


def _combine[A: Axes](left: Vector[A] | Vec[A], right: object, op: str) -> Vec[A]:
    """`left + right` or `left - right`, component by component."""
    other = _operand(left, right, f"{_describe(left)} {op} {_describe(right)}")
    pairs = zip(_as_vec(left).components, other.components)
    if op == "+":
        return Vec(left.axes, tuple(a + b for a, b in pairs))
    return Vec(left.axes, tuple(a - b for a, b in pairs))


def _start_sum[A: Axes](other: object, v: Vector[A] | Vec[A]) -> Vec[A]:
    """`0 + v`, as `sum()` starts. Any other left operand is a misuse."""
    if type(other) is not int or other != 0:
        raise UsageError(
            f"{_describe(other)} + {_describe(v)}: {_describe(other)} isn't a vector,"
            " or the 0 that sum() starts with"
        )
    return _as_vec(v)


def _scalar(k: object, v: object) -> sp.Expr | float:
    """`k`, once it's a scalar: a SymPy expression, an `int` or a `float`."""
    if not isinstance(k, sp.Expr | int | float):
        raise UsageError(f"{_describe(v)} * {_describe(k)}: {_describe(k)} isn't a scalar")
    return k


def _equations[A: Axes](left: Vector[A] | Vec[A], right: object) -> list[sp.Eq]:
    other = _operand(left, right, f"{_describe(left)}.eq({_describe(right)})")
    pairs = zip(_as_vec(left).components, other.components)
    return [cast(sp.Eq, sp.Eq(a, b)) for a, b in pairs]
