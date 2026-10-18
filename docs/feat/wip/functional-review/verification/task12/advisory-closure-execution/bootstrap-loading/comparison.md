# Advisory-closure measured comparison

> Task 12.22 · 2026-10-18
> Status: complete — 64 captures, 464 original grades and independent completion review APPROVE
> Bounded disposition: **REJECT**
> Owner: implementing agent

The [result report](comparison-result.md) records original and effective grades,
the two demonstrated candidate decision failures, advisory-trigger coverage,
runtime retention, evidence limits and the recommended next action.
[Machine-readable results](comparison-results.json) retain every run and assertion;
[bounded decision rows](bounded-decision-checks.json) preserve the frozen mapping.
[Independent completion review](comparison-completion-review.md) approves this
record and finds no outstanding prerequisite for the bounded decision.

The user selected the frozen comparison after successful preflight, then explicitly
answered **“yes”** to the concrete 64-session transfer/setup request. See
[authorization](comparison-authorization.md). The earlier
[automatic approval rejection](comparison-approval-result.json) occurred before
any process creation and remains retained; explicit approval resolved that blocker.

All 64 inputs were [prepared](checks/comparison-prepare.txt) and
[validated](checks/comparison-validation.json) before the first capture. The
reviewed `listing_guard.py run` ran the full serial matrix once; exec session 20564
completed exit 0. Every capture has successful sealed completion and unchanged
subjects. No actor retry, skip, overwrite, source/rubric/threshold change or PAL
resumption occurred.

[Preflight](preflight.json), the execution freeze
`4a0c926f6af7a70e5b12fc175e670b7d68715ccb0295d8a94b8ba2dd7ebecdec`
and separate verifier freeze
`4659cc668c11a7ff81f44afa735c5523250f3a1aa609987e96ac11a6fe0a457b`
retain their original identities. The reviewed post-capture retainer archived 480
runtime files, verified their hashes and confirmed owned Codex cleanup for 32 jobs.
See [retention receipt](comparison-runtime-inputs.json).

Exact primary requests, configured roles and fresh grader identities are retained
in `grading-dispatch/`, original tables in `grading-returns/`, and narrow
same-packet clarifications in `grading-reassessments/`. The
[reconciliation review](reconciliation-review.md) preserves resolved audit findings
and independently checked correction reasoning. Original FAIL/PARTIAL rows are
never overwritten.

The comparison does not establish causal attribution, reliability or full feature
acceptance. Original Task 12/PAL/report obligations, legacy controls, unfinished
verification and Task 13 remain open. Recommend reverting only the closure
candidate when selected; no rollback or next experiment follows automatically.
