import re

import sympy as sp

from equarium import Solution, System
from equarium.display import plain, render, render_history, render_solution
from examples.up_15e.ch02.example_2_4_handwritten import sol_a
from examples.up_15e.ch02.example_2_5_handwritten_step_by_step import m_a, speeds

from example_2_4 import base, part_a, pre, t0, t1, v0, v1, x0, x1
from kinematics_005 import derived

D, g = sp.symbols("D g")

PART_A = """\
(2.2)  v_av = (-x0 + x1)/t1
(2.7)  a = (-v0 + v1)/t1
(2.10)  v_av = v0/2 + v1/2
knowns: t0 = 0, x0 = 5, v0 = 15, a = 4, t1 = 2
wants: x1, v1
connected: v1, v_av, x1 (3 unknowns in 3 equations)
ready: (2.7)"""

PART_A_HISTORY = """\
1. add (2.2)
2. add (2.7)
3. add (2.10)
4. known t0 = 0
5. known x0 = 5
6. known v0 = 15
7. known a = 4
8. eliminate zeros t0: into (2.2), (2.7)
9. known t1 = 2
10. want x1, v1"""


def uncolored(text: str) -> str:
    return re.sub(r"\x1b\[\d+m", "", text)


def last_step(system: System) -> str:
    return render_history(system, symbol=plain).splitlines()[-1]


def test_render_part_a() -> None:
    assert render(part_a, symbol=plain) == PART_A


def test_render_terminal() -> None:
    rendered = render(part_a)
    assert rendered.splitlines()[0] == (
        "(2.2)  v_av = (-\x1b[32mx0\x1b[0m + \x1b[31mx1\x1b[0m)/\x1b[32mt1\x1b[0m"
    )
    assert uncolored(rendered) == PART_A


def test_render_before_eliminate_zeros() -> None:
    lines = render(pre, symbol=plain).splitlines()
    assert lines[0] == "(2.2)  v_av = (-x0 + x1)/(-t0 + t1)"
    assert lines[3] == "knowns: t0 = 0, x0 = 5, v0 = 15, a = 4"


def test_term_order() -> None:
    # The old display printed `m_1_t - m_0_t` once m_1_t was colored.
    dt, m_0_t, m_1_t = sp.symbols("dt m_0_t m_1_t")
    system = System().add(sp.Eq(dt, -m_0_t + m_1_t)).want(m_1_t)
    assert render(system, symbol=plain).splitlines()[0] == "(1)  dt = -m_0_t + m_1_t"
    assert uncolored(render(system).splitlines()[0]) == "(1)  dt = -m_0_t + m_1_t"


def test_render_knowns_with_no_number() -> None:
    assert render(System().known(D).known(g, 9.8), symbol=plain) == (
        "knowns: D, g = 9.8\nwants: none\nconnected: none\nready: none"
    )


def test_render_history_part_a() -> None:
    assert render_history(part_a, symbol=plain) == PART_A_HISTORY


def test_render_history_uses_each_steps_roles() -> None:
    lines = render_history(part_a).splitlines()
    assert lines[3] == "4. known \x1b[32mt0\x1b[0m = 0"
    assert lines[9] == "10. want \x1b[31mx1\x1b[0m, \x1b[31mv1\x1b[0m"
    assert uncolored(render_history(part_a)) == PART_A_HISTORY
    forgotten = System().known(t1, 2).forget(t1)
    assert render_history(forgotten).splitlines()[-1] == "2. forget t1"


def test_render_history_forms() -> None:
    y0, y1 = sp.symbols("y0 y1")
    assert last_step(System().add(sp.Eq(x1, x0), sp.Eq(v0, t1))) == "1. add (1), (2)"
    assert last_step(System().known({D: None, g: 9.8})) == "1. known D, g = 9.8"
    assert last_step(System().known(t1, 2).forget(t1)) == "2. forget t1"
    assert last_step(System().want()) == "1. want none"
    two_zeros = (
        System()
        .add(
            sp.Eq(x1, x0 + v0 * (t1 - t0)),
            sp.Eq(v0, x1 / t1),
            sp.Eq(y1, y0 + v0 * t1),
            sp.Eq(y0, t0),
        )
        .known({t0: 0, y0: 0})
        .eliminate_zeros()
    )
    assert last_step(two_zeros) == "3. eliminate zeros t0, y0: into (1), (3), dropped (4)"
    dropped = System().add(sp.Eq(t0, 0)).known(t0, 0).eliminate_zeros()
    assert last_step(dropped) == "3. eliminate zeros t0: dropped (1)"
    unchanged = System().add(sp.Eq(x1, x0)).known(t0, 0).eliminate_zeros()
    assert last_step(unchanged) == "3. eliminate zeros t0: no change"
    none = System().add(sp.Eq(x1, x0)).eliminate_zeros()
    assert last_step(none) == "2. eliminate zeros: none"
    assert render_history(System(), symbol=plain) == ""


