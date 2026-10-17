# Advisory closure: bounded candidate assessment

> Date: 2026-10-17
> Task: [12.18](tasks.md#task-1218-assess-and-prepare-a-bounded-advisory-closure-correction)
> Status: Task 12.18 complete; candidate locally checked and independently approved; behavioral comparison unrun
> Source before this change: `11b2c6efb0638605bb6acd3eb184edb9abd10f56`

## Decision and evidence

Prepare a small replacement in the two existing review closing branches. A report
that surfaces a substantiated inherited defect should give a concrete separate
follow-up when repair is outside the reviewed task. Its presence does not make an
otherwise supported increment unsafe. A review with no supported issue or required
check still closes without new work. This is a candidate for measurement, not an
accepted behavioral fix or a broader discovery obligation.

The [R6 diagnostic](verification/task12/r6-validity/diagnostic/README.md) retained
four 22.6 failures. All four complete R6D reports describe the inherited
empty-detailed-input exception, approve the label change correctly, and omit a
next action. The evidence is independently graded under the unchanged
[rubric](verification/task12/r6-validity/rubric.md); no reinterpretation is needed.

| Final report | Relevant observation |
| --- | --- |
| [Claude 1](verification/task12/r6-validity/diagnostic/grading/claude-candidate-R6D-standard-1/captured/report.md) | Reports the defect under coverage limits, explicitly excludes it from Findings, and states no changes are recommended. |
| [Claude 2](verification/task12/r6-validity/diagnostic/grading/claude-candidate-R6D-standard-2/captured/report.md) | Explains the inherited trigger and disabled default; ends with no changes recommended for this increment, without separate advice. |
| [Codex 1](verification/task12/r6-validity/diagnostic/grading/codex-candidate-R6D-standard-1/captured/report.md) | Compares successful outputs and inherited exceptions, then reports no actionable findings and no changes recommended. |
| [Codex 2](verification/task12/r6-validity/diagnostic/grading/codex-candidate-R6D-standard-2/captured/report.md) | Likewise demonstrates unchanged exceptional behavior without a follow-up. |

The practical loss is actionability, not a wrong verdict or demonstrated incident.
Claude 2 already scopes its closing sentence correctly: merely appending "for this
increment" cannot by itself satisfy the missing action.

## Source explanation and candidate boundary

Before this change, [standard closure](../../../../klaude-plugin/skills/review-code/review-process.md#10-close-the-review-or-handle-required-next-steps)
and [isolated closure](../../../../klaude-plugin/skills/review-code/review-isolated.md#step-9-present-report-and-confirm-next-steps)
select the no-action branch when there are no "actionable findings" or required
evidence/prerequisites. They direct the report to say no changes are recommended.
The [common method](../../../../klaude-plugin/skills/review-code/functional-review.md#evidence-qualified-reporting)
already asks for corrections to behavioral findings and separate attribution of
inherited issues. A surfaced advisory placed outside Findings can therefore be
treated as outside the action branch. The four reports are consistent with this
ambiguity; they do not isolate closure wording as its cause.

The candidate replaces existing closure text in both procedures. It explicitly
connects a surfaced, substantiated inherited defect to a concrete separate action
when repair is outside the task. It retains corrections for in-scope findings,
required evidence checks, scoped verdicts, and review-only authorization limits.
The standard evidence threshold still applies to optional notes; isolated closure
still excludes hypothetical future work. Common methodology, agent instructions,
loading order, descriptions and fixtures are unchanged.

The two canonical files grow by **19 and 37 whitespace-delimited words**,
respectively. Codex copies are generated mechanically. There is no new workflow
phase, report section, menu, mandatory dormant-path search, tracking artifact or
automatic issue creation. Distributed instructions contain no toolbox-doc links.

Rejected approaches: changing only the final sentence misses Claude 2's failure;
adding a mandatory advisory section or restoring remediation menus raises cost and
risks R5 regressions; adding a discovery rule addresses no demonstrated failure
in this diagnostic. A new common-method rule would duplicate existing correction
guidance without resolving which closing branch applies.

## Meaning-based checks before measurement

These are assessment examples, not new assertions or actor prompt hints. Reuse
the existing rubric and fixtures; interpret each complete report, not keywords.

| Situation | Expected meaning |
| --- | --- |
| R6D surfaces the inherited exception | Approve the label change; suggest separately defining empty detailed behavior and covering that boundary. Repair is not a merge condition. |
| R6D mentions the defect but says only "no changes to this increment" | Correct scoped verdict; follow-up remains missing under 22.6. |
| R6D does not surface an advisory | Scoped approval can pass; record the follow-up trigger as absent, never as demonstrated follow-up capability. |
| R6M newly exposes the inherited calculation failure | Request changes and give a correction that preserves required detailed output and empty-input success. "Inherited" must not excuse the new exposure. |
| R5 has unreachable pending functionality but no current defect | Approve without suggesting future implementation, a flag framework, cleanup or tracking work. |
| R9 recovery preserves the required retry guarantee | Approve without removing required recovery or inventing replacement mechanisms. |
| Repair of an inherited defect is explicitly part of the reviewed task | Keep that repair in scope; the separate-follow-up clause does not waive it. |
| Essential acceptance evidence remains unknown | Preserve the common method's qualified verdict and next check; this correction supplies no release approval. |
| Review-only request | Describe the follow-up; do not edit, file an issue or send a message without authorization. |

## Prospective comparison and adoption boundary

**Corrected probes completed 2026-10-17:** after explicit host/API approval,
[both fresh Claude bindings](verification/task12/advisory-closure-execution/high-effort-host/preflight-result.md)
completed with verified high-effort launch configuration. Baseline satisfies the
receipt audit; candidate omits all eight required detection-file reads. Readiness
stays BLOCKED, confirmed by independent completion review. Its guard finding is
resolved in a separately reviewed/frozen receipt-verification layer; five new
tests pass and the actual incomplete candidate is rejected.
No additional actor, measurement, adoption or operative instruction change follows.

**Effort correction reviewed 2026-10-17:** the [launcher successor](verification/task12/advisory-closure-execution/high-effort-host/README.md)
enforces/records high and passes nine new plus 26 predecessor tests. Independent
source review approves; frozen actor instructions remain unchanged. Corrected
host bindings are unrun because automatic approval review requires explicit
private-payload authorization to authenticated Claude/API. The earlier sandboxed
startup failure is preserved. Preflight and behavioral adoption remain open.

**Preflight executed 2026-10-17:** [Task 12.21's result](verification/task12/advisory-closure-execution/preflight-result.md)
records four binding and two state probes, but readiness is BLOCKED by unverified
Claude child effort against the declared high setting. Source/model receipts and
state checks remain supported; the effort assessment owns the concrete successor
launcher/fresh-binding proposal. No measured comparison or adoption follows yet.

**Adapter/calibration completed 2026-10-17:** [Task 12.20](verification/task12/advisory-closure-execution/README.md)
adds the independently reviewed execution adapter and freeze. Twenty-five fresh
calibration sessions match all 69 assertion judgments and 11 trigger values.
Binding/state probes, reviewed preflight, actor measurement and adoption remain
unrun; these are calibration results, not evidence of improved review behavior.

**Preparation completed 2026-10-17:** [Task 12.19's record](verification/task12/advisory-closure/README.md)
now preserves the candidate and inputs. Its independently reviewed
[run contract](verification/task12/advisory-closure/run-contract.md) is authoritative
for the concrete 64-session declaration and bounded disposition criteria. The
proposal below records the prior scope/cost reasoning. Execution, preflight and
adoption remain unrun; no historical assertion grade or feature gate is waived.

Owner: implementing agent. The next measurement should exercise R6D, R6M, R5 and
R9 recovery through ordinary standard and actual isolated review on Claude and
Codex, twice per side. Under the existing immutable pre-feature baseline rule,
that is **64 measured sessions**: four cases × two modes × two providers × two
revisions × two repetitions. This is a coverage/cost proposal, not a frozen run
contract or a selected batch. The user selected assessment and candidate review.

Before launch, independently review the concrete declaration; pin candidate,
baseline `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`, fixture/rubric/grader hashes,
runtime/models and permissions; calibrate grading and prove instruction binding
and fresh state. Preserve all attempts and use the same configuration on both
sides. Existing diagnostic captures are contextual evidence, not matching control
runs. A pre-feature comparison cannot isolate this replacement's incremental
effect; that claim would need a separately declared unchanged-current control.

Grade all applicable pinned assertions. Require exercised final-advisory
follow-up in both candidate repetitions of each R6D provider/mode, with correct
attribution and scoped approval; an absent advisory trigger is inconclusive for
that capability even when conditional 22.6 passes. Preserve R6M's required feature
and correction behavior, R5's no-action closure and R9's recovery guarantees.
Do not retry until an advisory appears or change criteria after seeing results.

The declaration must distinguish a bounded adoption decision from full-feature
acceptance, retain every FAIL/PARTIAL and specify disposition before capture.
PAL remains user-deferred: isolated orchestration rows cannot pass without its
required evidence. Existing trace/report failures are not waived by this proposal;
if they still fail, retain them and their existing ownership. Neither static checks
nor passing follow-up rows establish full diagnostic or feature acceptance.

Task 12.18 ends at an independently reviewed candidate and local verification.
No actor launch, new freeze, historical regrading or keep decision occurs here.
Original R6/R7 acceptance, unfinished implementation verification, capture gaps,
legacy controls and [Task 13](tasks.md#task-13-document-and-verify-the-complete-feature)
retain their existing status and next actions.

## Verification and review

Local checks on 2026-10-17, using installed Python 3.12.11:

- `make generate-kodex` passes its Go and plugin/Codex structure checks. A second
  generation preserves all 958 generated file hashes, including agent files.
- Nine instruction-packet tests pass, including full common-source inclusion,
  evaluator exclusion and routing/selected-checklist handling.
- `make plugin-graph` passes with its existing cycle warning and no broken edges
  or orphans. `go test ./...` passes.
- All twelve repository shell suites were attempted: eleven pass;
  `test/test-codex-hooks.sh` reproduces the pre-existing "Legacy: curl is denied"
  fixture mismatch. Its unchanged inputs, owner, cause and next action remain
  documented in the [R6 authoring record](verification/task12/r6-validity/README.md#environment-attempts-and-unrelated-test-follow-up).
  No full-repository-green claim is made.
- Local file links in all four changed feature documents resolve;
  `git diff --check` passes. Each review mode retains its single post-instruction
  investigation entry point, with routing and later focused reads unchanged.

Initial generation was blocked by the sandbox's protected `.codex/agents` path;
the permitted rerun succeeded. Two schema tests initially failed on uv-cache
access and passed with permitted cache access in offline mode. No dependencies,
persistent settings, hook fixtures or historical evidence were changed.

[Independent source review](reviews/advisory-closure-review.md) approves candidate
preparation with no findings. It verifies the four reports, preserved closure
contracts and generated text while attributing execution/freshness checks to the
parent. PAL remains user-deferred; no corroboration is claimed. These checks
establish packaging and source integrity; behavioral verification and adoption
remain unrun. Task 12.18 is complete within that boundary.
