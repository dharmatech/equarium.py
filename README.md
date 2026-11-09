# equarium

Solve physics problems from core equations with SymPy.

Start from the fundamental equations, say what you know and what you want, and let the solver derive the rest — symbolically first, then numerically.

This is a rebuild of [combine-equations.py](https://github.com/dharmatech/combine-equations.py), using what that project taught.

## Usage

Example 2.4 of University Physics (15th ed.), with its equations written
out: a motorcycle at 15 m/s, 5 m past a signpost at t = 0, accelerating
at 4 m/s². Where is it, and how fast is it going, at t = 2 s?

```python
import sympy as sp
from equarium import System

x0, x1, v0, v1, t0, t1, v_av, a = sp.symbols("x0 x1 v0 v1 t0 t1 v_av a")

motorcycle = (
    System()
    .add(sp.Eq(v_av, (x1 - x0) / (t1 - t0)), label="2.2")
    .add(sp.Eq(a, (v1 - v0) / (t1 - t0)), label="2.7")
    .add(sp.Eq(v_av, (v0 + v1) / 2), label="2.10")
    .known(t0, 0)
    .known(x0, 5)
    .known(v0, 15)
    .known(a, 4)
    .eliminate_zeros()  # t0 drops out; the other knowns stay symbols
)

part_a = motorcycle.known(t1, 2).want(x1, v1)
sol_a = part_a.solve()
sol_a.show()
```

`show()` prints each want's formula, in terms of the knowns, then its
number (knowns in green and wants in red, in a terminal):

```
x1 = a*t1**2/2 + t1*v0 + x0
x1 = 43.0
v1 = a*t1 + v0
v1 = 23.0
```

`sol_a.number(x1)` is the number alone.

A solution can have several roots. When is the motorcycle at x = 55 m?
The quadratic gives two times, and `where` keeps the roots for which a
SymPy relation holds:

```python
sol = motorcycle.known(x1, 55).solve(t1)   # two roots: t1 = -10.0 and 2.5
sol.where(t1 > 0).number(t1)               # 2.5 (s)
```

The full example, with part (b),
is in [examples/up_15e/ch02/examples/n04/](examples/up_15e/ch02/examples/n04/), and runs with:

```bash
uv run python -m examples.up_15e.ch02.examples.n04.main_handwritten
```

[examples/up_15e/](examples/up_15e/) holds the examples ported from
combine-equations.py, one folder per problem: `ch02/examples/n04/` is
Example 2.4, and `ch02/exercises/n003/` is Exercise 2.3. Each folder's
`main.py` is the main version, and a version in another style has a
slug, as in `main_handwritten.py`. Most of them run on the old physics
code, which equarium carries as `equarium.physics`, such as Example
2.4's:

```bash
uv run python -m examples.up_15e.ch02.examples.n04.main
```

## Docs

- [Implementation series](docs/design/implementation/README.md): one
  numbered folder per series of changes, from the
  [project setup](docs/design/implementation/000-project-setup/README.md)
  on.

## Development

```bash
uv sync
uv run pytest
uv run pytest -m slow
uv run pyright
```

`uv run pytest` skips the tests marked `slow`, those that take more than
5 s; `uv run pytest -m slow` runs only them, a few minutes in all.
