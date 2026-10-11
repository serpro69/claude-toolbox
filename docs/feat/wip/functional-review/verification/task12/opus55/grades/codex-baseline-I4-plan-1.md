Grader: `/root/grade55_codex_b_i4_p1`; fresh eval-grader role, workflow mode.
Manifest: `c8062d0d375bc07e3b2ed212e9e3827164447cdb022d2f8bba809008581482e2`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | Manifest confirms plan mode, but events/0018 starts source inspection before events/0017 finishes loading Python test guidance; review checklists load later in events/0019. |
| 11.2 | PASS | events/0005 and events/0018 read the handoff and all current sources before dispatch events/0021; events/0024 identifies snapshot-2 as contradicting the completion claim. |
| 11.3 | PASS | events/0023 runs two passing tests; events/0022 reproduces three compatibility failures. events/0027 attributes the failure to `records.py:2` and identifies the snapshot as synthetic. |
| 11.4 | PASS | Controller-validated initial/final hashes match for both specification documents, runtime code, tests and state; final verification retains the hard compatibility requirement without a waiver. |
| 11.5 | PASS | captured/final/docs/feat/wip/label-reader/tasks.md keeps feature and Task 1 in-progress and unchecks mixed-format implementation. |
| 11.6 | FAIL | The final Task 1 Execution context records evidence, failure and repair steps, but assigns no code-repair owner and does not explicitly mark ownership unassigned. |
| 11.7 | PASS | Final tasks.md retains Release coordinator ownership, publication before activation, acknowledgement verification and permission for the notice to remain pending after code completion; no external action appears in the audited events. |
| 11.8 | PARTIAL | events/0021 and events/0026 retain reviewer identity but lack submitted handoff content; refreshed results in events/0054 cannot establish the required payload, and rubric revision 2 grants no I4 receipt/use fallback. |
| 11.9 | FAIL | events/0031 and final verification.md declare isolated review complete despite disabled PAL in captured/command.json; events/0034 does not identify incomplete review or explicitly distinguish unverified production state. |

**Summary**: 5 PASS / 3 FAIL / 1 PARTIAL of 9 assertions.

Controller note: PAL is user-deferred. The report still needs to disclose the
review limitation; the I4 handoff does not gain a receipt/use exception.
