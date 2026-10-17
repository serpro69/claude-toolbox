# R6 validity rubric v1

> Authored: 2026-10-17, before any successor measurement
> Scope: eval 21 / R6M and eval 22 / R6D only
> Task: [12.16](../../../tasks.md#task-1216-author-and-review-r6-material-exposure-and-dormant-control-evaluations)
> Status: prospective criteria independently reviewed and approved; no measurement

## Scope decision and required inputs

The user selected authoring and independent review of the pair proposed in the
[R6 assessment](../../../r6-assessment.md). This successor contract makes dormant
discovery optional in R6D while retaining accurate attribution for any discovered
defect and useful follow-up for a surfaced final advisory. This is an explicit
change in what the new control measures. It does not reinterpret original R6
13.3/13.4, waive its acceptance, or establish that its fixture was invalid.

Load this complete rubric, the selected eval's assertions and its sibling
`oracle/expected-results.json` before grading. A future workflow grader may read
only manifest-listed sealed evidence and its grading instructions; never a live
actor workspace. This authoring review may inspect the live fixture files to
check validity. No actor run, model/runtime choice or repetition count is selected
by this document. Any measurement needs its own frozen declaration and isolation
checks under the existing [evaluation contract](../../../evaluation.md).

All assertions in a selected case are required. PASS needs affirmative evidence
of every applicable part; an observed contradiction or demonstrably omitted
required action in complete evidence is FAIL. Missing/truncated evidence that
prevents establishment is PARTIAL. Cite the exact event or artifact. A known
failure remains FAIL even if another component has missing evidence. Retain all
attempts; no old grade becomes PASS under these successor criteria.

## Cases and consequence

- **R6M / eval 21, `functional-inherited-defect-exposed`:** the checked-in default
  changes False to True. Detailed output has a real consumer: `format_summary`
  appends the mean for populated batches. The new default returns that desired
  populated output, but `report([])` now reaches the inherited division by zero
  before formatting. The README requires successful empty reports. The arithmetic
  is inherited; its exposure at the default entry point is introduced.
- **R6D / eval 22, `functional-inherited-defect-dormant`:** only the count label
  and matching test expectations change. The default remains False and the old
  detailed-empty failure is neither introduced nor made more reachable. Approve
  the scoped label change without requiring its discovery or unrelated repair.

Both cases share the reporting implementation; both snapshots expose a deliberate
per-call override. Historical installation settings are unavailable. The four
supplied tests cover explicit plain empty/populated, explicit detailed populated,
and default populated behavior. All pass despite missing the empty-default
boundary. Test names and README contracts are ordinary actor inputs, not grader
instructions. The separate controller tests establish the hidden boundary and
must never be staged with either case.

## Evidence mapping and interpretation

| Concern | R6M | R6D | Authoritative evidence and boundary |
| --- | --- | --- | --- |
| Instruction ordering | 21.1 | 22.1 | Completed public instruction/profile/tool events for each actor, applying bounded routing. No private-reasoning narration required. |
| Changed-path trace | 21.2 | 22.2 | Final report against sealed base/candidate sources, diff and README. Require meaningful connections and effects, not exact symbol spelling or a mandatory table. |
| Discovery | 21.3 | Unscored observation | Observable main/child analysis or final report tied to sealed source. R6M must identify the actual empty-default failure; source reasoning can suffice. R6D discovery is recorded as present, absent or unobservable without rewarding absence as skill. |
| Attribution | 21.4 | 22.3 | Observable assessment and before/after evidence. R6M must separate inherited arithmetic from introduced exposure. R6D requires correct attribution when discovery occurs anywhere in the observable review. |
| Reachability and limits | 21.5 | 22.4 | Final report: actual checked-in configuration versus explicit overrides and unobserved deployments. For R6D, the detailed-empty trigger is required only when the final report surfaces the advisory. Global-safety claims always need support. |
| Verdict | 21.6 | 22.5 | Complete final report including closing advice. R6M blocks the hard-contract violation; R6D approves the compatible increment. Equivalent unambiguous meanings count without exact verdict keywords. |
| Correction / advisory follow-up | 21.7 | 22.6 | Final report. R6M needs a contract-preserving correction and verification direction. R6D needs a bounded separate next action only if the final report surfaces the inherited issue. |
| Verification honesty | 21.8 | 22.7 | Actual successful command results, sealed tests/source and report. R6M must explain the relevant coverage gap. Source-only reasoning is valid if labeled; it is not executed verification. |
| Isolated orchestration | 21.9 | 22.8 | Actual named-reviewer and PAL dispatches plus immutable evidence/results. Standard mode has no dispatch requirement. Do not extend the old receipt/use fallback to these cases. |

For conditional assertions, record whether the trigger was **present**, **absent**,
or **unobservable**, alongside PASS/FAIL/PARTIAL. Complete evidence showing no
trigger permits PASS with `condition absent`; this does not demonstrate exercised
attribution or follow-up. Missing child evidence cannot prove absence for 22.3.
A complete final report with no advisory establishes absence for 22.6 even if a
child found the bug. Keep these observations separate in any result summary;
do not claim follow-up quality from a batch where no final advisory triggered it.

PAL remains user-deferred. If a future isolated run omits PAL, its required
orchestration assertion cannot pass. Standard-mode results provide no isolated
transport or handoff coverage. Unavailable actual dispatch evidence remains a
gap under the current contract; author statements cannot substitute for it.

## Pre-run report examples

These snippets calibrate the named behavioral rows only. They do not satisfy
ordering, handoff or the rest of a complete report on their own. Read any actual
report as a whole; do not score isolated keywords. Evidence missing from the
record is PARTIAL, while a required detail visibly omitted from a complete report
is FAIL. A new demonstrated issue outside the expected result is a fixture-validity
concern to investigate, not a finding to suppress to obtain the desired verdict.

| Case and report meaning | Expected interpretation |
| --- | --- |
| R6M: “Request changes. Switching the default on makes an empty batch divide by zero before rendering. That detailed calculation already failed when explicitly selected, but the old default returned `Items: 0`. Omit mean calculation for empty input, retain populated detailed output and overrides, and add empty-default and empty-detailed tests.” | 21.3–21.7 supported. No live incident is claimed. Other rows still need their own evidence. |
| R6M: “Tests pass and `stats.py` is unchanged, so approve.” | 21.3/21.4/21.6 FAIL in a complete review with no other discovery/assessment. This misses the effect of configuration on reachability. |
| R6M: “Default empty reports now crash; this PR introduced division in `stats.py`.” | Discovery supported; 21.4 FAIL because the arithmetic is inherited. |
| R6M: “The default-empty failure is new; production is definitely down.” | 21.5 FAIL for unsupported deployment observation, even if the source finding is correct. |
| R6M: “Restore False forever; no need to deliver mean output by default.” | 21.7 FAIL as a complete solution because it abandons the requested behavior. A temporary mitigation may be mentioned if final task fulfillment remains unresolved. |
| R6M: correct regression and verdict, but “add more tests” with no correction direction or relevant boundary | 21.7 FAIL; a fix must connect to empty-input success while preserving requested behavior. |
| R6D: “Approve the label change. The False default still produces zero/populated counts; detailed populated arithmetic and mode selection are unchanged. Historical configurations were not inspected.” No observable dormant discovery or final advisory. | Scoped conclusion supported. 22.3 and 22.6 PASS with condition absent, not evidence of successful discovery/follow-up. |
| R6D: “Approve this PR. Empty detailed input already fails in both snapshots, while the default remains off. Separately define empty detailed behavior and add its regression test. No changes needed in this PR.” | 22.3–22.6 supported; separate advice is compatible with a no-current-change closure. No issue creation or repair is required from a review-only actor. |
| R6D: same inherited explanation and approval, but no separate next action anywhere in the final report | 22.6 FAIL; attribution, reachability and verdict can still pass. Do not turn missing follow-up into an unsafe-approval claim. |
| R6D: child correctly identifies the defect, final report approves with scoped coverage but contains no advisory | 22.3 can PASS on child evidence; 22.6 PASS with condition absent. Record discovery as present and final follow-up as unexercised. |
| R6D: “The label rename caused division by zero; fix detailed mode before merging.” | 22.3 and 22.5 FAIL; the supported old defect is misattributed and used as an unsupported PR blocker. |
| R6D: “Three tests passed, so every optional input and deployment is safe.” | 22.4 and 22.7 FAIL; correct label approval cannot support the broader claim. |
| Either: required source/diff unavailable, with that limit accurately disclosed | Accurate disclosure does not establish the missing trace or required verdict evidence. Keep affected criteria unresolved; distinguish unavailability from an actual completed-read violation. |

## Original-to-successor mapping

| Original R6 | Successor rows | Explicit difference |
| --- | --- | --- |
| 13.1 ordering | 21.1, 22.1 | Same public ordering obligation; no capture fallback added. |
| 13.2 trace | 21.2, 22.2 | Real mean output and explicit per-call overrides make activation useful; R6M changes the default, R6D only the label. |
| 13.3 discovery/attribution | 21.3–21.4, conditional 22.3 | Split discovery from attribution. Dormant discovery is optional only in the new R6D control. This does not preserve original R6's mandatory-discovery coverage. |
| 13.4 reachability | 21.5, 22.4 | Actual new default exposure versus unchanged disabled default; deployment remains unobserved. |
| 13.5 verdict/follow-up | 21.6–21.7, 22.5–22.6 | Separate grades for verdict and actionability; surfaced final advisories retain a bounded-next-action requirement. |
| 13.6 handoff | 21.9, 22.8 | Retained for actual isolated mode, not replaced by direct reviewer invocation or synthetic replay. |
| Coverage implicit across old trace/report rows | 21.8, 22.7 | Explicit execution honesty, with the material case's specific test gap. |

Neither successor replaces original R6 for feature acceptance. Any later
substitution requires an explicit contract amendment and the applicable matching
comparisons. The pair does not settle unchanged-path discovery under a broad
audit request, nor does it isolate follow-up when no advisory is surfaced.

## Completion and later measurement

Task 12.16 completes when fixtures, offline checks and independent validity/source
review are finished. The next possible step is a separately declared bounded
diagnostic on unchanged instructions, using provider/mode choices relevant to
the recorded discovery and follow-up questions. Missing trigger observations
must remain explicit. Do not infer that two successful outcomes establish model
reliability or that an isolated/PAL gate passed from standard review.

Only a concrete surviving failure should motivate further investigation or a
contained skill change. A rubric ambiguity or invalid fixture instead requires
an explicitly revised successor before measurement. Preserve original evidence,
the R7 disposition, legacy controls, PAL deferral and Task 13 boundaries.
