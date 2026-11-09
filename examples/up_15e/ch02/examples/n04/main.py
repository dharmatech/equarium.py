"""University Physics, 15th edition, Example 2.4, with the physics code.

A motorcyclist accelerates at a constant 4.0 m/s² from 5.0 m east of a
signpost, moving east at 15 m/s at t = 0. (a) Where is he, and how fast
is he going, at t = 2.0 s? (b) Where is he when his speed is 25 m/s?

Ported from combine-equations.py's
`examples/up/ch2/up-example-2.4/up-example-2.4-v4-001-ks-display-solution.py`.
Its `Eq(m0.t, 0)`, which `sp.solve` took with the rest, is `known(m0.t, 0)`
here, followed by `eliminate_zeros()` in the base, before the parts branch.

    uv run python -m examples.up_15e.ch02.examples.n04.main
"""

from equarium import System
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.answers import Answer

m = make_states_model("m", 2, include_v_av=True)  # the motorcyclist
m0, m1 = m.states
e01 = m.edges[0]  # the interval from state 0 to state 1

motorcycle = (
    System()
    .add(
        *kinematics_fundamental(
            m,
            axes=("x",),
            include_dt_defs=True,
            include_eq2=True,
            include_eq7=True,
            include_eq10=True,
        )
    )
    .known(m0.t, 0)  # s
    .known(e01.a.x, 4)  # m/s²
    .known(m0.pos.x, 5)  # m
    .known(m0.vel.x, 15)  # m/s
    .eliminate_zeros()  # m_0_t drops out; the other knowns stay symbols
)

# (a) Position and velocity at t = 2.0 s.
part_a = motorcycle.known(m1.t, 2).want(m1.pos.x, m1.vel.x)
sol_a = part_a.solve()
# m_1_x = a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x   43
# m_1_v_x = a_x_m_0_1*m_1_t + m_0_v_x                     23

# (b) Where is he when his speed is 25 m/s?
part_b = motorcycle.known(m1.vel.x, 25).want(m1.pos.x)
sol_b = part_b.solve()
# m_1_x = (2*a_x_m_0_1*m_0_x - m_0_v_x**2 + m_1_v_x**2)/(2*a_x_m_0_1)   55

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol_a, m1.pos.x, "43"),  # m
    Answer(sol_a, m1.vel.x, "23"),  # m/s
    Answer(sol_b, m1.pos.x, "55"),  # m
]

if __name__ == "__main__":
    part_a.show()
    print()
    sol_a.show()
    print()
    part_b.show()
    print()
    sol_b.show()
