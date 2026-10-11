# Implementation: clink fallback for isolated reviews

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: pending; Task 0 must pass before plugin instruction authoring

## Repository orientation

Edit canonical instructions under `klaude-plugin/`; generated files under `kodex-plugin/` and `.codex/agents/` come from `make generate-kodex`. Shared sources have bare names in `skills/_shared/` and each skill consumer gets a `shared-<name>.md` symlink. Agents refer to shared sources through resolved plugin-root paths rather than per-skill symlinks.

Follow [plugin architecture](../../../contributing/architecture.md), [testing conventions](../../../contributing/testing.md) and the repository's instruction-ordering rules. Load all common instructions and resolved profile checklists before content investigation. Plugin instructions must stand alone in a consumer repository: this feature's documentation is not a runtime dependency and must not be linked from plugin prose.

Preserve the existing API transport in `skills/_shared/pal-codereview-invocation.md`. Add shared routing and clink instructions rather than replicating the API sequence in both callers. Do not add a design-review command wrapper: no such wrapper exists at the design baseline.

## Task 0: Verify the new PAL contract

**Strategy:** Risk-First / Contract-First. This task produces verification evidence and any necessary design correction; it does not author plugin instructions.

1. Inspect the candidate PAL implementation, its new CLI-only/reliability plans and advertised tool schemas. Record commit/release, CLI versions, sanitized effective review-role configuration and actual working-directory behavior in `verification/pal-contract.md` → verify: every C1–C8 row in [the acceptance contract](design.md#task-0-acceptance-contract) has an explicit result, evidence reference and reproducible setup.
2. Exercise discovery with an API-backed reviewer available, API review omitted, no eligible API models, and failed/ambiguous discovery. Use isolated configuration and captured/stubbed responses where appropriate → verify: the three discovery states remain distinct and no secret values enter evidence.
3. Establish how discovered clients map to providers and configured review models, including duplicate clients and unknown authorship. Confirm the usable review role and whether model identity is observed or only configured → verify: a deterministic eligible roster can exclude the authoring provider without fabricated fields or CLI-name assumptions.
4. Prepare small disposable code/document fixtures, plugin-like criteria files and a candidate snapshot outside the fixture worktree. Run a live review and a context-dependent follow-up through the actual MCP path without API credentials → verify: needed files are read, fixture content remains unchanged, current-request edit controls remain false, and continuation requires no API model context.
5. Capture representative execution failures, partial read denial and output truncation/summary. Deterministic runner/parser fixtures may cover destructive or impractical failure injections; identify these separately from live evidence → verify: diagnostic-only responses never count as completed reviews and unobserved file receipt never counts as corroboration.
6. Exercise separate reviewer conversations and equivalent evidence. Test concurrent isolation when supported → verify: no cross-review context or result contamination; choose and record parallel or sequential scheduling for the authored protocol. A concurrency failure alone permits sequential scheduling, not skipping reviewers.
7. Resolve the required contract rows and publish the verified schema/configuration mapping and minimum PAL revision in the evidence record → verify: no C1–C8 row remains failed, skipped or unknown before Task 1 starts. Record any upstream gap with observed behavior, required behavior, owner and concrete next action; keep Task 0 blocked if a required capability is absent.

Do not run a paid/login-dependent probe silently while claiming it is a static check. Use already authorized test accounts and disposable fixtures, and follow the execution environment's approval rules. Never install CLIs, initiate login or rewrite user model configuration as a workaround. The selected providers' full live acceptance coverage must be stated; a skipped provider is not a passed contract.

The evidence record is deliberately absent until execution. Creating this plan does not satisfy Task 0. PAL plans at the design-time revision are inputs to verification, not a release pin or implementation evidence.

## Task 1: Code review with discovery-only clink selection

Deliver the full isolated code-review path and its regression evals in one slice.

Primary files:

- New `klaude-plugin/skills/_shared/external-review-invocation.md` and the `review-code/shared-external-review-invocation.md` symlink.
- `klaude-plugin/skills/review-code/review-isolated.md` and `SKILL.md`.
- `klaude-plugin/commands/review-code/isolated.md`.
- Focused scenarios under `klaude-plugin/skills/review-code/evals/`.

1. Write the shared procedure using Task 0's verified contract: discover once, select API/clink/unavailable, freeze the branch and retain per-reviewer records → verify: evaluate API-available, API-unavailable and discovery-error fixtures; no execution failure transitions to clink.
2. Define the clink roster, provider exclusion, configured-model ownership, fresh conversations, no edits, continuation and outcome reporting. State the verified scheduling policy once → verify: the multi-provider fixture attempts every eligible provider exactly once, excludes the authoring provider, and reports missing/unknown candidates without guessing.
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
| Truncated or summarized result; semantic CLI failure | Both | Completion and coverage remain qualified even after transport success |
| Independent continuation and additional evidence | Both | Correct reviewer continuation; `allow_edits=false`; no author history or other reviewer findings; relevant additions shared without conclusions |
| Staged/range source differs from worktree | Code | Supplied candidate/historical snapshots used; no default-worktree scope replacement |
| Default and explicit document scopes | Design | All three documents by default; selected subsets respected; missing targets disclosed; planned implementation is not a code defect |
| Several independent supporters; internal reviewer disagrees | Both | Evidence-backed corroboration names supporters; severity differences retained; no majority-vote suppression |
| All reviewers fail | Both | No completed review or approval claim; suggest standard mode without silently running it |
| Standard review invocation | Both | Existing standard mode; no new discovery or clink path |

Run both host variants for discovery-only routing, author exclusion, instruction ordering and scope. Exercise the complete remaining matrix at least once per affected skill. Record fixture identity, host/model, expected assertions, actual result and limits. Behavioral outcomes cannot be inferred solely from keyword/structure tests.

## Task 3: Final verification and documentation

1. Run `/kk:test` over the changed skill instructions and fixtures, the repository shell suites, `make generate-kodex`, `make plugin-graph`, and the affected generator tests → verify: all required checks pass; intentionally partial eval links remain untouched; a second generation produces identical generated file content.
2. Complete and record the behavioral matrix plus live code/document smoke reviews against the Task 0 PAL build → verify: author exclusion, discovery-only selection, configured model use, source coverage and independent continuation survive the final integrated instructions. Recheck affected contracts if PAL changed since Task 0.
3. Run `/kk:document` and update `klaude-plugin/README.md`, relevant user-facing skill guidance, and root `README.md` where it describes isolated review → verify: users can find the minimum verified PAL requirement, configured model ownership, discovery-only behavior, provider count/cost and partial-failure reporting. Plugin prose contains no links back to toolbox-only feature documents.
4. Run `/kk:review-code` with the `skill-md` domain and relevant fixture languages, then `/kk:review-spec` over all three feature documents and final instructions → verify: findings are fixed or recorded with concrete reasons and next actions; the agreed discovery policy and Task 0 gate have not drifted.
5. Record commands, eval outcomes, live evidence and outstanding limitations in `verification/final.md` → verify: no skipped live prerequisite is called passed and no pending implementation is marked done. Apply the repository's feature-completion convention only after the work is actually complete.

## Deferred verification and upstream gaps

Task 0 is intentionally pending because PAL's new contract is still being implemented. Its next action is to run C1–C8 against a candidate build, not to infer readiness from the upstream design status. In particular, provider identity and child read-receipt observability have no universal schema established by this design. If unsupported, record the exact gap in `verification/pal-contract.md`, identify the PAL component that must supply it and block downstream authoring until resolved.

No old-PAL shim, automatic model selector or runtime backend switch is a deferred task: those are explicit exclusions. Concurrent dispatch is conditional on verified isolation; sequential dispatch remains a complete supported execution strategy.
