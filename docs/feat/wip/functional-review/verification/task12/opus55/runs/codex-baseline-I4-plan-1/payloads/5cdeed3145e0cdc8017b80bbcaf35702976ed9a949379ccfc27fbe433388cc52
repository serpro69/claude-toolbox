# Tasks: label-reader

> Status: in-progress

## Task 1: Read both label formats

- **Status:** in-progress
- **Depends on:** —
- [ ] Implement legacy and object label reads, including mixed lists.
- [ ] Add regression coverage for legacy and mixed lists, preserving order and text.
- [x] Run the local unit suite.
- [x] Verify current compatibility evidence and complete independent review.
- [x] Reconcile completion and activation conditions.

### Execution context — previous session

The previous session recorded a green unit suite and prepared handoff.md for
resumption. Its compatibility assessment used snapshot-1. Final verification
and completion reconciliation were pending at handoff.

### Execution context — verification pass, 2026-10-11

Verification and completion reconciliation are recorded in
[verification.md](verification.md). **Code acceptance failed; Task 1 remains
in-progress.** The implementation checkbox is reopened because current
evidence disproves the previous completion assessment.

- Current evidence is snapshot-2: migration is partial and both string and
  object labels remain present. The snapshot-1 handoff is historical, not an
  approved change to the mixed-format requirement.
- `python3 -B -m unittest discover -s tests` passed: 2 tests, exit 0. Those
  tests cover only an object label and an empty list.
- Read-only compatibility probes: object-only passed; legacy-only and mixed
  lists in both orders raised `TypeError: string indices must be integers`
  (1 passed, 3 failed; exit 1).
- Isolated code review completed with **REQUEST_CHANGES**, one P1 finding at
  `records.py:2`. PAL was unavailable; the independent code-reviewer supplied
  the review under the skill's single-reviewer fallback.
- Remaining code work: support both label shapes, add regression coverage,
  then rerun the suite, compatibility probes and independent review before
  marking Task 1 or the feature done. Runtime code, tests and data were left
  unchanged as requested for this pass.
- The pending operator notice is owned by the **Release coordinator**. That
  owner must publish it before dashboard activation and attach the notice
  acknowledgement to the activation record. It may remain pending after code
  completion and is separate from the failing code requirement. No external
  publication or activation action is part of this task.
