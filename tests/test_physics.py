"""The physics layer: `Var`'s identity, the names, the misuses, the
kinematics equations, vectors and their equations, polar, events and
their links, the projectile setup, Newton's second law and the mass, and
the book's notation. Also the old physics code's copy, until increment
007 deletes it, and the layers."""

import pickle
import re
import subprocess
import sys
from typing import Any, cast

import pytest
import sympy as sp

from equarium import System, UsageError
from equarium.analysis import Role
from equarium.display import GREEN, RED, RESET, render, render_solution
from equarium.physics import (
    XY,
    BookNotation,
    Edge,
    Event,
    Particle,
    Setup,
    State,
    Var,
    Vec,
    Vector,
    X,
    Y,
)
from equarium.physics.kinematics_states import (
    kinematics_fundamental,
    magnitude_and_angle_equations,
    make_point,
    make_states_model,
)
from equarium.physics.newtons_laws import newtons_second_law, superposition_equations
from examples.up_15e.ch02.examples.n04.main import sol_a
from examples.up_15e.ch02.examples.n05.main import sol as sol_2_5
from old_names import old_str

m = Particle("m", 2, X)
m0, m1 = m.states
m01 = m.edge(0, 1)

F1, F2, F3, R = Vector("F1", XY), Vector("F2", XY), Vector("F3", XY), Vector("R", XY)
d0, d1 = Particle("d", 2, XY).states

# 2.5's meeting, in X, and 3.10's hit, in XY.
p1 = Particle("p", 2, X).states[1]
meet = Event("meet", m1, p1)
hit = Event("hit", d1, Particle("m", 2, XY).states[1])


# Var's identity


def test_equal_particles_give_equal_symbols() -> None:
    again = Particle("m", 2, X)
    assert again == m and hash(again) == hash(m)
    assert again.states == m.states and hash(again.states[0]) == hash(m0)
    assert again.edge(0, 1) == m01 and hash(again.edge(0, 1)) == hash(m01)
    symbol = again.states[0].pos.x
    assert symbol == m0.pos.x and hash(symbol) == hash(m0.pos.x)
    assert again.edge(0, 1).a.x == m01.a.x


def test_a_var_is_its_structure() -> None:
    assert Var("m", "0", "pos", "x") == m0.pos.x
    assert hash(Var("m", "0", "pos", "x")) == hash(m0.pos.x)


def test_a_plain_symbol_with_the_same_name_differs() -> None:
    assert sp.Symbol("m0.pos.x") != m0.pos.x


def test_a_var_that_prints_alike_differs() -> None:
    other = Var("m0", "", "pos", "x")
    assert str(other) == "m0.pos.x"
    assert other != m0.pos.x


def test_pickling_round_trips() -> None:
    symbol = pickle.loads(pickle.dumps(m01.a.x))
    assert isinstance(symbol, Var)
    assert (symbol.owner, symbol.where, symbol.path) == ("m", "01", ("a", "x"))
    assert symbol == m01.a.x
    eq = m.kinematics()[2]
    assert pickle.loads(pickle.dumps(eq)) == eq


def test_different_particles_differ() -> None:
    assert Particle("m", 2, X) != Particle("p", 2, X)
    assert Particle("m", 2, X) != Particle("m", 3, X)
    assert Particle("m", 2, X) != Particle("m", 2, XY)


# Names


def test_names() -> None:
    y0 = Particle("m", 2, Y).states[0]
    p12 = Particle("p", 3, X).edge(1, 2)
    assert [s.name for s in (m0.pos.x, y0.vel.y, m1.t, m01.dt, m01.a.x, m01.v_av.x)] == [
        "m0.pos.x",
        "m0.vel.y",
        "m1.t",
        "m01.dt",
        "m01.a.x",
        "m01.v_av.x",
    ]
    assert p12.dt.name == "p12.dt"


def test_states_and_edges() -> None:
    p = Particle("p", 3, X)
    assert p.states == (State("p", 0, X), State("p", 1, X), State("p", 2, X))
    assert p.edges == (p.edge(0, 1), p.edge(1, 2))
    assert p.edge(1, 2) == Edge(State("p", 1, X), State("p", 2, X))
    assert p.edge(1, 2).where == "12"


