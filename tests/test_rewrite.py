import pytest
import sympy as sp

from equarium import (
    Contradiction,
    EliminationError,
    IsolationError,
    System,
    UsageError,
    eq_flat,
)
from equarium.display import plain, render_history
from equarium.equations import Derived, Given
from equarium.steps import EliminateStep, IsolateStep
from equarium.sympy_compat import free_symbols, safe_simplify
from examples.answers import Answer
from examples.up_15e.ch02.examples.n05 import main_handwritten as ex_2_5
from examples.up_15e.ch02.examples.n05 import main_handwritten_step_by_step as ex_2_5_steps

from example_2_4 import base, part_a, v1, x0, x1
from kinematics_005 import a_x, derived, dt, kinematics, v_1x, v_2x, v_av_x, x_1, x_2


def labels(system: System) -> tuple[str, ...]:
    return tuple(e.label for e in system.equations)


def history(system: System) -> list[str]:
    """The rendered steps, without their numbers."""
    return [line.split(". ", 1)[1] for line in render_history(system, symbol=plain).splitlines()]


def equations(system: System) -> list[str]:
    return [f"({e.label})  {e.eq.lhs} = {e.eq.rhs}" for e in system.equations]


# kinematic-equations 005's first derivation


def test_005_derivation() -> None:
    eq = derived.equation("2.2").eq
    assert eq == sp.Eq(v_av_x, a_x * (x_1 - x_2) / (v_1x - v_2x))
    assert safe_simplify(eq.rhs - a_x * (x_2 - x_1) / (v_2x - v_1x)) == 0


def test_005_what_it_changed() -> None:
    assert labels(derived) == ("2.2", "2.10")
    assert derived.equation("2.10") is kinematics.equation("2.10")
    assert derived.equation("2.10").origin == Given()
    assert derived.equation("2.2").origin == Derived(
        "eliminate", dt, (kinematics.equation("2.2"), kinematics.equation("2.7"))
    )
    assert derived.step == EliminateStep(
        symbol=dt, using="2.7", replacement=(-v_1x + v_2x) / a_x, rewritten=("2.2",), dropped=()
    )
    assert derived.previous is kinematics


# The six links of 2.5

LINKS = (ex_2_5.m_0_v, ex_2_5.m_1_v, ex_2_5.m_1_x, ex_2_5.p_1_x, ex_2_5.m_1_t, ex_2_5.p_1_t)
linked = ex_2_5.chase.eliminate(*LINKS)


def test_2_5_links_are_gone() -> None:
    for e in linked.equations:
        assert not free_symbols(e.eq) & set(LINKS), e


def test_2_5_six_steps() -> None:
    assert history(linked)[-6:] == [
        "eliminate m_0_v using (7): into (2), (3)",
        "eliminate m_1_v using (8): into (2), (3)",
        "eliminate m_1_x using (9): into (1)",
        "eliminate p_1_x using (10): into (4)",
        "eliminate m_1_t using (11): into (1)",
        "eliminate p_1_t using (12): into (4), (5)",
    ]
    steps: list[EliminateStep] = []
    current: System | None = linked
    while current is not ex_2_5.chase:
        assert current is not None and isinstance(current.step, EliminateStep)
        steps.append(current.step)
        current = current.previous
    assert [step.symbol for step in reversed(steps)] == list(LINKS)


def test_2_5_links_still_solve() -> None:
    sol = linked.solve()
    (root,) = sol.roots
    assert [str(f) for f in root.formulas.values()] == ["2*m_v/p_a", "2*m_v", "2*m_v**2/p_a"]
    assert [float(n) for n in root.numbers.values()] == [10.0, 30.0, 150.0]


def test_2_5_shape_is_kept() -> None:
    # Simplifying the whole Eq would have given `m_v = v_av_m_0_1` and
    # `p_1_v = 2*v_av_p_0_1`.
    assert linked.equation("3").eq.lhs == ex_2_5.v_av_m_0_1
    assert equations(linked)[2] == "(3)  v_av_m_0_1 = m_v"
    assert linked.equation("6").eq.lhs == ex_2_5.v_av_p_0_1
    assert equations(linked)[5] == "(6)  v_av_p_0_1 = p_1_v/2"


def test_2_5_step_by_step_meet() -> None:
    assert equations(ex_2_5_steps.meet) == [
        "(1)  m_v = dist/t_01",
        "(4)  v_av_p_0_1 = dist/t_01",
        "(5)  p_a = p_1_v/t_01",
        "(6)  v_av_p_0_1 = p_1_v/2",
    ]
    (root,) = ex_2_5_steps.sol.roots
    assert [str(f) for f in root.formulas.values()] == ["2*m_v/p_a", "2*m_v", "2*m_v**2/p_a"]


# 3.10: the dart always hits the monkey.

