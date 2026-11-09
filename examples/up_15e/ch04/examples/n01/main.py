"""University Physics, 15th edition, Example 4.1, written out with the
physics code's `Vector`.

Three wrestlers pull horizontally on a belt, seen from above:
F1 = 50 N along +x, F2 = 120 N along -y, and F3 = 250 N at 53° above
the -x axis. (a) Find the x- and y-components of the net force R on the
belt. (b) Find its magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.1/up-example-4.1-v1-007-ok.py`: polar one
way, each force's components from its magnitude and angle, and R's
magnitude and angle from its components, all at once. Its local
`make_force`, `polar_to_components` and `components_to_polar` are the
physics code's lone vectors, `from_polar()` and `to_polar()`, and its
`superposition_equations` is `R.eq(F1 + F2 + F3)`. Its degrees equation
is `R.degrees()`. `F1.angle = 0` is a
value, so a zero known, never eliminated: the formulas keep
`cos(F1.angle)` and `sin(F1.angle)`. Its three solves are one here, with
`R.x` and `R.y` added as wants.

The book rounds F3's components first, so R = (-100 N, 80 N), and its
angle is 141°; unrounded, it's 141.59°. The book's step is a second
system: the angle from the rounded components.

    uv run python -m examples.up_15e.ch04.examples.n01.main
"""

import sympy as sp

from equarium import System
from equarium.physics import XY, Vector
from examples.answers import Answer

F1 = Vector("F1", XY)
F2 = Vector("F2", XY)
F3 = Vector("F3", XY)
R = Vector("R", XY)  # the net force

belt = (
    System()
    .add(*R.eq(F1 + F2 + F3))  # (1), (2)
    .add(*F1.from_polar())  # (3), (4)
    .add(*F2.from_polar())  # (5), (6)
    .add(*F3.from_polar())  # (7), (8)
    .add(*R.to_polar())  # (9), (10)
    .add(*R.degrees())  # (11)
    .known({F1.mag: 50, F1.angle: sp.rad(0)})  # N
    .known({F2.mag: 120, F2.angle: sp.rad(270)})
    .known({F3.mag: 250, F3.angle: sp.rad(180 - 53)})
)

sol = belt.solve(R.x, R.y, R.mag, R.angle, R.angle_deg)
# R.x = F1.mag*cos(F1.angle) + F2.mag*cos(F2.angle) + F3.mag*cos(F3.angle)   -100.45
# R.y = F1.mag*sin(F1.angle) + F2.mag*sin(F2.angle) + F3.mag*sin(F3.angle)   79.66
# R.mag = sqrt(F1.mag**2 + 2*F1.mag*F2.mag*cos(F1.angle - F2.angle)
#         + 2*F1.mag*F3.mag*cos(F1.angle - F3.angle) + F2.mag**2
#         + 2*F2.mag*F3.mag*cos(F2.angle - F3.angle) + F3.mag**2)            128.2
# R.angle = atan2(R.y's formula, R.x's)                                      2.471
# R.angle_deg = 180*atan2(R.y's formula, R.x's)/pi                           141.59

# The book's step: the angle from R's components rounded, (-100 N, 80 N).
book_step = (
    System()
    .add(*R.to_polar())  # (1), (2)
    .add(*R.degrees())  # (3)
    .known({R.x: -100, R.y: 80})  # N
)
sol_book = book_step.solve(R.angle_deg)
# R.angle_deg = 180*atan2(R.y, R.x)/pi   141.34

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, R.x, "-100"),  # N, a new want
    Answer(sol, R.y, "80"),  # N, a new want
    Answer(sol, R.mag, "128"),  # N
    Answer(sol_book, R.angle_deg, "141"),  # degrees, the book's step
]

if __name__ == "__main__":
    belt.show()
    print()
    sol.show()
    print()
    book_step.show()
    print()
    sol_book.show()
