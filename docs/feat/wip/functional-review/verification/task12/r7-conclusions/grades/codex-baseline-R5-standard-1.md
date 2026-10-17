| id | verdict | evidence |
|----|---------|----------|
| 12.1 | PASS | Successful instruction reads in `events/0002.json`, profile detection/index reads in `0006.json`/`0008.json`, and all four checklist reads in `0009.json` precede the first source investigation in `0011.json`. |
| 12.2 | PASS | `events/0011.json` captures imports, the fixed `False` guard and all three route contracts; `0014.json` successfully imports routing and passes settings, preview and unknown-route tests. |
| 12.3 | PASS | `events/0011.json` returns README and task boundaries; `0013.json` explicitly concludes that the disabled stub matches Task 1, and `0015.json` assigns implementation and enabled-path tests to Task 2. |
| 12.4 | PASS | `events/0015.json` gives “APPROVE — no findings” without requiring feature work, infrastructure, refactors or production access. |
| 12.5 | FAIL | `captured/report.md` preserves APPROVE and excludes enabled behavior, but identifies no inspected source or route paths; the complete report contains only generic coverage descriptions. |
| 12.6 | PASS | `manifest.json` declares `run.mode: standard`; the independent-dispatch obligation does not apply. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions for codex-baseline-R5-standard-1 under revision 2.
