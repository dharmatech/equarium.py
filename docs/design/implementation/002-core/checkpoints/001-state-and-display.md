# core 001: state and display

**Status:** Done at `8137727` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The immutable `System` and everything that changes it without solving:
labeled equations with origins, knowns with or without a number, wants,
the explicit `eliminate_zeros()` step, the history of steps,
`analyze()`, and the terminal display with its symbol hook. Plus
`eq_flat`. Nothing solves yet; increment 002 adds that. Stop when the
checks pass and the commit is in.

## Read first

- [The spec](../spec.md): "What the prototype showed", the decisions
  from "The state" to "The package", "SymPy to watch", and §001, which
  this checkpoint carries out. The later increments are context, not
  work. Where this page is more exact than the spec, follow this page.
- [The charter](../charter.md), for background only: the user's
  preferences, and what the old library taught.
- The old library, read-only, in
  `~/src/combine-equations.py/src/combine_equations/`: `eq_flat` in
  `misc.py`, `connected_unknowns` in `solve_system.py`,
  `_safe_simplify`, `_is_tautology`, `cleanup_equations` and
  `eliminate_zero_eqs` in `eliminate_variable_subst.py`, and
  `display_equations.py`, whose coloring by renaming this replaces.
  `examples/up/ch2/up-example-2.4/up-example-2.4-v3-001-step-by-step.py`
  has 2.4's equations written out. Don't edit that repo.
- `pyproject.toml`, `src/equarium/__init__.py` and
  `tests/test_package.py`, which are all the code there is.

## Starting point

`master` at the commit that adds this checkpoint, on top of `ddc4f4a`
(the spec). The package is `src/equarium/__init__.py` (a docstring
only), `src/equarium/py.typed`, and `tests/test_package.py` (one import
check). `uv run pytest` passes 1 test, and `uv run pyright` reports 0
errors and 0 warnings. Python 3.14, SymPy 1.14.0, pytest 9.2.0, pyright
1.1.414.

## Build

### Layout

The spec's layout, with one change it allows: `Equation`, the origins
and the steps move out of `system.py`, one layer down. `rewrite.py`
builds them at runtime, and `system.py` imports `rewrite.py` for its
delegating methods, so leaving them in `system.py` would be an import
cycle. From the bottom up, each module imports at runtime only the ones
above it in this list:

```
src/equarium/
  errors.py         EquariumError, UsageError, Contradiction
  sympy_compat.py   safe_simplify
  equations.py      Equation, Given, Derived, Origin; eq_flat
  steps.py          the step types and their union, Step
  analysis.py       Role, Analysis, analyze
  rewrite.py        cleanup, eliminate_zeros
  display.py        the printer, plain, terminal, render, render_history
  system.py         System
  __init__.py       re-exports System, eq_flat and the three errors
```

`analysis.py`, `rewrite.py` and `display.py` take a `System`, so they
import it only under `if TYPE_CHECKING:`. Python 3.14 evaluates
annotations lazily, so no quotes or `__future__` import are needed. A
scratch prototype of this pattern ran on 3.14 and passed pyright. How
`rewrite.py` builds the next system (`dataclasses.replace` with
`previous=system`, or a small helper on `System`) is up to you, as long
as there's no import cycle at runtime.

**Not in this increment,** though the spec names them: `solve`,
`Solution`, `Root`, `all_at_once`, `eliminate`, `isolate`,
`EliminationError`, `IsolationError`, `show(origins=True)`,
`show_history()`, the strategies, units, `examples/`, and the `slow`
marker. `pyproject.toml` doesn't change.

### `errors.py`

`EquariumError(Exception)`, built as
`EquariumError(reason, *, symbol=None, labels=())`, with the attributes
`reason: str`, `symbol: sp.Symbol | None` and `labels: tuple[str, ...]`.
`str(error)` is the reason. Two subclasses for now, `UsageError` and
`Contradiction`. 003 adds the other two.

### `sympy_compat.py`

