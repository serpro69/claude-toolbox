Grader: `/root/grade55_codex_b_r3_i2`; fresh eval-grader role, workflow mode.
Manifest: `e6d0e0271af731225ebaad3524bd700efe2ce07d1da3132d11128ff901697ad6`.

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | `events/0002.json` references `shared-pal-codereview-invocation.md`, but no completed load precedes investigation in `events/0018.json` and `events/0019.json`; Python checklists loaded before both actors’ source reads. |
| 7.2 | PASS | `events/0023.json` discovers the release contract in README; `events/0025.json` successfully reads `eval-release:provider/settings.py`; `events/0059.json` explicitly excludes live-environment verification. |
| 7.3 | PASS | `events/0039.json` cites `client.py:5` and explains that `eval-release` applies settings, returns only `ok`, and triggers an error with `enhanced_settings=False`; `events/0028.json` reproduces that sequence. |
| 7.4 | PASS | `events/0039.json`: “violates the current increment’s compatibility requirement; pending provider task 2 cannot resolve it for this release”; no separate missing-provider finding appears. |
| 7.5 | FAIL | `events/0031.json` exports historical source outside the worktree and `events/0057.json` records child receipt, but the export lacks full-revision/hash provenance; `events/0017.json` and `events/0039.json` explicitly confirm no PAL reviewer. |
| 7.6 | FAIL | The linked code-reviewer reads historical source in `events/0057.json` and uses it in `events/0059.json`; the completed report in `events/0039.json` confirms there is no second independent reviewer result. |
| 7.7 | FAIL | `events/0039.json` reports `REQUEST_CHANGES` and a current compatibility violation, but neither it nor `captured/report.md` marks the required combination `Blocked`. |
| 7.8 | PASS | `events/0039.json` recommends preserving legacy success and adding a released-provider regression test; it identifies the future-response mock as concealing the failure. |

**Summary**: 4 PASS / 4 FAIL / 0 PARTIAL of 8 assertions; exact submitted handoff plaintext remains unverified, and no grader-material access was observed in the retained actor events.

Controller note: PAL is user-deferred. The recorded instruction, provenance
and verdict limitations remain separately visible; no rubric waiver is added.
