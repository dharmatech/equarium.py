"""Setup sketches: a problem's model drawn as SVG, from its `System`.

An experiment, with notes in `docs/experiments/sketches/`. A sketch is
the book's "set up" step, drawn from the model:
- the axis, with the origin
- each state as a point on it, with its velocity as an arrow
- each edge as an arrow from one state to the next
- every symbol the system uses, in the book's notation

Knowns are green, with their values, wants are red, with `?`, and other
unknowns are gray, as `show()` colors them. It's a schematic, not to
scale: the states are evenly spaced, in order, right of the origin.

For now: one particle, on the x axis.
"""

from collections.abc import Iterable
from xml.sax.saxutils import escape

import sympy as sp
from sympy.physics.units import Quantity, hour, minute

from equarium.analysis import Role
from equarium.errors import UsageError
from equarium.physics import BookNotation, Particle, Var, X
from equarium.sympy_compat import free_symbols
from equarium.system import System

COLOR = {Role.KNOWN: "#1a7f37", Role.WANT: "#cf222e", Role.UNKNOWN: "#6e7781"}
INK = "#24292f"
FONT = "DejaVu Sans, Helvetica, Arial, sans-serif"
SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
ABBREVIATION: dict[Quantity, str] = {hour: "h", minute: "min"}  # SymPy's are the names

WIDTH = 760
HEIGHT = 310  # one panel
FOOTER = 36  # the legend, once, below the panels
AXIS_Y = 205  # in a panel
ORIGIN_X = 70
AXIS_END = WIDTH - 50
LINE = 21  # a label line's height


def sketch(
    particle: Particle[X],
    *parts: tuple[str, System],
    notation: BookNotation | None = None,
) -> str:
    """One panel per part, `(title, system)`, stacked, as an SVG document.

    `sketch(m, ("(a) ...", part_a), ("(b) ...", part_b))`.
    """
    if particle.axes is not X:
        raise UsageError(f"a sketch draws the x axis only, for now, not {particle.axes.names}")
    if not parts:
        raise UsageError("a sketch needs a part: sketch(m, ('(a)', part_a))")
    book = notation if notation is not None else BookNotation(color=False)
    height = HEIGHT * len(parts) + FOOTER
    body: list[str] = []
    for k, (title, system) in enumerate(parts):
        if k:
            body.append(
                f'<line x1="20" y1="{k * HEIGHT}" x2="{WIDTH - 20}" y2="{k * HEIGHT}"'
                ' stroke="#d0d7de" stroke-width="1"/>'
            )
        body.append(f'<g transform="translate(0,{k * HEIGHT})">')
        body.extend(_panel(particle, title, system, book))
        body.append("</g>")
    body.append(f'<g transform="translate(0,{height - 14})">')
    body.extend(_legend())
    body.append("</g>")
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}"'
            f' viewBox="0 0 {WIDTH} {height}" font-family="{FONT}" font-size="15">',
            _markers(),
            f'<rect width="{WIDTH}" height="{height}" fill="#ffffff"/>',
            *body,
            "</svg>",
            "",
        ]
    )


def _panel(particle: Particle[X], title: str, system: System, book: BookNotation) -> list[str]:
    used = _used(system)
    out = [
        _text(20, 30, title, INK, weight="bold", size=16),
        *_axis(),
    ]
    states = particle.states
    span = AXIS_END - 60 - (ORIGIN_X + 130)
    step = span / max(len(states) - 1, 1)
    xs = [ORIGIN_X + 130 + i * step for i in range(len(states))]

    for edge, (x0, x1) in zip(particle.edges, zip(xs, xs[1:])):
        syms = [s for s in (edge.dt, *edge.a.components, *edge.v_av.components) if s in used]
        out.extend(_edge(x0, x1, [_label(s, system, book) for s in syms]))

    for state, x in zip(states, xs):
        (vx,) = state.vel.components
        syms = [s for s in (state.t, *state.pos.components, vx) if s in used]
        out.extend(_state(x, f"state {state.index}", _velocity(vx, system), [_label(s, system, book) for s in syms]))
    return out


def _used(system: System) -> frozenset[sp.Symbol]:
    """Every symbol the system has: its knowns, its wants, and those in its equations."""
    syms: set[sp.Symbol] = set(system.knowns) | set(system.wants)
    for equation in system.equations:
        syms |= free_symbols(equation.eq)
    return frozenset(syms)


def _role(sym: sp.Symbol, system: System) -> Role:
    if sym in system.knowns:
        return Role.KNOWN
    if sym in system.wants:
        return Role.WANT
    return Role.UNKNOWN


type Label = tuple[str, str, str, Role]  # the letter, its subscript, the rest, the role


def _label(sym: Var, system: System, book: BookNotation) -> Label:
    """`x0 = 5 m` for a known, `x1 = ?` for a want, `t1` for another
    unknown, with the book's subscript split off the letter."""
    letter, subscript = split_subscript(book.text(sym))
    role = _role(sym, system)
    match role:
        case Role.KNOWN:
            value = system.knowns[sym]
            rest = "" if value is None else f" = {quantity(value)}"
        case Role.WANT:
            rest = " = ?"
        case Role.UNKNOWN:
            rest = ""
    return (letter, subscript, rest, role)


LETTERS = ("Δt", "vav", "θ", "α", "v", "a", "t", "x", "y", "r", "m")


def split_subscript(name: str) -> tuple[str, str]:
    """The book's glued name as a letter and its subscript: `v0x` is `v`
    and `0x`, `Δt01` is `Δt` and `01`, and `vavx` is `v` and `av-x`, as
    the book prints the average velocity. A name with no known letter,
    or nothing after it, has no subscript."""
    for letter in LETTERS:
        if name.startswith(letter) and len(name) > len(letter):
            rest = name[len(letter) :]
            if letter == "vav":
                return ("v", f"av-{rest}")
            return (letter, rest)
    return (name, "")


