# core 002: all at once

**Status:** Done at `dcda22a` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

Solving: `System.solve()`, the `all_at_once` strategy, and its result,
a `Solution` of `Root`s with a formula and a number for every want,
several wants at once. Plus the examples convention: the first two
ported examples, 2.4 and 2.5 with their equations written out, each
with the book's answers in a `BOOK`, and one test that checks every
example. Stop when the checks pass and the commit is in.

## Read first

- [The spec](../spec.md): "What the prototype showed", the decisions
  "Solving", "Strategies", "The display" and "Examples in the repo",
  "SymPy to watch", the 2.4 sketch, and §002, which this checkpoint
  carries out. The later increments are context, not work. Where this
  page is more exact than the spec, follow this page.
- [Checkpoint 001](001-state-and-display.md), for how the package is
  laid out and why, and the code it describes: everything in
  `src/equarium/`, and `tests/`.
- The old scripts, read-only, in `~/src/combine-equations.py/examples/up/ch2/`:
  `up-example-2.4/up-example-2.4-v3-001-step-by-step.py` and
  `up-example-2.5/up-example-2.5-v3-002-concise.py`. Their printed
  formulas are in their comments. `solve_and_display_` in
  `src/combine_equations/solve_and_display.py` is the old display of
  a result. Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `8137727`
(increment 001). `uv run pytest` passes 40 tests, and `uv run pyright`
reports 0 errors and 0 warnings.

## Build

### Layout

New or changed:

```
src/equarium/
  solve.py          Root, Solution, Strategy, all_at_once, the entry point
  display.py        + render_solution
  system.py         + System.solve
  __init__.py       + Solution, Root, all_at_once
examples/
  __init__.py       and one in each folder below
  answers.py        Answer
  up_15e/ch02/example_2_4_handwritten.py
  up_15e/ch02/example_2_5_handwritten.py
tests/
  test_solve.py     new
  test_examples.py  new
  test_display.py   + the solution display
```

The imports keep 001's layering. `solve.py` imports `analysis`,
`display` and `errors` at runtime, and `System` only under
`TYPE_CHECKING`. `display.py` imports `Solution` only under
`TYPE_CHECKING`. `system.py` imports `solve.py`. Import the names
rather than the module there, since the method is also called
`solve`. A scratch prototype checked that a frozen dataclass field
typed with a `TYPE_CHECKING` name (`system: System`) works on 3.14 and
passes pyright.

**One name changes from the spec:** a solution renders with
`render_solution(solution, symbol=terminal)`, not `render(solution)`.
One `render` for both types would have to tell them apart at runtime,
which means `display.py` importing `System` or `Solution` at runtime,
and both of their modules import `display.py`. `render(system)` stays
as it is.

**Not in this increment,** though the spec names them: `where`,
`in_units`, `Answer`'s `unit`, `eliminating`, the time on the display,
the `slow` marker, `eliminate`, `isolate`, `show_history()` and
`show(origins=True)`. Leave `tests/example_2_4.py` and the 001 tests
as they are. The 001 helper's `motorcycle()` is the system before
`eliminate_zeros()`, and the example's `motorcycle` is the one after,
so the two don't merge.

### `solve.py`

- **`Root`,** frozen: `formulas` and `numbers`, both
  `Mapping[sp.Symbol, sp.Expr]` (a `MappingProxyType`), keyed by the
  wants in their order. `formula(sym)` and `number(sym)`, with
  `UsageError` for a symbol that isn't a want.
- **`Solution`,** frozen: `system: System` (the system it was solved
  from, with its history), `roots: tuple[Root, ...]`,
  `elapsed: float` (seconds) and `reason: str | None` (set exactly when
  there are no roots). `formula(sym)` and `number(sym)` need exactly
  one root, and otherwise raise `UsageError` naming the count, as in
  `2 roots`. `show()` prints `display.render_solution(self)`.
- **`type Strategy = Callable[[System], Solution]`.**
- **The entry point,** behind `System.solve(*wants, strategy=all_at_once)`.
  You choose its name, for example `solve_with(system, wants, strategy)`.
  Wants given here replace the system's wants first, through
  `system.want(*wants)`, so the solution's system records that step.
  A system that still has no wants raises `UsageError` before the
  strategy runs. Strategies can then count on there being wants.
