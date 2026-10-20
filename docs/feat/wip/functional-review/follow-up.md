# Functional review: next-session handoff

> Updated: 2026-10-20
> Status: Task 12.24 complete and independently approved; material-verification assessment and finalization remain
> Owner: implementing agent, Task 12.25
> Next-session starting point: [current acceptance reassessment](acceptance-reassessment.md)
> Evidence: [completed matrix](verification/task12/opus55/README.md), [Claude](verification/task12/opus55/claude-results.md), [Codex](verification/task12/opus55/codex-results.md)

## Start here

**Current decision — 2026-10-20:** the user authorized replacing the
all-assertions-pass-twice gate with proportionate acceptance. Read
[the reassessment](acceptance-reassessment.md) and
[evaluation policy](evaluation.md#comparison-identity-and-acceptance) first.
Original R6/R7, optional follow-up/report details, perfect transport receipts,
all-eight advisory coverage, deferred PAL and blanket legacy actor runs no longer
block local functional-review acceptance. Their old grades remain unchanged.
Earlier paragraphs retaining those gates are historical and superseded.

Next: Task 12.25 assesses the retained implementation-mode verification/diff
acquisition gap using existing evidence and current instructions. No new actor
batch, reviewer simplification or closure-wording restoration is selected.
Task 13 then owns final docs/checks and human-owned archive work. The ADR and
shared design/test/review guidance make this lesson durable for future work.

[Completion review](reviews/verification-policy-review.md) approves with no
findings. Generator/graph checks, 259 structure assertions and repeat-generation
freshness pass. This verifies policy integration; no new actor batch was run.

## Historical checkpoints

**Closure rollback complete — 2026-10-18:** the user explicitly requested the
rollback. The canonical standard/isolated closing instructions and generated
Codex copies restore the exact pre-candidate wording. Verification passes and
independent review approves. The rejected candidate and comparison evidence are retained;
completion-time handoff copies preserve the original comparison-seal hashes.
The rollback does not resolve the broader Task 12 acceptance obligations.

**Measured comparison complete — 2026-10-18:** all 64 sessions completed
successfully; all 464 original assertions and eight separate grading clarifications
are retained. The strict audit passes and owned Codex setup is cleaned up.
The disposition is **REJECT**: two candidate decision failures and an
absent final advisory in one of eight dormant runs prevent KEEP. Independent
completion review approves the record. The next recommendation is reverting only the closure candidate
when selected; no automatic rollback or further wording experiment follows.
Original Task 12 acceptance and Task 13 remain open.

## Earlier checkpoints

The entries below retain historical preparation and superseded blockers. They
do not authorize relaunching the now-completed batch.

**Comparison prepared — 2026-10-18:** the user selected the frozen comparison.
All 64 inputs are prepared and individually validated, with strict preflight and
runtime identities still passing. Automatic approval review rejected the batch
launch before process creation and requires explicit approval of the 64-session
instruction/fixture transfer to authenticated Anthropic Claude and OpenAI Codex.
No measured actor ran. [Task 12.22's execution record](verification/task12/advisory-closure-execution/bootstrap-loading/comparison.md)
specifies the approval scope and resume command. After approval, reverify and run
the existing prepared batch; do not rerun preparation or overwrite inputs.
Independent grading, bounded disposition and completion review remain pending.

**Runtime preflight PASS — 2026-10-18:** explicit user approval resolved the launch
blocker. Both corrected Claude bindings completed; all required reads, including
eight candidate detections and five child sources, are verified. The original
auditor rejected two permitted instruction-filename listings; a separately
reviewed/frozen verifier now validates their narrow scope without counting them
as Reads. Twelve verifier tests pass. Original captures/failures and operative
skill bytes stay unchanged. Independent evidence review approves, and the strict
guard passes. [Task 12.21.4 is complete](verification/task12/advisory-closure-execution/bootstrap-loading/preflight-result.md).

The next item is the frozen 64-session advisory-closure comparison when selected.
Use `verification/task12/advisory-closure-execution/bootstrap-loading/listing_guard.py`
for preparation/measurement and reverify the declared inputs. No measured session
or adoption decision occurred in this preflight task. Original feature acceptance,
PAL deferral, legacy controls, other investigations and Task 13 remain open.
The entries below retain the earlier sequence and superseded blockers.

**Corrected bindings completed — 2026-10-17:** explicit user approval resolved
the host/API authorization blocker. Both Claude probes completed once with high
in their actual launch/command records, expected models/roots and unchanged
subjects. The [result](verification/task12/advisory-closure-execution/high-effort-host/preflight-result.md)
keeps preflight BLOCKED: baseline passes, but candidate explicitly skips all eight
profile-detection files required by bootstrap/fallback loading. Independent
review confirms the failure. Its P2 guard finding is fixed in a separately
reviewed/frozen verification entry with five passing regressions; the strict guard
rejects the actual incomplete candidate. Next investigation: reconcile the probe's stopping
point with its required instruction inventory and review a bounded successor
before another affected capture. No operative skill change, additional actor or
measured comparison is selected; original acceptance and Task 13 remain open.

**Effort correction prepared — 2026-10-17:** the user selected the next step.
The [successor](verification/task12/advisory-closure-execution/high-effort-host/README.md)
enforces and records Claude high effort without changing actor instructions.
Nine successor tests and 26 predecessor regressions pass; independent review
approves the launcher and calibration/Codex/state reuse under original identities.
The first sandboxed baseline attempt failed normal startup and is preserved as
incomplete. The separately reviewed/frozen host successor was rejected before
launch by automatic approval review over private-payload authorization to Claude/API.
Next: obtain explicit approval for two fresh bindings sending the filtered plugin
and synthetic fixture to authenticated Claude, with normal host session access,
isolated Capy and PAL excluded; then capture, audit and independently review them.
No host probe or measured session ran; 12.21.4 remains open. Earlier evidence and
all broader acceptance gates retain their status.

**Preflight executed, readiness blocked — 2026-10-17:** the user selected
[Task 12.21](tasks.md#task-1221-run-and-independently-review-runtime-preflight).
Four binding probes and two Capy state probes completed, with full instruction
receipts, expected model identities, unchanged subjects and owned cleanup. The
[result](verification/task12/advisory-closure-execution/preflight-result.md) and
independent review retain one blocker: Claude child effort is not established at
the declared high value, and the candidate definition specifies xhigh. Prepare a
reviewed successor launcher that enforces/records high, then fresh affected Claude
bindings. No measured run, runtime/requirement change or replacement attempt was
made. Earlier calibration and all historical grades remain unchanged.

**Completed adapter and calibration — 2026-10-17:** the user selected
[Task 12.20](tasks.md#task-1220-prepare-the-execution-adapter-and-run-fresh-calibration).
The [execution record](verification/task12/advisory-closure-execution/README.md)
retains the reviewed/frozen adapter and 25 fresh grader sessions. All 69 assertion
judgments and 11 conditional-trigger values match; expected FAIL/PARTIAL controls
remain visible. Completion review approves with no findings. No binding/state
probe or measured actor ran. Next work is four provider/source binding probes,
two independent state probes and a reviewed preflight attestation. PAL, original
acceptance, other assigned investigations and Task 13 remain open.

**Completed freeze and declaration — 2026-10-17:** the user selected
[Task 12.19](tasks.md#task-1219-freeze-the-closure-candidate-and-review-its-comparison-contract).
The [preparation record](verification/task12/advisory-closure/README.md) preserves
the exact source/filtered bundles, 64-session matrix, grading inputs and reviewed
KEEP / REJECT / INCONCLUSIVE contract. Both independent reviews approve after one
22.4 component-mapping clarification; archive, source-delta and checksum checks pass.
No actor execution was selected or performed. Next execution-preparation work is
the successor adapter, execution freeze, fresh calibration/binding/state checks
and preflight attestation. Original acceptance, PAL and Task 13 remain open.

**Completed candidate preparation — 2026-10-17:** the user selected the bounded
advisory-closure investigation. [Task 12.18](tasks.md#task-1218-assess-and-prepare-a-bounded-advisory-closure-correction)
prepared a small replacement in the standard and isolated closing rules, with
generated parity, local checks and [independent source approval](reviews/advisory-closure-review.md).
Eleven of twelve shell suites pass; the known hook-fixture mismatch remains assigned. The
[assessment](advisory-closure.md) explains the evidence, preserved controls and
prospective comparison. Behavioral improvement and adoption remain unmeasured;
no actor batch was selected and historical acceptance is unchanged. Next action:
review and freeze a concrete comparison declaration if measurement is selected.

**Completed measurement — 2026-10-17:** the user authorized the proposed eight
R6M/R6D sessions across Claude/Codex standard review, twice each, on unchanged
instructions. [Task 12.17](tasks.md#task-1217-measure-the-bounded-r6-diagnostic)
completed calibration, freezing, binding/state probes and all eight captures with
independent grading: **58 PASS / 10 FAIL / 0 PARTIAL**. Every scoped verdict is
correct. All four dormant reports surface the old defect but omit a separate next
action; Codex also omits required trace/reachability details. The
[diagnostic record](verification/task12/r6-validity/diagnostic/README.md) preserves
the evidence and independently approved dispositions: investigate bounded
advisory closure, defer additional trace prose pending value, and add no broader
discovery obligation. Original acceptance, higher-impact implementation verification,
PAL, legacy controls and Task 13 stay open. No patch or further batch is selected.

**Completed continuation — 2026-10-17:** the user accepted the proposed fixture
and rubric authoring step. [Task 12.16](tasks.md#task-1216-author-and-review-r6-material-exposure-and-dormant-control-evaluations)
authored evals 21/R6M and 22/R6D, verified them offline and obtained independent
validity/source approval with no findings. The [authoring record](verification/task12/r6-validity/README.md)
and [prospective rubric](verification/task12/r6-validity/rubric.md) record the
optional-discovery decision for the new dormant control. The possible next step
is a separately declared bounded diagnostic on unchanged instructions after
grading calibration; no run is selected automatically. A pre-existing hook-test
fixture failure is separately assigned in the authoring record. Historical
acceptance remains open; no skill edits or historical regrading occurred.

**Current outcome — 2026-10-17:** the user selected the next priority, R6 evaluation
validity. [Task 12.15](tasks.md#task-1215-assess-r6-evaluation-validity-and-review-scope)
completed the [R6 assessment](r6-assessment.md): source-backed consequences,
report examples, a proposed affected-path/dormant pair and assertion mapping.
Independent completion review approves with no findings. It changes no operative
instructions or historical grades and launches no actors.
The assessment proposes fixture/rubric authoring next; that subsequent task is
not automatically selected. Other report-detail and implementation-verification
investigations retain the assignments below.

**Current outcome — 2026-10-14:** [Task 12.14's four-session diagnostic](verification/task12/r7-validity/README.md)
is captured and independently graded: 23 PASS / 1 FAIL / 0 PARTIAL. Both material
cases retain Unknown target readiness, and both benign controls give justified
scoped approval. One report omits the explicit endpoint in its behavior trace;
that failure remains. The disposition is **no further operative instruction change
for the R7 compatibility concern**. Independent completion review approves this
disposition with the failed assertion and broader acceptance gates retained.

The 2026-10-13 handoff below is historical and has now been executed. These
successor cases do not replace original R7 for feature acceptance. No broader
batch or next implementation is selected automatically; Task 12's remaining
dispositions, live PAL deferral, legacy controls and Task 13 retain their owners
and verification conditions.

## Remaining issues for the next session

**Discussion captured 2026-10-14 at the user's request.** Task 12.14 is complete
and committed as `b20d11f0`. The user asked what the remaining failures mean and
whether the same evaluation-validity approach could help. This section preserves
that discussion and the recommended investigations. It does not select another
implementation task, change a requirement, amend grading, or launch measurements.
Owner of the next assessment: the implementing agent when feature work resumes.

Most observations below come from the earlier full matrix, not a fresh test of
the current revision. Task 12.12 improved selected isolated-review acquisition
cases; Task 12.14 investigated R7. Neither result establishes that every similar
issue in other modes is fixed. The [observation ledger](assessment-observations.md)
remains the exhaustive mapping to old grades; its overlapping group totals are
not a count of distinct bugs or the current candidate's failure rate.

### What 12.14 teaches us

The original whitespace fixture did not establish why missing provider evidence
was consequential. Separately identified material-dependency and benign cases,
with explicit contracts and pre-run report examples, elicited appropriate
compatibility conclusions twice each using unchanged skill instructions. Overall
grading remained 23 PASS / 1 FAIL: one report omitted the endpoint from its trace.
The [results](verification/task12/r7-validity/README.md) support no further R7
instruction change for this slice. They do not prove the old test invalid or the
skill reliable, and they do not replace original R7 for feature acceptance.

Apply the same discipline elsewhere: establish the consequence of the behavior
being tested, include a benign control, define acceptable report meanings before
measurement, and first test unchanged instructions. Distinguish a wrong conclusion,
an incomplete report, a procedure violation, an unavailable capability and an
unobservable event. A red assertion alone does not justify more runtime prose.

### A. Verification left unfinished after command denial

**Observed:** in both Claude I2 implementation runs, the code and regression tests
were written but no successful test execution occurred. One trace never invokes
the tests; the other attempts a denied Capy execution tool. That denial is not
evidence that the permitted Python shell command was unavailable. In a typo-only
I3 run, the independent reviewer received no actual diff. Some I4 verification
also remains source-only. See [I2 repetition 1](verification/task12/opus55/grades/claude-candidate-I2-standalone-1.md),
[I2 repetition 2](verification/task12/opus55/grades/claude-candidate-I2-standalone-2.md)
and [I3's missing diff](verification/task12/opus55/grades/claude-candidate-I3-standalone-1.md).

**Why it matters:** code inspection and written tests do not provide executed
verification. A reviewer without the diff cannot establish change attribution.
The isolated-command correction in Task 12.12 does not establish a fix for these
implementation-mode paths. See the existing [acquisition disposition](#acquisition).

**Recommended investigation:** inspect actual allowed tools and attempted commands
before attributing the failure to the skill or changing permissions. A successor
diagnostic should distinguish an available permitted verification route from
genuinely unavailable execution. In the first case require actual execution and
diff delivery; in the second require accurate limits and an unresolved verification
obligation. Disclosure alone must not turn unrun required tests into a PASS.
This remains the higher-impact behavioral concern, separate from report wording.

### B. R6 expects discovery of an unchanged, disabled-path bug

**2026-10-17 assessment:** [R6 scope, evidence and successor proposal](r6-assessment.md)
separates mandatory dormant discovery from introduced exposure and conditional
follow-up. Original grades remain binding; optional discovery in a successor
control is explicitly a prospective proposal, not an acceptance amendment.

**Observed:** the requested change only renames a report label from “Items” to
“Records.” Unchanged `summarize([], detailed=True)` divides by zero in both base
and candidate, while the supplied entry point uses `DETAILED_REPORT=False`.
Codex standard misses that old defect in both candidate and baseline runs.
The [eval](../../../../klaude-plugin/skills/review-code/evals/functional-inherited-conditional-defect/eval.json)
requires discovery and attribution despite the narrow review prompt. Other reports
surface it but omit the bounded follow-up required by assertion 13.5; the
[Claude report](verification/task12/opus55/grading/claude-candidate-R6-standard-2/captured/report.md)
approves the label change, explains the inherited bug, and ends “No changes recommended.”

**Question to settle:** does safe review of this increment reasonably require
finding that dormant defect? Separately, does the closing advice mean no changes
to this PR, or does it misleadingly dismiss an acknowledged issue? Do not conflate
missed discovery, correct attribution and follow-up usefulness.

**Recommended application of 12.14:** compare a defect reached or worsened by the
changed path with an unchanged dormant-bug control. State review scope explicitly
and define useful scoped approval/advisory examples before measuring. This is the
strongest candidate for evaluation-validity reassessment. A new requirement to
audit every optional path would have broad cost and is not justified by this
fixture alone. Preserve the original 13.3–13.5 grades and the existing
[detection](#inherited-defect-detection)/[follow-up](#inherited-defect-follow-up)
dispositions until a prospective decision is made.

### C. Correct outcomes with missing report details

**Observed:** [R2](verification/task12/opus55/grades/codex-candidate-R2-standard-2.md)
finds both retry defects, gives justified REQUEST_CHANGES and useful fixes, but
does not explain why the existing green tests missed them. Some I4 reports
correctly identify mixed-format incompatibility, preserve the hard requirement
and reopen the task, but omit the required final qualification that production
state was not verified. In one [Codex I4 run](verification/task12/opus55/grades/codex-candidate-I4-plan-2.md)
that qualification exists in task context but not the final response. These
observations do not establish false task completion.

**Recommended application of 12.14:** write examples of genuinely misleading
completion/compatibility claims and concise reports that communicate enough to
make the correct decision. Assess the whole report, its actual evidence and any
explicitly linked verification record. Decide which omitted information changes
the user's understanding; avoid inventing a required phrase or extra report
section to obtain a clean score. Record any proposed change to the existing
final-response requirement explicitly before applying it.

The [R1 scenario-order failure](verification/task12/opus55/grades/claude-candidate-R1-standard-1.md)
needs a distinct semantic check: the report finds cleanup corruption but reverses
part of the required event sequence. That is not merely missing wording; assess
whether its described execution actually supports the claimed consequence.

### D. Tests demand evidence the capture does not expose

**Observed:** some Codex runs lack captured successful skill-entry delivery or
exact submitted reviewer prompts, despite later instruction reads or reviewer
use of context. Both Claude typo-edit runs have an unobservable pre-edit
non-runtime assessment; the typo fix and proportionate behavior themselves pass.
Private reasoning was deliberately excluded. See [entry receipts](#entry-point-receipts),
[handoff receipts](#handoff-receipts) and [pre-edit assessment receipts](#pre-edit-assessment-receipts).

**Recommended application of 12.14:** define public evidence of the useful
behavior, then determine whether capture can supply it. Inspect existing raw
events first. Reviewer receipt/use may establish context consumption but cannot
prove exact submitted wording. Observable edits and verification can demonstrate
a proportionate typo correction without compulsory narration of private reasoning.
Any narrower evidence contract requires an explicit prospective amendment and
calibration; the approved receipt/use fallback currently covers only R3 7.5/7.6
and I2 9.5. Missing evidence stays missing under the existing contract.

### E. One context/source read overlapped by 49 milliseconds

**Observed:** [Codex I4 repetition 1](verification/task12/opus55/grades/codex-candidate-I4-plan-1.md)
starts a full source read 49 ms before task/design/implementation loading completes.
The later outcome correctly refreshes stale context, finds the incompatibility
and keeps acceptance open. This is a demonstrated ordering violation; no harmful
downstream decision was established in that run.

**Recommended treatment:** retain the failure and keep its impact separate from
missing context or a wrong decision. Consider a focused sequencing check or small
scheduling correction if warranted. Task 12.10's proposed preparation guard does
not establish this later context barrier and remains conditional, not the next
default task. A broader mechanism needs evidence of a material problem it solves.

### F. The external reviewer was intentionally unavailable

PAL absence is user-deferred verification, not evidence that another actor
instruction is needed. Historical composite assertions may also contain local
failures; assess those components separately. Resume actual invocation, source
receipt/use and integration checks only when the existing deferral is lifted.
Keep the [PAL disposition](#pal-deferral), synthetic R8 results and live transport
coverage distinct.

### Recommended starting point and completion boundary

The recommendation discussed was to reassess **R6 and report-detail expectations**,
while separately investigating **unfinished implementation verification**. These
are two different questions: whether the evaluation asks for something useful,
and whether the agent completes verification that is actually available. It is
not a selected patch or an approved batch size.

A useful first deliverable for the next session is a compact assessment of those
cases with the exact failed assertion/report, practical consequence, acceptable
and unacceptable examples, any proposed successor/control, and a fix/investigate/
defer/no-change disposition. Consult the current design, implementation, evaluation
contract and task status before acting. Only then select a bounded next task and
declare any measurement. Preserve historical fixtures, grades and freezes; review
new criteria before testing unchanged instructions; keep actor inputs isolated
from grading material. No automatic full-matrix rerun follows from this handoff.

Task 12 still needs legacy routing/pre-write controls, resolution of its required
acceptance conditions and an explicit decision about original R7 versus successor
coverage. Task 13 retains final documentation/reviews and human-executed release
evidence housekeeping. This note records future investigation; none of those
remaining gates has been run or closed by saving it.

Optional wording-only refinement: `/kk:clarify-docs
docs/feat/wip/functional-review/follow-up.md
docs/feat/wip/functional-review/tasks.md`.

## Historical handoff — 2026-10-13

**Recorded starting point (2026-10-13): [Task 12.14](tasks.md#task-1214-redesign-the-r7-evaluation-before-further-skill-changes).**
The user questioned whether the simplified R7 fixture and its interpretation of
conditional approval justify treating the observed reports as a material skill
defect. Document and develop a revised test and grading criteria first. The
[handoff below](#r7-evaluation-redesign--next-session) supersedes the earlier
proposal to change standard-review closing guidance. Leave operative skill
instructions unchanged while investigating evaluation validity.

Task 12.12's [outcome](#task-1212-outcome--2026-10-11) retains the isolated command's
explicit instruction paths after its bounded comparison. The original
[assessment](#assessment--2026-10-11) and [observation ledger](assessment-observations.md)
remain tied to the earlier full matrix; its grades are not rewritten by this
follow-up. [Task 12.13](tasks.md#task-1213-keep-compatibility-and-release-conclusions-within-their-evidence)
tested the user-approved bounded wording replacement in all 48 declared sessions.
Both Claude standard R7 reports still overclaim provider/deployment compatibility,
so the candidate is rejected and the operative changes are reverted. All 336
assertion rows, integrity checks and cleanup are recorded; [independent completion
review](verification/task12/r7-conclusions/completion-review.md) approves the rejection
record with no findings. All 52 actor workspaces were removed after archive checks.
The user explicitly authorized the external transfer and comparison after the
initial launch rejection; no authorization block remains for that completed
batch. R7 is unresolved; its evaluation redesign is now the selected next task.
No successor skill patch or new actor batch has been executed.
Before resuming, read the current Task 12 status, [design](design.md),
[implementation](implementation.md), [evaluation contract](evaluation.md) and
the relevant sealed grades, then check the worktree.

The user's latest constraint is explicit: fixing minor issues by overloading
instructions can make the skills worse overall. Assess severity before adding
more obligations. A small, contained correction remains worthwhile when its
benefit is clear and it does not materially increase instruction burden.
Keep this assessment in repository planning documents; it is not a new runtime
checklist for every skill invocation.

## R7 evaluation redesign — next session

**Historical plan, now completed by Task 12.14.** Use the
[remaining-issues handoff](#remaining-issues-for-the-next-session) for new work.

**Direction recorded 2026-10-13 at the user's request.** Start from commit
`d5fb1694`, which records Task 12.13's rejected experiment. This handoff documents
future work only; it does not implement revised fixtures or launch sessions.

**Why reassess the test:** R7 trims a request's display-name string and asks whether
the change is ready to deploy, without a provider contract or deployed revision.
Its fixture never establishes that whitespace and empty strings have different
operational meanings. That was a hypothetical example, not a demonstrated defect.
The two failed Claude standard reports acknowledge missing evidence and return
COMMENT, then offer stronger conditional advice. Their historical 14.3/14.4 FAILs
remain valid under the pinned rubric, but the rubric's ability to distinguish
useful scoped judgment from material overconfidence is now in question. Neither
the fixture's invalidity nor the cause of the agent behavior is established.

The next deliverable is a revised R7 fixture pair and explicit grading examples:

1. **Material missing evidence:** use a small, realistic compatibility dependency,
   such as a documented request capability requiring API v2 while the deployed
   provider version is unknown. Explain the consequence of the missing fact.
   Local mock success cannot settle that question. Keep this distinct from R3,
   whose supported provider baseline is known and demonstrates incompatibility.
2. **Benign control:** document the supported inputs and unchanged external
   contract of a small change. Allow justified, scoped code approval without
   demanding production access or inventing a deployment blocker. Make the review
   scope clear in both cases so prompt ambiguity does not decide the outcome.
3. **Meaning-based grading:** write acceptable and unacceptable example reports
   before measuring agents. Distinguish code support, source-level compatibility,
   and a particular deployment conclusion. Judge whether conditions and limits
   address the material requirements; conditional phrasing alone is not proof of
   overclaiming. Reconcile any proposed verdict-rule change explicitly with
   design.md and the existing rubric before adopting it.
4. **Small diagnostic after fixture/rubric review:** prospectively declare two
   fresh Claude standard sessions per case, four sessions total, using the same
   unchanged current skill revision. Pin fixture, rubric, grader, runtime and
   model identities, and retain independent grades and all attempts. This tests
   the revised evaluation's usefulness; it is not a baseline/candidate improvement
   comparison or full-feature acceptance. Broaden only if a concrete failure
   warrants a separately documented next step.

Preserve old fixtures, assertions, captures, corrections, grades and freezes.
Give successor cases/rubric separate identities and an old-to-new assertion
mapping; do not retroactively turn old FAILs into PASS or pool unlike results.
Do not add skill instructions, resume the reverted wording, launch another
48-session matrix, expand PAL, or design a general deployment framework for this
task. The four-run diagnostic follows the written fixture/rubric deliverable;
it is not work to start merely by resuming the feature. Task 12 acceptance and
Task 13 remain open. Owner: next implementing agent.

Resume with `/kk:implement functional-review Task 12.14`, beginning with the
fixture/rubric work. Optional `/kk:clarify-docs` can refine `follow-up.md`,
`design.md`, `implementation.md`, `evaluation.md` and `tasks.md`; then use
`/kk:review-design functional-review` to check the prospective evaluation plan
before measurement. These are next-session recommendations, not reviews already
performed or an instruction to start actor runs from this handoff.

## Established result and open gates

The complete comparison ran **192 fresh sessions**: both providers, all 24
applicable case/mode combinations, baseline and candidate, twice each. Baseline
is `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; candidate is
`581dd0e11455398cb73e3d6ae5542854c016fe7f`. Claude Code 2.1.296 used Opus 5.5/high;
Codex 0.162.1 used gpt-6-astra/xhigh with gpt-6.1-sol/xhigh as named reviewer.
The [frozen contract](verification/task12/opus55/run-contract.md) is authoritative
for the complete configuration.

Both candidates improve overall assertion counts, but acceptance remains unmet.
R5 standard and both synthetic R8 variants pass twice on both providers. Two
repetitions are descriptive evidence, not a reliability estimate. Historical
runtime/model configurations differ; do not attribute every improvement to the
Opus change or pool those runs.

Task 12.1 capture is complete. Task 12.2 is partial: R8 is complete, live PAL
remains explicitly user-deferred, and legacy routing/pre-write controls remain
unrun. Task 12.3 grading is complete but its acceptance condition is not.
Task 13 remains pending. Preserve sealed captures, grades, corrections and old
failed checkpoints. Deferring a fix does not change a FAIL/PARTIAL to PASS or
complete a required gate. Any requirement or evidence-contract amendment must
be explicit, versioned and prospective.

## Decide whether a change is worth making

For each distinct issue, record a short decision containing:

- **Evidence and impact:** case/assertion/run links, observed behavior versus
  unavailable evidence, practical consequence, affected provider/mode, recurrence
  and confidence. A severe bug inside a fixture does not automatically make an
  instruction change high priority. Use existing severity conventions, with a
  reason tied to skill users rather than the number of red assertions.
- **Smallest useful correction and cost:** likely files/consumers; whether
  existing guidance can be removed, replaced or consolidated; added always-loaded
  words and transitive content; new mandatory steps, branches, tool calls,
  coordination or state; expected latency and regression exposure. A short diff
  can still impose a large new obligation. Retain the existing 800/1,200-word
  budgets; staying below them alone does not demonstrate proportionality.
- **Disposition and verification:** fix, investigate, defer or no change, with
  rationale and acceptance consequence. Deferred items need an owner and revisit
  trigger. A selected fix needs an affected comparison set, adjacent regression
  controls and a condition for rejecting/reverting it.

Material behavioral impact can justify a broader correction when expected value
outweighs its cost. A minor issue can justify a local wording replacement or
tooling correction with low regression risk and no material added load. A minor
issue that needs another mandatory phase, duplicated protocol or broad mechanism
should normally be deferred. Missing evidence first calls for capture diagnosis,
not extra actor instructions to manufacture an observable read.

## Provisional investigation inventory

This is the original investigation inventory, preserved for provenance; the
dated assessment below supplies its dispositions. These were **not an approved
priority order or fix list**.
Account for every remaining candidate FAIL/PARTIAL from the provider grade
indexes, grouping common causes without losing assertion-to-evidence links.

| Area | Observed distinction | Decision to resolve |
| --- | --- | --- |
| R6 inherited defect | Codex standard misses the inherited empty detailed-input defect in both candidate runs and both baselines. Claude standard finds it but omits bounded follow-up in both candidates, regressing from baseline. Codex isolated also omits follow-up once after surfacing it. | Assess missed detection separately from closure wording. A local closure correction may be cheap; it must preserve R5's clean no-action outcome and R9's justified recovery mechanism. |
| Claude evidence acquisition | Several isolated/implementation traces treat a denied shell request as general Bash unavailability, then omit diffs, history or executed tests. R3 isolated includes an early stop. | Establish whether command selection/tool-policy interpretation is the cause and how broadly it matters. Unattempted permitted Git commands are not evidence that Git was denied. Prefer correct use of resolved paths and available tools; do not silently broaden permissions. |
| Unsupported conclusions and verification | Claude R7 retains unsupported compatibility claims; I2 verification and some I4 test execution remain unestablished. | Distinguish misleading conclusions from missing capture, and inspect overlap with acquisition failures before prescribing another instruction. These may matter more than report completeness. |
| I4 sequencing | Codex candidate repetition 1 starts a source read before task/design/implementation context finishes loading. | Assess a local sequencing correction. This is a later context-before-source dependency, not the original instruction-before-investigation failure; the proposed preparation guard may not cover it. |
| I4 final qualification | Claude candidates and one Codex candidate omit the final production-state qualification. The Codex candidates preserve the hard specification and reopen the failed task. | Judge whether the omission materially misleads the reader, considering linked evidence. Do not equate it with silently waiving a hard requirement. Prefer an existing report location if a correction is justified. |
| Other report omissions | Codex R2 standard finds defects but omits the test-gap explanation once; other individual grades identify coverage/report gaps. | Assess effect on a user's decision. Do not add a mandatory section for every missed phrase; consider a contained replacement or defer. |
| Evidence gaps | Some Codex SKILL.md deliveries and I3/I4 submitted handoff arguments are not captured. Other grades distinguish unobserved pre-edit assessment from demonstrated failures. | Diagnose instrumentation before actor behavior. The receipt/use fallback is limited to R3 7.5/7.6 and I2 9.5; extending it requires an explicit prospective contract decision. |

For a selected issue, follow the relevant grade into its sealed evidence before
claiming a root cause. Likely investigation targets are the canonical
`klaude-plugin/skills/review-code/` files (`review-process.md`,
`review-isolated.md`, `functional-review.md`, `packet-preparation.md`,
`scripts/prepare_instructions.py`), `klaude-plugin/skills/implement/` files
(`plan-mode.md`, `standalone-mode.md`),
`klaude-plugin/skills/_shared/change-context.md`, and
`klaude-plugin/agents/code-reviewer.md`.
Capture questions start with `verification/task12/opus55/matrix.py` and its
declared helpers. These are investigation targets, not instructions to edit all
of them. Load the applicable implementation/profile instructions first.

### Conditional ordering proposal

[Task 12.10 and its proposal](ordering.md) remain available but are not the
default next action. Their original candidate-6 R5 failure did not recur in this
matrix. That observation neither proves ordering solved nor establishes a need
for a guard. Re-select the bounded feasibility probe only if triage demonstrates
a material remaining problem the mechanism actually addresses, with acceptable
cost. Revalidate capabilities against the exact runtimes then selected; old
hook-documentation research is not runtime proof. Preserve the probe's GO/NO-GO
limits and design review before any production integration.

## Produce and verify the next bounded step

The Task 12.11 completion contract was a compact disposition record covering remaining
candidate failures/gaps, plus at most one selected next implementation task with
concrete files, limits and verification. Add the decisions as a dated assessment
section in this file and link it from Task 12.11; record the selected next task
in tasks.md. If no fix has favorable value/cost,
record that outcome and the still-open acceptance obligations. Do not accumulate
speculative fixes just to make the matrix green.

For a later selected change, freeze its source and evaluation configuration;
preserve the immutable baseline and use fresh affected baseline/candidate pairs,
two runs each, under matching declarations. Keep fixtures and grading unchanged
unless a separate contract revision is explicitly adopted. Never encode fixture
names, hidden defects or expected counts into operative instructions.

Judge the net effect using the target cases and nearby negative controls:
R6 closure changes need R5 and R9 checks; shared changes need affected providers
and modes; routing/pre-write changes need their legacy controls. Include I3's
proportionality when adding common obligations. Complete relevant static checks
and generated parity after operative edits. A narrow improvement that worsens
broader behavior or adds unjustified instruction burden should be rejected or
reverted. A full 192-session rerun is not the default for a small correction;
targeted evidence still does not replace the remaining feature acceptance gates.

## Assessment — 2026-10-11

**Decision:** select one contained correction: give the isolated-review command
explicit paths to its existing skill and workflow. The [Task 12.12 plan](tasks.md#task-1212-resolve-isolated-review-instructions-at-entry)
defines its bounds and diagnostic comparisons. Do not add a general permission
protocol, another checklist, a reporting section or an ordering guard in this
slice. This assessment changes planning records only.

The [observation ledger](assessment-observations.md) maps all **79 FAIL and 14
PARTIAL** candidate grades, with matched baseline verdicts and original evidence
links. Groups overlap where an assertion has several unsatisfied components;
in particular, 44 assertions include PAL absence, and some also lack local
evidence. All original grades, source identities and acceptance requirements
remain unchanged. No new actor run or regrading was performed.

Priorities below use the existing P1–P3 impact vocabulary for the **skill user's
consequence**, not the severity of a planted fixture defect. Unknown receipt
evidence and explicit PAL deferral have no inferred behavioral severity.
Confidence describes these traces, not recurrence rates in general use.

**Ownership and open acceptance:** the implementing agent owns every disposition
below, including deferred work. Each subsection gives its revisit trigger and
verification condition. All required non-PASS observations remain open under
Task 12; a selected diagnostic improvement cannot complete feature acceptance.
Live PAL requires the user to lift the existing deferral. Legacy routing/pre-write
controls and Task 13 remain separate, unrun gates.

### Acquisition

**Investigate through the selected entry-path fix; P1, high confidence in the
observed loss of evidence, moderate confidence in the proposed remedy.** This
group contains 28 observations, including composite PAL failures. Claude misses
diff attribution, historical comparison or executed verification, and sometimes
withholds otherwise supportable approval. The two R3-isolated candidates each
make one shell request containing broad instruction discovery; its denial is
followed by a blanket shell-unavailable conclusion. The second stops before
investigation. See their actual [first request](verification/task12/opus55/grading/claude-candidate-R3-isolated-1/events/0003.json),
[second-run request](verification/task12/opus55/grading/claude-candidate-R3-isolated-2/events/0003.json),
[denial](verification/task12/opus55/grading/claude-candidate-R3-isolated-2/events/0004.json)
and [stopped report](verification/task12/opus55/grading/claude-candidate-R3-isolated-2/captured/report.md).
Their [launch policy](verification/task12/opus55/grading/claude-candidate-R3-isolated-2/captured/command.json)
lists Git/Python tools; neither run separately attempts the needed Git operation.
This establishes an unsupported generalization, not proof that every alternative
command would have succeeded.

Successful R6/R9-recovery isolated repetitions start from the resolved helper
path and later obtain diffs; the [R9 helper call](verification/task12/opus55/grading/claude-candidate-R9-recovery-isolated-2/events/0009.json)
and [Git call](verification/task12/opus55/grading/claude-candidate-R9-recovery-isolated-2/events/0043.json)
illustrate the available route. This contrast is a hypothesis, not a controlled
test of the entry text. The command currently names the workflow without its
resolved location. Replacing that reference with plugin-root paths has a smaller
cost than teaching every invocation how to recover from shell denial.

The same symptom in I2/I3/I4 is **deferred, not claimed fixed** by this command
change: their first denied requests concern file/root discovery in implementation
mode. I2 repetition 2 additionally tries a denied Capy execution tool; that is
not a denied `Bash(python3 ...)` test invocation. R5's unsupported lazy-import
suggestion and R6/R9's conditional final verdicts also remain separate report
components even when diff acquisition contributed. Revisit these after Task
12.12, using their sealed calls before considering shared guidance. Verify actual
diff/history receipt and test results in fresh affected pairs; never broaden
permissions or reclassify a denied action as successful. Existing common guidance
already says to retry permitted individual reads, so duplicating that instruction
is not selected.

### PAL deferral

**Defer; no actor fix.** All 44 affected assertions retain FAIL because an
explicitly required reviewer was absent. The [run contract](verification/task12/opus55/run-contract.md)
declared that absence. User-visible single-reviewer limits generally remain
disclosed; absence is not evidence that the functional method failed. No extra
runtime words or workflow steps are justified. Revisit when the user authorizes
live PAL: verify actual invocation, relevant source receipt/use and the real
smoke test, while retaining each assertion's other components. R8 replay passes
do not substitute for those checks.

### Unsupported compatibility claims

**Current disposition — 2026-10-14:** [Task 12.14](verification/task12/r7-validity/README.md)
is complete. The clearer material/benign cases preserve appropriate compatibility
conclusions twice each; one endpoint-trace omission remains failed. Select no
further operative instruction change for this concern. Original R7 acceptance
is not replaced or waived. The dated assessment and rejected experiment below
remain historical evidence; their P1 characterization alone does not justify
another skill change.

**Successor decision — 2026-10-13:** the user approved retaining Unknown and a
concrete next check until missing compatibility evidence is supplied and assessed.
Task 12.13 replaces existing common-method wording for Supported, the Unknown
verdict row and final evidence reconciliation. Known rollout prerequisites and
scoped code approval remain valid. No new checklist, report section or blanket
deployment restriction is selected. Test the hypothesis with unchanged R7/R3/R5
in both modes/providers, two fresh baseline/candidate repetitions each; preserve
all original grades and the live-PAL deferral. The completed experiment below
rejects that wording; this paragraph records the original hypothesis.

**Measured disposition — 2026-10-13: reject.** All 48 sessions completed after
explicit user authorization. Both Claude standard R7 candidates fail 14.3/14.4
despite receiving the instructions; all Codex and Claude isolated R7 candidates
meet the local target rows. R5's candidate non-PAL rows pass. Codex candidate R3
isolated repetition 1 identifies the incompatibility but omits explicit Blocked
classification in its final parent report; this also occurs in the baseline.
Effective candidate totals are 147 PASS / 21 FAIL / 0 PARTIAL, with 16 required
PAL omissions retained as FAIL. [Results and corrected grading provenance](verification/task12/r7-conclusions/results.md)
remain separate from the historical full matrix.

The 28-word increase and generated copy are reverted. Source checks passing did
not establish the desired behavior. [The verification record](verification/task12/r7-conclusions/README.md)
retains the rejected patch, immutable candidate, captures and grades. R7 remains
unresolved; no further wording or actor iteration is selected automatically.

**Earlier assessment — P1; action superseded by Task 12.14.** Five Claude R7
observations (four FAIL, one PARTIAL) mix unavailable provider/deployment evidence
with supported-server or safe-to-deploy language. This can mislead a release
decision; confidence is high for the explicit claims and lower for the ambiguous
isolated report. In [standard repetition 1](verification/task12/opus55/grading/claude-candidate-R7-standard-1/captured/report.md)
and [repetition 2](verification/task12/opus55/grading/claude-candidate-R7-standard-2/captured/report.md),
an earlier Unknown does not qualify the later deployment assurance sufficiently.
These standard runs already obtained the diff and ran tests, so missing shell
access is not a sufficient explanation.

The common method already requires named baselines and bounded conclusions.
Do not add another deployment checklist. Revisit by tracing the unsupported
conclusion into existing verdict/report wording and test whether replacement or
consolidation can remove the conflict. Likely targets are `functional-review.md`,
the existing report templates and `code-reviewer.md`; any shared edit affects
both providers and modes. Verification must cover R7 both modes, R3's demonstrated
incompatibility and R5's justified approval, twice per affected side/provider.
Reject a proposed change that turns unrelated operational unknowns into blockers.

### Inherited-defect detection

**Defer broader detection changes; P2, high confidence in these misses.** Codex
R6-standard misses the empty detailed-input condition in both candidates and both
baselines (four candidate observations). The reviewed label change is still
correct; the missed defect is inherited and unreachable with checked-in settings.
There is no supported current-production incident or introduced regression.
Revisit after acquisition/claim work if a general affected-path improvement can
explain this miss without requiring whole-system or every-flag audits. The common
method and Python guidance already cover boundaries. A new mandatory enumeration
would impose broad cost for this bounded miss. Verify R6 detection and attribution
while retaining R5/R9 clean and justified-complexity outcomes on both providers;
fixture-specific hints are unacceptable.

### Inherited-defect follow-up

**Defer a small closure replacement; P2.** Three observations omit a bounded
next action after surfacing a known inherited defect: both Claude standard runs
regress from passing baselines, and one Codex isolated candidate also omits the
next action. That Codex baseline never surfaced the defect; its conditional
assertion PASS is not evidence of better follow-up. The
[Claude report](verification/task12/opus55/grading/claude-candidate-R6-standard-2/captured/report.md)
both describes the defect and says no changes are recommended. This is lost
actionability, not an incorrect approval of the label change. Confidence in the
omission is high; the clean-closure rule's causal role remains an inference.
Do not combine it with the detection miss: the other Codex isolated final report
does not surface the advisory, so that conditional follow-up assertion passes.

Revisit after the selected slice. A worthwhile change would replace the existing
closure condition in `review-process.md`/`review-isolated.md`, allow one bounded
out-of-scope follow-up, and add no menu or mandatory work item to clean reviews.
It affects both modes/providers and must retain R5's no-action closure and R9's
necessary recovery mechanism in fresh paired checks. Reject added generic cleanup
suggestions or any treatment of the inherited defect as a current-PR blocker.

### Scenario order

**No instruction change now; P2, high confidence in the reporting mismatch.**
One Claude R1-standard observation changes the required failed-A/queued-cleanup
then successful-B sequence into a different ordering. The supported corruption
finding survives, but coverage of the requested sequence is unproved. The common
method already requires the actual state transitions and a scenario record.
Another sequence checklist has poor marginal value. Revisit if it recurs in a
later affected-path comparison; verify both R1 repetitions against the exact
event order, preserving the ordinary prompt and unchanged-consumer trace.

### Report precision

**Defer contained wording changes; P2 for I4, P3 for R2.** Three I4 final reports
omit the production-state qualification; hard acceptance stays open and protected
requirements remain intact. One calls fixture data “real data.” That is potentially
misleading, but not evidence of a silent requirement waiver. One Codex R2 report
finds the relevant defects yet fails to explain why green tests miss them.
Confidence in these omissions is high. Existing report fields already have space
for these qualifications. Revisit after higher-impact acquisition/claim work;
consider replacing wording in implement's completion guidance or review's coverage
guidance only if it adds no section or extra reporting phase. Verify I4's final
qualification and preserved hard requirement, R2's test-gap explanation, and I3's
proportionality across affected providers/modes. Do not use stricter ceremony for
a trivial edit to obtain a cleaner score.

### Context ordering

**Defer a local sequencing correction; P2.** One Codex I4 run begins reading
source 49 ms before the feature-document read completes; the [original grade](verification/task12/opus55/grades/codex-candidate-I4-plan-1.md)
links both timestamps. Subsequent output refreshes the handoff and preserves the
hard requirement, so harmful downstream reasoning is not demonstrated. This is
a real dependency-order violation with high evidential confidence, not missing
capture. Revisit if it recurs or a local replacement in implement's common
investigation step can make the dependency clearer without another checkpoint.
Verify I4 and the legacy plan/pre-write controls; use I3 as the cost control if
shared guidance changes. Task 12.10's preparation guard does not establish this
later context barrier, so its multi-provider hook/state cost is not justified
by this observation. Keep that probe deferred unless new evidence demonstrates
a material failure it actually addresses; design review and its GO/NO-GO gates
still apply if reselected.

### Entry-point receipts

**Investigate capture when the controller next changes; no actor fix.** Six
Codex PARTIALs have common/profile reads but lack captured successful SKILL.md
delivery. They do not prove skipped instructions. Inspect existing raw delivery
events and the capture adapter before adding any redundant actor read. A
controller correction has zero added skill words but costs sealing, calibration
and evidence review. Verify captured bytes, actor identity and ordering using
positive/missing-event controls; follow the contract's regrading/recapture rules
on both sides. Do not convert catalog metadata or a loading claim into a receipt.

### Handoff receipts

**Investigate the evidence contract before another affected capture; no actor
fix.** I3/I4 have four Codex PARTIALs for unavailable submitted arguments despite
observable reviewer reads/use. Sixteen non-R3 Codex isolated FAILs already fail
on PAL absence and also retain the exact-handoff evidence obligation. The ledger
tracks this latent gap without inventing another failed grade. R3 7.5/7.6 and
I2 9.5 alone have the approved receipt/use fallback; no extension is made here.
Revisit existing supported capture surfaces and the prior bounded investigation
before choosing capture work or requesting an explicit prospective contract
amendment. Do not repeat unchanged plaintext probes or weaken the rubric silently.
Acceptance needs original dispatch evidence or a separately authorized, calibrated
contract applied consistently to both sides. Extra actor prose cannot expose an
unavailable transport field and is not selected.

### Pre-edit assessment receipts

**No actor instruction change; defer evidence-method decision.** Both Claude
I3 PARTIALs concern an unobserved pre-edit non-runtime assessment; the exact typo
fix succeeds and the visible assessment comes afterward. Private reasoning was
excluded. There is no demonstrated inappropriate deployment gate or behavior
change. Revisit alongside handoff/entry capture decisions: determine what public
evidence can establish the current assertion, or explicitly propose a prospective
contract change. Adding a compulsory narration step to every typo fix has worse
cost than this unproved benefit. Both observations remain PARTIAL and acceptance
open until sufficient evidence or an authorized successor contract exists.

### Selected scope and verification limits

Task 12.12 selects the earliest, cheapest acquisition intervention: replace the
isolated command's ambiguous instruction location with resolved paths. It does
not claim to cure permission interpretation, all 28 acquisition observations,
R7 conclusions, implementation verification or missing transport evidence.
The entry substitution should add at most 30 authored words, zero new phases,
mandatory tool calls, dependencies or runtime state; it should eliminate discovery
work rather than add a protocol. Existing common 800/1,200-word budgets remain.
The task specifies fresh target/negative-control comparisons and rejection limits;
PAL-related composite assertions retain their full original FAILs while deferred.

The assessment itself is checked by reconciling all 608 candidate grade rows,
every non-PASS identity and matched baseline, group counts, local links and the
documentation diff. These checks establish accounting and traceability, not new
behavioral acceptance. Independent review and its outcome are recorded in the
Task 12.11 execution context.

## Task 12.12 outcome — 2026-10-11

[Twelve fresh Claude isolated comparisons](verification/task12/entry-path-no-pal/README.md)
are captured and independently graded. Candidate totals are **32 PASS / 8 FAIL /
0 PARTIAL**, versus baseline **20 / 20 / 0**. Both repetitions satisfy the local
R3 acquisition/history/ordering requirements and preserve R5 clean approval and
R9 required recovery. The eight candidate FAILs are the still-required PAL
components; positive local evidence does not turn those aggregate grades into PASS.

**Keep the correction:** only the isolated command changes, adding two words and
explicit paths to existing instructions. Common instructions and all 902 generated
Codex files remain unchanged. No new actor phase, permission or general recovery
protocol was added. The first loading probe unexpectedly connected PAL without
calling it; a separately reviewed/frozen run-local configuration then excluded
PAL for both fresh loading probes and all measured pairs. User settings, prompts,
fixtures, models and grading thresholds stayed unchanged.

The comparison uses the immutable pre-feature baseline, not an additional arm
running the immediate predecessor. Its counts do not isolate the causal effect
of two words or estimate reliability. It supports this bounded keep decision;
implementation-mode acquisition, R7 claims, receipt gaps, other matrix cases and
Codex behavior are not certified by it. Keep the ordering guard deferred.

The implementing agent still owns the remaining dispositions and acceptance
obligations above. Reassess R7's fixture and grading validity next under Task 12.14,
applying the existing cost/benefit constraint before selecting any new
operative slice. Live PAL remains user-deferred; legacy controls and Task 13
remain pending. [Final independent review](verification/task12/entry-path-no-pal/completion-review.md)
approved the completion record and bounded keep decision with no findings.
