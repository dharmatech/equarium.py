"""University Physics, 15th edition, Example 3.10, with the physics code.

A monkey hangs in a tree at horizontal distance d from a dart gun, which
is aimed straight at it at angle α0 with muzzle speed v0, so the monkey
starts at height d tan α0 above the muzzle. The monkey lets go just as
the dart is fired; no air resistance. Show that the dart always hits the
monkey, provided it gets there before the monkey reaches the ground.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.10-v1-001.py`: two models, the dart's
launch polar both ways, and 19 eliminations by hand in its order. Each
model's zero equations are zero knowns, eliminated in its own system
before the two meet, as in the old script. The book's d is `D`. All the
givens are symbols: knowns with no number. The old script's g = 9.81
was never used.

The old script keeps three equations, picked by index, and links them
through new symbols `t` and `y`; here they're picked by label. What is
left is the stated condition, which holds exactly when the dart reaches
x = D. With `d1.pos.x = D` added, which the old script had commented
out, nothing is left. The displayed equations have their sides the
other way round from the old output's: they're the same equations.

The book's time, a new want, comes from where the x's agree: the dart's
x equation, the monkey's x equations, which the old script dropped, and
the links through `t` and the x's.

    uv run python -m examples.up_15e.ch03.example_3_10
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics.kinematics_states import (
    kinematics_fundamental,
    magnitude_and_angle_equations,
    make_states_model,
)
from examples.answers import Formula

D, g = sp.symbols("D g")  # the horizontal distance to the monkey, and gravity
t, y = sp.symbols("t y")  # when and at what height they meet

# The dart.
d = make_states_model("d", 2)
d0, d1 = d.states
d01 = d.edges[0]
assert d0.vel.mag is not None and d0.vel.angle is not None  # make_states_model sets both
assert d01.v_av is not None  # make_states_model includes it by default

dart_start = (
    System()
    .add(*kinematics_fundamental(d, axes=["x", "y"]))  # (1) to (7)
    .add(*magnitude_and_angle_equations(d0))  # (8) to (11)
    .add(*eq_flat(d01.a.y, -g, d0.vel.x, d1.vel.x))  # (12), (13): projectile motion
    .known({d0.pos.x: 0, d0.pos.y: 0, d01.a.x: 0, d0.t: 0})  # from the muzzle, at t = 0
    .known(g)
    .known(d0.vel.mag)  # v0
    .known(d0.vel.angle)  # α0
    .eliminate_zeros()
)
dart = dart_start.eliminate(
    d01.dt, d01.v_av.x, d0.vel.x, d1.vel.x, d0.vel.y, d01.v_av.y, d01.a.y, d1.vel.y
)
# The two equations the old script keeps:
# (8)  d_1_x/d_1_t = d_0_v_mag*cos(d_0_v_angle)
# (9)  d_1_t*g/2 + d_1_y/d_1_t = d_0_v_mag*sin(d_0_v_angle)

# The monkey.
m = make_states_model("m", 2)
m0, m1 = m.states
m01 = m.edges[0]
assert m01.v_av is not None  # make_states_model includes it by default

monkey_start = (
    System()
    .add(*kinematics_fundamental(m, axes=["x", "y"]))  # (1) to (7)
    .add(*eq_flat(m0.pos.x, D, m0.pos.y, D * sp.tan(d0.vel.angle), m01.a.y, -g))  # (8) to (10)
    .known(D)
    .known(g)
    .known(d0.vel.angle)
    .known({m01.a.x: 0, m0.t: 0, m0.vel.x: 0, m0.vel.y: 0, m1.vel.x: 0})  # it lets go at t = 0
    .eliminate_zeros()
)
monkey = monkey_start.eliminate(m0.pos.y, m01.dt, m01.v_av.y, m1.vel.y, m01.a.y)
# The one the old script keeps:
# (9)  g*m_1_t**2/2 + m_1_y = D*tan(d_0_v_angle)
# and its x equations, which it drops:
# (2)  v_av_x_m_0_1 = (-m_0_x + m_1_x)/m_1_t
# (6)  v_av_x_m_0_1 = 0
# (8)  m_0_x = D

# They meet: the same time and height.
meet = (
    System()
    .add(dart.equation("8").eq, dart.equation("9").eq, monkey.equation("9").eq)  # (1) to (3)
    .add(*eq_flat(d1.t, t, m1.t, t, d1.pos.y, y, m1.pos.y, y))  # (4) to (7)
    .known(D)
    .known(g)
    .known(d0.vel.mag)
    .known(d0.vel.angle)
)
proved = meet.eliminate(d1.t, m1.t, d1.pos.y, m1.pos.y, y, t)
# (2)  D*d_0_v_mag*sin(d_0_v_angle)/d_1_x = d_0_v_mag*sin(d_0_v_angle)
# which holds exactly when the dart reaches x = D:
reached = meet.add(sp.Eq(d1.pos.x, D)).eliminate(d1.t, m1.t, d1.pos.y, m1.pos.y, y, t, d1.pos.x)
# no equations left

# The time when the x's agree.
agree = (
    System()
    .add(dart.equation("8").eq)  # (1)
    .add(monkey.equation("2").eq, monkey.equation("6").eq, monkey.equation("8").eq)  # (2) to (4)
    .add(*eq_flat(d1.t, t, m1.t, t, d1.pos.x, m1.pos.x))  # (5) to (7)
    .known(D)
    .known(d0.vel.mag)
    .known(d0.vel.angle)
)
sol_t = agree.solve(d1.t)
# d_1_t = D/(d_0_v_mag*cos(d_0_v_angle))

BOOK: list[Formula] = [  # University Physics, 15th ed.
    Formula(sol_t, d1.t, "D/(d_0_v_mag*cos(d_0_v_angle))"),
]

STAGES: list[tuple[str, System]] = [
    ("dart", dart),
    ("monkey", monkey),
    ("meet", meet),
    ("proved", proved),
    ("reached", reached),
    ("agree", agree),
]

if __name__ == "__main__":
    for name, stage in STAGES:
        print(f"{name}:")
        stage.show()
        print()
    sol_t.show()