# Origins and the new history forms


def test_render_origins_after_eliminating() -> None:
    lines = render(derived, symbol=plain, origins=True).splitlines()
    assert lines[:3] == [
        "(2.2)  v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)",
        "  (2.2) ← (2.2) + (2.7), eliminate dt",
        "(2.10)  v_av_x = v_1x/2 + v_2x/2",
    ]
    assert lines[3] == "knowns: none"  # nothing under (2.10)


def test_render_origins_after_eliminating_zeros() -> None:
    lines = render(base, symbol=plain, origins=True).splitlines()
    assert lines[:5] == [
        "(2.2)  v_av = (-x0 + x1)/t1",
        "  (2.2) ← (2.2), t0 = 0",
        "(2.7)  a = (-v0 + v1)/t1",
        "  (2.7) ← (2.7), t0 = 0",
        "(2.10)  v_av = v0/2 + v1/2",
    ]
    # The symbols go through the hook: t0 is a known.
    assert render(base, origins=True).splitlines()[1] == "  (2.2) ← (2.2), \x1b[32mt0\x1b[0m = 0"


def test_render_origins_after_isolating() -> None:
    isolated = base.isolate(v1, "2.7")
    lines = render(isolated, symbol=plain, origins=True).splitlines()
    assert lines[2:4] == ["(2.7)  v1 = a*t1 + v0", "  (2.7) ← (2.7), isolate v1"]


def test_render_without_origins_is_unchanged() -> None:
    assert render(part_a, symbol=plain, origins=False) == PART_A
    for system in (derived, base, base.isolate(v1, "2.7")):
        with_origins = render(system, symbol=plain, origins=True).splitlines()
        assert render(system, symbol=plain) == "\n".join(
            line for line in with_origins if not line.startswith("  ")
        )


def test_render_history_eliminate_and_isolate() -> None:
    assert last_step(derived) == "4. eliminate dt using (2.7): into (2.2)"
    assert last_step(base.isolate(v1, "2.7")) == "9. isolate v1 in (2.7)"
    assert last_step(speeds.eliminate(m_a)).endswith(". eliminate m_a using (2)")
    x, y, z = sp.symbols("x y z")
    dropped = System().add(sp.Eq(x, y), sp.Eq(x, y), sp.Eq(z, x)).eliminate(x)
    assert last_step(dropped) == "2. eliminate x using (1): into (3), dropped (2)"
    only_dropped = System().add(sp.Eq(x, y), sp.Eq(x, y)).eliminate(x)
    assert last_step(only_dropped) == "2. eliminate x using (1): dropped (2)"


# Solutions

SOL_A = """\
x1 = a*t1**2/2 + t1*v0 + x0
x1 = 43.0
v1 = a*t1 + v0
v1 = 23.0"""


def test_render_solution() -> None:
    assert render_solution(sol_a, symbol=plain) == SOL_A


def test_render_solution_terminal() -> None:
    rendered = render_solution(sol_a)
    assert rendered.startswith("\x1b[31mx1\x1b[0m = ")
    assert "\x1b[32mt1\x1b[0m" in rendered.splitlines()[0]
    assert uncolored(rendered) == SOL_A


def test_render_several_roots() -> None:
    x = sp.Symbol("x")
    solution = System().add(sp.Eq(x**2, 4)).want(x).solve()
    lines = render_solution(solution, symbol=plain).splitlines()
    assert len(lines) == 6
    assert (lines[0], lines[3]) == ("root 1:", "root 2:")
    # Either root may come first, but each keeps its formula and number together.
    roots = {(lines[1], lines[2]), (lines[4], lines[5])}
    assert roots == {("  x = -2", "  x = -2.0"), ("  x = 2", "  x = 2.0")}


def test_render_no_roots() -> None:
    x, y = sp.symbols("x y")
    solution = System().add(sp.Eq(x + y, 1), sp.Eq(x + y, 2)).want(x).solve()
    assert render_solution(solution, symbol=plain) == "no roots: sp.solve found no roots"


# The time, from 1 s


def test_render_solution_with_the_time() -> None:
    slow = Solution(sol_a.system, sol_a.roots, 1.5)
    assert render_solution(slow, symbol=plain) == SOL_A + "\ntime: 1.50 s"


def test_render_no_roots_with_the_time() -> None:
    slow = Solution(sol_a.system, (), 2.0, "sp.solve found no roots")
    assert render_solution(slow, symbol=plain) == (
        "no roots: sp.solve found no roots\ntime: 2.00 s"
    )


def test_render_solution_under_1_s_has_no_time() -> None:
    assert sol_a.elapsed < 1
    assert "time:" not in render_solution(sol_a, symbol=plain)
