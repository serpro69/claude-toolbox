# Brainstorm skill

> Status: design agreed; implementation pending
> Created: 2026-10-03
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)

## Problem and outcome

Technical ideas often need a conversation before they need a written specification. `/kk:design` supports that conversation, but its workflow leads through formal checkpoints to design documents, an implementation plan, and tasks. Users need a separate entry point for refining an idea without committing to those outputs.

`/kk:brainstorm` interviews the user until the idea is clear enough for their next decision. Its audience includes developers, architects, and anyone else thinking through a technical topic. The topic boundary is technical; the user's job title is not a restriction. Architecture, infrastructure, technical products, tools, operations, and engineering workflows are valid subjects.

Success means the user can explain the idea, whether it is worth pursuing, the main trade-offs, the important unresolved assumptions, and their next decision. That decision can be to pursue, discard, narrow, or investigate the idea. An implementation-ready specification is not required.

This feature adds a skill. The documents in this directory describe how to build it; running the finished skill does not produce documents like these.

## Accepted decisions

| Concern | Decision |
| --- | --- |
| Audience | Anyone discussing a technical idea or decision; not restricted to developers |
| Depth | Adapt to the user's next decision |
| Rhythm | Ask one question at a time |
| Research | Read relevant project material and look up technical facts when useful |
| Persistence | Keep working context and output in the conversation |
| Reuse | Separate interview workflow; share ideation and evaluation references with `/kk:design` |
| Existing design behavior | Preserve `/kk:design`'s process, gates, outputs, and handoffs |

The skill needs no special batching mode or rules about when the user may override its rhythm. Ordinary user instructions already provide that flexibility.

## Research and provenance

The comparison used the current [design entry point](../../../../klaude-plugin/skills/design/SKILL.md), [fresh-idea process](../../../../klaude-plugin/skills/design/idea-process.md), and [WIP process](../../../../klaude-plugin/skills/design/existing-task-process.md).

The external inspiration is Matt Pocock's [grilling skill at commit `85f83d3`](https://github.com/mattpocock/skills/blob/85f83d3fde1d3a90d5c9a657f6998c79a6c37308/skills/productivity/grilling/SKILL.md), inspected on 2026-10-03. That revision orders questions by decision dependencies, groups ready questions into rounds, recommends answers, delegates fact-finding, and seeks confirmation after exhausting the decision tree. These are reference observations, not instructions to execute during this feature's development.

| Existing material | Adopt for `/kk:brainstorm` | Adaptation |
| --- | --- | --- |
| `/kk:design`: framing, alternatives, constraints, assumption audit | Keep these reasoning tools available | Select what advances the current decision; do not copy the mandatory interview checkpoints |
| `/kk:design`: ideation frameworks and refinement criteria | Share their existing content | Treat product-market questions and differentiation as context-dependent |
| Grilling: prerequisite-aware questions and revisiting the decision tree | Order questions using settled decisions; revisit affected decisions when premises change | Track this in the conversation without a formal schema or saved ledger |
| Grilling: distinguish researched facts from user decisions | Investigate discoverable facts and seek user judgment where needed | Use focused research; no mandatory subagent delegation |
| Grilling: recommendations alongside questions | Explain a recommendation when supported | Do not invent a recommendation for an open preference question |
| Grilling: batch the entire frontier and exhaust every branch | Do not adopt these defaults | Use one question at a time and stop at sufficient clarity for the next decision |

The new interview instructions will be written for this workflow, with a brief attribution link to the pinned inspiration. They will not vendor the grilling skill or load it at runtime. The two existing reasoning references retain their current upstream attribution and pinned source comments when moved.

## Interaction contract

### Entry and instruction loading

The description should lead with technical brainstorming and interviewing triggers. Requests to think through, explore, or pressure-test a technical idea should select the skill. Direct requests to implement, fix, or write a design document should continue to select the appropriate existing workflow. Unrelated nontechnical brainstorming is outside the skill's advertised scope.

