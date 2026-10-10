# Functional and operational review

> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: implementation slices and baseline capture complete; candidate acceptance and final verification pending
> Revised: 2026-10-10 with gate 2B closed and the candidate-6 ordering follow-up scoped
> Review disposition: [Consolidated assessment](reviews/design-review-consolidation.md)
> Evaluation contract: [evaluation.md](evaluation.md)
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Source baseline: c2d28c9e

## Problem and evidence

The user repeatedly needed to ask whether completed implementation met requirements and whether an intermediate release would break production. Subsequent reviews found valid defects despite earlier checks passing. The desired outcome is for /kk:review-code and /kk:implement to perform that reasoning without those additional prompts.

At the c2d28c9e baseline, the workflow contains correctness, reliability and surrounding-code guidance, but its organizing activity is applying profile checklists. Standard review makes caller and contract investigation conditional on "if needed". Isolated review explicitly falls back to "code quality alone" without specification context. Its external-review preparation selects nearby files rather than the complete affected behavior. /kk:implement requires a completed code review but supplies no common record of intended behavior, compatibility constraints or evidence limits.

The task-scope protocol correctly prevents reports of unfinished future work as missing implementation. It needs an explicit distinction between those expected gaps and a current increment that breaks an existing flow while awaiting future work.

User-authorized historical investigation supplied these anonymized failure patterns:

- Cleanup of one unsuccessful setup clears a different entity's valid association.
- Retrying after partial failure reports success but discards edited inputs.
- A completed recovery record incorrectly matches a later legitimate operation.
- A consumer requires a new backend acknowledgement even while the larger feature is disabled.
- A settings save receives success from an older provider without applying the requested values.
- An apparently equivalent read orchestration loses an underlying retry mechanism.

The evidence also contained findings that were real but pre-existing, unsupported as current production incidents, or overstated as release blockers. Improvement therefore includes precision and proportionality, not merely producing more findings. These examples motivate evaluation; they do not establish that instruction changes alone will improve every model's reviews. No private project names, source, records, links or transcripts belong in the distributed fixtures.

## Outcomes and acceptance

After this change:

1. A normal /kk:review-code invocation examines intended and existing behavior, affected contracts and applicable compatibility risks without a separate functional-review request.
2. /kk:implement establishes material behavior and delivery constraints before editing, then passes source-backed context to independent review.
3. Review conclusions distinguish implementation correctness, compatibility of the increment, and readiness of a particular deployment or activation.
4. Missing documents or production access narrow the conclusions; they do not disable functional review or create an automatic access/approval ceremony.
5. Evidence-based findings explain a trigger, affected path and consequence. A clean review identifies inspected paths and important limits.

