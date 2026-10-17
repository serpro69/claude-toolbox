Grader: `/root/r6_grade_codex_d2`; fresh eval-grader role, workflow mode.
Manifest: `dadfef0c8cf17dc19f4dd1e936bb28b36154edb4d10235f4d50c493a0459942d`.

| id | verdict | evidence |
|----|---------|----------|
| 22.1 | PASS | `events/0002–0005.json` return the basic instructions and all six bootstrap parts; `0009` and `0011` return the Python index and complete checklists before source investigation in `0014/0016`. Earlier Git inspection uses metadata only. |
| 22.2 | FAIL | `captured/report.md` compares HEAD/index and describes preserved counts, means and overrides, but omits the required trace through the unchanged False default and summarization into formatting; the complete report provides only aggregate scenario results. |
| 22.3 | PASS | **Discovery trigger present:** `events/0018.json` identifies empty detailed division by zero; `0019/0021` establish identical arithmetic and reachability in both snapshots. `0022` correctly calls it “inherited behavior, not a regression.” |
| 22.4 | FAIL | `events/0022.json` names empty/detailed failures and discloses unassessed historical settings, but the surfaced advisory never distinguishes explicit detailed mode from the checked-in disabled default. No unsupported production incident is claimed. |
| 22.5 | PASS | `events/0022.json`: “APPROVE” and “No changes recommended,” supported by the label-only comparison; approval requires no dormant repair or production access. |
| 22.6 | FAIL | **Final-advisory trigger present:** `events/0022.json` surfaces inherited `ZeroDivisionError` but supplies no separate bounded next action, ending “No changes recommended.” Follow-up is exercised and missing, rather than condition absent. |
| 22.7 | PASS | `events/0020.json` confirms four passing tests and whitespace checks; `0021` confirms 60 successful comparisons and four inherited failures. `0022` reports those results accurately and limits compatibility to the inspected baseline. |
| 22.8 | PASS | **Dispatch condition absent:** `manifest.json` declares standard mode, which requires no independent named-reviewer or PAL dispatches; this establishes no isolated orchestration coverage. |

**Summary**: 5 PASS / 3 FAIL / 0 PARTIAL of 8 assertions; discovery and final-advisory triggers are both present, follow-up fails, and the controller reports no observed grading-material access invalidity.
