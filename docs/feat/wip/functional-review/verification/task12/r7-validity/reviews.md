# Independent review checkpoints

## Fixture/rubric validity

A fresh design-reviewer reviewed the two cases, prospective rubric/examples,
assertion mapping and scoped feature requirements before measurement. Initial
disposition: CONCERNS_FOUND, one P2 (AMBIGUOUS): “Unicode whitespace” was insufficient
to prove all-string equivalence with Python str.strip(). All four protocol copies
now specify that exact rule. A focused recheck returned SOUND with no remaining
fixture/rubric blocker. No run or runtime claim came from that review.

## Source and host correction

A fresh code-reviewer inspected 31 initial scoped files and their unchanged
capture/grading/bundle consumers. It found no actionable source defect but returned
COMMENT while host runtime portability was unresolved. The inherited Linux helper
failed five local tests with killpg PermissionError after observing exited children.
No actor had launched; the failed attempt is retained in the execution notes.

The controller-only host_runtime.py correction accepts that Darwin EPERM only for
an unreaped, observed-exited leader and a successful bounded process-table snapshot
whose entire group is dead. Missing/live/malformed observations remain errors.
The wrapper is scoped to serial capture and restores the historical function.
A focused review covering 33 source files returned APPROVE with no P0–P3 findings.
The reviewer did not run tests. Root subsequently recorded 27 passing checks
(including 18 inherited runtime regressions, four denial controls and five fixture/
adapter checks), with an actual macOS descendant-state check replacing Linux /proc.

PAL remains user-deferred. These are independent source/validity judgments, not
external corroboration or behavioral acceptance. No systemic P0/P1 finding requires
indexing. [Final evidence/completion review](completion-review.md) approves closing
Task 12.14; its P3 calibration-path metadata correction is resolved.
