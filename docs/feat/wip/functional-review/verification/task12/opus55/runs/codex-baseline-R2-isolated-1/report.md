I’m using `kk:review-code` in isolated mode to review the staged save recovery update with independent reviewers.

The staged change touches only `service.py`, so I’m applying the Python review checklists. The external PAL reviewer isn’t available in this session; the isolated review will proceed with the independent code-reviewer agent.

All three existing tests pass. The reviewer is checking recovery edge cases against the README contract, particularly edited retries, fresh operation IDs, and completed-operation replay.

The isolated reviewer found three regressions, and I reproduced each: edited retries keep old values, fresh IDs reuse an earlier save, and replaying a completed operation can fail on another receipt write. I’m recording the two high-priority recovery patterns before presenting the report.

**Request changes:** the isolated code reviewer found two P1 issues and one P2. PAL was unavailable, so no second-reviewer corroboration was possible.

1. **P1 — Fresh operation IDs silently reuse an earlier save** ([service.py:2](/tmp/fr-opus55-matrix-20261011/codex-baseline-R2-isolated-1/service.py:2)). After `op-1` saves blue, `op-2` requesting red reports success but leaves blue active and creates no `op-2` recovery record. Restore lookup by `operation_id`.

2. **P1 — Edited retries report success with stale values** ([service.py:8](/tmp/fr-opus55-matrix-20261011/codex-baseline-R2-isolated-1/service.py:8)). After a receipt failure, retrying with red skips applying it because the record is already `applied`. Reapply the current submitted values for incomplete operations and update their recovery record.

3. **P2 — Completed-operation replay can fail** ([service.py:11](/tmp/fr-opus55-matrix-20261011/codex-baseline-R2-isolated-1/service.py:11)). Replaying a completed ID writes another receipt and can raise `ReceiptUnavailable`. Restore the completed-record early return.

All findings use the Python `security-checklist.md`, triggered by `.py`; confidence is 100% after runtime reproduction. The three existing tests pass but miss these cases. Both P1 patterns were indexed as `kk:review-findings`. No repository files were changed.

Would you like all three fixed, only the P1s, specific items, or no changes?

The [review skill](/home/sergio/.codex/plugins/cache/fr-opus55-c2d28c9e-20261011/kk/0.23.0/skills/review-code/SKILL.md) requires “Next steps confirmation from user,” which is why I’m asking before implementing fixes.
