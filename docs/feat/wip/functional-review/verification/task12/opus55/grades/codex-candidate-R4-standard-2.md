Grader: `/root/grade55_codex_c_r4_s2`; fresh eval-grader role, workflow mode.
Manifest: `edf0ec827bfa9c77d485e60efc5b408b934d8fc1c879b9098815a8089a66bca3`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PASS | events/0003, 0006–0007, 0011 and 0013 return complete instructions and Python guidance before investigation; events/0008–0009 inspect filenames/metadata only. |
| 9.2 | PASS | events/0019–0020 inspect both readers, persisted records and unchanged API/writer/migration sources; events/0025 identifies the removed legacy fallback. |
| 9.3 | PASS | events/0021 reproduces initial and one-record-batch `KeyError('destination')`, with successful completed migration; events/0025 reports both failures, interruption of the entire listing and preserved addresses after completion. |
| 9.4 | PASS | events/0018 supplies the mixed-snapshot/background-batch contract; events/0025 returns `REQUEST_CHANGES`, marks compatibility “blocked” and limits verification to local snapshots. |
| 9.5 | PASS | events/0025 recommends restoring the fallback across initial/intermediate/completed states and explains that passing tests omit legacy records; events/0024 explicitly retains dual-shape reads during migration. |
| 9.6 | PASS | manifest.json declares `run.mode: standard`; the conditional independent-dispatch obligation does not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions; no grader-material access is observed in the retained events.
