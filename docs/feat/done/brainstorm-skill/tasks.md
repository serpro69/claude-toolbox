# Tasks: Brainstorm skill

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Review resolutions: [review-findings.md](review-findings.md)
> Status: done
> Created: 2026-10-03
> Not Doing: persistent state, output artifacts, implementation or automatic handoff, nontechnical topics, shared interview procedure, changes to neighboring workflow gates/outputs, knowledge-store/session-vault search, automatic profiles, mandatory subagents, batching modes, new eval runner

## Task 1: Deliver the core conversation and closing recap

- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Complete conversational path](implementation.md#complete-conversational-path), [Manual runbook contract](implementation.md#manual-runbook-contract), [Interaction contract](design.md#interaction-contract)
- **Verification:** [Task 1 evidence](verification/task-1/README.md) — six accepted runs; two invalid originals retained; source review and final evidence audit approved.

### Subtasks

- [x] 1.1 Relocate `design/frameworks.md` and `design/refinement-criteria.md` to `_shared/ideation-frameworks.md` and `_shared/idea-refinement-criteria.md`, preserving exact content and attribution. → verify: no editorial differences from their pre-change contents.
- [x] 1.2 Add the two shared-reference symlinks to `skills/design/` and `skills/brainstorm/`; update `design/SKILL.md` and `design/idea-process.md` links and anchors. → verify: relative targets resolve, stale operative references are absent, and the existing design procedure is unchanged.
- [x] 1.3 Create `klaude-plugin/skills/brainstorm/SKILL.md` with its trigger-first description and complete ordered workflow: adaptive depth, technical audience, one question at a time, targeted file/web research, challenge, revision, and chat closure. Keep ordinary user overrides implicit. Exclude knowledge-store/session-vault searches and persistence. → verify: description budget checked, instructions load before subject matter, and content-read instructions occur once.
- [x] 1.4 Sharpen `/kk:design`'s description and Ideas and Prototypes example around written planning. If scenario 1 demonstrates a collision with `/kk:model`, allow a minimal discovery-description change there too. Preserve all neighboring procedures and gates. → verify: scenario 1 selects brainstorming from the competing catalog; record any discovery edits with the relevant routing evidence.
- [x] 1.5 Make the closing recap distinguish settled decisions, rationale, and open assumptions. Retain optional user-directed transition to `/kk:design` without waiving its confirmations. Include the pinned inspiration attribution. → verify: completion and early-stop transcripts remain truthful and do not initiate another workflow.
- [x] 1.6 Register `brainstorm` in `test/test-plugin-structure.sh`, assert the two consumers' shared-reference symlinks, and generate Codex output. Leave command/profile-consumer lists unchanged. → verify: plugin/Codex structure checks, `make plugin-graph`, and generation stability pass.
- [x] 1.7 Add `brainstorm/evals/README.md` and scenarios 1, 5, and 7 with evaluator-only `oracle/runbook.md` files using the fixed contract. → verify: fixture links, reply IDs/conditions, turn limits, stop rules, and assertion mappings are complete; no oracle is staged.
- [x] 1.8 Execute those three scenarios against canonical and generated instructions. → verify: record six runs with exact prompts/replies, catalog and instruction hashes, traces, file state, and assertion verdicts; missing executions remain pending.

Size M covers the core workflow and three baseline scenarios. Moves, symlinks, and generated copies are mechanical; designing and executing the scenarios is substantive work included in this task's size.

## Task 2: Verify evidence gathering and revised decisions

- **Status:** done
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Scenario matrix](implementation.md#scenario-matrix), [Research facts](design.md#research-facts), [Interview and challenge](design.md#interview-and-challenge)
- **Verification:** [Task 2 evidence](verification/task-2/README.md) — eight accepted runs, 44 passing assertions, stable generation, and independent source/evidence review approved; no operative instruction changes or Task 1 reruns needed.

### Subtasks

- [x] 2.1 Author scenarios 2, 3, 4, and 6 with their fixtures and fixed-format runbooks: architecture audience, discoverable project fact, changed premise, and unavailable evidence. → verify: each assertion observes a concrete decision, read, revision, or uncertainty rather than merely restating instructions.
- [x] 2.2 Execute all four scenarios against canonical and generated instructions; fix any research or interview defects in `brainstorm/SKILL.md` and regenerate. → verify: record eight runs, including preservation of unrelated settled decisions, honest unavailable evidence, and the absence of writes or knowledge-store searches.
- [x] 2.3 Rerun affected Task 1 cases after instruction changes and retain all original traces. → verify: no operative instructions changed, so no earlier case requires rerunning; Task 1 instructions, scenarios, and evidence remain byte-identical.

Size M is bounded to four evidence/revision behaviors and their manual verification. It does not include competing-producer routing or documentation.

## Task 3: Verify competing-skill selection and design compatibility

- **Status:** done
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Entry and instruction loading](design.md#entry-and-instruction-loading), [Behavioral evaluations](implementation.md#behavioral-evaluations)
- **Verification:** [Task 3 evidence](verification/task-3/README.md) — all 18 current pairs and 74 assertions pass after the approved confirmation-enforcement fix. Forty-four attempts are retained, including the original failure. Structural checks pass and [independent review approved](verification/task-3/enforcement-review.md).

### Subtasks

- [x] 3.1 Author scenarios 8–12 with `brainstorm`, `design`, `model`, and `implement` available: direct implementation, implicit written planning, nontechnical non-trigger, explicit design invocation, and implicit domain-kit creation. → verified: ordinary routing prompts name no skill; scenario 11 alone covers explicit invocation; bodies are not preloaded in routing tests.
- [x] 3.2 Run those five scenarios in both variants, supplying the scripted confirmations needed to reach the requested producer outputs. → verified: all ten current runs pass actual selection, output boundaries and confirmations. The canonical scenario 9 failure is preserved and resolved by the approved fix and fresh executions in 3.6.
- [x] 3.3 Resolve routing collisions through the scoped discovery wording in `/kk:brainstorm`, `/kk:design`, and, when demonstrated, `/kk:model`; regenerate after changes. → verified: no selection collisions or discovery edits occurred. Scenario 1 and earlier brainstorm inputs remain unchanged. The separately approved operative enforcement fix is covered by 3.6 and its affected design reruns.
- [x] 3.4 Prepare evaluator-only `oracle/runbook.md` files for the existing `/kk:design` scenarios `hard-gate-enforcement`, `proportional-diverge-routing`, `wip-feature-no-subphases`, and `clarity-after-drafting`. Apply the shared runbook contract and cover these legacy runs in `brainstorm/evals/README.md`. Specify explicit design selection, canonical/generated handling, fixture-to-workspace mappings, permitted writes, bounded replies, and termination. → verified: runbooks prepared and original prompts, assertions, and fixture contents unchanged.
- [x] 3.5 Execute those four existing regressions against canonical and generated instructions using their prepared runbooks. → verified: eight current runs pass. Review found a WIP runbook coverage gap; bounded policy replies and an explicit refinement/handoff stopping condition resolved it in fresh runs. The original partial attempts remain recorded, and original prompts, assertions and fixtures remain unchanged.
- [x] 3.6 Approved scope extension: enforce existing `/kk:design` foundation and classification confirmations while preserving prior approvals and WIP routing. → verified: all twelve affected reruns and their 56 assertions pass; original failure retained; full shell suite, generation stability and graph validation pass; independent enforcement review approved with no findings.

Size M covers five routing scenarios plus bounded runbook preparation and execution for four existing regressions; the existing regression fixtures and assertions are reused. The manual preparation/execution workload is explicit, not a mechanical fixture update. Tasks are sequenced because fixes may touch the same entry points.

## Task 4: Final documentation and verification

- **Status:** done
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Documentation and final verification](implementation.md#documentation-and-final-verification), [Evaluation and acceptance](design.md#evaluation-and-acceptance)
- **Verification:** [Final evidence](verification/task-4/README.md) — nine documentation pages updated; 15-skill counts reconciled; 32 accepted pairs and 146 passing assertions remain applicable; full shell suite, generation stability and graph validation pass; independent code/spec reviews approved without findings.

### Subtasks

- [x] 4.1 Use `/kk:document` to update `docs/user-guide/skills.md`, `README.md`, `klaude-plugin/README.md`, the hand-authored `kodex-plugin/README.md`, and `docs/getting-started/quickstart.md`. → verify: brainstorming is optional, output is chat-only, and the Codex README uses its invocation spelling.
- [x] 4.2 Reconcile all live skill counts listed in the implementation plan to 15 after the skill exists, including the Codex README's stale count of 10. → verify: counts agree with canonical/generated catalogs and `EXPECTED_SKILLS`; generation preserves the README edit; frozen history remains untouched.
- [x] 4.3 Use `/kk:test` for the full shell suite, generator checks, plugin-graph validation, and the recorded behavioral evidence. Reuse valid earlier results where inputs have not changed. → verify: the baseline 32 scenario/variant runs and any required reruns are accounted for; missing or invalid runs remain explicit and prevent completion of their verification tasks.
- [x] 4.4 Use `/kk:review-code` for the Markdown skill instructions and shell structure changes. → verify: findings are fixed or durably recorded with a concrete next step.
- [x] 4.5 Use `/kk:review-spec` against this feature's design, implementation plan, and full implementation. → verify: accepted behavior, scope boundaries, and implementation agree; required pending work is not marked complete.

## Dependency Graph

```text
Task 1 (core) -> Task 2 (evidence) -> Task 3 (routing) -> Task 4 (final checks)
```
