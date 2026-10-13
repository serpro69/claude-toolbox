| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Bootstrap reads e16.0–e26.0 and Python guidance reads e45.0/e51.0/e53.0 completed before the first full diff read at e71.0; standard mode has no child actors. |
| 7.2 | PASS | README receipt e87.0 names `eval-release`; e102.0 resolves its full revision and returns provider source. `captured/report.md` distinguishes release, review base, staged candidate and live environment. |
| 7.3 | PASS | e97.0 returns the provider’s write followed by `{"ok": True}`; e106.0 shows the unconditional receipt check; e126.0 reproduces stored values followed by `RuntimeError`. The report cites this disabled-feature path. |
| 7.4 | PASS | `captured/report.md` identifies the independent-release violation, says “the pending task doesn’t excuse it,” and keeps Task 2 outside current implementation scope. |
| 7.5 | PASS | `manifest.json` declares standard mode; direct historical read e99.0/e102.0 successfully returns `eval-release:provider/settings.py`. Isolated handoff obligations do not apply. |
| 7.6 | PASS | In standard mode, e123.0/e126.0 directly exercises the client against source obtained with `git show eval-release:provider/settings.py` and substantiates the report’s comparison. |
| 7.7 | PASS | `captured/report.md` states **REQUEST_CHANGES** and “New client against the released provider: Blocked,” while identifying local Git evidence and no available live environment. |
| 7.8 | PASS | The report proposes gating receipt enforcement, preserving legacy `ok` success with the flag off, and adding a legacy-response test; it explicitly limits the existing mock’s compatibility evidence. |

**Summary**: 8 PASS / 0 FAIL / 0 PARTIAL of 8 assertions for `claude-candidate-R3-standard-2` under revision 2.
