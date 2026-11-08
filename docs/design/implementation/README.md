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
| 001 | [example catalog](001-example-catalog/README.md) | one checkpoint | Catalog written (2026-11-08), waiting for the user's review |
| 002 | [core](002-core/README.md) | charter, spec, checkpoints | Spec agreed (2026-11-07); 006 of 7 done (2026-11-08); 007 waits for 001 |

- **001 example catalog:** every example and exercise in
  combine-equations.py, with the problem, the textbook's answers, the
  techniques used, and the alternative solving styles worth keeping.
  This becomes the test list and the to-do list for the rebuild, and
  the input to 002's increment 007.
- **002 core:** the problem state (equations, knowns, wants, and the
  steps that produced them), the operations on it, and the display.
  The old physics code then runs on it with no design changes, before
  any physics redesign. It doesn't shape the core.