def test_components_follow_the_axes() -> None:
    d01 = Particle("d", 2, XY).edge(0, 1)
    assert d01.a.components == (d01.a.x, d01.a.y)
    assert m0.pos.components == (m0.pos.x,)
    assert Vector("m", X, "0", ("pos",)) == m0.pos


def test_a_lone_vector() -> None:
    assert [s.name for s in (F1.x, F1.y, F1.mag)] == ["F1.x", "F1.y", "F1.mag"]
    assert F1.x == Var("F1", "", "x")
    again = Vector("F1", XY)
    assert again == F1 and hash(again) == hash(F1)
    assert again.mag == F1.mag


def test_the_polar_parts_names() -> None:
    xy0 = Particle("m", 2, XY).states[0]
    symbols = (xy0.vel.mag, xy0.vel.angle, xy0.vel.angle_deg, xy0.pos.mag, F1.angle)
    assert [s.name for s in symbols] == [
        "m0.vel.mag",
        "m0.vel.angle",
        "m0.vel.angle_deg",
        "m0.pos.mag",
        "F1.angle",
    ]


# Misuses


@pytest.mark.parametrize("name", ["p2", "m.x", "", "2m"])
def test_a_bad_name_raises(name: str) -> None:
    with pytest.raises(UsageError, match="name"):
        Particle(name, 2, X)


@pytest.mark.parametrize("name", ["m.x", "", "2F", "F 1"])
def test_a_bad_vector_name_raises(name: str) -> None:
    with pytest.raises(UsageError, match="name"):
        Vector(name, XY)


@pytest.mark.parametrize("states", [1, 11])
def test_two_to_ten_states(states: int) -> None:
    with pytest.raises(UsageError, match="2 to 10 states"):
        Particle("m", states, X)


def test_edges_join_consecutive_states_only() -> None:
    with pytest.raises(UsageError, match="from 0 to 2"):
        Particle("p", 3, X).edge(0, 2)
    with pytest.raises(UsageError, match="from 1 to 2"):
        m.edge(1, 2)


def test_an_axis_the_vector_doesnt_have_raises() -> None:
    # Through getattr, so pyright doesn't see the misuse here.
    with pytest.raises(UsageError, match="m0.pos is in X, so it has no y"):
        getattr(m0.pos, "y")
    b0 = Particle("b", 2, Y).states[0]
    with pytest.raises(UsageError, match="b0.vel is in Y, so it has no x"):
        getattr(b0.vel, "x")


def test_vector_misuses_raise() -> None:
    # Through getattr, or with an operand cast to Any, so pyright doesn't
    # see the misuse here.
    f = Vector("f", X)
    with pytest.raises(UsageError, match="f is in X, so it has no mag"):
        getattr(f, "mag")
    with pytest.raises(UsageError, match="f is in X, so it has no mag"):
        getattr(f, "from_polar")()
    with pytest.raises(UsageError, match="f is in X, so it has no angle_deg"):
        getattr(f, "degrees")()
    with pytest.raises(UsageError, match=re.escape("F1 + f: F1 is in XY, but f is in X")):
        _ = F1 + cast(Any, f)
    with pytest.raises(UsageError, match=re.escape("F1 - f: F1 is in XY, but f is in X")):
        _ = F1 - cast(Any, f)
    with pytest.raises(UsageError, match=re.escape("R.eq(f): R is in XY, but f is in X")):
        R.eq(cast(Any, f))
    with pytest.raises(UsageError, match=re.escape("F1 + 1: 1 isn't a vector")):
        _ = F1 + cast(Any, 1)
    with pytest.raises(UsageError, match=re.escape("1 + F1: 1 isn't a vector")):
        _ = cast(Any, 1) + F1
    with pytest.raises(UsageError, match=re.escape("F1 * F2: F2 isn't a scalar")):
        _ = F1 * cast(Any, F2)


# The kinematics


def test_kinematics_of_two_states() -> None:
    assert [str(eq) for eq in m.kinematics()] == [
        "Eq(m01.dt, -m0.t + m1.t)",
        "Eq(m01.v_av.x, (-m0.pos.x + m1.pos.x)/m01.dt)",
        "Eq(m01.a.x, (-m0.vel.x + m1.vel.x)/m01.dt)",
        "Eq(m01.v_av.x, m0.vel.x/2 + m1.vel.x/2)",
    ]


