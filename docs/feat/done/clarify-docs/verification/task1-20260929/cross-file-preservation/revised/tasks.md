# Tasks: import preview

## Task 1: Preview

**Status:** in-progress
**Depends on:** —

Resume here: column parsing is recorded as done, and counting is pending.
The planned preview reports valid and invalid row counts while writing zero rows.
For a three-row CSV with one invalid row, it will report two valid rows and one
invalid row. No implementation source was supplied to verify the recorded progress.

- [x] Accept id,name columns.
- [ ] Return valid and invalid counts.

Enable preview only after the support owner approves the sample-file walkthrough,
as required by the [deployment gate](design.md#deployment-gate).

## Task 2: Apply

**Status:** pending
**Depends on:** Task 1

Apply remains future work and disabled in the preview increment. Product owns the
open duplicate-row policy decision.

- [ ] Decide duplicate-row policy with product before implementing apply.
