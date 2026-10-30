# Tasks: Manual handoff through a secret gist

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#102](https://github.com/serpro69/claude-toolbox/issues/102)
> Status: in-progress
> Design readiness: review findings reconciled; ready for implementation
> Created: 2026-10-28
> Not Doing: lifecycle automation, automatic discovery/loading, post-publication inspection, Capy indexing/archival, whole-transcript export, private storage, persistent local handoff store, automatic retention, worktree transfer, separate resume skill or helper, custom override syntax

The accepted storage is a fresh secret gist with `prompt.md` and `handoff.md`; anyone-with-the-link access is accepted for v1. The earlier local-state storage proposal is superseded. Capy references require evidence of prior indexing/archival of the relevant material. The handoff must never initiate indexing or archival, directly or indirectly.

Successful `gh` publishing commands complete the producer workflow. Do not add a remote read-back, download or metadata check after publication.

Manual-only invocation uses Claude Code's `disable-model-invocation: true` and Codex's `policy.allow_implicit_invocation: false`. Credential exclusion is applied to outgoing content before upload. The fresh-session exercise below evaluates produced artifacts during development; it is not part of the runtime skill.

## Task 1: Deliver the manual handoff path in both plugin distributions

- **Status:** done
- **Depends on:** —
- **Size:** M
- **Sizing rationale:** The core work is the skill, user guide and small fixture stub/runbook. Policy metadata, one-line terminology changes, registrations, fixtures and generation are mechanical consequences; no reusable runner is planned.
- **Can run in parallel with:** —
- **Docs:** [Complete manual path](implementation.md#implement-the-complete-manual-path), [Capy boundary](design.md#capy-references-and-the-indexing-prohibition), [Publication](design.md#gist-storage-and-publication)

### Subtasks

- [x] 1.1 Create `klaude-plugin/skills/handoff/SKILL.md` with manual-only Claude metadata, a description that makes GitHub publication clear, mandatory instruction loading, one investigation entry point and the active-task content outline. Add the Codex manual-only policy in `klaude-plugin/skills/handoff/agents/openai.yaml`. Keep ordinary explicit instructions under normal LLM instruction following.
- [x] 1.2 Implement the existing-reference branch in that skill: reference only relevant material whose prior indexing/archival is evidenced; omit references otherwise. Prohibit indexing, fetch-and-index, archival and indirect indexing through tools, skills, agents or the starter prompt.
- [x] 1.3 Implement the instruction-only publication sequence: isolated temporary preparation, credential/unrelated-private-content exclusion before each payload is sent, secret gist creation with `handoff.md`, addition of the URL-bearing `prompt.md`, and completion on successful `gh` responses. Add no post-publication inspection. Report partial/uncertain failures and preserve recovery content without remote inspection or automatic retries.
- [x] 1.4 Add the five producer scenario directories, `evals/README.md`, evaluator-only multi-turn runbooks and test-only `evals/_support/gh` described in [Conversation and GitHub setup](implementation.md#conversation-and-github-setup). Keep project inputs in `test-files/` and grader-only material outside it. Include the synthetic-credential assertion, real-host invocation-policy control, and the fresh-session leg using the actual successful producer's output.
- [x] 1.5 Add `handoff` to `test/test-plugin-structure.sh` `EXPECTED_SKILLS` and check both provider metadata fields in canonical/generated output. Update `docs/user-guide/skills.md`, both README inventories and `docs/contributing/architecture.md`. Apply the specific live terminology changes in [Entry and context](implementation.md#entry-and-context) to implement, design and clarify-docs. Do not add a command wrapper, hook, generator override or indexing protocol dependency.
- [x] 1.6 Run `make generate-kodex` through captured execution and inspect the generated handoff skill, unchanged YAML policy sidecar and affected terminology. Verify structure, transformed invocation prefixes and semantic boundaries; record results below.

### Execution context

- **2026-10-30 — Task 1 complete:** Delivered the manual skill in both distributions, policy metadata, five scenario runbooks with isolated CLI support, structure registration, live terminology and documentation inventories. Final checks after review corrections all passed: `bash test/test-handoff-stub.sh`, `make generate-kodex` (existing Python 3.12 via temporary PATH), `make plugin-graph`, and strict `make docs-build` (existing default virtualenv via PATH), capture `3560f01a-651a-46c7-9871-c6e12487d0d5`, exit 0. Final generation freshness passed for all 1,153 files including executable modes, capture `c4e1403a-13e7-47e8-972f-e07b4a907f59`. `git diff --check` passed.
- **2026-10-30 — review closure:** Internal `code-reviewer` approved the initial scope and focused follow-up with no findings. External Claude (`claude-opus-5-5`, observed Anthropic) initially returned COMMENT; its fixture cue, cleanup/redaction wording, inventory, record and stub observations were addressed, and its focused follow-up returned APPROVE. The native reviews, receipt limits and corrections are preserved in [review-task-1.md](review-task-1.md). No systemic P0/P1 findings require indexing. The external review corrected an unsupported initial command-execution claim; its later response includes successful source reads and capture inspection. Remaining real-host behavior is explicitly Task 2 evidence, not a Task 1 approval claim.
- **2026-10-30 — bounded fixture support:** Optional `gh auth status` and all-files `gist view` are outside the authored stub surface. Owner: Task 2 evaluator. No expansion is needed preemptively; if a legitimate actor call hits this boundary, classify it as a harness coverage limit, add only the needed support and rerun that affected scenario. This preserves the runbook's concrete failure handling without treating an unsupported stub call as a skill defect. Live GitHub experiments remain optional and separately authorized.

- **2026-10-30 — independent review:** Isolated `code-reviewer` (`gpt-6.1-sol`, OpenAI) inspected the 67-file Task 1 candidate against `3a2744a323996efa256ef043a6b0600d1ac24d66` and returned **APPROVE**, with no P0–P3 findings or evidence requests. It explicitly leaves real-host policy enforcement, summary quality and fresh-session behavior to Task 2. No systemic findings require indexing. PAL discovery selected only the `claude` CLI for external review (Anthropic assumed from the shipped client mapping; model not yet observed); `agy`/`codex` executables were absent and `gemini` is retired. External result pending at this checkpoint.

- **2026-10-30 — superseding verification:** The strict docs build now passes using the existing `/home/sergio/.virtualenvs/default/bin` on PATH (`make docs-build`, capture `67bee989-77b5-4118-819b-c21775644efa`); the earlier missing-command result below was a PATH limitation, with no installation needed. Generated graph artifacts are refreshed. YAML metadata, description budget, five eval schemas and fixture paths passed for both distributions; the generated skill differs only by the expected header/prefix transformation, and its policy/stub are byte-identical (capture `f7cc940c-757e-4db3-8bfd-6e3955c7bf35`). A before/after hash-and-mode snapshot of all 1,153 generated files remained identical after rerunning the generator (capture `09ccbabd-2091-4f66-a9bd-9d7cf04cf5eb`). Task 2 may reuse these repository-check results unless its edits justify repeating them.

- **2026-10-30 — verified:** `test/test-handoff-stub.sh` passed: exact upload snapshots (including failed uploads), public/secret recording, unique snapshots, exact-ID/named-file reads and rejected operations. Captured run `11e1df0a-a957-4eec-a9cd-d74117da849e` also passed generator tests and plugin structure, but its Codex TOML assertions failed because system Python 3.10 lacks `tomllib`/`tomli`. Repeating `make generate-kodex` with the already installed Python 3.12 selected through a temporary PATH entry passed both structure suites (run `f83f87ce-12f5-4bbc-b5bc-0d5d5971c964`); no repository assertion or dependency was changed.
- **2026-10-30 — verified/limited:** `make plugin-graph` passed in that second captured run. The extra `make docs-build` attempt generated the graph artifacts but could not invoke missing `mkdocs`. Task 2 owns the outstanding strict site build: use the documented docs environment and rerun the gate; this is not a successful site-build claim. The generic skill-creator validator rejects the required Claude `disable-model-invocation` key (run `6117bc1f-1a50-45bb-b65d-ff6db49b3bcb`); its restricted schema is not authoritative for this cross-provider field, which is checked directly by the repository tests.
- **2026-10-30 — pending Task 2 evidence:** The five producer scenarios, corresponding-host policy checks and two fresh-session legs are authored, not executed. Task 2's implementer owns those runs under the runbooks' isolated setup; record actual traces and assertion results or specific unavailable execution. No live gist was created. These pending checks do not establish behavioral reliability from deterministic structure/stub results.

- **2026-10-30 — observed:** Task 1 starts from clean revision `3a2744a323996efa256ef043a6b0600d1ac24d66`. Scope is the manual skill, invocation metadata, fixture support, targeted terminology, inventories and generated distribution. Task 2 retains host behavioral evaluations, fresh-session exercises and feature completion. No release or live gist publication is requested.
- **2026-10-30 — authority and preserved contracts:** The accepted design and implementation plan govern; the earlier Capy note prescribing receiver retrieval restrictions is superseded by the recorded user disposition withdrawing F1. Preserve instruction-only publication, no producer read-back/retries/indexing, and existing workflow behavior outside the named terminology edits. Existing generation copies nested YAML without an override.
- **2026-10-30 — observed interface evidence:** This environment has `gh` 2.38.0, unlike the design session's 2.103.3. Its local create/edit help and current official GitHub manuals confirm secret-by-default creation and noninteractive `gist edit --add`. Current Claude skill documentation confirms the 1,536-character description cap; official Codex documentation confirms `policy.allow_implicit_invocation: false`. These are interface checks, not publication or host-policy execution evidence.

Design preparation inspected the generator manifest's `include_all: true`, skill registration, documentation inventories and existing scenario conventions. GitHub visibility and CLI operations were checked against official documentation and installed `gh` 2.103.3 help on 2026-10-28. No handoff skill, gist or live behavioral test has been created by this design task. Refresh repository state before implementation and attribute each later test result to the actual candidate.

On 2026-10-28 the user explicitly retired post-publication inspection: prepare temporary files, publish through `gh`, and accept its success response. This supersedes the original design's read-back/visibility/file checks and its incomplete-verification failure condition. Earlier document-check results remain historical; future producer evaluations must use the revised completion criterion.

The subsequent request to address valid findings authorized the document amendments for outgoing-content checks, provider invocation metadata, targeted terminology cleanup, concrete evaluation setup and a bounded artifact-usability exercise. F1 remains withdrawn; F6's two-file trade-off is documented, and F7 does not require a task split with the now-bounded fixture support. These are implementation requirements, not claims that the skill or evaluations already exist.

## Task 2: Verify, document and review the complete feature

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Verification](implementation.md#verification), [Acceptance](design.md#acceptance-and-evidence-limits)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the five producer scenarios on canonical and generated instructions plus the success cases' fresh-session legs. Use actual prior turns and the isolated `gh` substitute. Record credential exclusion, provider-policy behavior, artifact usability, attempted indexing, partial publication and unavailable execution under the implementation plan's bounded evidence rules.
- [ ] 2.2 Complete the applicable `make plugin-graph`, `make docs-build` and generated-freshness checks. Reuse Task 1's successful generator/structure results unless changes or failures justify repeating them; preserve all required repository/release gates.
- [ ] 2.3 Invoke `/kk:document` to reconcile the user-facing workflow and inventories with the implemented behavior. Explain secret visibility, explicit loading and the prohibition on handoff indexing.
- [ ] 2.4 Invoke `/kk:review-code` with Markdown/agent-skill context and `/kk:review-spec` for `docs/feat/wip/handoff/`. Address material findings and record any remaining issue, its reason and concrete next action durably.
- [ ] 2.5 Assess completion using the evidence: faithful and usable continuation, manual-only invocation, credential-free payloads, correct two-file secret-gist submission and completion on successful `gh` responses, no post-publication inspection, no unintended worktree changes or overwritten snapshots, truthful failure states and no handoff-initiated indexing/archival. Distinguish material failures from prose-quality observations and coverage limits.
- [ ] 2.6 Once implementation and its applicable checks/reviews are complete, move the feature documents to `docs/feat/done/handoff/` and update affected references and status. Do not mark the feature complete merely because design documents exist.

### Verification record

Task 1's deterministic stub, generated-output, metadata, structure, graph, strict docs and freshness checks are recorded in its Execution context above. Producer/consumer behavioral evaluations and real-host invocation-policy execution remain pending Task 2; authored scenarios are not evidence that those behaviors passed. Design-document checks below are historical and separate from implementation verification.

Historical design-only verification on 2026-10-28 checked all 18 then-existing local document links, including heading targets, and trailing whitespace successfully. The user subsequently supplied an independent review and discussed the findings; those dispositions are now reflected in these documents. The feature documents are excluded from the rendered site by `mkdocs.yml`'s `feat/**` rule. No site build, implementation suite or behavioral run has been performed for these documentation changes.

After the review amendments, all 38 local links (including heading targets) across the three feature documents and the corroboration report passed validation; whitespace and diff checks also passed. This establishes document consistency, not implementation or runtime behavior.

A fresh read of all documents against revision `7e2224eb` clarified two remaining evaluation details: the invented credential is presented as authentication material rather than a publishable example, and the consumer exercise uses the existing CLI stub's named-file read rather than an unspecified endpoint. The plan also separates local cleanup failure from successful publication. These clarifications add no production retrieval or post-publication verification.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