def test_kinematics_of_three_states_in_the_old_order() -> None:
    assert [str(eq) for eq in Particle("p", 3, X).kinematics()] == [
        "Eq(p01.dt, -p0.t + p1.t)",
        "Eq(p12.dt, -p1.t + p2.t)",
        "Eq(p01.v_av.x, (-p0.pos.x + p1.pos.x)/p01.dt)",
        "Eq(p12.v_av.x, (-p1.pos.x + p2.pos.x)/p12.dt)",
        "Eq(p01.a.x, (-p0.vel.x + p1.vel.x)/p01.dt)",
        "Eq(p12.a.x, (-p1.vel.x + p2.vel.x)/p12.dt)",
        "Eq(p01.v_av.x, p0.vel.x/2 + p1.vel.x/2)",
        "Eq(p12.v_av.x, p1.vel.x/2 + p2.vel.x/2)",
    ]


def test_kinematics_renamed_back_are_the_old_copys() -> None:
    # Uses the old copy, so increment 007 deletes it with the copy.
    new = [old_str(eq) for eq in Particle("m", 2, Y).kinematics()]
    old = [str(eq) for eq in kinematics_fundamental(make_states_model("m", 2), axes=("y",))]
    assert new == old
    new = [old_str(eq) for eq in Particle("m", 3, XY).kinematics()]
    old = [str(eq) for eq in kinematics_fundamental(make_states_model("m", 3), axes=("x", "y"))]
    assert new == old


# Vectors: the arithmetic, `.eq` and polar


def test_vectors_add_subtract_and_scale() -> None:
    k = sp.Symbol("m")
    total = (F1.x + F2.x + F3.x, F1.y + F2.y + F3.y)
    results = [
        (F1 + F2, (F1.x + F2.x, F1.y + F2.y)),
        (F1 - F2, (F1.x - F2.x, F1.y - F2.y)),
        (-F1, (-F1.x, -F1.y)),
        (2 * F1, (2 * F1.x, 2 * F1.y)),
        (F1 * k, (k * F1.x, k * F1.y)),
        (k * F1, (k * F1.x, k * F1.y)),  # SymPy gives way to Vector.__rmul__
        ((F1 + F2) + F3, total),  # a Vec and a Vector mix
        (F3 + (F1 + F2), total),
    ]
    for result, components in results:
        assert isinstance(result, Vec)
        assert result.axes is XY
        assert result.components == components


def test_sum_adds_vectors() -> None:
    assert sum([F1, F2, F3]) == F1 + F2 + F3


def test_eq_makes_one_equation_per_axis() -> None:
    F, n, w, a = Vector("F", XY), Vector("n", XY), Vector("w", XY), Vector("a", XY)
    k = sp.Symbol("m")
    assert [str(eq) for eq in R.eq(F1 + F2 + F3)] == [
        "Eq(R.x, F1.x + F2.x + F3.x)",
        "Eq(R.y, F1.y + F2.y + F3.y)",
    ]
    assert [str(eq) for eq in (F + n + w).eq(a * k)] == [
        "Eq(F.x + n.x + w.x, m*a.x)",
        "Eq(F.y + n.y + w.y, m*a.y)",
    ]


def test_polar_one_way_each() -> None:
    assert [str(eq) for eq in d0.vel.from_polar()] == [
        "Eq(d0.vel.x, d0.vel.mag*cos(d0.vel.angle))",
        "Eq(d0.vel.y, d0.vel.mag*sin(d0.vel.angle))",
    ]
    assert [str(eq) for eq in d0.vel.to_polar()] == [
        "Eq(d0.vel.mag, sqrt(d0.vel.x**2 + d0.vel.y**2))",
        "Eq(d0.vel.angle, atan2(d0.vel.y, d0.vel.x))",
    ]
    assert [str(eq) for eq in d0.vel.degrees()] == ["Eq(d0.vel.angle_deg, 180*d0.vel.angle/pi)"]