def _velocity(vx: Var, system: System) -> tuple[int, Role]:
    """The velocity arrow's direction, +1 or -1, and its role. An unknown
    velocity points right: a guess, which the arrow's dashes say."""
    role = _role(vx, system)
    value = system.knowns.get(vx)
    if role is Role.KNOWN and value is not None and value.is_number and bool(value < 0):
        return (-1, role)
    return (1, role)


def quantity(value: sp.Expr) -> str:
    """A value as the book prints it: `4 m/s²`, `5 m`, `2.0 s`, or `15`
    with no units. Anything else prints as SymPy prints it."""
    number, unit = value.as_coeff_Mul()
    if not number.is_number:
        return sp.sstr(value)
    text = sp.sstr(number, full_prec=False)
    if unit == 1:
        return text
    above: list[str] = []
    below: list[str] = []
    for factor in sp.Mul.make_args(unit):
        base, power = factor.as_base_exp()
        if not isinstance(base, Quantity) or not power.is_Integer:
            return sp.sstr(value)
        side = above if power > 0 else below
        n = abs(int(power))
        abbrev = ABBREVIATION.get(base, str(base.abbrev))
        side.append(abbrev + ("" if n == 1 else str(n).translate(SUPERSCRIPT)))
    units = "·".join(above) or "1"
    if below:
        units += "/" + "·".join(below)
    return f"{text} {units}"


def _axis() -> list[str]:
    return [
        f'<line x1="{ORIGIN_X - 30}" y1="{AXIS_Y}" x2="{AXIS_END}" y2="{AXIS_Y}"'
        f' stroke="{INK}" stroke-width="1.5" marker-end="url(#arrow-ink)"/>',
        f'<line x1="{ORIGIN_X}" y1="{AXIS_Y - 8}" x2="{ORIGIN_X}" y2="{AXIS_Y + 8}"'
        f' stroke="{INK}" stroke-width="1.5"/>',
        _text(ORIGIN_X, AXIS_Y + 28, "O", INK, anchor="middle"),
        _text(AXIS_END + 8, AXIS_Y + 5, "x", INK, style="italic", size=17),
    ]


def _state(x: float, caption: str, velocity: tuple[int, Role], labels: list[Label]) -> list[str]:
    direction, role = velocity
    dash = ' stroke-dasharray="5 4"' if role is not Role.KNOWN else ""
    out = [
        f'<line x1="{x}" y1="{AXIS_Y - 24}" x2="{x + 52 * direction}" y2="{AXIS_Y - 24}"'
        f' stroke="{COLOR[role]}" stroke-width="2.5"{dash}'
        f' marker-end="url(#arrow-{role.name.lower()})"/>',
        f'<circle cx="{x}" cy="{AXIS_Y}" r="6" fill="{INK}"/>',
        _text(x, AXIS_Y + 26, caption, COLOR[Role.UNKNOWN], anchor="middle", size=13, style="italic"),
    ]
    for i, label in enumerate(labels):
        out.append(_rich(x, AXIS_Y + 50 + i * LINE, label))
    return out


def _edge(x0: float, x1: float, labels: list[Label]) -> list[str]:
    """An arc above the axis from one state to the next, its symbols above it."""
    y = AXIS_Y - 50
    mid = (x0 + x1) / 2
    out = [
        f'<path d="M {x0 + 10} {y} Q {mid} {y - 70} {x1 - 10} {y}" fill="none"'
        f' stroke="{INK}" stroke-width="1.5" marker-end="url(#arrow-ink)"/>',
    ]
    top = y - 35 - 16  # the arc's apex is halfway to its control point
    for i, label in enumerate(reversed(labels)):
        out.append(_rich(mid, top - i * LINE, label))
    return out


def _legend() -> list[str]:
    y = 0
    items = [("known", Role.KNOWN), ("want = ?", Role.WANT), ("unknown", Role.UNKNOWN)]
    out: list[str] = []
    x = 20
    for text, role in items:
        out.append(f'<rect x="{x}" y="{y - 10}" width="10" height="10" fill="{COLOR[role]}"/>')
        out.append(_text(x + 15, y, text, COLOR[role], size=12))
        x += 95
    out.append(_text(WIDTH - 20, y, "schematic, not to scale", COLOR[Role.UNKNOWN], anchor="end", size=12, style="italic"))
    return out


def _markers() -> str:
    colors: Iterable[tuple[str, str]] = [
        ("ink", INK),
        *((role.name.lower(), color) for role, color in COLOR.items()),
    ]
    markers = "".join(
        f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5"'
        f' markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
        for name, color in colors
    )
    return f"<defs>{markers}</defs>"


def _rich(x: float, y: float, label: Label) -> str:
    """A label, centered, with its subscript lowered and smaller."""
    letter, subscript, rest, role = label
    inner = escape(letter)
    if subscript:
        inner += f'<tspan dy="5" font-size="11">{escape(subscript)}</tspan>'
        inner += f'<tspan dy="-5">{escape(rest)}</tspan>' if rest else ""
    else:
        inner += escape(rest)
    return f'<text x="{x}" y="{y}" fill="{COLOR[role]}" text-anchor="middle">{inner}</text>'


def _text(
    x: float,
    y: float,
    text: str,
    color: str,
    *,
    anchor: str = "start",
    size: int = 15,
    weight: str = "normal",
    style: str = "normal",
) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" font-size="{size}"'
        f' font-weight="{weight}" font-style="{style}">{escape(text)}</text>'
    )
