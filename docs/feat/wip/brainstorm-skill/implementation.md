# Implementing the brainstorm skill

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: Tasks 1–2 implemented; Tasks 3–4 pending
> Review resolutions: [review-findings.md](review-findings.md)

## Repository context

Author skill instructions in `klaude-plugin/`, the source of truth. `make generate-kodex` regenerates Codex skills, profiles, plugin metadata, and `.codex/agents/`; do not hand-edit those outputs. The top-level `kodex-plugin/README.md` is hand-authored and is not rewritten by the generator. Follow the supplied `AGENTS.md` and [plugin authoring conventions](../../../contributing/plugin-development.md). Plugin instructions must be self-contained and must not link back to these feature documents.

This is a Markdown workflow change with shell-based structure checks. It needs no runtime dependency, new agent, command variant, profile, or generator change. Four tasks separate the core interview, evidence and revision behavior, competing-skill routing, and final documentation. Eval design and manual execution are substantive work, not mechanical consequences of registration or generation.

## Complete conversational path

### Share the reasoning references

1. Move `klaude-plugin/skills/design/frameworks.md` to `klaude-plugin/skills/_shared/ideation-frameworks.md`, and `design/refinement-criteria.md` to `_shared/idea-refinement-criteria.md`. Preserve their contents, headings, copyright notices, and pinned source comments. → verify: compare each moved file with its pre-change contents; the relocation has no editorial diff.
2. Create `shared-ideation-frameworks.md` and `shared-idea-refinement-criteria.md` symlinks in both `skills/design/` and the new `skills/brainstorm/`, targeting the corresponding `../_shared/` files. → verify: each is a symlink, has the expected relative target, and resolves to the shared source.
3. Update all references in `design/SKILL.md` and `design/idea-process.md`, including the HMW heading anchor. Preserve mandatory ordering and the existing procedure. Do not retain duplicate private copies under the old names. → verify: this relocation contributes only link/name changes; search for stale operative references and run `make plugin-graph` after the new skill exists. Discovery-wording changes are specified separately below.

### Author the skill

