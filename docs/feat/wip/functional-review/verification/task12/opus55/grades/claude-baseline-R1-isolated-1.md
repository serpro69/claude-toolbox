Grader: `/root/grade55_claude_b_r1_i1`; fresh eval-grader role, workflow mode.
Manifest: `47c44eacca03b996163aa80297e2684050f2d1b37eb0773e424089ad119fe279`.

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | FAIL | Main reads source at e28.0–e43.0 before the profile index at e63.0 and never reads its resolved checklists; child completes checklist reads before e82.0. |
| 6.2 | PASS | e89.0 returns unchanged `setup.py`; e106.0 traces A's queued cleanup deleting successful B's association and `active_connection` returning `None`. |
| 6.3 | PASS | e120.0 identifies `cleanup.py:3`, the supported ordering and silently lost connection; `captured/initial.patch` confirms removal of the ownership guard. |
| 6.4 | PASS | e106.0/e120.0 propose checking the existing `setup_id` before deletion, with no additional infrastructure required. |
| 6.5 | FAIL | e106.0/e120.0 assign P0 without supporting critical-impact evidence; `oracle/expected-results.json` supports P1 or justified P2. |
| 6.6 | FAIL | e64.0 explicitly supplies no diff; no PAL dispatch or result appears in `event-index.json`, and e120.0 confirms PAL did not run. |

**Summary**: 3 PASS / 3 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.

Controller note: PAL receipt/use was explicitly user-deferred. The unchanged
assertion still fails; this does not waive its other named-reviewer obligations.
