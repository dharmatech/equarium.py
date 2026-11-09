"""University Physics, 15th edition, Example 4.1, written out with the
physics code's `Point3`.

Three wrestlers pull horizontally on a belt, seen from above:
F1 = 50 N along +x, F2 = 120 N along -y, and F3 = 250 N at 53° above
the -x axis. (a) Find the x- and y-components of the net force R on the
belt. (b) Find its magnitude and direction.

Ported from combine-equations.py's
`examples/up/ch4/up-example-4.1/up-example-4.1-v1-007-ok.py`: polar one
way, each force's components from its magnitude and angle, and R's
magnitude and angle from its components, all at once. Its local
`make_force`, `polar_to_components` and `components_to_polar` stay here,
and its `superposition_equations` is the physics code's. `F1_angle = 0`
is a value, so a zero known, never eliminated: the formulas keep
`cos(F1_angle)` and `sin(F1_angle)`. Its three solves are one here, with
R_x and R_y added as wants.

The book rounds F3's components first, so R = (-100 N, 80 N), and its
angle is 141°; unrounded, it's 141.59°. The book's step is a second
system: the angle from the rounded components.

    uv run python -m examples.up_15e.ch04.examples.n01.main
"""

import sympy as sp
from sympy.logic.boolalg import BooleanAtom

from equarium import System, eq_flat
from equarium.physics.kinematics_states import Point3
from equarium.physics.newtons_laws import superposition_equations
from examples.answers import Answer


def make_force(prefix: str) -> Point3:
    return Point3(
        x=sp.Symbol(f"{prefix}_x"),
        y=sp.Symbol(f"{prefix}_y"),
        z=sp.Symbol(f"{prefix}_z"),
        mag=sp.Symbol(f"{prefix}_mag"),
        angle=sp.Symbol(f"{prefix}_angle"),
    )


def polar_to_components(force: Point3) -> list[sp.Equality | BooleanAtom]:
    assert force.mag is not None and force.angle is not None  # make_force sets both
    return eq_flat(
        force.x, force.mag * sp.cos(force.angle),
        force.y, force.mag * sp.sin(force.angle),
    )


def components_to_polar(force: Point3) -> list[sp.Equality | BooleanAtom]:
    assert force.mag is not None and force.angle is not None  # make_force sets both
    return eq_flat(
        force.mag, sp.sqrt(force.x**2 + force.y**2),
        force.angle, sp.atan2(force.y, force.x),
    )


F1 = make_force("F1")
F2 = make_force("F2")
F3 = make_force("F3")
R = make_force("R")  # the net force
assert F1.mag is not None and F1.angle is not None  # make_force sets both
assert F2.mag is not None and F2.angle is not None
assert F3.mag is not None and F3.angle is not None
assert R.mag is not None and R.angle is not None

R_angle_deg = sp.Symbol("R_angle_deg")

belt = (
    System()
    .add(*superposition_equations(R, [F1, F2, F3]))  # (1), (2)
    .add(*polar_to_components(F1))  # (3), (4)
    .add(*polar_to_components(F2))  # (5), (6)
    .add(*polar_to_components(F3))  # (7), (8)
    .add(*components_to_polar(R))  # (9), (10)
    .add(sp.Eq(R_angle_deg, sp.deg(R.angle)))  # (11)
    .known({F1.mag: 50, F1.angle: sp.rad(0)})  # N
    .known({F2.mag: 120, F2.angle: sp.rad(270)})
    .known({F3.mag: 250, F3.angle: sp.rad(180 - 53)})
)

sol = belt.solve(R.x, R.y, R.mag, R.angle, R_angle_deg)
# R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)   -100.45
# R_y = F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)   79.66
# R_mag = sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle)
#         + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2
#         + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)            128.2
# R_angle = atan2(R_y's formula, R_x's)                                      2.471
# R_angle_deg = 180*atan2(R_y's formula, R_x's)/pi                           141.59

# The book's step: the angle from R's components rounded, (-100 N, 80 N).
book_step = (
    System()
    .add(*components_to_polar(R))  # (1), (2)
    .add(sp.Eq(R_angle_deg, sp.deg(R.angle)))  # (3)
    .known({R.x: -100, R.y: 80})  # N
)
sol_book = book_step.solve(R_angle_deg)
# R_angle_deg = 180*atan2(R_y, R_x)/pi   141.34

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, R.x, "-100"),  # N, a new want
    Answer(sol, R.y, "80"),  # N, a new want
    Answer(sol, R.mag, "128"),  # N
    Answer(sol_book, R_angle_deg, "141"),  # degrees, the book's step
]

if __name__ == "__main__":
    belt.show()
    print()
    sol.show()
    print()
    book_step.show()
    print()
    sol_book.show()
