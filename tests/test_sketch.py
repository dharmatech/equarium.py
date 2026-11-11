"""The setup sketches, an experiment: `equarium.sketch`, and each
problem's `sketch.py` and the `sketch.svg` it writes."""

import importlib
import pkgutil
import xml.etree.ElementTree as ET

import pytest
import sympy as sp
from sympy.physics.units import hour, kilometer, meter, second

import examples
from equarium import System, UsageError
from equarium.analysis import Role
from equarium.physics import XY, Particle, X
from equarium.sketch import COLOR, quantity, sketch, split_subscript

SVG = "{http://www.w3.org/2000/svg}"


def labels(svg: str) -> dict[str, str]:
    """Each text's whole content, subscripts included, and its color."""
    root = ET.fromstring(svg)
    return {"".join(text.itertext()): text.get("fill", "") for text in root.iter(f"{SVG}text")}


@pytest.mark.parametrize(
    ("name", "split"),
    [
        ("x0", ("x", "0")),
        ("v0x", ("v", "0x")),
        ("vavx", ("v", "av-x")),
        ("ax", ("a", "x")),
        ("Δt", ("Δt", "")),
        ("Δt01", ("Δt", "01")),
        ("t", ("t", "")),
        ("m01.a.mag", ("m", "01.a.mag")),
    ],
)
def test_split_subscript(name: str, split: tuple[str, str]) -> None:
    assert split_subscript(name) == split


@pytest.mark.parametrize(
    ("value", "text"),
    [
        (sp.Integer(5), "5"),
        (4 * meter / second**2, "4 m/s²"),
        (5 * meter, "5 m"),
        (sp.Float(28.0) * second, "28.0 s"),
        (105 * kilometer / hour, "105 km/h"),
        (sp.Symbol("g") * meter, "meter*g"),  # not a number: as SymPy prints it
    ],
)
def test_quantity(value: sp.Expr, text: str) -> None:
    assert quantity(value) == text


def test_a_sketch_labels_knowns_wants_and_unknowns() -> None:
    m = Particle("m", 2, X)
    m0, m1 = m.states
    m01 = m.edge(0, 1)
    part = (
        System()
        .add(*m.kinematics())
        .add(*m01.constant_acceleration())
        .known(m0.t, 0)
        .known(m01.a.x, 4 * meter / second**2)
        .known(m0.pos.x, 5 * meter)
        .known(m0.vel.x, 15 * meter / second)
        .known(m1.t, 2 * second)
        .want(m1.pos.x, m1.vel.x)
    )
    found = labels(sketch(m, ("(a)", part)))
    assert found["(a)"]
    assert found["x0 = 5 m"] == COLOR[Role.KNOWN]
    assert found["ax = 4 m/s²"] == COLOR[Role.KNOWN]
    assert found["t1 = 2 s"] == COLOR[Role.KNOWN]
    assert found["x1 = ?"] == COLOR[Role.WANT]
    assert found["v1x = ?"] == COLOR[Role.WANT]
    assert found["Δt"] == COLOR[Role.UNKNOWN]
    assert found["vav-x"] == COLOR[Role.UNKNOWN]


def test_a_sketch_leaves_out_symbols_the_system_doesnt_have() -> None:
    m = Particle("m", 2, X)
    m0, m1 = m.states
    part = System().add(sp.Eq(m1.pos.x, m0.pos.x)).known(m0.pos.x, 5).want(m1.pos.x)
    found = labels(sketch(m, ("only x", part)))
    assert "x0 = 5" in found and "x1 = ?" in found
    assert not any(text.startswith(("t", "v", "Δt", "a")) for text in found)


def test_a_sketch_needs_the_x_axis_and_a_part() -> None:
    m = Particle("m", 2, X)
    d = Particle("d", 2, XY)
    with pytest.raises(UsageError, match="x axis only"):
        sketch(d, ("(a)", System()))  # pyright: ignore[reportArgumentType]
    with pytest.raises(UsageError, match="needs a part"):
        sketch(m)


def sketch_modules() -> list[str]:
    """Each problem folder's `sketch` module, such as
    `examples.up_15e.ch02.examples.n04.sketch`."""
    return sorted(
        info.name
        for info in pkgutil.walk_packages(examples.__path__, prefix="examples.")
        if not info.ispkg and info.name.rsplit(".", 1)[-1] == "sketch"
    )


def test_the_sketches_are_found() -> None:
    assert "examples.up_15e.ch02.examples.n04.sketch" in sketch_modules()


@pytest.mark.parametrize("name", sketch_modules())
def test_the_written_sketch_is_todays(name: str) -> None:
    # Rewrite it with `uv run python -m <name>`.
    module = importlib.import_module(name)
    assert module.SVG.read_text() == module.draw()