def test_vector_equations_renamed_back_are_the_old_copys() -> None:
    # Uses the old copy, so increment 007 deletes it with the copy.
    new = [old_str(eq) for eq in (*d0.vel.from_polar(), *d0.vel.to_polar())]
    old = [str(eq) for eq in magnitude_and_angle_equations(make_states_model("d", 2).states[0])]
    assert new == old

    F, n, w, a = Vector("F", XY), Vector("n", XY), Vector("w", XY), Vector("a", XY)
    k = sp.Symbol("m")
    new = [old_str(eq) for eq in (F + n + w).eq(a * k)]
    forces = [make_point("F"), make_point("n"), make_point("w")]
    old = [str(eq) for eq in newtons_second_law(forces, k, make_point("a"))]
    assert new == old

    new = [old_str(eq) for eq in R.eq(F1 + F2 + F3)]
    forces = [make_point("F1"), make_point("F2"), make_point("F3")]
    old = [str(eq) for eq in superposition_equations(make_point("R"), forces)]
    assert new == old


# Events


def test_an_events_symbols() -> None:
    assert [s.name for s in (meet.t, meet.pos.x)] == ["meet.t", "meet.pos.x"]
    assert meet.t == Var("meet", "", "t")
    assert meet.pos == Vector("meet", X, "", ("pos",))
    assert meet.axes is X
    again = Event("meet", m1, p1)
    assert again == meet and hash(again) == hash(meet)
    assert again.t == meet.t and again.pos.x == meet.pos.x


def test_an_events_equations() -> None:
    assert [str(eq) for eq in meet.equations()] == [
        "Eq(m1.t, meet.t)",
        "Eq(p1.t, meet.t)",
        "Eq(m1.pos.x, meet.pos.x)",
        "Eq(p1.pos.x, meet.pos.x)",
    ]


def test_an_events_equations_on_the_axes_chosen() -> None:
    assert [str(eq) for eq in hit.equations(Y)] == [
        "Eq(d1.t, hit.t)",
        "Eq(m1.t, hit.t)",
        "Eq(d1.pos.y, hit.pos.y)",
        "Eq(m1.pos.y, hit.pos.y)",
    ]
    assert [str(eq) for eq in hit.equations(X)[2:]] == [
        "Eq(d1.pos.x, hit.pos.x)",
        "Eq(m1.pos.x, hit.pos.x)",
    ]
    # All the axes by default: the time, then x, then y.
    assert hit.equations() == hit.equations(X) + hit.equations(Y)[2:]
    assert hit.equations(XY) == hit.equations()


def test_event_misuses_raise() -> None:
    # The mixed axes with a state cast to Any, so pyright doesn't see the
    # misuse here. It doesn't check `axes=` against the event's.
    for name in ("e2", "m.x", ""):
        message = (
            f"an event's name is a Python identifier that doesn't end in a digit, not {name!r}"
        )
        with pytest.raises(UsageError, match=re.escape(message)):
            Event(name, m1, p1)
    with pytest.raises(UsageError, match="meet needs two or more states, not 1"):
        Event("meet", m1)
    with pytest.raises(UsageError, match="hit: m1 is in X, but d1 is in XY"):
        Event("hit", m1, cast(Any, d1))
    with pytest.raises(UsageError, match="meet has a state twice"):
        Event("meet", m1, p1, m1)
    with pytest.raises(UsageError, match="meet is in X, so it has no y"):
        meet.equations(Y)


# The projectile setup


def test_the_projectile_setup() -> None:
    g = sp.Symbol("g")
    d01 = Particle("d", 2, XY).edge(0, 1)
    flight = d01.projectile(g)
    assert isinstance(flight, Setup)
    assert [str(eq) for eq in flight.equations] == ["Eq(d01.a.y, -g)", "Eq(d0.vel.x, d1.vel.x)"]
    assert flight.knowns == {d01.a.x: 0}
    equations, knowns = flight  # a named tuple
    assert (equations, knowns) == (flight.equations, flight.knowns)
    assert d01.projectile(g) == flight


def test_the_projectile_setup_of_a_later_edge() -> None:
    g = sp.Symbol("g")
    p12 = Particle("p", 3, XY).edge(1, 2)
    flight = p12.projectile(g)
    assert [str(eq) for eq in flight.equations] == ["Eq(p12.a.y, -g)", "Eq(p1.vel.x, p2.vel.x)"]
    assert flight.knowns == {p12.a.x: 0}


