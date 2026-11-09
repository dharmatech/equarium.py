"""University Physics, 15th edition, Example 2.8, with the physics code.

For the ball of Example 2.7, at what time after release is it 5.00 m
below the railing? (The book's Fig. 2.25a shows both times.)

Ported from the last part of combine-equations.py's
`examples/up/ch2/up-example-2.7/up-example-2.7-v1-000.py`, on Example
2.7's base system, `ball`, which has its zeros eliminated already. The
old script prints both roots and chooses neither; `where(b1.t > 0)` is
the book's choice.

    uv run python -m examples.up_15e.ch02.examples.n08.main
"""

from examples.answers import Answer
from examples.up_15e.ch02.examples.n07.main import b1, ball

below = ball.known(b1.pos.y, -5.0).want(b1.t)  # m
sol = below.solve()
# b_1_t = (-b_0_v_y - sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1   3.36
# b_1_t = (-b_0_v_y + sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1   -0.30

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, b1.t, "-0.30", "3.36"),  # s, both roots
    Answer(sol.where(b1.t > 0), b1.t, "3.36"),  # s
]

if __name__ == "__main__":
    below.show()
    print()
    sol.show()
    print()
    sol.where(b1.t > 0).show()
