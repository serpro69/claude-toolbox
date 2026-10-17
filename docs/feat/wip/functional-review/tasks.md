# Tasks: Functional and operational review

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Evaluation: [evaluation.md](evaluation.md)
> Review disposition: [consolidated assessment](reviews/design-review-consolidation.md)
> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: in-progress
> Created: 2026-10-07
> Revised: 2026-10-17 with Task 12.20's adapter frozen and fresh calibration independently approved
> Next-session handoff: [advisory-closure execution record](verification/task12/advisory-closure-execution/README.md#verification-and-next-action)
> Current slice: Task 12.20 done — 25 fresh calibration controls matched; binding/state/preflight and measurement unrun
> Not Doing: new review skill, whole-system audits, mandatory production access, deployments, generic release engine, new models/dependencies, profile redesign
> Delivery: preserve existing invocations/shared consumers; regenerate Codex artifacts with every operative slice.

Scope and direction are approved; the reviews have been assessed and the detailed plan revised. Tasks 1–11 are done, including Task 2 gates 2A and 2B. Task 12's full core matrix is captured and graded; acceptance remains incomplete. **Task 12.12 is done:** keep the entry-path correction after its bounded diagnostic comparison. Remaining acceptance gates and dispositions stay open; Task 12.14's evaluation-validity reassessment is done: both target conclusions pass twice, one report-trace assertion remains failed, and no further R7 instruction change is selected. Task 13 retains final feature documentation and verification. The [gate 2B completion record](verification/task2b/README.md) documents the selected receipt/use contract, four new baselines and evidence limits. Exact submitted prompts remain unverified, and capture completion is not candidate acceptance. Earlier six-task numbering is superseded by this sequence; no completed work was renumbered. Size includes authored reasoning complexity; mechanical copies/symlinks/generated files are excluded. Parallel markers permit compatible work only and do not authorize delegation. Serialize generation if tasks run concurrently.

## Task 1: Prove revision-bound evaluation loading

- **Status:** done
- **Depends on:** —
- **Size:** M
- **Strategy:** Risk-First
- **Can run in parallel with:** —
- **Docs:** [Instruction binding](evaluation.md#bind-the-actual-instructions)

### Subtasks

- [x] 1.1 Preserve c2d28c9e as the unchanged actor baseline and prepare a separate candidate loading location; write the initial verification/run-contract.md → verify: baseline identity, primary provider, modes, models and two-run threshold are fixed before measured results; candidate hashes are frozen before each later candidate batch.
- [x] 1.2 Build filtered Claude/Codex actor bundles with source, exclusion and retained-file manifests → verify: operative bytes are unchanged and bundles/cache copies contain no eval metadata, oracles, grading fixtures, results or links into an unfiltered checkout.
- [x] 1.3 Prepare fresh probe workspaces and run-local Capy servers/stores with the declared unavailable-vault policy → verify: knowledge indexing works, a marker from probe A is absent from probe B, and no real store, history or prior fixture mutation is inherited.
- [x] 1.4 Probe Claude loading through --plugin-dir plus the existing CPR_PLUGINS_FILE override → verify: entry points, agents, hook-exported root and instruction reads all resolve to the selected filtered bundle.
- [x] 1.5 Probe Codex through separate local marketplaces, refreshed filtered-cache hashes and project-scoped generated agents → verify: loaded skill and role bytes match the chosen bundle; runtime unavailability is an explicit blocker to that provider's runs.
- [x] 1.6 Record actual launch configuration, bundle scan and state-isolation evidence → verify: a root-only override, mixed installed cache, evaluator-material leak or reused knowledge state cannot count as a full-skill comparison.

### Execution context — 2026-10-08

Observed evidence: [verification record](verification/README.md), [run contract](verification/run-contract.md), and [independent controller review](verification/review.md). Baseline source identity is the full c2d28c9e commit; 435 operative files retained, 836 evaluator files excluded. Fresh Capy stores passed actual search/index and unavailable-vault probes. Eight controller tests and nine existing shell suites passed (three existing skips). Controller review findings were fixed and independently re-reviewed; no operative skill changes or measured behavioral runs occurred.

Initial authenticated Claude loading failed because OAuth expired; the user refreshed login. Fresh baseline and candidate-location probes then passed registered entry-point reads, hook-root binding, named reviewer dispatch, child instruction reads and run-local Capy marker retrieval. Earlier failed attempts remain retained, not counted as passes.

Codex's two filtered installed caches, generated role-file bytes, isolated trusted catalogs and registered skill reads passed. The first ephemeral CLI stream omitted child evidence. Fresh persisted runs resolved this: actual parent dispatch, child linkage/model, exact emitted public role-body bytes, child reads and Capy results are retained for both locations. Independent review verified those relationships. Temporary Codex trust and evaluation plugin/marketplace registrations were approved, used, and removed; normal configuration remains.

Task 1 is complete. These are loading probes only, with unchanged baseline bytes in the candidate loading location. Task 2 remains pending; fixture/grader/candidate hashes must be frozen before their measured batches. No acceptance threshold or provider selection changed.

## Task 2: Create final seed fixtures and capture every workflow baseline

- **Status:** done
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Tasks 3–11 (gate 2B only, after 2A)
- **Docs:** [Baseline preparation](implementation.md#baseline-preparation), [capture resolution](evaluation.md#codex-handoff-capture-resolution), [run-contract amendment](verification/run-contract-2026-10-09.md)
- **Gate 2A — implementation readiness:** done; final fixtures, frozen inputs and 16 baseline captures retained. Satisfies Task 3's prerequisite without asserting behavioral acceptance.
- **Gate 2B — capture completion:** done; all four missing Codex baselines captured and independently graded under revision 2. Original captures remain preserved. Task 12 retains candidate comparisons and acceptance.

### Subtasks

- [x] 2.1 Create complete final R1/R3 eval directories under review-code/evals/ and I1/I2 under implement/evals/, including eval.json and grader-only oracles → verify: later tasks reuse these exact directories and all new IDs avoid existing IDs.
- [x] 2.2 Stage seed snapshots manually in disposable repositories; create R3's released-provider history/tag → verify: the decisive old source is absent from candidate files and PR hunks but present in local Git.
- [x] 2.3 Complete baseline captures under the evidence contract selected by 2.5–2.6, using immutable c2d28c9e and fresh workspace/knowledge state per run → verify: retain the existing 16 captures and four fresh Codex R3-isolated/I2-standalone runs (two each), plus any required baseline recaptures, with ordered events, reviewer evidence, initial/final files and bundle/state identity. Capture completion does not require baseline behavioral PASS; candidate counterparts remain Task 12 work.
- [x] 2.4 Freeze fixture hashes and the grader procedure/rubric with the captures → verify: subsequent paired runs use identical fixture bytes and any changed fixture requires both sides to rerun.
- [x] 2.5 Conduct one bounded capture investigation under [the resolution procedure](evaluation.md#codex-handoff-capture-resolution) → verify: record a supported alternative and at most one fresh marker probe, or document that no viable alternative exists; retain the outcome and stop repeating unchanged capture paths.
- [x] 2.6 Record the selected evidence contract before further handoff-dependent captures → verify: a successful probe retains exact-handoff assertions; otherwise version the rubric/assertion mapping for observable reviewer receipt and use, preserving the original freeze and disclosing that exact prompt content is unverified. Record regrading/recapture obligations for Tasks 8/12 and baseline recaptures for 2.3. Close 2B only after 2.3, 2.5 and 2.6 are complete.

### Execution context — 2026-10-08

Observed evidence: [Task 2 verification](verification/task2/README.md), [frozen inputs](verification/task2-frozen.json), [grading procedure](verification/task2-rubric.md), and [independent review](verification/task2/review.md). Final seeds use review IDs 6/7 and implement IDs 8/9; no fixture or rubric changed after freeze. Real before/after reproductions and local R3 release history match the declared oracle. Codex copies regenerated without drift; no operative instructions changed.

Captured 12 Claude baseline workflows (all six seed/mode pairs twice) and four Codex baselines (R1 standard/I1 plan twice), all against immutable c2d28c9e in fresh workspaces with empty run-local knowledge. Capy 0.16.8 was declared before capture and passed fresh isolation probes. Traces retain permission denials, actual dispatches/results, payload artifacts and initial/final files; capture completion is not behavioral acceptance. Three failed controller attempts remain retained. Fifteen controller tests, all nine shell suites and plugin graph checks passed; corrected capture code passed independent review.

**Capture disposition at 2026-10-08 — superseded for sequencing by the decision below.** Codex R3 isolated and I2 standalone remained **UNRUN**, two repetitions each. Public app-server history and separately trusted observation hooks omitted/encrypted submitted reviewer messages; a final claim could not satisfy exact-handoff evidence. The original contract held Task 3 until plaintext capture was established. Temporary Codex trust/hook/plugin registrations were removed. These observations did not establish behavioral acceptance.

**Capture note from Task 1 — owner: implementing agent.** Codex CLI JSON omits some child events; persisted parent/child runtime records expose them. The parent dispatch's message field is encrypted. Before any later exact-handoff assertion is captured, retain plaintext at submission or use another supported trace surface alongside the encrypted record. Task 1's role bytes/read results prove loading, not exact plaintext handoff content; ciphertext alone cannot pass that later assertion. See [completed probe evidence and limits](verification/README.md#completed-probes-after-login-refresh).

### Accepted sequencing decision — 2026-10-09

The user approved separating implementation readiness from full verification, one bounded capture investigation, and a conditional fallback to observable reviewer receipt/use if plaintext remains unavailable. Gate 2A is satisfied by the frozen fixtures and retained captures; Task 3 may start. Gate 2B remains owned by the implementing agent and blocks Task 12 and feature completion, not Tasks 3–11. The immutable baseline can be launched after candidate development without using candidate instructions.

Subtasks 2.5–2.6 own the deferred capture work because the tested Codex surfaces cannot expose the required messages. Follow the [run-contract amendment](verification/run-contract-2026-10-09.md) and record the bounded investigation's outcome before choosing the evidence path. No new probe, rubric revision, capture or behavioral grade is claimed by this documentation update. Existing captures, manifests, frozen rubric and assertions remain unchanged; a fallback requires a separately versioned contract applied to both sides. Provider coverage and the two-run candidate threshold remain required.

### Gate 2B execution context — 2026-10-10

**Authority:** the user approved proceeding with the receipt/use proposal and resolving gate 2B. Preserve revision-1 evidence and unchanged actor baseline `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; Task 12 candidate acceptance remains separate. All eight installed profile detection rules and applicable Python core/skill-md guidance are loaded; no async constructs or new dependency is planned. Installed schemas and official documentation supply app-server API lookup because no Context7 capability is available in this session.

**Bounded investigation:** installed Codex is 0.162.1 (retained runs used 0.161.0); this host is Linux with Python 3.12.11 available for the controller. The public collaboration prompt remains optional. `debug prompt-input` accepts an optional new prompt but no recorded thread/child selector; it cannot establish an actual submitted child message. Hook documentation supplies child IDs but no submitted-message field. No viable materially different plaintext surface was found; no further plaintext marker probe is warranted. Proceed with a separately frozen receipt/use contract. Runtime binding/receipt and state-isolation checks are still required before measurement.

**Superseding completion:** [revision-2 contract and evidence](verification/task2b/README.md) record the selected fallback before measurement, unchanged subject files/prompts, grader pin/calibration, and all four fresh Codex baselines. Final independent grades are **21 PASS / 9 FAIL / 0 PARTIAL**. Changed assertions in retained Claude traces yield six demonstrable FAILs without a PARTIAL requiring baseline recapture for this rubric change. Original evidence and grades are preserved. Missing exact prompts and some child verification-result receipt remain unknown; independently observed false components establish baseline failures without pretending those positive components were seen.

**Review and checks:** [independent review](verification/task2b/review.md) approved capture completion after correcting a premeasurement staging-validator mismatch and replacing insufficient PAL history markers with successful-read/format/inclusion evidence. All four graders reassessed the stronger sealed packages. Twenty-three new controller/adapter tests, 15 retained tests, all ten shell suites (644 assertions), Go/graph checks and repeated generation pass. The host-Python generation failure is retained; the declared Python 3.12 rerun passed with identical bytes across 892 generated files. All temporary trust entries and the evaluation plugin/cache were removed.

**Gate 2B is closed; Task 2 is done.** Task 12 is next and must use matching declared configurations and consistent grader pins, regrade or recapture affected pairs where necessary, and establish every required candidate component twice. Task 13 and feature acceptance remain pending.

## Task 3: Align the instruction-routing convention

- **Status:** done
- **Depends on:** Task 2 gate 2A (done); does not wait for gate 2B
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Routing-convention slice](implementation.md#routing-convention-slice)

### Subtasks

- [x] 3.1 Amend docs/adr/0004-skill-workflow-ordering.md with the narrowly bounded routing exception and its rationale → verify: predicate inspection is distinct from behavioral analysis and preserves instruction-before-action.
- [x] 3.2 Update AGENTS.md ordering wording consistently → verify: approximately 16 KiB bounds, declared predicates, conservative loading when undecidable, and the prohibition on early findings/edits/tests agree with the ADR.

### Execution context — 2026-10-09

Implemented the accepted [routing-convention slice](implementation.md#routing-convention-slice) in [ADR 0004](../../../adr/0004-skill-workflow-ordering.md) and [AGENTS.md](../../../../AGENTS.md). Both require basic instructions before predicate-only inspection, approximately 16 KiB per candidate file, predicate/path logging, conservative conditional loading, and all selected guidance before investigation. The single investigation entry point permits later targeted verification reads. The ADR distinguishes this convention amendment from pending operative adoption in Tasks 4–5; no behavioral acceptance is claimed.

Verification: profile detection returned no active profiles for these three repository documentation files. All nine `test/test-*.sh` suites passed with 630 assertions and no skips; `git diff --check` and new ADR link-target checks passed. Initial schema-validation attempts were blocked by sandbox access to the `uv` cache; approved access resolved them. Template fixture runs used per-command `commit.gpgsign=false` to avoid inheriting personal signing requirements. No persistent Git settings changed. Canonical plugin files were unchanged, so regeneration was not required.

Review: /kk:review-code:isolated's independent code-reviewer inspected the diff and source documents against Task 3 and returned APPROVE with no findings. PAL (`gemini-3.1-pro-preview`) also returned no findings, but reported zero embedded files; its source coverage is unverified and does not establish corroboration. No systemic P0/P1 findings required indexing. Task 3 is complete without changing requirements; Task 2 gate 2B and all later implementation/acceptance work remain open.

## Task 4: Standard review assesses behavior and compatibility

- **Status:** done
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Standard review slice](implementation.md#standard-review-slice)

### Subtasks

- [x] 4.1 Add _shared/change-context.md, review-code/functional-review.md and the review-code/shared-change-context.md symlink → verify: all required semantics fit the 800/1,200-word ceilings and links resolve.
- [x] 4.2 Update review-code/SKILL.md and review-process.md for instruction loading, behavior tracing, historical evidence, coverage and verdict mapping → verify: R1 is detected through an ordinary prompt and material Unknown evidence is qualified.
- [x] 4.3 Clarify _shared/review-scope-protocol.md → verify: current incompatibility remains reportable while genuinely pending work is excluded; /kk:review-spec's existing payload remains valid.
- [x] 4.4 Add shared-source/symlink and word-budget assertions to test/test-plugin-structure.sh → verify: exact targets, resolution, regular-file substitution and excess wording are checked; do not register the implement link before it exists.
- [x] 4.5 Regenerate Codex output and run structure/graph checks plus the seed standard dry-run → verify: canonical/generated parity and evidence-backed reporting; preserve actual results for later paired grading.

### Execution context — 2026-10-09

Implemented the shared change context (573 words), common functional method (877 words), standard instruction/routing/investigation sequence, historical-evidence and verdict guidance, and shared task-scope clarification. The canonical review-code link has the required relative target; generated consumer copies, including review-spec's existing scope protocol, are refreshed. No skill description or dependency changed. Profile detection activated `skill-md`; all three applicable implement/review checklists were loaded, with the accepted Task 3 routing exception taking precedence over older absolute checklist wording.

[Local verification](verification/task4/checks.json): all nine shell suites passed (640 assertions, no skips); five disposable mutation checks rejected regular-file replacement, wrong/broken targets and either word-budget overflow. `make generate-kodex`, a second-generation hash comparison across 684 files, `make plugin-graph`, Bash syntax and whitespace checks passed. The graph's cycle warning is retained in its log. Independent code review found no substantiated defects, while the required R1/ordering behavioral evidence remains Unknown.

**Verification completed after user approval.** The user authorized the prepared Claude/PAL checks. The [run contract](verification/task4/run-contract.md) and [verification record](verification/task4/README.md) retain the original approval rejection, an incomplete binding attempt, its successful fresh retry, and candidate1's failed ordering trace. Candidate1 read the diff before Python checklists. The correction adds a returned-content loading ledger/checkpoint and explicit profile enumeration. Final candidate `d0ab5f0122724c050c2ecbd4563bb6e6fce2b68c` passed binding; its fresh ordinary-prompt R1 run loaded the common method and all applicable Python checklists before investigation, inspected the unchanged consumers and README, ran the two passing existing tests, and reproduced failed-A cleanup deleting successful B's association. It recommended the ownership check and returned REQUEST_CHANGES. Final generation, graph and 684-file freshness checks passed; capture and source-manifest hashes verified. Fixtures, rubric, model, permission policy and baseline were unchanged.

Independent source review and execution-evidence audit approved the Task 4 slice with no actionable source findings. PAL returned two native LOW wording suggestions; its zero embedded-file count and retained earlier review context leave coverage/isolation unverified, so it is not corroboration. Details and author context are in [review.md](verification/task4/review.md). No systemic P0/P1 implementation finding required indexing.

**Deferred verification — owner: implementing agent, Task 12.** Candidate2 skipped the full known-profile detection enumeration and `kk:lang-idioms` lookup; these remain failed procedural observations. Its P0 severity is not validated by this audit and differs from the fixture's suggested P1/justified P2. Re-run the existing routing controls, check the omitted procedure steps and grade severity against supported impact under the pinned Task 8 grader before final acceptance; fix and recapture affected cases if required. One intermediate dry-run is not a paired matrix pass. Task 2 gate 2B, Task 12's two-run threshold and feature completion remain open; Task 4 completion waives none of them.

## Task 5: Isolated reviewers independently compare current and historical behavior

- **Status:** done
- **Depends on:** Task 4
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Isolated review slice](implementation.md#isolated-review-slice)

### Subtasks

- [x] 5.1 Update review-code/review-isolated.md to prepare change context and bounded historical-source bundles after instruction loading → verify: R3's old-provider blob and provenance reach both reviewers.
- [x] 5.2 Update agents/code-reviewer.md with common-method loading and explicit additional-evidence requests → verify: the parent can supply requested local history through resume/reinvoke; unavailable evidence remains Unknown without adding shell access.
- [x] 5.3 Introduce code-review/document-review branches in _shared/pal-codereview-invocation.md and align commands/review-code/isolated.md → verify: PAL receives the same material facts; /kk:review-design remains compatible.
- [x] 5.4 Apply evidence-qualified reporting while preserving native findings and author annotations → verify: no quality-only fallback, unsupported corroboration or broad approval from incomplete external coverage.
- [x] 5.5 Regenerate output, run structure/graph checks and the R3 isolated dry-run → verify: actual dispatches/read artifacts prove the historical comparison, not the parent's summary.

### Execution context — 2026-10-09

Implemented the approved isolated-review slice in the workflow, code-reviewer agent, shared PAL protocol and command wrapper. Both reviewers receive the common method, factual context, all resolved criteria and historical source with provenance. The parent resolves named local baselines before declaring them unavailable, handles additional-evidence requests through continuation/reinvocation, and checks criteria/receipt before qualified reporting. The document-review PAL branch preserves its existing caller. No dependency, model, tool permission or requirement changed.

[Verification](verification/task5/README.md): all nine shell suites passed (640 assertions, no skips after environment-limited retries). Generation, plugin/Codex structure tests, plugin graph validation and second-generation comparison across 684 generated files passed. Current canonical/generated/agent contents match frozen candidate `33ba4a2697cdfcb5f48a701f39e45bf347e08c53` across 1,379 source entries. Original seed/rubric hashes remain unchanged. Initial generator wording failures, sandbox-limited checks and all failed actor attempts are retained rather than relabeled.

The ordinary-prompt R3 isolated run loaded all eight detection rules and applicable common/Python criteria before investigation, resolved the released provider from local Git, delivered the actual source and all eight criteria to both reviewers, and identified the flag-off incompatibility with REQUEST_CHANGES. Its provenance manifest still contained a command placeholder for the blob hash. The [declared supplemental review](verification/task5/run-contract.md) exercised the additional-evidence path: actual Git lookup/hash results matched, a corrected manifest preserved the original, and both reviewers received and used the correction. The expired PAL continuation was explicitly replaced by a fresh two-step review carrying only PAL's own prior findings. The first supplement's command denial is retained; its retry used directly permitted Git commands without changing policy. All completed captures retain ordered public events and hashes; subject files and actor bundles stayed unchanged.

[Independent review and evidence audit](verification/task5/review.md): source findings were corrected and re-reviewed. The final audit returned APPROVE scoped to Task 5, with no remaining hard slice blocker or systemic P0/P1 implementation finding to index. The initial run's missing provenance is not retroactively a pass; the supplement is not a fresh matrix repetition. This took more iteration than source checks suggested: actual traces exposed early diff reads, incomplete criteria manifests and unsupported absence/receipt assumptions. Explicit loading/manifest checks and named-baseline lookups address those observed paths.

**Deferred acceptance — owner: implementing agent, Tasks 8/12.** Pin and apply the workflow grader, run all required fresh baseline/candidate pairs and routing/reporting controls, and calibrate severity against supported impact. Every required assertion must pass twice under the selected contract; the preserved failed attempts and supplemental repair do not waive that threshold or establish model reliability. Task 2 gate 2B remains open. Task 5 is complete as an implementation/integration slice; Task 6 is next and the feature remains in progress.

## Task 6: Implementation establishes constraints and hands off verified context

- **Status:** done
- **Depends on:** Task 5
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Implementation slice](implementation.md#implementation-slice)

### Subtasks

- [x] 6.1 Add implement/shared-change-context.md and integrate it in implement/SKILL.md → verify: both modes load the shared contract and profiles before source investigation/edits.
- [x] 6.2 Align plan-mode.md and standalone-mode.md with the execution core → verify: one authoritative post-instruction investigation phase; existing pre-write controls remain valid.
- [x] 6.3 Establish intended outcomes, affected contracts and delivery constraints; record observations in the current task's labeled Execution context → verify: I1 detects its conflict and observations cannot silently amend specifications.
- [x] 6.4 Refresh evidence for independent review and separate task completion from deployment conditions → verify: real handoff uses finished Task 5 consumers, stale evidence is rejected and a hard unmet requirement stays open.
- [x] 6.5 Extend shared-link structure assertions for implement, regenerate output and verify both modes → verify: exact link targets and budgets pass; I2 remains usable without a full feature plan.

### Execution context — 2026-10-09

**Accepted scope:** the user's request to implement the next task selects Task 6 after completed Task 5. The accepted 2026-10-09 sequencing decision leaves Task 2 gate 2B and full matrix acceptance open; this task does not waive them. Sources: this task, [implementation slice](implementation.md#implementation-slice), and [implement contract](design.md#kkimplement-workflow).

**Observed before edits:** repository base `61093fc7d610f44d3eba7f861bc4058a8f3c384b` with a clean worktree. The standalone entry currently reads source before profile loading; plan entry and the shared execution core duplicate ordering/completion rules. The Task 5 review consumers already accept the shared factual context and own both independent reviewer handoffs. Preserve those invocations, the standard-review override, profile/dependency/test steps and accurate task scope. This instruction-only slice has no deployment operation; compatibility concerns are instruction ordering, shared consumers and generated Codex output.

**Instruction loading:** all eight installed detection rules were read. `skill-md` activates through implement/SKILL.md and sibling adjacency; its universal, Claude Code and kk-plugin implement guidance loaded. Provider guidance is selected by the plugin's hooks/commands/agents directories; kk guidance by canonical klaude-plugin paths. No dependency change. Verification and review are pending; no behavioral acceptance is claimed.

**Initial verification and source review:** [643 shell assertions](verification/task6/check-summary.json) pass with no skips; Go tests, plugin graph and [685-file regeneration freshness](verification/task6/freshness.json) pass. Initial environment-limited attempts are retained. The independent review identified a pre-profile requirement-read exemption; the corrected candidate moves full requirements/knowledge lookup after profiles and has no remaining source findings. PAL also found no source defects, with actual file embedding recorded. See [review](verification/task6/review.md).

**Earlier slice gate — subsequently completed below:** complete the frozen I1/I2 mode dry-runs and independent execution-evidence audit under [the Task 6 run contract](verification/task6/run-contract.md), then verify subtask outcomes before marking done. Automatic approval review initially rejected the external launch; the user explicitly approved these Claude/PAL runs. The first binding probe did not observe the shell root; a fresh retry uses the directly allowed command. Full matrix acceptance and Task 2 gate 2B remain open.


**Superseding completion — 2026-10-09:** final candidate `10463ff31d654520b5712f1dc053407fccf48e9b` implements the shared context, metadata-first mode entry, one common investigation phase, explicit requirement-decision boundary, refreshed actual review evidence and accurate completion/follow-up gates. [Final verification](verification/task6/README.md) records the approved Claude/PAL runs, failed attempts, frozen identities and [candidate6 freshness](verification/task6/freshness-candidate6.json). All 643 shell assertions, Go tests, structure and graph checks pass; 685 generated files remain unchanged on second generation and 1,381 source entries match the final candidate.

**Observed integration and independent review:** I1 records the contradictory outcomes and proposals, requests a real decision and changes only task observations; client/provider/tests/design/implementation remain unchanged. I2 inspects callers before editing, passes six focused tests, rejects stale scratch evidence before review and sends current source plus all eight criteria to both independent reviewers. Its PAL payload contains no child conclusions and precedes the child final report. The [independent source/evidence audit](verification/task6/review.md#final-disposition) returns **APPROVE scoped to Task 6**, with no remaining hard slice blocker. Native PAL source results remain attributed opinions, not runtime guarantees. No systemic P0/P1 implementation findings or new project conventions require indexing.

**Deferred acceptance — owner: implementing agent, Tasks 8/12:** formal per-assertion grading, fresh repeated comparisons, existing routing/pre-write controls and I3/I4 remain open. The final I2 run is bounded integration evidence, not a pristine matrix run: it saw a previous scratch patch before rejecting/replacing it. Also retain metadata overfetch, broad/late or omitted knowledge lookup and copied-diff context-space loss. Next actions: ensure fresh run-owned scratch evidence and exact diff materialization, tighten metadata/knowledge procedure execution, then grade/recapture affected cases under the pinned contract. Verification condition: every required assertion passes twice with fresh inputs and actual handoff evidence; failed/unknown observations never count as PASS. Task 2 gate 2B still blocks Task 12 and feature completion.

**Reflection:** static source review was insufficient to establish execution behavior. Actual traces exposed early reads, workflow bypass, self-authorized requirement relaxation and contaminated external review. The final instructions make the loading checkpoint, conflicting-outcome comparison and review handoff explicit. Plan requirements and acceptance were preserved; no fixture, model, tool policy or threshold changed. Task 6 is complete as an implementation/integration slice; Task 7 is next.

## Task 7: Stage before/after and historical fixtures reliably

- **Status:** done
- **Depends on:** Task 6
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Evaluation staging slice](implementation.md#evaluation-staging-slice)

### Subtasks

- [x] 7.1 Extend review-code/evals/_harness/setup.sh for paired snapshots and optional history.json while preserving flat fixtures → verify: base/candidate diff and local release history match the fixture contract.
- [x] 7.2 Add test/test-review-eval-staging.sh → verify: offline tests cover added/changed/deleted/unchanged and hidden files, tagged historical source, malformed pairs/history, escaping links, .git entries and destination refusal.
- [x] 7.3 Stage the existing seed directories through the helper → verify: wrappers, eval metadata and oracle answers stay outside the actor workspace; fixture hashes remain comparable.

### Execution context — 2026-10-09

**Accepted scope:** the user requested Task 7. Task 6 is complete; the accepted sequencing decision leaves Task 2 gate 2B and Tasks 8–13 open. Requirements come from this task and [fixture lifecycle and staging](evaluation.md#fixture-lifecycle-and-staging).

**Observed before edits:** the helper copies every fixture as added against an empty commit, reuses caller destinations and deletes existing eval subdirectories. Preserve flat staging, stdout's absolute stage path and complete hidden/unchanged context; add paired snapshots, ordered tagged history and refusal of existing destinations. R3's frozen manifest uses `snapshots` entries with `path` and `tag`. Repository-local offline checks establish staging behavior, not actor review quality or deployment readiness.

**Instruction loading:** all eight installed detection rules loaded. `skill-md` activates for the harness through its nearest `review-code/SKILL.md`; universal, Claude Code and kk-plugin implement guidance loaded (provider directories and canonical paths satisfy both conditional predicates). No test-phase guidance exists for this profile. Use existing Git and Python 3 standard-library tooling, without adding packages or changing fixture bytes. Verification and isolated review are pending.

**Superseding completion — 2026-10-09:** the helper now stages complete before/after trees, optional ordered historical commits/tags and legacy flat fixtures in fresh owned destinations. It preserves hidden/unchanged context, stages deletions, isolates Git configuration and rejects unsafe snapshot paths, links, metadata and refs before staging. `HEAD` and `eval-base` identify the review base. The harness playbook and generated Codex copies reflect the staging contract.

[Verification](verification/task7/README.md): all ten shell suites passed (644 helper assertions, no skips), including 20 staging integration tests. Actual R1/R3 and all five legacy review fixtures stage correctly; R3's released source is reachable through its tag and absent from base/candidate files and the PR diff. All 51 frozen R1/R3/I1/I2 file hashes remain unchanged. Go tests, graph validation, shell syntax, structure checks and [685-file regeneration freshness](verification/task7/freshness.json) passed. Environment-limited and mistaken-path attempts are retained with their successful corrections.

[Independent review](verification/task7/review.md) returned **APPROVE scoped to Task 7** after fixing a reserved `eval-base/` tag-namespace conflict. A focused reproduction and regression verify rejection before any Git operation. PAL returned no actionable findings, but zero embedded/examined files leave its coverage unverified; it is not corroboration. No systemic P0/P1 findings or new project conventions require indexing.

**Evidence limits:** these are offline staging checks, not actor behavioral acceptance. Task 2 gate 2B and Tasks 8–13 retain their existing owners, next actions and verification requirements. Task 8 is next; the feature remains in progress. No requirement, fixture, model, capture contract or acceptance threshold changed.

## Task 8: Grade workflow behavior from execution evidence

- **Status:** done
- **Depends on:** Task 7
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Workflow-grading slice](implementation.md#workflow-grading-slice), [evidence contract](evaluation.md#execution-evidence-contract)

### Subtasks

- [x] 8.1 Extend agents/eval-grader.md with explicit workflow mode and manifest-limited Read access → verify: the omitted/default mode preserves the legacy component contract.
- [x] 8.2 Update review-code/evals/_harness/HARNESS.md and add implement/evals/README.md for capture, dispatch evidence, resulting-file snapshots and mode selection → verify: acting sessions never receive grading material.
- [x] 8.3 Add and grade calibration records → verify: an early edit despite a reassuring final response is FAIL, missing events are PARTIAL, and complete correct ordering is PASS; legacy component grades stay compatible.
- [x] 8.4 Pin the grader implementation and grade available baseline traces under the same versioned contract used for candidate traces → verify: no self-attested ordering or payload claim substitutes for execution evidence; regrade affected traces if 2.6 later selects the fallback, and leave missing captures for 2B/Task 12 rather than blocking grader implementation.
- [x] 8.5 Regenerate the grader/playbook output and run structure/graph checks → verify: both distributions preserve the explicit mode boundary.

### Execution context — 2026-10-09

**Accepted scope:** the user requested Task 8. Task 7 is complete. Grade the 16 retained baseline captures under the frozen revision-1 rubric; Task 2 gate 2B retains the four missing captures and any later fallback/regrading obligations. No candidate acceptance or capture-contract change is implied.

**Observed before edits:** the grader currently judges output text only and exempts itself from instruction loading. The harness has only the component path; there is no implementation-eval playbook. Preserve omitted-mode component inputs/output and Read-only tools while adding an explicit, sealed-evidence workflow path. Capture evidence already includes returned tool content, payload artifacts and initial/final files; completeness must be assessed per assertion, not inferred from a successful runtime exit.

**Instruction loading:** all eight installed detection rules loaded. `skill-md` activates through harness/implementation-eval adjacency to their skill roots; universal, Claude Code and kk-plugin implement guidance loaded. Provider directories and canonical paths satisfy both conditional predicates. The accepted bounded-routing convention takes precedence over older absolute wording. No new dependency or live deployment action is needed. Verification, calibration and isolated review are pending.

**Superseding completion — 2026-10-09:** explicit workflow grading now uses sealed manifests, completed instruction reads, actual dispatches and resulting files; omitted mode preserves component text grading. Both harness playbooks document actor/grader isolation and versioned evidence contracts. [Verification](verification/task8/README.md) retains seven accepted calibration controls, two superseded component input-shape attempts and all 16 baseline grades under the [pinned grader/revision-1 rubric](verification/task8/inputs/pin.json): **51 PASS / 44 FAIL / 11 PARTIAL across 106 assertions**. Both Codex R1 standard baselines pass every assertion; no candidate comparison or model-reliability claim follows.

**Checks and review:** all ten shell suites pass (644 helper assertions), eight evidence-adapter tests pass, Go/graph checks pass and second generation preserves 725 files. Frozen seed/rubric bytes remain unchanged. [Independent review](verification/task8/review.md) returns **APPROVE scoped to Task 8** after restricting event/oracle imports to original seals and correcting trusted-root alias handling. The corrected adapter reproduces all 611 graded evidence files unchanged; original preparation source and failed attempts remain retained. Native PAL findings and zero-file coverage are disclosed; they do not establish corroboration. No new project convention or systemic P0/P1 implementation finding requires indexing.

**Deferred acceptance — owner: implementing agent, Tasks 2 gate 2B and 12:** four Codex captures remain UNRUN; candidate comparisons and intermediate Task 4–6 recapture/grade obligations remain open. Follow the bounded capture investigation and record any fallback before measurement; if selected, add receipt/use calibration and regrade affected baseline/candidate evidence, recapturing both sides where insufficient. Every required candidate assertion must pass twice. The grader runtime used fresh default agents loading pinned bytes, with a read-only command adapter; exact service-model identity and OS confinement are not claimed. Future comparisons must use a consistent declared grading runtime or regrade both sides under a new pin. Task 9 is next; feature completion remains open.

## Task 9: Author state, retry and intent scenarios

- **Status:** done
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 10, Task 11
- **Docs:** [Fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [x] 9.1 Add R2 retry/lifecycle and R4 stored-data compatibility scenarios in final review-code/evals directories → verify: each failure has a supported synthetic path and precise required assertions.
- [x] 9.2 Add separate R9 mismatch and justified-complexity companion directories → verify: green implementation-shaped tests do not excuse a requirement mismatch, and necessary recovery behavior is preserved.
- [x] 9.3 Validate files[], numeric IDs and oracle placement; regenerate fixture output → verify: no prompt leaks an expected finding and no duplicate minimal fixture is created.

### Execution context — 2026-10-09

**Accepted scope:** the request for the next task selects Task 9 after completed Task 8. Author final R2, R4 and both R9 fixtures only; Task 2 gate 2B and Tasks 10–13 remain open. Sources: this task, the design's evaluation table and the implementation's fixture-authoring slice. No requirement or capture contract changes.

**Observed before edits:** clean base `c554f92d4bde6b1dbf98335fa1d450a57c935372`; review eval IDs currently end at 7. Existing seeds use complete paired snapshots, ordinary prompts, required assertions and sibling grader-only oracles. Preserve these seeds and the staging/grading contracts. Use Python standard-library fixtures with synthetic state, persisted JSON and deterministic retry outcomes; no service, deployment or dependency installation is needed.

**Instruction loading:** all eight installed detection rules loaded. Planned `.py` files activate `python`; fixture adjacency to `review-code/SKILL.md` activates `skill-md`. Loaded Python core idiom/type/error guidance (no async constructs planned) and universal/provider/kk implement guidance (provider directories and canonical paths satisfy both conditionals). The repository's bounded-routing convention takes precedence over older absolute wording. Test guidance includes Python testing and validator protocols; `skill-md` has no test-phase index. Verification and isolated review remain pending.

**Superseding completion — 2026-10-09:** four final scenario directories (review IDs 8–11) now provide R2, R4 and both R9 variants, with 24 required assertions, complete paired snapshots and separate oracles. [Verification](verification/task9/README.md) records eight passing snapshot suites (18 tests), eight deterministic reproduction groups, exact staged diffs and 51 unchanged frozen seed files. All ten shell suites pass (644 helper assertions), Go/graph checks pass, and 785 generated files remain stable after repeated generation. Corrected attempts and final logs are retained; no fixture actor run or behavioral acceptance is claimed.

**Review:** [independent source review](verification/task9/review.md) approved Task 9 after tightening R2's verdict/remedy assertions and verifier path/encoding handling. The initial P2 finding is resolved. Native PAL feedback and zero/one-file embedding limits remain disclosed; they do not establish corroboration. No systemic P0/P1 findings or new project conventions require indexing.

**Deferred acceptance — owner: implementing agent, Task 12:** after Task 2 gate 2B and Tasks 10–11, freeze these new fixture/rubric hashes and run both standard and actual isolated baseline/candidate comparisons with fresh inputs, twice per required pair. Grade sealed traces under the selected evidence contract; every required candidate assertion must pass twice. Authoring, staging and source review do not waive missing captures or failed/partial grades. Task 10 is next; the feature remains in progress.

## Task 10: Author compatibility, uncertainty and degraded-report controls

- **Status:** done
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 9, Task 11
- **Docs:** [R8 replay](evaluation.md#r8-controlled-report-phase-replay), [fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [x] 10.1 Add R5 clean partial feature, R6 inherited defect and R7 missing evidence controls → verify: no invented blockers; verdict assertions distinguish material from out-of-scope Unknown evidence.
- [x] 10.2 Add two R8 report-phase checkpoint variants with labeled synthetic PAL outcomes → verify: zero-source success and external failure both retain independent findings and expose limits without claiming live MCP validation.
- [x] 10.3 Reuse final R1/R3 seed directories and validate all review fixtures → verify: R3 history is discoverable only through the intended baseline trace; no re-authored seed invalidates the baseline silently.

### Execution context — 2026-10-10

**Accepted scope:** the user's request for the next task selects Task 10 only. Add R5/R6/R7 and two R8 report-phase replay directories; preserve all frozen seeds. Task 2 gate 2B and Tasks 11–13 remain open. The replay inputs are explicitly synthetic reporting checkpoints, not live reviewer/transport evidence.

**Before edits:** clean base `4c91bc9e`; review eval IDs end at 11. All eight installed profile detection rules were read. Planned Python fixtures/verifier activate `python`; eval adjacency to `review-code/SKILL.md` activates `skill-md`. Python core implement/test guidance and universal/provider/kk implement guidance are loaded. Provider directories and canonical paths satisfy the skill conditionals; no async constructs are planned. The repository's bounded-routing convention takes precedence over older absolute wording. Knowledge searches found the existing staging-isolation convention; no new dependencies are planned. Verification and independent review are pending.

**Superseding completion — 2026-10-10:** five final scenario directories (IDs 12–16) provide R5/R6/R7 and both R8 variants with **29 required assertions** and sibling grader-only oracles. [Verification](verification/task10/README.md) records six passing snapshot suites (18 tests), eight reproduction groups, all 16 review worktrees validated, R3's historical-only provider and 51 unchanged frozen seed files. R8 inputs differ only in the synthetic PAL result; patch applicability and the fixed independent finding are checked. All ten shell suites pass (644 helper assertions), Go/graph checks pass, and 851 generated files remain stable across repeated generation. Failed attempts and corrected checks are retained. No actor run or behavioral acceptance is claimed.

**Review:** [independent source review](verification/task10/review.md) returned APPROVE after correcting the summary count from 27 to 29; no fixture assertion changed. PAL returned no actionable findings but reported zero embedded files, so its source coverage remains unverified and is not corroboration. No systemic P0/P1 findings or new project conventions require indexing.

**Deferred acceptance — owner: implementing agent, Task 12:** after gate 2B and Task 11, freeze these fixtures/rubric and run the required fresh baseline/candidate comparisons twice, including both R8 report-phase replays and separate actual PAL smoke coverage. Grade sealed evidence; every required candidate assertion must pass twice. Preserve earlier recapture obligations and failures/partial results. Task 11 is next; the feature remains in progress and Task 13 retains final documentation/verification.

## Task 11: Author implementation completion and proportionality controls

- **Status:** done
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 9, Task 10
- **Docs:** [Fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [x] 11.1 Add I3 trivial-change and I4 resume/completion/spec-integrity fixtures; reuse I1/I2 → verify: meaningful tool-order and resulting-file assertions, no irrelevant release gate or silent spec rewrite.
- [x] 11.2 Validate fixture files, required assertions and composite result identities → verify: new IDs are unique; the pre-existing duplicate ID 4 is tolerated via (skill, eval name, assertion ID) without renumbering history.
- [x] 11.3 Regenerate fixture output and check structure/links → verify: assertions/oracles never enter acting-session workspaces.

### Execution context — 2026-10-10

**Accepted scope:** after committing Task 10, the user requested Task 11. Add I3 standalone trivial-document correction and I4 plan-mode resume/verification fixtures only, reusing I1/I2 unchanged. Task 2 gate 2B and Tasks 12–13 remain open; no actor acceptance run is authorized by fixture authoring alone.

**Before edits:** clean base `4bd5c532`. Existing implement IDs end at 9, with the documented duplicate 4 in two legacy directories. All eight installed detection rules were read; Python fixture/verifier filenames activate `python` and implement/SKILL.md adjacency activates `skill-md`. Previously loaded Python core implement/test and universal/provider/kk guidance applies; provider directories and canonical paths satisfy both skill conditionals. No async constructs or dependencies are planned. Knowledge searches confirm actor staging must be outside any SKILL.md ancestor. The proposed resume fixture uses a read-only code/test request so stale completion claims cannot be masked by changing the implementation; its independent external activation prerequisite remains explicitly permitted by the supplied design. Verification and independent review are pending.

**Superseding completion — 2026-10-10:** two final scenario directories (implement IDs 10–11) provide I3 and I4 with **15 required assertions** and sibling grader-only oracles. [Verification](verification/task11/README.md) records three passing existing specimen tests, probes for the exact typo correction and legacy/mixed-record failure, all 12 implementation fixtures staged as clean repositories, and 51 unchanged frozen seed files. Composite identity checks preserve the legacy duplicate ID 4 across 73 implement assertions and 175 combined implement/review assertions. All ten shell suites pass (644 helper assertions), Go/graph checks pass, and 871 generated files remain identical across repeated generation. No actor workflow run or behavioral grade is claimed.

**Review:** [independent source review](verification/task11/review.md) returned APPROVE with no findings. PAL returned no actionable findings but zero embedded files; its coverage is unverified and its broad readiness claims are not adopted. No systemic P0/P1 findings or new project conventions require indexing.

**Deferred acceptance — owner: implementing agent, Task 12:** after gate 2B, freeze final fixtures/rubric and run the declared fresh baseline/candidate comparisons twice. Grade actual instruction/tool events and resulting task/spec files; every required candidate assertion must pass twice. Keep I4's hard requirement, stale observations and permitted external prerequisite distinct, and preserve all earlier recapture obligations. Gate 2B is the remaining prerequisite before Task 12; Task 13 retains final documentation/verification and the feature remains in progress.

## Task 12: Execute and assess the full comparison matrix

- **Status:** in-progress
- **Depends on:** Task 2 gate 2B, Task 9, Task 10, Task 11 (all complete)
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Matrix execution](implementation.md#matrix-execution), [acceptance](evaluation.md#comparison-identity-and-acceptance)

### Subtasks

- [x] 12.1 Run all declared case/mode pairs using two fresh baseline and candidate sessions per pair → verify: identical fixtures/rubric/model configuration, filtered revision-bound actor bundles, fresh writable state and identical initial knowledge seeds with the declared unavailable-vault policy. The user-expanded scope covers both providers fully: [192 completed sessions](verification/task12/opus55/README.md).
- [ ] 12.2 Run R8 phase replays, real PAL integration smoke and legacy routing/pre-write controls → verify: replay success is not reported as transport coverage and missing integration remains explicit. R8 complete; live PAL user-deferred; legacy actor controls unrun.
- [ ] 12.3 Grade sealed execution packages, including R3 history, R3/R7 verdicts and I4 resulting task/spec state → verify: every required candidate assertion passes twice under the selected versioned contract; contrary or missing evidence cannot pass, and any receipt/use fallback explicitly leaves exact prompt content unverified. All 192 packages are graded; required acceptance remains unmet.
- [x] 12.4 Retain failures, fixes and unrun gates with owner/reason/next action → verify: baseline comparisons are not cherry-picked and no statistical reliability or untested-provider parity is claimed. See [the latest matrix record](verification/task12/opus55/README.md) and [historical stop record](verification/task12/README.md); retained observations do not complete the other gates.

### Execution context — 2026-10-10

**Authority:** the user requested the next task through /kk:implement after gate 2B closed. Task 12 is selected; Task 13 remains pending. Preserve baseline `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`, all earlier evidence and the revision-2 receipt/use limits. Candidate 1 is committed source `4fb1941779f6b24dbed4440c288f1d901f0c4609`.

**Before execution:** installed Claude 2.1.272, Codex 0.162.1, Capy 0.16.8, controller Python 3.12.11 and actor-test Python 3.10.12 differ from the original macOS batch. Declare fresh matching pairs in [the Task 12 run contract](verification/task12/run-contract.md); do not pool historical runs with this configuration. Python controller paths activate `python`; core guidance is loaded, with async guidance conservatively loaded before controller inspection. Any operative skill correction also requires `skill-md` guidance, which is loaded. No new dependency or actor model substitution is planned. New artifacts remain controller-only. Required runtime binding, measurement, grading and review are pending.

**Accepted temporary exception:** after the standalone PAL launcher failed with missing API configuration, the user instructed “ignore pal-based verification for now.” Defer PAL-dependent receipt/use, corroboration and live-integration verification; continue other verification. Owner: implementing agent when PAL verification resumes. Next action: restore the declared launcher's API configuration, validate startup, then rerun affected baseline/candidate pairs and grade the deferred components. Verification condition: actual PAL receipt/use and integration evidence under matching configuration. Preserve original assertion results; this exception does not turn missing PAL evidence into PASS or claim full two-reviewer acceptance. The named independent reviewer and all other behavioral obligations remain in scope.

**Execution result:** 42 measured Claude captures and their isolated grades are retained in [the Task 12 record](verification/task12/README.md). The latest candidate's R1–R6 standard runs have 57 PASS / 19 FAIL; no case passes every required assertion twice. Mandatory ordering, lifecycle coverage and proportionate recommendations still fail. Earlier candidate results remain visible; two candidate-1 isolated runs are invalid for acceptance because they shared temporary evidence paths. The user exception also defers R8 PAL-report replays. No Task 12 Codex, legacy actor-control or full latest-source isolated/implementation matrix is claimed.

**Stopped on repeated verification failure:** /kk:implement requires stopping when “Verification fails repeatedly.” No further actors were launched after candidate 4. A workflow redesign or explicit continuation decision is pending. Source amendments and generated counterparts remain an unaccepted draft. Static checks pass (ten shell suites, Go tests, graph validation, generation freshness and twelve controller tests), while the final independent controller review retains three open subprocess/finalization findings. Owner: implementing agent. Before resuming, resolve the behavioral approach and runner findings, freeze any successor source, then rerun affected comparisons and complete material-access audits. Task 12 remains in-progress and Task 13 pending; no acceptance threshold is waived.

### Accepted focused rework — continuation after commit 87a26bb7

The user accepted the recommendation to fix the runner, structurally simplify
instruction preparation, preserve substantive requirements, classify failure
types, then validate R1/R3/R5 before expanding. PAL remains deferred. This
explicit continuation supersedes the stop above for the bounded work below.

- [x] 12.5 Add successor owned-capture and probe-finalization helpers, preserving
  frozen controllers → verify offline preparation/runtime/interruption/cleanup
  failures and obtain independent review before model launches.
- [x] 12.6 Implement consolidated instruction preparation and contract-driven
  scenario reporting; remove conflicting speculative-suggestion cues → verify
  packet integrity/path boundaries, source review and generated parity.
- [ ] 12.7 Freeze a twelve-run diagnostic R1/R3/R5 standard comparison, including
  fresh baseline pairs under the successor capture configuration → verify each
  candidate assertion twice using the unchanged rubric, classify failures, and
  expand only after this checkpoint passes.

All eight installed profile rules were read before investigation. Python and
skill-md activate; their core implement/test guidance and both provider/plugin
conditionals are loaded, with Python async guidance conservatively included.
Neither profile contributes design guidance. No package dependency or model
change is planned. New runtime helpers use Python 3.12's existing standard
library; signal/subprocess semantics were checked against versioned docs.

**Source/runner checkpoint:** [the rework record](verification/task12/rework/README.md)
retains approved independent helper/driver and packet-source reviews. All eleven
shell suites, Go/graph checks, twelve historical controller tests, nine packet
tests and eighteen successor/evidence tests pass; 902 generated files remain
stable. Candidate `be1a283cf872ec97fe569c9fd481bbe623cc8214` and its final successor
capture freeze are declared before binding in [candidate 5](verification/task12/candidate5/run-contract.md).
The earlier unmeasured preflight freeze/source remain retained. Both binding
probes now pass: candidate packet Reads return all six parts and fifteen source
bodies exactly; parent/child model and bundle identity match. The reported alias
discrepancy is an expected symlink, verified against actual bytes.

**Diagnostic completed; gate failed:** [candidate-5 results](verification/task12/candidate5/results.md)
retain all twelve fresh captures and eighty independent assertion grades.
Candidate: **37 PASS / 3 FAIL**; baseline: **20 PASS / 18 FAIL / 2 PARTIAL**.
R1 and R3 pass every assertion twice. R5 repetition 1 reads task requirements
before checklist completion (12.1); both R5 repetitions propose an unnecessary
flag-import change while acknowledging current correctness (12.4). No assertion
or threshold changed. All source/packet hashes and file-tool paths were checked,
all 67 shell requests inspected, and nineteen proven-owned packet directories
removed with sealed contents retained. No evaluator access or PAL call was observed.

**Continuation checkpoint:** 12.7's captures, grading and audits are complete,
but its acceptance condition remains unmet. No wider matrix or further candidate
iteration was started. Owner: implementing agent, Task 12. A next bounded
follow-up must address early requirements reading and clean-review Next Steps
offering unsupported work, then rerun affected comparisons under a new source
identity. Preserve the current improvements and failed observations. Task 12
remains in-progress, Task 13 pending, and PAL remains user-deferred.

### Accepted R5-only follow-up — after commit 17344213

The user agreed to a narrow R5 follow-up and requested that the preceding work
be committed first. Commit `17344213` preserves candidate 5 and its failures;
the follow-up edits begin afterward. This supersedes the prior stop only for
the bounded R5 work. PAL remains deferred.

- [ ] 12.8 Separate early Git-diff selection from task-scope investigation and
  close clean reviews without a remediation menu or invented follow-up work
  → verify: source review, generated parity and two fresh R5-standard candidate
  PASSes against matching fresh baseline repetitions under the unchanged rubric.

The observed causes are a mandatory Next Steps menu even when no issue exists,
and an early phase named scope that can be confused with reading task scope.
The correction makes closure conditional on actual findings/required evidence,
preserves conditional verdicts for unmet hard requirements, and places task
document inspection after checklist completion. The shared scope note is
explicitly code-review-specific; /kk:review-spec retains its payload and scope
semantics. No fixture, assertion, grader, model or runner changes are planned.

All eight detection rules were evaluated; skill-md activates through SKILL.md
and sibling adjacency. Its universal/provider/kk guidance is loaded; there are
no new dependencies. Reuse the complete feature context and reviewed runner,
freeze a separately identified candidate, and run only R5 in this follow-up.

**Premeasurement verification:** independent source review approves the follow-up
with no findings. All eleven shell suites, Go/graph checks and generation
freshness pass (902 generated files). Candidate
`ab7daa7f2833abefc64dedc08e8e44790ce5a0ee` is frozen under
[the candidate-6 declaration](verification/task12/candidate6/run-contract.md).
Its binding probe returned all six complete packets containing fifteen original
instruction sources, with matching parent/child model and bundle identity.
The unchanged runner completed all four fresh R5-standard comparisons.

**Follow-up completed; gate failed:** [candidate-6 results](verification/task12/candidate6/results.md)
retain all four captures and twenty-four independent assertion grades. Candidate:
**11 PASS / 1 FAIL**; baseline: **4 PASS / 6 FAIL / 2 PARTIAL**. Both candidates
avoid unnecessary recommendations and approve the scoped increment. Repetition 1
still reads the full diff/config before checklist completion (12.1); repetition 2
passes all six assertions. No threshold or assertion changed.

Integrity and access audits pass within the captured evidence: subjects/bundles
unchanged, complete packet bytes verified, all 22 shell requests inspected, and
seven proven-owned packet directories removed with sealed evidence retained.
No evaluator-material access or PAL call was observed. Source/generated parity
remains intact. The new follow-up remains uncommitted after `17344213`.

**Continuation checkpoint:** 12.8's execution, grading and audits are complete,
but its two-run acceptance condition remains unmet. Stop here under /kk:implement's
repeated-verification-failure rule; no broader matrix or further candidate was
started. Owner: implementing agent, Task 12. Retain the clean-closure improvement
and define a separate approach to establish instruction completion before source
access. This follow-up is proposed, not implemented. Task 12 remains in-progress,
Task 13 pending, and PAL user-deferred.

### Scoped ordering proposal — after candidate 6

The user answered “yes” to scoping a separate ordering fix. This authorizes the
documentation below; it does not claim a successful guard, amend acceptance,
or start another candidate batch. [The proposal](ordering.md) retains the
clean-closure change and recommends a bounded feasibility experiment before any
production hook integration. Historical 12.7/12.8 results remain unchanged.

- [x] 12.9 Scope a mechanism for instruction completion before source access
  → verify: [ordering.md](ordering.md) ties the proposal to candidate-6 events,
  evaluates alternatives, identifies runtime uncertainties, defines a bounded
  GO / NO-GO experiment and preserves the original acceptance requirements.
- [ ] 12.10 Prove or reject the proposed guard's runtime feasibility
  → verify: complete [the bounded slice](ordering.md#bounded-feasibility-slice)
  with a frozen probe contract, offline receipt/state controls, at most two
  fresh top-level sessions per provider, sealed actual tool events and an
  independent evidence review. Missing activation, receipt, denial, ordering or
  lifetime evidence is NO-GO, not an invitation to weaken the gate.

**12.10 planning metadata:** Status pending, conditional; size M; strategy Risk-First;
depends on 12.9, selection after 12.11's severity/cost assessment, and design review;
cannot run in parallel with another source or runtime-policy change. The
implementing agent owns it if selected for execution; it is not the default next task.
Candidate-6 source/evidence remain uncommitted; no additional commit is made by
this scope revision.

All eight installed detection rules were consulted. Existing skill artifacts
activate skill-md; the prospective Python probe/helper activates Python. Neither
has installed design-phase guidance. Current official hook documentation and
existing repository hooks establish research targets, not pinned-runtime proof.
Capy supplied no existing receipt-enforcement decision. No operative code, hook,
profile, fixture, grader, generated artifact or permission was changed in this
scoping turn. Independent design review and all probe execution remain pending.

Scoping verification: all 115 local links/anchors across the four documents
resolve, `git diff --check` passes, and canonical plugin bytes still match the
frozen candidate-6 source. No behavioral test result is added by these checks.

### Authorized full matrix rerun — Opus 5.5, 2026-10-11

The user requested the complete functional matrix on both Claude and Codex,
all applicable modes, twice per baseline/candidate, and explicitly retained the
PAL deferral. This supersedes the earlier narrow diagnostic/probe scope and
authorizes measurement without actor changes. The user upgraded Claude Code to
2.1.296 after 2.1.272 rejected Opus 5.5. Preserve that failed probe and all prior
captures. Baseline remains c2d28c9e; candidate is immutable 581dd0e1.

[The new run contract](verification/task12/opus55/run-contract.md) declares
192 fresh core sessions, unchanged fixtures/assertions/revision-2 grading, and
separate R8 synthetic replays. PAL-dependent acceptance stays incomplete.
[Runner review](verification/task12/opus55/review.md) approves the controller after
two cleanup fixes; offline regressions and all ten fresh
[grader controls](verification/task12/opus55/calibration.md) pass. Both providers
and sides pass binding. [The completed execution record](verification/task12/opus55/README.md)
retains **192/192 captures and independent grades**, with no unrun core cells or
measured transport/finalization failures. No actor instructions, fixtures or
assertion thresholds changed during this comparison.

**Final results:** Claude baseline **189 PASS / 114 FAIL / 1 PARTIAL**, candidate
**251 / 49 / 4**; Codex baseline **203 / 96 / 5**, candidate **264 / 30 / 10**.
Each side/provider has 304 assertion observations. Candidate passes every
required assertion twice in **9/24 Claude** and **7/24 Codex** combinations.
R5 standard and both synthetic R8 replays pass twice on both providers; R6
inherited-defect coverage/follow-up remains a gap, alongside other ordering,
reporting and evidence failures. Required PAL omissions remain visible.

**Integrity and cleanup:** [the final audit](verification/task12/opus55/audit.md#final-batch-audit)
verifies every capture, actor bundle, runtime configuration, Git reference and
grading package. All 1,216 required assertion observations are present exactly
once per run; grader/rubric pins are unchanged. No evaluator access was observed
in the targeted traces. All temporary evaluation registrations and caches were
removed. Original review fixtures remain unchanged; report-only additions and
four evidence-based grading corrections are retained transparently.

Owner: implementing agent. **The requested rerun is complete; Task 12 acceptance
remains in-progress and Task 13 pending.** Any behavioral fix or evidence-contract
amendment needs a separately identified comparison with fresh affected pairs.
Live PAL remains user-deferred; legacy actor controls and final feature
verification remain separate gates. No statistical reliability or broader
provider parity is claimed.

### Severity and instruction-cost assessment — Task 12.11

The user requested a durable handoff and emphasized that additional instructions
for minor issues can make the skills worse overall. [The handoff](follow-up.md)
records the evidence, assessment criteria and provisional investigation inventory.
This supersedes the earlier recommendation to proceed directly to guard task
12.10. It changes sequencing, not historical grades or acceptance requirements.

- [x] 12.11 Assess remaining issues and select a proportionate next step
  → verify: every remaining candidate FAIL/PARTIAL is accounted for in a linked
  disposition record, separating behavioral impact, report omissions, evidence
  gaps and PAL deferral. Each proposed fix explains its smallest useful scope,
  instruction/workflow cost and regression checks. Record fix, investigate,
  defer or no change with reasons and acceptance consequences; select at most
  one bounded next implementation task. Minor issues may justify small contained
  corrections without materially added load. No operative edit or model run is
  required to complete this assessment.

**12.11 planning metadata:** Status done; size M; strategy Risk-First;
depends on the completed Opus 5.5 matrix and this user constraint; cannot run in
parallel with source, rubric or runtime-policy changes. Owner: implementing agent.
Assessment entry was `/kk:implement task 12.11 of functional-review`. Preserve existing
word budgets; avoid adding this assessment as a runtime skill protocol. Deferral
leaves required acceptance open, with an owner and revisit trigger.

### Task 12.11 execution context — 2026-10-11

**Authority and scope:** the user requested proceeding with Task 12.11. Assess
the retained matrix, record every remaining candidate observation and choose at
most one bounded next task. Preserve the user constraint against added instruction
burden and the explicit live-PAL deferral. No operative edit, actor run, grading
change, permission change or evidence archiving is part of this task.

**Observed:** the [dated assessment](follow-up.md#assessment--2026-10-11) and
[observation ledger](assessment-observations.md) account for all 608 candidate
grades: 515 PASS, 79 FAIL and 14 PARTIAL. Each non-PASS has its original grade,
matching baseline and one or more dispositions. Forty-four include PAL absence;
composite local/evidence gaps remain separately identified. Root-cause hypotheses
are distinguished from denied requests, missing receipts and observed omissions.

**Selected:** Task 12.12's entry-path correction is the smallest proposed
intervention in the evidence-acquisition failures. It does not promise to fix
implementation-mode acquisition or all review failures. Unsupported compatibility
claims retain higher-impact investigation priority; other bounded corrections
and evidence decisions have owners, revisit triggers and verification conditions
in the assessment. Task 12.10's guard remains deferred. No acceptance is waived.

**Instructions and checks:** /kk:implement plan mode, all eight installed profile
detection rules and the shared protocols were loaded before assessment edits.
The target files are repository planning Markdown outside any skill root; no
profile activates, and no dependency changes. /kk:test and isolated code-review
instructions are loaded for accounting/link verification and independent review.
Verification reconciles all 608 candidate rows, all 93 unique non-PASS identities
and matching baseline verdicts, and all 11 overlapping group totals. All 480
local links/anchors across the six changed documents resolve; `git diff --check`
passes. Canonical/generated files, fixtures, grades and capture contracts are
unchanged, so no regeneration or behavioral rerun is warranted for this
documentation-only task.

**Independent review and completion:** the [isolated code-review checkpoint](reviews/task12-11-assessment.md)
returns **APPROVE scoped to Task 12.11**, with no P0–P3 findings. The reviewer
independently reconciled all 608 candidate and 608 baseline grade rows and the
93-row ledger, inspected decisive sealed traces and verified scope/cost limits.
Its initial missing-methodology request was resolved from the unchanged canonical
plugin root before investigation. PAL remains deferred; no external corroboration
or behavioral acceptance is claimed. No new project convention or review finding
requires indexing. **Task 12.11 is complete; Task 12.12 remains pending.** Task 12
acceptance and Task 13 retain their open status. Final link verification includes
the retained review record: 484 local links/anchors across seven documents pass,
along with the task-status boundary check and `git diff --check`.

### Task 12.12: Resolve isolated-review instructions at entry

- **Status:** done; bounded diagnostic accepted, broader feature acceptance remains open
- **Depends on:** Task 12.11
- **Size:** S for the source correction; targeted measurement is separately bounded below
- **Strategy:** Risk-First
- **Owner:** implementing agent
- **Can run in parallel with:** —; serialize source, runtime-policy and rubric changes
- **Docs:** [acquisition evidence](follow-up.md#acquisition), [scope/cost limits](follow-up.md#selected-scope-and-verification-limits)

Replace the ambiguous skill/workflow reference in
`klaude-plugin/commands/review-code/isolated.md` with explicit plugin-root paths
to the existing `review-code/SKILL.md` and `review-isolated.md`, preserving the
current invocation, arguments, selector and instruction-before-investigation
sequence. Use the repository's plugin-load substitution convention. This is an
entry-location correction, not a new shell-denial recovery mechanism. Check the
actual generated distribution before asserting a Codex effect; command wrappers
are not currently mirrored as standalone Codex skills.

- [x] 12.12.1 Load applicable profile instructions, make only the entry-path
  replacement and regenerate → verify: no new phase, mandatory call, state,
  dependency or permission; at most 30 added authored words; common instruction
  bytes and their 800/1,200-word budgets preserved. Do not edit actors to name
  fixture defects or add fallback/retry prose. If this bound cannot address the
  observed entry ambiguity, record no change and return to assessment.
- [x] 12.12.2 Independently review the source change and verify path resolution,
  plugin structure/graph and generation freshness → verify: installed command
  loading resolves the intended files from the selected bundle, without global
  discovery; the existing direct-read and instruction-loading requirements remain.
  Reuse existing checks rather than adding text-presence tests for the wording.
- [x] 12.12.3 Freeze a new candidate and matching comparison declaration, then
  run Claude R3-isolated plus R5-isolated and R9-recovery-isolated controls,
  two fresh runs per immutable baseline/candidate (**12 sessions**) → verify:
  unchanged fixtures, prompts, rubric and declared permission policy; actual
  instruction receipt before investigation, selected diff and historical source
  acquisition, named-reviewer receipt/use, and supported final conclusions.
  Preserve live-PAL deferral and independently grade every original assertion.
  If generated operative Codex bytes change, include the same Codex pairs under
  their own matching declaration; otherwise record unchanged bytes and no new
  Codex behavioral claim. Runtime/policy changes require a revised declaration
  and fresh matched pairs, not silent substitution.
- [x] 12.12.4 Record the bounded experiment's disposition → verify: both R3
  candidates establish all non-PAL components (including local historical
  receipt/use); R5 retains clean scoped approval, R9 retains necessary recovery,
  and both controls retain instruction ordering/coverage. Reject or revert if
  entry discovery/early stopping persists, required non-PAL target components
  fail, controls regress or the cost bound is exceeded. Retain failed attempts;
  do not begin another iteration automatically. Composite PAL failures remain
  FAIL even when their local components improve. A useful diagnostic result
  completes only this slice, not Task 12 acceptance or the remaining dispositions.

### Task 12.12 execution context — 2026-10-11

The user authorized Task 12.12 and required the assessment to be committed first;
`c84fc0f7` preserves it. The command now identifies the existing skill/workflow
through explicit plugin-root paths, adding two words. Common methodology stays
unchanged at 573/1,147 words. Both generation passes leave all 902 generated files
byte-identical, so this command-only slice requires no new Codex measurements.

All eight installed detection rules were evaluated. The command/planning files
activate no profile; the new bounded capture adapter/tests activate Python.
Core implement/test and all four review checklists are loaded, with no async
conditional. /kk:dependency-handling checked path substitution against official
documentation after Context7 lacked the exact runtime version. Existing capture
APIs and transport are reused; no dependency or actor permission changed.

The [comparison contract](verification/task12/entry-path/run-contract.md) and
[temporary candidate provenance](verification/task12/entry-path/source-provenance.json)
declare the selected 12 Claude isolated sessions, plus separate loading probes,
and retain PAL deferral. Repository suites, graph/Go checks, 19 existing capture
regressions, three adapter controls and fresh Capy state-isolation checks pass.
Independent source review, actual command-path loading and measured outcomes
remain pending; static checks establish no behavioral improvement.

**Source checkpoint and runtime observation:** [independent review](verification/task12/entry-path/review.md)
approved the source/adapter with no findings. The initial candidate loading probe
completed and retained the substituted command and intended instruction reads,
but PAL unexpectedly connected under the unchanged launcher. No PAL tool call
occurred and no measured workflow started. Preserve the initial freeze/probe;
[the runtime-change record](verification/task12/entry-path/runtime-change.md)
explains why it cannot establish continuing PAL unavailability.

**Required successor configuration:** [the revised declaration](verification/task12/entry-path-no-pal/run-contract.md)
keeps the same candidate and all grading obligations but explicitly excludes PAL
from the launched run-local MCP configuration on both sides. Original controller
bytes/configuration and evidence remain retained. Four successor adapter controls
pass; independent review and fresh binding under this configuration precede all
twelve measurements. This enforces the existing user deferral without changing
normal user settings, ordinary prompts or the actor's tool permission policy.

**Successor ready for measurement:** [independent review](verification/task12/entry-path-no-pal/review.md)
approved the configuration successor. Its separately frozen baseline/candidate
probes both pass [the binding audit](verification/task12/entry-path-no-pal/binding-audit.json):
Capy connected, PAL absent, Opus 5.5 for both parent/child, complete returned
instruction content, selected-root identities and unchanged subjects. Candidate
command delivery includes both substituted paths directly. Measured results
remain pending; these loading observations do not establish functional improvement.

**Completed comparison; keep decision:** [all twelve captures and independent grades](verification/task12/entry-path-no-pal/README.md)
are complete under the successor declaration, with no measured transport failures.
Baseline: **20 PASS / 20 FAIL / 0 PARTIAL**; candidate: **32 PASS / 8 FAIL / 0
PARTIAL**. Both candidate repetitions meet all non-PAL diagnostic conditions for
R3, R5 and R9-recovery, including the local receipt/use components of the composite
failures. All eight candidate FAILs retain the required absent-PAL component.
**Keep the two-word entry-path correction.** This does not waive full-feature
acceptance or establish broader provider/mode reliability.

[The integrity audit](verification/task12/entry-path-no-pal/audit.json) verifies
582 capture files, 1,835 grading files, all 80 assertion identities, frozen inputs,
bundles, runtime configurations, Git refs and unchanged subjects. All 534 tool
requests and 93 shell requests were inspected. One baseline globally listed
external instruction filenames; no evaluator file-content read was observed,
and OS confinement is not claimed. [Cleanup](verification/task12/entry-path-no-pal/cleanup.json)
retains and verifies contents before removing 21 proven-owned directories and
six newly created files; a denied write's pre-existing destination stays untouched.
Exact source archives and runtime inputs are retained for future release archiving.
[Final independent review](verification/task12/entry-path-no-pal/completion-review.md)
approves the completion record and bounded keep decision with no findings. It
independently reconciled all grade rows/counts and inspected selected sealed
receipts, runtime records and cleanup provenance. All documentation links and
`git diff --check` pass; no source or grading change followed the review.
**Task 12.12 is complete.** Task 12 acceptance, PAL, remaining dispositions,
legacy controls and Task 13 stay open. No additional operative slice or actor
iteration is selected; R7 unsupported-claim investigation retains next priority.

### Task 12.13: Keep compatibility and release conclusions within their evidence

- **Status:** done — rejected experiment; R7 correction remains open
- **Depends on:** Task 12.12 (done), user-approved brainstorm outcome (2026-10-13)
- **Size:** S for operative wording; 48-session comparison under the existing contract
- **Owner:** implementing agent
- **Disposition:** reject and revert the candidate; R7 remains unresolved
- **Docs:** [R7 disposition](follow-up.md#unsupported-compatibility-claims), [slice](implementation.md#r7-conclusion-consistency--task-1213), [results](verification/task12/r7-conclusions/results.md)

The user selected Unknown plus a concrete next check until missing compatibility
evidence is supplied and assessed. The candidate replaced three existing common
method passages, preserving the intended treatment of known prerequisites and
scoped code approval without adding a checklist, report section or workflow phase.

- [x] 12.13.1 Replace Supported, Unknown-verdict and closing reconciliation wording; regenerate Codex → candidate was 1,175/1,200 words; shared context stayed 573/800. The failed candidate is now reverted; source archive and patch remain.
- [x] 12.13.2 Run repository checks and independent source/controller reviews → generation/structure, Go tests, graph validation, 19 capture regressions and four adapter controls pass; reviews have no current source finding.
- [x] 12.13.3 Freeze, bind and capture R7/R3/R5 in both modes/providers, twice per baseline/candidate → all four loading probes and all 48 fresh sessions complete; real Capy state isolation and grader calibration pass.
- [x] 12.13.4 Independently grade, audit and record keep/reject disposition → 336 assertion rows and integrity/cleanup audits complete; independent completion review approves the rejection record.

#### Outcome — 2026-10-13

[The frozen contract](verification/task12/r7-conclusions/run-contract.md) required
both R7 candidate repetitions in every provider/mode to meet 14.1–14.6. Both
Claude standard repetitions still fail 14.3/14.4: unsupported provider claims and
conditional deployment approval survive the new wording. **Reject.** All Codex
and Claude isolated R7 candidates meet those local rows, but that does not satisfy
the cross-provider criterion. R5's candidate non-PAL rows pass. Codex candidate
R3 isolated repetition 1 identifies the incompatibility but omits explicit
Blocked classification from the parent report (7.7 FAIL); baseline reports also
omit it, so no incremental regression is established.

Effective candidate totals are **147 PASS / 21 FAIL / 0 PARTIAL**; baseline totals
are **95 PASS / 72 FAIL / 1 PARTIAL**. Sixteen candidate failures are required PAL
omissions, four are Claude R7 target failures, and one is the R3 reporting gap.
[Two independent grader corrections](verification/task12/r7-conclusions/grade-corrections/README.md)
fix grading-display truncation errors; original grades and sealed captures remain
unchanged. Exact Codex prompts remain unverified and the existing receipt/use
exception is not expanded. A pre-feature baseline and two repetitions do not
isolate incremental causality or establish reliability.

The canonical and generated operative files match starting
`cc07a614a999e8f35e2f408a505546077154031f`; the prior Task 12.12 correction stays.
[The rejected patch](verification/task12/r7-conclusions/candidate-method.patch)
and candidate `bf873de63369662ebe3b0cde4226dbda1c16104b` remain archived.
[Integrity checks](verification/task12/r7-conclusions/integrity-audit.json)
verify frozen inputs, all 48 bundles, subjects/Git refs, 2,001 capture files,
5,350 grading files and every assertion identity. [Access inspection](verification/task12/r7-conclusions/access-audit.json)
covers 1,782 tool/lifecycle records, including 914 shell requests; no evaluator
content read is observed, without claiming OS-wide confinement.
[Cleanup](verification/task12/r7-conclusions/cleanup.json) preserves temporary
evidence before removing proven-owned paths; temporary plugin/trust entries are
absent. Exact runtime inputs and source archives are retained.

The initial external loading command was rejected before launch by automatic
approval review. The user then explicitly authorized the synthetic fixture and
filtered-instruction transfer to authenticated Claude/Codex for probes and all
48 sessions, with PAL excluded. That block was resolved before execution. The
[verification record](verification/task12/r7-conclusions/README.md) retains the
prospective declaration, source/runtime changes, original and corrected freeze,
binding receipts, grades and local check limitations.

No successor wording or actor iteration is selected. R7, Task 12 acceptance,
other assigned dispositions, live PAL, legacy controls and Task 13 remain open.

[Independent completion review](verification/task12/r7-conclusions/completion-review.md)
approves this experiment's completion/rejection record with no current findings;
it independently reconciles every assertion and both corrections, while attributing
execution/hash verification to the root. [Final workspace cleanup](verification/task12/r7-conclusions/workspace-cleanup.json)
rechecks all archived runtime inputs and final subject snapshots before removing
the 52 proven-owned actor workspaces. **Task 12.13 is complete as a rejected
experiment, not an accepted R7 fix.**

### Task 12.14: Redesign the R7 evaluation before further skill changes

- **Status:** done — diagnostic complete; 23 PASS / 1 FAIL retained; no operative skill change
- **Depends on:** Task 12.13 (done); user-requested reassessment documented 2026-10-13
- **Size:** M
- **Strategy:** Risk-First — establish test validity before changing shared instructions
- **Owner:** next implementing agent
- **Can run in parallel with:** —
- **Docs:** [handoff and rationale](follow-up.md#r7-evaluation-redesign--next-session), [implementation scope](implementation.md#r7-evaluation-validity--task-1214), [prospective contract](evaluation.md#planned-r7-validity-reassessment)

The immediate deliverable is a revised fixture pair and grading criteria, with
acceptable/unacceptable report examples. The whitespace example does not establish
a real provider incompatibility. Preserve all historical results; assess whether
their significance warrants a skill change instead of optimizing for old labels.

- [x] 12.14.1 Audit `klaude-plugin/skills/review-code/evals/functional-missing-baseline/eval.json`, its sibling `oracle/`, and the Task 12.13 failed/passing reports → verify: distinguish demonstrated report claims, hypothetical server semantics, missing evidence and ambiguous review scope; identify exactly what the successor should measure.
- [x] 12.14.2 Design separately identified material-dependency and benign-control cases, with meaningful expected outcomes → verify: the unknown deployment fact matters in the first, scoped approval is justified in the second, and neither requires live access, fixture-specific actor hints or a large system.
- [x] 12.14.3 Author the successor fixtures/rubric and pre-run acceptable/unacceptable examples; document assertion mapping and any proposed verdict-contract amendment in `evaluation.md` → verify: historical files/grades stay unchanged, oracles remain grader-only, and report meaning rather than isolated approval keywords decides the revised criteria. Regenerate Codex output if canonical eval files are added.
- [x] 12.14.4 Review fixture/rubric validity before measurement, then declare and run the bounded diagnostic: two Claude standard sessions per case, four total, on the same unchanged current skill revision → verify: fresh staged workspaces outside a SKILL.md ancestor, pinned inputs/runtime, no evaluator material exposed, independent grading and retained attempts. No new skill candidate or 48-run comparison.
- [x] 12.14.5 Record whether a concrete skill failure survives the clearer test and choose investigate/defer/no-change accordingly → verify: distinguish evaluation validity from skill effectiveness, preserve PAL/capture limits and full-feature gates, and document any broader comparison separately before executing it.

The fixture/rubric work, four-session diagnostic and final independent evidence
review are complete. No additional operative instruction change is selected.

#### Execution context — 2026-10-14

The user requested implementation of Task 12.14. The starting worktree is clean
at `6bc277ea`; the existing Task 12.13 evidence and operative instruction bytes
remain unchanged. Scope is the revised fixture pair, explicit grading examples,
premeasurement independent review and four fresh Claude standard sessions on the
same current skill revision. PAL remains user-deferred; Task 12 acceptance and
Task 13 are separate open gates.

All eight installed profile detection rules were loaded before investigation.
Planned Python fixtures/controller activate `python`; canonical eval files
activate `skill-md` through their nearest `review-code/SKILL.md` ancestor.
Python core and universal/provider/kk implementation guidance are loaded.
Existing staging-isolation knowledge was consulted. No operative instruction
change or new package dependency was introduced.

**Observed result:** [Task 12.14 verification](verification/task12/r7-validity/README.md)
retains separately identified evals 19/R7M and 20/R7B, prospective examples/rubric,
independent premeasurement validity/source reviews, frozen source/runtime inputs,
binding/state probes, all four fresh Claude standard captures and independent
grades. All target compatibility conclusions pass twice: material target readiness
stays Unknown; benign code receives justified scoped approval. Totals are
**23 PASS / 1 FAIL / 0 PARTIAL**. R7M repetition 1's 19.2 remains FAIL because its
report omits the explicit PUT /settings endpoint from the behavior trace.

**Disposition:** no further operative skill change for the R7 compatibility concern.
The retained report-completeness omission does not demonstrate material overconfidence
or justify added instruction burden. This is not a full diagnostic pass, proof that
old R7 is invalid, or replacement of its historical acceptance requirement. Owner:
implementing agent; revisit the omission if it obscures a material consequence,
under a separately declared comparison. Task 12 acceptance, live PAL, other assigned
dispositions, legacy controls and Task 13 remain open.

**Checks:** 27 fixture/host-runtime checks and all four supplied snapshot suites
(10 fixture tests) pass; all 11 shell suites (645 assertions), Go tests, graph
validation and repeated-generation freshness (926 files) pass. The initial
inherited Linux helper failed five Darwin cleanup checks before any actor ran;
the independently reviewed controller-only correction passed before capture.
No operative instructions, prior evals, historical captures/grades or persistent
user settings changed. Exact runtime/packet inputs are archived and hash-verified.
Recorded owned scratch copies are intentionally retained until Task 13 housekeeping;
durable evidence does not depend on them.

**Completion review:** the independent code-reviewer approves the completed
diagnostic and no-change disposition, with the 19.2 failure and broader gates
unchanged. Its one P3 calibration-path metadata finding was corrected and
independently rechecked; no open in-scope source finding remains. See the
[completion review](verification/task12/r7-validity/completion-review.md).
**Task 12.14 is done.** This does not close Task 12 acceptance or Task 13.

### Next-session handoff — remaining Task 12 issues

The user requested a durable record of the 2026-10-14 discussion explaining what
still fails and how Task 12.14's evaluation-validity approach could apply. See
[the concrete failures, evidence and recommendations](follow-up.md#remaining-issues-for-the-next-session).
Owner: implementing agent when work resumes. The recommendation is to reassess
R6's dormant-defect and report-detail expectations while separately investigating
unfinished implementation verification after command denial. Missing capture,
the I4 read-order violation and user-deferred PAL coverage retain distinct
dispositions and verification conditions.

The next useful deliverable is an evidence-backed assessment with pre-run examples
and a bounded proposed next task. No Task 12.15, operative change, revised assertion,
model run or acceptance waiver is selected by this documentation request.
Task 12.14 stays done; Task 12 acceptance and Task 13 stay open.

**Selected on 2026-10-17:** the user subsequently requested the next priority.
Task 12.15 below selects the R6 assessment only; the preceding paragraph records
the earlier documentation-only boundary.

### Task 12.15: Assess R6 evaluation validity and review scope

- **Status:** done — assessment complete; no operative change or actor measurement
- **Depends on:** Task 12.14 (done)
- **Owner:** implementing agent
- **Size:** S
- **Docs:** [R6 assessment and successor proposal](r6-assessment.md)
- **Scope:** the user's 2026-10-17 request to do the next priority selects the R6
  assessment from the remaining-issues handoff. Produce an evidence-backed
  assessment and one bounded proposed next task. Other report-detail cases and
  unfinished implementation verification retain their existing owners.

- [x] 12.15.1 Inspect the original R6 prompt, snapshots, assertions/oracle and matched reports/grades → verify: distinguish discovery, attribution, reachability, follow-up and acquisition failures.
- [x] 12.15.2 Establish the practical consequence and write acceptable/unacceptable report examples → verify: scoped approval, inherited advisories and introduced exposure have distinct meanings without prescribing exact wording.
- [x] 12.15.3 Propose an affected-path case and dormant control, with an explicit old-to-proposed assertion mapping → verify: the proposal preserves original fixtures/grades and identifies any prospective requirement change before measurement.
- [x] 12.15.4 Record a bounded next task and disposition, verify the documentation and obtain independent review → verify: no operative patch, actor batch, regrading or acceptance waiver is implied by this assessment.

#### Execution context — 2026-10-17

Started from clean `6093213a` on `feat/functional_review`. All eight installed
profile detection rules were read; repository planning Markdown has no matching
file signals or `SKILL.md` ancestor, so no implement/test profile content applies.
Relevant knowledge searches and the current design, implementation, evaluation
contract and task handoff are loaded. The authorized output is a repository-local
R6 assessment with tracking updates. Live PAL remains user-deferred. Task 12
acceptance, Task 13 and the original R7 disposition stay unchanged.

**Outcome:** the [assessment](r6-assessment.md) separates missed dormant discovery
from correct PR approval, conditional advisory follow-up, and acquisition/capture
failures. It proposes R6M/R6D cases and an explicit old-to-proposed mapping, with
report examples written before measurement. Optional discovery in the dormant
successor is a proposed coverage change, not a waiver of original 13.3/13.4.
No broader skill instruction is selected. The bounded next proposal is fixture
and rubric authoring plus independent validity review; it is not automatically
selected or measured by completing this task.

**Verification:** original snapshot suites pass 3/3 each; read-only probes confirm
the inherited failure and unchanged checked-in reachability. All 1,738 hashes
across 16 historical R6 packages verify, and current candidate snapshot/oracle
bytes match captured inputs. Local Markdown links and whitespace checks pass.
[Independent completion review](reviews/r6-assessment-review.md) approves with
no findings; test/hash/link results remain parent-attributed. PAL remains deferred.
Only planning documents changed, so regeneration and full runtime suites are
not applicable. Historical grades were not recomputed; Task 12 acceptance and
Task 13 remain open.

**Reflection:** a single composite failure can represent a discovery miss, a
useful but incomplete advisory, or missing evidence. Separating those meanings
supports a smaller next experiment without pretending the original gate passed.

### Task 12.16: Author and review R6 material-exposure and dormant-control evaluations

- **Status:** done — fixtures/rubric reviewed; actor measurement remains unrun
- **Depends on:** Task 12.15 (done)
- **Owner:** implementing agent
- **Size:** M
- **Docs:** [assessment](r6-assessment.md#bounded-next-task-and-completion-boundary), [authoring/verification record](verification/task12/r6-validity/README.md), [rubric](verification/task12/r6-validity/rubric.md)
- **Authority:** on 2026-10-17 the user accepted the proposed next step: author and
  independently review the two fixtures and grading criteria, verify them locally,
  and review the optional-discovery rule explicitly. Actor measurements and
  operative skill changes are outside this task.

- [x] 12.16.1 Author separately identified R6M/R6D evals with complete before/after snapshots and grader-only oracles → verify: a real changed default exposes the inherited failure in R6M; the label-only R6D change preserves reachability and allows scoped approval.
- [x] 12.16.2 Write prospective criteria, evidence mapping and positive/negative report examples → verify: discovery, attribution, reachability, verdict and follow-up are distinct; optional dormant discovery applies only to the new control and no old grade changes.
- [x] 12.16.3 Verify snapshot behavior, declared file lists, staging isolation and generated parity → verify: supplied tests pass while a separate boundary probe demonstrates the intended failure; no evaluator material enters staged actor inputs.
- [x] 12.16.4 Obtain independent fixture/rubric and source review, resolve findings and record the disposition → verify: reviewed authoring completes this task without claiming diagnostic or full-feature acceptance.

#### Execution context — 2026-10-17

Started at `6093213a` with the four uncommitted Task 12.15 planning files preserved.
The next available review eval IDs are 21 and 22. Python activates for fixture
and verification `.py` files; skill-md activates for eval assets through the
review-code skill ancestor. Python core implement/test guidance and skill-md
universal/provider/kk implement guidance are loaded; provider directories and
canonical paths satisfy the skill-md conditionals. No async constructs or new
package dependencies are planned. The successor control's optional discovery is
the explicit prospective scope decision for this authoring task, subject to
independent validity review; original R6 and feature acceptance remain binding.
PAL stays user-deferred, and no actor configuration or measurement is selected.

**Outcome:** evals 21/R6M and 22/R6D and their generated counterparts provide the
material default-exposure case and dormant label-only control. The rubric includes
separate evidence mappings and pre-run examples; conditional absence is recorded
without claiming exercised discovery or follow-up. The explicit optional-discovery
scope decision applies only to R6D. [Independent review](verification/task12/r6-validity/review.md)
approves source and evaluation validity with no findings. No operative instruction
or original fixture/assertion/grade changed.

**Verification:** six controller tests pass, including 16 supplied snapshot tests,
32 scenario outcomes and real staging isolation. Generation is stable across 958
files; structure, Go tests and graph validation pass. Eleven shell suites pass
686 assertions without skips. The twelfth has a pre-existing hook-fixture mismatch,
reproduced with unchanged committed inputs and durably assigned with its next
action in the [verification record](verification/task12/r6-validity/README.md#environment-attempts-and-unrelated-test-follow-up).
The initial protected-path generation failure and Python/TOML environment failures
are recorded with their successful recovery. No full-repository-green claim is made.

**Completion boundary:** Task 12.16 is done. A future diagnostic needs empirical
grading calibration, a frozen declaration and fresh isolated inputs; no batch is
selected automatically. Original R6 acceptance, R7 disposition, PAL, legacy actor
controls, other remaining investigations and Task 13 stay open as previously assigned.

**Reflection:** giving detailed output a real consumer and a per-call override
makes the exposure/control distinction explicit without changing operative review
instructions. Keeping conditional trigger observations separate avoids mistaking
an unexercised advisory path for successful follow-up.

### Task 12.17: Measure the bounded R6 diagnostic

- **Status:** done — eight captures/grades complete; diagnostic failures retained
- **Depends on:** Task 12.16 (done)
- **Owner:** implementing agent
- **Authority:** user approved the proposed eight-session diagnostic on 2026-10-17:
  R6M/R6D × Claude/Codex standard review × two fresh repetitions, after grader
  calibration and input freezing. Independent grading and accurate trigger
  accounting are required; no operative patch or broader batch is selected.
- **Docs:** [rubric](verification/task12/r6-validity/rubric.md), [diagnostic record](verification/task12/r6-validity/diagnostic/README.md), [results](verification/task12/r6-validity/diagnostic/results.json)

- [x] 12.17.1 Calibrate the pinned independent grader on ordering, report meaning and conditional-trigger controls → verify: expected PASS/FAIL/PARTIAL results and present/absent/unobservable conditions match without exposing expected answers.
- [x] 12.17.2 Review the capture adapter, declare/freeze source, fixtures, rubric, grader and runtime; prove binding and state isolation → verify: unchanged HEAD instructions, filtered bundles and fresh per-run state; actual selected runtime and configuration are recorded.
- [x] 12.17.3 Prepare all eight inputs, capture serially, seal and audit every attempt → verify: ordinary prompts, no evaluator leakage, no reuse/overwrite or automatic iteration; capture errors remain explicit.
- [x] 12.17.4 Independently grade all sealed packages, record trigger coverage and disposition, obtain completion review → verify: no unexercised conditional pass is evidence of follow-up capability; no original acceptance or PAL waiver.

#### Execution context — 2026-10-17

Existing uncommitted Task 12.15/12.16 files are preserved. Operative source remains
`6093213a2710708d90b43733ac024da6779bc32b`; new eval assets are excluded from actor
bundles. This is an unchanged-instruction diagnostic, not a baseline/candidate
comparison. Installed versions observed: Claude Code 2.1.296, Codex 0.163.0,
Capy 0.17.3; controller/actor Python will be the installed 3.12.11. Python and
skill-md guidance from the preceding task remains loaded; new controller files
activate Python, while existing eval additions still activate skill-md. No async
constructs or new dependency is introduced. The historical transports are reused
through a successor adapter; no historical controller or evidence is edited.
PAL stays excluded. The unrelated hook-fixture failure retains its existing owner.

**Outcome:** all eight declared sessions completed without retry and received
independent grades: **58 PASS / 10 FAIL / 0 PARTIAL** across 68 assertions. Every
scoped verdict is correct. All four material cases find/attribute the new exposure
and propose bounded corrections. All four dormant reports surface the inherited
defect but omit a separate next action (22.6 FAIL). Codex additionally omits required
path-report details in all four runs (21.2/22.2) and checked-in reachability context
in both dormant reports (22.4). These are ten failed assertion observations, not
ten independent bugs. No absent dormant trigger supplies a pass; all four are
present. Eight isolated-dispatch conditions are absent in standard mode and give
no isolated/PAL coverage. The full diagnostic pass condition is unmet.

**Verification/review:** 33 calibration judgments match; six new controller,
18 inherited runtime and six matrix tests pass. Both binding and both state probes
pass. All capture seals, 700 grading-file hashes and 75 archived runtime files
verify; frozen inputs and subjects remain unchanged. Temporary Codex registration
and trust entries are gone. [Independent completion review](verification/task12/r6-validity/diagnostic/completion-review.md)
approves with no findings; it reconciles reports/grades/manifests while attributing
execution/hash checks to the parent. The unrelated hook-test failure remains
assigned, with no full-repository-green claim.

**Disposition:** no broader discovery rule or operative patch. The
[diagnostic follow-up](verification/task12/r6-validity/diagnostic/README.md#disposition-and-concrete-follow-up)
assigns bounded advisory-closure investigation and defers extra trace prose pending
demonstrated practical value; both retain concrete next actions and verification
conditions. No further batch is automatically selected. Original R6/R7 acceptance,
unfinished implementation verification, PAL, legacy actor controls and Task 13
remain open. Task 12.17 completion records the experiment, not feature acceptance.

**Reflection:** the clearer fixture pair produces the correct change-attribution
and scope decisions, while advisory actionability still fails in both providers.
Separating these from report-detail omissions makes the next investigation smaller
without relabeling failed required rows or treating two repetitions as reliability.

### Task 12.18: Assess and prepare a bounded advisory-closure correction

- **Status:** done — candidate preparation only; behavioral comparison/adoption unrun
- **Depends on:** Task 12.17 (done)
- **Owner:** implementing agent
- **Authority:** on 2026-10-17 the user selected the first proposed next step:
  assess a small closure-rule replacement, review it before measurement, and
  preserve clean approvals and required corrective advice.
- **Scope:** source-backed assessment, a minimal candidate in the standard and
  isolated closing rules, generated parity, local checks and independent review.
  This task does not select or launch another actor batch or establish adoption.
- **Docs:** [assessment and comparison proposal](advisory-closure.md)

- [x] 12.18.1 Reconcile the four missing follow-ups with existing closure and reporting guidance → verify: distinguish a plausible instruction ambiguity from established causation; preserve correct verdicts and historical failures.
- [x] 12.18.2 Prepare the smallest justified replacement in both closing branches → verify: surfaced substantiated inherited defects receive a bounded separate action; clean reviews, in-scope corrections, required evidence and review-only authorization retain their contracts.
- [x] 12.18.3 Regenerate Codex output and run relevant local checks → verify: generated parity, instruction packaging and links; no static-check result is reported as behavioral improvement.
- [x] 12.18.4 Obtain independent source review and record a prospective comparison/disposition → verify: explicit advisory-trigger coverage, negative controls, providers/modes and unchanged acceptance boundaries; any adoption decision remains dependent on measurement.

#### Execution context — 2026-10-17

Starting revision is `11b2c6efb0638605bb6acd3eb184edb9abd10f56`, with a clean
worktree. Four R6D final reports describe the inherited failure and omit a next
action, despite appropriate scoped approval. Current closure branches use
"actionable findings" and "no changes are recommended" without explicitly
addressing an inherited issue reported outside Findings. That is a plausible
ambiguity, not an isolated cause. The common method already requires a correction
for behavioral findings; avoid adding another report section or broad audit rule.

All eight installed profile detection rules were loaded. `skill-md` activates
through the nearest `review-code/SKILL.md` for both target procedure files;
universal, Claude Code and kk-plugin implement/review guidance is loaded. The
provider directories and canonical paths satisfy both conditional predicates.
No dependency, profile, description or workflow-order change is needed. PAL
remains user-deferred. Measurement, original acceptance and Task 13 remain open.

**Outcome:** the two closure replacements and generated copies are prepared;
canonical growth is 19 words in standard review and 37 in isolated review.
The [assessment](advisory-closure.md) records source evidence, meaning-based
examples, rejected alternatives and a prospective 64-session comparison covering
R6D/R6M/R5/R9 recovery across both providers and modes. This is not a selected or
frozen batch, and no actor was launched or historical grade changed.

**Verification/review:** generation, all Go tests, graph validation and nine packet
tests pass; second generation preserves 958 file hashes. Eleven of twelve shell
suites pass; the unchanged, previously assigned Codex hook-fixture mismatch remains
open. Initial sandbox-only generation/cache failures passed on permitted retries.
[Independent source review](reviews/advisory-closure-review.md) approves candidate
preparation with no findings, attributing execution checks to the parent. Local
links and whitespace checks pass. No new conventions or systemic findings need
indexing.

**Reflection and boundary:** the observed actionability gap survives appropriate
scoped approval and correct attribution. The candidate
connects an already surfaced issue to a separate action at closure. Whether that
wording improves behavior is still unknown. The implementing agent owns the next
concrete declaration and measurement under the assessment's controls; adoption,
PAL, original acceptance and Task 13 remain open.

### Task 12.19: Freeze the closure candidate and review its comparison contract

- **Status:** done — reviewed source/criteria freeze; no actor execution
- **Depends on:** Task 12.18 (done)
- **Size:** S
- **Can run in parallel with:** —
- **Owner:** implementing agent
- **Authority:** on 2026-10-17 the user selected the first next step: freeze the
  candidate and write an independently reviewed run contract with explicit
  keep/reject criteria. Actor execution and adoption are not selected.
- **Docs:** [run contract](verification/task12/advisory-closure/run-contract.md)

- [x] 12.19.1 Preserve the exact reviewed operative candidate and immutable baseline → verify: archived source and filtered-bundle identities, only the four expected closure files differ from the parent, and no branch/index/cache registration changes.
- [x] 12.19.2 Pin the 64-session matrix, fixtures, ordinary prompts, grading inputs and runtime declaration → verify: same inputs per side, explicit conditional-trigger evidence and separate prelaunch calibration/binding gates.
- [x] 12.19.3 Define keep/reject/inconclusive criteria and obtain independent contract review → verify: target follow-up and negative controls cannot pass on absent evidence; original required grades, PAL deferral and broader acceptance remain intact.
- [x] 12.19.4 Seal and locally verify the preparation artifacts, then record the outcome → verify: hashes, recoverable archives, generated parity and no actor execution; launch readiness is not claimed before the remaining gates run.

#### Execution context — 2026-10-17

The Task 12.18 changes remain uncommitted and are preserved. Freeze a temporary
source snapshot from `11b2c6efb0638605bb6acd3eb184edb9abd10f56` plus only the four
reviewed canonical/generated closure files, without committing the working branch.
Installed version probes report Claude Code 2.1.296, Codex 0.163.0, Capy 0.17.3
and the existing Python 3.12.11 interpreter. A new launch adapter and fresh
calibration/binding results are separate prelaunch obligations; no previous result
substitutes for them. PAL stays excluded under the existing user deferral.

Profile detection reuses the eight loaded rules. Existing operative changes
activate `skill-md`; declaration files outside skill roots do not. Python guidance
is loaded for any necessary preparation helper, with no async constructs planned.
Use the existing offline bundle builder; no dependency or operative edit is needed.

**Outcome:** [preparation record](verification/task12/advisory-closure/README.md)
retains candidate `4b69421465131e2e9e497f200ec9ddbdb439ac83`, baseline source and
filtered actor archives, 159 evaluation-input files, 17 existing controller files,
all 64 ordinary prompts/jobs and 464 original assertion rows. Only the four
reviewed closure files differ from the parent; working HEAD and staged content
are unchanged. No runtime registration or actor/calibration/binding call occurred.

**Review:** independent design review resolved one P2 ambiguity by explicitly
mapping 22.4's required components and sole tolerated reporting omission. Missing
trigger detail means REJECT; truncated evidence is PARTIAL; original whole-row
grades remain intact. Final design assessment is SOUND; independent preparation
source review is APPROVE with no findings. PAL remains deferred. Both reviews
attribute archive/hash execution to the parent.

**Verification:** all six archives recover with matching path/byte/mode/link and
exclusion manifests; a tampered instruction is rejected. Source delta, generated
closure parity, matrix, prompts and local links pass. The final preparation seal
checksums 27 files including `freeze.json`; its SHA-256 is
`2850e0416ef0277109849e206e11851f10d92fdcfd6954d8ecf5d68127e95bea`.
No unchanged full-repository suite was rerun; Task 12.18's known hook-fixture issue
retains its assignment. Preparation attempts and their corrections are recorded.

**Reflection and next action:** explicit component mapping prevents an omission
exception from accidentally permitting other missing evidence. The implementing
agent owns the successor adapter/review, execution freeze, fresh calibration,
four binding probes, two state probes and preflight attestation before measurement
when that work is selected. This preparation freeze is not launch readiness,
adoption, a change to historical grades or completion of broader acceptance.

### Task 12.20: Prepare the execution adapter and run fresh calibration

- **Status:** done — adapter/freeze/calibration only; binding/measurement unrun
- **Depends on:** Task 12.19 (done)
- **Size:** M
- **Owner:** implementing agent
- **Can run in parallel with:** —
- **Authority:** on 2026-10-17 the user requested execution-adapter preparation,
  independent review/freezing and fresh calibration. Binding/state probes and the
  64 measured actor sessions remain unselected.
- **Docs:** [frozen contract](verification/task12/advisory-closure/run-contract.md)

- [x] 12.20.1 Implement a successor adapter using the frozen source/criteria and existing transports → verify: exact matrix/prompt identity, per-case rubric routing, fresh inputs, refusal of overwrite/reuse and preflight gates.
- [x] 12.20.2 Verify offline controls and obtain independent source review before freezing → verify: frozen-input drift, preparation/capture failure and interruption cannot silently pass; historical files and preparation seal remain unchanged.
- [x] 12.20.3 Freeze execution dependencies and calibration inputs, then dispatch fresh independent graders → verify: five ordering and eight semantic controls plus the declared disposition cases match their controller-only expected results, with expected-verdict tables excluded from every permitted grader packet.
- [x] 12.20.4 Retain dispatches, verbatim returns, comparison results and independent completion review → verify: calibration success is not actor effectiveness or completed binding/preflight; any mismatch stays visible and unresolved until reviewed.

#### Execution context — 2026-10-17

Task 12.19's preparation freeze remains authoritative, SHA-256
`2850e0416ef0277109849e206e11851f10d92fdcfd6954d8ecf5d68127e95bea`.
Create execution artifacts in a separate `verification/task12/advisory-closure-execution/`
directory. Restore controller/fixture/source inputs from the checked archives;
do not modify historical controllers or use an installed plugin as the candidate.
Python activates for the new adapter/tests; core implement/test and all review
checklists are loaded. No async constructs or new dependency are planned.
Existing skill-md guidance remains loaded for the retained candidate changes.
PAL remains deferred. Only independent calibration graders may be launched here.

**Outcome:** the [execution record](verification/task12/advisory-closure-execution/README.md)
retains the successor adapter and execution freeze
`edc9cc7798bc3b2f7759a0c707db26abe2ead848bf51b6ec9de8535497a5dd85`.
All 25 fresh calibration controls matched: 69 assertion verdicts and 11 explicit
trigger values. Returned totals are 32 PASS / 35 FAIL / 2 PARTIAL, matching the
deliberate negative/missing-evidence controls. No calibration attempt was retried.
No binding/state probe, measured actor, PAL call or runtime registration occurred.

**Review and checks:** independent source review approved after correcting exact
dispatch validation, frozen-expectation verification and mandatory Plugin Root
delivery. Calibration review resolved one P1 inconsistency in absent-advisory
controls before freeze, retaining unchanged expected outcomes. Final validity is
SOUND; [completion review](verification/task12/advisory-closure-execution/review/completion-review.md)
approves with no findings. Twenty-one new offline tests, 19 inherited runtime
tests and six matrix tests pass. Parent verification checks the 26 preparation
files, five execution dependencies and 203 calibration inputs against their hashes;
standalone reconciliation/verification pass. Initial packets and superseded
requests remain retained. The whole repository suite was not rerun; its existing
unrelated hook-fixture issue retains its assignment.

**Evidence limits and next action:** public role settings, exact submitted
requests, returned task identities and verdict tables are retained; internal
service-model telemetry and per-grader raw read histories are unavailable. Expected
answers were excluded from supplied packet manifests; no OS-confinement claim is
made. The implementing agent owns four binding probes, two independent state
probes and reviewed preflight before measured execution when selected. Calibration
does not establish candidate improvement, adoption or broader acceptance.

**Reflection:** independent pre-freeze review caught controls that accidentally
tested two failure causes and dispatch metadata that could not substantiate the
declared setup. The corrected controls isolate the intended decisions, and the
result checks now tie every observation to frozen inputs and a distinct request.

## Task 13: Document and verify the complete feature

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#documentation-and-final-verification)

### Subtasks

- [ ] 13.1 Use /kk:document to update README.md, docs/user-guide/skills.md and docs/contributing/testing.md → verify: behavior, evidence limits, fixture staging and grading contracts are accurately described.
- [ ] 13.2 Run /kk:test over all test/test-*.sh suites, make plugin-graph and go test ./... → verify: structural/plumbing checks pass with environment failures explicitly reported.
- [ ] 13.3 Run make generate-kodex and confirm a second generation introduces no drift → verify: canonical/generated parity including agent definitions.
- [ ] 13.4 Reconcile matrix evidence and shared-consumer checks → verify: all required declared coverage passes; /kk:review-spec and /kk:review-design retain their contracts.
- [ ] 13.5 Run /kk:review-code with actual profiles and /kk:review-spec against design.md, implementation.md, evaluation.md and tasks.md → verify: findings are resolved or durably assigned without waiving required acceptance.
- [ ] 13.6 Record feature verification completion after 13.1–13.5 and required acceptance are verified → verify: no unresolved hard constraint, unrun gate or unreviewed requirement change is represented as complete. Track release housekeeping in 13.7 separately; Task 13 remains open until both are complete.
- [ ] 13.7 **Human-executed, AI-guided:** retain the compact verification record and reusable tooling, archive the full evidence as assets of the GitHub release containing this feature, then remove the archived evidence from the repository and its history → verify: follow the retention plan below; the human confirms archive retrieval/integrity, retained-content checks and history cleanup before closing this subtask.

### 13.7 Evidence retention and release archive

**Owner:** human maintainer; AI supplies the inventory, proposed keep/archive
mapping, command guidance and verification interpretation. The human executes
archiving/upload, repository removal, history rewriting, reflog expiry and garbage
collection. A later /kk:implement session must not execute these actions
automatically.

**Sequencing:** prepare after 13.1–13.6 and the final evidence are complete.
Use the GitHub release that includes the feature as the archive destination;
record its actual tag and URL when known. This is release housekeeping, not a
new behavioral acceptance gate: feature verification can finish before the
release exists, while 13.7 and Task 13 remain explicitly open. Verify the uploaded
archive before removing repository evidence or purging history.

| Keep in Git | Required content and disposition |
| --- | --- |
| Compact verification record outside `verification/` | Create `verification-summary.md` at the feature-document root, retained when the feature moves to `docs/feat/done/`. Include final baseline/candidate results for both providers and modes, two-run coverage, material failures/regressions, evidence limits, acceptance disposition, accepted exceptions and unresolved follow-up. Preserve the lessons from failed iterations without copying their transcripts. |
| Small result and provenance records | Retain a compact per-case/mode/repetition/assertion result table, in Markdown or JSON, linked by the summary. Record original source, fixture and grader identities; model/runtime/permission configuration; rubric/evidence-contract version and amendments. Record the release URL, asset names, archive SHA-256, manifest and archive-member paths needed to retrieve supporting evidence. Existing detailed grades may be consolidated; their originals remain in the archive. |
| Durable design and regression assets | Keep feature design/implementation/task decisions and any still-relevant follow-up. Keep canonical eval definitions, fixtures, oracles, harness documentation and regression tests under `klaude-plugin/`, with their generated counterparts; these are maintained test assets, not disposable captures. |
| Reusable execution tooling and tests | Extract the minimal runnable set into a repository tooling location such as `scripts/functional-review-evals/`, with tests and usage instructions. Assess `verification/task12/opus55/matrix.py`, `task12/rework/`, and the capture/grading helpers under `verification/`, `task2b/` and `task8/`. Resolve their existing cross-directory imports and frozen-path assumptions before removing the old tree. Retain only helpers/dependencies needed for future runs; archive historical variants. This cleanup does not require a new general-purpose evaluation framework. |

**Archive outside Git:** package the complete retained
`docs/feat/wip/functional-review/verification/` tree, or its eventual `done/`
location, before removing it. Include all candidates and unsuccessful attempts,
raw run/protocol transcripts, initial/final workspace and actor-bundle snapshots,
copied grading inputs, detailed grades and corrections, manifests/freezes,
contracts/rubrics, binding/calibration/audit/review records, controller versions,
and startup/administrative logs. Include any exact source/fixture/grader inputs
required by the frozen contracts that are not already sealed in that tree.
The archive must remain interpretable after original Git commits are purged;
preserve original IDs and content hashes rather than relabeling old evidence
with rewritten commit IDs. Only regenerable local caches such as `__pycache__/`
may be omitted, with exclusions recorded in the manifest.

Attach a compressed archive (for example,
`functional-review-evidence-<release-tag>.tar.zst`), its SHA-256 file and an
inventory manifest to the feature's GitHub release. Keep these assets outside
the Git object database. The manifest records original relative paths, file
counts/hashes, exclusions and source provenance; the retained summary provides
the lookup instructions. Do not preserve only successful runs or rely on an
old commit URL as the archive.

**Human execution and completion checks:**

1. Finalize the keep/archive mapping and extract retained records/tooling
   → verify: future evaluation inputs and required helper imports are accounted
   for; retained tooling tests pass independently of the evidence directory.
2. Create and upload the archive, checksum and manifest; download and extract
   the uploaded copy outside the checkout → verify: its SHA-256 and manifest
   match, and representative captures, grades and pinned inputs can be located.
3. Remove the archived repository tree and repair references, including links
   from feature documents and `docs/reviews/` → verify: retained links resolve
   to the compact record or a release asset with an explicit member path;
   canonical fixtures/tests remain intact. The entire `verification/` directory
   can go once the keep list has been relocated.
4. Perform the maintainer's chosen history cleanup with `git filter-repo`,
   `git reflog expire` and `git gc --prune`, including the relevant refs and
   historical evidence paths → verify: archived evidence is absent from the
   intended retained history, kept files still exist, and the release/archive
   remains accessible after any tag/ref changes. Retain any old-to-new revision
   mapping needed to interpret the summary without modifying sealed evidence.
5. Record the actual release assets, checksums, retained destinations and human
   confirmation in the summary/task → verify: 13.7 closes only on observed
   completion, not on a proposed command sequence or a locally prepared archive.

## Dependency Graph

Revised with the user-approved sequencing decision on 2026-10-09. Gates 2A and 2B are parts of Task 2, not renumbered tasks.

~~~
Task 1 -> Task 2 gate 2A -> Task 3 -> Task 4 -> Task 5 -> Task 6 -> Task 7 -> Task 8
Task 2 gate 2A -> Task 2 gate 2B --+
Task 8 -> Task 9 ----------------+
Task 8 -> Task 10 ---------------+-> Task 12 -> Task 13
Task 8 -> Task 11 ---------------+
~~~

## Design-stage disposition

- The two supplied design reviews are consolidated and assessed in the linked disposition; revised documents have not been independently re-reviewed in this session.
- All valid design gaps are specified above. Canonical skills, grader, harness, ADR/AGENTS and generated output are implementation targets, not changes performed by this document revision.
- The pre-existing duplicate implement eval ID remains unchanged. Composite result identity resolves the immediate ambiguity; any future renumbering must update assertion IDs and references together.
