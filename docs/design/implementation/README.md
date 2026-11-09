# Implementation series

One folder per series of changes, numbered in the order the work
happens, so the history reads top to bottom.

Each series is as light as its work allows:

- **A README** when the work is done in one conversation. It records
  the status, why, decisions, what changed, what was checked, and
  what's next.
- **One checkpoint** when the work is a settled task for a fresh
  conversation. The checkpoint is the whole assignment.
- **A charter, a spec and checkpoints** only when there is real design
  to settle first. The charter is the handoff, the spec is what was
  decided, and the checkpoints come one at a time, each after the
  previous one has landed and been reviewed.

Every document carries what the next conversation needs, since that
conversation won't have the transcript. That way no conversation grows
long enough to be compacted.

## Series

| # | Series | Form | Status |
|---|---|---|---|
| 000 | [project setup](000-project-setup/README.md) | README | Done (2026-11-07) |
| 001 | [example catalog](001-example-catalog/README.md) | one checkpoint | Catalog written (2026-11-08), its questions answered |
| 002 | [core](002-core/README.md) | charter, spec, checkpoints | Done (2026-11-08): 8 of 8 increments reviewed |
| 003 | [example layout](003-example-layout/README.md) | README | Done (2026-11-08) |
| 004 | [physics](004-physics/README.md) | charter, spec, checkpoints | In progress (2026-11-08): 1 of 7 increments done, on branch `2026-11-08-physics-redesign` |

- **001 example catalog:** every example and exercise in
  combine-equations.py, with the problem, the textbook's answers, the
  techniques used, and the alternative solving styles worth keeping.
  This becomes the test list and the to-do list for the rebuild, and
  the input to 002's increment 007.
- **002 core:** the problem state (equations, knowns, wants, and the
  steps that produced them), the operations on it, and the display.
  The old physics code then runs on it with no design changes, before
  any physics redesign. It doesn't shape the core. Done: the old
  physics code runs on the core, and the catalog's examples are ported
  under `examples/up_15e/`. The physics redesign would be the next
  series.
- **003 example layout:** each example, exercise and table under
  `examples/up_15e/` in a folder of its own, such as
  `ch02/examples/n04/main.py` for Example 2.4, with room for its
  versions, notes and diagrams.
- **004 physics:** the physics layer's redesign, on the core
  unchanged: structured symbols named by their access path
  (`m0.pos.x`), the dimension set once, and helpers for polar form,
  events, the projectile setup and Newton's laws. The examples move
  over in place, with the same book answers. It runs on the branch
  `2026-11-08-physics-redesign`, from the tag `v0.1.0`, the core with
  the old physics code.
