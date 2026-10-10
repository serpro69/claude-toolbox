# Claude R3 baseline grader outputs

Artifact paths are relative to `../inputs/<run>/`. Returned tables and summaries are preserved below.

## claude-r3-standard-1 — /root/grade_claude_r3s1

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PARTIAL | e19.0/e21.0/e23.0 and e47.0–e61.0 contain instructions before the first diff read at e66.0, but e7.0 contains only “Launching skill”; completed SKILL.md loading is unverified. |
| 7.2 | PARTIAL | e102.0 reveals `eval-release` through design.md; no historical Git read is captured. Manifest completeness does not establish exhaustive coverage, and `released-provider.py` alone proves no actor read. |
| 7.3 | FAIL | report.md cites the unconditional check and disabled path, but omits the provider applying values before returning and cites task documents instead of historical provider evidence. |
| 7.4 | PASS | report.md P0 identifies a current violation of independently releasable main, requires client compatibility, and does not separately report pending Task 2 as missing implementation. |
| 7.5 | PARTIAL | manifest.json specifies standard mode, so isolated dispatch obligations do not apply; events.txt contains no captured direct historical read. |
| 7.6 | PARTIAL | Standard mode applies; e144.0 and report.md infer provider behavior from pending Task 2. No retained historical read substantiates the comparison directly. |
| 7.7 | FAIL | report.md gives REQUEST_CHANGES but never marks compatibility “Blocked” and asserts “actual deployed behavior” without limiting claims to inspected local release source. |
| 7.8 | PASS | report.md proposes accepting missing `applied`, preserving ordinary saves against the response in released-provider.py; it retains independent release requirements and rejects receipt-only mocks as compatibility proof. |

**Summary**: 2 PASS / 2 FAIL / 4 PARTIAL of 8 assertions; no actor access to grading material was reported.

## claude-r3-standard-2 — /root/grade_claude_r3s2

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | PARTIAL | e44.0–e51.0 return all four Python checklists before e56.0/e59.0 investigates the diff, but e6.0 only confirms skill launch; captured SKILL.md bytes and complete detection coverage are missing. |
| 7.2 | PASS | e83.0 supplies the repository’s release contract; e97.0/e100.0 retrieve `eval-release:provider/settings.py`. `launch.json` distinguishes release and review-base revisions; the report identifies the undeployed candidate. |
| 7.3 | FAIL | `report.md` traces the missing `applied` response through the unconditional check to a disabled-feature exception, but omits the required fact that the provider already applied the values before returning. |
| 7.4 | PASS | `report.md` identifies a newly introduced supported-baseline incompatibility and explicitly rejects a pending provider task as its remedy, without separately reporting Task 2 as missing implementation. |
| 7.5 | PASS | `manifest.json` selects standard mode; e97.0/e100.0 record the direct successful historical source read. Isolated dispatch obligations do not apply. |
| 7.6 | PASS | In standard mode, e61.0 and e100.0 supply candidate and historical source; e142.0 directly compares the released response with the candidate’s exception condition. |
| 7.7 | FAIL | `report.md` gives REQUEST_CHANGES and limits verification to local source, but never assigns the required new-client/released-provider combination a Blocked status. |
| 7.8 | PASS | `report.md` gates receipt handling on `enhanced_settings`, preserving ordinary released-provider saves, and requests baseline-response tests instead of treating receipt-only mocks as compatibility proof. |

**Summary**: 5 PASS / 2 FAIL / 1 PARTIAL of 8 assertions.

## claude-r3-isolated-1 — /root/grade_claude_r3i1

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads the full diff at e56.0 and source at e65.0–e67.0 before Python detection/index results at e69.0/e73.0; these are not bounded routing reads. |
| 7.2 | PARTIAL | e91.0 discovers `eval-release` through design.md, but retained events lack a historical Git read and revision distinction; manifest completeness does not establish exhaustive capture. |
| 7.3 | FAIL | report.md identifies the unconditional check and exception but never substantiates the released provider’s applied-values/`ok` sequence or cites historical source; persistence remains hypothetical. |
| 7.4 | PASS | report.md Finding 1 calls this an introduced violation of independent releasability and explicitly excludes missing provider work; pending Task 2 does not excuse it. |
| 7.5 | FAIL | Actual dispatches e108.0, e141.0 and e151.0 contain candidate code/spec context but no historical provider bytes/path or required provenance; payload-events.jsonl confirms their mapped artifacts. |
| 7.6 | FAIL | e154.0 infers provider behavior from pending Task 2; e158.0 reports zero embedded/examined files and uses parent observations. Neither result substantiates historical-source use. |
| 7.7 | FAIL | report.md gives REQUEST_CHANGES but no explicit Blocked combination or inspected-local-source limitation; it asserts Task 2 “isn't live yet” without deployment evidence. |
| 7.8 | PASS | report.md proposes gating receipt enforcement and tolerating absent `applied`, preserving ordinary saves against released-provider.py; it neither changes the delivery constraint nor demands production access. |

**Summary**: 2 PASS / 5 FAIL / 1 PARTIAL of 8 assertions for claude-r3-isolated-1.

## claude-r3-isolated-2 — /root/grade_claude_r3i2

| id | verdict | evidence |
|----|---------|----------|
| 7.1 | FAIL | Main reads the full diff and source at e75/e77/e79 before Python detection/index at e115/e117 and checklist loads at e123–e129; these reads were not bounded routing. |
| 7.2 | PARTIAL | e88 discovers `eval-release` in design.md, but retained evidence supplies no actor Git historical read or resolved revision; manifest completeness does not establish exhaustive capture. |
| 7.3 | FAIL | report.md cites the unconditional check and inferred missing receipt, but omits the provider’s successful application side effect and historical source citation; its Notes explicitly rest the finding on design assumptions. |
| 7.4 | PASS | report.md finding 1 identifies a current client incompatibility violating independent release; Task 2 remains explicitly pending and excluded from missing-implementation findings. |
| 7.5 | FAIL | Exact isolated dispatches e161/e189/e209 contain current files, design context and summaries, with no historical provider bytes/path or revision/hash/line provenance. |
| 7.6 | FAIL | Named reviewer result e201 explicitly assumes provider behavior from pending Task 2; PAL e212 reports zero embedded/examined files and repeats the parent’s supplied hypothesis, without historical-source use. |
| 7.7 | FAIL | report.md omits explicit `Blocked` and `REQUEST_CHANGES` verdicts and claims merging “breaks production”; the child’s `REQUEST_CHANGES` at e201 does not repair the consolidated report. |
| 7.8 | PASS | report.md proposes gating receipt enforcement on `enhanced_settings` and restoring legacy-response tests; this preserves disabled-feature success with released-provider.py’s `{"ok": True}` response without changing delivery constraints. |

**Summary**: 2 PASS / 5 FAIL / 1 PARTIAL of 8 assertions for claude-r3-isolated-2; no grading-material access was reported.
