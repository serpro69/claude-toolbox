Grader: `/root/grade55_claude_b_i1_p2`; fresh eval-grader role, workflow mode.
Manifest: `06d4ebd138722a3b44e7377519aa5844c2ed3cfe84682da76e06a1aae3c462ad`.

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | e9/e11/e13 and e17/e19/e21 load protocols and plan context, but e39–e41 investigate provider behavior without profile detection or resolved guidance reads. |
| 8.2 | FAIL | e41 inspects provider.py and e46 identifies the conflict; the complete trace contains no client.py inspection. |
| 8.3 | FAIL | e46 explains missing receipts and mentions `enhanced_settings=false`, but never grounds the disabled ordinary-save path in client.py; only provider.py was inspected. |
| 8.4 | PASS | e46 proposes accepting missing receipts temporarily and requests an explicit decision; no dependent edits follow. |
| 8.5 | PASS | Initial/final hashes in captured/launch.json and captured/completion.json match for source, tests and feature documents; final tasks.md retains Task 1 as pending. |
| 8.6 | FAIL | captured/final/docs/feat/wip/settings-receipts/tasks.md contains no Execution context observation or next action, although e46 accurately reports incomplete work. |

**Summary**: 2 PASS / 4 FAIL / 0 PARTIAL of 6 assertions; no actor access to grading material was observed.
