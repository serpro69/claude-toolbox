# Tasks: Functional and operational review

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Evaluation: [evaluation.md](evaluation.md)
> Review disposition: [consolidated assessment](reviews/design-review-consolidation.md)
> Issue: [#166](https://github.com/serpro69/claude-toolbox/issues/166)
> Status: in-progress
> Created: 2026-10-07
> Revised: 2026-10-07 after two design reviews
> Not Doing: new review skill, whole-system audits, mandatory production access, deployments, generic release engine, new models/dependencies, profile redesign
> Delivery: preserve existing invocations/shared consumers; regenerate Codex artifacts with every operative slice.

Scope and direction are approved; the reviews have been assessed and the detailed plan revised. Task 1 is done; Task 2 is in progress; later tasks remain pending. Earlier six-task numbering is superseded by this sequence; no completed work was renumbered. Size includes authored reasoning complexity; mechanical copies/symlinks/generated files are excluded. Parallel markers permit compatible work only and do not authorize delegation. Serialize generation if tasks run concurrently.

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
- **Can run in parallel with:** —
- **Docs:** [Baseline preparation](implementation.md#baseline-preparation), [fixture lifecycle](evaluation.md#fixture-lifecycle-and-staging)

### Subtasks

- [x] 2.1 Create complete final R1/R3 eval directories under review-code/evals/ and I1/I2 under implement/evals/, including eval.json and grader-only oracles → verify: later tasks reuse these exact directories and all new IDs avoid existing IDs.
- [x] 2.2 Stage seed snapshots manually in disposable repositories; create R3's released-provider history/tag → verify: the decisive old source is absent from candidate files and PR hunks but present in local Git.
- [ ] 2.3 Capture standard, isolated, plan and standalone baseline runs before operative changes, using the immutable actor revision and fresh workspace/knowledge state per run → verify: ordered tool traces, actual dispatches, initial/final relevant files, bundle identity and initial state are retained.
- [x] 2.4 Freeze fixture hashes and the grader procedure/rubric with the captures → verify: subsequent paired runs use identical fixture bytes and any changed fixture requires both sides to rerun.

### Execution context — 2026-10-08

Observed evidence: [Task 2 verification](verification/task2/README.md), [frozen inputs](verification/task2-frozen.json), [grading procedure](verification/task2-rubric.md), and [independent review](verification/task2/review.md). Final seeds use review IDs 6/7 and implement IDs 8/9; no fixture or rubric changed after freeze. Real before/after reproductions and local R3 release history match the declared oracle. Codex copies regenerated without drift; no operative instructions changed.

Captured 12 Claude baseline workflows (all six seed/mode pairs twice) and four Codex baselines (R1 standard/I1 plan twice), all against immutable c2d28c9e in fresh workspaces with empty run-local knowledge. Capy 0.16.8 was declared before capture and passed fresh isolation probes. Traces retain permission denials, actual dispatches/results, payload artifacts and initial/final files; capture completion is not behavioral acceptance. Three failed controller attempts remain retained. Fifteen controller tests, all nine shell suites and plugin graph checks passed; corrected capture code passed independent review.

**Open capture gate — owner: implementing agent.** Codex R3 isolated and I2 standalone remain **UNRUN**, two repetitions each. Public app-server history and separately trusted observation hooks both omit/encrypt submitted reviewer messages; a final claim cannot satisfy exact-handoff evidence. Establish a supported plaintext-at-submission surface in a separate probe, then capture four fresh baselines with the frozen inputs. If runtime changes, revise the contract and recapture affected comparisons. No requirement waiver, provider switch or Task 2 completion is authorized by these observations. Temporary Codex trust/hook/plugin registrations were removed. Task 3 remains pending until this gate closes.

**Capture note from Task 1 — owner: implementing agent.** Codex CLI JSON omits some child events; persisted parent/child runtime records expose them. The parent dispatch's message field is encrypted. Before any later exact-handoff assertion is captured, retain plaintext at submission or use another supported trace surface alongside the encrypted record. Task 1's role bytes/read results prove loading, not exact plaintext handoff content; ciphertext alone cannot pass that later assertion. See [completed probe evidence and limits](verification/README.md#completed-probes-after-login-refresh).

## Task 3: Align the instruction-routing convention

- **Status:** pending
- **Depends on:** Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Routing-convention slice](implementation.md#routing-convention-slice)

### Subtasks

- [ ] 3.1 Amend docs/adr/0004-skill-workflow-ordering.md with the narrowly bounded routing exception and its rationale → verify: predicate inspection is distinct from behavioral analysis and preserves instruction-before-action.
- [ ] 3.2 Update AGENTS.md ordering wording consistently → verify: approximately 16 KiB bounds, declared predicates, conservative loading when undecidable, and the prohibition on early findings/edits/tests agree with the ADR.

## Task 4: Standard review assesses behavior and compatibility

- **Status:** pending
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Standard review slice](implementation.md#standard-review-slice)

### Subtasks

- [ ] 4.1 Add _shared/change-context.md, review-code/functional-review.md and the review-code/shared-change-context.md symlink → verify: all required semantics fit the 800/1,200-word ceilings and links resolve.
- [ ] 4.2 Update review-code/SKILL.md and review-process.md for instruction loading, behavior tracing, historical evidence, coverage and verdict mapping → verify: R1 is detected through an ordinary prompt and material Unknown evidence is qualified.
- [ ] 4.3 Clarify _shared/review-scope-protocol.md → verify: current incompatibility remains reportable while genuinely pending work is excluded; /kk:review-spec's existing payload remains valid.
- [ ] 4.4 Add shared-source/symlink and word-budget assertions to test/test-plugin-structure.sh → verify: exact targets, resolution, regular-file substitution and excess wording are checked; do not register the implement link before it exists.
- [ ] 4.5 Regenerate Codex output and run structure/graph checks plus the seed standard dry-run → verify: canonical/generated parity and evidence-backed reporting; preserve actual results for later paired grading.

## Task 5: Isolated reviewers independently compare current and historical behavior

- **Status:** pending
- **Depends on:** Task 4
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Isolated review slice](implementation.md#isolated-review-slice)

### Subtasks

- [ ] 5.1 Update review-code/review-isolated.md to prepare change context and bounded historical-source bundles after instruction loading → verify: R3's old-provider blob and provenance reach both reviewers.
- [ ] 5.2 Update agents/code-reviewer.md with common-method loading and explicit additional-evidence requests → verify: the parent can supply requested local history through resume/reinvoke; unavailable evidence remains Unknown without adding shell access.
- [ ] 5.3 Introduce code-review/document-review branches in _shared/pal-codereview-invocation.md and align commands/review-code/isolated.md → verify: PAL receives the same material facts; /kk:review-design remains compatible.
- [ ] 5.4 Apply evidence-qualified reporting while preserving native findings and author annotations → verify: no quality-only fallback, unsupported corroboration or broad approval from incomplete external coverage.
- [ ] 5.5 Regenerate output, run structure/graph checks and the R3 isolated dry-run → verify: actual dispatches/read artifacts prove the historical comparison, not the parent's summary.

## Task 6: Implementation establishes constraints and hands off verified context

- **Status:** pending
- **Depends on:** Task 5
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Implementation slice](implementation.md#implementation-slice)

### Subtasks

- [ ] 6.1 Add implement/shared-change-context.md and integrate it in implement/SKILL.md → verify: both modes load the shared contract and profiles before source investigation/edits.
- [ ] 6.2 Align plan-mode.md and standalone-mode.md with the execution core → verify: one authoritative post-instruction investigation phase; existing pre-write controls remain valid.
- [ ] 6.3 Establish intended outcomes, affected contracts and delivery constraints; record observations in the current task's labeled Execution context → verify: I1 detects its conflict and observations cannot silently amend specifications.
- [ ] 6.4 Refresh evidence for independent review and separate task completion from deployment conditions → verify: real handoff uses finished Task 5 consumers, stale evidence is rejected and a hard unmet requirement stays open.
- [ ] 6.5 Extend shared-link structure assertions for implement, regenerate output and verify both modes → verify: exact link targets and budgets pass; I2 remains usable without a full feature plan.

## Task 7: Stage before/after and historical fixtures reliably

- **Status:** pending
- **Depends on:** Task 6
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Evaluation staging slice](implementation.md#evaluation-staging-slice)

### Subtasks

- [ ] 7.1 Extend review-code/evals/_harness/setup.sh for paired snapshots and optional history.json while preserving flat fixtures → verify: base/candidate diff and local release history match the fixture contract.
- [ ] 7.2 Add test/test-review-eval-staging.sh → verify: offline tests cover added/changed/deleted/unchanged and hidden files, tagged historical source, malformed pairs/history, escaping links, .git entries and destination refusal.
- [ ] 7.3 Stage the existing seed directories through the helper → verify: wrappers, eval metadata and oracle answers stay outside the actor workspace; fixture hashes remain comparable.

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
- [ ] 8.4 Pin the grader implementation and regrade retained baseline traces under the same contract used for candidate traces → verify: no self-attested ordering or payload claim substitutes for actual execution evidence.
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
- **Depends on:** Task 9, Task 10, Task 11
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Matrix execution](implementation.md#matrix-execution), [acceptance](evaluation.md#comparison-identity-and-acceptance)

### Subtasks

- [ ] 12.1 Run all declared primary-provider case/mode pairs and secondary representative checks using two fresh baseline and candidate sessions per pair → verify: identical fixtures/rubric/model configuration, filtered revision-bound actor bundles, fresh writable state and identical initial knowledge seeds with the declared unavailable-vault policy.
- [ ] 12.2 Run R8 phase replays, real PAL integration smoke and legacy routing/pre-write controls → verify: replay success is not reported as transport coverage and missing integration remains explicit.
- [ ] 12.3 Grade sealed execution packages, including R3 history, R3/R7 verdicts and I4 resulting task/spec state → verify: every required candidate assertion passes twice; contrary or missing evidence cannot pass.
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

~~~
Task 1 -> Task 2 -> Task 3 -> Task 4 -> Task 5 -> Task 6 -> Task 7 -> Task 8
Task 8 -> Task 9  --+
Task 8 -> Task 10 --+-> Task 12 -> Task 13
Task 8 -> Task 11 --+
~~~

## Design-stage disposition

- The two supplied design reviews are consolidated and assessed in the linked disposition; revised documents have not been independently re-reviewed in this session.
- All valid design gaps are specified above. Canonical skills, grader, harness, ADR/AGENTS and generated output are implementation targets, not changes performed by this document revision.
- The pre-existing duplicate implement eval ID remains unchanged. Composite result identity resolves the immediate ambiguity; any future renumbering must update assertion IDs and references together.
