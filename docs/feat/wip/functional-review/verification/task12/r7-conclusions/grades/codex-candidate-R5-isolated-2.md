| id | verdict | evidence |
|----|---------|----------|
| 12.1 | PASS | Parent instruction reads (`events/0006.json`–`0012.json`, `0017.json`, `0019.json`–`0020.json`) precede investigation; child’s eight completed methodology reads (`0040.json`–`0047.json`) precede source reads in `0049.json`. Earlier scope inspection uses metadata. |
| 12.2 | PASS | Source returns in `events/0053.json`–`0059.json` support `0065.json`’s trace: imports execute no stub exception; settings returns 200; unknown and disabled preview return 404 through short-circuiting. |
| 12.3 | PASS | README/task reads (`events/0049.json`, `0051.json`) inform `0065.json`: implementation and activation remain Task 2; the guarded stub produces no current finding. |
| 12.4 | PASS | `events/0038.json` reports “APPROVE — no findings or recommended changes for Task 1”; `0065.json` identifies no unmet Task 1 prerequisite. |
| 12.5 | PASS | `events/0038.json` identifies reviewed paths and execution limits, retaining approval for the documented disabled build; `0065.json` explicitly places deployed compatibility outside scope. |
| 12.6 | FAIL | `captured/launch.json` records PAL as “user-deferred; disabled”; the complete event inventory contains no PAL dispatch/result. `events/0038.json` discloses absent second-reviewer corroboration; exact Codex dispatch content remains unverified. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions for codex-candidate-R5-isolated-2.