def test_the_projectile_setup_goes_into_a_system() -> None:
    g = sp.Symbol("g")
    d = Particle("d", 2, XY)
    d01 = d.edge(0, 1)
    flight = d01.projectile(g)
    system = System().add(*d.kinematics()).add(*flight.equations).known(flight.knowns)
    assert [e.label for e in system.equations[-2:]] == ["8", "9"]
    assert dict(system.knowns) == {d01.a.x: 0}
    # The zero goes into (4): 0 = (v1x - v0x)/Δt.
    assert str(system.eliminate_zeros().equation("4").eq) == "Eq(0, (-d0.vel.x + d1.vel.x)/d01.dt)"


def test_the_projectile_setup_needs_xy() -> None:
    # Through getattr, so pyright doesn't see the misuse here.
    g = sp.Symbol("g")
    with pytest.raises(UsageError, match="m01 is in X, so it has no projectile setup"):
        getattr(m01, "projectile")(g)
    b01 = Particle("b", 2, Y).edge(0, 1)
    with pytest.raises(UsageError, match="b01 is in Y, so it has no projectile setup"):
        getattr(b01, "projectile")(g)


# Newton's second law, and the mass


def test_a_particles_mass() -> None:
    b = Particle("b", 2, X)
    assert b.mass.name == "b.mass"
    assert b.mass == Var("b", "", "mass")
    assert sp.Symbol("b.mass") != b.mass
    # The name is the identity: the same mass, whatever the states and axes.
    assert Particle("b", 3, XY).mass == b.mass
    assert Particle("box", 2, XY).mass != b.mass


def test_newton_on_an_edge() -> None:
    b = Particle("b", 2, X)
    b01 = b.edge(0, 1)
    n, w, f = Vector("n", X), Vector("w", X), Vector("f", X)
    (eq,) = b01.newton(n, w, f)
    assert str(eq) == "Eq(f.x + n.x + w.x, b.mass*b01.a.x)"
    # The particle's mass and the edge's own acceleration.
    assert eq.rhs == b.mass * b01.a.x
    assert b01.newton(n, w, f) == b.edge(0, 1).newton(f, w, n)


def test_newton_makes_one_equation_per_axis() -> None:
    box = Particle("box", 2, XY)
    F, n, w = Vector("F", XY), Vector("n", XY), Vector("w", XY)
    assert [str(eq) for eq in box.edge(0, 1).newton(F, n, w)] == [
        "Eq(F.x + n.x + w.x, box.mass*box01.a.x)",
        "Eq(F.y + n.y + w.y, box.mass*box01.a.y)",
    ]
    c01 = Particle("c", 2, Y).edge(0, 1)
    assert [str(eq) for eq in c01.newton(Vector("w", Y))] == ["Eq(w.y, c.mass*c01.a.y)"]


def test_newton_of_a_later_edge_and_of_a_vector_expression() -> None:
    p = Particle("p", 3, X)
    f, n = Vector("f", X), Vector("n", X)
    assert [str(eq) for eq in p.edge(1, 2).newton(f)] == ["Eq(f.x, p.mass*p12.a.x)"]
    # A vector expression is a force too.
    assert [str(eq) for eq in p.edge(0, 1).newton(f, -n)] == ["Eq(f.x - n.x, p.mass*p01.a.x)"]


def test_newton_with_the_kinematics_needs_no_link() -> None:
    # 4.5's shape: (3), the book's 2.7, and (5), Newton's second law, have
    # the same acceleration, so f.x comes out with no equation to link them.
    b = Particle("b", 2, X)
    b0, b1 = b.states
    b01 = b.edge(0, 1)
    f = Vector("f", X)
    system = System().add(*b.kinematics()).add(*b01.newton(f))
    assert [e.label for e in system.equations] == ["1", "2", "3", "4", "5"]
    assert str(system.equation("3").eq) == "Eq(b01.a.x, (-b0.vel.x + b1.vel.x)/b01.dt)"
    assert str(system.equation("5").eq) == "Eq(f.x, b.mass*b01.a.x)"
    sol = system.known({b.mass: 2, b0.vel.x: 0, b1.vel.x: 6, b0.t: 0, b1.t: 3}).solve(f.x)
    assert str(sol.formula(f.x)) == "b.mass*(b0.vel.x - b1.vel.x)/(b0.t - b1.t)"
    assert float(sol.number(f.x)) == 4.0  # as a float, since Float(4) == 4 is false


