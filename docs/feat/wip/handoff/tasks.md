# Tasks: Manual handoff through a secret gist

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#102](https://github.com/serpro69/claude-toolbox/issues/102)
> Status: pending
> Created: 2026-10-28
> Not Doing: lifecycle automation, automatic discovery/loading, Capy indexing/archival, whole-transcript export, private storage, persistent local handoff store, automatic retention, worktree transfer, separate resume skill or helper, custom override syntax

The accepted storage is a fresh secret gist with `prompt.md` and `handoff.md`; anyone-with-the-link access is accepted for v1. The earlier local-state storage proposal is superseded. Capy references require evidence of prior indexing/archival of the relevant material. The handoff must never initiate indexing or archival, directly or indirectly.

## Task 1: Deliver the manual handoff path in both plugin distributions

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Complete manual path](implementation.md#implement-the-complete-manual-path), [Capy boundary](design.md#capy-references-and-the-indexing-prohibition), [Publication](design.md#gist-storage-and-publication)

### Subtasks

- [ ] 1.1 Create `klaude-plugin/skills/handoff/SKILL.md` with a trigger-first description that makes manual GitHub publication clear, mandatory instruction loading, one investigation entry point and the active-task content outline. Keep ordinary explicit instructions under normal LLM instruction following.
- [ ] 1.2 Implement the existing-reference branch in that skill: reference only relevant material whose prior indexing/archival is evidenced; omit references otherwise. Prohibit indexing, fetch-and-index, archival and indirect indexing through tools, skills, agents or the starter prompt.
- [ ] 1.3 Implement the instruction-only publication sequence: isolated temporary preparation outside the repository, secret gist creation with `handoff.md`, addition of `prompt.md` with the returned URL, final verification and a copyable starter prompt. Cover partial/uncertain failures and preserve recovery content without blind creation retries.
- [ ] 1.4 Add the five scenario directories and execution guide under `klaude-plugin/skills/handoff/evals/` specified in [Verification](implementation.md#verification). Keep real input fixtures in `test-files/` and grader-only material outside it. Use synthetic GitHub responses rather than real session uploads.
- [ ] 1.5 Add `handoff` to `test/test-plugin-structure.sh` `EXPECTED_SKILLS`; update `docs/user-guide/skills.md`, both README inventories and the counts in `docs/contributing/architecture.md`. Do not add a command wrapper, hook, generator override or indexing protocol dependency.
- [ ] 1.6 Run `make generate-kodex` through captured execution and inspect the generated handoff skill. Verify structure, transformed invocation prefixes and unchanged semantic boundaries; record results below.

### Execution context

Design preparation inspected the generator manifest's `include_all: true`, skill registration, documentation inventories and existing scenario conventions. GitHub visibility and CLI operations were checked against official documentation and installed `gh` 2.103.3 help on 2026-10-28. No handoff skill, gist or live behavioral test has been created by this design task. Refresh repository state before implementation and attribute each later test result to the actual candidate.

## Task 2: Verify, document and review the complete feature

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Verification](implementation.md#verification), [Acceptance](design.md#acceptance-and-evidence-limits)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the five semantic scenarios on canonical and generated instructions, using the bounded effort and evidence rules in the implementation plan. Record outcomes, actual provider/host coverage, attempted indexing, partial publication behavior and any unavailable execution.
- [ ] 2.2 Complete the applicable `make plugin-graph`, `make docs-build` and generated-freshness checks. Reuse Task 1's successful generator/structure results unless changes or failures justify repeating them; preserve all required repository/release gates.
- [ ] 2.3 Invoke `/kk:document` to reconcile the user-facing workflow and inventories with the implemented behavior. Explain secret visibility, explicit loading and the prohibition on handoff indexing.
- [ ] 2.4 Invoke `/kk:review-code` with Markdown/agent-skill context and `/kk:review-spec` for `docs/feat/wip/handoff/`. Address material findings and record any remaining issue, its reason and concrete next action durably.
- [ ] 2.5 Assess completion using the evidence: faithful continuation, two-file secret gist, no unintended worktree changes or overwritten snapshots, truthful failure states and no handoff-initiated indexing/archival. Distinguish material failures from prose-quality observations and coverage limits.
- [ ] 2.6 Once implementation and its applicable checks/reviews are complete, move the feature documents to `docs/feat/done/handoff/` and update affected references and status. Do not mark the feature complete merely because design documents exist.

### Verification record

Pending implementation. No runtime, generated-output or behavioral checks have yet been executed for the new skill. Design-document link/whitespace checks are recorded separately from feature verification.

Design-only verification on 2026-10-28 checked all 18 local document links, including heading targets, and trailing whitespace successfully. The three feature documents are excluded from the rendered site by `mkdocs.yml`'s `feat/**` rule; no site build or implementation suite was run for this documentation-only change. Independent design review remains pending.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
