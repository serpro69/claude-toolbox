# Assessment of the two design reviews

> Date: 2026-09-29
> Scope: design corrections only; feature implementation remains pending
> Sources: [review 1](review-design-1.md), [review 2](review-design-2.md)
> Current artifacts: [design](../../design.md), [implementation plan](../../implementation.md), [tasks](../../tasks.md)

Nine reported findings reduce to eight distinct issues: six corroborated and two
partially corroborated. The latter contain valid specification gaps but recommendations
that do not follow from the evidence. No whole finding was rejected. Report 2 has no
IDs; R2-F1 through R2-F8 below number its findings in presentation order. Original
severity is retained for traceability rather than promoted by duplicate reporting.

| ID | Source / original severity | Disposition | Correction |
| --- | --- | --- | --- |
| A1 | R1-F1 P2; R2-F1 P1 | Corroborated; fixed | Qualify automatic implementation coverage as plan-mode completion. |
| A2 | R2-F2 P1 | Corroborated; fixed | Define ordered audience-access rules and counterexample fixtures. |
| A3 | R2-F3 P2 | Partially corroborated; limits fixed, optional variant deferred | Identify self-check versus downstream review per entry point. |
| A4 | R2-F4 P2 | Corroborated; fixed | Budget mandatory shared instruction loading and measure it. |
| A5 | R2-F5 P2 | Corroborated; fixed | Name evidence locations and split eval execution from final verification. |
| A6 | R2-F6 P2 | Partially corroborated; fixed with different mechanism | Define isolated readers, grading and baseline-dependent acceptance. |
| A7 | R2-F7 P3 | Corroborated; fixed | Name maintained count/catalog files. |
| A8 | R2-F8 P3 | Corroborated; fixed | Define one instruction-target response and its workflow suggestion. |

## A1 — Implementation-mode coverage