def test_newton_misuses_raise() -> None:
    # With a force cast to Any, so pyright doesn't see the misuse here.
    f = Vector("f", X)
    d01 = Particle("d", 2, XY).edge(0, 1)
    message = "m01.newton(f, F1): m01 is in X, but F1 is in XY"
    with pytest.raises(UsageError, match=re.escape(message)):
        m01.newton(f, cast(Any, F1))
    message = "d01.newton(f): d01 is in XY, but f is in X"
    with pytest.raises(UsageError, match=re.escape(message)):
        d01.newton(cast(Any, f))
    message = "m01.newton((-F1.x, -F1.y)): m01 is in X, but (-F1.x, -F1.y) is in XY"
    with pytest.raises(UsageError, match=re.escape(message)):
        m01.newton(cast(Any, -F1))
    with pytest.raises(UsageError, match=re.escape("m01.newton(f, f.x): f.x isn't a vector")):
        m01.newton(f, cast(Any, f.x))
    with pytest.raises(UsageError, match=re.escape("m01.newton() needs one or more forces")):
        m01.newton()


def test_newton_renamed_back_is_the_old_copys() -> None:
    # Uses the old copy, so increment 007 deletes it with the copy. The old
    # code took the mass and the acceleration, here 4.4's `m` and `a`.
    box = Particle("box", 2, XY)
    box01 = box.edge(0, 1)
    F, n, w = Vector("F", XY), Vector("n", XY), Vector("w", XY)
    k, a = sp.Symbol("m"), make_point("a")
    names = {box.mass: k, box01.a.x: a.x, box01.a.y: a.y}
    new = [old_str(eq.xreplace(names)) for eq in box01.newton(F, n, w)]
    forces = [make_point("F"), make_point("n"), make_point("w")]
    old = [str(eq) for eq in newtons_second_law(forces, k, a)]
    assert new == old


# BookNotation


def test_the_book_notation_of_a_state() -> None:
    book, with_p = BookNotation(), BookNotation(owners={"m": "P"})
    y0 = Particle("m", 2, Y).states[0]
    assert [book.text(s) for s in (m0.pos.x, y0.pos.y, m0.vel.x, m0.t)] == ["x0", "y0", "v0x", "t0"]
    assert [with_p.text(s) for s in (m0.pos.x, m0.vel.x, m0.t)] == ["xP0", "vP0x", "tP0"]


def test_the_book_notation_of_an_edge() -> None:
    symbols = (m01.dt, m01.a.x, m01.v_av.x)
    assert [BookNotation().text(s) for s in symbols] == ["Δt", "ax", "vavx"]
    assert [BookNotation(owners={"m": "P"}).text(s) for s in symbols] == ["ΔtP", "aPx", "vavPx"]
    assert [BookNotation(edge_index=True).text(s) for s in symbols] == ["Δt01", "a01x", "vav01x"]
    with_both = BookNotation(owners={"m": "P"}, edge_index=True)
    assert [with_both.text(s) for s in symbols] == ["ΔtP01", "aP01x", "vavP01x"]


def test_the_book_notation_of_the_polar_parts() -> None:
    xy0 = Particle("m", 2, XY).states[0]
    symbols = (xy0.pos.mag, xy0.vel.mag, xy0.vel.angle, xy0.pos.angle)
    assert [BookNotation().text(s) for s in symbols] == ["r0", "v0", "α0", "θ0"]
    with_p = BookNotation(owners={"m": "P"})
    assert [with_p.text(s) for s in symbols] == ["rP0", "vP0", "αP0", "θP0"]


def test_the_book_notation_of_an_angle_in_degrees() -> None:
    xy0 = Particle("m", 2, XY).states[0]
    symbols = (xy0.vel.angle_deg, xy0.pos.angle_deg)
    assert [BookNotation().text(s) for s in symbols] == ["α0°", "θ0°"]
    with_p = BookNotation(owners={"m": "P"})
    assert [with_p.text(s) for s in symbols] == ["αP0°", "θP0°"]
    lone = (R.angle_deg, F1.angle_deg)
    assert [BookNotation().text(s) for s in lone] == ["θR°", "θF1°"]
    # A lone vector's name is its own: owners applies to particles.
    with_p = BookNotation(owners={"R": "P", "F1": "P"})
    assert [with_p.text(s) for s in lone] == ["θR°", "θF1°"]