Acceptance uses the scenarios in [Evaluation](#evaluation) and the binding/grading rules in [evaluation.md](evaluation.md). Every assertions[] entry in a new full-workflow eval is required; optional observations live outside that array. Predeclare model, modes and fixture revisions, then run two independent fresh sessions per baseline/candidate case and mode. All required candidate assertions must pass in both runs; a missing trace is not a pass. Retain failures and report observed results without claiming statistical reliability. There is no promise of zero missed bugs, no target finding count, and no claim that static structure tests establish behavioral quality.

The user-approved [2026-10-09 amendment](verification/run-contract-2026-10-09.md) separates implementation readiness from final verification. Both Task 2 gates are now complete: the [2026-10-10 gate 2B record](verification/task2b/README.md) preserves the bounded investigation, selected revision-2 receipt/use contract and four new Codex baselines against the immutable actor revision. Exact submitted prompt content remains unverified. Tasks 1–11 are complete; Task 12's candidate comparison matrix and Task 13's final verification remain pending. Baseline capture completion does not establish behavioral acceptance.

## Scope and ownership

| Component | Responsibility in this change |
| --- | --- |
| /kk:review-code, standard and isolated | Review the current change's behavior, consequences and justified complexity; report coverage and limits. |
| /kk:implement, plan and standalone | Establish change context before editing; verify intended outcomes and applicable compatibility; provide review context and accurate completion claims. |
| code-reviewer agent and PAL code-review framing | Receive the same applicable context and methodology; independently inspect evidence. |
| Shared task-scope protocol | Preserve pending-task exclusions while retaining current regression and compatibility responsibility. |
| /kk:review-spec | Retain full feature/specification comparison and document-consistency ownership. A changed requirement can still support a code-review finding. |
| /kk:review-design and /kk:review-architecture | Retain their current responsibilities; changes to a shared PAL protocol must preserve document-review callers. |

Functional review applies to all changes, including libraries, CLIs, infrastructure and agent instructions. Production rollout questions apply only when there is a deployment or activation consequence. For an instruction-only change, the relevant consumers may be another skill, an agent payload, a generator or an output parser.

### Not Doing

- A new opt-in review skill: the user needs this reasoning in existing invocations.
- Whole-system audits or exhaustive exploration of unrelated code: investigation follows the affected behavior.
- Mandatory live production access, deployments, migrations or activation: review does not grant those permissions.
- A redesign of /kk:design, /kk:test or /kk:review-spec: this feature improves execution and code review.
- A generic CI release-enforcement engine, new models or additional reviewer services: existing capabilities remain.
- Automatic compatibility frameworks, feature flags or concurrency machinery: choose mechanisms only for demonstrated requirements.
- A rewrite of profile detection or every language checklist: functional reasoning is a common layer supplemented by existing profiles.

## Shared change context

Add klaude-plugin/skills/_shared/change-context.md, consumed through local symlinks in implement/ and review-code/. The file defines the context fields, provenance rules, compatibility vocabulary and producer/consumer responsibilities. It is always loaded by these two skills, including when no profile matches. This is an instruction and handoff contract, not a new database or mandatory generated document.

| Field | Minimum useful content |
| --- | --- |
| Intent and authority | Intended outcomes and constraints, their source locations, and whether each is explicit, inferred or unresolved. |
| Change boundary | Current task or request, resolved diff scope, candidate revision/worktree state, affected components and deliberately pending functionality. |
| Existing behavior | Entry points, callers/consumers, state/data contracts and important invariants the change must preserve. |
| Delivery constraints | Relevant repository policy, independent or ordered deployment expectations, flags/migrations, prerequisites and accepted exceptions. |
| Baselines | Review base and candidate; separately, any released/deployed revisions, configurations and data shapes relevant to compatibility. Unknowns are explicit. |
| Scenarios and evidence | Representative success, boundary, failure/retry and lifecycle cases; source/test bindings, actual results and unverified conditions. |

Scale the record to the change. A small pure helper fix may need a few sentences; a cross-service mutation may need a compact scenario table. Empty boilerplate fields are not useful. Irrelevant operational dimensions receive a short reason. The reviewer may discover additional affected paths.

Keep change-context.md at most 800 whitespace-delimited words and functional-review.md at most 1,200, counted over each complete canonical file. These are authoring budgets, not runtime truncation. Deduplicate first and move optional examples to eval/operator documentation if a draft exceeds its budget. Preserve all normative rules; if they still cannot fit, record a justified design-budget revision before implementation acceptance instead of hiding excess content in another always-loaded file. The structure test checks both budgets and each source/symlink pair.

### Evidence and source rules

User decisions and applicable repository instructions establish requirements. Use current design/task contracts where available; inspect linked issues when relevant without assuming that issue text is newer or more authoritative. Explain conflicts that change the assessment. Existing code proves current behavior, not intended product requirements; tests can encode the same mistaken assumption as the implementation.

The producer provides factual context with file/symbol or revision references. It labels assumptions, accepted decisions and unavailable evidence. Author explanations and claimed test results are attributed inputs, not independent verification. Reviewers may challenge an inference or request the specific missing evidence.

Never equate the review base, local main, a stable tag and the deployed revision. A compatibility statement names the baseline it actually uses. If only source at a tag was inspected, describe source-level compatibility with that tag; do not claim the deployed environment was verified.

Refresh affected fields after scope changes, a revised requirement or review fixes. On resume, inspect current repository state instead of trusting an old handoff. In plan mode, record execution observations and unresolved actions in a labeled Execution context subsection of the current task in tasks.md. Distinguish observations, proposals and explicitly accepted requirement changes; an observation does not amend the specification. Standalone work uses conversational context by default; a deferred issue must be recorded in an existing appropriate tracking location or a concise repository-local review note with a next action.

### Readable historical evidence

The parent workflow owns preparation of historical source whenever a compatibility comparison requires code absent from candidate files or diff hunks. Obtain the relevant local Git blob or bounded source excerpt and materialize it in a read-only evidence bundle outside the worktree under review. Label each item with repository identity, full revision, original path, blob/content hash, original line span, and any omitted/redacted extent. Include actual source, not the parent's summary, in both independent-review payloads; distinguish historical files from candidate files and methodology.

The code-reviewer requests further evidence by naming repository, revision, path or symbol, and the comparison it needs. The parent obtains locally available source, resumes or re-invokes that reviewer with the original context and new evidence, and supplies the same relevant addition through PAL's continuation. Retain provisional findings and evidence-request provenance. No new reviewer shell permissions are needed. If the source is unavailable or bounded investigation cannot settle the question, state the specific gap and keep the conclusion Unknown; do not substitute the author's interpretation. Evidence collection does not authorize network access or production access that the task otherwise lacks.

## Functional review procedure

Add review-code/functional-review.md as the authoritative common review method. Standard review and isolated preparation load it; the code-reviewer agent receives its resolved path and loads it before analyzing evidence. PAL receives it as review criteria, distinctly identified from files under review.

After all instructions and resolved profile content have loaded:

1. Establish or reconstruct the change context. Without a spec, infer a provisional purpose from the request, diff, callers and tests; label it. Ask only when materially different interpretations prevent a useful judgment. Continue independent investigation.
2. Describe the relevant behavior before and after the change. Trace the changed entry point or caller through its meaningful dependencies to the response, side effect or durable state. Include unchanged consumers whose expectations may now fail.
3. Exercise that model with concrete scenarios. Consider success and boundaries, partial failure, retries, edits between attempts, cleanup and later reuse where those operations exist. Check whether tests actually exercise the contract and failure path being claimed.
4. Compare the approach with the requirement and existing conventions. Challenge complexity only by naming its cost and a simpler alternative that preserves the required behavior. Do not equate more abstraction with better design or treat every theoretical race as a new requirement.
5. Examine applicable delivery and compatibility consequences using the rules below.
6. Apply profile guidance as additional expertise, substantiate findings, and present conclusions with the assessed scope and evidence limits.

These are reasoning steps, not a request to mechanically enumerate every failure category for every file. Read adjacent code to answer an identified contract or impact question. Stop expanding a path once the relevant contract and consequence are established, or state the missing boundary that prevents a conclusion. A hard file-count limit must not silently truncate a necessary behavior trace.

## Compatibility and release assessment

For changes to deployable behavior, persistence, startup, configuration or inter-component contracts, identify the affected combinations that the delivery policy requires. Examples include new consumer/old provider, old consumer/new provider, partial data migration, disabled configuration, staged data, mixed versions and rollback. Select relevant combinations; do not generate an indiscriminate Cartesian product.

Deployment, feature activation and migration are distinct operations. A flag is evidence of safety only after checking whether all affected startup, read, write and consumer paths obey the relevant condition. Inspect actual error/status handling: a successful transport response or green unit suite does not establish a successful business operation.

Assess the reviewed increment first. Expand to a production-to-candidate comparison only when a requested release assessment or a relevant inherited change requires it and the baseline is available. Attribute inherited findings separately rather than treating them as introduced by the PR. If the full candidate cannot be assessed, bound the release conclusion accordingly.

Pending tasks do not excuse broken current flows. Conversely, a feature whose incomplete paths are genuinely unreachable need not implement its future tasks before an otherwise compatible increment can ship. A documented deployment prerequisite is a condition, not proof that an independently releasable-main requirement has been met.

Use these evidence-qualified conclusions for applicable compatibility rows:

- Supported: named scenarios against a named baseline support compatibility within stated limits.
- Blocked: a demonstrated incompatibility or known unmet delivery requirement prevents the stated release.
- Unknown: material baseline, environment, consumer or data evidence is missing.
- Not applicable: the change has no consequence for that dimension, with a reason.

These conclusions complement P0–P3 severity and the code-review verdict:

| Evidence | Code-review verdict | Release assessment |
| --- | --- | --- |
| Demonstrated in-scope incompatibility caused or worsened by the change | Emit one severity-rated finding based on actual impact, not an automatic P0/P1. REQUEST_CHANGES for P0/P1 or a violated hard acceptance/delivery requirement; otherwise COMMENT for an actionable nonblocking issue. | Blocked for the affected required combination. |
| Known external rollout prerequisite, with no demonstrated code defect | Assess the code on its merits; APPROVE can be explicitly scoped to code. | Blocked until the prerequisite is met; document the dependency. |
| Unknown evidence essential to task acceptance or an explicitly requested release conclusion | COMMENT if there is no demonstrated defect warranting REQUEST_CHANGES. Do not issue an unconditional approval of the unverified requirement. | Unknown with the missing evidence and next action. |
| Unknown operational detail outside the requested/required assessment | It does not automatically downgrade a supported, explicitly scoped code verdict. | Unknown for that unassessed environment. |
| Supported or Not applicable | Apply existing findings/severity rules; neither status overrides another defect. | Preserve the named baseline and limits. |

Supported is not a production guarantee; missing information is not an invented code defect. A report can approve code while withholding release readiness, but cannot use that distinction to bypass an explicit independently-releasable-main requirement.

## /kk:implement workflow

### Before editing

Load the mode procedure, shared protocols, resolved profile guidance and applicable dependency instructions first. Plan mode uses existing feature documents; standalone mode establishes the request and candidate filenames before source investigation. Move detailed standalone source investigation into the common post-instruction phase. Re-detect and load guidance when exploration adds a target covered by a new profile.

Then inspect affected behavior and assemble the change context before the first implementation edit. In plan mode, append newly observed delivery constraints and verification evidence to the current task's Execution context subsection. Correct or supersede earlier observations with a dated note, preserving their provenance. Do not silently rewrite design.md, implementation.md or acceptance criteria to fit the code. A genuine requirement change follows explicit user authorization and is recorded as such, with its source and rationale. Respect existing formats; do not create a parallel task system.

Check that the proposed approach can satisfy the requirement and the applicable delivery policy. Resolve consequential ambiguity or a proposed exception before dependent implementation. Reuse prior user authorization and decisions; routine choices do not create new approval gates. If a requirement is incompatible with the proposed mechanism, explain the concrete flow, trade-off and smallest alternatives before building it.

### Verification, handoff and completion

Implement and test the relevant outcomes, including preserved behavior and compatibility cases where applicable. Passing tests are evidence only for the cases they exercise. Use focused reproductions or existing meaningful checks; avoid duplicating tests simply to fill a category.

Refresh the change context and send it, task scope and evidence references into the existing isolated review checkpoint. The user may still select standard review. The reviewer independently checks the evidence; the implementing session cannot pre-certify the answer.

Completion reporting identifies requirement coverage, verification, review outcome, and any outstanding release/migration/activation conditions separately. A known violation of a hard task or delivery requirement prevents marking that task done unless the user has explicitly changed the requirement or accepted an exception, recorded with its rationale and prerequisites. A documented external deployment action can remain pending after code completion when that is consistent with the agreed task contract; the release assessment remains conditional or unknown.

Every deferred material action has an owner or explicitly unassigned owner, reason, concrete next step and verification condition in a durable repository location. Do not hide required work in a final chat caveat or mark the feature complete merely because code was written.

## Isolated review and reporting

The existing two-reviewer arrangement remains. Pass the same change-context facts, scope and method to the code-reviewer agent and PAL without implementation-session history. Supply resolved paths to both _shared/change-context.md and review-code/functional-review.md as instructions; the agent loads both before evidence, alongside profile checklists. The agent can inspect repository sources within its existing read-only tools. It must not claim to have run tests. The parent may provide attributed execution evidence or obtain a focused probe through tools it is authorized to use.

Replace the "code quality alone" fallback in both isolated prompts. Missing specification context still permits functional review of demonstrated behavior, caller contracts and inferred intent.

Select PAL context files by the required behavior trace: entry points, relevant dependencies, consumers, state contracts and delivery configuration. The current ten-surrounding-file cap becomes an initial selection budget, not proof that the trace is complete. Keep the first request focused; use the existing continuation capability for specific missing context or report the uncovered boundary. Do not send whole repositories by default.

Introduce explicit code-review and document-review branches in the currently flat shared PAL protocol; then add the new behavior and historical-evidence requirements to the code-review branch. /kk:review-design must remain valid with document inputs. Maintain native external findings, reviewer attribution, independent judgments and the annotation policy. Agreement between reviewers is not a substitute for evidence. A response that reports no embedded/read source or otherwise incomplete coverage cannot support a broad clean-review claim.

Both final report modes include:

- Intent, actual review scope and baseline used.
- A compact behavior/compatibility assessment, including important paths checked and evidence limits even when defects were found.
- Existing severity-grouped or reviewer-attributed findings. For behavioral findings, give the trigger, path, expected/actual outcome, impact and suggested correction; retain profile/checklist labels, using generic for common reasoning.
- Outstanding evidence or release prerequisites with next actions. State where deferred work is recorded.

One issue spanning several lenses is one finding. Keep confidence reasoning and existing severity conventions; avoid creating a competing severity taxonomy. Preserve disagreement and uncertainty rather than silently resolving them through the author's preference.

## Instruction ordering and integration

### Focused Task 12 rework — accepted continuation

After candidate 4 repeatedly failed ordering and scenario coverage, the user
accepted focused rework followed by a small R1/R3/R5 checkpoint. Preserve the
existing requirements, original grades and two-run threshold. PAL verification
remains temporarily deferred. This supersedes the earlier stop for this bounded
rework; it does not authorize silently weakening a failed assertion.

Use a local instruction-packet helper to reduce navigation during preparation.
It reads only the selected plugin's instructions, never subject code, Git state,
or evaluation material. A bootstrap packet contains the common methodology and
every detection rule named by the shared procedure. After ordinary detection and
conditional routing, a checklist packet contains the selected original profile
files with their source paths and hashes. The actor reads complete packet files
before investigation; unread/truncated packets do not open the checkpoint.
Direct source reads remain the fallback when the helper is unavailable and the
path for read-only isolated agents. No detection predicate is reimplemented.

Packet completeness and source identity are mechanically testable. They do not
prove the actor consumed the returned content or prevent arbitrary early reads;
actual ordered tool events remain authoritative. Cross-provider hook enforcement
is outside this bounded experiment: current integrations lack one shared
instruction-receipt barrier, and adding a session policy engine would exceed the
scope. The hypothesis being tested is that fewer instruction-navigation steps,
followed by one visible completion checkpoint, improve compliance.

Replace competing generic suggestions with one evidence-backed recommendation
rule. Build a compact scenario record from actual contracts: starting state,
operation/transition, expected result, candidate result and evidence. Use it for
the final coverage assessment; this connects the stated requirement to the
demonstrated path without adding fixture-specific hints or exhaustive categories.

Classify evaluation failures as procedure, behavioral correctness, or report
precision/recommendation quality for diagnosis. Keep all existing assertions
required. Classification does not alter their PASS/FAIL/PARTIAL semantics, so
the pinned rubric and both sides' prior grades remain valid.

### Proposed ordering feasibility — after candidate 6

The user approved scoping a separate ordering fix after candidate 6 passed both
clean-closure checks but still investigated source early in one repetition.
[The ordering proposal](ordering.md) recommends a bounded, controller-only
feasibility experiment for a review-scoped tool guard. It defines activation,
same-actor instruction receipts, pre-execution denial, concurrent-call ordering
and review lifetime as explicit capability gates on both declared runtimes.

This is a scoped proposal, not implemented enforcement or authorization to
expand the matrix. The earlier exclusion of cross-provider hook enforcement
still applies to operative code. Current hook documentation motivates the
experiment but does not prove support in the pinned runtimes. Preserve the
existing direct-read path, profile semantics, assertions and two-run threshold;
integrate a guard only after feasibility and design review. Task 12 remains open.

### Existing integration constraints

Keep one post-instruction entry point for content-level investigation in each workflow. The standard summary, detailed procedure, isolated wrapper, agent and implement mode files must agree. Subsequent targeted verification uses evidence gathered under that phase; the wording must not prohibit re-reading evidence to substantiate a finding.

Before operative workflow changes, amend [ADR 0004](../../../adr/0004-skill-workflow-ordering.md) and the ordering section of [AGENTS.md](../../../../AGENTS.md) to state a narrow routing exception. Current absolute wording conflicts with existing content-based detection and with this proposal; do not describe the new ordering as already fully authorized by those documents.

After basic process instructions load, bounded inspection solely to resolve a declared detection or conditional-load predicate may precede profile loading. Inspect at most approximately 16 KiB per candidate file, limited to the predicate; log the predicate/path and load every matching instruction before analyzing behavior. If bounded inspection cannot decide a conditional, conservatively load that instruction. The exception permits no findings, full-diff investigation, edits or tests. This locally replaces standard review's deferred-checklist sequence and isolated review's diff-first preparation without redesigning shared detection.

The shared task-scope clarification also reaches /kk:review-spec; preserve its existing pending-task behavior and add no new mandatory change-context payload to that skill. Plugin files explain the rules in full and never link back to these toolbox design documents.

Canonical edits remain under klaude-plugin/. Generate kodex-plugin/ and .codex/agents/ with make generate-kodex after each operative slice. No new skill names, profiles, agents, dependencies or tool permissions are required.

## Evaluation

Build small synthetic fixtures, independently reproducible without private repositories, cloud access or service credentials. Stage them outside any ancestor containing SKILL.md. Assertions and expected answers are grader-only; oracles remain outside test-files/ and are also excluded from the actor's plugin bundle/cache. Retain operative instruction bytes through a recorded filtering manifest. Every run starts with fresh fixture and Capy state, with identical empty or explicitly seeded knowledge inputs and no real session-vault history. [Evaluation isolation](evaluation.md#per-run-state-isolation) defines the controls. Prompts request ordinary review or implementation and do not hint at the hidden defect.

| Case | Required observation |
| --- | --- |
| R1: changed cleanup, unchanged consumer | Trace setup A failure, setup B success, cleanup A; identify corruption of B's association. |
| R2: partial-operation retry | Detect success with discarded edited inputs and completed recovery records matching a later operation. |
| R3: disabled feature, incompatible consumer | Identify a new provider requirement reached while disabled. The decisive released-provider implementation exists only in local Git history, outside candidate files and PR diff hunks; both independent reviewers must receive and cite historical source. Pending provider work does not waive present breakage. |
| R4: persistence compatibility | Detect a new assumption about unmigrated/partly migrated records using fixture data; no production access required. |
| R5: clean partial feature | Accept a compatible increment with unreachable unfinished paths; do not demand pending features or an elaborate release mechanism. |
| R6: pre-existing conditional defect | Attribute the old defect correctly, distinguish supported reachability from hypotheticals, and avoid an unsupported current-PR blocker. |
| R7: missing baseline and spec | Continue functional reasoning with attributed assumptions; report unknown deployment compatibility without certifying production or demanding access. |
| R8: degraded external review | Preserve substantiated available findings while disclosing incomplete external coverage; no broad safety claim from an empty/underfed result. |
| R9: stated intent and justified complexity | Detect a mismatch between an explicit requirement and behavior despite green implementation-shaped tests. In a corrected companion variant, retain a recovery mechanism needed for that requirement rather than recommending a simpler approach that loses its guarantee. |
| I1: plan-mode incompatible approach | Before editing, identify that the planned consumer change violates the supplied independent-delivery constraint; obtain a real resolution rather than assuming pending work excuses it. |
| I2: standalone meaningful change | Before editing, establish intended behavior and affected callers/contracts without creating a full feature plan or inventing product requirements. |
| I3: trivial non-runtime change | Perform required instruction/profile steps; keep functional assessment proportionate and avoid irrelevant deployment gates or duplicated tests. |
| I4: completion and resume | Refresh a stale handoff, distinguish tests from release evidence, keep a violated hard requirement open, and durably record a permitted external prerequisite. |

Run R1–R7 and both R9 variants through standard review and actual isolated orchestration, not only a directly prompted reviewer. R8 is a deliberately narrower report-phase replay with controller-supplied synthetic PAL outcomes, including success with zero source coverage and tool failure; it does not certify live MCP transport. A separate real PAL smoke run checks integration. Inspect actual agent/PAL invocations and historical evidence for required context coverage under the selected [evidence contract](evaluation.md#execution-evidence-contract); the conditional receipt/use fallback leaves exact prompt parity unverified. Run I1/I4 through plan mode and I2/I3 through standalone mode. Existing profile-routing and pre-write-ordering evals remain regression controls.

Extend the existing eval-grader with an explicit workflow mode that accepts a sealed evidence manifest, ordered tool events, captured dispatches and resulting-file snapshots. Its default component mode remains unchanged. Ordering and handoff assertions are graded from execution evidence, not claims in the final response. Details, required negative grading controls and the baseline/candidate loading mechanisms are in [evaluation.md](evaluation.md).

The current review eval staging script treats every fixture file as newly added; extend it narrowly for real before/after snapshots so reviewers must discover unchanged callers and historical attribution. Full staging and grading rules are in [evaluation.md](evaluation.md#fixture-lifecycle-and-staging).

## Rejected alternatives and trade-offs

| Direction | Benefit | Cost / decision |
| --- | --- | --- |
| Add more generic checklist bullets | Smallest change | Rejected: already-present concerns can still be skipped, and implement supplies no shared intent or release context. |
| Separate opt-in functional/release review | Easy to isolate additional effort | Rejected: preserves the need for the user's additional prompt. |
| Shared context plus mandatory behavior reasoning in existing workflows | Addresses preparation, investigation and claims at their current boundaries | Selected: adds context work, controlled by relevance and evidence limits. |
| Mandatory whole-system/live-environment audit | Broader possible coverage | Rejected: unavailable access and disproportionate scope would make ordinary reviews impractical. |
| Hold all implementation for Codex plaintext handoff capture | Completes seed capture before any operative edit | Rejected on 2026-10-09: the immutable baseline remains runnable later. Keep the capture work as an acceptance gate and bound further investigation; use the versioned receipt/use fallback if plaintext remains unavailable. |

The method increases review effort when a change crosses contracts or persistent state. Small changes remain small. Additional prose can become ceremony; the evals must grade demonstrated reasoning and outcomes, not whether a report repeats section names.

## Assumptions, risks and open verification

- Existing tools can inspect enough of the affected repository to trace representative paths. Missing sibling repositories must produce a bounded conclusion; they do not imply compatibility.
- Source-backed context can improve independent review without importing authorship attachment. Payload evals must prove that conclusions remain challengeable and implementation-session narratives are excluded.
- Models will follow scenario reasoning more reliably than the current optional caller investigation. Baseline/candidate behavioral evals must test this; structure checks cannot establish it.
- The existing PAL tool can receive criteria and the required evidence within a focused invocation/continuation. Verify actual coverage; its failure does not disable the local independent reviewer.
- No design-phase files exist in the installed skill-md profile. The user confirmed that profile; implementation and review must resolve its applicable phase guidance when operative skills are changed.

The product requirements remain approved. The ordering mechanism in
[the scoped follow-up](ordering.md) remains a feasibility question; no hard
cross-provider enforcement guarantee is established. The original two supplied
reviews were assessed in [the consolidated disposition](reviews/design-review-consolidation.md).
The new proposal has not received independent design review. Any failed or unrun
acceptance scenario stays explicitly open in tasks.md with its reason and next
action; it is not silently treated as passed.