The entry point states the purpose, conversation-only boundary, required reference reads, and complete interview workflow. Keep the procedure in `SKILL.md`; this small workflow does not need a second process file that restates the same steps.

Follow the repository's mandatory ordering: load `SKILL.md` and both shared reasoning references before researching project content or refining the idea. Put the instruction-before-action directive at the top of the Workflow section. Include the content-reading step once, after instruction loading. This skill does not invoke the profile-detection procedure or introduce a `brainstorm/` profile phase.

### Establish the current decision

Identify the idea and what the user needs to decide. Use information already supplied. Ask a framing question only when it would resolve a real ambiguity; do not require a ceremonial framing confirmation, persona questionnaire, or numerical success metric in every session.

A loose idea may need problem discovery. A specific architecture proposal may need its assumptions challenged immediately. Match vocabulary and explanatory detail to the user's understanding.

### Interview and challenge

Track settled decisions, assumptions, open questions, and their dependencies conversationally. Ask the highest-value question whose prerequisites are understood. Avoid asking downstream questions that require guessing an unresolved upstream answer. When an answer changes a premise, revisit the affected decisions.

Ask one question at a time. Prefer meaningful choices where they help, with a reasoned recommendation when evidence supports one. Use open questions when suggested answers would bias the discussion. Challenge contradictions and weak assumptions directly and constructively.

Draw on the shared references to explore alternatives, map constraints, examine failure scenarios, and audit assumptions. Select relevant lenses instead of running every framework. Do not force market differentiation or adoption questions onto an internal architecture or operational decision where they add no value.

### Research facts

Read relevant files, documentation, and external sources when evidence could change the advice. Research is targeted to the current uncertainty; neither a repository nor an initial repository-wide inspection is required.

Do not ask the user to supply a fact that available material can answer. Distinguish evidence, assumptions, recommendations, and user decisions. If evidence cannot be obtained, identify the uncertainty and explain whether it affects the current decision. Other useful questions can continue when they do not depend on that evidence.

The contract is read-only research. The skill creates no project files, saved notes, temporary interview artifacts, task records, knowledge-store entries, or external resource changes. It adds no memory or indexing integration. This describes the skill's intentional actions; it does not promise to disable the host application's transcript storage or tool infrastructure.

### Converge and close

Wrap up when the idea, rationale, meaningful trade-offs, material uncertainties, and next decision are clear enough for the user. Do not equate readiness with exhausting every possible branch. A blocking unknown may make targeted investigation the next decision instead of supporting a premature recommendation to build.

Give a concise recap in chat at a useful stopping point. Preserve unresolved assumptions and distinguish details that can wait from uncertainties that might change the direction. If the user stops early, reflect the actual state of the discussion without declaring an unfinished idea validated.

The skill may suggest `/kk:design` when written planning would help. It does not invoke that skill or begin implementation automatically. A later user request to write or build is a new workflow using the conversation as input. Do not reopen settled decisions merely because the workflow changes.

## Structure and reuse

The canonical implementation belongs in `klaude-plugin/`. `kodex-plugin/` remains generated.

| Path | Planned responsibility |
| --- | --- |
| `klaude-plugin/skills/brainstorm/SKILL.md` | Trigger, boundaries, ordered reference loading, interview, research, and closure |
| `klaude-plugin/skills/_shared/ideation-frameworks.md` | Existing contents of `design/frameworks.md`, relocated without editorial changes |
| `klaude-plugin/skills/_shared/idea-refinement-criteria.md` | Existing contents of `design/refinement-criteria.md`, relocated without editorial changes |
| `skills/{design,brainstorm}/shared-ideation-frameworks.md` | Per-skill symlink to `../_shared/ideation-frameworks.md` |
| `skills/{design,brainstorm}/shared-idea-refinement-criteria.md` | Per-skill symlink to `../_shared/idea-refinement-criteria.md` |
| `klaude-plugin/skills/design/{SKILL.md,idea-process.md}` | Update reference names and links, including heading anchors |
| `klaude-plugin/skills/brainstorm/evals/` | Behavioral and trigger-boundary scenarios |

