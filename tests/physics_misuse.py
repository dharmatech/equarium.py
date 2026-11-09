# pyright: reportUnnecessaryTypeIgnoreComment=true
"""Misuses of the physics layer that pyright must flag, one per marked line.

pyright checks this file, and pytest neither collects it nor runs it.
Each misuse carries an ignore comment for the error pyright gives, so
the run stays clean. An ignore that isn't needed fails `uv run pyright`,
so a misuse pyright stops flagging fails it too. Later increments add the
misuses their features can have.
"""

from equarium.physics import XY, Particle, Vector, X, Y

# An axis that the model doesn't have.
m = Particle("m", 2, X)
m0, m1 = m.states
m01 = m.edge(0, 1)
m0.pos.y  # pyright: ignore[reportAttributeAccessIssue]
m01.a.y  # pyright: ignore[reportAttributeAccessIssue]

b = Particle("b", 2, Y)
b0, b1 = b.states
b0.vel.x  # pyright: ignore[reportAttributeAccessIssue]

# The polar parts in one dimension, and vectors of different dimensions.
F1, R = Vector("F1", XY), Vector("R", XY)
f = Vector("f", X)
f.mag  # pyright: ignore[reportAttributeAccessIssue]
f.from_polar()  # pyright: ignore[reportAttributeAccessIssue]
_ = F1 + f  # pyright: ignore[reportOperatorIssue]
R.eq(f)  # pyright: ignore[reportArgumentType]
