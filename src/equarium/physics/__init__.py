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
has polar parts, `mag`, `angle` and `angle_deg`, and `from_polar()`,
`to_polar()` and `degrees()` write its polar equations, one way each.

An `Event` is two or more states at the same time and place,
`Event("meet", m1, p1)`, with its own time and position, `meet.t` and
`meet.pos`. `meet.equations()` writes the links, and `hit.equations(Y)`
links the positions on y only.

An `XY` edge has the projectile setup, `d01.projectile(g)`: a `Setup` of
equations, `d01.a.y = -g` and `d0.vel.x = d1.vel.x`, and knowns,
`d01.a.x` zero. The example adds both,
`.add(*flight.equations).known(flight.knowns)`, and sets its own origin
and clock.

The old physics code from combine-equations.py, `kinematics_states` and
`newtons_laws`, stays here until increment 007 of the 004 series. No
example uses it any more: only `tests/test_physics.py` does, to compare.
"""

from equarium.physics.axes import XY, X, Y
from equarium.physics.events import Event
from equarium.physics.notation import BookNotation
from equarium.physics.particles import Edge, Particle, State
from equarium.physics.projectile import Setup
from equarium.physics.symbols import Var
from equarium.physics.vectors import Vec, Vector

__all__ = [
    "BookNotation",
    "Edge",
    "Event",
    "Particle",
    "Setup",
    "State",
    "Var",
    "Vec",
    "Vector",
    "X",
    "XY",
    "Y",
]
