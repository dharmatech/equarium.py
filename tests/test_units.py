"""Units: Exercise 2.23 (the airbag) and Exercise 2.3 (the trip home),
in two steps and in one, with `Solution.in_units` and `Answer(unit=…)`,
and their refusals."""

from typing import Any

import pytest
import sympy as sp
from sympy.physics.units import hour, kilometer, meter, minute, second

from equarium import Solution, System, UsageError, eq_flat
from equarium.display import plain, render
from examples.answers import Answer


def matches(*answers: Answer) -> None:
    mismatches = [message for answer in answers if (message := answer.mismatch()) is not None]
    assert not mismatches, "\n".join(mismatches)


def kinematics(o: str) -> list[sp.Basic]:
    """The four equations for an object `o` in one dimension, in 003's
    3.10 scheme of symbols and the old physics code's order."""
    o_dt, o0t, o1t, o0x, o1x, o0vx, o1vx, o_vav_x, o_a_x = sp.symbols(
        f"{o}_dt {o}0t {o}1t {o}0x {o}1x {o}0vx {o}1vx {o}_vav_x {o}_a_x"
    )
    return [
        sp.Eq(o_dt, o1t - o0t),
        sp.Eq(o_vav_x, (o1x - o0x) / o_dt),  # 2.2
        sp.Eq(o_a_x, (o1vx - o0vx) / o_dt),  # 2.7
        sp.Eq(o_vav_x, (o0vx + o1vx) / 2),  # 2.10
    ]


# 2.23: an airbag stops a body from 105 km/h at 250 m/s². Over what
# distance? The book's answer is 1.70 m.

b_a_x, b0vx, b1vx, b0t, b0x, b1x = sp.symbols("b_a_x b0vx b1vx b0t b0x b1x")

airbag = (
    System()
    .add(*kinematics("b"))
    .known(b_a_x, -250 * meter / second**2)
    .known(b0vx, 105 * kilometer / hour)
    # Zeros left as values, not eliminated, as in the old script.
    .known(b1vx, 0 * meter / second)
    .known(b0t, 0 * second)
    .known(b0x, 0 * meter)
)
stopped = airbag.want(b1x).solve()


def test_2_23_render() -> None:
    lines = render(airbag, symbol=plain).splitlines()
    assert [line for line in lines if line.startswith("knowns: ")] == [
        "knowns: b_a_x = -250*meter/second**2, b0vx = 105*kilometer/hour,"
        " b1vx = 0, b0t = 0, b0x = 0"
    ]


def test_2_23_solve() -> None:
    assert len(stopped.roots) == 1
    assert str(stopped.formula(b1x)) == "(-b0vx**2 + 2*b0x*b_a_x + b1vx**2)/(2*b_a_x)"
    assert str(stopped.number(b1x)) == "22.05*kilometer**2*second**2/(hour**2*meter)"


def test_2_23_in_units() -> None:
    converted = stopped.in_units(meter, second)
    assert str(converted.number(b1x)) == "1.70138888888889*meter"
    assert converted.formula(b1x) == stopped.formula(b1x)
    assert converted.system is stopped.system
    assert converted.elapsed == stopped.elapsed
    assert converted.reason is None


def test_2_23_matches_the_book() -> None:
    matches(Answer(stopped.in_units(meter, second), b1x, "1.70", unit=meter))


def test_2_23_a_number_in_kilometers_doesnt_match_meters() -> None:
    answer = Answer(stopped.in_units(kilometer, second), b1x, "1.70", unit=meter)
    assert answer.mismatch() == (
        "b1x: printed 1.70, found 0.00170138888888889*kilometer, which isn't in meter"
    )


def test_2_23_the_wrong_dimension_doesnt_match() -> None:
    answer = Answer(stopped.in_units(meter, second), b1x, "1.70", unit=second)
    assert answer.mismatch() == (
        "b1x: printed 1.70, found 1.70138888888889*meter, which isn't in second"
    )


def test_2_23_an_unconverted_number_doesnt_match() -> None:
    message = Answer(stopped, b1x, "1.70", unit=meter).mismatch()
    assert message is not None and message.endswith(", which isn't in meter")


def test_2_23_units_without_unit_dont_match() -> None:
    message = Answer(stopped.in_units(meter, second), b1x, "1.70").mismatch()
    assert message == (
        "b1x: printed 1.70, found 1.70138888888889*meter, which has units: give unit="
    )


def test_2_23_a_filter_with_units() -> None:
    converted = stopped.in_units(meter, second)
    assert converted.where(b1x > 0).roots == converted.roots


# 2.3: the usual trip home takes 1 h 50 min at 105 km/h, and the slow
# one goes the same distance at 70 km/h. How much longer does it take?
# The book's answer is 55 min.