- **`all_at_once(system)`:**
  - **The solve.** Analyze, take the equations in `connected_labels`,
    and run one `sp.solve(equations, unknowns, dict=True)`, with the
    connected unknowns sorted by name. Knowns stay symbols.
  - **The time.** `elapsed` times the `sp.solve` call, with
    `time.perf_counter()`.
  - **Each root.** For each dict SymPy returns, the root's formula for
    a want is that dict's value. Its number is `sp.N` of the formula
    after substituting the knowns that have a number. A known with no
    number stays a symbol, and units would stay as they come.
  - **No roots is a result, not an exception.** Each case gets an
    exact reason:
    - `sp.solve` returns `[]`: `"sp.solve found no roots"`.
    - `sp.solve` raises `NotImplementedError`: `"sp.solve: "` plus its
      message.
    - Any root leaves a want out of its dict: `"sp.solve left x1
      undetermined"`, naming the first such want. SymPy does this when
      a known is missing. With 2.4's t1 not known, it solves t1, v1 and
      v_av in terms of x1.

    Any other exception propagates.
- `sp.solve` is poorly typed. A `cast` to `list[dict[sp.Symbol, sp.Expr]]`
  is better than a `# type: ignore`.

### `system.py` and `__init__.py`

`System.solve(*wants: sp.Symbol, strategy: Strategy = all_at_once) -> Solution`,
one line delegating to the entry point. `__init__.py` adds `Solution`,
`Root` and `all_at_once` to its imports and `__all__`.

### `display.py`

`render_solution(solution, symbol=terminal) -> str`, with the
printer and hook from 001 and the roles of `solution.system`. For each
want, in order, its formula line `want = formula`, then its number line
`want = number`, as the old `solve_and_display_` printed them. For
`sol_a` (below), with `symbol=plain`:

```
x1 = a*t1**2/2 + t1*v0 + x0
x1 = 43.0
v1 = a*t1 + v0
v1 = 23.0
```

The printer's `full_prec=False` turns `sp.N`'s `43.0000000000000` into
`43.0`. With several roots, each root's lines come after a line
`root 1:`, `root 2:`, … in SymPy's order, indented by two spaces. With
none: `no roots: ` plus the reason. `elapsed` isn't shown until 006.

### The examples

As the spec's "Examples in the repo" says:

- **Packages.** `examples/`, `examples/up_15e/` and
  `examples/up_15e/ch02/` each get an `__init__.py`.
- **`pyproject.toml`.** Add `pythonpath = ["."]` under
  `[tool.pytest.ini_options]`, and `"examples"` to pyright's `include`.
- **The modules.** Each builds its systems and solutions at import, has
  a `BOOK: list[Answer]`, and prints only under
  `if __name__ == "__main__":`. Each runs with
  `uv run python -m examples.up_15e.ch02.<name>`. The module docstring
  names the book, the edition, the example and the old script it was
  ported from.

**`examples/answers.py`:** `Answer(solution, symbol, *printed)`, a
frozen value. Write its varargs constructor however reads best.
`mismatch() -> str | None` returns `None` when the answer matches, and
otherwise says what differs, naming the symbol, the printed values and
the numbers found. It matches when:

- every root's number for that symbol is a real number (no free
  symbols, not complex);
- the numbers, sorted, pair one to one with the printed values, also
  sorted, with the same count;
- each number is within half a unit in the printed value's last digit,
  inclusive. "43" allows ±0.5, "1.70" allows ±0.005, and "-11.3" allows
  ±0.05. Read the printed values with `Decimal`, so the half unit is
  exact.

`unit=` comes in 005.

**`example_2_4_handwritten.py`:** the spec's 2.4 sketch, as written
there. It defines `motorcycle` (after `eliminate_zeros()`), `part_a`,
`sol_a = part_a.solve()` and `sol_b = motorcycle.known(v1, 25).solve(x1)`.
Its `BOOK` holds the book's "43", "23" and "55" (Example 2.4 prints
43 m, 23 m/s and 55 m). Under `__main__` it shows `part_a`, `sol_a`
and `sol_b`. The old v3 script's `Eq(m_0.t, 0)` is now `known(t0, 0)`
plus `eliminate_zeros()`, and its formula
`m_0_v*m_1_t + m_0_x + m_1_t**2*m_a/2` comes out as
`a*t1**2/2 + t1*v0 + x0` with the sketch's names.

**`example_2_5_handwritten.py`:** the old v3-002 script written out
with its own symbol names: `m_0_x … m_1_v`, `m_a`, `v_av_m_0_1`, the
same for `p`, and `m_v`, `dist`, `t_01`. Drop its `Obj` and `Interval`
helpers.

- **The base, in the old order.** `add` the motorist's 2.2, 2.7 and
  2.10, then the officer's, then, through `eq_flat`, the two speed
  links (`m_0_v, m_v`, `m_1_v, m_v`) and the four meeting links
  (`dist, m_1_x`, `dist, p_1_x`, `t_01, m_1_t`, `t_01, p_1_t`). That
  gives automatic labels (1) to (12).
