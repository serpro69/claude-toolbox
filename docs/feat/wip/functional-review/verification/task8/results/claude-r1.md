# Claude R1 baseline grader outputs

Each section preserves the returned table and summary from its fresh independent agent. Artifact paths are relative to `../inputs/<run>/`; event IDs identify captured events, not controller interpretations.

## claude-r1-standard-1-capture2 — /root/grade_claude_r1s1

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PARTIAL | e18.0/e20.0/e22.0 and e36.0–e52.0 return methodology and Python checklists before source investigation at e57.0; e6.0 only says “Launching skill,” leaving SKILL.md contents and complete profile detection unverified. |
| 6.2 | FAIL | `report.md` traces active A → failed B → cleanup B, omitting queued cleanup A after successful B and `active_connection`; retained source reads e60.0/e62.0 cover only cleanup. |
| 6.3 | FAIL | `report.md` correctly cites unconditional removal at `cleanup.py:3`, but substitutes active-A/cleanup-B and leaves consumer impact hypothetical instead of reporting B’s lost connection under the expected queued-cleanup trigger. |
| 6.4 | PASS | `report.md` proposes restoring `active["setup_id"] == setup_id` before removal, without unrelated locking, migrations, deployment controls or redesign. |
| 6.5 | FAIL | `report.md` gives P1 and REQUEST_CHANGES, but never distinguishes existing passing tests from the uncovered interleaving; its possible P0 impact remains speculative. |
| 6.6 | PASS | `manifest.json` identifies `mode: standard`; independent named-reviewer/PAL dispatches are not required. |

**Summary**: 2 PASS / 3 FAIL / 1 PARTIAL of 6 assertions.

## claude-r1-standard-2 — /root/grade_claude_r1s2

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PARTIAL | e17.0–e48.0 show process, protocol, and four Python checklist reads before the diff at e58.0; e6.0 only says “Launching skill,” leaving SKILL.md contents and complete profile detection unverified. |
| 6.2 | FAIL | e78.0 reads unchanged `setup.py`, but e115.0 traces two successful setups followed by stale cleanup, substituting successful A for the required failed A with queued cleanup. |
| 6.3 | PASS | e115.0 cites `cleanup.py:3`, identifies the removed ownership check, and explains that stale cleanup deletes the newer association so `active_connection` returns `None`; supported by `initial.patch` and e78.0. |
| 6.4 | PASS | e115.0 proposes restoring the `setup_id` ownership guard and adding a focused regression test, without requiring locking, migrations, deployment controls, or redesign. |
| 6.5 | FAIL | `report.md` requests changes and distinguishes existing tests from missing coverage, but assigns P0 without supporting critical impact; `expected-expected-results.json` supports P1 or justified P2, and the report acknowledges uncertain production reachability. |
| 6.6 | PASS | `manifest.json` specifies standard mode, which exempts independent dispatch requirements. |

**Summary**: 3 PASS / 2 FAIL / 1 PARTIAL of 6 assertions.

## claude-r1-isolated-1 — /root/grade_claude_r1i1

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | FAIL | Main reads `cleanup.py` at e30.0 before shared detection at e32.0 and profile resolution at e72.0–e74.0; e105.0 analyzes correctness before loading the PAL protocol. Child checklist reads precede its source reads. |
| 6.2 | PARTIAL | e94.0/e139.0 return unchanged `setup.py`; e160.0 traces begin A → begin B → complete B → cleanup A → `active_connection=None`, but does not establish A failing and queuing cleanup before B starts. |
| 6.3 | PASS | `report.md` cites `cleanup.py:3`, explains unconditional removal of the newer setup’s association, and identifies the resulting lost connection; this matches `initial.patch` and the expected outcome. |
| 6.4 | PASS | `report.md` proposes restoring the `setup_id` ownership guard and adding a regression test, without requiring unrelated locking, migrations, deployment controls, or redesign. |
| 6.5 | PASS | `report.md` supports P1 with silent connection loss, rejects the change, and distinguishes matching-owner tests from the missing stale-cleanup case; e160.0 explicitly identifies the review as static, with no execution performed. |
| 6.6 | FAIL | e110.0/e143.0 dispatch matching diff/setup/store references, mapped in `payload-events.jsonl`, and both results are retained; however, PAL reports `files_embedded: 0` at e170.0, while `report.md` claims independent corroboration without disclosing missing source coverage. |

**Summary**: 3 PASS / 2 FAIL / 1 PARTIAL of 6 assertions for `claude-r1-isolated-1`.

## claude-r1-isolated-2 — /root/grade_claude_r1i2

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | FAIL | Main reads the full diff at e38.0 and source “for context” at e46.0–e48.0 before detection/protocol/profile reads at e50.0–e76.0; these are not bounded routing reads. |
| 6.2 | FAIL | e96.0/e141.0 inspect unchanged `setup.py`, but e149.0 and `report.md` trace completed A → completed B → cleanup A, omitting the required failed A and queued cleanup. |
| 6.3 | FAIL | `report.md` correctly cites `cleanup.py:3` and B’s lost connection, but substitutes a completed-A trigger for the failed-A/queued-cleanup trigger in `initial/README.md` and `expected-expected-results.json`. |
| 6.4 | PASS | `report.md` restores the `setup_id` ownership guard and explicitly defers locking; its recommended fixes require no migration, deployment control or redesign. |
| 6.5 | FAIL | `report.md` recommends reverting and explains the test gap, but assigns P0 while asserting “dropped service + resource leak” despite acknowledging unknown connection lifecycle and no observed production ordering. |
| 6.6 | FAIL | e115.0/e145.0 dispatch matching diff/setup/store context and retain results, but PAL reports `files_embedded: 0` at e156.0; e166.0 and `report.md` claim independent corroboration without disclosing missing source coverage. |

**Summary**: 1 PASS / 5 FAIL / 0 PARTIAL of 6 assertions.
