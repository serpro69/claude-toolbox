# Tasks: clink fallback for isolated reviews

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#168](https://github.com/serpro69/claude-toolbox/issues/168)
> Status: pending
> Created: 2026-10-11
> Not Doing: runtime API-to-clink fallback, old PAL compatibility, standard-mode changes, automatic model ranking, CLI installation/login/configuration changes, authoring-provider external reviews, new orchestration service or general eval runner, PAL implementation in this repository

The user-approved scope covers both isolated review skills, every eligible non-authoring provider and configured review models. **Task 0 must pass before any plugin instruction authoring starts.** All implementation and verification work below is pending; writing these documents completes none of these tasks.

## Task 0: Verify the new PAL review contract

- **Status:** pending
- **Depends on:** candidate PAL implementation of the required new contract
- **Size:** M
- **Slicing:** Risk-First / Contract-First
- **Can run in parallel with:** —
- **Docs:** [Implementation: Task 0](implementation.md#task-0-verify-the-new-pal-contract), [C1–C8 acceptance contract](design.md#task-0-acceptance-contract)

### Subtasks

- [ ] 0.1 Inspect implemented PAL discovery, schemas, review-role configuration and revision; create `verification/pal-contract.md` → verify: C1–C8 each have a result and evidence reference, with planned behavior distinguished from observed behavior.
- [ ] 0.2 Verify API available/unavailable/unknown states, client launchability, provider identity, author exclusion and configured models → verify: C1–C3 yield a deterministic eligible roster without guessed parameters, credentials or duplicate-provider counts.
- [ ] 0.3 Run disposable live code/document review and provider-free continuation fixtures through MCP, including plugin criteria and outside-worktree snapshots → verify: C4–C5 demonstrate file access, unchanged fixture contents, fresh conversations and per-request `allow_edits=false`.
- [ ] 0.4 Exercise semantic errors, permission-denied partial output, timeout and truncation/summary handling; identify observable read receipts → verify: C6–C7 distinguish usable review from diagnostic output or unverified coverage.
- [ ] 0.5 Verify complete multi-provider execution and test concurrent isolation → verify: C8 covers every eligible provider once; record parallel or sequential scheduling without changing the roster.
- [ ] 0.6 Record the minimum verified PAL revision, exact integration contract and any gaps → verify: every required row passes before Task 1 starts; otherwise set this task blocked with observed behavior, required upstream change, owner and next action.

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
- [ ] 3.2 Complete the behavioral matrix for both skills and supported hosts, plus live code/document smoke reviews → verify: final instructions satisfy discovery-only selection, configured models, provider exclusion, scope, read evidence and independent continuation against the verified PAL build.
- [ ] 3.3 Run `/kk:document` and update plugin/root user guidance where isolated review is described → verify: minimum PAL contract, reviewer count/cost, model ownership and failure behavior are clear, with no toolbox-only documentation dependencies inside plugin files.
- [ ] 3.4 Run `/kk:review-code` with the `skill-md` domain and relevant fixture languages → verify: instruction ordering, shared-file reuse, routing simplicity and regressions are reviewed; unresolved findings have durable reasons and concrete next actions.
- [ ] 3.5 Run `/kk:review-spec` against design, implementation, tasks and final instructions → verify: implementation matches all confirmed choices and no required Task 0 row was waived.
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
