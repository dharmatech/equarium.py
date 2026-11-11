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
| 004 | [physics](004-physics/README.md) | charter, spec, checkpoints | Done (2026-11-09): 7 of 7 increments done; merged into `master` (2026-11-11) as version 0.2.0 |
| 005 | [constant acceleration](005-constant-acceleration/README.md) | README, checkpoints | Checkpoint 001 done (2026-11-11); 002, the audit, built (2026-11-11), not yet reviewed |

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
  under `examples/up_15e/`. Series 004 then redesigned the physics
  layer and deleted that code.
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
  the old physics code. Done: every example runs on the new layer, the
  old physics code's copy is deleted, and the version is 0.2.0. The
  branch merged into `master` on 2026-11-11, with two experiments
  merged into it first: setup sketches and transcript mode, each with
  its notes in `docs/experiments/`.
- **005 constant acceleration:** `m.kinematics()` assumed constant
  acceleration on every edge, through the book's 2.10, without saying
  so. It gives only the definitions, which hold for any motion, and
  `m01.constant_acceleration()` states the assumption for one edge.
  001 adds the call to every example, with no result changed; 002
  audits each problem against the book. On the branch
  `2026-11-11-constant-acceleration`, from `master`. 001 is done; 002
  is built, not yet reviewed: it drops the call from Exercises 2.1, 2.3
  and 2.5, which use averages only, with no result changed, and the 13
  other problems keep theirs, each with the problem's reason in a
  comment. The series is done once 002 is reviewed.
