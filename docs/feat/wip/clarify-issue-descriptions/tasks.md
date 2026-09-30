# Tasks: clarify issue descriptions

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#157](https://github.com/serpro69/claude-toolbox/issues/157)
> Status: pending
> Created: 2026-09-30
> Not Doing: remote publication/comments, issue implementation/reproduction, invented decisions/criteria, mandatory integrations/live certification, separate issue guide/new skill/profile, automatic clarification, bulk rewrites/extra summaries, completed-design edits

## Task 1: Clarify bug reports into local drafts

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Bug-report slice](implementation.md#task-1-clarify-bug-reports-locally), [request contract](design.md#request-and-output-contract)

### Subtasks

- [ ] 1.1 Author `github-issue-bug` and `issue-local-draft` under `klaude-plugin/skills/clarify-docs/evals/`, with isolated grader oracles → verify: scenario IDs 16/17 are unique, manifests are self-contained, and baseline runs record observed routing/evidence/file effects.
- [ ] 1.2 Extend `klaude-plugin/skills/clarify-docs/SKILL.md` for issue-description inputs and explicit implement/fix non-triggers → verify: preserve existing scope/loading rules and recheck current description guidance and measured length.
- [ ] 1.3 Add issue evidence and bug-report preservation guidance to `klaude-plugin/skills/_shared/document-clarity.md` → verify: scenarios 16/17 preserve reported versus verified behavior, reproduction details, local output, and collision protection without requiring PR revisions.
- [ ] 1.4 Extend `clarify-docs/evals/README.md` with offline issue staging → verify: both scenarios run without live tracker access, oracle leakage, or PR base/head setup.
- [ ] 1.5 Count shared instructions, run `make generate-kodex` and `make plugin-graph`, inspect generated changes, and run `dense-source`/`runtime-pr` smoke regressions → verify: at most 1,200 words, structural checks pass, all applicable behavioral assertions pass with recorded evidence.

## Task 2: Clarify unimplemented features for the intended audience

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Proposal slice](implementation.md#task-2-clarify-proposals-for-their-actual-audience), [audience rules](design.md#audience-and-incomplete-context)

### Subtasks

- [ ] 2.1 Author `linear-issue-feature` and `issue-destination-visibility` evals, IDs 18/19 → verify: baseline evidence records existing behavior and oracles separate accepted intent, proposals, unknown decisions, and actual audience access.
- [ ] 2.2 Extend the shared procedure's feature/other-issue guidance → verify: scenario 18 preserves existing criteria and unknowns without demanding implementation, inventing criteria, or imposing bug-report sections.
- [ ] 2.3 Scope PR-head visibility to its existing audience and apply common sharing rules to issue readers → verify: scenario 19 retains shared references and excludes restricted facts/pointers from the draft and report, including uncited paraphrases.
- [ ] 2.4 Regenerate Codex output, count instructions, and run structure/graph checks plus `contract-only-pr`/`destination-visibility` regressions → verify: all applicable assertions pass; rerun 16/17 when changed rules affect them.

## Task 3: Handle incomplete inputs and execution non-triggers

- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Gap and routing slice](implementation.md#task-3-handle-gaps-and-keep-execution-requests-out), [eval matrix](implementation.md#evaluation-matrix)

### Subtasks

- [ ] 3.1 Author `issue-pasted-missing-destination`, `issue-unavailable-source`, and `issue-unavailable-body` evals, IDs 20–22 → verify: respectively ask before writing, produce a qualified draft, and request missing body text without fabricated output.
- [ ] 3.2 Clarify entry-point/shared rules only where these cases reveal a gap → verify: accessible context is investigated first; input captures and unrelated files remain unchanged; unresolved claims retain next steps and known/unknown ownership.
- [ ] 3.3 Author separate `issue-implement-non-trigger` and `issue-fix-non-trigger` evals, IDs 23/24, with ordinary execution requests and small source fixtures; expose only the skill description for selection → verify: normal fixture handling does not load editorial instructions, edit issue text, or create an editorial draft; do not prime the agent with classification-only prompts.
- [ ] 3.4 Regenerate and run instruction-size/structure/graph checks and applicable existing missing-context/non-trigger regressions → verify: all assertions pass with complete traces and no instruction-budget regression.

## Task 4: Document and verify the complete extension

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#task-4-document-usage-and-verify-the-complete-extension), [evidence protocol](implementation.md#execution-and-evidence-protocol), [repository checks](implementation.md#repository-checks)

### Subtasks

- [ ] 4.1 Run `/kk:document` to update `README.md`, `docs/getting-started/overview.md`, and `docs/user-guide/skills.md` → verify: documented issue examples, local output, gaps, disclosure, and implementation boundaries match the design and preserve optional clarification.
- [ ] 4.2 Execute all nine new scenarios, all fifteen current standalone scenarios, and the five current design/document consumer scenarios listed in the implementation plan → verify: every applicable assertion passes on the final instructions, with fresh-reader comparison where applicable and no leaked or incomplete traces.
- [ ] 4.3 Maintain this feature's `verification.md` and `verification/<run-id>/` evidence as runs occur → verify: exact prompts/settings, hashes/manifests, traces, reader answers, failures and per-assertion verdicts are linked; authored-but-unrun cases remain explicitly incomplete.
- [ ] 4.4 Run `/kk:test` over all shell suites, generation, graph validation, and Go tests → verify: each outcome is recorded, generation is idempotent, and intended generated changes are distinguished from drift.
- [ ] 4.5 Run `/kk:review-code` for Markdown skill instructions, JSON eval specifications, and generated Codex content → verify: resolve findings or record remaining work durably with owner and next action; do not relax acceptance to close the task.
- [ ] 4.6 Run `/kk:review-spec` against all three design artifacts → verify: implementation, docs, generated output, and executed evidence cover every issue acceptance criterion before marking the feature complete.

## Dependency Graph

```text
Task 1 ──→ Task 2 ──→ Task 3 ──→ Task 4
   └───────────────────────────→ Task 4
             └─────────────────→ Task 4
```
