"""University Physics, 15th edition, Example 2.4, with the physics code.

A motorcyclist accelerates at a constant 4.0 m/s² from 5.0 m east of a
signpost, moving east at 15 m/s at t = 0. (a) Where is he, and how fast
is he going, at t = 2.0 s? (b) Where is he when his speed is 25 m/s?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.4/up-example-2.4-v4-001-ks-display-solution.py`.
Its `Eq(m0.t, 0)`, which `sp.solve` took with the rest, is
`known(m0.t, 0 * second)` here, followed by `eliminate_zeros()` in the
base, before the parts branch.

The knowns carry SymPy's units, and the book's answers are checked in
them. Units come in only with the numbers: the equations and the
formulas are the same as without them.

    uv run python -m examples.up_15e.ch02.examples.n04.main
"""

from sympy.physics.units import meter, second

from equarium import System
from equarium.display import render, render_solution
from equarium.physics import BookNotation, Particle, X
from examples.answers import Answer

m = Particle("m", 2, X)  # the motorcyclist
m0, m1 = m.states
m01 = m.edge(0, 1)  # the interval from state 0 to state 1

motorcycle = (
    System()
    .add(*m.kinematics())
    .add(*m01.constant_acceleration())  # a constant 4.0 m/s²
    .known(m0.t,      0 * second)
    .known(m01.a.x,   4 * meter / second**2)
    .known(m0.pos.x,  5 * meter)
    .known(m0.vel.x, 15 * meter / second)
    .eliminate_zeros()  # m0.t drops out; the other knowns stay symbols
)

# (a) Position and velocity at t = 2.0 s.
part_a = motorcycle.known(m1.t, 2 * second).want(m1.pos.x, m1.vel.x)
sol_a = part_a.solve()
# m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2   43.0*meter
# m1.vel.x = m0.vel.x + m01.a.x*m1.t                        23.0*meter/second

# (b) Where is he when his speed is 25 m/s?
part_b = motorcycle.known(m1.vel.x, 25 * meter / second).want(m1.pos.x)
sol_b = part_b.solve()
# m1.pos.x = (2*m0.pos.x*m01.a.x - m0.vel.x**2 + m1.vel.x**2)/(2*m01.a.x)   55.0*meter

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, m1.pos.x, "43", unit=meter),
    Answer(sol_a, m1.vel.x, "23", unit=meter / second),
    Answer(sol_b, m1.pos.x, "55", unit=meter),
]

if __name__ == "__main__":
    part_a.show()
    print()
    sol_a.show()
    print()
    part_b.show()
    print()
    sol_b.show()
    print()
    print("In the book's notation:")
    print()
    book = BookNotation()
    print(render(part_a, symbol=book))
    print()
    print(render_solution(sol_a, symbol=book))
    print()
    print(render(part_b, symbol=book))
    print()
    print(render_solution(sol_b, symbol=book))
