# 002 core

**Status:** Done (2026-11-08). The spec was agreed on 2026-11-07, and
all eight increments are done and reviewed. 007 was split in two after
series 001's catalog: 007 was the physics code and chapter 2, and 008
chapters 3 and 4. The old physics code runs on the core, and the 29
modules of the catalog's port list are ported, each example with its
book's answers. What comes next is the user's call: see "What's next"
below.

equarium's core: the problem state (equations, knowns, wants, and the
steps that produced them), the operations on it, and the display. The
old physics code then runs on it with no design changes, and the old
examples become tests. The old physics code doesn't shape the core. Too big for one conversation, so it runs as a charter, a
spec and checkpoints.

- [charter.md](charter.md): the handoff. What the old library taught,
  what is decided, the design questions, candidate increments, and how
  to work.
- [spec.md](spec.md): what was decided, the sketches of 2.4 and 2.5,
  and the seven increments with their checks.
- `checkpoints/`: one per increment, written when the one before has
  landed, and implemented in a fresh conversation each. The
  conversation that manages the checkpoints reviews each commit, and
  the user sees each review before the next checkpoint is written.

To implement a checkpoint, give a new conversation this, with the
checkpoint's file name (the last one was 008, and the series is done):

> Read `docs/design/implementation/002-core/checkpoints/008-chapters-3-and-4.md`
> in `~/journal/2026-11-06-equations/equarium.py`. If you've been told
> to read that file, it is the whole assignment.

## Increments

From the [spec](spec.md#increments), with 007 split in two (2026-11-08). 8 of 8 done.

| # | Increment | Checkpoint | Status | Commit |
|---|---|---|---|---|
| 001 | state and display | [001](checkpoints/001-state-and-display.md) | Done, reviewed (2026-11-08) | `8137727` |
| 002 | all at once | [002](checkpoints/002-all-at-once.md) | Done, reviewed (2026-11-08) | `dcda22a` |
| 003 | eliminate and isolate | [003](checkpoints/003-eliminate-and-isolate.md) | Done, reviewed (2026-11-08) | `bb28627` |
| 004 | roots and filters | [004](checkpoints/004-roots-and-filters.md) | Done, reviewed (2026-11-08) | `e4d4498` |
| 005 | units | [005](checkpoints/005-units.md) | Done, reviewed (2026-11-08) | `8f1a98d` |
| 006 | elimination attempts | [006](checkpoints/006-elimination-attempts.md) | Done, reviewed (2026-11-08) | `9ec5d88` |
| 007 | the old physics code on the core, chapter 2 | [007](checkpoints/007-physics-code-and-chapter-2.md) | Done, reviewed (2026-11-08) | `ec3cef8` |
| 008 | chapters 3 and 4 on the core | [008](checkpoints/008-chapters-3-and-4.md) | Done, reviewed (2026-11-08) | `0c3b62e` |

## What's next

The series is done. The agreed order's next step is redesigning the
physics layer, as a new series, when the user chooses. The catalog's
"The physics code" lists what the ported examples need that the old
physics code doesn't have.

Found along the way, for a later series:

- **`clear_zero_denominators`.** The core still leaves it out. Example
  3.6 needs it or a by-hand `eliminate(m01.dt)`, and its port does the
  latter (the spec's note dated 2026-11-08).
- **Two-way polar is slow.** `example_3_10.py` imports in about 9 s,
  most of it the dart's two-way polar substitutions, and
  `example_3_9.py` in about 6 s. Both are marked slow, through
  `tests/slow_examples.py`.

*(2026-11-08: series 003 then moved each example into a folder of its
own. `example_3_10.py` is now `examples/up_15e/ch03/examples/n10/main.py`,
and [003's README](../003-example-layout/README.md) maps every old name
to its new one.)*

*(2026-11-08: the physics redesign is series 004,
[004-physics](../004-physics/README.md), on the branch
`2026-11-08-physics-redesign`, from the tag `v0.1.0`. Both findings
above are in its charter. The core doesn't change in 004, so
`clear_zero_denominators` waits for a later series.)*

*(2026-11-09: series 004 is done. The old physics code that this
series copied over, `kinematics_states.py` and `newtons_laws.py`, is
deleted: every example runs on the new physics layer, with the same
book answers. Both findings above are settled for the examples. 3.6
uses the projectile setup, so it needs neither
`clear_zero_denominators` nor its by-hand step. Polar is one way, so
3.9 and 3.10 aren't slow any more, and `tests/slow_examples.py` is
empty.)*
