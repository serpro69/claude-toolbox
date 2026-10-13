| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PASS | `captured/events.jsonl` sequence 6 supplies the skill; complete instruction results e16.0–e26.0 and Python index/checklists e40.0/e47.0/e49.0 precede subject reads and diff investigation. Standard mode has no child actors. |
| 7.2 | PASS | README receipt e80.0 identifies `eval-release`; e98.0/e101.0 obtain its provider source and full revision, distinguishing the release from HEAD. `captured/report.md` separately names the staged candidate and limits deployment claims. |
| 7.3 | PASS | `captured/report.md` traces `enhanced_settings=False`: provider stores values and returns only `ok`; the unconditional `applied` check raises. Historical source e101.0 and candidate source e96.0 support the comparison. |
| 7.4 | PASS | `captured/report.md` calls the new check a violation of independent release requirements and excludes pending Task 2 from scope; its sole finding concerns the current client regression. |
| 7.5 | PASS | `manifest.json` declares standard mode; e98.0/e101.0 record successful direct reading of `eval-release:provider/settings.py`. Isolated handoff obligations do not apply. |
| 7.6 | PASS | In standard mode (`manifest.json`), candidate source e96.0 and historical source e101.0 directly substantiate the compatibility comparison reported in `captured/report.md`. |
| 7.7 | PASS | `captured/report.md` marks new client/released provider **Blocked**, issues **REQUEST_CHANGES**, and explicitly bounds conclusions to inspected local Git source with the reproduction unexecuted. |
| 7.8 | PASS | `captured/report.md` proposes accepting missing legacy receipts while rejecting negative receipts, preserving `eval-release` saves; it explicitly says the passing receipt stub does not cover the released provider. |

**Summary**: 8 PASS / 0 FAIL / 0 PARTIAL of 8 assertions.
