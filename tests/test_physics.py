"""The physics layer: `Var`'s identity, the names, the misuses, the
kinematics equations and the book's notation. Also the old physics code's
copy, until increment 007 deletes it, and the layers."""

import pickle
import subprocess
import sys

import pytest
import sympy as sp

from equarium import UsageError
from equarium.analysis import Role
from equarium.display import GREEN, RED, RESET, render_solution
from equarium.physics import XY, BookNotation, Edge, Particle, State, Var, Vector, X, Y
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
from examples.up_15e.ch02.examples.n04.main import sol_a
from old_names import old_str

m = Particle("m", 2, X)
m0, m1 = m.states
m01 = m.edge(0, 1)


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


# Misuses


@pytest.mark.parametrize("name", ["p2", "m.x", "", "2m"])
def test_a_bad_name_raises(name: str) -> None:
    with pytest.raises(UsageError, match="name"):
        Particle(name, 2, X)


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


def test_the_book_notation_of_other_symbols_is_the_name() -> None:
    book = BookNotation()
    assert book.text(sp.Symbol("m_v")) == "m_v"
    assert book.text(Var("F1", "", "x")) == "F1.x"
    assert book.text(Var("m", "0", "pos", "mag")) == "m0.pos.mag"


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