d0x, d1x, d0y, d1y, d0vx, d1vx, d0vy, d1vy, d0t, d1t = sp.symbols(
    "d0x d1x d0y d1y d0vx d1vx d0vy d1vy d0t d1t"
)
d_dt, d_vav_x, d_vav_y, d_a_x, d_a_y = sp.symbols("d_dt d_vav_x d_vav_y d_a_x d_a_y")
m0x, m1x, m0y, m1y, m0vx, m1vx, m0vy, m1vy, m0t, m1t = sp.symbols(
    "m0x m1x m0y m1y m0vx m1vx m0vy m1vy m0t m1t"
)
m_dt, m_vav_x, m_vav_y, m_a_x, m_a_y = sp.symbols("m_dt m_vav_x m_vav_y m_a_x m_a_y")
D, g, v_mag, angle, t, y = sp.symbols("D g v_mag angle t y")


dart_and_monkey = (
    System()
    # The dart's seven, in the old physics code's order: (1) to (7).
    .add(
        sp.Eq(d_dt, d1t - d0t),
        sp.Eq(d_vav_x, (d1x - d0x) / d_dt),  # 2.2
        sp.Eq(d_vav_y, (d1y - d0y) / d_dt),
        sp.Eq(d_a_x, (d1vx - d0vx) / d_dt),  # 2.7
        sp.Eq(d_a_y, (d1vy - d0vy) / d_dt),
        sp.Eq(d_vav_x, (d0vx + d1vx) / 2),  # 2.10
        sp.Eq(d_vav_y, (d0vy + d1vy) / 2),
    )
    # Its launch, polar form one way, and its fall: (8) to (11).
    .add(*eq_flat(d0vx, v_mag * sp.cos(angle), d0vy, v_mag * sp.sin(angle), d_a_y, -g, d0vx, d1vx))
    # The monkey's seven: (12) to (18).
    .add(
        sp.Eq(m_dt, m1t - m0t),
        sp.Eq(m_vav_x, (m1x - m0x) / m_dt),
        sp.Eq(m_vav_y, (m1y - m0y) / m_dt),
        sp.Eq(m_a_x, (m1vx - m0vx) / m_dt),
        sp.Eq(m_a_y, (m1vy - m0vy) / m_dt),
        sp.Eq(m_vav_x, (m0vx + m1vx) / 2),
        sp.Eq(m_vav_y, (m0vy + m1vy) / 2),
    )
    # Its start, in line with the gun, and its fall: (19) to (21).
    .add(*eq_flat(m0x, D, m0y, D * sp.tan(angle), m_a_y, -g))
    # The dart meets the monkey: the same time and height, (22) to (25).
    .add(*eq_flat(d1t, t, m1t, t, d1y, y, m1y, y))
    .known(D)
    .known(v_mag)
    .known(angle)
    .known(g, 9.81)  # m/s²
    .known({sym: 0 for sym in (d0x, d0y, d_a_x, d0t, m_a_x, m0t, m0vx, m0vy, m1vx)})
    .eliminate_zeros()
)

# The monkey's x first: otherwise the automatic choice uses the monkey's
# x equation to eliminate t.
ORDER_3_10 = (
    (m_vav_x, m1x, m0x)
    + (d_dt, d_vav_x, d0vx, d1vx, d0vy, d_vav_y, d_a_y, d1vy)
    + (m0y, m_dt, m_vav_y, m1vy, m_a_y)
    + (d1t, m1t, d1y, m1y, y, t)
)


def test_3_10_base() -> None:
    assert len(dart_and_monkey.equations) == 24


def test_3_10_the_stated_condition_is_left() -> None:
    proved = dart_and_monkey.eliminate(*ORDER_3_10)
    assert len(proved.equations) == 1
    (left,) = proved.equations
    assert left.label == "9"
    assert left.eq == sp.Eq(D * v_mag * sp.sin(angle) / d1x, v_mag * sp.sin(angle))
    # It holds exactly when the dart reaches x = D.
    assert left.eq.subs(d1x, D) == sp.true


def test_3_10_nothing_is_left_once_the_dart_reaches_D() -> None:
    reached = dart_and_monkey.add(sp.Eq(d1x, D)).eliminate(*ORDER_3_10, d1x)
    assert reached.equations == ()


# 4.1: three forces on a belt, eliminated by hand.

F1_x, F1_y, F1_mag, F1_angle = sp.symbols("F1_x F1_y F1_mag F1_angle")
F2_x, F2_y, F2_mag, F2_angle = sp.symbols("F2_x F2_y F2_mag F2_angle")
F3_x, F3_y, F3_mag, F3_angle = sp.symbols("F3_x F3_y F3_mag F3_angle")
R_x, R_y, R_mag, R_angle, R_angle_deg = sp.symbols("R_x R_y R_mag R_angle R_angle_deg")

