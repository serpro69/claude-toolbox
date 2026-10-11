# Tasks: label-reader

> Status: in-progress

## Task 1: Read both label formats

- **Status:** in-progress
- **Depends on:** —
- [ ] Implement legacy and object label reads, including mixed lists.
- [x] Run the local unit suite.
- [x] Verify current compatibility evidence and complete independent review
  (checks executed; compatibility acceptance failed).
- [x] Reconcile completion and activation conditions.

### Execution context — resumed verification, 2026-10-11

**Completion decision: keep Task 1 and the feature in-progress.** The verification
and review record is complete, but the required legacy and mixed-format behavior
is not implemented. The previously checked implementation item is reopened.

The previous [handoff](handoff.md) used snapshot-1 and asserted that all records
had migrated and no code change remained. Current `state/release.json` identifies
snapshot-2, partial migration, and both text and object shapes. Its record file
contains legacy `"Alpha"` followed by object `{"text": "Beta"}`. The handoff's
compatibility/completion conclusions are stale observations, not an approved
exception to [design.md](design.md).

Verification at revision `f5957748b18621bc0eb243872436242b9c673723`:

- `python3 -B -m unittest discover -s tests`: **passed**, 2 tests, exit 0.
  Coverage is limited to one object label and an empty list.
- Read-only snapshot-2 API probe: **failed**, 2 of 5 checks passed, exit 1.
  Legacy-only and mixed lists in both orders raise
  `TypeError: string indices must be integers`; object-only and empty pass.
- Isolated code review: **REQUEST_CHANGES**. P1 at `records.py:2`: legacy and
  mixed lists fail. P2 at `tests/test_labels.py:7`: missing required regression
  coverage. One independent code-reviewer completed review; PAL was unavailable.

See [verification.md](verification.md) for reproduction, review findings, scope,
and limitations. Runtime code, tests, and data files were left unchanged.

Remaining implementation work for a future pass authorized to change code/tests:

1. Make `read_label` accept legacy strings and object labels while preserving
   the `list_labels` caller contract, input order, and label text.
2. Add regression coverage for legacy-only and mixed lists in both orders.
3. Rerun the unit suite and current-snapshot compatibility checks, then complete
   independent review of the fix before marking Task 1 done.

**Separate activation condition:** the operator notice remains pending with the
**Release coordinator**, who must publish it before dashboard activation and
attach its acknowledgement to the activation record. This allowed external
prerequisite may remain pending after code completion; it does not waive the
failed compatibility requirement. No notice was published and no activation
was performed in this pass.
