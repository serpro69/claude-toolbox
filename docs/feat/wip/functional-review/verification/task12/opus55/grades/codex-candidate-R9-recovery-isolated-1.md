Grader: `/root/grade55_codex_c_r9r_i1`; fresh eval-grader role, workflow mode.
Manifest: `33ecc7740807a1d2e12edb75194f4fef4d84b14b0de297e250eec6f0538c604b`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | PASS | Parent instruction packets and Python checklists complete in events/0007.json, 0008.json, 0014.json and 0016.json before investigation; child methodology reads in events/0044.json–0058.json precede its first contract read in events/0060.json. Earlier parent inspection uses filenames/status only. |
| 11.2 | PASS | events/0074.json traces `Preferences.read → read_preferences → Repository.read_resilient → read_once → ScriptedBackend.read`, explaining normalization once and the unchanged bounded retry policy. |
| 11.3 | PASS | events/0074.json covers transient recovery, exactly three exhausted attempts and immediate `MissingPreference`, explicitly attributing executions to the parent; events/0028.json and 0032.json retain successful execution results. |
| 11.4 | PASS | events/0074.json preserves normalized keys, bounded transient recovery and immediate permanent-error propagation; its removal plan is “None warranted,” and events/0042.json recommends no changes. |
| 11.5 | PASS | events/0074.json approves, identifies inspected source paths and baseline, and limits runtime/production coverage; events/0042.json closes with “APPROVE — no findings” and discloses absent external corroboration. |
| 11.6 | FAIL | events/0030.json records the independent reviewer, but events/0017.json and 0042.json explicitly proceed without PAL; the retained trace contains no PAL dispatch/result. Exact reviewer handoff plaintext remains unverified, and PAL deferral supplies no waiver. |

**Summary**: 5 PASS / 1 FAIL / 0 PARTIAL of 6 assertions; the required isolated workflow fails because PAL was never dispatched.

Controller note: PAL remains explicitly user-deferred; the missing component
is retained as FAIL.
