# Tasks: Functional and operational review

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Evaluation: [evaluation.md](evaluation.md)
> Review disposition: [consolidated assessment](reviews/design-review-consolidation.md)
> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: in-progress
> Created: 2026-10-07
> Revised: 2026-10-09 with user-approved separation of implementation readiness from capture completion
> Not Doing: new review skill, whole-system audits, mandatory production access, deployments, generic release engine, new models/dependencies, profile redesign
> Delivery: preserve existing invocations/shared consumers; regenerate Codex artifacts with every operative slice.

Scope and direction are approved; the reviews have been assessed and the detailed plan revised. Tasks 1, 3, 4, 5, 6 and 7 are done. Task 2 remains in progress: its implementation-readiness gate (2A) is done; its capture-completion gate (2B) remains open. Task 8 is ready to start; Tasks 8–11 follow their existing sequence without waiting for 2B. Task 12 and feature completion still depend on 2B. The [2026-10-09 run-contract amendment](verification/run-contract-2026-10-09.md) records the authorization and evidence limits. Earlier six-task numbering is superseded by this sequence; no completed work was renumbered. Size includes authored reasoning complexity; mechanical copies/symlinks/generated files are excluded. Parallel markers permit compatible work only and do not authorize delegation. Serialize generation if tasks run concurrently.

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

