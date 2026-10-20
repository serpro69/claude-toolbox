# Acceptance reassessment

> Decision: 2026-10-20, user-authorized Task 12.24
> Scope: current acceptance policy and retained evidence; no actor reruns or regrading
> Governs: [evaluation](evaluation.md), [tasks](tasks.md), [handoff](follow-up.md)
> General learning: [ADR 0010](../../../adr/0010-proportionate-verification.md)

## Decision and authority

The user challenged treating probabilistic reviews as deterministic programs,
making optional report details into hard requirements, changing instructions
before validating tests, and accumulating instruction burden. They explicitly
accepted that an accurately explained bug can be useful without a prescribed
follow-up, then approved the acceptance reset and durable guidance.

This supersedes the all-assertions-pass-twice gate and the rule that only the
immutable pre-feature revision may serve as a comparison baseline. Historical
grades, frozen protocols and rejection/rollback records stay unchanged. They
describe the decisions made under those protocols, not current release vetoes.
No rejected wording is reinstated. This is a policy decision over existing
evidence, not a new estimate of reliability or a claim that every old test was bad.

Material failures concern missed consequential defects, wrong approval/blocking,
harmful advice or materially unsupported claims. Quality observations concern
useful but optional detail/advice. Evidence limits constrain what can be claimed.
A missing trace is not success; a disclosed unavailable tool is not proof that
the actor's reasoning failed. The controller must assess impact rather than
convert any red row into a veto.

## Dispositions from existing evidence