def test_the_book_notation_of_a_lone_vector() -> None:
    symbols = (F1.x, F1.y, F1.mag, R.angle)
    assert [BookNotation().text(s) for s in symbols] == ["F1x", "F1y", "F1", "θR"]
    # A lone vector's name is its own: owners applies to particles.
    with_p = BookNotation(owners={"F1": "P", "R": "P"})
    assert [with_p.text(s) for s in symbols] == ["F1x", "F1y", "F1", "θR"]


def test_the_book_notation_of_an_event() -> None:
    symbols = (meet.t, meet.pos.x, hit.pos.y)
    assert [BookNotation().text(s) for s in symbols] == ["t", "x", "y"]
    # The book's plain t, x and y: owners applies to particles.
    with_p = BookNotation(owners={"meet": "P", "hit": "P"})
    assert [with_p.text(s) for s in symbols] == ["t", "x", "y"]
    assert BookNotation().text(hit.pos.mag) == "hit.pos.mag"


def test_the_book_notation_of_a_mass() -> None:
    b = Particle("b", 2, X)
    assert BookNotation().text(b.mass) == "m"
    assert BookNotation(owners={"b": "B"}).text(b.mass) == "mB"
    # Newton's second law, as the book writes it.
    system = System().add(*b.edge(0, 1).newton(Vector("n", X), Vector("w", X), Vector("f", X)))
    printed = render(system, symbol=BookNotation(color=False))
    assert printed.startswith("(1)  fx + nx + wx = m*ax\n")


def test_the_book_notation_of_other_symbols_is_the_name() -> None:
    book = BookNotation()
    assert book.text(sp.Symbol("m_v")) == "m_v"
    assert book.text(Var("m", "01", "a", "mag")) == "m01.a.mag"
    assert book.text(Var("m", "01", "a", "angle_deg")) == "m01.a.angle_deg"


def test_the_book_notation_colors_by_role() -> None:
    book = BookNotation()
    assert book(m0.pos.x, Role.KNOWN) == f"{GREEN}x0{RESET}"
    assert book(m1.pos.x, Role.WANT) == f"{RED}x1{RESET}"
    assert book(m01.dt, Role.UNKNOWN) == "Δt"
    plain = BookNotation(color=False)
    assert [plain(m0.pos.x, role) for role in Role] == ["x0", "x0", "x0"]


def test_the_book_notation_of_2_4() -> None:
    printed = render_solution(sol_a, symbol=BookNotation(color=False))
    assert printed.startswith("x1 = x0 + v0x*t1 + ax*t1**2/2\n")


def test_the_book_notation_of_2_5_with_owners() -> None:
    book = BookNotation(owners={"m": "M", "p": "P"})
    p = Particle("p", 2, X)
    assert book.text(p.edge(0, 1).a.x) == "aPx"
    assert book.text(p.states[1].vel.x) == "vP1x"
    printed = render_solution(sol_2_5, symbol=BookNotation(owners=book.owners, color=False))
    assert printed.startswith("t = 2*m_v/aPx\n")


# The old copy, and the layers


def test_the_same_equations_as_the_old_library() -> None:
    # The old library's own output, from its venv in combine-equations.py
    # (2026-11-08).
    assert [str(eq) for eq in kinematics_fundamental(make_states_model("m", 2), axes=("x",))] == [
        "Eq(dt_m_0_1, -m_0_t + m_1_t)",
        "Eq(v_av_x_m_0_1, (-m_0_x + m_1_x)/dt_m_0_1)",
        "Eq(a_x_m_0_1, (-m_0_v_x + m_1_v_x)/dt_m_0_1)",
        "Eq(v_av_x_m_0_1, m_0_v_x/2 + m_1_v_x/2)",
    ]


def test_the_core_doesnt_import_the_physics_code() -> None:
    # In a fresh interpreter, since other tests import the physics code.
    check = "import sys, equarium; print('equarium.physics' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", check], capture_output=True, text=True, check=True
    )
    assert result.stdout.strip() == "False"
