# Tasks: Brainstorm skill

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: persistent state, output artifacts, implementation or automatic handoff, nontechnical topics, shared interview procedure, design behavior changes, automatic profiles, mandatory subagents, batching modes, new eval runner

## Task 1: Deliver the conversation-only technical interview

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Complete conversational path](implementation.md#complete-conversational-path), [Behavioral evaluations](implementation.md#behavioral-evaluations), [Interaction contract](design.md#interaction-contract)

### Subtasks

- [ ] 1.1 Relocate `design/frameworks.md` and `design/refinement-criteria.md` to `_shared/ideation-frameworks.md` and `_shared/idea-refinement-criteria.md`, preserving exact content and attribution. → verify: no editorial differences from their pre-change contents.
- [ ] 1.2 Add `shared-ideation-frameworks.md` and `shared-idea-refinement-criteria.md` symlinks to both `skills/design/` and `skills/brainstorm/`; update `design/SKILL.md` and `design/idea-process.md` references and anchors. → verify: correct relative targets, resolving links, and no stale operative references or changes to design behavior.
- [ ] 1.3 Create `klaude-plugin/skills/brainstorm/SKILL.md` with a trigger-first description and the complete ordered workflow. Cover adaptive depth, a technical audience, one question at a time, useful challenge, targeted research, and chat closure. Keep ordinary user overrides implicit. → verify: current description-budget guidance checked; instructions load before subject matter; content-reading instructions appear once.
- [ ] 1.4 Include the conversation-only boundary and optional user-directed transition to `/kk:design`, without persistence, automatic handoffs, profile setup, or required delegation. Include the pinned inspiration attribution. → verify: the skill's reachable instructions do not import an artifact-writing or memory-indexing procedure.
- [ ] 1.5 Register `brainstorm` in `test/test-plugin-structure.sh` and assert the new shared-reference symlinks for both consumers. Leave command and profile-consumer lists unchanged. → verify: plugin structure checks pass after generation.
- [ ] 1.6 Add the ten scenarios specified in [Behavioral evaluations](implementation.md#behavioral-evaluations), with concrete assertions, local fixtures where needed, and evaluator-only multi-turn reply scripts outside `test-files/`. → verify: fixture references resolve, oracles are not staged, and positive and negative routing cases are distinct.
- [ ] 1.7 Run `make generate-kodex`; inspect new skill output, shared references, updated design links, and removed obsolete generated paths. → verify: `bash test/test-plugin-structure.sh`, `bash test/test-codex-structure.sh`, and `make plugin-graph` pass; a second generation is stable.
- [ ] 1.8 Execute the brainstorm scenarios and the four named `/kk:design` regressions against canonical instructions and representative generated output. → verify: record assertion-level transcript/tool evidence, including research, revised decisions, no deliberate writes, and unchanged design behavior. Record unavailable runs explicitly rather than marking them passed.

The size reflects one new workflow. Reference moves, symlinks, registrations, generated copies, and test fixtures are mechanical consequences rather than separate architectural changes.

## Task 2: Final documentation and verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Documentation and final verification](implementation.md#documentation-and-final-verification), [Evaluation and acceptance](design.md#evaluation-and-acceptance)

### Subtasks

- [ ] 2.1 Use `/kk:document` to update `docs/user-guide/skills.md`, the two READMEs, and `docs/getting-started/quickstart.md` with the new skill and the conversation-versus-written-design distinction. → verify: brainstorming is optional and its output is clearly chat-only.
- [ ] 2.2 Update the live skill counts listed in the implementation plan from 14 to 15. → verify: counts agree with `EXPECTED_SKILLS`; frozen history and unrelated pages remain untouched.
- [ ] 2.3 Use `/kk:test` for the full shell suite, generator checks, plugin-graph validation, and the recorded behavioral evaluation evidence. Reuse valid Task 1 results where the inputs have not changed. → verify: all required results are recorded, with missing runs or failures explicit.
- [ ] 2.4 Use `/kk:review-code` for the Markdown skill instructions and shell structure changes. → verify: findings are fixed or durably recorded with a concrete next step.
- [ ] 2.5 Use `/kk:review-spec` against this feature's design, implementation plan, and full implementation. → verify: accepted behavior, scope boundaries, and implementation agree; do not mark the feature complete while required work remains.

## Dependency Graph

```text
Task 1: complete interview path ──→ Task 2: documentation and final verification
```
