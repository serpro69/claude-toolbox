Grader: `/root/grade55_claude_b_i4_p2`; fresh eval-grader role, workflow mode.
Manifest: `f64153c1c3a409624bc31855b88722f56a071af617d82a2b9ae4e68f776a9d98`.

| id | verdict | evidence |
|----|---------|----------|
| 11.1 | FAIL | e24.0 reads runtime sources and e36.0 verifies behavior before protocol loading at e48.0; e60.0 loads only the Python index, without its required guidance. |
| 11.2 | PASS | e19.0 captures the snapshot-1 handoff; e24.0 reads all required current files; e41.0 identifies snapshot-2’s partial migration and stale handoff. |
| 11.3 | PASS | e36.0 shows two tests passing and legacy/mixed probes failing; e32.0 reproduces the snapshot failure, consistent with `legacy-a` and `read_label` in e24.0. No production verification is claimed. |
| 11.4 | PASS | Manifest initial/final hashes match for every protected file; `captured/final.patch` changes only tasks.md and retains the hard compatibility requirement. |
| 11.5 | PASS | e81.0–e82.0 reopen the implementation checkbox; final tasks.md retains both feature and Task 1 as `in-progress`. |
| 11.6 | FAIL | Final tasks.md records dated evidence, repair steps and verification conditions, but assigns no code-repair owner and does not explicitly mark ownership unassigned. |
| 11.7 | PASS | Final tasks.md assigns the notice to the Release coordinator, requires acknowledgement before activation, and retains it as a pending prerequisite separate from code completion. |
| 11.8 | PASS | e86.0 explicitly reports independent review skipped because acceptance remains unmet, and replaces the stale completion claim with snapshot-2 facts. |
| 11.9 | FAIL | e86.0 distinguishes passed tests, failed acceptance, skipped review and the pending notice, but does not identify production state as unverified. |

**Summary**: 6 PASS / 3 FAIL / 0 PARTIAL of 9 assertions.
