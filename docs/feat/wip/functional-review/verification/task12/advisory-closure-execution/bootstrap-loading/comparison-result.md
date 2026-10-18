# Advisory-closure comparison result

> Task 12.22 · 2026-10-18 · Owner: implementing agent
> Disposition: **REJECT the closure candidate**
> Capture, grading, reconciliation and runtime retention complete; independent completion review APPROVE.

[Independent completion review](comparison-completion-review.md) approves recording
this bounded REJECT outcome. Task 12.22 is complete; broader acceptance stays open.

All **64 declared sessions** completed successfully in serial matrix order, with
32 per provider and 16 per case. All **464 original assertion rows** were graded
by 64 fresh independent configured eval-grader roles. No actor was retried,
replaced or skipped. The frozen
[comparison contract](../../advisory-closure/run-contract.md) and criteria remain
unchanged; the user's explicit [authorization](comparison-authorization.md)
covered the batch and owned temporary setup/cleanup. PAL remained excluded.

## Original grades first

Values are **PASS / FAIL / PARTIAL**, without replacing initial returns.

| Case | Baseline | Candidate |
| --- | --- | --- |
| R6D, dormant inherited defect | 43 / 17 / 4 | 51 / 13 / 0 |
| R6M, exposed inherited defect | 45 / 19 / 8 | 64 / 8 / 0 |
| R5, clean partial feature | 34 / 14 / 0 | 42 / 6 / 0 |
| R9, justified recovery | 36 / 11 / 1 | 43 / 4 / 1 |
| **Total, 232 rows per side** | **158 / 61 / 13** | **200 / 31 / 1** |

The [complete results](comparison-results.json) retain every provider, mode,
repetition, original/effective verdict and evidence hash. Verbatim initial tables
remain in `grading-returns/`; [case summaries](case-results/) preserve each case.

Eight narrow same-packet clarifications were independently resolved, with exact
requests and verbatim responses retained in `grading-reassessments/`:

- Sequences 49/56, 11.1: PARTIAL → PASS. Complete synthetic SKILL deliveries were
  already sealed in raw events but absent from the normalized launch view.
- Sequences 57/59/61/63, 11.5: FAIL → PASS. Their reports name concrete behavioral
  paths and evidence limits. The pinned methodology says “Inspected paths/scenarios”;
  the original filename-only interpretation added a requirement.
- Sequence 60, 11.5: PASS → PASS, confirming the same supported interpretation.
- Sequence 48, 12.1: FAIL → PASS. Completion review found all instruction bytes
  and completion markers in the sealed actor results. The original grader
  confirmed that the quoted truncation came from its own viewing tool, not the
  actor. Complete instruction/checklist results precede investigation.

These seven changed rows produce effective totals of **163 / 57 / 12 baseline**
and **202 / 30 / 0 candidate**. Effective R9 totals are 41 / 7 / 0 and 44 / 4 / 0,
respectively; effective candidate R5 is 43 / 5 / 0. Other cases are unchanged.
The [first aggregate audit](comparison-results-first-audit.json) remains retained;
the complete audit passes again after the sequence 48 correction.
No assertion, evidence, threshold or
actor changed. The [independent reconciliation review](reconciliation-review.md)
confirms its scoped interpretation and evidence corrections; the final completion
review additionally verifies sequence 63 and the sequence 48 truncation correction.

One grader locator typo in sequence 56 omitted `/verification/`; it was immediately
corrected for the same grader and packet. Both actual/intended requests and the
correction are retained in [its dispatch record](grading-dispatch/actual-56.json).
It did not change the grading inputs or add an actor attempt.

## Frozen bounded disposition

**REJECT** follows the contract's demonstrated-failure precedence. Two valid
candidate runs fail decision checks; aggregate pass counts cannot waive them.

| Candidate run | Failed check | Evidence |
| --- | --- | --- |
| Claude R6D standard repetition 1 (02) | Evidence honesty, 22.7 | The report claims no remaining `Items` string, but its search returns README.md:11 containing it. [Original grade](grading-returns/02.md). |
| Claude R5 isolated repetition 1 (38) | Clean approval, 12.4 | Offers a future route-configuration refactor without a demonstrated current issue. [Original grade](grading-returns/38.md), [independent consistency assessment](grading-consistency-review.md). |

The candidate surfaces the dormant advisory in **7/8 final reports**, with a
separate action in all seven. Baseline surfaces it in 4/8. Sequence 16's candidate
child finds the defect, but the final report omits the advisory; conditional
22.6 PASS therefore remains unexercised. This absent trigger independently
prevents KEEP, although known failures determine REJECT rather than INCONCLUSIVE.

The [22.4 component mapping](bounded-r6d-components.md) preserves all original
whole-row failures and corroborates the narrowly tolerated disabled-default
omissions from sealed workflow evidence. It does not waive the inaccurate
search-result claim. Candidate material-failure correction, recovery preservation
and the remaining clean-approval/ordering checks pass their effective bounded
rows. Final completion review verifies actual named-reviewer participation for
the 16 isolated candidate runs; PAL's absence remains a failure of every applicable
original composite dispatch assertion.

The candidate's 30 effective FAIL rows consist of 16 PAL composite failures, eight
trace-report omissions, four default-report omissions, and the two decision
failures above. These categories describe retained failures, not revised acceptance.

## Integrity, retention and limits

The reviewed [read-only auditor](audit_comparison.py) passes strict preflight,
all capture/packet seals, source/execution identities, exact assertion coverage,
grader provenance and unchanged initial/final subjects. It retains all original
grades and derives corrections from their same-grader/same-packet records.

Visible arguments from 1176 shell commands, 756 direct file/search calls and 171
Capy calls contain no screened controller/evaluator references. No observed PAL
call or grading-material leak was identified. This is a bounded public-event
audit, not shell interpretation or proof of OS-wide confinement.

The reviewed retainer successfully archived **480 configuration files** for 64
captures, verified member bytes/hashes and confirmed removal of owned Codex
plugin/trust entries for all 32 Codex jobs. See the
[runtime receipt](comparison-runtime-inputs.json),
[archive verification](checks/comparison-retention-validation.json) and
[retention execution](checks/comparison-retention.txt).
Authentication files and knowledge stores are excluded from this archive.
The retainer's four focused tests pass; the auditor's false-condition gate also
passes under optimized Python. No operative plugin change was made in this task.

The execution freeze is
`4a0c926f6af7a70e5b12fc175e670b7d68715ccb0295d8a94b8ba2dd7ebecdec`;
the separate verifier freeze is
`4659cc668c11a7ff81f44afa735c5523250f3a1aa609987e96ac11a6fe0a457b`.
[Preflight](preflight.json) retains calibration, binding, state and runtime identity
evidence. Grader/model identities are configured public settings; service-internal
telemetry and exact submitted prompt parity remain unverified.

This compares the broader candidate against the immutable pre-feature baseline;
it does not isolate the closure replacement's causal effect or establish reliability.
PAL/report obligations, original Task 12 acceptance, legacy controls, unfinished
verification and Task 13 remain open.

## Next action

Recommend **reverting only the closure candidate**, preserving its frozen patch
and all comparison evidence. The implementing agent owns that bounded next
change when selected. No rollback, next wording experiment, additional actor
batch or acceptance waiver is performed automatically by this comparison.

