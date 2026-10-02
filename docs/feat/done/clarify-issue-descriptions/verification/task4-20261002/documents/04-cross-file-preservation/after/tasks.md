# Tasks: import preview

Resume Task 1 by adding valid and invalid counts. The checklist records current
task progress; no implementation source is supplied to verify it.

## Task 1: Preview

**Status:** in-progress
**Depends on:** —

- [x] Accept id,name columns.
- [ ] Return valid and invalid counts.

The planned preview writes zero rows. A three-row CSV with one invalid row must
report two valid rows and one invalid row. Apply remains disabled.

Read the [deployment gate](design.md#deployment-gate) before enabling preview.

## Task 2: Apply

**Status:** pending
**Depends on:** Task 1

Apply is future work, outside the preview increment. Product owns the open
duplicate-row policy decision.

- [ ] Decide duplicate-row policy with product before implementing apply.
