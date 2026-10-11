Grader: `/root/grade55_codex_c_r4_s1`; fresh eval-grader role, workflow mode.
Manifest: `d912dec6fbdd0c0a1341b3dbde3b268cd68a663e09d0b6b9ad5ac0aba381a898`.

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | PARTIAL | `events/0006.json`, `0007.json`, `0011.json`, and `0013.json` return complete methodology, detection, index, and checklist bytes before investigation at `0016.json`; completed loading of `SKILL.md` is not captured. |
| 9.2 | PASS | `events/0020.json` returns the snapshot and unchanged API, writer, and migration; `0019.json` shows the removed fallback, and `0026.json` identifies the legacy-record regression. |
| 9.3 | PASS | `events/0022.json` reproduces aborted listings with `KeyError('destination')` at zero and one migrated record, with successful fully migrated controls; `0026.json` reports both failures and completion behavior. |
| 9.4 | PASS | `events/0016.json` returns the explicit background-batch contract; `0026.json` gives `REQUEST_CHANGES`, marks migration compatibility “blocked,” and limits validation to the local JSON model. |
| 9.5 | PASS | `events/0026.json` recommends restoring the fallback under the contract requiring both shapes until completion, while explaining that passing tests cover only new writes and empty input. |
| 9.6 | PASS | `manifest.json` records `run.mode: standard`; independent reviewer and PAL dispatch obligations do not apply. |

**Summary**: 5 PASS / 0 FAIL / 1 PARTIAL of 6 assertions.

Controller note: absent entry-point delivery evidence remains PARTIAL; no
successful injection or actor skip is inferred.
