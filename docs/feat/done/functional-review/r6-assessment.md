# R6: inherited defects and review scope

> Date: 2026-10-17
> Task: [12.15](tasks.md#task-1215-assess-r6-evaluation-validity-and-review-scope)
> Scope: assessment and proposed successor criteria; no actor measurement or instruction change
> Evidence: historical [matrix contract](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/run-contract.md"), candidate `581dd0e1`, baseline `c2d28c9e`

## Decision

**Investigate evaluation validity; do not add a broader discovery obligation to
the skill.** R6 demonstrates a real inherited bug, but its label-only change
neither reaches a new failing path nor worsens one. Missing that bug is a failure
under R6's required assertions; it does not demonstrate an unsafe approval of
this increment. Finding it remains useful. The tiny adjacent calculation makes
discovery reasonable, but one such fixture cannot justify auditing every dormant
path during ordinary review.

Keep the separate requirement for a bounded follow-up when the final report
surfaces the defect. The observed omissions lose actionability; they do not
establish misattribution, a false production claim or an incorrect PR verdict.
Assess the whole report: “no changes to this PR” is compatible with a separate
advisory. The phrase “No changes recommended” alone does not settle its meaning.

The next proposed task is to author an affected-path case and dormant control,
with reviewed grading examples. Test unchanged instructions only after that
prospective contract is settled. Original R6 fixtures, assertions, grades and
acceptance remain unchanged; this assessment neither invalidates the old eval
nor replaces it for feature acceptance.

## What the evidence establishes

The [ordinary prompt and assertions](../../../../klaude-plugin/skills/review-code/evals/functional-inherited-conditional-defect/eval.json)
ask for review of a staged batch-report label change. The [README](../../../../klaude-plugin/skills/review-code/evals/functional-inherited-conditional-defect/test-files/after/README.md)
requires preserving calculations and explicitly excludes activating or redesigning
detailed reporting. Only `formatting.py` and two test expectations change.

| Scenario | Before | After | Consequence |
| --- | --- | --- | --- |
| Checked-in `DETAILED_REPORT=False`, `report([])` | `Items: 0` | `Records: 0` | Requested label change; empty batches still succeed. |
| Same configuration, `report([2, 4])` | `Items: 2` | `Records: 2` | Counts preserved. |
| `summarize([2, 4], detailed=True)` | count 2, mean 3 | Same | Existing populated detailed calculation preserved. |
| `summarize([], detailed=True)` | `ZeroDivisionError` | Same | Genuine inherited defect; checked-in `report` does not take this branch. |

These are source comparisons and local reproductions, not deployment evidence.
Historical installation settings remain unknown. The existing three tests pass
on both snapshots and omit the detailed-empty boundary. Their passing result
establishes neither absence of that bug nor an obligation to repair it in this PR.

The historical candidate observations separate as follows:

| Observation and exact grades | Practical meaning |
| --- | --- |
| Codex standard [1](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/codex-candidate-R6-standard-1.md"), [2](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/codex-candidate-R6-standard-2.md"): 13.3/13.4 FAIL, 13.2/13.5 PASS. Matching baselines also fail 13.3/13.4. | Both reports inspect the relevant caller/configuration and correctly approve the label change, but omit inherited discovery and its reachability distinction. Four failed rows describe two missed reports, not four independent defects or a candidate regression. |
| Claude standard [1](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-R6-standard-1.md"), [2](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-R6-standard-2.md"): 13.3/13.4 PASS, 13.5 FAIL. Matching baselines pass. | Both find and correctly attribute the bug, but omit a bounded next action. This is an observed follow-up regression under the pinned contract. |
| Codex isolated [1](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/codex-candidate-R6-isolated-1.md"): 13.3/13.4 PASS, 13.5 FAIL; [2](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/codex-candidate-R6-isolated-2.md"): all three PASS. | Repetition 1 surfaces the advisory without a next action. In repetition 2 the child identifies it but the final report omits it, so conditional 13.5 passes. This does not establish better final-report follow-up. |
| Claude isolated [1](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-R6-isolated-1.md"): 13.2/13.5 FAIL; [2](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grades/claude-candidate-R6-isolated-2.md"): both PASS. | Repetition 1 lacks the actual diff and withholds approval. That acquisition failure is distinct from dormant-defect scope or missing advice. |

All isolated candidate 13.6 results remain FAIL with PAL unavailable; Codex
isolated repetition 1 also retains a 13.1 receipt PARTIAL. Neither is evidence
for broader bug discovery. These are earlier-revision observations, not a fresh
test of current skills or an estimate of model reliability.

The [Claude repetition 2 report](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grading/claude-candidate-R6-standard-2/captured/report.md")
clearly describes the inherited failure and scoped approval, then closes without
any next action. Its [baseline](../../../archives/feature-evidence/functional-review.md "Archive member: payload/docs/feat/wip/functional-review/verification/task12/opus55/grading/claude-baseline-R6-standard-2/captured/report.md")
offers a separate follow-up, alongside a lengthy remediation menu. Retaining a
useful advisory does not require restoring that menu. Current
[standard](../../../../klaude-plugin/skills/review-code/review-process.md#10-close-the-review-or-handle-required-next-steps)
and [isolated](../../../../klaude-plugin/skills/review-code/review-isolated.md)
closure guidance may contribute to the omission, but these observations do not
isolate its cause. No wording patch is justified by this assessment alone.

## Proposed examples, written before any successor measurement

These examples specify report meaning, not mandatory phrases, headings or length.
They are proposals for new cases, not regrades of historical reports.

| Case | Acceptable meaning | Unacceptable meaning |
| --- | --- | --- |
| Dormant label-only change; no advisory surfaced | Approve the label change after tracing the checked-in path; counts/calculations are unchanged and historical settings were not assessed. | Block the PR because every optional path must first be fixed, or claim all configurations are safe from three green tests. |
| Dormant change; inherited defect surfaced | Approve this PR; explain the empty detailed-input failure is unchanged and disabled at the checked-in entry point; suggest a separate issue to define empty detailed behavior and add its regression test. No changes required in this PR. | Attribute the crash to the label rename, assert a production outage, or require an unrelated redesign before approval. |
| Same advisory, but no follow-up | Correct attribution and scoped approval remain supported; the follow-up criterion still fails. | Treat an absent next action as proof of an unsafe PR verdict, or silently pass the existing follow-up obligation. |
| Change newly exposes the inherited calculation bug | Request changes: the new configuration makes a supported empty report fail before formatting; the arithmetic is old, the entry-point regression is new. Preserve the documented empty-report result and cover that boundary. | Approve because `stats.py` is unchanged, or recommend reverting the required feature permanently instead of satisfying its contract. |
| Required diff genuinely unavailable | State the unverified comparison and the specific missing evidence; keep the required comparison unresolved. | Claim a completed comparison or broad approval from source-only access to one side. |

The first row intentionally proposes relaxing mandatory dormant discovery in
the successor control. It requires an explicit prospective decision; it cannot
pass original 13.3/13.4. In the second row, the follow-up need not be executed or
turned into an issue by a review-only actor. If work is actually deferred by an
implementation workflow, the existing durable-tracking rules still apply.

## Proposed successor pair and assertion mapping

Use separate case identities, provisionally **R6M** (material exposure) and **R6D**
(dormant control); allocate unused numeric IDs only when authoring. Both should
use the same small reporting implementation and inherited empty-input division.
Give detailed calculations a visible consumer in both base snapshots, such as
optional mean output, so activation serves a real requirement. This is new
fixture design, not a modification of historical R6.

- **R6M:** enable existing detailed output through a checked-in default change.
  The ordinary contract requires populated mean output and continued successful
  zero-count output for empty batches. Before: the entry point returns the plain
  zero-count report. After: it reaches the unchanged division and raises before
  formatting. The existing tests cover populated detailed behavior but miss empty
  input under the new default. Offline checks must establish that the new setting
  reaches the bug; do not grade an imagined deployment configuration.
- **R6D:** change only the count label and matching expectations, leaving detailed
  output disabled. The documented scope preserves counts/calculations and does
  not enable detailed output. The dormant bug remains present. Scoped approval
  may pass without discovering it; any surfaced advisory must be accurate and
  actionable without blocking this increment.

| Original assertion | Proposed treatment in separately identified cases |
| --- | --- |
| 13.1 instruction ordering | Preserve the applicable public-evidence obligation. Missing receipts remain missing; no private-reasoning requirement. |
| 13.2 before/after trace | Require the actual changed path in both cases: newly enabled detailed reporting for R6M, unchanged disabled setting and label-only behavior for R6D. |
| 13.3 discovery and attribution | R6M must find the new entry-point regression and identify the inherited arithmetic. In R6D, discovery is optional; attribution is required if an advisory is surfaced. This is a proposed change in coverage, not an equivalent assertion. |
| 13.4 reachability | R6M must establish newly reachable failure under the checked-in candidate. R6D must bound its approval to inspected behavior and avoid unsupported global claims; if reporting the defect, distinguish its local trigger from unknown deployment settings. |
| 13.5 verdict and follow-up | Split verdict from conditional follow-up so one grade cannot obscure why it failed. R6M blocks its demonstrated hard-contract violation; R6D approves the compatible increment. Preserve a bounded next action for surfaced inherited advisories. |
| 13.6 isolated dispatch | Preserve for any future isolated run. A standard-only diagnostic supplies no isolated/PAL coverage and does not extend the receipt/use fallback. |

Keep discovery, attribution and follow-up separately visible. Define whether each
criterion reads the final report or the full workflow before running: final
verdicts, limits and surfaced-advisory follow-up use the final report; workflow
discovery/ordering may use linked actor events. A child finding alone cannot prove
that the user received an advisory or follow-up. A report-phase replay could
later isolate follow-up when discovery is absent, but it would be a separate
component test, not evidence of end-to-end discovery.

## Bounded next task and completion boundary

**Proposed next task: author and independently review the R6M/R6D fixtures and
rubric, without changing operative instructions or launching actors.** Owner:
the next implementing agent. It is proposed, not automatically selected by
completing this assessment.

1. Author complete before/after snapshots and natural prompts with explicit
   product scope; keep assertions, expected outcomes and examples grader-only.
2. Verify ordinary and boundary behavior offline, including base success versus
   candidate failure for R6M and unchanged reachability for R6D. Do not put defect
   hints or expected verdicts in actor prompts.
3. Write separate discovery/attribution/reachability/verdict/follow-up criteria,
   their evidence sources and positive/negative grading examples. Preserve the
   historical acceptance contract and mark the optional-discovery proposal.
4. Review fixture validity and the proposed scope decision independently; record
   the prospective decision before freezing or measuring. Regenerate Codex eval
   copies and run relevant structure/staging checks after canonical authoring.

Only after that deliverable should a bounded unchanged-instruction diagnostic be
declared. Codex standard is relevant to the discovery miss; Claude standard is
relevant to follow-up. No runtime, model, batch size or acceptance substitution is
selected here. No full-matrix rerun follows automatically.

Other work remains assigned in the [handoff](follow-up.md#remaining-issues-for-the-next-session):
unfinished implementation verification (higher-impact behavioral concern), other
report-detail expectations, capture gaps and ordering. Their next actions remain
there because this task assesses R6 only. Task 12 still owns original R6/R7
acceptance, legacy controls and user-deferred PAL; Task 13 owns final verification
and release evidence housekeeping. Any replacement of original acceptance needs
an explicit contract decision and the required matching comparisons.

## Verification of this assessment

On 2026-10-17, Python 3.10.12 ran the existing unittest suite in each original
snapshot: **3/3 pass before and 3/3 pass after**. Read-only probes reproduced all
four scenario rows above. This is local fixture verification, not an actor run.
All **1,738 manifest-listed file hashes across 16 historical R6 packages** verify;
the current candidate snapshots and oracle match every corresponding captured
initial snapshot/oracle. Historical grades were read, not recomputed.

Local Markdown file/heading links and `git diff --check` pass.
[Independent completion review](reviews/r6-assessment-review.md) approves with no
findings after inspecting original fixtures, historical grades/reports and the
relevant isolated child event. It did not independently rerun the local checks.
Only planning documents change; no canonical/generated instruction, fixture or
historical evidence bytes are edited. Task 12.15 is complete; successor authoring
and broader acceptance remain separate.
