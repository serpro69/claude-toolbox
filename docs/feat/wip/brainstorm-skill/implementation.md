# Implementing the brainstorm skill

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: planned; no skill implementation has been made

## Repository context

Author skill instructions in `klaude-plugin/`, the source of truth. `make generate-kodex` regenerates `kodex-plugin/` and `.codex/agents/`; do not hand-edit those outputs. Follow the supplied `AGENTS.md` and [plugin authoring conventions](../../../contributing/plugin-development.md). Plugin instructions must be self-contained and must not link back to these feature documents.

This is a Markdown workflow change with shell-based structure checks. It needs no runtime dependency, new agent, command variant, profile, or generator change. The two implementation tasks are a complete usable skill followed by final documentation and verification. The first task is one cohesive behavior change; relocations, registrations, generated files, and fixtures are mechanical consequences of it.

## Complete conversational path

### Share the reasoning references

1. Move `klaude-plugin/skills/design/frameworks.md` to `klaude-plugin/skills/_shared/ideation-frameworks.md`, and `design/refinement-criteria.md` to `_shared/idea-refinement-criteria.md`. Preserve their contents, headings, copyright notices, and pinned source comments. → verify: compare each moved file with its pre-change contents; the relocation has no editorial diff.
2. Create `shared-ideation-frameworks.md` and `shared-idea-refinement-criteria.md` symlinks in both `skills/design/` and the new `skills/brainstorm/`, targeting the corresponding `../_shared/` files. → verify: each is a symlink, has the expected relative target, and resolves to the shared source.
3. Update all references in `design/SKILL.md` and `design/idea-process.md`, including the HMW heading anchor. Preserve mandatory ordering and all existing behavior. Do not retain duplicate private copies under the old names. → verify: inspect the diff for link/name changes only; search the operative design files for stale reference names and run `make plugin-graph` after the new skill exists.

### Author the skill

