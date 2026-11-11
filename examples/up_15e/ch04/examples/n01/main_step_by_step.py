"""University Physics, 15th edition, Example 4.1, written out with the
physics code's `Vector`, the forces' components eliminated by hand, a
display after each stage.

Three wrestlers pull horizontally on a belt, seen from above:
F1 = 50 N along +x, F2 = 120 N along -y, and F3 = 250 N at 53° above
the -x axis. (a) Find the x- and y-components of the net force R on the
belt. (b) Find its magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.1/up-example-4.1-v1-006-ok-manual-elim.py`,
with the forces of `main.py`, beside it: the six components eliminated
by hand, x then y, then the four equations left solved all at once, and
the degrees added after. Its two solves before the degrees are one
here, with `R.x` and `R.y` added as wants. The book's angle step is
`main.py`'s.

    uv run python -m examples.up_15e.ch04.examples.n01.main_step_by_step
"""

import sympy as sp

from equarium import System
from examples.answers import Answer
from examples.up_15e.ch04.examples.n01.main import F1, F2, F3, R, sol_book

start = (
    System()
    .add(*R.eq(F1 + F2 + F3))  # (1), (2)
    .add(*F1.from_polar())  # (3), (4)
    .add(*F2.from_polar())  # (5), (6)
    .add(*F3.from_polar())  # (7), (8)
    .add(*R.to_polar())  # (9), (10)
    .known({F1.mag: 50, F1.angle: sp.rad(0)})  # N
    .known({F2.mag: 120, F2.angle: sp.rad(270)})
    .known({F3.mag: 250, F3.angle: sp.rad(180 - 53)})
)

xs = start.eliminate(F1.x, F2.x, F3.x)
ys = xs.eliminate(F1.y, F2.y, F3.y)
# The four equations the old script solves, in the shapes the eliminations
# leave here. It printed (3) and (4) with their sides the other way round.
# (3)  -F2.mag*cos(F2.angle) - F3.mag*cos(F3.angle) + R.x = F1.mag*cos(F1.angle)
# (4)  -F2.mag*sin(F2.angle) - F3.mag*sin(F3.angle) + R.y = F1.mag*sin(F1.angle)
# (9)  R.mag = sqrt(R.x**2 + R.y**2)
# (10) R.angle = atan2(R.y, R.x)

sol = ys.solve(R.x, R.y, R.mag, R.angle)
# The same formulas as main.py's: -100.45, 79.66, 128.2 and 2.471.

degrees = ys.add(*R.degrees())  # (11)
sol_deg = degrees.solve(R.angle_deg)
# R.angle_deg = 180*atan2(R.y's formula, R.x's)/pi   141.59

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, R.x, "-100"),  # N, a new want
    Answer(sol, R.y, "80"),  # N, a new want
    Answer(sol, R.mag, "128"),  # N
    Answer(sol_book, R.angle_deg, "141"),  # degrees, the book's step
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