- **Status:** in-progress
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Tasks 3–11 (gate 2B only, after 2A)
- **Docs:** [Baseline preparation](implementation.md#baseline-preparation), [capture resolution](evaluation.md#codex-handoff-capture-resolution), [run-contract amendment](verification/run-contract-2026-10-09.md)
- **Gate 2A — implementation readiness:** done; final fixtures, frozen inputs and 16 baseline captures retained. Satisfies Task 3's prerequisite without asserting behavioral acceptance.
- **Gate 2B — capture completion:** open; four Codex baselines remain UNRUN. Owner: implementing agent. Required before Task 12 and feature completion.

### Subtasks

- [x] 2.1 Create complete final R1/R3 eval directories under review-code/evals/ and I1/I2 under implement/evals/, including eval.json and grader-only oracles → verify: later tasks reuse these exact directories and all new IDs avoid existing IDs.
- [x] 2.2 Stage seed snapshots manually in disposable repositories; create R3's released-provider history/tag → verify: the decisive old source is absent from candidate files and PR hunks but present in local Git.
- [ ] 2.3 Complete baseline captures under the evidence contract selected by 2.5–2.6, using immutable c2d28c9e and fresh workspace/knowledge state per run → verify: retain the existing 16 captures and four fresh Codex R3-isolated/I2-standalone runs (two each), plus any required baseline recaptures, with ordered events, reviewer evidence, initial/final files and bundle/state identity. Capture completion does not require baseline behavioral PASS; candidate counterparts remain Task 12 work.
- [x] 2.4 Freeze fixture hashes and the grader procedure/rubric with the captures → verify: subsequent paired runs use identical fixture bytes and any changed fixture requires both sides to rerun.
- [ ] 2.5 Conduct one bounded capture investigation under [the resolution procedure](evaluation.md#codex-handoff-capture-resolution) → verify: record a supported alternative and at most one fresh marker probe, or document that no viable alternative exists; retain the outcome and stop repeating unchanged capture paths.
- [ ] 2.6 Record the selected evidence contract before further handoff-dependent captures → verify: a successful probe retains exact-handoff assertions; otherwise version the rubric/assertion mapping for observable reviewer receipt and use, preserving the original freeze and disclosing that exact prompt content is unverified. Record regrading/recapture obligations for Tasks 8/12 and baseline recaptures for 2.3. Close 2B only after 2.3, 2.5 and 2.6 are complete.

### Execution context — 2026-10-08

Observed evidence: [Task 2 verification](verification/task2/README.md), [frozen inputs](verification/task2-frozen.json), [grading procedure](verification/task2-rubric.md), and [independent review](verification/task2/review.md). Final seeds use review IDs 6/7 and implement IDs 8/9; no fixture or rubric changed after freeze. Real before/after reproductions and local R3 release history match the declared oracle. Codex copies regenerated without drift; no operative instructions changed.

Captured 12 Claude baseline workflows (all six seed/mode pairs twice) and four Codex baselines (R1 standard/I1 plan twice), all against immutable c2d28c9e in fresh workspaces with empty run-local knowledge. Capy 0.16.8 was declared before capture and passed fresh isolation probes. Traces retain permission denials, actual dispatches/results, payload artifacts and initial/final files; capture completion is not behavioral acceptance. Three failed controller attempts remain retained. Fifteen controller tests, all nine shell suites and plugin graph checks passed; corrected capture code passed independent review.

**Capture disposition at 2026-10-08 — superseded for sequencing by the decision below.** Codex R3 isolated and I2 standalone remained **UNRUN**, two repetitions each. Public app-server history and separately trusted observation hooks omitted/encrypted submitted reviewer messages; a final claim could not satisfy exact-handoff evidence. The original contract held Task 3 until plaintext capture was established. Temporary Codex trust/hook/plugin registrations were removed. These observations did not establish behavioral acceptance.

**Capture note from Task 1 — owner: implementing agent.** Codex CLI JSON omits some child events; persisted parent/child runtime records expose them. The parent dispatch's message field is encrypted. Before any later exact-handoff assertion is captured, retain plaintext at submission or use another supported trace surface alongside the encrypted record. Task 1's role bytes/read results prove loading, not exact plaintext handoff content; ciphertext alone cannot pass that later assertion. See [completed probe evidence and limits](verification/README.md#completed-probes-after-login-refresh).

### Accepted sequencing decision — 2026-10-09

The user approved separating implementation readiness from full verification, one bounded capture investigation, and a conditional fallback to observable reviewer receipt/use if plaintext remains unavailable. Gate 2A is satisfied by the frozen fixtures and retained captures; Task 3 may start. Gate 2B remains owned by the implementing agent and blocks Task 12 and feature completion, not Tasks 3–11. The immutable baseline can be launched after candidate development without using candidate instructions.

Subtasks 2.5–2.6 own the deferred capture work because the tested Codex surfaces cannot expose the required messages. Follow the [run-contract amendment](verification/run-contract-2026-10-09.md) and record the bounded investigation's outcome before choosing the evidence path. No new probe, rubric revision, capture or behavioral grade is claimed by this documentation update. Existing captures, manifests, frozen rubric and assertions remain unchanged; a fallback requires a separately versioned contract applied to both sides. Provider coverage and the two-run candidate threshold remain required.

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

- **Status:** pending
- **Depends on:** Task 7
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Workflow-grading slice](implementation.md#workflow-grading-slice), [evidence contract](evaluation.md#execution-evidence-contract)

### Subtasks

- [ ] 8.1 Extend agents/eval-grader.md with explicit workflow mode and manifest-limited Read access → verify: the omitted/default mode preserves the legacy component contract.
- [ ] 8.2 Update review-code/evals/_harness/HARNESS.md and add implement/evals/README.md for capture, dispatch evidence, resulting-file snapshots and mode selection → verify: acting sessions never receive grading material.
- [ ] 8.3 Add and grade calibration records → verify: an early edit despite a reassuring final response is FAIL, missing events are PARTIAL, and complete correct ordering is PASS; legacy component grades stay compatible.
- [ ] 8.4 Pin the grader implementation and grade available baseline traces under the same versioned contract used for candidate traces → verify: no self-attested ordering or payload claim substitutes for execution evidence; regrade affected traces if 2.6 later selects the fallback, and leave missing captures for 2B/Task 12 rather than blocking grader implementation.
- [ ] 8.5 Regenerate the grader/playbook output and run structure/graph checks → verify: both distributions preserve the explicit mode boundary.

## Task 9: Author state, retry and intent scenarios

- **Status:** pending
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 10, Task 11
- **Docs:** [Fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [ ] 9.1 Add R2 retry/lifecycle and R4 stored-data compatibility scenarios in final review-code/evals directories → verify: each failure has a supported synthetic path and precise required assertions.
- [ ] 9.2 Add separate R9 mismatch and justified-complexity companion directories → verify: green implementation-shaped tests do not excuse a requirement mismatch, and necessary recovery behavior is preserved.
- [ ] 9.3 Validate files[], numeric IDs and oracle placement; regenerate fixture output → verify: no prompt leaks an expected finding and no duplicate minimal fixture is created.

## Task 10: Author compatibility, uncertainty and degraded-report controls

- **Status:** pending
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 9, Task 11
- **Docs:** [R8 replay](evaluation.md#r8-controlled-report-phase-replay), [fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [ ] 10.1 Add R5 clean partial feature, R6 inherited defect and R7 missing evidence controls → verify: no invented blockers; verdict assertions distinguish material from out-of-scope Unknown evidence.
- [ ] 10.2 Add two R8 report-phase checkpoint variants with labeled synthetic PAL outcomes → verify: zero-source success and external failure both retain independent findings and expose limits without claiming live MCP validation.
- [ ] 10.3 Reuse final R1/R3 seed directories and validate all review fixtures → verify: R3 history is discoverable only through the intended baseline trace; no re-authored seed invalidates the baseline silently.

## Task 11: Author implementation completion and proportionality controls

- **Status:** pending
- **Depends on:** Task 8
- **Size:** M
- **Can run in parallel with:** Task 9, Task 10
- **Docs:** [Fixture-authoring slices](implementation.md#fixture-authoring-slices)

### Subtasks

- [ ] 11.1 Add I3 trivial-change and I4 resume/completion/spec-integrity fixtures; reuse I1/I2 → verify: meaningful tool-order and resulting-file assertions, no irrelevant release gate or silent spec rewrite.
- [ ] 11.2 Validate fixture files, required assertions and composite result identities → verify: new IDs are unique; the pre-existing duplicate ID 4 is tolerated via (skill, eval name, assertion ID) without renumbering history.
- [ ] 11.3 Regenerate fixture output and check structure/links → verify: assertions/oracles never enter acting-session workspaces.

## Task 12: Execute and assess the full comparison matrix

- **Status:** pending
- **Depends on:** Task 2 gate 2B, Task 9, Task 10, Task 11
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Matrix execution](implementation.md#matrix-execution), [acceptance](evaluation.md#comparison-identity-and-acceptance)

### Subtasks

- [ ] 12.1 Run all declared primary-provider case/mode pairs and secondary representative checks using two fresh baseline and candidate sessions per pair → verify: identical fixtures/rubric/model configuration, filtered revision-bound actor bundles, fresh writable state and identical initial knowledge seeds with the declared unavailable-vault policy.
- [ ] 12.2 Run R8 phase replays, real PAL integration smoke and legacy routing/pre-write controls → verify: replay success is not reported as transport coverage and missing integration remains explicit.
- [ ] 12.3 Grade sealed execution packages, including R3 history, R3/R7 verdicts and I4 resulting task/spec state → verify: every required candidate assertion passes twice under the selected versioned contract; contrary or missing evidence cannot pass, and any receipt/use fallback explicitly leaves exact prompt content unverified.
- [ ] 12.4 Retain failures, fixes and unrun gates with owner/reason/next action → verify: baseline comparisons are not cherry-picked and no statistical reliability or untested-provider parity is claimed.

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
- [ ] 13.6 Mark completion only after all required work is verified → verify: no unresolved hard constraint, unrun gate or unreviewed requirement change is represented as complete.

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
