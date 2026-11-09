"""University Physics, 15th edition, Example 3.10, with the physics code.

A monkey hangs in a tree at horizontal distance d from a dart gun, which
is aimed straight at it at angle α0 with muzzle speed v0, so the monkey
starts at height d tan α0 above the muzzle. The monkey lets go just as
the dart is fired; no air resistance. Show that the dart always hits the
monkey, provided it gets there before the monkey reaches the ground.

Ported from combine-equations.py's
`examples/up/ch3/up-example-3.10-v1-001.py`: two models, the dart's
launch polar one way, where the old script had it both ways, and 19
eliminations by hand in its order. The dart's eliminations leave the
same two equations as the old script's. Each model's zero equations are
zero knowns, eliminated in its own system before the two meet, as in
the old script. The book's d is `D`. All the givens are symbols: knowns
with no number. The old script's g = 9.81 was never used.

The old script keeps three equations, picked by index, and links them
through new symbols `t` and `y`; here they're picked by label. What is
left is the stated condition, which holds exactly when the dart reaches
x = D. With `d1.pos.x = D` added, which the old script had commented
out, nothing is left. The displayed equations have their sides the
other way round from the old output's: they're the same equations.

The book's time, a new want, comes from where the x's agree: the dart's
x equation, the monkey's x equations, which the old script dropped, and
the links through `t` and the x's.

    uv run python -m examples.up_15e.ch03.examples.n10.main
"""

import sympy as sp

from equarium import System, eq_flat
from equarium.physics import XY, Particle
from examples.answers import Formula

D, g = sp.symbols("D g")  # the horizontal distance to the monkey, and gravity
t, y = sp.symbols("t y")  # when and at what height they meet

# The dart.
d = Particle("d", 2, XY)
d0, d1 = d.states
d01 = d.edge(0, 1)

dart_start = (
    System()
    .add(*d.kinematics())  # (1) to (7)
    .add(*d0.vel.from_polar())  # (8), (9)
    .add(*eq_flat(d01.a.y, -g, d0.vel.x, d1.vel.x))  # (10), (11): projectile motion
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
# (8)  d1.pos.x/d1.t = d0.vel.mag*cos(d0.vel.angle)
# (9)  g*d1.t/2 + d1.pos.y/d1.t = d0.vel.mag*sin(d0.vel.angle)

# The monkey.
m = Particle("m", 2, XY)
m0, m1 = m.states
m01 = m.edge(0, 1)

monkey_start = (
    System()
    .add(*m.kinematics())  # (1) to (7)
    .add(*eq_flat(m0.pos.x, D, m0.pos.y, D * sp.tan(d0.vel.angle), m01.a.y, -g))  # (8) to (10)
    .known(D)
    .known(g)
    .known(d0.vel.angle)
    .known({m01.a.x: 0, m0.t: 0, m0.vel.x: 0, m0.vel.y: 0, m1.vel.x: 0})  # it lets go at t = 0
    .eliminate_zeros()
)
monkey = monkey_start.eliminate(m0.pos.y, m01.dt, m01.v_av.y, m1.vel.y, m01.a.y)
# The one the old script keeps:
# (9)  g*m1.t**2/2 + m1.pos.y = D*tan(d0.vel.angle)
# and its x equations, which it drops:
# (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m1.t
# (6)  m01.v_av.x = 0
# (8)  m0.pos.x = D

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
# (2)  D*d0.vel.mag*sin(d0.vel.angle)/d1.pos.x = d0.vel.mag*sin(d0.vel.angle)
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
# d1.t = D/(d0.vel.mag*cos(d0.vel.angle))

BOOK: list[Formula] = [  # University Physics, 15th ed.
    Formula(sol_t, d1.t, D / (d0.vel.mag * sp.cos(d0.vel.angle))),
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
