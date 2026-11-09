"""equarium's physics layer: structured symbols for particles, their
states and the edges between them, the kinematics equations, and the
book's notation.

A symbol is a `Var`, whose name is its access path, `m0.pos.x`, and
whose identity is its structure. A model's dimension is a type, `X`, `Y`
or `XY`, set once when it's made: `Particle("m", 2, X)`. The layer
imports the core, and the core imports nothing from here.

The old physics code from combine-equations.py, `kinematics_states` and
`newtons_laws`, stays here until increment 007 of the 004 series, for
chapters 3 and 4.
"""

from equarium.physics.axes import XY, X, Y
from equarium.physics.notation import BookNotation
from equarium.physics.particles import Edge, Particle, State
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vector

__all__ = [
    "BookNotation",
    "Edge",
    "Particle",
    "State",
    "Var",
    "Vector",
    "X",
    "XY",
    "Y",
]