4. Create `klaude-plugin/skills/brainstorm/SKILL.md` with `name: brainstorm` and a short, trigger-first description covering technical idea refinement through an interview, with chat-only output. Distinguish it from implementation, written-design, and durable domain-kit requests. Sharpen `design/SKILL.md`'s description and Ideas and Prototypes example to advertise written planning. Allow minimal `model/SKILL.md` description changes only when routing evidence requires them; retain all neighboring workflow gates and outputs. Check the current [Claude Code description guidance](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) before touching any description. → verify: each edited description meets the documented cap and the repository's 1,024-character portability target; the implicit-selection scenarios pass with competing skills exposed.
5. Put the full concise workflow in `SKILL.md`: load the two shared references, establish the current decision from available context, interview using dependencies and relevant reasoning lenses, research facts, then converge and recap. Place the mandatory instruction-order directive at the start of Workflow. → verify: a trace shows both references loaded before subject-matter research or refinement; content-read instructions occur once in the workflow.
6. Express the accepted behavior from [the interaction contract](design.md#interaction-contract) without adding a state schema, modes, numerical question budgets, a mandatory questionnaire, or a batching exception protocol. Include constructive challenge, useful recommendations, revision of affected decisions, and honest unresolved assumptions. → verify: staged loose-idea, architecture, and changed-premise scenarios meet their assertions.
7. State the read-only research and conversation-only output boundary. Research uses project files and web sources; knowledge-store/session-vault search and indexing are excluded. Do not load `/kk:design` as a procedure, add the Capy protocol, activate profiles, or require subagents. Make the closing recap distinguish settled decisions and open assumptions without instructing the next workflow to skip its confirmations. Include a brief pinned attribution link to the external inspiration. → verify: inspect the instruction graph and scenario traces for unintended searches, workflows, or deliberate writes; assess recap content without claiming to control the follow-on workflow.

### Register and generate

8. Add `brainstorm` to `EXPECTED_SKILLS` in `test/test-plugin-structure.sh`. Add focused structural assertions that both consumers' new links resolve to the two shared sources. Do not change `EXPECTED_COMMANDS` or `PROFILE_DETECTION_CONSUMERS`; this feature adds neither a command wrapper nor a profile consumer. → verify: `bash test/test-plugin-structure.sh` passes after generation.
9. Run `make generate-kodex` and inspect generated changes for the new skill, moved references, updated design links, and `/kk:` to `$kk:` transformations. The current generator clears generated skill output before rebuilding it, so obsolete private filenames should disappear. → verify: no stale generated reference paths remain; rerunning generation produces identical output and `bash test/test-codex-structure.sh` passes.

## Behavioral evaluations

Author self-contained scenarios under `klaude-plugin/skills/brainstorm/evals/<name>/eval.json`, following the repository schema: numeric `id`, matching `name`, `description`, `skills`, natural `prompt`, explicit `trap`, `files`, and numbered assertions. Use bare skill names in `skills` arrays. A routing prompt uses ordinary natural language unless the scenario explicitly tests invocation syntax.

The competing catalog is `brainstorm`, `design`, `model`, and `implement`. Scenarios 1 and 8–12 expose all four descriptions and provide their normal loading paths, without preloading a skill body or telling the tested agent which skill to select. Scenarios 2–7 test interview behavior with `brainstorm` selected explicitly; they do not count as implicit-selection evidence. Scenario 11 retains an explicit `/kk:design` invocation as a separate regression, not as evidence for description-based selection. Use the generated invocation spelling in that case when testing Codex.

Provide filesystem inputs under each scenario's `test-files/`. Oracles and evaluator-only runbooks belong under its sibling `oracle/`, never under `test-files/`. `files: []` is appropriate when the idea needs no project context. Stage fixtures as an isolated workspace outside any `SKILL.md` ancestor; do not evaluate fixtures in place under the hosting skill. Do not expose `eval.json`, the oracle directory, or the evaluator README to the tested agent.

### Manual runbook contract

Create `klaude-plugin/skills/brainstorm/evals/README.md` as the shared evaluator guide, following the isolation and evidence conventions in the [clarify-docs eval guide](../../../../klaude-plugin/skills/clarify-docs/evals/README.md). The new README must state the contract below in full and remain self-contained within the plugin. This is a new manual runbook convention; it needs neither an automated runner nor changes to `eval.json`'s schema.

Every scenario has an evaluator-only `oracle/runbook.md` with these fixed sections:

| Section | Required contents |
| --- | --- |
| `## Setup` | Skill catalog or explicitly selected skill; canonical/generated variant; allowed fixture paths; tool availability; permitted writes; any synthetic source responses. These must agree with `eval.json`. |
| `## Start` | Send `eval.json.prompt` exactly once. State any mechanical invocation-spelling conversion for the generated variant; never add the expected skill or answer to a natural-language routing prompt. |
| `## Replies` | An ordered table with columns `ID`, `Send when`, and `Exact user reply`. IDs are unique. Each condition names an observable topic or event in the latest assistant response; each reply supplies user facts or choices, not grading guidance. Send at most one row after a response, mark it consumed, and never resend it. If multiple unused rows match, take the first matching row. An empty table is allowed for a single-turn scenario. |
| `## Stop` | A positive integer `Max assistant turns` counting the initial response; an observable completion condition; any expected early-stop condition. Check completion first. If more user input is needed but no reply row matches, stop as `off-script`; at the bound, stop as `turn-limit`. Do not improvise answers or silently extend the bound. |
| `## Grade` | Map each assertion ID to response, file-state, or tool-trace evidence. Grade PASS/FAIL/PARTIAL. Assertions not reached or not observable are PARTIAL, never inferred passes. |

Keep future replies hidden from the tested agent, delivering only the chosen user reply at each step. These evaluator turn bounds do not impose a question budget on the skill. An off-script run can expose an incomplete test script rather than a skill defect: preserve the trace, repair the runbook explicitly if warranted, and rerun; never convert the interrupted run into a pass. Tool/harness failures are recorded separately as unavailable execution.

Capture the exact submitted prompts and replies, skill/fixture hashes, supplied catalog, provider/model settings, complete tool trace, final file state, run termination reason, and assertion verdicts. The normal skill-loading trace establishes selection; the subsequent transcript and file state establish the conversation/artifact boundary. A run with oracle access or an incomplete trace is invalid. A harness that cannot expose competing descriptions and record actual loading cannot certify implicit routing; record those runs as unavailable rather than substituting a skill-name classification question.

### Scenario matrix

| ID | Directory | Essential fixture and assertions |
| --- | --- | --- |
| 1 | `loose-technical-idea` | Natural-language prompt such as "Help me think through whether a local cache is worth adding to our developer tool; I want to explore the trade-offs." Name no skill. With the competing catalog, assert `/kk:brainstorm` selection, instruction loading, adaptive follow-ups, and a decision-ready chat recap without artifacts. |
| 2 | `architecture-audience` | An architect comparing operational approaches. Assert relevant technical trade-offs and no forced developer persona, market differentiation, or implementation-ready specification. |
| 3 | `discoverable-project-fact` | A small local config or document containing a fact needed for the decision. Assert the agent reads it instead of asking the user to repeat it, and separates the fact from the preference decision. |
| 4 | `changed-premise` | An evaluator reply revises a constraint after a provisional direction is discussed. Assert affected conclusions are revisited and unrelated decisions are preserved. |
| 5 | `no-repository` | A self-contained technical question in an otherwise empty workspace. Assert useful progress without requiring project files, creating setup files, or conducting a broad filesystem search. |
| 6 | `unavailable-evidence` | A question depends on an explicitly unavailable document or service. Assert an explicit uncertainty, no fabricated evidence, and no definite downstream recommendation based on the missing fact. |
| 7 | `early-stop` | An evaluator reply ends the interview while an assumption is unresolved. Assert a truthful partial recap, no further interrogation, no readiness claim, and no writes or automatic handoff. |
| 8 | `direct-implementation-request` | A small editable fixture and a direct implementation request, with neighboring skills available. Assert `/kk:brainstorm` is not selected implicitly and does not intercept the task. |
| 9 | `written-design-request` | Natural-language prompt such as "Write a design document, implementation plan, and task list for adding an archive command." Name no skill. With the competing catalog, assert `/kk:design` selection. Script the required confirmations through its existing gates; assert the requested artifacts are produced rather than only a chat recap. |
| 10 | `nontechnical-non-trigger` | An unrelated nontechnical brainstorming request with the skill catalog available. Assert `/kk:brainstorm` is not selected implicitly; ordinary assistant behavior remains available. |
| 11 | `explicit-design-invocation` | Explicit `/kk:design` request with the competing catalog. Preserve user-directed invocation, existing gates, and artifact behavior. This is an invocation regression and is not counted as implicit routing coverage. |
| 12 | `domain-kit-request` | Natural-language request to create a durable domain glossary and divergences/traps pages for a named bounded context. With the competing catalog, assert `/kk:model` selection and its kit-producing workflow rather than a brainstorm recap. |

Across positive brainstorm scenarios, inspect tool traces for no deliberate file writes, saved interview artifacts, knowledge-store/session-vault searches, memory indexing, implementation, or external mutations. This prohibition applies to the brainstorm workflow; it does not apply to the neighboring workflow selected in a negative routing scenario. In scenarios 9, 11, and 12, fixture-scoped artifact writes are expected and permitted; the evaluator supplies the confirmations those workflows require. Include an internal architecture example so the shared product-oriented rubric is tested for relevance rather than blindly applied.

Author and stage the scenarios → verify: every assertion has observable transcript or tool-trace evidence; every listed fixture exists; every runbook follows the fixed sections and reply-table columns; no oracle is staged. Run all twelve scenarios against canonical instructions and representative generated Codex instructions. In particular, implicit scenarios 1 and 9 must exercise actual competing-skill selection in both variants. If an execution environment is unavailable, record exactly which scenario/variant pairs were not run and the procedure needed to finish; keep their verification tasks pending. Authored evals are not passed evals.

After relocating references, rerun `/kk:design`'s existing `hard-gate-enforcement`, `proportional-diverge-routing`, `wip-feature-no-subphases`, and `clarity-after-drafting` scenarios. These exercise the entry paths and artifact behavior whose instructions must remain unchanged. Do not rewrite their prompts or assertions to accommodate a regression.

Task 3 must prepare these legacy runs as well as execute them. Add an evaluator-only `oracle/runbook.md` to each of the four existing `design/evals/<scenario>/` directories, using the same fixed sections and bounded-reply contract. Explicitly select the design workflow for these behavior regressions; they are not new implicit-routing tests. Specify variant handling, allowed writes, and the mapping from declared source fixtures to the workspace locations the original prompt expects. Keep existing oracle files grader-only. Supply scripted foundation/classification confirmations where needed and an empty reply table where a scenario needs no follow-up. Preserve the original prompts, assertions, and fixture contents; record staging mappings instead of changing the scenario to fit a convenient workspace. The new evaluator README must cover these regression runs too.

The baseline acceptance matrix is sixteen scenarios in each of two variants: twelve brainstorm scenarios plus four existing design regressions, for 32 runs before any necessary reruns. Task 1 owns scenarios 1, 5, and 7 plus the common runbook guide; Task 2 owns 2, 3, 4, and 6; Task 3 owns authoring/execution of 8–12 and runbook preparation/execution for the four design regressions. If Task 3 changes discovery wording, rerun scenario 1 in both variants. Any other instruction changes require rerunning affected earlier cases. This is substantive manual verification, split by user-facing behavior rather than hidden inside a single implementation task.

## Documentation and final verification

10. Update the skill catalog in `docs/user-guide/skills.md` with the technical audience, adaptive interview, chat-only output, and optional transition to `/kk:design`. Add the distinction to `README.md`, `klaude-plugin/README.md`, `kodex-plugin/README.md`, and the getting-started quickstart without making brainstorming a required pipeline stage. Use the Codex invocation spelling in its README. → verify: a reader can choose between conversation and written planning before invoking either skill.
11. After the skill exists, reconcile live skill counts to 15 in those three READMEs, `docs/user-guide/skills.md`, `docs/getting-started/{index,overview,plugin-only}.md`, and `docs/contributing/architecture.md`. Most currently say 14; the hand-authored `kodex-plugin/README.md` currently says 10, so a blind 14-to-15 replacement would miss it. Preserve frozen `docs/feat/done/` content and unrelated documentation. → verify: a targeted search finds no stale counts in those live pages; the count agrees with the actual canonical/generated catalogs and `EXPECTED_SKILLS`; generation preserves the Codex README edit.
12. Run the required checks: the full shell suite (`for test_script in test/test-*.sh; do "$test_script" || exit; done`), `make generate-kodex`, and `make plugin-graph`. Confirm generation is stable by comparing generated output before and after a second run; an ordinary diff against HEAD is expected to contain the feature's generated changes until committed. → verify: record actual exit results and investigate every failure without weakening assertions.
13. Use `/kk:test`, `/kk:document`, `/kk:review-code` with Markdown skill instructions and shell checks as the review scope, and `/kk:review-spec` against these documents. → verify: review findings are resolved or recorded durably with the issue, reason for deferral, and concrete next step; task state reflects actual completion.

Record execution evidence with the feature tasks or in a linked verification note under this feature directory. Do not add review claims before those reviews run. No implementation or evaluation has run as part of writing this plan.