- **The knowns.** The old script's five zero equations become
  `known({p_0_v: 0, p_0_x: 0, m_0_t: 0, p_0_t: 0, m_0_x: 0})`. Then
  come `known(m_v, 15)`, `known(p_a, 3)` and
  `want(t_01, p_1_v, dist)`. Call that `setup`.
- **The solve.** `chase = setup.eliminate_zeros()`, and
  `sol = chase.solve()`.

The three wants solve together, in one root: `t_01 = 2*m_v/p_a`,
`p_1_v = 2*m_v` and `dist = 2*m_v**2/p_a`, the old script's formulas.
The spec's `t` is `t_01` here. The `BOOK` holds "10", "30" and "150"
(the book prints 10 s, 30 m/s and 150 m). Under `__main__` it shows
`setup`, `chase` and `sol`. The prototype got that root in 0.17 s.
Without `eliminate_zeros()`, the same solve takes about 2 s and gives
two roots, the second one being t = 0, when the motorist passes the
officer.

### Tests

**`tests/test_examples.py`:**

- **Every example.** It finds every module under `examples/` whose
  last name starts with `example_` or `exercise_`
  (`pkgutil.walk_packages`), with one parametrized case per module. A
  case imports the module and fails if it has no `BOOK`, or an empty
  one. Otherwise it asserts each answer's `mismatch()` is `None`,
  showing the message when it isn't.
- **`Answer` itself,** on 2.4's `sol_a` and on small systems:
  - "43" matches x1, and "43.0" matches too (±0.05);
  - "44" doesn't match, and neither does "43", "1" (two printed values
    for one root);
  - the two roots of `x**2 = 4` match "2", "-2" in either order;
  - a number with a free symbol doesn't match, as for
    `System().add(sp.Eq(x, 2*D)).known(D).want(x).solve()`.

**`tests/test_solve.py`,** the spec's §002 checks, made exact.
Compare formulas by `str`, which is SymPy's own order and what the
display prints. Compare numbers with floats: in SymPy 1.14, `sp.N(43)
== 43` is False, but `== 43.0` holds.

- **2.4 (a)** solves x1 and v1 in one root: `a*t1**2/2 + t1*v0 + x0`
  and `a*t1 + v0`, with numbers `43.0` and `23.0`, which
  `sol_a.number(x1)` returns too. `sol_a.system is part_a`.
- **2.4 (b):** `(2*a*x0 - v0**2 + v1**2)/(2*a)`, then `55.0`.
  `sol_b.system.wants` is `(x1,)`, and its step is `WantStep((x1,))`.
- **2.5:** one root, the three formulas above, then `10.0`, `30.0` and
  `150.0`.
- **No wants:** `motorcycle.solve()` raises `UsageError`.
- **No roots:**
  - `System().add(sp.Eq(x + y, 1), sp.Eq(x + y, 2)).want(x).solve()`
    has no roots, with the reason `"sp.solve found no roots"`.
  - `sp.Eq(x, sp.cos(x))` gives `"sp.solve: could not solve x - cos(x)"`.
  - `motorcycle.want(x1, v1).solve()` (no t1) gives
    `"sp.solve left x1 undetermined"`.
  - None of these raises.
- **Several roots:** `x**2 = 4` gives two roots, whose numbers are
  `{-2.0, 2.0}` as a set. Then `solution.number(x)` raises
  `UsageError`, whose message contains `2 roots`, and
  `root.formula(y)` raises `UsageError`. `elapsed` is a float, at least
  0.

**`tests/test_display.py`,** added:

- `render_solution(sol_a, symbol=plain)` is the block above.
- With the terminal hook, the codes removed give the same block, and
  the formula line starts with x1 in red.
- For `x**2 = 4`, the lines `root 1:` and `root 2:` are there, each
  followed by two lines indented by two spaces. Don't depend on which
  root comes first.
- A solution with no roots renders as `no roots: sp.solve found no roots`.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **`README.md`,** the package's: a short "Usage" section from the 2.4
  example. The system written out, `solve`, and what `show()` prints,
  plain, then the command that runs the example.
- **The series [README](../README.md):** mark 002 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 002 of 7 is
  done.

## Check and commit

- `uv run pytest` passes: the 40 tests from 001, plus yours. No test
  is slow.
- `uv run pyright`: 0 errors, 0 warnings, now including `examples/`.
- Both examples run with `uv run python -m examples.up_15e.ch02.example_2_4_handwritten`
  and the 2.5 one, and print what their comments and this page say.
- One commit on `master`, with the code, tests and docs, in the style
  of `git log`: a subject line, then a wrapped paragraph saying what
  and why. Don't push.

## Report

When done, say in a few lines:

- the commit and the number of tests;
- the entry point's name;
- how long 2.5's solve took;
- where you needed a `cast` for SymPy's types;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop; increment 003 is a separate checkpoint.