The two `skills/` rows are relative to `klaude-plugin/`. Shared files keep the existing guidance; the caller selects relevant lenses and owns workflow order. Sharing references does not make `/kk:design` adaptive or introduce its artifact-writing procedure into `/kk:brainstorm`.

The existing generator includes all skill directories, resolves per-skill symlinks into generated files, and rewrites `/kk:` references for Codex. No new generator feature, agent, command wrapper, dependency, profile, or runtime integration is needed. Implementation must verify generation and link integrity rather than edit generated output directly.

## Evaluation and acceptance

Structure checks establish packaging correctness. Staged, multi-turn scenarios establish interview behavior; a green shell suite alone cannot prove those behaviors.

| Scenario | Evidence required |
| --- | --- |
| Loose technical idea | Instructions load first; the first question addresses a material uncertainty; subsequent questions respond to answers; one question per turn |
| Technical audience beyond developers | An architect's infrastructure decision receives relevant trade-off analysis without a developer-persona or product-market questionnaire |
| Discoverable project fact | The agent reads the supplied fixture to establish the fact, then asks for the user's decision instead of asking them to repeat the fact |
| Changed premise | A later answer changes an earlier constraint; affected conclusions are reopened while unrelated settled decisions remain intact |
| No repository | A self-contained technical idea progresses without requiring files or project setup |
| Unavailable evidence | The uncertainty remains explicit; dependent recommendations are qualified and unrelated discussion can proceed |
| Natural completion and early stop | The recap matches the agreed depth and actual state, including material unknowns; no automatic handoff or writes occur |
| Trigger boundaries | Direct implementation, explicit design-document, and unrelated nontechnical requests do not get diverted into this interview |
| `/kk:design` regression | Existing fresh-idea gates and WIP routing still behave as specified after the reference relocation |

Inspect tool traces as well as responses for the absence of deliberate writes and memory indexing. For complete scenarios, inspect the whole exchange rather than grading only the first answer. Evaluation definitions and staging details are specified in the implementation plan.

## Assumptions

- The existing reasoning references serve technical decisions beyond feature implementation when the caller omits irrelevant lenses. Validate with the architecture scenario.
- A bounded interview can preserve relevant decisions in conversation context without a separate persistence mechanism. Validate through a changed-premise scenario and describe unresolved state honestly at closure.
- Selective reference reuse can preserve `/kk:design` behavior. Validate with unchanged reference content, its existing evals, and generated-output checks.

## Not Doing

- **Persistent interview state or output artifacts:** the skill's result is a conversation and recap.
- **Implementation or automatic workflow handoff:** deciding to write or build belongs to a subsequent user instruction.
- **General nontechnical brainstorming:** the toolbox's topic boundary remains technical.
- **A shared interview procedure or changes to `/kk:design`'s behavior:** the two skills have different completion contracts.
- **Automatic profile activation:** the first version uses shared reasoning lenses and targeted research without profile setup prompts.
- **Mandatory subagents:** fact-finding does not require delegation infrastructure.
- **Special batching modes or override rules:** one-question guidance is sufficient; ordinary user steering needs no additional protocol.
- **A new evaluation runner:** use the repository's existing staged-scenario convention.

These are scope decisions, not promised follow-up work. The design introduces no knowingly partial implementation to defer.

## Rejected Alternatives

| Alternative | Reason rejected |
| --- | --- |
| Fully independent skill with duplicated guidance | Easy to start, but overlapping reasoning guidance could diverge from `/kk:design` |
| Shared interview procedure for both skills | Couples adaptive conversation to formal design gates and creates unnecessary mode logic |
| Full design depth without files | The user chose clarity for the next decision over mandatory implementation readiness |
| Grilling's complete question frontier as the default | The user chose one question at a time |
| Exhaust every branch before finishing | Has no practical bound for an exploratory idea and conflicts with adaptive depth |
