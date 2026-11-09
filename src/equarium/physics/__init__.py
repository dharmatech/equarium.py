"""equarium's physics layer: structured symbols for particles, their
states and the edges between them, the kinematics equations, vectors and
their equations, and the book's notation.

A symbol is a `Var`, whose name is its access path, `m0.pos.x`, and
whose identity is its structure. A model's dimension is a type, `X`, `Y`
or `XY`, set once when it's made: `Particle("m", 2, X)`. The layer
imports the core, and the core imports nothing from here.

A `Vector` is a state's or an edge's, `m0.vel` or `m01.a`, or a lone
vector, such as a force, `Vector("F1", XY)`. Vectors add, subtract and
scale into a `Vec`, a vector expression, and `.eq` makes one equation
per axis: `R.eq(F1 + F2 + F3)`, `(F + n + w).eq(a * m)`. An `XY` vector
has polar parts, `mag`, `angle` and `angle_deg`, and `from_polar()` and
`to_polar()` write its polar equations, one way each.

The old physics code from combine-equations.py, `kinematics_states` and
`newtons_laws`, stays here until increment 007 of the 004 series. No
example uses it any more: only `tests/test_physics.py` does, to compare.
"""

from equarium.physics.axes import XY, X, Y
from equarium.physics.notation import BookNotation
from equarium.physics.particles import Edge, Particle, State
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vec, Vector

__all__ = [
    "BookNotation",
    "Edge",
    "Particle",
    "State",
    "Var",
    "Vec",
    "Vector",
    "X",
    "XY",
    "Y",
]
