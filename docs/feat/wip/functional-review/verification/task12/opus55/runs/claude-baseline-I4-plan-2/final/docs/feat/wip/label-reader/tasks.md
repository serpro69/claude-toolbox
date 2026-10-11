# Tasks: label-reader

> Status: in-progress

## Task 1: Read both label formats

- **Status:** in-progress
- **Depends on:** —
- [ ] Implement legacy and object label reads, including mixed lists.
      (Unchecked 2026-10-11: the code reads only object labels. See the resume session notes below.)
- [x] Run the local unit suite.
- [ ] Verify current compatibility evidence and complete independent review.
- [ ] Reconcile completion and activation conditions.

### Execution context — previous session

The previous session recorded a green unit suite and prepared handoff.md for
resumption. Its compatibility assessment used snapshot-1. Final verification
and completion reconciliation remain pending.

### Execution context — resume session (2026-10-11)

Verification-only pass: runtime code, tests and data files were left unchanged.

**handoff.md is stale.** It assessed snapshot-1 and said all records were
migrated to object form. The current snapshot does not support that:
`state/release.json` reports `snapshot-2`, `"migration": "partial"`, and
`active_label_shapes: ["text", "object"]`. `state/records.json` holds one legacy
string label (`legacy-a`) and one object label (`current-b`).

**Evidence:**

- `python3 -m unittest discover -s tests -v`: 2 tests passed
  (`test_object_labels`, `test_empty_list`). Neither test covers legacy or
  mixed lists, so a passing suite does not show the design.md contract is met.
- `list_labels` on `state/records.json`:
  `TypeError: string indices must be integers`.
- `list_labels([{"label": "Alpha"}])` (legacy only): same `TypeError`.
- `list_labels` on a mixed legacy + object list: same `TypeError`.
- `records.read_label` reads only `record["label"]["text"]`. The legacy and
  mixed-list subtask is checked above, but the current code does not do it.

**Reconciliation:**

- Code completion: **not met.** design.md says list_labels must read legacy,
  object and mixed lists in input order, and it allows no exception. Task 1
  cannot be marked `done` yet.
- Dashboard activation: separate from code completion. The operator notice in
  `state/release.json` is `pending`, and the Release coordinator owns it. It
  must be published, with its acknowledgement attached to the activation
  record, before the dashboard is activated. It does not block code completion
  and does not relax mixed-format support. Publishing it is outside this
  repository task.
- Independent review (`kk:review-code:isolated`): not run. This pass changed no
  code, and the current code already fails the acceptance contract. Run the
  review after the fix below.

**Remaining work for Task 1:**

1. Change `read_label` in records.py to handle string labels as well as
   `{"text": ...}` labels. Keep api.py's `list_labels` contract and input order.
2. Add unit tests for legacy-only and mixed lists. A mixed-list test should
   match `state/records.json` and expect `["Alpha", "Beta"]`.
3. Re-run the suite and the `state/records.json` check, then run
   `kk:review-code:isolated`.
4. Re-tick the implementation subtask, tick the rest, and set Task 1 to `done`. Record the operator
   notice as a pending activation prerequisite, not a code-completion
   blocker.
