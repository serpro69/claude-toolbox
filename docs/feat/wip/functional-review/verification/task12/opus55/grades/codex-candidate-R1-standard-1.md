Grader: `/root/grade55_codex_c_r1_s1`; fresh eval-grader role, workflow mode.
Manifest: `da49e1ac47cc07fa13744e9be5036987e28aee6275ff61246788e79f14098bf2`.

| id | verdict | evidence |
|----|---------|----------|
| 6.1 | PASS | `events/0005.json`–`0010.json`, `0017.json`, and `0019.json`–`0020.json` retain successful instruction reads through packet-end markers before the first subject read in `0025.json`; earlier repository reads contain filenames/status only. |
| 6.2 | PASS | `events/0028.json` returns unchanged `setup.py`; `0036.json` executes failed A → completed B → cleanup A and observes B’s connection becoming `None`. |
| 6.3 | PASS | `events/0041.json` identifies unconditional deletion at `cleanup.py:3`, describes the delayed-cleanup trigger and lost connection; `0030.json` confirms the introduced removal. |
| 6.4 | PASS | `events/0041.json` proposes restoring `association["setup_id"] == setup_id` while retaining pending cleanup, with focused regression coverage. |
| 6.5 | PASS | `events/0041.json` gives P1 and `REQUEST_CHANGES`; `0036.json` demonstrates connection loss against HEAD, while `0037.json` confirms the two existing tests pass. |
| 6.6 | PASS | `manifest.json` records `run.mode: "standard"`; the independent-dispatch obligation does not apply. |

**Summary**: 6 PASS / 0 FAIL / 0 PARTIAL of 6 assertions; no grading-material access appears in the retained actor events.
