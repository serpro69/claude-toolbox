# Tasks: clink fallback for isolated reviews

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#168](https://github.com/serpro69/claude-toolbox/issues/168)
> Status: Task 0 complete against the recorded corrected PAL build; Tasks 1–3 pending
> Created: 2026-10-11
> Not Doing: runtime API-to-clink fallback, old PAL compatibility, standard-mode changes, automatic model ranking, CLI installation/login/configuration changes, authoring-provider external reviews, new orchestration service or general eval runner, PAL implementation in this repository

The user-approved scope covers both isolated review skills, every eligible non-authoring provider and configured review models. **Task 0 must pass before any plugin instruction authoring starts.** Task 0 has passed against the precisely identified corrected local PAL build; Tasks 1–3 remain pending. This is not a claim that unmodified PAL 1.4.2 or the currently connected server contains the correction.

The [2026-10-21 review corrections](design.md#review-corrections-2026-10-21) apply to these gates: C7 requires accurate reporting when telemetry is absent, not telemetry availability; C4/C5 require no-edit behavior and per-request controls without claiming an enforced sandbox or changing native permissions.

## Task 0: Verify the new PAL review contract

- **Status:** done
- **Depends on:** candidate PAL implementation of the required new contract
- **Size:** M
- **Slicing:** Risk-First / Contract-First
- **Can run in parallel with:** —
- **Docs:** [Implementation: Task 0](implementation.md#task-0-verify-the-new-pal-contract), [C1–C8 acceptance contract](design.md#task-0-acceptance-contract)

### Execution context

- 2026-10-23 — **Committed / provenance reconciled:** at the user's request, PAL revision `c73dab7d8cf9d791961b84614a0e082b74ee5569` now contains the reviewed fix. Its diff from `d25c2d029a5d157935aa9bb836c18e9725969b8f` exactly matches the retained patch hash, and all three file hashes match the tested source. This commit is the minimum verified PAL revision; publication and installation activation remain separate.
- 2026-10-23 — **Completed / independently approved:** the authorized PAL fix now exposes CLI startup observations in API-mode `listmodels` while preserving API catalog and provider-free behavior. Four regressions failed before the correction; afterward 74 focused tests and the complete PAL quality check passed (**3,449 passed, 17 skipped, 26 deselected, 19 subtests**, lint/format/import checks passed). The repeated empty-catalog probe confirms returned CLI availability and unchanged API catalog text. The three reviewed files are applied to the sibling PAL worktree. Minimum verified build: base `d25c2d029a5d157935aa9bb836c18e9725969b8f` plus [the retained patch](verification/linux-20261023/pal-discovery.patch), SHA-256 `b8de8e14faea5b87c242b20342a32481b5d056029ab07127b170f73f2c098475`; file hashes and commands are in [validation evidence](verification/linux-20261023/pal-fix-validation.json). [Independent review](verification/linux-20261023/independent-review.md) approved closure of C1/C2 and retention of the unchanged C3–C8 evidence. All Task 0 checks pass for this candidate, now committed as `c73dab7d8cf9d791961b84614a0e082b74ee5569`. PAL publication/activation remains with its maintainer: publish/release the commit, update/restart the intended installation, then verify its discovery metadata before relying on the new branch there. Task 1 authoring is now unblocked against the verified contract; no plugin instructions changed.
- 2026-10-23 — **Explicitly accepted:** after the discovery gap was explained, the user authorized the minimal sibling `pal-mcp-server` fix, its focused regression and affected verification to finish Task 0. Work is limited to exposing existing CLI startup observations in API-mode `listmodels`, preserving model-selection behavior, and updating the verified candidate/evidence. The historical blocked result remains valid for the original PAL revision.
- 2026-10-23 — **Observed / independently reviewed:** [829 existing upstream tests passed](verification/linux-20261023/upstream-tests.json), with 11 live agy combinations explicitly deselected. The selected live Claude/agy fixture reviews and context-dependent continuations passed on Linux; both returned the four file-only markers and intended defects, with six unchanged fixture hashes. A fresh internal reviewer received equivalent substantive criteria/evidence. The user explicitly approved a fixture-only temporary Claude read grant; the separately sourced MCP server retained `sonnet` and default permission mode without saved configuration changes. Agy used existing native `auto` mode. C3–C8 are supported within the [recorded limits](verification/linux-20261023/README.md).
- 2026-10-23 — **Observed / blocked:** final interface reconciliation and independent review identified a C1/C2 gap. A [focused executed probe](verification/linux-20261023/empty-api-discovery.json) confirms that a configured API provider with zero eligible models returns no CLI executable observations from `listmodels`; these are only exposed in provider-free mode. The clink schema lists configured clients, not launchability. Owner: PAL upstream implementer. Next action: expose existing CLI observations in API-mode discovery, add the empty-catalog regression, run affected checks, then reconcile the candidate revision and independent review. No minimum fully verified PAL revision is established; Task 1 remains gated. Historical Capy/Claude/agy access blockers are superseded by the new Linux evidence.
- 2026-10-23 — **Explicitly accepted / observed:** resumed Task 0 on Linux at toolbox revision `09f9be3b334b0f9265d0a5b9107af6cafe429b5e`; the user requested revalidation of previously passed checks as well as completion of open cases. PAL checkout remains `d25c2d029a5d157935aa9bb836c18e9725969b8f`. Live PAL 1.4.2 discovery finds Claude and agy, with no API providers/models; Codex and Gemini executables are unavailable to PAL. Capy capture now starts successfully. Historical macOS results remain intact; this run uses disposable fixtures and records host-specific results under `verification/linux-20261023/`. No plugin authoring is in scope.
- 2026-10-22 — **Observed:** verification started from clean toolbox revision `5d0c5dd1e30ceb37b56bd83a8c61add853012f8c`. Scope is Task 0 only: evidence and disposable fixtures, with no plugin instruction changes. The corrected C1–C8 contract in `design.md` governs acceptance.
- 2026-10-22 — **Observed:** connected PAL reports version `1.4.2`, provider-free mode, no API models, and executable-present `agy`, `claude`, `codex`, `gemini`; authentication remains unverified. The local PAL checkout and cached 1.4.2 package provenance both name `d25c2d029a5d157935aa9bb836c18e9725969b8f`. Live/source equivalence and the remaining checks will be recorded in [verification/pal-contract.md](verification/pal-contract.md).
- 2026-10-22 — **Unresolved:** PAL discovery has no provider identity field. The current fixture author is OpenAI (this Codex session), so OpenAI is excluded. Operator selection was requested for `gemini`/`agy` before dispatching either ambiguous provider entry. Native login, model configuration and permissions remain unchanged.
- 2026-10-22 — **Explicitly accepted, superseding the pending roster question:** the user selected agy for Google and excluded Gemini. Claude/Anthropic and agy/Google were both attempted. Claude authentication initially failed and was repaired by the user; subsequent MCP requests and continuation succeeded, but criteria reads were denied. agy returned a native read-permission failure.
- 2026-10-22 — **Explicitly accepted / observed:** the user proposed a Claude read grant and said “try that.” A process-local `--allowedTools Read` direct CLI probe returned all four file-only receipt markers, identified both intended defects, and left all six fixture hashes unchanged. Saved configuration was not changed. This is a direct CLI result, not a passed MCP acceptance check; see [read-grant evidence](verification/claude-read-grant.json).
- 2026-10-22 — **Unresolved:** required automated checks cannot start because Capy capture reports Linux-only supervision on this macOS host. MCP verification with the Claude grant, agy access, remaining C1–C8 cases and independent review remain open. Owners, concrete next actions and evidence limits are recorded in [the partial contract record](verification/pal-contract.md#reproduction-and-outstanding-actions); Task 1 remains gated.
- 2026-10-22 — **Observed / repaired:** after the user updated the Claude client manifest and relaunched the session, no PAL tools were exposed. The user override at `~/.pal/cli_clients/claude.json` lacked the required `name` and `command` fields; PAL's registry parses complete client definitions, not partial merges. Added only `"name": "claude"` and `"command": "claude"`, retaining the user's `--allowedTools Read,Glob,Grep` and permission-mode arguments. Original saved at `/private/tmp/clink-contract-20261022/claude-manifest-before-repair.json`. JSON parsing succeeds; PAL startup is still unverified until the operator reconnects/restarts it. No explicit model or roles are in this override, so a new default-role call will use Claude's native model configuration and PAL's automatically supplied default prompt.
- 2026-10-22 — **Observed, superseding the pending Claude startup/access check:** after the user's next restart, PAL discovery and a fresh `role: "default"`, `allow_edits: false` MCP review succeeded. The returned launch command contains `--allowedTools Read,Glob,Grep`; observed model is the native default `claude-fable-5-1`. Returned tool results show criteria first, five successful file reads including the external snapshot, and the expected missing optional file. Both intended defects and all four markers were returned. A context-dependent MCP follow-up inherited the same role/directory, retained two messages and recalled the defects/markers with no new tool calls. All six fixture hashes stayed unchanged. See [MCP evidence](verification/claude-default-mcp.json) and [continuation evidence](verification/claude-default-mcp-followup.json). Claude's fixture access is verified; agy access, automated cases and independent review remain open.
- 2026-10-22 — **Explicitly accepted / observed:** the user requested Codex clink verification as an additional integration check. Codex CLI `0.163.0` passed fresh default-role MCP review and context-dependent continuation with its existing shipped manifest and `allow_edits=false`; both intended defects and four file-only markers returned, all six fixture hashes unchanged. A separate Git-backed fixture permits read-only shell commands because Codex uses them for file access. PAL removed event traces and returned no model identity; configured `gpt-6-astra` is not an observed model claim. See [Codex evidence](verification/codex-default-mcp.json) and [follow-up](verification/codex-default-mcp-followup.json). The authoring-provider exclusion for independent review remains intact; this transport check is not corroboration.
- 2026-10-22 — **Observed, superseding the agy access blocker:** under the user's request to resolve agy, added only `permissions.allow: ["read_file(/private/tmp/clink-contract-20261022)"]` to native agy settings, backed up at `/private/tmp/agy-read-grant.rf4FUy/settings.before.json`. With installed agy `1.4.5`, a fresh default-role MCP review and context-dependent continuation both succeeded with `allow_edits=false`, all four markers, both intended defects and unchanged hashes for six fixtures. No PAL configuration/restart, mode flag, write or command grant was needed. See [agy evidence](verification/agy-default-mcp.json) and [follow-up](verification/agy-default-mcp-followup.json). Model identity and detailed read trace remain unavailable; native severity/optional advice are retained as quality observations, not added acceptance gates. Other external input directories need their own operator-approved read scopes; this grant covers only the disposable fixture.
- 2026-10-22 — **Status audit:** live review/access/continuation checks now succeeded for Claude, agy and the separately requested Codex integration check. C3 configuration ownership/identity reporting, C4 fixture access/no-edit behavior and C7 coverage reporting are satisfied within their recorded bounds; unavailable returned model names/traces do not create new gates. Remaining work is C1/C2 discovery/eligibility cases, C5 edit-opt-in reset and cross-conversation isolation, C6 missing-executable/partial-output/timeout/output-limit cases, C8 internal payload parity, and independent review/final baseline reconciliation. Capy's capture admission failure still blocks automated execution. Parallel dispatch remains unverified and sequential scheduling is supported; no parallel-support claim is made.

### Subtasks

- [x] 0.1 Inspect implemented PAL discovery, schemas, review-role configuration and revision; create `verification/pal-contract.md` → verify: C1–C8 each have a result and evidence reference, with planned behavior distinguished from observed behavior.
- [x] 0.2 Verify API available/unavailable/unknown states, client launchability, provider identity, author exclusion and configured models → verify: C1–C3 yield a deterministic eligible roster without guessed parameters, credentials or duplicate-provider counts.
- [x] 0.3 Run disposable live code/document review and provider-free continuation fixtures through MCP, including plugin criteria and outside-worktree snapshots → verify: C4–C5 demonstrate access through file-only content absent from the prompt or observed reads, unchanged fixture contents, fresh conversations and per-request `allow_edits=false` without reusing an earlier edit opt-in; record inherited native permissions without claiming enforced read-only access.
- [x] 0.4 Exercise semantic errors, permission-denied partial output, timeout, truncation/summary and absent read telemetry → verify: C6–C7 distinguish diagnostics from useful attributed results, keep unknown receipt explicit and prohibit unsupported corroboration or broad approval; absent telemetry alone does not fail C7.
- [x] 0.5 Verify complete multi-provider execution and test concurrent isolation → verify: C8 covers every eligible provider once; record parallel or sequential scheduling without changing the roster.
- [x] 0.6 Record the minimum verified PAL revision, exact integration contract and any gaps → verify: every required check passes before Task 1 starts; unknown receipt may remain a disclosed limit after C7 passes. For an unmet required check, keep this task blocked with observed behavior, required correction, owner and next action; no unrun check is passed.

## Task 1: Deliver discovery-only clink code review

- **Status:** pending
- **Depends on:** Task 0
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Implementation: Task 1](implementation.md#task-1-code-review-with-discovery-only-clink-selection)

### Subtasks

- [ ] 1.1 Create `_shared/external-review-invocation.md` and its `review-code/shared-external-review-invocation.md` symlink → verify: shared rules select one backend at discovery and preserve the existing API transport.
- [ ] 1.2 Integrate the protocol into `review-code/review-isolated.md`, keeping all instruction loads before investigation → verify: loading traces include every common/profile criterion and one post-instruction investigation entry.
- [ ] 1.3 Dispatch the complete selected snapshot/evidence manifest to every eligible clink reviewer with fresh conversations and configured models → verify: author exclusion, roster completeness, selected revision and evidence parity hold in the multi-provider fixture.
- [ ] 1.4 Generalize code-review result aggregation and failures for multiple external reviewers → verify: native findings, evidenced corroboration, unknown coverage and useful partial results retain their attribution.
- [ ] 1.5 Update `review-code/SKILL.md` and `commands/review-code/isolated.md`; add code-review scenarios from the evaluation matrix → verify: API success and runtime-failure cases make zero clink calls, and standard mode remains unchanged.
- [ ] 1.6 Run code-review evals, `make generate-kodex`, `bash test/test-plugin-structure.sh`, `bash test/test-codex-structure.sh` and `make plugin-graph` → verify: recorded assertions and structure checks pass without repairing intentionally partial eval links.

## Task 2: Deliver clink design review with shared criteria

- **Status:** pending
- **Depends on:** Task 0, Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Implementation: Task 2](implementation.md#task-2-design-review-with-the-same-external-selection)

### Subtasks

- [ ] 2.1 Extract reusable checks into `_shared/design-review-criteria.md`, add the per-skill symlink and update `agents/design-reviewer.md` → verify: all prior checks remain, methodology loads before evaluation, and agent access/output contracts are preserved.
- [ ] 2.2 Integrate shared external selection into `review-design/review-isolated.md` with explicit instruction loading → verify: the same discovery table applies and API runtime failure never triggers clink.
- [ ] 2.3 Supply document-review framing, shared criteria, selected documents and existing source to each external reviewer → verify: default and explicit scopes work, missing targets are disclosed and planned code is not reported as missing implementation.
- [ ] 2.4 Generalize design reporting and update `review-design/SKILL.md` → verify: reviewer roster, native output, coverage limits, independent corroboration and all-reviewer failure are represented accurately.
- [ ] 2.5 Add and run design-review scenarios, regenerate Codex artifacts and run targeted structure/graph checks → verify: code-review regressions still pass and no new design-review command or agent name is introduced.

## Task 3: Final verification and user documentation

- **Status:** pending
- **Depends on:** Task 0, Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Implementation: Task 3](implementation.md#task-3-final-verification-and-documentation)

### Subtasks

- [ ] 3.1 Run `/kk:test`, the full repository shell suites, generator checks and `make plugin-graph` → verify: tests pass and repeated generation leaves identical generated content.
- [ ] 3.2 Complete the behavioral matrix for both skills and supported hosts, plus live code/document smoke reviews → verify: final instructions satisfy discovery-only selection, configured models, provider exclusion, scope, honest receipt reporting, no-edit behavior and independent continuation against the verified PAL build.
- [ ] 3.3 Run `/kk:document` and update plugin/root user guidance where isolated review is described → verify: minimum PAL contract, reviewer count/cost, model ownership, failure behavior and permission/receipt limits are clear, with no toolbox-only documentation dependencies inside plugin files.
- [ ] 3.4 Run `/kk:review-code` with the `skill-md` domain and relevant fixture languages → verify: instruction ordering, shared-file reuse, routing simplicity and regressions are reviewed; unresolved findings have durable reasons and concrete next actions.
- [ ] 3.5 Run `/kk:review-spec` against design, implementation, tasks and final instructions → verify: implementation matches all confirmed choices and every Task 0 check under the corrected acceptance contract passed; superseded telemetry and sandbox interpretations are not reintroduced as gates.
- [ ] 3.6 Write `verification/final.md` with actual commands, eval outcomes, live evidence and remaining limits → verify: skipped checks remain explicit and completion is claimed only after required work passes.

## Dependency Graph

```text
New PAL candidate
        |
        v
Task 0: verify contracts
        |
        v
Task 1: isolated code review
        |
        v
Task 2: isolated design review
        |
        v
Task 3: final verification and documentation
```
