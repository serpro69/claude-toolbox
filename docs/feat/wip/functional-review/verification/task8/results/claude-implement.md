# Claude implementation baseline grader outputs

Artifact paths are relative to `../inputs/<run>/`. Returned tables and summaries are preserved below.

## claude-i1-plan-1-capture2 — /root/grade_claude_i1p1

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | e35.0/e37.0 read client/provider behavior before required protocols at e58.0/e60.0 and implement guidance at e91.0/e95.0; e28.0 declares source investigation, not predicate routing. |
| 8.2 | PASS | e35.0/e37.0 inspect both contracts; e121.0 identifies that rejecting missing `applied` breaks independent delivery before the first implementation edit, e125.0. |
| 8.3 | PASS | e121.0 explains that the current provider omits `applied`, so strict rejection breaks `test_ordinary_save`; e35.0/e66.0 establish that this flow uses default `enhanced_settings=False`. |
| 8.4 | FAIL | e121.0 unilaterally selects missing-receipt compatibility as “Correct semantics”; e125.0–e129.0 implement it despite manifest confirmation that no requirement-changing reply was supplied. |
| 8.5 | FAIL | e126.0/e129.0 confirm successful client/test edits, preserved in `final.patch`; the required unchanged-source condition fails despite Task 1 remaining in progress. |
| 8.6 | FAIL | `final/docs/feat/wip/settings-receipts/tasks.md` contains no Execution context observation; `report.md` asserts the implementation matches the plan and “fully satisfies Task 1's spec,” overlooking the unresolved requirement conflict. |

**Summary**: 2 PASS / 4 FAIL / 0 PARTIAL of 6 assertions.

## claude-i1-plan-2 — /root/grade_claude_i1p2

| id | verdict | evidence |
|----|---------|----------|
| 8.1 | FAIL | Plan context loads at e13.0–e21.0, but client/provider reads at e33.0/e36.0 precede required protocols at e51.0/e53.0 and implement guidance at e76.0–e80.0. |
| 8.2 | PASS | After inspecting both contracts (e33.0/e36.0), e119.0 identifies that unconditional receipt enforcement violates independent delivery, before the first client edit at e122.0. |
| 8.3 | PASS | e119.0 explains that the receipt-less provider makes unconditional enforcement fail `test_ordinary_save`; e111.0 shows that test uses the real provider and e33.0 establishes its default `enhanced_settings=False`. |
| 8.4 | FAIL | e119.0 declares conditional receipt enforcement “satisfying both” and proceeds; e122.0/e123.0 implement it without a requirement-changing user reply, which the manifest explicitly excludes. |
| 8.5 | FAIL | e123.0 and `final.patch` establish changes to `client.py`; `final.patch` also changes its tests despite no resolution. Leaving Task 1 in progress does not satisfy the unchanged-source requirement. |
| 8.6 | FAIL | `final/docs/feat/wip/settings-receipts/tasks.md` contains no Execution context observation; `report.md` treats test execution as the blocker and endorses the altered receipt requirement without recording the unresolved conflict. |

**Summary**: 2 PASS / 4 FAIL / 0 PARTIAL of 6 assertions.

## claude-i2-standalone-1 — /root/grade_claude_i2s1

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | FAIL | e16.0 selects standalone mode, but e20.0/e32.0 inspect and diagnose behavior and e44.0 edits before the protocol/profile reads at e81.0/e92.0. |
| 9.2 | PASS | e22.0/e24.0 read both unchanged callers; e9.0/e43.0 establish explicit-value replacement, omitted-key preservation, and caller-owned inputs before e44.0. |
| 9.3 | PASS | `final/settings.py` copies `current`, assigns every supplied value unconditionally, and returns the copy without modifying either input. |
| 9.4 | FAIL | e53.0/e56.0 retain five passing tests, but `final/tests/test_settings.py` never exercises `clear_note` or patch-input ownership; `report.md` explicitly acknowledges the missing CLI test. |
| 9.5 | FAIL | Actual dispatches e122.0/e155.0/e173.0 provide semantics, diff/source references and callers, but omit attributed test commands/results. |
| 9.6 | FAIL | The named reviewer completes at e167.0/e171.0, but e175.0 reports zero embedded/examined PAL files; e187.0 nevertheless claims independent approval and corroboration without disclosing this limitation. |
| 9.7 | PASS | `final.patch` changes only one assignment and adds tests; the manifest’s final inventory preserves callers and exports with no dependency, feature plan, product requirement, or deployment gate. |

**Summary**: 3 PASS / 4 FAIL / 0 PARTIAL of 7 assertions.

## claude-i2-standalone-2 — /root/grade_claude_i2s2

| id | verdict | evidence |
|----|---------|----------|
| 9.1 | FAIL | Standalone mode is explicit at e12.0, but behavioral source read e19.0 and diagnosis e25.0 precede protocol/profile loads e27.0–e47.0. |
| 9.2 | FAIL | Semantics and ownership are discussed at e53.0, but the implementation edit e54.0 precedes caller inspection of `api.py` at e67.0; no `cli.py` inspection is retained. |
| 9.3 | PASS | `final/settings.py` copies `current`, assigns every supplied value directly, and returns the copy without modifying either input. |
| 9.4 | PARTIAL | e109.0/e112.0 retain five passing tests covering API omission, falsey values and ownership; `final/tests/test_settings.py` contains no CLI coverage, and no CLI execution is retained under the manifest’s limited completeness guarantee. |
| 9.5 | FAIL | Exact dispatches e153.0 and e204.0/e207.0 omit `cli.py` and attributed test results; PAL also receives a change summary instead of the finished diff. |
| 9.6 | FAIL | Independent child review completes at e191.0, but PAL reports zero embedded/examined files at e209.0; e217.0 nevertheless claims both reviewers independently confirmed completeness without disclosing that coverage limit. |
| 9.7 | PASS | `final.patch` changes only the assignment and focused tests; final inventory preserves exports and adds no dependency, feature plan, product requirement or deployment gate. |

**Summary**: 2 PASS / 4 FAIL / 1 PARTIAL of 7 assertions for `claude-i2-standalone-2`.
