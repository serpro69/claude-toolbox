| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | Completed bootstrap reads in `events/0006.json`, `0007.json`, `0008.json`, index read in `0011.json`, and all four checklist reads in `0013.json` precede subject investigation in `0016.json`; standard mode has no child actors. |
| 7.2 | PASS | `events/0016.json` returns README’s named release contract; `0018.json` returns full release revision `22140737b2bc5792b535f3f8ce16f7fa162101db` and its provider source separately from HEAD and staged client. |
| 7.3 | PASS | `captured/report.md` identifies `client.py:5` and traces settings applied → `ok` without `applied` → client exception with enhancement disabled; `events/0021.json` reproduces it. |
| 7.4 | PASS | `captured/report.md` reports one introduced incompatibility violating independent release, says pending task 2 cannot resolve this increment’s requirement, and reports no separate missing-provider finding. |
| 7.5 | PASS | `manifest.json` declares standard mode; `events/0018.json` records a successful direct `git show eval-release:provider/settings.py` with returned source. Isolated receipt obligations do not apply. |
| 7.6 | PASS | In standard mode, `events/0021.json` directly compares HEAD and staged clients against the historical provider: HEAD succeeds; staged client raises after applying both saves. |
| 7.7 | PASS | `captured/report.md` states `REQUEST_CHANGES` and marks staged client plus released provider **Blocked**, grounding the conclusion in historical-source reproduction without claiming a production incident. |
| 7.8 | PASS | `captured/report.md` proposes preserving legacy saves and requiring receipts only after provider support is established; it identifies the receipt-only stub as hiding the regression and requires no live access. |

**Summary**: 8 PASS / 0 FAIL / 0 PARTIAL of 8 assertions.