ca0t, ca1t, ca0x, ca1x, ca_vav_x = sp.symbols("ca0t ca1t ca0x ca1x ca_vav_x")
cb0t, cb1t, cb0x, cb1x, cb_vav_x = sp.symbols("cb0t cb1t cb0x cb1x cb_vav_x")
longer = sp.Symbol("longer")

USUAL = {
    ca0t: 0 * hour,
    ca1t: hour + sp.Rational(50, 60) * hour,
    ca0x: 0 * kilometer,
    ca_vav_x: 105 * kilometer / hour,
}
SLOW = {
    cb0t: 0 * hour,
    cb0x: 0 * kilometer,
    cb_vav_x: 70 * kilometer / hour,
}


def test_2_3_two_steps() -> None:
    usual = System().add(*kinematics("ca")).known(USUAL).want(ca1x).solve()
    assert str(usual.formula(ca1x)) == "-ca0t*ca_vav_x + ca0x + ca1t*ca_vav_x"
    assert str(usual.number(ca1x)) == "192.5*kilometer"

    slow = (
        System()
        .add(*kinematics("cb"))
        .known(SLOW)
        .known(cb1x, usual.number(ca1x))  # the distance from the first trip
        .want(cb1t)
        .solve()
    )
    assert str(slow.formula(cb1t)) == "(cb0t*cb_vav_x - cb0x + cb1x)/cb_vav_x"
    in_hours = slow.in_units(hour, kilometer)
    assert str(in_hours.number(cb1t)) == "2.75*hour"
    matches(Answer(in_hours, cb1t, "2.75", unit=hour))


# One step: both trips, the same distance, and how much longer the slow
# one takes. The old script stopped at the slow trip's time.

both_trips = (
    System()
    .add(*kinematics("ca"), *kinematics("cb"))
    .add(*eq_flat(ca1x, cb1x, longer, cb1t - ca1t))
    .known(USUAL)
    .known(SLOW)
)


def test_2_3_one_step_the_slow_trips_time() -> None:
    sol = both_trips.solve(cb1t)
    assert str(sol.formula(cb1t)) == (
        "(-ca0t*ca_vav_x + ca0x + ca1t*ca_vav_x + cb0t*cb_vav_x - cb0x)/cb_vav_x"
    )
    assert str(sol.in_units(hour, kilometer).number(cb1t)) == "2.75*hour"


def test_2_3_one_step_how_much_longer() -> None:
    sol = both_trips.solve(longer)
    assert str(sol.number(longer)) == "0.916666666666667*hour"
    in_minutes = sol.in_units(minute)
    assert str(in_minutes.number(longer)) == "55.0*minute"
    matches(Answer(in_minutes, longer, "55", unit=minute))


# What passes through `in_units` unchanged, and the refusals

x, y, z, D = sp.symbols("x y z D")
no_roots = System().add(sp.Eq(x, y + z)).want(x).solve()


def test_in_units_leaves_numbers_without_units() -> None:
    sol = System().add(sp.Eq(x, 2 * y), sp.Eq(z, 3 * D)).known(y, 3).known(D).want(x, z).solve()
    converted = sol.in_units(meter)
    assert converted == sol
    assert sp.sstr(converted.number(x), full_prec=False) == "6.0"
    assert sp.sstr(converted.number(z), full_prec=False) == "3.0*D"


def test_in_units_with_no_roots() -> None:
    assert no_roots.roots == ()
    assert no_roots.in_units(meter) is no_roots


@pytest.mark.parametrize("units", [(), (3,), (meter, 3), (3 * meter,), (x * meter,)])
def test_in_units_refuses(units: tuple[Any, ...]) -> None:
    with pytest.raises(UsageError, match="in_units"):
        stopped.in_units(*units)


def test_in_units_refuses_on_no_roots_too() -> None:
    bad: Any = 3
    with pytest.raises(UsageError, match="in_units takes units"):
        no_roots.in_units(bad)


def test_answer_refuses_a_unit_that_isnt_one() -> None:
    bad: Any = 3
    with pytest.raises(UsageError, match="unit is a unit"):
        Answer(stopped, b1x, "1.70", unit=bad)


def test_in_units_keeps_every_root() -> None:
    two = System().add(sp.Eq(x**2, y)).known(y, 4 * meter**2).want(x).solve()
    converted = two.in_units(kilometer)
    assert isinstance(converted, Solution)
    assert sorted(str(root.number(x)) for root in converted.roots) == [
        "-0.002*kilometer",
        "0.002*kilometer",
    ]
    matches(Answer(two.in_units(meter), x, "-2.0", "2.0", unit=meter))
