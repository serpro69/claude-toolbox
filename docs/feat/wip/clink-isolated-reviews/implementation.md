# Implementation: clink fallback for isolated reviews

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: Task 0 verified against the recorded corrected PAL build; Task 1 code complete (2026-10-23); Task 2 code complete (2026-10-24); Task 2b code complete (2026-10-24); Task 3 pending

## Repository orientation

Edit canonical instructions under `klaude-plugin/`; generated files under `kodex-plugin/` and `.codex/agents/` come from `make generate-kodex`. Shared sources have bare names in `skills/_shared/` and each skill consumer gets a `shared-<name>.md` symlink. Agents refer to shared sources through resolved plugin-root paths rather than per-skill symlinks.

Follow [plugin architecture](../../../contributing/architecture.md), [testing conventions](../../../contributing/testing.md) and the repository's instruction-ordering rules. Load all common instructions and resolved profile checklists before content investigation. Plugin instructions must stand alone in a consumer repository: this feature's documentation is not a runtime dependency and must not be linked from plugin prose.

Preserve the existing API transport in `skills/_shared/pal-codereview-invocation.md`. Add shared routing and clink instructions rather than replicating the API sequence in both callers. Do not add a design-review command wrapper: no such wrapper exists at the design baseline.

## Task 0: Verify the new PAL contract

**Strategy:** Risk-First / Contract-First. This task produces verification evidence and any necessary design correction; it does not author plugin instructions.