belt = (
    System()
    .add(*eq_flat(R_x, F1_x + F2_x + F3_x, R_y, F1_y + F2_y + F3_y))
    .add(
        *eq_flat(
            F1_x, F1_mag * sp.cos(F1_angle), F1_y, F1_mag * sp.sin(F1_angle),
            F2_x, F2_mag * sp.cos(F2_angle), F2_y, F2_mag * sp.sin(F2_angle),
            F3_x, F3_mag * sp.cos(F3_angle), F3_y, F3_mag * sp.sin(F3_angle),
        )
    )
    .add(
        *eq_flat(
            R_mag, sp.sqrt(R_x**2 + R_y**2),
            R_angle, sp.atan2(R_y, R_x),
            R_angle_deg, sp.deg(R_angle),
        )
    )
    .known({F1_mag: 50, F1_angle: 0})  # N; the zero stays a known, as in the old values
    .known({F2_mag: 120, F2_angle: 3 * sp.pi / 2})
    .known({F3_mag: 250, F3_angle: sp.rad(127)})
)
COMPONENTS = (F1_x, F2_x, F3_x, F1_y, F2_y, F3_y)


def test_4_1() -> None:
    by_hand = belt.eliminate(F1_x, F2_x, F3_x).eliminate(F1_y, F2_y, F3_y)
    for e in by_hand.equations:
        assert not free_symbols(e.eq) & set(COMPONENTS), e
    # The two roots for F1_x are equally simple, and (1) comes first, as
    # in the old library.
    first = belt.eliminate(F1_x)
    assert isinstance(first.step, EliminateStep)
    assert first.step.using == "1"

    sol = by_hand.want(R_mag, R_angle_deg).solve()
    assert len(sol.roots) == 1
    assert Answer(sol, R_mag, "128").mismatch() is None  # N
    assert Answer(sol, R_angle_deg, "141.6").mismatch() is None  # degrees
    assert abs(float(sol.number(R_mag)) - 128.2049) < 1e-4
    assert abs(float(sol.number(R_angle_deg)) - 141.5859) < 1e-4


# Isolate


def test_isolate() -> None:
    isolated = base.isolate(v1, "2.7")
    after = isolated.equation("2.7")
    assert str(after.eq) == "Eq(v1, a*t1 + v0)"
    assert after.origin == Derived("isolate", v1, (base.equation("2.7"),))
    assert labels(isolated) == labels(base)
    assert isolated.step == IsolateStep(v1, "2.7")


# Errors

x, y_, z = sp.symbols("x y z")
quadratic = System().add(sp.Eq(y_, x**2), label="q").add(sp.Eq(y_, x + 2), label="l")


def test_eliminate_from_an_equation_without_the_symbol() -> None:
    with pytest.raises(EliminationError) as caught:
        kinematics.eliminate(x_1, using="2.10")
    assert caught.value.symbol == x_1
    assert caught.value.labels == ("2.10",)


def test_two_roots() -> None:
    chosen = quadratic.eliminate(x)
    assert isinstance(chosen.step, EliminateStep)
    assert chosen.step.using == "l"
    with pytest.raises(EliminationError) as caught:
        quadratic.eliminate(x, using="q")
    assert "2 roots" in caught.value.reason


def test_no_equation_gives_one_root() -> None:
    with pytest.raises(EliminationError) as caught:
        System().add(sp.Eq(y_, x**2), label="q").eliminate(x)
    assert caught.value.labels == ("q",)
    assert "(q) gives 2 roots" in caught.value.reason


def test_eliminate_a_known_or_a_want() -> None:
    with pytest.raises(EliminationError):
        base.eliminate(x0)
    with pytest.raises(EliminationError):
        part_a.eliminate(x1)


def test_isolate_two_roots() -> None:
    with pytest.raises(IsolationError) as caught:
        quadratic.isolate(x, "q")
    assert "2 roots" in caught.value.reason
    with pytest.raises(IsolationError):
        quadratic.isolate(z, "q")


def test_contradiction() -> None:
    contradictory = System().add(sp.Eq(x, y_ + 5), sp.Eq(x, y_))
    with pytest.raises(Contradiction) as caught:
        contradictory.eliminate(x)
    assert caught.value.labels == ("1",)
    assert caught.value.symbol == x


def test_misuse() -> None:
    with pytest.raises(UsageError):
        kinematics.eliminate(dt, x_1, using="2.7")
    with pytest.raises(UsageError):
        kinematics.eliminate()
    with pytest.raises(UsageError):
        kinematics.eliminate(dt, using="9.9")
    with pytest.raises(UsageError):
        kinematics.isolate(dt, "9.9")


def test_undefined() -> None:
    a, v, t1 = sp.symbols("a v t1")
    with pytest.raises(Contradiction) as caught:
        System().add(sp.Eq(a, (v - x) / t1)).known(t1, 0).eliminate_zeros()
    assert "undefined" in caught.value.reason
    # Eq(a, zoo) would be `false`, so the sides are checked first.
    with pytest.raises(Contradiction) as caught:
        System().add(sp.Eq(a, 1 / t1)).known(t1, 0).eliminate_zeros()
    assert "undefined" in caught.value.reason


@pytest.mark.parametrize("value", [sp.oo, sp.nan, sp.zoo, -sp.oo, float("inf")])
def test_known_refuses_infinities(value: sp.Expr | float) -> None:
    with pytest.raises(UsageError):
        System().known(x, value)
