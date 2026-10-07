# Functional and operational review

> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: draft; problem, scope and shared-context direction approved on 2026-10-07; detailed design awaiting review
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Source baseline: c2d28c9e

## Problem and evidence

The user repeatedly needed to ask whether completed implementation met requirements and whether an intermediate release would break production. Subsequent reviews found valid defects despite earlier checks passing. The desired outcome is for /kk:review-code and /kk:implement to perform that reasoning without those additional prompts.

The current workflow contains correctness, reliability and surrounding-code guidance, but its organizing activity is applying profile checklists. Standard review makes caller and contract investigation conditional on "if needed". Isolated review explicitly falls back to "code quality alone" without specification context. Its external-review preparation selects nearby files rather than the complete affected behavior. /kk:implement requires a completed code review but supplies no common record of intended behavior, compatibility constraints or evidence limits.

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

Acceptance uses the scenarios in [Evaluation](#evaluation): required behavioral assertions pass in the applicable real workflow, including negative controls. Record baseline and candidate outcomes under the same fixture, model and invocation conditions. There is no promise of zero missed bugs, no target finding count, and no claim that static structure tests establish behavioral quality.

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

### Evidence and source rules

User decisions and applicable repository instructions establish requirements. Use current design/task contracts where available; inspect linked issues when relevant without assuming that issue text is newer or more authoritative. Explain conflicts that change the assessment. Existing code proves current behavior, not intended product requirements; tests can encode the same mistaken assumption as the implementation.

The producer provides factual context with file/symbol or revision references. It labels assumptions, accepted decisions and unavailable evidence. Author explanations and claimed test results are attributed inputs, not independent verification. Reviewers may challenge an inference or request the specific missing evidence.

Never equate the review base, local main, a stable tag and the deployed revision. A compatibility statement names the baseline it actually uses. If only source at a tag was inspected, describe source-level compatibility with that tag; do not claim the deployed environment was verified.

Refresh affected fields after scope changes, a revised requirement or review fixes. On resume, inspect current repository state instead of trusting an old handoff. In plan mode, keep enduring constraints and unresolved actions in the existing implementation/task documents. Standalone work uses conversational context by default; a deferred issue must be recorded in an existing appropriate tracking location or a concise repository-local review note with a next action.

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

These conclusions do not replace P0–P3 severity or the existing code-review verdict. Supported is not a guarantee about production. Missing information is not itself an invented code defect. Continue useful review, identify what would settle the unknown, and avoid an unconditional release-safe statement.

## /kk:implement workflow

### Before editing

Load the mode procedure, shared protocols, resolved profile guidance and applicable dependency instructions first. Plan mode uses existing feature documents; standalone mode establishes the request and candidate filenames before source investigation. Move detailed standalone source investigation into the common post-instruction phase. Re-detect and load guidance when exploration adds a target covered by a new profile.

Then inspect affected behavior and assemble the change context before the first implementation edit. In plan mode, record newly established enduring delivery constraints near the implementation plan's existing constraints and in the current task's verification. Respect existing formats; do not create a parallel task system.

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

Update the shared PAL protocol only within its code-review branch; /kk:review-design must remain valid with document inputs. Maintain native external findings, reviewer attribution, independent judgments and the annotation policy. Agreement between reviewers is not a substitute for evidence. A response that reports no embedded/read source or otherwise incomplete coverage cannot support a broad clean-review claim.

Both final report modes include:

- Intent, actual review scope and baseline used.
- A compact behavior/compatibility assessment, including important paths checked and evidence limits even when defects were found.
- Existing severity-grouped or reviewer-attributed findings. For behavioral findings, give the trigger, path, expected/actual outcome, impact and suggested correction; retain profile/checklist labels, using generic for common reasoning.
- Outstanding evidence or release prerequisites with next actions. State where deferred work is recorded.

One issue spanning several lenses is one finding. Keep confidence reasoning and existing severity conventions; avoid creating a competing severity taxonomy. Preserve disagreement and uncertainty rather than silently resolving them through the author's preference.

## Instruction ordering and integration

Keep one post-instruction entry point for content-level investigation in each workflow. The standard summary, detailed procedure, isolated wrapper, agent and implement mode files must agree. Subsequent targeted verification uses evidence gathered under that phase; the wording must not prohibit re-reading evidence to substantiate a finding.

Bounded inspection necessary to resolve declared profile or conditional-load predicates remains permitted before full investigation. Load every resulting checklist before analysis. This replaces standard review's current deferred-checklist sequence and isolated review's diff-first preparation locally, without redesigning the shared detection algorithm.

The shared task-scope clarification also reaches /kk:review-spec; preserve its existing pending-task behavior and add no new mandatory change-context payload to that skill. Plugin files explain the rules in full and never link back to these toolbox design documents.

Canonical edits remain under klaude-plugin/. Generate kodex-plugin/ and .codex/agents/ with make generate-kodex after each operative slice. No new skill names, profiles, agents, dependencies or tool permissions are required.

## Evaluation

Build small synthetic fixtures, independently reproducible without private repositories, cloud access or service credentials. Stage them outside any ancestor containing SKILL.md. Assertions and expected answers are grader-only; oracles remain outside test-files/. Prompts request ordinary review or implementation and do not hint at the hidden defect.

| Case | Required observation |
| --- | --- |
| R1: changed cleanup, unchanged consumer | Trace setup A failure, setup B success, cleanup A; identify corruption of B's association. |
| R2: partial-operation retry | Detect success with discarded edited inputs and completed recovery records matching a later operation. |
| R3: disabled feature, incompatible consumer | Identify a new provider requirement reached while disabled; pending provider work does not waive present breakage. |
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

Run R1–R7 and both R9 variants through standard review and actual isolated orchestration, not only a directly prompted reviewer. Exercise R8 with a controlled degraded PAL response. Inspect the assembled independent-agent and PAL payloads for parity. Run I1/I4 through plan mode and I2/I3 through standalone mode. Existing profile-routing and pre-write-ordering evals remain regression controls.

The current review eval staging script treats every fixture file as newly added; extend it narrowly for real before/after snapshots so reviewers must discover unchanged callers and historical attribution. Full staging and grading rules are in [implementation.md](implementation.md#evaluation-staging-and-execution).

## Rejected alternatives and trade-offs

| Direction | Benefit | Cost / decision |
| --- | --- | --- |
| Add more generic checklist bullets | Smallest change | Rejected: already-present concerns can still be skipped, and implement supplies no shared intent or release context. |
| Separate opt-in functional/release review | Easy to isolate additional effort | Rejected: preserves the need for the user's additional prompt. |
| Shared context plus mandatory behavior reasoning in existing workflows | Addresses preparation, investigation and claims at their current boundaries | Selected: adds context work, controlled by relevance and evidence limits. |
| Mandatory whole-system/live-environment audit | Broader possible coverage | Rejected: unavailable access and disproportionate scope would make ordinary reviews impractical. |

The method increases review effort when a change crosses contracts or persistent state. Small changes remain small. Additional prose can become ceremony; the evals must grade demonstrated reasoning and outcomes, not whether a report repeats section names.

## Assumptions, risks and open verification

- Existing tools can inspect enough of the affected repository to trace representative paths. Missing sibling repositories must produce a bounded conclusion; they do not imply compatibility.
- Source-backed context can improve independent review without importing authorship attachment. Payload evals must prove that conclusions remain challengeable and implementation-session narratives are excluded.
- Models will follow scenario reasoning more reliably than the current optional caller investigation. Baseline/candidate behavioral evals must test this; structure checks cannot establish it.
- The existing PAL tool can receive criteria and the required evidence within a focused invocation/continuation. Verify actual coverage; its failure does not disable the local independent reviewer.
- No design-phase files exist in the installed skill-md profile. The user confirmed that profile; implementation and review must resolve its applicable phase guidance when operative skills are changed.

No product-scope decision remains open. Detailed behavior is a proposal awaiting /kk:review-design. Any failed or unrun acceptance scenario stays explicitly open in tasks.md with its reason and next action; it is not silently treated as passed.