The [implement entry point](../../../../../../klaude-plugin/skills/implement/SKILL.md)
labels Step 5 plan-mode only. [Plan-mode completion](../../../../../../klaude-plugin/skills/implement/plan-mode.md#completion)
calls `/kk:document`; [standalone mode](../../../../../../klaude-plugin/skills/implement/standalone-mode.md)
has no corresponding completion step. Both reports are correct. We retained the
agreed integration scope and corrected the design, plan, task and eval wording;
adding a standalone completion hook would be new behavior. Explicit documentation
invocation is still available. No automatic standalone coverage is advertised.

## A2 — Visibility decisions

The initial design required authorized facts and accessible references without
defining evidence of either. That ambiguity is real. The proposed shortcut that
tracked files or reachable URLs establish shareability is insufficient: explicit
restrictions can apply to tracked content, and an editor's credentials do not
establish audience access. Also, public repository task IDs are not inherently private.

[Ordered rules](../../design.md#truth-preservation-and-visibility) now prioritize explicit
restrictions, then target-repository audience and revision, then evidenced external
access. Unknown access stays unknown. Fixtures declare these facts and cover both
restricted material and legitimate shared references. Permission to remove a private
citation is not permission to disclose its contents.

## A3 — Fidelity self-check and review coverage

The initial workflow did use the editing session for the runtime comparison. The
authorship-bias risk is valid. However, `/kk:implement`'s mandatory isolated **code
review** does not establish that every editorial check must spawn a reviewer. The
initial design did not promise independent runtime verification.

The [integration table](../../design.md#integration-boundaries) now names the actual
downstream review per entry point: design retains a recommendation, and standalone
editing/documentation make no automatic independent-review claim. An optional
runtime verifier is recorded under [deferred work](../../implementation.md#deferred-work)
with the feature maintainer as owner, cost rationale and a concrete evaluation step.
This is an acknowledged limit of v1, not an implemented guarantee.

## A4 — Always-loaded instruction cost

The planned consumers load the whole shared procedure before subject matter, including
unchanged resumes. Its size was unbounded. This is a real design omission, although
no actual runtime cost can be measured before the procedure exists. The design now
targets 1,000 whitespace-delimited words with a 1,200-word ceiling, counting mandatory
linked instructions too. Task 1 records the count. Late loading and moving prose
behind mandatory links cannot bypass the budget or instruction-ordering rule.

## A5 — Evidence location and task size

The original plan named no evidence path, and its S-sized final task bundled baseline
and revised-reader execution across multiple scenario classes with release checks.
Both claims are supported by the reviewed text. Evidence now goes in feature-local
`verification.md` and `verification/<run-id>/<scenario>/`. Task 4 (M) owns behavioral
eval execution and repairs; Task 5 (S) owns final verification and documentation.
Their dependencies and graph are updated. These future run artifacts are not created
as empty evidence, and no eval execution is claimed by this design repair.

## A6 — Fresh readers and a passing baseline

The original protocol omitted who reads and how a passing baseline affects the
verdict. That gap is real. Two suggested remedies are refuted:

- The existing [eval-grader](../../../../../../klaude-plugin/agents/eval-grader.md) is not
  a reader. It expressly prohibits fixture access and grades supplied reviewer text.
- Correct baseline answers alone do not establish that the document is already clear.
  A capable reader can recover answers despite a concrete orientation defect.

The [protocol](../../implementation.md#fresh-reader-protocol) uses separate general-purpose
read-only sessions for original and revised artifacts and a separate evidence-aware
grader. It specifies manifests, source/tool traces, oracle separation and verdicts.
No-op requires a baseline satisfying all applicable requirements, not just correct
answers and good orientation. A baseline with correct answers can still need factual,
visibility or structural repairs; an edit must fix a declared defect while preserving
answer accuracy. Missing evidence or isolation leakage cannot yield a valid run.

## A7 — Maintained inventories

The cited counts exist in [README](../../../../../../README.md) and the
[skills guide](../../../../../user-guide/skills.md). Searches also found maintained counts
in the plugin README, getting-started pages and the architecture guide. The
[implementation plan](../../implementation.md#1-standalone-editing-of-local-documentation)
now enumerates these files and limits their changes to mechanical count/catalog
updates. The utility is not inserted as a mandatory pipeline stage. Counts are not
updated during this repair because the new skill does not exist yet.

## A8 — Instruction-target handling

The original design promised a redirect without naming a destination, while its eval
table required only surfacing the unsupported target. This was ambiguous. All three
artifacts now require the same response: explain that the instruction file is outside
editorial scope, suggest `/kk:implement`, and perform neither edits nor automatic
handoff. That workflow detects its own profiles; `skill-md` applies only when the
target matches its signals, not to every agent-instruction file by assumption.

## Verification of this reconciliation

Source corroboration used current repository instructions, consumers, the eval-grader
definition and maintained inventories. Initial local link/anchor, whitespace and task
metadata checks passed across all six documents; all implementation tasks remain pending.

An independent `code-reviewer` inspected the correction diff and all six files. It
corroborated the source dispositions and found one new P2 issue: the proposed
baseline rule allowed only orientation improvements when all five answers passed,
thereby excluding necessary factual or visibility repairs. This was valid. The four
affected artifacts now require no-op only when **all** applicable requirements pass,
and the eval plan adds a clear-prose factual/private-reference regression case.
Focused independent re-review directly read the four corrected artifacts and returned
**APPROVE**, with no remaining findings. Final local links/anchors, task metadata and
dependency checks passed; `git diff --check` passed. The original reports were changed
only by adding links to this assessment. All five implementation tasks remain pending.

PAL/Gemini 3.1 Pro returned no findings but reported `files_embedded: 0`; its response
is not treated as evidence of independent file-level verification. No systemic P0/P1
finding was identified for indexing. No plugin source, generated output or runtime
behavior was changed, and no feature evals were executed.