| Evidence | Assessment | Current acceptance effect |
| --- | --- | --- |
| [Original R6 assessment](r6-assessment.md): unchanged detailed-empty defect, disabled default, label-only change | Mandatory dormant discovery exceeds this increment's scope. Attribution/reachability matter when the issue is reported. | Retire mandatory discovery and mandatory separate follow-up as blockers. Scoped approval remains supported. |
| [R6M/R6D diagnostic](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r6-validity/diagnostic/README.md"): all eight decisions correct; four final dormant advisories have no action | The material regression is detected. Identifying the inherited bug is useful even without repair advice. Missing populated-path/default detail does not establish a wrong verdict. | Accept these outcomes for the assessed cases; retain 10 historical FAIL rows as observations, not unresolved gates. |
| [R7 validity diagnostic](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/r7-validity/README.md"): material unknown and benign cases yield the intended conclusions twice each | The original whitespace example did not establish the consequence of provider uncertainty. Omission of `PUT /settings` does not undo the correct compatibility reasoning. | Retire original R7's extra acceptance obligation. Use the clearer evidence for this concern; preserve the requirement to qualify materially unknown readiness. |
| [Closure comparison](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/comparison-result.md"): seven final advisories have actions; one child-only advisory is omitted | A coverage requirement demanding eight advisory triggers effectively made optional discovery mandatory. The omitted dormant advisory limits demonstrated follow-up coverage. | No all-eight-trigger gate. Missing optional advice/discovery does not veto the skill. The rolled-back candidate stays rolled back. |
| [Claude R6D report](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/grading/claude-candidate-R6D-standard-1/captured/report.md"): falsely says no `Items` string remains | Real accuracy error: the search returned README text. It does not change the label-only verdict or demonstrate that the closure change caused the error. | Retain as quality/accuracy feedback for this report. No blanket feature veto; a claim concealing a broken contract would be material. |
| [R5 note](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/grading/claude-candidate-R5-isolated-1/captured/report.md") and [consistency assessment](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/advisory-closure-execution/bootstrap-loading/grading-consistency-review.md") | The report approves and labels the future configuration note as not a current finding. The old literal grading is defensible; its shipping consequence is disproportionate. | Retire this optional-note veto. Advice that demands unnecessary work before approval or breaks required behavior remains material. |
| [R1 sequence](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-R1-standard-1.md"), [R2 detail](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/codex-candidate-R2-standard-2.md") and [I4 report](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-I4-plan-1.md") | Supported defects and justified verdicts survive sequence/detail omissions. I4 keeps the hard requirement open and does not claim test execution. | Retire exact-report-detail gates for these observations. No need to reproduce a runtime failure just to reject an already demonstrated broken implementation. Incorrect causal claims or false completion remain material. |
| [Observation ledger](assessment-observations.md): context ordering, entry/handoff and pre-edit receipts | Procedural deviations and missing transport evidence do not alone establish harmful reasoning. Required instruction order is still operative; observed receipt is not proof of exact prompt parity. | Retain limits without an automatic acceptance veto. No new narration, transport probe or ordering guard solely to clear historical rows. |
| [Entry-path correction](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/entry-path-no-pal/README.md") | Targeted acquisition checks improved; other modes are not thereby certified. | Keep the correction. Do not describe all historical acquisition misses as fixed. |
| [I2 repetition 1](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-I2-standalone-1.md"), [repetition 2](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-I2-standalone-2.md") and [acquisition assessment](follow-up.md#acquisition) | Tests were written but not executed; denial of one tool did not establish every permitted route unavailable. Implementation-mode diff acquisition also remains limited. | [Task 12.25](implementation-verification-assessment.md) completes the assessment: retain the disclosed execution/recovery limitation without another feature gate. Historical I2 verification remains incomplete; no runtime pass is invented. |
| User-deferred PAL and unrun legacy actor controls | PAL coverage is unavailable by decision; replay/source checks cannot certify live transport. Unrun controls are coverage limits, not demonstrated regressions. | Remove their blanket veto on local functional-review acceptance. Keep live two-reviewer claims unverified. Select future controls only for affected behavior or a concrete risk. |

These are dispositions, not replacement PASS/FAIL tables. Counts from different
revisions, modes and cases are not pooled into a success rate. The broader
pre-feature comparisons cannot isolate the effect of a later wording change.

## Remaining work and stopping condition

**Task 12.25 is complete and Task 12 is closed** under the revised policy.
The [completed assessment](implementation-verification-assessment.md) retains the
real I2 execution shortfall and inaccurate blanket shell-unavailability inference.
The reports disclose unrun checks, saved patches pass retrospective tests, I3's
edits are exact and I4 keeps its hard requirement open. Independent review finds
no additional instruction defect or harmful resulting patch requiring a new
correction or batch. This accepts the feature with a documented recovery
limitation; it does not complete historical actor verification.

Task 13's implementing agent owns carrying that limitation into the final summary.
Revisit only when consequential new evidence or changed verification/recovery
instructions make it decision-relevant. Any later diagnostic must name that
question and use an immediate-predecessor comparison for a targeted change.
Retired R6/R7, report-detail and receipt gates remain retired.

Task 13 retains final documentation, applicable repository checks, source/spec
review and the separately human-owned release archive. Its evidence reconciliation
uses this policy; obsolete grade gates cannot block it again. No full-feature
completion or improved actor reliability is claimed by Task 12.24.

**Subsequent completion:** Tasks 13.1–13.6 now pass their final checks and independent
reviews; see [verification-summary.md](verification-summary.md). Only the
human-owned release/tooling/archive work in Task 13.7 remains, with no new actor
performance claim.

## Policy checks for this change

The following retained examples check the decision rule without new model runs:

| Example | Required policy judgment |
| --- | --- |
| R6D report explains the inherited empty-input crash and approves, without follow-up | Accept the scoped review; optional next action is not a hard failure. |
| R6M default newly reaches that crash, but a hypothetical report approves because arithmetic is unchanged | Material failure: approval violates the explicit empty-report contract. This is a policy counterexample, not an observed passing actor. |
| R7M correctly withholds readiness while omitting the endpoint name | Accept the material conclusion; retain the report-completeness observation. |
| I2 writes tests but does not run them | Evidence of written tests only; preserve the unresolved execution obligation when it is required and available. |

[Source/structural verification and independent review](reviews/verification-policy-review.md)
complete Task 12.24 with APPROVE and no findings. They establish policy integration
and consistency, not end-to-end LLM behavior.