1. Inspect the candidate PAL implementation, its new CLI-only/reliability plans and advertised tool schemas. Record commit/release, CLI versions, sanitized effective review-role configuration and actual working-directory behavior in `verification/pal-contract.md` → verify: every C1–C8 row in [the acceptance contract](design.md#task-0-acceptance-contract) has an explicit result, evidence reference and reproducible setup.
2. Exercise discovery with an API-backed reviewer available, API review omitted, no eligible API models, and failed/ambiguous discovery. Use isolated configuration and captured/stubbed responses where appropriate → verify: the three discovery states remain distinct and no secret values enter evidence.
3. Establish how discovered clients map to providers and configured review models, including duplicate clients and unknown authorship. Confirm the usable review role and whether model identity is observed or only configured → verify: a deterministic eligible roster can exclude the authoring provider without fabricated fields or CLI-name assumptions.
4. Prepare small disposable code/document fixtures, plugin-like criteria files and a candidate snapshot outside the fixture worktree. Run a live review and a context-dependent follow-up through the actual MCP path without API credentials → verify: access is demonstrated through file-only fixture content absent from the prompt or observed read events, fixture content remains unchanged, `allow_edits=false` is sent on every request without reusing a prior edit opt-in, and continuation requires no API model context. Record native permission behavior separately: an unchanged fixture demonstrates no-edit behavior for that run, not enforced read-only access. Inherited native permissions alone do not exclude a client; do not alter them.
5. Capture representative execution failures, partial read denial and output truncation/summary, including a response with no read telemetry. Deterministic runner/parser fixtures may cover destructive or impractical failure injections; identify these separately from live evidence → verify: diagnostic-only responses never count as completed reviews; unverified receipt retains useful attributed findings but establishes neither corroboration nor broad approval. C7 passes on correct classification and reporting, not on telemetry being present.
6. Exercise separate reviewer conversations and equivalent evidence. Test concurrent isolation when supported → verify: no cross-review context or result contamination; choose and record parallel or sequential scheduling for the authored protocol. A concurrency failure alone permits sequential scheduling, not skipping reviewers.
7. Resolve the required contract rows and publish the verified schema/configuration mapping and minimum PAL revision in the evidence record → verify: no C1–C8 check remains failed, skipped or unverified before Task 1 starts. C7 may pass while a review's source receipt remains unknown; missing telemetry is a recorded coverage limit, not an upstream prerequisite. Record any missing required capability with observed behavior, required behavior, owner and concrete next action; keep Task 0 blocked until that capability is resolved.

Do not run a paid/login-dependent probe silently while claiming it is a static check. Use already authorized test accounts and disposable fixtures, and follow the execution environment's approval rules. Never install CLIs, initiate login or rewrite user model configuration as a workaround. The selected providers' full live acceptance coverage must be stated; a skipped provider is not a passed contract.

Execution evidence now lives in [verification/pal-contract.md](verification/pal-contract.md), with [Linux revalidation, the resolved discovery gap and exact corrected build](verification/linux-20261023/README.md). Task 0 passed for that local candidate; the installed/released PAL must contain the correction before relying on API-mode clink discovery. Creating this plan did not satisfy Task 0. PAL plans at the design-time revision are inputs to verification, not a release pin or implementation evidence.

## Task 1: Code review with discovery-only clink selection

Deliver the full isolated code-review path and its regression evals in one slice.

Primary files:

- New `klaude-plugin/skills/_shared/external-review-invocation.md` and the `review-code/shared-external-review-invocation.md` symlink.
- `klaude-plugin/skills/review-code/review-isolated.md` and `SKILL.md`.
- `klaude-plugin/commands/review-code/isolated.md`.
- Focused scenarios under `klaude-plugin/skills/review-code/evals/`.

1. Write the shared procedure using Task 0's verified contract: discover once, select API/clink/unavailable, freeze the branch and retain per-reviewer records → verify: evaluate API-available, API-unavailable and discovery-error fixtures; no execution failure transitions to clink.
2. Define the clink roster, provider exclusion, configured-model ownership, fresh conversations, no-edit behavior, native permission limits, continuation and outcome reporting. State the verified scheduling policy once → verify: the multi-provider fixture attempts every eligible provider exactly once, excludes the authoring provider, and reports missing/unknown candidates without guessing or treating inherited native permissions as enforced read-only access.
3. Integrate selection before external dispatch in the code workflow. Load the new protocol and existing PAL protocol before investigation; retain the single post-instruction investigation entry → verify: an instruction-loading trace shows all required criteria before evidence and no duplicated full-diff entry.
4. Reuse the complete existing criteria/evidence manifest for each clink reviewer. Send the full bundle on its initial call, while preserving the existing API planning/continuation distinction → verify: changed candidate, unchanged consumer, historical provenance and all common/profile criteria appear in every intended payload; staged/range fixtures use supplied snapshots.
5. Generalize external result annotation and failure handling from one external reviewer to a roster. Preserve native external output, qualified verdicts and useful internal findings → verify: independent external reviewers can corroborate one issue; unsupported coverage and duplicate-provider results cannot inflate corroboration.
6. Update skill overview and command wording so they describe variable reviewer count and discovery-only selection consistently → verify: targeted text audit finds no operative two-reviewer-only assumption or API-error-to-clink transition in the changed code-review flow.
7. Add the code-review scenarios in the [evaluation matrix](#evaluation-matrix), regenerate Codex output and run targeted structural validation → verify: required assertions pass in recorded runs, shared links resolve, generated instructions preserve paths, and the API-success/runtime-failure regressions are explicit.

Keep the PAL API protocol behavior intact. Only adjust terminology inside it if an existing sentence directly conflicts with its new shared caller; do not refactor the API transport or its model policy incidentally.

## Task 2: Design review with the same external selection

Deliver document review through the shared selector while preserving its scope and independence.

Primary files:

- `klaude-plugin/skills/review-design/review-isolated.md` and `SKILL.md`.
- New `review-design/shared-external-review-invocation.md` symlink.
- New `klaude-plugin/skills/_shared/design-review-criteria.md`, its `review-design/shared-design-review-criteria.md` symlink, and `klaude-plugin/agents/design-reviewer.md`.
- Focused scenarios under `klaude-plugin/skills/review-design/evals/`.

1. Extract reusable checks into the shared criteria file, retaining document quality, technical soundness, feature value, task-format checks and cross-document consistency. Keep the agent's identity, tool restrictions, finding taxonomy and output format in its wrapper → verify: compare old versus extracted obligations; all checks remain reachable and output/access contracts are unchanged.
2. Make the internal agent and isolated parent load the shared criteria before evaluating documents. Explicitly load the external-selection and existing PAL protocols before subject-matter work → verify: loading trace and a dedup audit show one post-instruction investigation entry in each changed workflow.
3. Replace design's unconditional API model selection with the already implemented shared discovery procedure → verify: API availability keeps the API path, unavailable discovery selects all eligible clink providers, and runtime API failures never select clink.
4. Build a document-review payload with selected targets, relevant existing source, criteria and resolved absolute paths. State that implementation described in a proposal is planned work → verify: default all-documents scope and each explicit subset remain correct, missing requested documents are disclosed, and no excluded document becomes a review target.
5. Generalize design reporting to a roster, preserving native external findings, author-context annotation and indexing. Require relevant observable evidence for corroboration → verify: partial external failure, two external supporters, unknown receipt and all-reviewer failure produce the specified report without fabricated completion.
6. Add design scenarios from the matrix and regenerate → verify: documented invocation examples still match the existing skill entry; no new command or agent name is introduced; canonical and generated fixtures/instructions agree.

Extraction is a reuse change within this feature, not authorization to revise unrelated standard-review behavior. If the extraction cannot preserve current obligations, record and resolve that issue within this task rather than silently omitting checks.

## Evaluation matrix

Use per-scenario `eval.json`, real files under `test-files/` and any grader-only expectations under sibling `oracle/`. Select unused numeric IDs from each skill's existing catalog. Each assertion names an observable call, payload, read order or report property. Do not put expected answers inside model-visible fixtures.

There is no general built-in runner. Use the repository's scenario convention and explicit recorded runs; an existing feature-specific harness is reusable only after confirming it supports this contract. Do not add a general runner as part of this feature.

| Scenario | Skills | Required assertions |
| --- | --- | --- |
| API review available | Both | Existing two-step API flow; zero clink calls; internal reviewer retained |
| API step 1, step 2 or later continuation fails | Both | Disclose failure; preserve useful results; zero clink calls and no discovery retry to change backend |
| No eligible API review; several CLI providers | Both | Every eligible non-authoring provider attempted once; configured models preserved; fresh conversations; equivalent criteria/evidence |
| API review tool omitted, clink advertised | Both | Discovery selects clink without attempting a missing API tool |
| Discovery error or malformed/ambiguous response | Both | Error stays distinct from empty API catalog; internal reviewer can proceed; no speculative clink dispatch |
| Only authoring provider or no launchable clients | Both | Zero external calls; explicit coverage limitation; no same-provider substitution |
| Unknown author/client identity or duplicate-provider clients | Both | Resolve required identity/mapping before affected dispatch; no guessing and no duplicate diversity claim |
| One CLI fails while others succeed | Both | All selected providers still attempted; partial result attribution; no retry cascade or API substitution |
| Missing criterion or evidence read; plausible citations | Both | Unread instructions stop dependent investigation; unverified receipt cannot establish corroboration |
| Review response with no exposed read telemetry | Both | Client remains eligible; retain useful attributed findings with unverified receipt; no corroboration or broad approval based on that response; missing telemetry alone does not fail C7 |
| Truncated or summarized result; semantic CLI failure | Both | Completion and coverage remain qualified even after transport success |
| Independent continuation and additional evidence | Both | Correct reviewer continuation; `allow_edits=false` on every request; no inherited prior-request edit opt-in, author history or other reviewer findings; relevant additions shared without conclusions |
| Native write permissions remain available with `allow_edits=false` | Both | Preserve native policy; prompt forbids edits; disclose lack of enforced read-only access without excluding the client solely for inherited permissions; unchanged fixture is no-edit evidence only, while an observed project-file edit fails C4 |
| Staged/range source differs from worktree | Code | Supplied candidate/historical snapshots used; no default-worktree scope replacement |
| Default and explicit document scopes | Design | All three documents by default; selected subsets respected; missing targets disclosed; planned implementation is not a code defect |
| Several independent supporters; internal reviewer disagrees | Both | Evidence-backed corroboration names supporters; severity differences retained; no majority-vote suppression |
| All reviewers fail | Both | No completed review or approval claim; suggest standard mode without silently running it |
| Standard review invocation | Both | Existing standard mode; no new discovery or clink path |

Run both host variants for discovery-only routing, author exclusion, instruction ordering and scope. Exercise the complete remaining matrix at least once per affected skill. Record fixture identity, host/model, expected assertions, actual result and limits. Behavioral outcomes cannot be inferred solely from keyword/structure tests.

**Superseded 2026-10-23 (user-approved criterion change, recorded in tasks.md Task 1 execution context):** the matrix above is the design-time inventory of concerns, not a one-scenario-per-row authoring or completion requirement. Ship only decision-relevant scenarios (several rows share one decision-table branch and are covered together), grade semantic outcomes rather than wording or layout, and apply the bounded gate in Task 3.2 instead of exercising every row on every host.

## Task 2b: Default provider mapping for shipped clients

Authorized 2026-10-24 after Task 2 (design.md [Review corrections (2026-10-24)](design.md#review-corrections-2026-10-24)). Deliver the default mapping and the provider-source label in one slice, before Task 3 documents the behavior.

Primary files:

- `klaude-plugin/skills/_shared/external-review-invocation.md` (roster rule, reviewer record, aggregation/report).
- `klaude-plugin/skills/review-code/review-isolated.md`, `review-code/SKILL.md`, `review-design/review-isolated.md`, `review-design/SKILL.md` (discovery sentence, roster report line, mode description).
- Code-review eval 40, rewritten from "undeclared mapping asks a question" to "shipped names get assumed defaults and no question"; eval 29 covers the custom-name question with assumed defaults present and an advertised retired gemini.

1. In the shared protocol, resolve each candidate's provider in order: operator declaration (`declared`), shipped-name default (`assumed from shipped manifest`), otherwise undeclared. State the three shipped names (`claude`, `codex`, `agy`) and their defaults in the protocol itself, and that `gemini` is retired and never a candidate, and keep the rules that a declaration overrides a default, that a mapping introduced by the reviewed diff is not a declaration, and that a custom name is never guessed → verify: eval 40's clients resolve without a question and eval 29's `mycli` still does not.
2. Carry the provider source into the reviewer record, the roster line of both report templates and the corroboration rule (a corroboration resting on an assumed provider is labeled) → verify: the report shows `declared` or `assumed` per external reviewer.
3. Update both SKILL.md isolated-mode descriptions so consumers learn that shipped clients work without configuration and that a declaration overrides or extends the defaults → verify: no remaining "must be declared" wording for shipped clients.
4. Rewrite eval 40 (rename to `external-default-mapping`), run it and eval 29 once in component mode, regenerate Codex output and run the structure/graph checks → verify: eval 40 shows assumed labels, codex excluded by default, no question; eval 29 still asks for `mycli` only and reports gemini as retired.

## Task 3: Final verification and documentation

1. Run `/kk:test` over the changed skill instructions and fixtures, the repository shell suites, `make generate-kodex`, `make plugin-graph`, and the affected generator tests → verify: all required checks pass; intentionally partial eval links remain untouched; a second generation produces identical generated file content.
2. Run the bounded behavioral verification (see Task 3.2 in tasks.md; supersedes the complete-matrix wording) plus live code/document smoke reviews against the Task 0 PAL build → verify: author exclusion, discovery-only selection, configured model use, honest receipt reporting, no-edit behavior and independent continuation survive the final integrated instructions. Recheck affected contracts if PAL changed since Task 0.
3. Run `/kk:document` and update `klaude-plugin/README.md`, relevant user-facing skill guidance, and root `README.md` where it describes isolated review → verify: users can find the minimum verified PAL requirement, configured model ownership, discovery-only behavior, provider count/cost, partial-failure reporting and the limits of no-edit controls and source-receipt evidence. Include the shipped-client provider defaults, the assumed label, how a `CLAUDE.md`/`AGENTS.md` declaration overrides them and when one is required (Task 2b). Plugin prose contains no links back to toolbox-only feature documents.
4. Run `/kk:review-code` with the `skill-md` domain and relevant fixture languages, then `/kk:review-spec` over all three feature documents and final instructions → verify: findings are fixed or recorded with concrete reasons and next actions; the agreed discovery policy and Task 0 gate have not drifted.
5. Record commands, eval outcomes, live evidence and outstanding limitations in `verification/final.md` → verify: no skipped live prerequisite is called passed and no pending implementation is marked done. Apply the repository's feature-completion convention only after the work is actually complete.
6. Reduce `verification/` to compact records before merge (Task 3.7): retain summaries and final.md, move raw captures to the ignored local archive with a hashed inventory → verify: no capture files remain in the feature tree and retained links resolve.

## Deferred verification and upstream gaps

Task 0 is complete for the exact base-plus-patch candidate recorded in [verification/pal-contract.md](verification/pal-contract.md); publication and installation activation remain separate. Provider identity comes from an operator declaration or, for PAL's shipped client names, the labeled defaults introduced by Task 2b; custom names still need a declaration. If later verification finds a required capability missing, record the exact gap with owner and next action, and keep dependent work blocked. Missing read telemetry remains a per-reviewer coverage limit under C7, without requiring a new PAL tracing feature. Native permission inheritance is documented under C4/C5, not deferred sandbox work.

No old-PAL shim, automatic model selector or runtime backend switch is a deferred task: those are explicit exclusions. Concurrent dispatch is conditional on verified isolation; sequential dispatch remains a complete supported execution strategy.