`safe_simplify(expr)`: `sp.simplify(expr)`, or the expression unchanged
when SymPy raises. A comment names
[SymPy issue 28926](https://github.com/sympy/sympy/issues/28926) as the
reason. It comes now, although the spec's §001 doesn't list the module,
because cleanup needs it. It's the package's only `try` around
`simplify`.

### `equations.py`

- **`Equation`,** frozen: `label: str`, `eq: sp.Equality` and
  `origin: Origin`, the origin with `compare=False`, so equations
  compare by label and `Eq` only.
- **`Given()`,** frozen, with no fields. **`Derived`,** frozen:
  `op: Op`, `symbol: sp.Symbol` and `parents: tuple[Equation, ...]`.
  `type Op = Literal["eliminate zeros"]` for now; 003 adds `"eliminate"`
  and `"isolate"`. `type Origin = Given | Derived`.
- **`eq_flat(*items)`:** pairs into `sp.Eq`s, returned as a list, as
  the old one. An odd count raises `UsageError` naming the count.

### `steps.py`

One frozen dataclass per operation, and `type Step = …` their union,
which `display.py` renders with `match`. Steps hold no description.

| Step | Fields |
|---|---|
| `AddStep` | `equations: tuple[Equation, ...]`, the ones added |
| `KnownStep` | `values: tuple[tuple[sp.Symbol, sp.Expr \| None], ...]`, in the order given |
| `ForgetStep` | `symbols: tuple[sp.Symbol, ...]` |
| `WantStep` | `symbols: tuple[sp.Symbol, ...]` |
| `EliminateZerosStep` | `zeros: tuple[sp.Symbol, ...]`, `rewritten: tuple[str, ...]`, `dropped: tuple[str, ...]` |

### `system.py`

**`System`,** a frozen dataclass. `System()` is the empty root, with no
step and no previous system. Everything else comes from its methods.
Each returns a new `System` whose `previous` is the receiver and whose
`step` records the call, and one call is one step.

The fields:

- `equations: tuple[Equation, ...]`, in the order added.
- `knowns: Mapping[sp.Symbol, sp.Expr | None]`, a `MappingProxyType`
  over a fresh dict, in insertion order. A replaced known keeps its
  place.
- `wants: tuple[sp.Symbol, ...]`, in the order given.
- With `compare=False`: `fixed: frozenset[sp.Symbol]` (the knowns
  `eliminate_zeros` substituted), `next_label: int` (the counter, from
  1), `step: Step | None`, and `previous: System | None`. `previous`
  also gets `repr=False`, or a repr prints the whole history.

So equality is content, as the spec says, and `hash` fails on the
mapping, which the spec allows.

The methods that edit the state are written here, since they are the
state's own:

- **`add(*eqs, label=None)`.** Each item is an `sp.Equality`, SymPy's
  `true` or `false`, or a Python bool. True is dropped, false raises
  `Contradiction`, and anything else raises `UsageError`. A label with
  more than one equation, or a label already in use, raises
  `UsageError`. An automatic label is `str(next_label)`, skipping any
  label in use, and the counter only goes up, so a label is never
  issued again after its equation is dropped. New equations are
  `Given()`.
- **`known(sym, value)`, `known(sym)` and `known({sym: value, …})`,**
  with `@overload`s. A key must be an `sp.Symbol`. A value is sympified
  and must be an `sp.Expr` with no free symbols (units pass, ready for
  005). `None`, or no value, means known with no number. Anything else
  is a `UsageError`, as for `known(x0, D*sp.tan(th))`. So are a want,
  and a fixed known given a value that isn't `==` its old one.
- **`forget(*syms)`.** `UsageError` for a symbol that isn't known, or
  one that is fixed.
- **`want(*syms)`** replaces the wants, and `want()` clears them.
  `UsageError` for a known, a duplicate, or a non-symbol.
- **`equation(label) -> Equation`:** the one with that label, or
  `UsageError`. It isn't in the spec's table, but the tests need it,
  and so will 003's `using`.
- **`eliminate_zeros()`, `analyze()` and `show()`:** one line each,
  delegating to `rewrite.eliminate_zeros`, `analysis.analyze` and
  `print(display.render(self))`.

### `rewrite.py`

- **Cleanup,** private to the package, applied to what a rewrite made
  of one equation. `true`, or an `Eq` whose
  `safe_simplify(lhs - rhs)` is 0, is dropped. `false`, or a difference
  with no free symbols that isn't zero, raises `Contradiction` with the
  label. Anything else is kept. Only the equations a step rewrote go
  through cleanup. An equation added as written stays as written.
- **`eliminate_zeros(system)`.** The zeros are the knowns whose value
  has `value.is_zero is True`, in the knowns' order. Don't test
  `== 0`: in SymPy 1.14, `Float(0.0) == 0` is False. They're
  substituted one at a time, as the old `eliminate_zero_eqs` did, each
  as `subs(zero, sp.S.Zero)` so no float zero gets into a formula, with
  cleanup after each. An equation a zero changes keeps its label and
  gets `Derived("eliminate zeros", zero, (before,))`, `before` being
  the `Equation` as it was. So an equation that contains two zeros
  gets two layers, the outer one for the later zero. The step records
  all the zeros, the labels rewritten and still there (in equation
  order), and the labels dropped. Every zero becomes fixed, whether it
  occurred in an equation or not. With no zeros, the result equals the
  input, and the step is still recorded.

### `analysis.py`

- **`Role`,** an `Enum`: `KNOWN`, `WANT`, `UNKNOWN`.
- **`Analysis`,** frozen:
  - `knowns: frozenset[sp.Symbol]`, including those with no number;
  - `wants: tuple[sp.Symbol, ...]`;
  - `connected: frozenset[sp.Symbol]`: the unknowns linked to the
    wants, wants included, grown as in the old `connected_unknowns`
    but without its `subs`;
  - `others: frozenset[sp.Symbol]`: the rest of the unknowns;
  - `ready: tuple[str, ...]`: the labels of the equations, any of
    them, with exactly one unknown;
  - `connected_labels: tuple[str, ...]`: the labels of the equations
    that contain a connected unknown, which 002's `all_at_once` takes.

  Both tuples of labels are in equation order. The spec's two counts
  are `len(connected)` and `len(connected_labels)`. `role(sym) -> Role`
  gives a symbol's role.
- **`analyze(system) -> Analysis`.**

### `display.py`

- **The hooks:** `type SymbolHook = Callable[[sp.Symbol, Role], str]`.
  `plain` returns the name. `terminal` wraps a known's name in
  `\x1b[32m` and `\x1b[0m`, a want's in `\x1b[31m` and `\x1b[0m`, as
  the old `display_equations.py` did, and leaves the rest plain.
- **The printer:** a `StrPrinter` subclass, built with the hook and
  the analysis, whose `_print_Symbol` returns the hook's string for
  the symbol and its role. It's built with `full_prec=False`, so
  `known(g, 9.8)` shows `g = 9.8` rather than `9.80000000000000`. An
  equation prints as its two sides, `lhs = rhs`, never through `Eq`.
  Symbol names don't change, so SymPy's term order doesn't either.
- **`render(system, symbol=terminal) -> str`.** Lines joined by
  `"\n"`, with no trailing newline. One line per equation,
  `(label)  lhs = rhs`, two spaces and no padding, then four summary
  lines. For `part_a` (see Tests), with `symbol=plain`:

  ```
  (2.2)  v_av = (-x0 + x1)/t1
  (2.7)  a = (-v0 + v1)/t1
  (2.10)  v_av = v0/2 + v1/2
  knowns: t0 = 0, x0 = 5, v0 = 15, a = 4, t1 = 2
  wants: x1, v1
  connected: v1, v_av, x1 (3 unknowns in 3 equations)
  ready: (2.7)
  ```

  The knowns are in the system's order, and one with no number is its
  name alone (`knowns: D, g = 9.8`). The wants are in their order, and
  the connected unknowns are sorted by name. An empty list reads
  `none`, as in `wants: none`, and with no wants `connected: none`.
  Every symbol goes through the hook. Values and labels don't.
- **`render_history(system, symbol=terminal) -> str`.** It walks back
  through `previous`, then prints the steps numbered from 1, each with
  the roles of the system that step produced. For `part_a`, with
  `symbol=plain`:

  ```
  1. add (2.2)
  2. add (2.7)
  3. add (2.10)
  4. known t0 = 0
  5. known x0 = 5
  6. known v0 = 15
  7. known a = 4
  8. eliminate zeros t0: into (2.2), (2.7)
  9. known t1 = 2
  10. want x1, v1
  ```

  The other forms: `add (1), (2)`, `known D, g = 9.8`, `forget t1`,
  `want none`, `eliminate zeros t0, y0: into (1), (3), dropped (4)`,
  `eliminate zeros t0: dropped (1)`,
  `eliminate zeros t0: no change`, and `eliminate zeros: none` when
  there are no zeros. `System()` has an empty history, which renders
  as `""`.

### `__init__.py`

The docstring, then the imports and an `__all__` for `System`,
`eq_flat`, `EquariumError`, `UsageError` and `Contradiction`. The rest
is imported from its module, as in
`from equarium.display import render, plain`.

### Tests

A helper builds 2.4's base as in the spec's sketch: the symbols
`x0 x1 v0 v1 t0 t1 v_av a`, three labeled adds, `known` t0 = 0,
x0 = 5, v0 = 15 and a = 4 in that order, each its own call, then
`eliminate_zeros()`. Then `part_a = base.known(t1, 2).want(x1, v1)`.
`pre` below is the base without its `eliminate_zeros()`.

**`tests/test_system.py`,** the spec's §001 checks, made exact:

- **Labels.** The base's labels are `2.2`, `2.7` and `2.10`. Two
  unlabeled adds get `1`, then `2`. A label with two equations, and a
  second `2.2`, raise `UsageError`. After `add(e, label="1")`, an
  unlabeled add gets `2`. `add` of `sp.Eq(x0, x0)` (SymPy's `true`)
  adds nothing, and `sp.Eq(x0, x0 + 1)` (`false`) raises
  `Contradiction`.
- **An old-style zero equation.**
  `System().add(sp.Eq(t0, 0)).known(t0, 0).eliminate_zeros()` drops
  `(1)`, and its step's `dropped` is `("1",)`. An unlabeled add after
  that gets `2`, not `1`.
- **Zeros.** In `pre`, the equations are the three as added.
  `eliminate_zeros()` leaves no t0 in any equation, and its step is
  `EliminateZerosStep((t0,), ("2.2", "2.7"), ())`. The origin of
  `(2.2)` is `Derived("eliminate zeros", t0, (pre.equation("2.2"),))`,
  that of `(2.7)` likewise, and `(2.10)` still has `Given()`. The same
  with `known(t0, 0.0)` also leaves no `sp.Float` in any equation.
- **Fixed knowns.** On the base, `forget(t0)` and `known(t0, 3)` raise
  `UsageError`. On `pre`, both are allowed.
- **A later zero.** `base.known(x0, 0)` leaves x0 in `(2.2)`, and a
  second `eliminate_zeros()` then takes it out.
- **No zeros, and a contradiction.**
  `System().add(e).eliminate_zeros()` equals its input, and its step is
  `EliminateZerosStep((), (), ())`.
  `System().add(sp.Eq(t0, 3)).known(t0, 0).eliminate_zeros()` raises
  `Contradiction`.
- **Knowns.** `known(x0, 5)` leaves the equations alone.
  `known(x0, D*sp.tan(th))` raises `UsageError`. After `known(D)`,
  `knowns[D]` is `None` and D's role is `KNOWN`. The dict form sets
  several knowns in one step. `part_a.known(x1, 3)`,
  `base.want(x0)` and `base.forget(t1)` raise `UsageError`.
- **Branches.** After `part_a`, `base.knowns` has no t1. Two branches
  built the same way are equal, and so are
  `base.known(t1, 2).want(x1, v1)` and `base.want(x1, v1).known(t1, 2)`,
  whose histories differ. Assigning to `part_a.knowns[t1]` raises
  `TypeError`, assigning a field raises `FrozenInstanceError`, and
  `part_a.previous.previous is base`.
- **Analysis.** For `part_a`: `connected` is `{x1, v1, v_av}`, `ready`
  is `("2.7",)`, `connected_labels` is `("2.2", "2.7", "2.10")`,
  `others` is empty, and the roles of x0, x1 and v_av are `KNOWN`,
  `WANT` and `UNKNOWN`. For the base, with no wants: nothing is
  connected, `others` is `{x1, v1, v_av, t1}`, and nothing is ready.
- **`eq_flat`.** `eq_flat(a, b, c, d)` is `[Eq(a, b), Eq(c, d)]`, and
  an odd count raises `UsageError`.

**`tests/test_display.py`:**

- `render(part_a, symbol=plain)` is the block above.
- With the terminal hook, the `(2.2)` line is
  `"(2.2)  v_av = (-\x1b[32mx0\x1b[0m + \x1b[31mx1\x1b[0m)/\x1b[32mt1\x1b[0m"`,
  and the whole render with the codes removed is the plain render.
- `render(pre, symbol=plain)` begins
  `(2.2)  v_av = (-x0 + x1)/(-t0 + t1)`, and lists `t0 = 0` among the
  knowns.
- **The term order the old display broke:** for
  `System().add(sp.Eq(dt, -m_0_t + m_1_t)).want(m_1_t)`, the equation
  line is `(1)  dt = -m_0_t + m_1_t` with the plain hook, and the same
  once the codes are removed with the terminal one.
- `render(System().known(D).known(g, 9.8), symbol=plain)` is
  `knowns: D, g = 9.8`, then `wants: none`, `connected: none` and
  `ready: none`.
- `render_history(part_a, symbol=plain)` is the block above.

**`tests/test_package.py`:** the import check becomes a check that each
name in `equarium.__all__` is an attribute of `equarium`.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **The series [README](../README.md):** mark 001 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager, who fills them in after
  review.
- **The [series map](../../README.md):** 002's status says 001 of 7 is
  done.
- **The package `README.md`** doesn't change. Its usage section starts
  in 002.

## Check and commit

- `uv run pytest` passes: the one old test, rewritten, plus yours. No
  test is slow.
- `uv run pyright`: 0 errors, 0 warnings.
- Look at `part_a.show()` once in a real terminal, from a short script
  outside the repo, to see the colors.
- One commit on `master`, with the code, tests and docs, in the style
  of `git log`: a subject line, then a wrapped paragraph saying what
  and why. Don't push.

## Report

When done, say in a few lines: the commit, the number of tests, how
`rewrite.py` builds the next system, where you needed a `cast` for
SymPy's types, and anything in the spec or this checkpoint that was
wrong or unclear, with what you did instead. Then stop; increment 002
is a separate checkpoint.
