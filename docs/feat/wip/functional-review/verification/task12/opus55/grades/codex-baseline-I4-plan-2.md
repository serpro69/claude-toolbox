Grader: `/root/grade55_codex_b_i4_p2`; fresh eval-grader role, workflow mode.
Manifest: `d3b333cc71c1119b494c40872c7438aa5377f74efab930cf5ae8c06bda61eab0`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | `events/0015.json` investigates source behavior before review checklists load in `0017`; the parent trace also lacks required review-process and PAL-protocol reads referenced in `0009`/`0013`. |
| 11.2 | PASS | `0015` reads all five current code/test/state files and the old handoff; `0016` identifies snapshot-2’s mixed shapes before dispatch `0020`. |
| 11.3 | PASS | `0022` executes two passing tests; `0021` reports snapshot-2, legacy-a, and three legacy/mixed failures; the verification record identifies synthetic rather than production evidence. |
| 11.4 | PASS | Controller-validated manifest hashes match for all seven immutable files; `0031` confirms protected files unchanged, and `0030` preserves the hard compatibility requirement. |
| 11.5 | PASS | Final `tasks.md` keeps feature and Task 1 in-progress and changes the mixed-format implementation checkbox to unchecked. |
| 11.6 | FAIL | Final `tasks.md` records stale/current evidence, failures and repair steps, but supplies neither a code-repair owner nor an explicitly unassigned owner. |
| 11.7 | PASS | Final `tasks.md` assigns notice publication and acknowledgement to the Release coordinator, permits it after code completion, and explicitly rejects a compatibility waiver. |
| 11.8 | PARTIAL | `0020`/`0025` identify dispatch and follow-up recipients without submitted context; refreshed handoff contents remain unverified, and rubric revision 2 provides no I4 receipt/use fallback. |
| 11.9 | FAIL | Final verification declares isolated review “completed” despite deferred PAL and no waiver; final response `0033` also omits explicit production-state limits. |

**Summary**: 5 PASS / 3 FAIL / 1 PARTIAL of 9 assertions; no grading-material access was observed in the retained actor events.

Controller note: PAL is user-deferred; review completion still requires an
accurate limitation disclosure. No I4 receipt/use fallback is added.
