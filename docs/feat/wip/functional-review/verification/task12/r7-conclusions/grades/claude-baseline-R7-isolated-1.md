| id | verdict | evidence |
|----|---------|----------|
| 14.1 | FAIL | Main source reads e37–e40 precede Python detection/index results e58/e60; main never loads resolved checklists. Child checklist reads e79–e88 precede its source reads. |
| 14.2 | FAIL | e92–e101 trace payload, caller and transport tests, but e117/e126 omit inferred normalization intent and a supported before/after explanation of preserved payload shape. |
| 14.3 | FAIL | captured/report.md discusses unknown old code and server semantics but never distinguishes the local Git base and MemoryTransport from a released/deployed provider baseline. |
| 14.4 | FAIL | e126 answers “Probably yes, but not confirmed”; it omits deployment-baseline evidence and a bounded action to obtain the applicable provider contract. |
| 14.5 | FAIL | Child e117 returns COMMENT, but final e126 replaces it with “Probably yes, but not confirmed,” without an unambiguous non-approval verdict. |
| 14.6 | PASS | e126 proposes local test execution, inspecting the cached old line and clarifying input semantics; it demands no credentials, production access, feature plan, rollout framework or speculative refactor. |
| 14.7 | FAIL | Isolated dispatch e68 explicitly lacks the raw diff; no PAL invocation/result exists in event-index.json, and e126 discloses the absent reviewer. |

**Summary**: 1 PASS / 6 FAIL / 0 PARTIAL of 7 assertions.