4. Create `klaude-plugin/skills/brainstorm/SKILL.md` with `name: brainstorm` and a short, trigger-first description covering technical idea refinement through an interview, with chat-only output. Distinguish it from direct implementation and written-design requests. Check the current [Claude Code description guidance](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) before authoring the description, as the repository requires. → verify: description stays within the documented cap and the repository's 1,024-character portability target; trigger scenarios distinguish neighboring skills.
5. Put the full concise workflow in `SKILL.md`: load the two shared references, establish the current decision from available context, interview using dependencies and relevant reasoning lenses, research facts, then converge and recap. Place the mandatory instruction-order directive at the start of Workflow. → verify: a trace shows both references loaded before subject-matter research or refinement; content-read instructions occur once in the workflow.
6. Express the accepted behavior from [the interaction contract](design.md#interaction-contract) without adding a state schema, modes, numerical question budgets, a mandatory questionnaire, or a batching exception protocol. Include constructive challenge, useful recommendations, revision of affected decisions, and honest unresolved assumptions. → verify: staged loose-idea, architecture, and changed-premise scenarios meet their assertions.
7. State the read-only research and conversation-only output boundary. Do not load `/kk:design` as a procedure, import its persistence steps, add Capy indexing, activate profiles, or require subagents. Include a brief pinned attribution link to the external inspiration in the skill; write the interview instructions for this feature. → verify: inspect the instruction graph and scenario tool traces for unintended workflows or deliberate writes.

### Register and generate

8. Add `brainstorm` to `EXPECTED_SKILLS` in `test/test-plugin-structure.sh`. Add focused structural assertions that both consumers' new links resolve to the two shared sources. Do not change `EXPECTED_COMMANDS` or `PROFILE_DETECTION_CONSUMERS`; this feature adds neither a command wrapper nor a profile consumer. → verify: `bash test/test-plugin-structure.sh` passes after generation.
9. Run `make generate-kodex` and inspect generated changes for the new skill, moved references, updated design links, and `/kk:` to `$kk:` transformations. The current generator clears generated skill output before rebuilding it, so obsolete private filenames should disappear. → verify: no stale generated reference paths remain; rerunning generation produces identical output and `bash test/test-codex-structure.sh` passes.

## Behavioral evaluations

Author self-contained scenarios under `klaude-plugin/skills/brainstorm/evals/<name>/eval.json`, following the repository schema: numeric `id`, matching `name`, `description`, `skills`, natural `prompt`, explicit `trap`, `files`, and numbered assertions. Use bare skill names in `skills` arrays and `/kk:` invocation spelling in canonical prompts. Scenarios 1–7 and 10 supply `brainstorm`; scenario 8 supplies `brainstorm` and `implement`; scenario 9 supplies `brainstorm` and `design`. Trigger tests expose the descriptions for selection rather than pre-invoking the brainstorm procedure.

Provide filesystem inputs under each scenario's `test-files/`. Oracles and evaluator-only reply scripts belong under its sibling `oracle/`, never under `test-files/`. `files: []` is appropriate when the idea needs no project context. Stage fixtures as an isolated workspace outside any `SKILL.md` ancestor; do not evaluate fixtures in place under the hosting skill.

Multi-turn scenarios need a short evaluator runbook stating the next user reply and the condition under which it is sent. The evaluator sends only the relevant reply at each turn; it must not expose future answers or expected behavior to the tested agent. No new runner or schema extension is required.

| ID | Directory | Essential fixture and assertions |
| --- | --- | --- |
| 1 | `loose-technical-idea` | A short initial idea; evaluator replies establish the next decision and constraints. Assert instruction loading, one meaningful question per turn, adaptive follow-ups, and a decision-ready chat recap. |
| 2 | `architecture-audience` | An architect comparing operational approaches. Assert relevant technical trade-offs and no forced developer persona, market differentiation, or implementation-ready specification. |
| 3 | `discoverable-project-fact` | A small local config or document containing a fact needed for the decision. Assert the agent reads it instead of asking the user to repeat it, and separates the fact from the preference decision. |
| 4 | `changed-premise` | An evaluator reply revises a constraint after a provisional direction is discussed. Assert affected conclusions are revisited and unrelated decisions are preserved. |
| 5 | `no-repository` | A self-contained technical question in an otherwise empty workspace. Assert useful progress without requiring project files, creating setup files, or conducting a broad filesystem search. |
| 6 | `unavailable-evidence` | A question depends on an explicitly unavailable document or service. Assert an explicit uncertainty, no fabricated evidence, and no definite downstream recommendation based on the missing fact. |
| 7 | `early-stop` | An evaluator reply ends the interview while an assumption is unresolved. Assert a truthful partial recap, no further interrogation, no readiness claim, and no writes or automatic handoff. |
| 8 | `direct-implementation-request` | A small editable fixture and a direct implementation request, with neighboring skills available. Assert `/kk:brainstorm` is not selected implicitly and does not intercept the task. |
| 9 | `written-design-request` | An explicit `/kk:design` request with both skills available. Assert the request routes to the artifact-producing design workflow, not chat-only brainstorming. |
| 10 | `nontechnical-non-trigger` | An unrelated nontechnical brainstorming request with the skill catalog available. Assert `/kk:brainstorm` is not selected implicitly; ordinary assistant behavior remains available. |

Across positive brainstorm scenarios, inspect tool traces for no deliberate file writes, saved interview artifacts, memory indexing, implementation, or external mutations. This prohibition applies to the brainstorm workflow; it does not apply to the neighboring workflow selected in a negative routing scenario. Include an internal architecture example so the shared product-oriented rubric is tested for relevance rather than blindly applied.

Author and stage the scenarios → verify: every assertion has observable transcript or tool-trace evidence; every listed fixture exists; no oracle is staged. Run them against the canonical skill and representative generated Codex output, recording provider, supplied skills, scenario, assertion verdicts, and evidence. If an execution environment is unavailable, record exactly which scenarios were not run and the command or manual procedure needed to finish; do not label authored evals as passed evals.

After relocating references, rerun `/kk:design`'s existing `hard-gate-enforcement`, `proportional-diverge-routing`, `wip-feature-no-subphases`, and `clarity-after-drafting` scenarios. These exercise the entry paths and artifact behavior whose instructions must remain unchanged. Do not rewrite their assertions to accommodate a regression.

## Documentation and final verification

10. Update the skill catalog in `docs/user-guide/skills.md` with the technical audience, adaptive interview, chat-only output, and optional transition to `/kk:design`. Add the distinction to `README.md`, `klaude-plugin/README.md`, and the getting-started quickstart without making brainstorming a required pipeline stage. → verify: a reader can choose between conversation and written planning before invoking either skill.
11. Update live skill-count references from 14 to 15 in the two READMEs, `docs/user-guide/skills.md`, `docs/getting-started/{index,overview,plugin-only}.md`, and `docs/contributing/architecture.md`. Preserve frozen `docs/feat/done/` content and unrelated documentation. → verify: a targeted search of those live pages finds no stale skill counts; the new count agrees with the skill catalog and `EXPECTED_SKILLS`.
12. Run the required checks: the full shell suite (`for test_script in test/test-*.sh; do "$test_script" || exit; done`), `make generate-kodex`, and `make plugin-graph`. Confirm generation is stable by comparing generated output before and after a second run; an ordinary diff against HEAD is expected to contain the feature's generated changes until committed. → verify: record actual exit results and investigate every failure without weakening assertions.
13. Use `/kk:test`, `/kk:document`, `/kk:review-code` with Markdown skill instructions and shell checks as the review scope, and `/kk:review-spec` against these documents. → verify: review findings are resolved or recorded durably with the issue, reason for deferral, and concrete next step; task state reflects actual completion.

Record execution evidence with the feature tasks or in a linked verification note under this feature directory. Do not add review claims before those reviews run. No implementation or evaluation has run as part of writing this plan.
