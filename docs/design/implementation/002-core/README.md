# 002 core

**Status:** Spec agreed (2026-11-07). Increments 001 to 006 are done
and reviewed (2026-11-08). Series 001's catalog is done, and 007 is
split in two: 007, the physics code and chapter 2, whose checkpoint
is written and waits for the user's review, and 008, chapters 3 and 4.

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
checkpoint's file name:

> Read `docs/design/implementation/002-core/checkpoints/007-physics-code-and-chapter-2.md`
> in `~/journal/2026-11-06-equations/equarium.py`. If you've been told
> to read that file, it is the whole assignment.

## Increments

From the [spec](spec.md#increments), with 007 split in two (2026-11-08). 006 of 8 done.

| # | Increment | Checkpoint | Status | Commit |
|---|---|---|---|---|
| 001 | state and display | [001](checkpoints/001-state-and-display.md) | Done, reviewed (2026-11-08) | `8137727` |
| 002 | all at once | [002](checkpoints/002-all-at-once.md) | Done, reviewed (2026-11-08) | `dcda22a` |
| 003 | eliminate and isolate | [003](checkpoints/003-eliminate-and-isolate.md) | Done, reviewed (2026-11-08) | `bb28627` |
| 004 | roots and filters | [004](checkpoints/004-roots-and-filters.md) | Done, reviewed (2026-11-08) | `e4d4498` |
| 005 | units | [005](checkpoints/005-units.md) | Done, reviewed (2026-11-08) | `8f1a98d` |
| 006 | elimination attempts | [006](checkpoints/006-elimination-attempts.md) | Done, reviewed (2026-11-08) | `9ec5d88` |
| 007 | the old physics code on the core, chapter 2 | [007](checkpoints/007-physics-code-and-chapter-2.md) | Checkpoint written (2026-11-08), waiting for review | |
| 008 | chapters 3 and 4 on the core | | Planned | |
