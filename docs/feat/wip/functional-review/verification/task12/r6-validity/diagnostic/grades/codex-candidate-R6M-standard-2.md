Grader: `/root/r6_grade_codex_m2`; fresh eval-grader role, workflow mode.
Manifest: `772ed34958285a01952be1a6aa681c5816beb6821608739ebed9bf2f2e9eb4cf`.

| id | verdict | evidence |
|----|---------|----------|
| 21.1 | PASS | Events 0002–0005 return common instructions and all detection rules; 0010/0012 return Python index/checklists before investigation in 0014. Child condition absent: standard mode, no children. |
| 21.2 | FAIL | Complete final report (0023) claims “Traced configuration through reporting, statistics, and formatting,” but omits the changed populated-default test expectation and explanation of preserved populated explicit-detailed behavior. Events 0016/0018 establish these facts but cannot replace required reporting. |
| 21.3 | PASS | Event 0023 identifies default `report([])` reaching unguarded division instead of README-required `Items: 0`; 0016 establishes division precedes formatting, and 0018 reproduces `ZeroDivisionError`. |
| 21.4 | PASS | Event 0023: “Explicit `detailed=True` already had this defect; this change exposes it through the default.” Event 0018 confirms inherited explicit failure and newly failing default calls. |
| 21.5 | PASS | Event 0023 ties the regression to enabling detailed reports through config.py, contrasts successful HEAD calls with inherited explicit-detailed failure, and states historical installations were not assessed. Event 0016 confirms False→True; no production incident is claimed. |
| 21.6 | PASS | Event 0023 gives “REQUEST_CHANGES — one P1 finding” for the empty-batch contract violation despite four passing tests. |
| 21.7 | PASS | Event 0023 recommends skipping mean calculation only for empty batches, preserving their count summary, and adding omitted/`None`/`True` empty-input coverage; this bounded correction retains populated arithmetic and override selection. |
| 21.8 | PASS | Event 0023 distinguishes four existing passing tests from additional boundary probes and requests missing empty-mode coverage. Event 0018 supports the execution claims; 0020 confirms Python 3.12.11. |
| 21.9 | PASS | Condition absent: manifest `run.mode` is `standard` and dispatch completeness explicitly records no isolated-dispatch requirement; this establishes no isolated or PAL coverage. |

**Summary**: 8 PASS / 1 FAIL / 0 PARTIAL of 9 assertions for `codex-candidate-R6M-standard-2`.
