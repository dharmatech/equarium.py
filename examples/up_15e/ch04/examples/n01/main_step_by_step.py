"""University Physics, 15th edition, Example 4.1, written out with the
physics code's `Point3`, the forces' components eliminated by hand, a
display after each stage.

Three wrestlers pull horizontally on a belt, seen from above:
F1 = 50 N along +x, F2 = 120 N along -y, and F3 = 250 N at 53° above
the -x axis. (a) Find the x- and y-components of the net force R on the
belt. (b) Find its magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.1/up-example-4.1-v1-006-ok-manual-elim.py`,
with the forces and helpers of `main.py`, beside it: the six components
eliminated by hand, x then y, then the four equations left solved all at
once, and the degrees added after. Its two solves before the degrees are one here,
with R_x and R_y added as wants. The book's angle step is
`main.py`'s.

    uv run python -m examples.up_15e.ch04.examples.n01.main_step_by_step
"""

import sympy as sp

from equarium import System
from equarium.physics.newtons_laws import superposition_equations
from examples.answers import Answer
from examples.up_15e.ch04.examples.n01.main import (
    F1,
    F2,
    F3,
    R,
    R_angle_deg,
    components_to_polar,
    polar_to_components,
    sol_book,
)

assert F1.mag is not None and F1.angle is not None  # make_force sets both
assert F2.mag is not None and F2.angle is not None
assert F3.mag is not None and F3.angle is not None
assert R.mag is not None and R.angle is not None

start = (
    System()
    .add(*superposition_equations(R, [F1, F2, F3]))  # (1), (2)
    .add(*polar_to_components(F1))  # (3), (4)
    .add(*polar_to_components(F2))  # (5), (6)
    .add(*polar_to_components(F3))  # (7), (8)
    .add(*components_to_polar(R))  # (9), (10)
    .known({F1.mag: 50, F1.angle: sp.rad(0)})  # N
    .known({F2.mag: 120, F2.angle: sp.rad(270)})
    .known({F3.mag: 250, F3.angle: sp.rad(180 - 53)})
)

xs = start.eliminate(F1.x, F2.x, F3.x)
ys = xs.eliminate(F1.y, F2.y, F3.y)
# The four equations the old script solves, in the shapes the eliminations
# leave here. It printed (3) and (4) with their sides the other way round.
# (3)  -F2_mag*cos(F2_angle) - F3_mag*cos(F3_angle) + R_x = F1_mag*cos(F1_angle)
# (4)  -F2_mag*sin(F2_angle) - F3_mag*sin(F3_angle) + R_y = F1_mag*sin(F1_angle)
# (9)  R_mag = sqrt(R_x**2 + R_y**2)
# (10) R_angle = atan2(R_y, R_x)

sol = ys.solve(R.x, R.y, R.mag, R.angle)
# The same formulas as main.py's: -100.45, 79.66, 128.2 and 2.471.

degrees = ys.add(sp.Eq(R_angle_deg, sp.deg(R.angle)))  # (11)
sol_deg = degrees.solve(R_angle_deg)
# R_angle_deg = 180*atan2(R_y's formula, R_x's)/pi   141.59

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, R.x, "-100"),  # N, a new want
    Answer(sol, R.y, "80"),  # N, a new want
    Answer(sol, R.mag, "128"),  # N
    Answer(sol_book, R_angle_deg, "141"),  # degrees, the book's step
]

STAGES: list[tuple[str, System]] = [
    ("start", start),
    ("x components", xs),
    ("y components", ys),
]

if __name__ == "__main__":
    for name, stage in STAGES:
        print(f"{name}:")
        stage.show()
        print()
    sol.show()
    print()
    sol_deg.show()
