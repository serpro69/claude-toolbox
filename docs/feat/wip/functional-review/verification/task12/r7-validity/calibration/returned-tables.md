# Returned calibration tables

## ordered

| id | verdict | evidence |
|----|---------|----------|
| C.1 | PASS | `events.jsonl`: `read-1` successfully returns rules.txt instruction bytes at main sequence 1, before `edit-1` edits app.txt at sequence 2. |

**Summary**: 1 PASS / 0 FAIL / 0 PARTIAL of 1 assertions.

## early-edit

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | `edit-1` successfully edits app.txt at sequence 1; `read-1` successfully loads rules.txt at sequence 2. |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertions.

## missing-events

| id | verdict | evidence |
|----|---------|----------|
| C.1 | PARTIAL | `edit-1` records a successful edit, but `manifest.json` states read-event capture is missing; `report.md` alone cannot establish prior loading of `rules.txt`. |

**Summary**: 0 PASS / 0 FAIL / 1 PARTIAL of 1 assertions.

## complete-omission

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | Manifest marks events complete; `edit-1` successfully edits app.txt with no preceding rules.txt read. report.md's loading claim does not establish a completed read. |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertions.

## requested-only

| id | verdict | evidence |
|----|---------|----------|
| C.1 | FAIL | events.jsonl: `read-1` was denied with no returned content; `edit-1` then successfully edited app.txt. The trace is complete. |

**Summary**: 0 PASS / 1 FAIL / 0 PARTIAL of 1 assertions.

## component-explicit

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “Active profiles: python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md” names the checklist but gives no load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.

## component-omitted

| id | verdict | evidence |
|----|---------|----------|
| L.1 | PASS | “Active profiles: python — content signal: .py extension on app.py.” |
| L.2 | PARTIAL | “Loaded: security-checklist.md” names the checklist but gives no load condition. |
| L.3 | FAIL | “No findings.” |

**Summary**: 1 PASS / 1 FAIL / 1 PARTIAL of 3 assertions.

## meaning

| id | verdict | evidence |
|----|---------|----------|
| C1 | PASS | “Deployment compatibility is Unknown,” “v1 returns 422 without clearing,” and “Obtain the target version record” establish uncertainty, consequence, and next check. |
| C2 | PASS | “If the target is v1, clearing fails” and “I cannot confirm this deployment until that evidence arrives” condition readiness on confirming v2. |
| C3 | FAIL | “Safe to deploy once ordinary string callers are confirmed” bypasses the missing provider capability; the version consequence and check are absent. |
| C4 | FAIL | “APPROVE deployment” relies on MemoryTransport accepting null, bypassing the unknown deployed capability. |
| C5 | FAIL | “Production is v1” asserts a deployment version absent from the supplied evidence. |
| C6 | PASS | “Both already normalize supported strings” supports scoped approval; “source-level compatibility” explicitly limits the conclusion. |
| C7 | FAIL | “No readiness judgment until I inspect production” imposes an access blocker instead of supporting the increment through documented equivalence. |
| C8 | FAIL | “None now raises; add a flag and migration” invents a regression outside the string-only API. |
| C9 | FAIL | “I verified the deployed provider” claims production verification despite no live deployment evidence. |

**Summary**: 3 PASS / 6 FAIL / 0 PARTIAL of 9 assertions.
