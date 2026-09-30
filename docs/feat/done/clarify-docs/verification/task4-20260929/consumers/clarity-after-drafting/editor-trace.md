# Visible session trace

Raw trace.jsonl is authoritative. This rendering expands JSON-wrapped command output where parsing is possible. Hidden reasoning and system boilerplate are excluded.

## Record 1; source line 1; session_meta


{
  "id": "01a0ee8c-bcc3-7081-8035-9b7766ffdb1e",
  "parent_thread_id": "01a0ee8a-00f7-7212-b97d-013f6c8d4960",
  "timestamp": "2026-09-29T19:03:15.912Z",
  "cwd": "/home/sergio/Projects/personal/claude-toolbox",
  "originator": "codex-tui",
  "cli_version": "0.159.0",
  "source": {
    "subagent": {
      "thread_spawn": {
        "parent_thread_id": "01a0ee8a-00f7-7212-b97d-013f6c8d4960",
        "depth": 2,
        "agent_path": "/root/consumer_evals/consumer_after_editor",
        "agent_nickname": "Sagan",
        "agent_role": null
      }
    }
  },
  "thread_source": "subagent",
  "agent_path": "/root/consumer_evals/consumer_after_editor",
  "model_provider": "openai"
}

## Record 2; source line 8; turn_context


{
  "turn_id": "01a0ee8c-bcf5-7d70-820b-cae4c8864fe9",
  "root_turn_id": "01a0ee86-dd60-70a3-a3e7-6cca7e02b8b3",
  "current_date": "2026-09-29",
  "timezone": "Europe/Oslo",
  "model": "gpt-6-astra",
  "effort": "xhigh",
  "summary": "none",
  "collaboration_mode": {
    "mode": "default",
    "settings": {
      "model": "gpt-6-astra",
      "reasoning_effort": "xhigh"
    }
  },
  "sandbox_policy": {
    "type": "workspace-write",
    "network_access": false,
    "exclude_tmpdir_env_var": false,
    "exclude_slash_tmp": false
  },
  "approval_policy": "on-request"
}

## Record 3; source line 10; agent_message


Message Type: NEW_TASK
Task name: /root/consumer_evals/consumer_after_editor
Sender: /root/consumer_evals
Payload:



## Record 4; source line 11; custom_tool_call


exec

const r=await tools.exec_command({cmd:"cat /tmp/clarify-task4/consumers/clarity-after-drafting/editor-request.md",max_output_tokens:6000});text(r.output);


## Record 5; source line 14; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

failed to initialize logging: "/home/sergio/.config/navi/navi.log" is not created

Caused by:
    Read-only file system (os error 30)
You are executing one isolated fixture request. Use only the frozen instruction package below as the operative plugin. Do not use the installed plugin copy.

## Plugin Root
/tmp/clarify-task4/instructions

Workspace: /tmp/clarify-task4/consumers/clarity-after-drafting/workspace
Start the explicitly requested skill at /tmp/clarify-task4/instructions/skills/design/SKILL.md. Resolve its linked instructions and profile paths within this package. This fixture contains no external knowledge service; .invalid URLs are simulated read-only responses. No network access.

## User request
Use /kk:design to document the accepted archive-label idea in docs/feat/wip/archive-label/. The accepted decisions are in accepted.md; all refinement choices and the design presentation are approved, so proceed with drafting without reopening them. This is for the next contributor. Do not implement or run the recommended review.

## Allowed reads
This request; the frozen /tmp/clarify-task4/instructions/skills/ and /tmp/clarify-task4/instructions/profiles/ instruction trees (no evals present); the files listed below and any documents you create within the user-authorized output scope. Directory/filename inspection is allowed within the workspace and frozen instruction package. Nothing outside these paths is permitted, including repository files, installed instructions, other runs, oracles, eval definitions or session transcripts.
- /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/accepted.md

## Allowed writes
Only the selected output documents authorized by the request, under /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/. Use native apply_patch for authored content. Do not mutate source fixtures outside that scope.
Observation-only recording: immediately after all selected draft documents exist and before any final clarity pass, copy those draft files preserving relative paths into /tmp/clarify-task4/consumers/clarity-after-drafting/draft-snapshot/. These copies are evidence, not extra product outputs; do not reread or edit the copies.

Do not spawn other agents. You are not alone in the shared filesystem; keep every action within this manifest and do not revert other work. Complete the user request and return your result as the final response.



## Record 6; source line 19; message


I’m using `/kk:design` from the frozen instruction package to draft the accepted design, then check its clarity for the next contributor.


## Record 7; source line 20; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/design/SKILL.md",login:false,max_output_tokens:10000})).output);


## Record 8; source line 23; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

---
name: design
description: |
  Use in pre-implementation (idea-to-design) stages to understand spec/requirements and create a correct implementation plan before writing actual code.
  Turns ideas into a fully-formed PRD/design/specification and implementation-plan. Creates design docs and task lists in docs/feat/wip/.
---

# Task Analysis Process

**Goal: Before writing any code, make sure you understand the requirements and have an implementation plan ready.**

## Conventions

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When an active profile contributes a `design/` subdirectory (e.g., `${TOOLBOX_PLUGIN_ROOT}/profiles/k8s/design/`), its `questions.md` feeds the idea-refinement question pool and its `sections.md` lists required sections the design document must cover. Both the idea-to-design and continue-WIP flows consult the shared procedure; see each flow's workflow file for the specific integration points.

For fresh ideas, two reference files provide methodology and evaluation rubric: [frameworks.md](./frameworks.md) (ideation lenses for the diverge phase) and [refinement-criteria.md](./refinement-criteria.md) (evaluation dimensions and MVP scoping for the converge phase). These are loaded during the instruction-load step and consumed by idea-process.md Step 3 sub-phases.

## Workflow

**Mandatory order — understanding before engagement.** The flow below is strictly sequential. Do not engage with idea prose beyond a keyword scan, read WIP document content, ask refinement questions, or write design content until all instructions — this SKILL.md, the relevant process file, the shared protocols including [shared-document-clarity.md](shared-document-clarity.md), every resolved profile's `design/` content, and the fresh-idea references below when applicable — are fully loaded. Bounded signal inspection for profile detection is the only content-read exception.

The `/kk:design` skill has two entry points; each has its own process file with a detailed workflow. Both follow the same mandatory ordering:

1. **Keyword scan only.** The idea prose (or WIP feature directory) is scanned at the keyword/filename level — enough to drive profile detection, not enough to engage with the content.
2. **Load instructions.** Read the relevant process file ([idea-process.md](./idea-process.md) or [existing-task-process.md](./existing-task-process.md)), the shared protocols above, [shared-document-clarity.md](shared-document-clarity.md) and [example-tasks.md](./example-tasks.md) (task format), even on an unchanged resume. For WIP, also load the drafting guidelines in idea-process.md for potential refinement, without running its fresh-idea sub-phases. For fresh ideas, also read [frameworks.md](./frameworks.md) (ideation lenses) and [refinement-criteria.md](./refinement-criteria.md) (evaluation rubric).
3. **Detect active profiles.** Delegate to [shared-profile-detection.md](shared-profile-detection.md). For fresh ideas, this uses the design interaction pattern (token matching against idea prose). For WIP features, this uses file-based detection with design-pattern fallback.
4. **Load profile content.** For each active profile contributing a `design/` subdirectory, read its `index.md` and all always-load and matching conditional entries. These feed the refinement question pool and required design sections.
5. **Engage with subject matter.** Follow the selected process file's content-reading, refinement and drafting steps.
6. **Clarify completed outputs.** Apply the loaded shared procedure once after all design, implementation and task artifacts are drafted; on resume, apply it only to documents changed by refinement. Supply the intended implementer/reviewer, selected outputs, accepted requirements and applicable source context. Preserve required sections, profile topics, decisions, task state and links. An unchanged resume skips the pass. The process file places this before review recommendation or implementation handoff.

Use the shared procedure directly, without invoking `/kk:clarify-docs` or another writing skill. Its comparison is in-session; retain the `/kk:review-design` recommendation, without claiming independent verification or automatically running that review.

## Ideas and Prototypes

_Use this for ideas that are not fully thought out and do not have a fully-formed design/specification and/or implementation-plan._

**For example:** I've got an idea I want to talk through with you before we proceed with the implementation.

**Your job:** Help me turn it into a fully formed design, spec, implementation plan, and task list.

See [idea-process.md](./idea-process.md).

## Continue WIP Feature

_Use this to resume work on a feature that already has design docs and a task list in `/docs/feat/wip/`._

**For example:** Let's continue working on the auth system.

**Your job:** Review the current state of the feature, understand what's been done and what's next, then proceed with implementation.

See [existing-task-process.md](./existing-task-process.md).


## Record 9; source line 25; custom_tool_call


exec

const results=await Promise.allSettled([
tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/design/idea-process.md /tmp/clarify-task4/instructions/skills/design/shared-capy-knowledge-protocol.md /tmp/clarify-task4/instructions/skills/design/shared-profile-detection.md",login:false,max_output_tokens:24000}),
tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/design/shared-document-clarity.md /tmp/clarify-task4/instructions/skills/design/example-tasks.md /tmp/clarify-task4/instructions/skills/design/frameworks.md /tmp/clarify-task4/instructions/skills/design/refinement-criteria.md",login:false,max_output_tokens:24000}),
tools.exec_command({cmd:"rg --files /tmp/clarify-task4/consumers/clarity-after-drafting/workspace /tmp/clarify-task4/instructions/profiles",login:false,max_output_tokens:8000})
]);for(let i=0;i<results.length;i++)text({i,...results[i]});


## Record 10; source line 30; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

Warning: truncated output (original token count: 14565)
Total output lines: 3

{"i":0,"status":"fulfilled","value":{"chunk_id":"1730fb","wall_time_seconds":0.000010686,"exit_code":0,"original_token_count":6497,"output":"### Workflow\n\n**Entry prerequisite — instructions before subject matter.** Complete the mandatory instruction loading and profile resolution in [SKILL.md](SKILL.md#workflow) before Step 1 below. That includes the shared clarity procedure and task-format example. The steps below begin with subject matter and do not repeat detection.\n\nCopy this checklist and check off items as you complete them:\n\n```\nTask Progress:\n- [ ] Step 1: Understand the current state of the project\n- [ ] Step 2: Check the documentation\n- [ ] Step 3: Refine the idea\n- [ ] Step 4: Describe the design\n- [ ] Step 5: Document the design\n- [ ] Step 6: Create the task list\n- [ ] Step 7: Clarify completed artifacts and recommend review\n```\n\n**Step 1: Understand the current state of the project**\n\nTo properly refine the idea into a fully-formed design you need to **understand the existing code** in our working directory to know where we're starting off.\n\n**Step 2: Check the documentation**\n\nIn order to gain a better understanding of the project, **check the contributing guidelines and any relevant documentation**. For example, take a look at `CONTRIBUTING.md` and `docs` directory.\n\n**Capy search:** Before refining the idea, search `kk:arch-decisions` and `kk:project-conventions` for prior design context related to the feature area being discussed.\n\n**Step 3: Refine the idea**\n\nUse the profiles resolved during entry; their loaded questions seed the refinement question pool. Integrate those questions into the sub-phases below — one question per message, as always.\n\nNote: [frameworks.md](frameworks.md) and [refinement-criteria.md](refinement-criteria.md) are already loaded during the mandatory instruction-load phase (SKILL.md step 2). Do not reload them here.\n\n**Interaction style throughout:** one question per message, multiple choice preferred. Open-ended questions are OK too. The sub-phases below add structure to _what_ is asked, not _how_.\n\n**Step 3 Progress:**\n- [ ] 3a HMW framing confirmed\n- [ ] 3b who/persona confirmed\n- [ ] 3b success metric confirmed\n- [ ] 3b constraints confirmed\n- [ ] 3c complexity classification confirmed\n- [ ] 3c alternatives presented\n- [ ] 3d direction chosen\n- [ ] 3e assumptions, Not Doing, and Rejected Alternatives presented\n\n**3a. Frame the problem.** Restate the idea as a rough \"How Might We\" problem statement — a directional anchor, not a fully specified template. Use [frameworks.md §HMW](frameworks.md#how-might-we-hmw) for format quality guidance (good vs bad HMW qualities), but do not attempt to fill every slot (specific user, key constraint) yet — those come from 3b. Present the framing to the user for confirmation or correction before proceeding. This anchors all subsequent questions on the problem, not a solution.\n\n**3b. Establish foundations.** Three things must be explicitly answered before advancing to alternatives. Ask one at a time, multiple choice preferred:\n\n1. **Who is this for** — specific user, persona, or role. \"Everyone\" is not an answer.\n2. **What does success look like** — a measurable outcome, not a feature name. \"Users can log in\" → \"Login p99 latency under 500ms with zero-downtime deployment.\"\n3. **Technical/system constraints** — what existing systems, APIs, data stores, infrastructure, or conventions must be respected. What is off-limits to change.\n\nDo not advance to 3c until all three are confirmed.\n\n**3c. Explore alternatives.** Select frameworks from the already-loaded [frameworks.md](frameworks.md) that fit the idea — pick by \"Best for\" guidance, never run every framework.\n\nClassify the idea before generating alternatives. **Non-trivial** if it involves architectural choices, multiple valid implementation approaches, or significant unknowns. **Simple** if the implementation path is singular and the main decisions are parameter-level. State which classification and why, then confirm with the user:\n\n- **For simple ideas:**\n  > \"This looks like a straightforward single-path problem — I'll propose the direct approach plus one alternative. Want me to explore more broadly instead?\"\n- **For non-trivial ideas:**\n  > \"This has multiple valid approaches with real trade-offs — I'll explore 2-3 alternative directions using [selected frameworks] and summarize their trade-offs. Sound right, or should I narrow the focus?\"\n\nTwo paths:\n\n- **Non-trivial ideas** (multiple valid approaches, significant unknowns, architectural choices): generate 2-3 alternative directions using selected lenses. Present each with a one-sentence trade-off summary. After presenting alternatives, stop and ask which alternatives to carry into evaluation — or whether to add a missed constraint and loop back. Do not evaluate or recommend a direction in the same message that first presents alternatives unless the user explicitly asks you to continue.\n- **Simple ideas** (single-concern, low-uncertainty, obvious path): propose the direct implementation path plus briefly mention one alternative optimized for a different constraint (e.g., \"We could also do X if extensibility matters more than simplicity\"). Ask which to proceed with.\n\nNever skip this step silently — the user always sees at least two options. If the user rejects all alternatives, ask what constraint or dimension was missed, then loop back to 3c with that input as an additional lens.\n\n**3d. Converge.** Evaluate each direction against the already-loaded [refinement-criteria.md](refinement-criteria.md) (User Value, Feasibility, Differentiation) via criteria-based analysis. Present a pros/cons matrix and recommend one direction with a one-line rationale per rejected alternative.\n\nIf alternatives make specific factual claims about APIs, libraries, or existing code, offer the user an explicit choice: \"Some of these alternatives make specific technical claims I can fact-check. Want me to run `/kk:chain-of-verification:isolated` to verify them, or should I proceed with the analysis as-is?\" Let the user decide — do not auto-invoke or auto-skip CoVe.\n\n**3e. Surface assumptions and scope.** Before moving to Step 4, produce and present to the user:\n\n- **Assumptions** — what is baked into the chosen direction but has not been validated. Each assumption should be specific enough to be testable or falsifiable — not vague hedges like \"the API is fast enough.\"\n- **Not Doing** — explicit scope exclusions with a one-line reason each.\n- **Rejected Alternatives** — each alternative evaluated in 3d that was not chosen, with a one-line rationale for why it lost. This is the convergence rationale from the pros/cons matrix, persisted so future reviewers can see what was considered and why.\n\nAll three become first-class artifacts in the design document (Step 5) and tasks.md header (Step 6 — Not Doing only).\n\n**Step 4: Describe the design**\n\nOnce you believe you understand what we're trying to achieve, stop and **describe the whole design** to me, **in sections of 200-300 words at a time**, **asking after each section whether it looks right so far**.\n\n**If the design recommends a specific library, SDK, framework, or API** — especially one not already in use in this project — apply the `/kk:dependency-handling` skill BEFORE committing to that recommendation. Verifying behavior against context7 at design time prevents proposing something that doesn't actually work the way you assumed.\n\n**Step 5: Document the design**\n\nDocument in .md files the entire design and write a comprehensive implementation plan.\n\nFeel free to break out the design/implementation documents into multi-part files, if necessary.\n\n**For each active profile** resolved during entry, apply the loaded guidance that shapes the final design document. Profile-contributed `sections.md` (when present) names required sections the design document must cover. Do not drop a required section silently; if a section genuinely does not apply, state so explicitly with a one-line justification.\n\nWhen creating documentation, follow this approach:\n\n- IF this is this a completely new feature - document it in in `/docs/feat/wip/[feature-title]/{design,implementation}.md`.\n- ELSE this an improvement or an addition to an existing feature:\n  - If the feature is still WIP (documented under `/docs/feat/wip`) - ask the user if you should update the existing design/implementation documents, or create new ones in a sub-directory of the existing feature.\n  - Else the feature is completed (documented under root of `/docs`) - create new design/implementation documents in a sub-directory of the existing feature.\n\n**When documenting design and implementation plan**:\n\n- Assume the developer who is going to implement the feature is an experienced and highly-skilled %LANGUAGE% developer, but has zero context for our codebase, and knows almost nothing about our problem domain. Basically - a first-time contributor with a lot of programming experience in %LANGUAGE%.\n- **Document everything the developer may need to know**: which files to touch for each task, code structure to be aware of, testing approaches, any potential docs they might need to check. Give them the whole plan as bite-sized tasks.\n- **Make sure the plan is unambiguous, detailed and comprehensive** so the developer can adhere to DRY, YAGNI, TDD, atomic/self-contained commits principles when following this plan.\n- **Pair each step with an explicit verification.** Every implementation step should name *how the developer will know it worked* — a specific test to run, a command whose output to check, or an observable behavior. Use the form `Step → verify: <check>`. Steps without a verification are a smell: either the step is too vague, or the work isn't really done when the step is.\n- **Include an Assumptions section** — carried from Step 3e. List assumptions baked into the design, each specific enough to be validated or invalidated during implementation. Assumptions are not caveats — they are testable bets the design depends on.\n- **Include a Not Doing section** — carried from Step 3e. Explicit scope exclusions with a one-line rationale each. These are genuine scope decisions, not deferred work items. If something is deferred (will be done later), say so in the implementation plan, not in Not Doing.\n- **Include a Rejected Alternatives section** — carried from Step 3e. Each alternative considered during convergence (3d) that was not chosen, with a one-line rationale for why it was rejected. Serves a different audience than Not Doing: Not Doing tells the implementer what's out of scope; Rejected Alternatives tells a future reviewer why this approach was chosen over others.\n\nBut, of course, **DO NOT:**\n\n- **DO NOT add complete code examples**. The documentation should be a guideline that gives the developer all the information they may need when writing the actual code, not copy-paste code chunks.\n- **DO NOT add commit message templates** to tasks, that the developer should use when committing the changes.\n- **DO NOT add other small, generic details that do not bring value** and/or are not specifically relevant to this particular feature. For example, adding something like \"to run tests, execute: 'go test ./...'\" to a task does not bring value. Remember, the developer is experienced and skilled!\n\n**Capy index:** After documenting the design, index key architecture decisions and trade-offs as `kk:arch-decisions`. Only index non-obvious rationale — skip if the decisions are self-evident from the docs themselves.\n\n**Step 6: Create the task list**\n\nBased on the implementation plan documented in Step 5, create a `tasks.md` file in the same `/docs/feat/wip/[feature-title]/` directory.\n\nFollow the structure and conventions in the [example task file](./example-tasks.md). Key points:\n\n- **Header metadata** links back to design/implementation docs and tracks overall feature status\n- **One H2 per task** with status, dependencies, and a link to the relevant docs section\n- **Checkbox subtasks** are concrete, actionable implementation steps — specific enough that a developer with no project context can follow them\n- **Subtask descriptions** name the file/function/component being touched and what to do with it — not vague (\"implement auth\") but precise (\"create `internal/auth/token.go` with `GenerateToken` and `ValidateToken` functions\")\n- **Dependencies** reference other tasks by number when ordering matters\n- **Status values:** `pending`, `in-progress`, `done`, `blocked` (with reason)\n- Tasks should map roughly 1:1 to atomic, self-contained commits\n- **Always include a final verification task** that depends on all other tasks — it should invoke `/kk:test` to run the full test suite, `/kk:document` to update any relevant docs, `/kk:review-code` with project's language input to review the code, and `/kk:review-spec` to verify the implementation matches the design and implementation docs\n- **Not Doing in header:** The tasks.md header metadata block includes a `> Not Doing:` line listing the concise scope exclusions from design.md (names only, no extended rationale). The implement skill reads tasks.md first; this puts scope boundaries front and center.\n- **Vertical slicing:** Each task delivers one complete, testable user-facing path — not a horizontal layer. Anti-pattern: \"Do not create tasks that complete an entire layer (all database work, then all API work, then all UI work) — this defers integration risk to the end.\" A task like \"create all DB models\" is wrong; \"create user registration end-to-end (model + endpoint + validation + test)\" is right.\n- **Size tags:** Each task gets a `**Size:** S/M/L` field. S = 1-2 files, M = 3-5 files, L = 5+ files. Size measures complexity, not raw file count — exclude boilerplate registrations, test fixtures, and config entries that are mechanical consequences of the main change. Hard rule: any task tagged L is forbidden as a single task. Break it into smaller vertical slices.\n- **Slicing strategies:** Three strategies, noted per-task only when deviating from default:\n  - **Vertical** (default): each task delivers one complete path from input to output, testable in isolation.\n  - **Contract-First**: define the interface/API boundary first, then implement each side independently. Use when introducing a new external boundary (API, SDK, message queue).\n  - **Risk-First**: tackle the most uncertain piece first to surface unknowns early. Use when one task carries significantly more uncertainty than others.\n- **Parallel markers:** Each task gets a `**Can run in parallel with:**` field listing task numbers with no blocking dependency, or `—`.\n- **Dependency graph:** After all tasks, add a `## Dependency Graph` section with an ASCII diagram showing task relationships. Written once, never updated during implementation.\n\n**Step 7: Clarify completed artifacts and recommend review**\n\nAfter all design, implementation and task artifacts exist, apply [shared-document-clarity.md](shared-document-clarity.md) once to that selected set, using the accepted requirements and applicable source understanding from drafting. Keep the required sections and task format above. This is the final pass summarized in SKILL.md, not an additional pass or skill invocation.\n\nThen recommend invoking `/kk:review-design <feature>` as the post-design gate. The default scope reviews all documents (`design.md + implementation.md + tasks.md`), including the task-format checks. The recommendation does not execute independent review.\n# Capy Knowledge Base Protocol\n\nIf `capy` MCP tools are not available in this session, skip all search and index steps below and proceed normally.\n\n## Source Label Taxonomy\n\nAll plugin-managed labels use the `kk:` namespace prefix.\n\n| Label                    | Contents                                                              |\n| ------------------------ | --------------------------------------------------------------------- |\n| `kk:arch-decisions`      | Architecture decisions, design rationale, trade-offs                  |\n| `kk:review-findings`     | Code review patterns, recurring issues, anti-patterns                 |\n| `kk:lang-idioms`         | Language best practices, idiomatic patterns from external sources     |\n| `kk:project-conventions` | Discovered project patterns, naming conventions, structural decisions |\n| `kk:test-patterns`       | Testing approaches, edge cases, test infrastructure decisions         |\n| `kk:debug-context`       | Root causes, tricky bugs and their fixes, environment gotchas         |\n\n## Search Conventions\n\n- Use 2-4 specific terms per query — not vague keywords\n- Always scope with `source` filter to relevant `kk:*` labels\n- Use `source: \"kk:\"` only for broad cross-domain searches (e.g., CoVe verification)\n- Default `limit: 3` per query unless more context is needed\n- **Cold-start fallback:** If no results, proceed with standard guidelines — empty results are normal for new projects\n\n## Index Conventions\n\n- Only index non-obvious learnings not derivable from reading the code or git history\n- Keep content concise — summarize the insight, don't dump raw output\n- Always use a `kk:` prefixed label from the taxonomy above\n- One concept per `capy_index` call — don't bundle unrelated learnings\n- Skip indexing if the insight is already captured in design docs or CLAUDE.md\n## Profile detection procedure\n\nSingle source of truth for computing the set of profiles active in the current context.\nConsumed by six skills: `/kk:review-code`, `/kk:review-spec`, `/kk:design`, `/kk:implement`, `/kk:test`, and `/kk:document`.\n\nEvery profile under `klaude-plugin/profiles/<name>/` declares its own trigger rule in `DETECTION.md` using the mandatory three-section schema (`## Path signals`, `## Filename signals`, `## Content signals`).\nThe shared procedure below applies the same algorithm against every profile's declared values.\n\n### Inputs per consuming skill\n\nNot every consumer has a diff available. Use the input listed for your skill:\n\n- **`/kk:review-code`** — git diff (staged, or an explicit commit range). Scope is\n  the set of files the diff touches.\n- **`/kk:review-spec`** — git diff when invoked standalone; the feature directory's\n  full file list when invoked by `/kk:implement` (spec review runs over the whole\n  feature, not just the current task's diff).\n- **`/kk:test`** — git diff mid-feature, OR the feature directory's file list\n  post-implementation.\n- **`/kk:implement`** — the current sub-task's target file list, augmented by the\n  diff accumulated so far in the feature.\n- **`/kk:design`** — **no file list available** (implementation does not yet exist).\n  Detection uses a user-declared or keyword-inferred signal instead; see\n  [The `/kk:design` interaction pattern](#the-design-interaction-pattern) below.\n- **`/kk:document`** — feature directory's current file list; diff optional.\n\n### The `/kk:design` interaction pattern\n\nThe design phase runs before any code exists, so file-based detection is impossible. Detection uses idea-prose keyword matching against tokens declared in each profile's `DETECTION.md`.\n\n**Algorithm:**\n\n1. **Collect tokens.** Iterate §Known profiles. For each `<name>`, `Read` `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/DETECTION.md`. If the file has no `## Design signals` section, skip — that profile does not participate in design-phase detection. Otherwise, parse `display_name` and `tokens` from the section.\n2. **Build union.** Collect all declared tokens into a single set, each tagged by its source profile name and `display_name`.\n3. **Match.** Check the idea prose against the union. Matc…4565 tokens truncated…ens that fits the idea; don't mechanically run every framework.\n\n## SCAMPER\n\nA structured way to transform an existing idea by applying seven different operations:\n\n- **Substitute:** What component, technology, or process could you swap out? What if you replaced the synchronous RPC with an event-driven approach? The relational database with a document store? The monolith deployment with a service mesh?\n- **Combine:** What if you merged this with another product, service, or idea? What two things that don't usually go together would create something new?\n- **Adapt:** What else is like this? What ideas from other domains or systems could you borrow? What parallel exists in nature?\n- **Modify (Magnify/Minimize):** What if you made it 10x bigger? 10x smaller? What if you exaggerated one feature? What if you stripped it to the absolute minimum?\n- **Put to other uses:** Who else could use this? What other problems could it solve? What happens if you use it in a completely different context?\n- **Eliminate:** What happens if you remove a feature entirely? What's the version with zero configuration? What would it look like with half the steps?\n- **Reverse/Rearrange:** What if you did the steps in the opposite order? What if the user/client did the work instead of the system/server (or vice versa)? What if you reversed the dependency direction, or the value chain?\n\n**Best for:** Improving or reimagining existing systems/products/features. Less useful for greenfield ideas.\n\n## How Might We (HMW)\n\nReframe problems as opportunities using the \"How Might We...\" format:\n\n- Start with an observation or pain point\n- Reframe it as \"How might we [desired outcome] for [specific user] without [key constraint]?\"\n- Generate multiple HMW framings of the same problem — different framings unlock different solutions\n\n**Good HMW qualities:**\n- Narrow enough to be actionable (\"...help new users find relevant content in their first 5 minutes\")\n- Broad enough to allow creative solutions (not \"...add a recommendation sidebar\")\n- Contains a tension or constraint that forces creativity\n\n**Bad HMW qualities:**\n- Too broad: \"How might we make users happy?\"\n- Too narrow: \"How might we add a button to the settings page?\"\n- Solution-embedded: \"How might we build a chatbot for support?\"\n\n**Best for:** Reframing stuck thinking. When someone is anchored on a solution, pull them back to the problem.\n\n## First Principles Thinking\n\nBreak the idea down to its fundamental truths, then rebuild from there:\n\n1. **What do we know is true?** (not assumed, not conventional — actually true)\n2. **What are we assuming?** List every assumption, even the ones that feel obvious\n3. **Which assumptions can we challenge?** For each, ask: \"Is this actually a law of physics, or just how it's been done?\"\n4. **Rebuild from the truths.** If you only had the fundamental truths, what would you build?\n\n**Best for:** Breaking out of incremental thinking. When every idea feels like a small improvement on the status quo.\n\n## Jobs to Be Done (JTBD)\n\nFocus on what the user is trying to accomplish, not what they say they want:\n\n- **Functional job:** What task are they trying to complete?\n- **Emotional job:** How do they want to feel?\n- **Social job:** How do they want to be perceived?\n\nFormat: \"When I [situation], I want to [motivation], so I can [expected outcome].\"\n\n**Key insight:** Users don't adopt tools — they hire them to do a job. The competing solution isn't always in the same category. (A CLI tool competes with a shell script alias, not just other CLI tools.)\n\n**Best for:** Understanding the real problem. When you're not sure if you're solving the right thing.\n\n## Constraint Mapping\n\nDeliberately impose constraints to force creative solutions:\n\n- **Time constraint:** \"What if you only had 1 day to build this?\"\n- **Feature constraint:** \"What if it could only have one feature?\"\n- **Tech constraint:** \"What if you couldn't use [the obvious technology]?\"\n- **Cost constraint:** \"What if it had to be free forever?\"\n- **Audience constraint:** \"What if your user had never used a computer before?\"\n- **Scale constraint:** \"What if it needed to work for 1 billion users? What about just 10?\"\n\n**Best for:** Cutting through complexity. When the idea is growing too large or too vague.\n\n## Pre-mortem\n\nImagine the idea has already failed. Work backwards:\n\n1. It's 12 months from now. The project shipped and flopped. What went wrong?\n2. List every plausible reason for failure — technical, adoption, integration, operational\n3. For each failure mode: Is this preventable? Is this a signal the idea needs to change?\n4. Which failure modes are you willing to accept? Which ones would kill the project?\n\n**Best for:** Phase 2 evaluation. Stress-testing ideas that feel good but haven't been pressure-tested.\n\n## Analogous Inspiration\n\nLook at how other domains solved similar problems:\n\n- What industry or system has already solved a version of this problem?\n- What would this look like if someone else built it?\n- What natural system or distributed system works this way?\n- What historical precedent exists?\n\nThe key is finding *structural* similarities, not surface-level ones. \"Git for config files\" is surface-level. \"A content-addressable store with branching semantics that solves the concurrent-edit problem\" is structural.\n\n**Best for:** Phase 1 expansion. Generating variations that feel genuinely different from the obvious approach.\n<!-- Adapted from addyosmani/agent-skills (MIT License, Copyright Addy Osmani)\n     Source: https://github.com/addyosmani/agent-skills/blob/539a78574773fe7e46cf8bbf9c67bcc9db63c335/skills/idea-refine/refinement-criteria.md\n     Pinned at: 539a78574773fe7e46cf8bbf9c67bcc9db63c335 -->\n\n# Refinement & Evaluation Criteria\n\nUse this rubric to stress-test idea directions during convergence. These criteria apply to software engineering features — APIs, infrastructure, developer tools, internal systems, library design. Not every criterion applies to every idea — use judgment about which dimensions matter most for the specific context.\n\n## Core Evaluation Dimensions\n\n### 1. User Value\n\nThe most important dimension. If the value isn't clear, nothing else matters.\n\n**Painkiller vs. Vitamin:**\n\n- **Painkiller:** Solves an acute, frequent problem. Users will actively seek this out. They'll switch from their current solution. Signs: people describe the problem with emotion, they've built workarounds, they'll pay for a solution.\n- **Vitamin:** Nice to have. Makes something marginally better. Users won't go out of their way. Signs: people nod politely, say \"that's cool,\" then don't change behavior.\n\n**Questions to ask:**\n\n- Can you name 3 specific people who have this problem right now?\n- What are they doing today instead? (The real competitor is always the current workaround.)\n- Would they switch from their current approach? What would make them switch?\n- How often do they encounter this problem? (Daily problems > monthly problems)\n- Is this a \"pull\" problem (users are asking for this) or a \"push\" problem (you think they should want this)?\n\n**Red flags:**\n\n- \"Everyone could use this\" — if you can't name a specific user, the value isn't clear\n- \"It's like X but better\" — marginal improvements rarely drive adoption\n- The problem is real but rare — high intensity but low frequency rarely justifies a product\n\n### 2. Feasibility\n\nCan you actually build this? Not just technically, but practically.\n\n**Technical feasibility:**\n\n- Does the core technology exist and work reliably?\n- What's the hardest technical problem? Is it a known-hard problem or a novel one?\n- Are there dependencies on third parties, APIs, or data sources you don't control?\n- What's the minimum technical stack needed? (If the answer is \"a lot,\" that's a signal.)\n\n**Resource feasibility:**\n\n- What's the minimum team/effort to build an MVP?\n- Does it require specialized expertise you don't have?\n- Are there regulatory, legal, or compliance requirements?\n\n**Time-to-value:**\n\n- How quickly can you get something in front of users?\n- Is there a version that delivers value in days/weeks, not months?\n- What's the critical path? What has to happen first?\n\n**Red flags:**\n\n- \"We just need to solve [very hard research problem] first\"\n- Multiple dependencies that all need to work simultaneously\n- MVP still requires months of work — likely not minimal enough\n\n### 3. Differentiation\n\nWhat makes this genuinely different? Not better — _different_.\n\n**Questions to ask:**\n\n- If a user described this to a friend, what would they say? Is that description compelling?\n- What's the one thing this does that nothing else does? (If you can't name one, that's a problem.)\n- Is this differentiation durable? Can a competitor copy it in a week?\n- Is the difference something users actually care about, or just something builders find interesting?\n\n**Types of differentiation (strongest to weakest):**\n\n1. **New capability:** Does something that was previously impossible\n2. **10x improvement:** So much better on a key dimension that it changes behavior\n3. **New audience:** Brings an existing capability to people who were excluded\n4. **New context:** Works in a situation where existing solutions fail\n5. **Better UX:** Same capability, dramatically simpler experience\n6. **Cheaper:** Same thing, lower cost (weakest — easily competed away)\n\n**Red flags:**\n\n- Differentiation is entirely about technology, not user experience\n- \"We're faster/cheaper/prettier\" without a structural reason why\n- The feature that differentiates is not the feature users care most about\n\n## Assumption Audit\n\nFor every idea direction, explicitly list assumptions in three categories:\n\n### Must Be True (Dealbreakers)\n\nAssumptions that, if wrong, kill the idea entirely. These need validation before building.\n\nExample: \"The external API supports batch operations\" — if it doesn't, the entire design around bulk processing doesn't work.\n\n### Should Be True (Important)\n\nAssumptions that significantly impact success but don't kill the idea. You can adjust the approach if these are wrong.\n\nExample: \"Teams will adopt the CLI over the existing manual workflow\" — if wrong, you need a different rollout strategy, but the core tool can still work.\n\n### Might Be True (Nice to Have)\n\nAssumptions about secondary features or optimizations. Don't validate these until the core is proven.\n\nExample: \"Teams will want to export reports to Slack\" — a convenience feature, not a core value proposition.\n\n## Decision Framework\n\nWhen choosing between directions, rank on this matrix:\n\n|                | High Feasibility | Low Feasibility |\n| -------------- | ---------------- | --------------- |\n| **High Value** | Do this first    | Worth the risk  |\n| **Low Value**  | Only if trivial  | Don't do this   |\n\nThen use differentiation as the tiebreaker between options in the same quadrant.\n\n## MVP Scoping Principles\n\nWhen defining MVP scope for the chosen direction:\n\n1. **One job, done well.** The MVP should nail exactly one user job. Not three jobs done partially.\n2. **The riskiest assumption first.** The MVP's primary purpose is to test the assumption most likely to be wrong.\n3. **Time-box, not feature-list.** \"What can we build and test in [timeframe]?\" is better than \"What features do we need?\"\n4. **The 'Not Doing' list is mandatory.** Explicitly name what you're cutting and why. This prevents scope creep and forces honest prioritization.\n5. **If it's not embarrassing, you waited too long.** The first version should feel incomplete to the builder. If it doesn't, you over-built.\n"}}
{"i":2,"status":"fulfilled","value":{"chunk_id":"844b7f","wall_time_seconds":0.000007446,"exit_code":0,"original_token_count":1962,"output":"/tmp/clarify-task4/consumers/clarity-after-drafting/workspace/accepted.md\n/tmp/clarify-task4/instructions/profiles/kotlin/overview.md\n/tmp/clarify-task4/instructions/profiles/kotlin/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/python/overview.md\n/tmp/clarify-task4/instructions/profiles/python/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/skill-md/implement/skill-structure-gotchas.md\n/tmp/clarify-task4/instructions/profiles/skill-md/implement/index.md\n/tmp/clarify-task4/instructions/profiles/skill-md/implement/kk-plugin-gotchas.md\n/tmp/clarify-task4/instructions/profiles/skill-md/implement/claude-code-gotchas.md\n/tmp/clarify-task4/instructions/profiles/skill-md/references/skill-building-guide.md\n/tmp/clarify-task4/instructions/profiles/skill-md/overview.md\n/tmp/clarify-task4/instructions/profiles/skill-md/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/python/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/python/review-code/security-checklist.md\n/tmp/clarify-task4/instructions/profiles/python/review-code/solid-checklist.md\n/tmp/clarify-task4/instructions/profiles/python/review-code/code-quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/python/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/skill-md/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/skill-md/review-code/claude-code-checklist.md\n/tmp/clarify-task4/instructions/profiles/skill-md/review-code/kk-plugin-checklist.md\n/tmp/clarify-task4/instructions/profiles/skill-md/review-code/skill-quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/js_ts/overview.md\n/tmp/clarify-task4/instructions/profiles/js_ts/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/k8s-operator/overview.md\n/tmp/clarify-task4/instructions/profiles/js_ts/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/js_ts/review-code/security-checklist.md\n/tmp/clarify-task4/instructions/profiles/js_ts/review-code/solid-checklist.md\n/tmp/clarify-task4/instructions/profiles/js_ts/review-code/code-quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/js_ts/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/k8s-operator/design/questions.md\n/tmp/clarify-task4/instructions/profiles/k8s-operator/design/index.md\n/tmp/clarify-task4/instructions/profiles/k8s-operator/design/sections.md\n/tmp/clarify-task4/instructions/profiles/k8s-operator/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/kotlin/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/kotlin/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/kotlin/review-code/security-checklist.md\n/tmp/clarify-task4/instructions/profiles/kotlin/review-code/solid-checklist.md\n/tmp/clarify-task4/instructions/profiles/kotlin/review-code/code-quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/twelve-factor/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/twelve-factor/overview.md\n/tmp/clarify-task4/instructions/profiles/twelve-factor/design/questions.md\n/tmp/clarify-task4/instructions/profiles/twelve-factor/design/index.md\n/tmp/clarify-task4/instructions/profiles/twelve-factor/design/sections.md\n/tmp/clarify-task4/instructions/profiles/k8s/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/java/overview.md\n/tmp/clarify-task4/instructions/profiles/java/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-spec/type-mapping.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-spec/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-spec/helm-verification.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/helm-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-spec/kustomize-verification.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/finops-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/reliability-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/security-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/architecture-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/review-code/kustomize-checklist.md\n/tmp/clarify-task4/instructions/profiles/k8s/overview.md\n/tmp/clarify-task4/instructions/profiles/java/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/java/review-code/security-checklist.md\n/tmp/clarify-task4/instructions/profiles/java/review-code/solid-checklist.md\n/tmp/clarify-task4/instructions/profiles/java/review-code/code-quality-checklist.md\n/tmp/clarify-task4/instructions/profiles/java/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/k8s/implement/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/implement/gotchas.md\n/tmp/clarify-task4/instructions/profiles/k8s/design/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/design/sections.md\n/tmp/clarify-task4/instructions/profiles/k8s/design/questions.md\n/tmp/clarify-task4/instructions/profiles/k8s/document/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/document/rubric.md\n/tmp/clarify-task4/instructions/profiles/k8s/test/policy-hook.md\n/tmp/clarify-task4/instructions/profiles/k8s/test/index.md\n/tmp/clarify-task4/instructions/profiles/k8s/test/presence-check-protocol.md\n/tmp/clarify-task4/instructions/profiles/k8s/test/validators.md\n/tmp/clarify-task4/instructions/profiles/go/DETECTION.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/code-style.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/security.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/error-handling.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/performance.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/index.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/concurrency.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/solid-checklist.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/naming.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/grpc.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/database.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/security-injection-ref.md\n/tmp/clarify-task4/instructions/profiles/go/review-code/removal-plan.md\n/tmp/clarify-task4/instructions/profiles/go/implement/structs-interfaces.md\n/tmp/clarify-task4/instructions/profiles/go/implement/grpc.md\n/tmp/clarify-task4/instructions/profiles/go/implement/database.md\n/tmp/clarify-task4/instructions/profiles/go/implement/design-patterns.md\n/tmp/clarify-task4/instructions/profiles/go/implement/security.md\n/tmp/clarify-task4/instructions/profiles/go/implement/error-handling.md\n/tmp/clarify-task4/instructions/profiles/go/implement/data-structures.md\n/tmp/clarify-task4/instructions/profiles/go/implement/index.md\n/tmp/clarify-task4/instructions/profiles/go/implement/dependency-injection.md\n/tmp/clarify-task4/instructions/profiles/go/implement/concurrency.md\n/tmp/clarify-task4/instructions/profiles/go/implement/context.md\n/tmp/clarify-task4/instructions/profiles/go/test/index.md\n/tmp/clarify-task4/instructions/profiles/go/test/testing.md\n/tmp/clarify-task4/instructions/profiles/go/test/benchmark.md\n/tmp/clarify-task4/instructions/profiles/go/overview.md\n/tmp/clarify-task4/instructions/profiles/go/design/observability.md\n/tmp/clarify-task4/instructions/profiles/go/design/index.md\n/tmp/clarify-task4/instructions/profiles/go/design/grpc.md\n/tmp/clarify-task4/instructions/profiles/go/design/database.md\n/tmp/clarify-task4/instructions/profiles/go/document/index.md\n/tmp/clarify-task4/instructions/profiles/go/document/cli.md\n/tmp/clarify-task4/instructions/profiles/go/document/continuous-integration.md\n"}}

## Record 11; source line 34; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/design/shared-profile-detection.md /tmp/clarify-task4/instructions/skills/design/shared-document-clarity.md /tmp/clarify-task4/instructions/skills/design/example-tasks.md",login:false,max_output_tokens:12000})).output);


## Record 12; source line 37; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

## Profile detection procedure

Single source of truth for computing the set of profiles active in the current context.
Consumed by six skills: `/kk:review-code`, `/kk:review-spec`, `/kk:design`, `/kk:implement`, `/kk:test`, and `/kk:document`.

Every profile under `klaude-plugin/profiles/<name>/` declares its own trigger rule in `DETECTION.md` using the mandatory three-section schema (`## Path signals`, `## Filename signals`, `## Content signals`).
The shared procedure below applies the same algorithm against every profile's declared values.

### Inputs per consuming skill

Not every consumer has a diff available. Use the input listed for your skill:

- **`/kk:review-code`** — git diff (staged, or an explicit commit range). Scope is
  the set of files the diff touches.
- **`/kk:review-spec`** — git diff when invoked standalone; the feature directory's
  full file list when invoked by `/kk:implement` (spec review runs over the whole
  feature, not just the current task's diff).
- **`/kk:test`** — git diff mid-feature, OR the feature directory's file list
  post-implementation.
- **`/kk:implement`** — the current sub-task's target file list, augmented by the
  diff accumulated so far in the feature.
- **`/kk:design`** — **no file list available** (implementation does not yet exist).
  Detection uses a user-declared or keyword-inferred signal instead; see
  [The `/kk:design` interaction pattern](#the-design-interaction-pattern) below.
- **`/kk:document`** — feature directory's current file list; diff optional.

### The `/kk:design` interaction pattern

The design phase runs before any code exists, so file-based detection is impossible. Detection uses idea-prose keyword matching against tokens declared in each profile's `DETECTION.md`.

**Algorithm:**

1. **Collect tokens.** Iterate §Known profiles. For each `<name>`, `Read` `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/DETECTION.md`. If the file has no `## Design signals` section, skip — that profile does not participate in design-phase detection. Otherwise, parse `display_name` and `tokens` from the section.
2. **Build union.** Collect all declared tokens into a single set, each tagged by its source profile name and `display_name`.
3. **Match.** Check the idea prose against the union. Matching is case-insensitive, whole-word (so `pod` in "podcast" does not fire).
4. **Confirm.** On match, surface a confirmation prompt per matched profile:
   *"This appears to be a {display_name} feature. Activate the {profile_name} profile?"* — let the user confirm yes/no. When multiple profiles match, confirm each independently.
5. **Fallback.** If no token matches but the idea is **ambiguous** — names infrastructure, deployment, runtime, or platform concerns without naming a specific technology (e.g., _"add a caching layer for the service"_, _"build a CI pipeline"_, _"deploy to production"_); or includes overloaded tokens that collide across domains — build the fallback prompt dynamically from all profiles that declare `## Design signals`:
   *"Does this feature involve {display_name_1, display_name_2, ...}? If yes, which?"*

Confirmation is required — the /kk:design skill never auto-activates a profile silently. The narrow per-profile token sets avoid noisy false positives from tokens that overload across domains.

Once activated, subsequent design-phase steps treat the profile as active in the same record shape produced by file-based detection (see §Output shape).

### Known profiles

This is the authoritative enumeration of profile `<name>`s — do NOT try discover profiles via any other means.
An explicit list is boring, deterministic, and unambiguous; runtime filesystem enumeration against the plugin tree has proven unreliable.

- `go`
- `python`
- `java`
- `js_ts`
- `kotlin`
- `k8s`
- `k8s-operator`
- `skill-md`

### Algorithm

This procedure reads files under the plugin root. The main agent resolves the plugin root from its shell variable `$TOOLBOX_PLUGIN_ROOT`; a Read-only sub-agent uses the absolute plugin-root path injected into its prompt under `## Plugin Root` (see its agent definition). Substitute that resolved path for the plugin-root prefix in every `…/profiles/…` read below.

1. **Iterate profiles.** For each §Known profiles `<name>`:
   1. Use the `Read` tool on `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/DETECTION.md`.
   2. If `Read` fails with ENOENT (profile name in list but directory missing — a stale list entry), skip silently and move on.
   3. If `Read` succeeds, parse the declared `## Path signals`, `## Filename signals`, and `## Content signals` sections.

2. **Evaluate in cost order.** For each input file, check signals in this order: path → filename → content. Cheapest first.
3. **Apply the authority rule.** A file activates the profile only if a **filename signal** OR **content signal** matches.
   A path-only match does NOT activate. Paths are a pre-filter that promotes files to "candidates"; authoritative activation requires filename or content confirmation.
   A file that matches NO path signal is still evaluated against filename and content signals — path pre-filtering is a cost hint, not a gate.
   (Otherwise a `Chart.yaml` at a non-standard path would be missed.)
4. **Bound content inspection.** Read at most ~16 KB per file when evaluating content signals.
   Multi-document YAML is inspected per `---`-separated block — a file may have five blocks, and only the third need match for the file to activate the profile.
5. **Collect records.** Accumulate one record per matched profile with the triggering files and the signal descriptions that fired.

### Tool choice

- Single file at `${TOOLBOX_PLUGIN_ROOT}/…` → `Read`. This is what the algorithm uses.
- Enumeration across profiles → iterate the §Known profiles list, `Read` each. Never `Glob` (cwd-scoped, misses outside-cwd paths).

### Two dimensions: cost vs authority

Signals live on two axes that point in different directions. Keep them separate in your mental model:

- **Evaluation cost** (cheapest first): path < filename < content.
  Path globs touch only the path string;
  filename matches are exact string compares;
  content inspection opens the file.
- **Authority** (most authoritative first): filename ≈ content > path.
  A filename or content match activates the profile; a path-only match does not.
  Filename and content are equally authoritative, but filename resolves first at runtime — a filename match short-circuits content inspection for that file.

Evaluating cheapest-first optimizes work. Applying authority correctly prevents false positives from incidental path matches — a stray `manifests/` directory in a Go project does not make the project Kubernetes.

### Plugin-root resolution failure

If every `Read` attempt in Algorithm step 1 fails — i.e., the plugin root could not be resolved (the variable is unset for the main agent, or no `## Plugin Root` path was provided to a sub-agent) or the paths do not exist — the procedure cannot continue.

On that failure:

1. Emit an actionable error pointing to `CLAUDE.md` §Profile Conventions.
2. Return an empty result set so the calling skill falls back to generic guidance rather than panicking.
3. Do not retry; do not silently guess a path.

Consumers inherit this check by invoking the shared procedure — no skill re-implements it.

### Output shape

A list of records, one per matched profile:

```
[
  {
    profile: "<name>",                     // directory name under profiles/
    triggered_by: [
      "filename: Chart.yaml",              // signal type + matched value
      "content: apiVersion+kind in block 2"
    ],
    files: [
      "path/to/file1.yaml",
      "path/to/file2.yaml"
    ]
  },
  ...
]
```

Field semantics:

- `profile` — the directory name under `profiles/` (e.g., `go`, `python`, `k8s`).
  Used downstream to resolve `profiles/<profile>/<phase>/index.md`,
  where `<phase>` is the profile phase subdirectory named identically to the calling skill:
  `review-code/`, `review-spec/`, `design/`, `implement/`, `test/`, or `document/`.
- `triggered_by` — which signal type fired and the specific value that matched.
  For debugging and for explaining detection to the user; never used as the key for profile lookup.
- `files` — the subset of input files that activated this profile.
  Skills use this to scope behavior (e.g., `helm lint` runs only on files triggered under Helm filename signals, not on every YAML in the diff).

When no profile matches, return the empty list `[]`. The caller falls back to generic guidance, identical to today's "no language detected" path.
# Document clarity

Load this procedure before subject-matter reads. Apply it to selected artifacts or
completed drafts after resolving reader, purpose, destination and scope. It adds
no linked instructions, profile detection or consumer calls.

## Understand the work

Read each selected artifact in full and the requirements, decisions,
implementation and tests behind its claims. Repetition does not verify a claim.
Inspect supplied sources to explain the behavior,
conditions and rationale at the applicable revision. Follow relevant references
far enough to understand the claim, without recursively auditing the whole feature.
Reading a source does not authorize editing it or executing its commands.

For a PR, establish the target repository, actual base/head revisions and review
diff using read-only context; inspect relevant code at those revisions. Branch
names, stack annotations and task numbers do not establish the increment. Separate
inherited changes from this diff and contract-only work from runtime integration.
If source access is missing, state that limit and constrain unsupported claims.

Requirements establish intent; implementation establishes current behavior. Tests
provide evidence of exercised cases, not proof of intent or complete coverage.
Distinguish accepted requirements, proposals, implemented behavior and future work.
When no implementation exists, explain the planned contract as planned. Do not
invent runtime evidence. Reuse source understanding from the invoking session only
after checking that its scope and revision still apply; inspect missing or changed
context instead of repeating unrelated investigation.

Investigate accessible references before asking. For remaining consequential gaps,
ask a focused question or retain a limitation in the artifact. Record the issue,
next step and known owner there or in an already-selected task document; identify
unknown owners.
Do not manufacture an answer, silently settle a product decision or create an extra
report to hide the gap. Continue independent, supported edits when possible.

## Establish protected meaning

Keep a working inventory of essential claims and their evidence; no separate ledger
is required. Preserve:

- Requirements, observable behavior, rationale, constraints and uncertainty.
- Mandatory versus optional language; conditions, exceptions and thresholds.
- Identifiers, interface shapes, ownership and decision provenance.
- Deployment gates, completion status, verification limits and unresolved decisions.
- Required document sections, domain-rubric topics, task checkboxes and dependencies.

Conclusive evidence can justify correcting a factual documentation error. A conflict
between accepted requirements and implementation must stay explicit: describe both
and the next action needed to reconcile them. Neither source automatically overrides
the other. Do not erase a requirement to make the prose agree with the code.

Apply destination visibility in order, to facts and references alike:

1. Explicit user/repository audience restrictions override tracking or reachability.
2. Otherwise, files tracked at the target repository's PR head are accessible to
   its established review audience, not automatically to a wider audience. Nearby
   private aggregator files and untracked drafts do not qualify.
3. External sources require evidence of audience access: public availability or
   user/repository confirmation that they are shared. The editor's credentials
   prove no audience access; unknown visibility stays unknown.
4. Use an accessible source or explicitly authorized standalone explanation. If
   neither exists, retain a non-disclosing limitation or ask for authorization.
   Deleting a citation never authorizes disclosure of its underlying private fact.

Retain accessible task references; task numbers and feature-directory paths are not
inherently private. Exclude private task IDs and absolute workspace paths from
destination artifacts, shared reports and gap notes. A caller-only completion
message may link its selected local output; this never authorizes private source
pointers or facts.

## Edit for the reader

Lead with purpose and the applicable current or planned behavior. Help the reader
answer, where relevant to the artifact:

1. Why does this work exist?
2. What happens in a representative case?
3. What changes in the current increment?
4. What remains outside it?
5. What still needs a decision?

Use an evidence-backed scenario when it resolves confusion. Explain unfamiliar terms
at first use. Explain causes and consequences
before storage fields or verification history; place technical reference detail
after orientation. Remove duplication while retaining the detail needed for the
reader's task. Preserve the project's organization and document-type requirements;
do not force every artifact into one template or invent answers to irrelevant
questions. An explicit unknown can be the correct answer.

For PRs, explain the problem, behavior and increment;
include a focused review path and meaningful validation with its limits. Avoid a
commit diary or an indiscriminate file inventory. Describe future integration as
future work, not behavior delivered by a contract-only change.

Reorganize within the selected scope. Preserve existing anchors or update affected
in-scope links, including cross-file references. Check accessible inbound references
when changing headings; keep the anchor when callers outside scope would break, or
surface the wider change needed. Keep executable examples intact unless an
authorized, evidence-backed correction is verified. Do not change implementation,
run deployments or migrations, or make production or external writes.

When the baseline already satisfies comprehension, correctness, fidelity, visibility
and structural requirements, leave it unchanged. Clear prose may still need a
factual or disclosure repair; passing the five reader questions alone is not a
reason to retain such a defect. Make only justified changes, without a word-count
reduction target or a new summary artifact.

## Verify separately

Compare the revision with the original, requirements and inspected source evidence.
Check comprehension first: can the intended reader answer the applicable questions
through the artifact's intended reading path, without relying on the editor's hidden
context? Check the specific confusion motivating the edit, not just sentence length.

Then check fidelity independently against the protected-meaning inventory. No
qualification may disappear and no unsupported claim may appear. Recheck headings,
anchors, links, task state, required topics and executable examples affected by the
edit. Correct editorial regressions; keep unresolved source disagreements visible
with their next step. Fluent prose cannot compensate for lost meaning.
Recheck destination visibility, including facts paraphrased from restricted sources.

Report changed paths, whether the result was unchanged, and material evidence gaps
or wider edits needed. This is an in-session comparison, not independent fidelity
verification or proof of improved human comprehension. The caller owns any further
review required by the project.
# Tasks: JWT Authentication System

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: in-progress
> Created: 2026-03-11
> Not Doing: OAuth/social login, API rate limiting, token revocation list

## Task 1: User login end-to-end
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 2
- **Docs:** [implementation.md#user-login](./implementation.md#user-login)

### Subtasks
- [x] 1.1 Create `internal/auth/token.go` with `GenerateToken(userID, role)` and `ValidateToken(tokenString)` — access token generation with configurable expiry via `internal/config/auth.go`
- [x] 1.2 Create `POST /api/v1/auth/login` endpoint — accept email/password, verify against user store, return access + refresh tokens
- [x] 1.3 Create `internal/middleware/auth.go` — extract token from `Authorization: Bearer <token>` header, validate via token library, inject user claims into request context. Wire to `/api/v1/auth/login` route in `cmd/server/routes.go`
- [x] 1.4 Integration tests for the login flow: valid credentials → tokens returned, invalid credentials → 401, malformed token → 401, expired token → 401

## Task 2: Token refresh end-to-end
- **Status:** in-progress
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1
- **Docs:** [implementation.md#token-refresh](./implementation.md#token-refresh)

### Subtasks
- [x] 2.1 Create `POST /api/v1/auth/refresh` endpoint — accept refresh token, validate, return new access token with rotation
- [ ] 2.2 Integration tests: valid refresh → new access token, expired refresh → 401, reused refresh token → 401

## Task 3: Protected routes end-to-end
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#protected-routes](./implementation.md#protected-routes)

### Subtasks
- [ ] 3.1 Apply auth middleware to all `/api/v1/*` routes except `/api/v1/auth/login` and `/api/v1/auth/refresh` in `cmd/server/routes.go`
- [ ] 3.2 Rejection tests: request without token → 401, expired token → 401, valid token → passes through with claims in context
- [ ] 3.3 Verify existing endpoint tests still pass with auth middleware applied

## Task 4: Password hashing migration
- **Status:** blocked
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 2
- **Docs:** [design.md#password-storage](./design.md#password-storage)
- **Blocked:** Waiting on DB migration tooling decision (see design.md#open-questions)

### Subtasks
- [ ] 4.1 Add bcrypt hashing to `internal/auth/password.go` with cost factor from config
- [ ] 4.2 Create migration to add `password_hash` column to users table
- [ ] 4.3 Update user registration flow to hash passwords on create
- [ ] 4.4 Tests: registration stores hashed password, login verifies against hash

## Task 5: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 5.1 Run `/kk:test` skill to verify all tasks — full test suite, integration tests, edge cases
- [ ] 5.2 Run `/kk:document` skill to update any relevant docs
- [ ] 5.3 Run `/kk:review-code` skill with the project language input to review the implementation
- [ ] 5.4 Run `/kk:review-spec` skill to verify implementation matches design and implementation docs

## Dependency Graph

```
Task 1 ─→ Task 3 ─→ Task 5
Task 2 ─────────────→ Task 5
Task 4 (blocked) ────→ Task 5
```


## Record 13; source line 39; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/profiles/go/DETECTION.md /tmp/clarify-task4/instructions/profiles/python/DETECTION.md /tmp/clarify-task4/instructions/profiles/java/DETECTION.md /tmp/clarify-task4/instructions/profiles/js_ts/DETECTION.md /tmp/clarify-task4/instructions/profiles/kotlin/DETECTION.md /tmp/clarify-task4/instructions/profiles/k8s/DETECTION.md /tmp/clarify-task4/instructions/profiles/k8s-operator/DETECTION.md /tmp/clarify-task4/instructions/profiles/skill-md/DETECTION.md",login:false,max_output_tokens:16000})).output);


## Record 14; source line 42; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

# Go — detection

Declares when the `go` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Multiple profiles may activate additively on the same diff.

## Path signals

_None._ Go detection does not use path heuristics; file extension alone is authoritative (see Content signals).

## Filename signals

_None._ Go detection is extension-based, not filename-based.

## Content signals

A file activates the Go profile if its extension is `.go`. The extension match is authoritative; no byte-level content inspection is required.

## Design signals

display_name: Go
tokens:
  - Go
  - Golang
  - goroutine
  - go module
  - go.mod
# Python — detection

Declares when the `python` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Multiple profiles may activate additively on the same diff.

## Path signals

_None._ Python detection does not use path heuristics; file extension alone is authoritative (see Content signals).

## Filename signals

_None._ Python detection is extension-based, not filename-based.

## Content signals

A file activates the Python profile if its extension is one of: `.py`, `.pyi`. The extension match is authoritative; no byte-level content inspection is required.
# Java — detection

Declares when the `java` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Multiple profiles may activate additively on the same diff.

## Path signals

_None._ Java detection does not use path heuristics; file extension alone is authoritative (see Content signals).

## Filename signals

_None._ Java detection is extension-based, not filename-based.

## Content signals

A file activates the Java profile if its extension is `.java`. The extension match is authoritative; no byte-level content inspection is required.
# JS/TS — detection

Declares when the `js_ts` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Multiple profiles may activate additively on the same diff.

The profile covers JavaScript and TypeScript jointly: review concerns (typing, async, modules, React patterns) overlap substantially, and the ecosystem tools (npm, bundlers, Node/browser runtimes) are shared.

## Path signals

_None._ JS/TS detection does not use path heuristics; file extension alone is authoritative (see Content signals).

## Filename signals

_None._ JS/TS detection is extension-based, not filename-based.

## Content signals

A file activates the JS/TS profile if its extension is one of: `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts`. The extension match is authoritative; no byte-level content inspection is required.
# Kotlin — detection

Declares when the `kotlin` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Multiple profiles may activate additively on the same diff.

## Path signals

_None._ Kotlin detection does not use path heuristics; file extension alone is authoritative (see Content signals).

## Filename signals

_None._ Kotlin detection is extension-based, not filename-based.

## Content signals

A file activates the Kotlin profile if its extension is one of: `.kt`, `.kts`. The extension match is authoritative; no byte-level content inspection is required.
# Kubernetes — detection

Declares when the `k8s` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Detection is additive: multiple profiles may activate on the same diff (e.g., `go` + `k8s`).

Evaluation follows the shared cost-ordered procedure (path → filename → content). Authority runs filename ≈ content > path: filename or content signals activate the profile; path alone never does, it only promotes a file to a candidate.

## Path signals

Case-insensitive substring match anywhere in the file's path. Pre-filter only — a path hit alone does NOT activate the profile.

- `k8s/`
- `manifests/`
- `charts/`
- `kustomize/`
- `deploy/`
- `templates/`

## Filename signals

Authoritative: any match activates the profile. Filename matches short-circuit content inspection for the matched file.

- `Chart.yaml` (exact) → Helm chart root.
- Any filename starting with `values` (e.g., `values.yaml`, `values.yml`, `values-prod.yaml`, `values-prod-v2-final.yaml`) when the containing directory also contains `Chart.yaml` → Helm values by adjacency. The `values*` glob has no upper bound on the wildcard; the adjacency rule (sibling `Chart.yaml` in the same directory) is the binding constraint. The match is filename-plus-adjacency only — file content is not inspected, so a file named `values-backup.yaml` next to a `Chart.yaml` activates regardless of what it actually contains.
- Any file with extension `.yaml`, `.yml`, or `.tpl` inside `<dir>/templates/` where `<dir>` itself contains a `Chart.yaml` as a direct child → Helm template. The binding constraint is that the `templates/` directory must sit *directly* next to a `Chart.yaml` — i.e., at a chart root or a subchart root under `<parent>/charts/<subchart>/`. A `templates/` nested elsewhere in the tree (e.g., `docs/templates/`, `ci/templates/`) does NOT activate this rule even when a `Chart.yaml` sits at the repository root, because `docs/` and `ci/` do not themselves contain a `Chart.yaml`. This avoids the monorepo false-positive where a repo-root umbrella `Chart.yaml` would otherwise claim every `templates/` directory in the tree. It still avoids the trap where a standalone edit to `<chart-root>/templates/deployment.yaml` contains `{{ if ... }}` directives before any `apiVersion:` and would otherwise fail the content signal.
- Exact filenames `kustomization.yaml`, `kustomization.yml`, or `Kustomization` → Kustomize.

## Content signals

Authoritative for generic YAML files (`.yaml` or `.yml`) not already caught by a filename signal. Inspection is bounded to the first ~16 KB per file; large generated manifests beyond that bound are not inspected.

- Split the file on `---` document separators. For each `---`-separated document block, check for a top-level `apiVersion:` AND a top-level `kind:` — parsed as YAML mapping keys at zero indent, not as substrings inside block scalars (`|`, `>`) or comments. A block satisfying both is a Kubernetes manifest document.
- One matching document activates the profile for that file. The first document need not match — a file whose second or later document is the only K8s document still activates.
- A `.yaml` / `.yml` file with no matching document in any block → not Kubernetes. (It may still match another profile; generic YAML belongs to no profile by default.)

---

## Multi-profile behavior

The Kubernetes profile is **additive**. It coexists with programming-language profiles or any other IaC profile on the same diff. When Go source files sit alongside Kubernetes manifests, both `go` and `k8s` activate; downstream skills consult both profiles' content and emit findings grouped by `(profile, checklist)`.

## Design signals

display_name: Kubernetes
tokens:
  - Kubernetes
  - K8s
  - Helm chart
  - kubectl
  - kustomize
  - manifest.yaml
  - Deployment resource
  - StatefulSet
  - DaemonSet
  - CronJob

## Dockerfile non-trigger

A Dockerfile on its own — even under a `deploy/` or `k8s/` directory — does NOT activate the `k8s` profile. Dockerfiles match no filename signal here (they are not `Chart.yaml` / `values*.yaml` / `kustomization.yaml`) and no content signal (they do not contain `apiVersion:` + `kind:`). When a Dockerfile appears in the same diff as Kubernetes manifests, `k8s` activates on the manifests' signals; the Dockerfile itself is not reviewed by this profile. A future container profile may own Dockerfiles independently.
# Kubernetes Operator — detection

Declares when the `k8s-operator` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Detection is additive: an operator project typically activates both `k8s-operator` (for controller code) and `k8s` (for the manifests it generates/deploys).

Evaluation follows the shared cost-ordered procedure (path → filename → content). Authority runs filename ≈ content > path: filename or content signals activate the profile; path alone never does, it only promotes a file to a candidate.

## Path signals

Case-insensitive substring match anywhere in the file's path. Pre-filter only — a path hit alone does NOT activate the profile.

- `internal/controller/`
- `api/`
- `controllers/`

## Filename signals

Authoritative: any match activates the profile. Filename matches short-circuit content inspection for the matched file.

- `PROJECT` (exact) → kubebuilder project marker. This file is generated by `kubebuilder init` and contains the project's domain, layout, and plugin metadata. Its mere presence signals an operator project.
- Any file under `config/crd/` → CRD kustomize bases generated by `controller-gen`.
- Any file under `config/webhook/` → admission/conversion webhook kustomize configuration.

## Content signals

Authoritative for files not already caught by a filename signal. Inspection is bounded to the first ~16 KB per file.

- A `Makefile` containing the literal string `controller-gen` OR a target named `manifests` (line starting with `manifests:`) → kubebuilder/operator-sdk generated Makefile with CRD/RBAC generation targets.
- A Go source file (`.go` extension) containing an import of `sigs.k8s.io/controller-runtime` → controller-runtime dependency, the standard library for writing Kubernetes controllers.

## Design signals

display_name: Kubernetes Operator
tokens:
  - operator
  - controller
  - kubebuilder
  - controller-runtime
  - CRD authoring
  - custom resource definition authoring
  - reconciliation loop
# Agent Skills — detection

Declares when the `skill-md` profile activates on a given set of files. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Detection is additive: multiple profiles may activate on the same diff (e.g., `go` + `skill-md` when editing a Go skill).

## Path signals

_None._ Skill detection uses filename signals exclusively; path heuristics would over-trigger on any directory named `skills/`.

## Filename signals

Authoritative: any match activates the profile. Filename matches short-circuit content inspection for the matched file.

- `SKILL.md` (exact) — the canonical skill entry point. Any file literally named `SKILL.md` activates the profile.
- **Skill-root adjacency rule:** any file whose nearest ancestor directory contains a `SKILL.md`. Walk upward from the file's parent directory toward the repo root; stop at the first directory containing a `SKILL.md`. If found, the file is part of that skill and the profile activates. This covers:
  - Direct siblings (e.g., `skills/review-code/plan-mode.md` where `skills/review-code/SKILL.md` exists)
  - Resource subdirectories (e.g., `skills/my-skill/references/guide.md`, `skills/my-skill/scripts/helper.py`)
  - Eval fixtures (e.g., `skills/my-skill/evals/test-1/eval.json`)

The binding constraint is nearest-ancestor `SKILL.md`, following the same ancestor-walk pattern as the Helm template rule in the k8s profile (files under `templates/` activate when the parent contains `Chart.yaml`).

**Scoping:** the walk stops at the *first* directory containing `SKILL.md`. A `SKILL.md` at the repo root does NOT claim every file in the repository — files in subdirectories that have their own `SKILL.md` are scoped to that nearer ancestor. Files outside any `SKILL.md`-containing ancestor do not activate.

**Edge cases and non-triggers:**
- Test-fixture `SKILL.md` files inside `evals/test-files/` are legitimate detection targets — they *are* skill files. The ancestor walk scopes them correctly.
- Generic markdown outside a skill root (`docs/design.md`, `README.md`, `CONTRIBUTING.md`) does NOT activate, regardless of content or frontmatter.
- Agent definitions (`agents/*.md`) with skill-like `name:` / `description:` frontmatter do NOT activate unless they sit under a `SKILL.md`-rooted ancestor.

## Content signals

_None._ Skill detection is entirely file-location-based. Content inspection cannot reliably distinguish skill instructions from other markdown.

## Design signals

display_name: Agent Skills
tokens:
  - skill
  - SKILL.md
  - agent skill
  - slash command
  - skill description
  - skill trigger


## Record 15; source line 44; custom_tool_call


exec

text((await tools.exec_command({cmd:"rg -io '\\b(Go|Golang|goroutine|go module|go\\.mod|Kubernetes|K8s|Helm chart|kubectl|kustomize|manifest\\.yaml|Deployment resource|StatefulSet|DaemonSet|CronJob|operator|controller|kubebuilder|controller-runtime|CRD authoring|custom resource definition authoring|reconciliation loop|skill|SKILL\\.md|agent skill|slash command|skill description|skill trigger)\\b' /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/accepted.md",login:false,max_output_tokens:2000})).output);


## Record 16; source line 47; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:



## Record 17; source line 51; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/design/frameworks.md /tmp/clarify-task4/instructions/skills/design/refinement-criteria.md",login:false,max_output_tokens:6500})).output);


## Record 18; source line 54; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

<!-- Adapted from addyosmani/agent-skills (MIT License, Copyright Addy Osmani)
     Source: https://github.com/addyosmani/agent-skills/blob/539a78574773fe7e46cf8bbf9c67bcc9db63c335/skills/idea-refine/frameworks.md
     Pinned at: 539a78574773fe7e46cf8bbf9c67bcc9db63c335 -->

# Ideation Frameworks Reference

These frameworks apply to software engineering features — APIs, infrastructure, developer tools, internal systems, library design. The goal is to unlock thinking about implementation approaches and architectural trade-offs, not to follow a checklist. Pick the lens that fits the idea; don't mechanically run every framework.

## SCAMPER

A structured way to transform an existing idea by applying seven different operations:

- **Substitute:** What component, technology, or process could you swap out? What if you replaced the synchronous RPC with an event-driven approach? The relational database with a document store? The monolith deployment with a service mesh?
- **Combine:** What if you merged this with another product, service, or idea? What two things that don't usually go together would create something new?
- **Adapt:** What else is like this? What ideas from other domains or systems could you borrow? What parallel exists in nature?
- **Modify (Magnify/Minimize):** What if you made it 10x bigger? 10x smaller? What if you exaggerated one feature? What if you stripped it to the absolute minimum?
- **Put to other uses:** Who else could use this? What other problems could it solve? What happens if you use it in a completely different context?
- **Eliminate:** What happens if you remove a feature entirely? What's the version with zero configuration? What would it look like with half the steps?
- **Reverse/Rearrange:** What if you did the steps in the opposite order? What if the user/client did the work instead of the system/server (or vice versa)? What if you reversed the dependency direction, or the value chain?

**Best for:** Improving or reimagining existing systems/products/features. Less useful for greenfield ideas.

## How Might We (HMW)

Reframe problems as opportunities using the "How Might We..." format:

- Start with an observation or pain point
- Reframe it as "How might we [desired outcome] for [specific user] without [key constraint]?"
- Generate multiple HMW framings of the same problem — different framings unlock different solutions

**Good HMW qualities:**
- Narrow enough to be actionable ("...help new users find relevant content in their first 5 minutes")
- Broad enough to allow creative solutions (not "...add a recommendation sidebar")
- Contains a tension or constraint that forces creativity

**Bad HMW qualities:**
- Too broad: "How might we make users happy?"
- Too narrow: "How might we add a button to the settings page?"
- Solution-embedded: "How might we build a chatbot for support?"

**Best for:** Reframing stuck thinking. When someone is anchored on a solution, pull them back to the problem.

## First Principles Thinking

Break the idea down to its fundamental truths, then rebuild from there:

1. **What do we know is true?** (not assumed, not conventional — actually true)
2. **What are we assuming?** List every assumption, even the ones that feel obvious
3. **Which assumptions can we challenge?** For each, ask: "Is this actually a law of physics, or just how it's been done?"
4. **Rebuild from the truths.** If you only had the fundamental truths, what would you build?

**Best for:** Breaking out of incremental thinking. When every idea feels like a small improvement on the status quo.

## Jobs to Be Done (JTBD)

Focus on what the user is trying to accomplish, not what they say they want:

- **Functional job:** What task are they trying to complete?
- **Emotional job:** How do they want to feel?
- **Social job:** How do they want to be perceived?

Format: "When I [situation], I want to [motivation], so I can [expected outcome]."

**Key insight:** Users don't adopt tools — they hire them to do a job. The competing solution isn't always in the same category. (A CLI tool competes with a shell script alias, not just other CLI tools.)

**Best for:** Understanding the real problem. When you're not sure if you're solving the right thing.

## Constraint Mapping

Deliberately impose constraints to force creative solutions:

- **Time constraint:** "What if you only had 1 day to build this?"
- **Feature constraint:** "What if it could only have one feature?"
- **Tech constraint:** "What if you couldn't use [the obvious technology]?"
- **Cost constraint:** "What if it had to be free forever?"
- **Audience constraint:** "What if your user had never used a computer before?"
- **Scale constraint:** "What if it needed to work for 1 billion users? What about just 10?"

**Best for:** Cutting through complexity. When the idea is growing too large or too vague.

## Pre-mortem

Imagine the idea has already failed. Work backwards:

1. It's 12 months from now. The project shipped and flopped. What went wrong?
2. List every plausible reason for failure — technical, adoption, integration, operational
3. For each failure mode: Is this preventable? Is this a signal the idea needs to change?
4. Which failure modes are you willing to accept? Which ones would kill the project?

**Best for:** Phase 2 evaluation. Stress-testing ideas that feel good but haven't been pressure-tested.

## Analogous Inspiration

Look at how other domains solved similar problems:

- What industry or system has already solved a version of this problem?
- What would this look like if someone else built it?
- What natural system or distributed system works this way?
- What historical precedent exists?

The key is finding *structural* similarities, not surface-level ones. "Git for config files" is surface-level. "A content-addressable store with branching semantics that solves the concurrent-edit problem" is structural.

**Best for:** Phase 1 expansion. Generating variations that feel genuinely different from the obvious approach.
<!-- Adapted from addyosmani/agent-skills (MIT License, Copyright Addy Osmani)
     Source: https://github.com/addyosmani/agent-skills/blob/539a78574773fe7e46cf8bbf9c67bcc9db63c335/skills/idea-refine/refinement-criteria.md
     Pinned at: 539a78574773fe7e46cf8bbf9c67bcc9db63c335 -->

# Refinement & Evaluation Criteria

Use this rubric to stress-test idea directions during convergence. These criteria apply to software engineering features — APIs, infrastructure, developer tools, internal systems, library design. Not every criterion applies to every idea — use judgment about which dimensions matter most for the specific context.

## Core Evaluation Dimensions

### 1. User Value

The most important dimension. If the value isn't clear, nothing else matters.

**Painkiller vs. Vitamin:**

- **Painkiller:** Solves an acute, frequent problem. Users will actively seek this out. They'll switch from their current solution. Signs: people describe the problem with emotion, they've built workarounds, they'll pay for a solution.
- **Vitamin:** Nice to have. Makes something marginally better. Users won't go out of their way. Signs: people nod politely, say "that's cool," then don't change behavior.

**Questions to ask:**

- Can you name 3 specific people who have this problem right now?
- What are they doing today instead? (The real competitor is always the current workaround.)
- Would they switch from their current approach? What would make them switch?
- How often do they encounter this problem? (Daily problems > monthly problems)
- Is this a "pull" problem (users are asking for this) or a "push" problem (you think they should want this)?

**Red flags:**

- "Everyone could use this" — if you can't name a specific user, the value isn't clear
- "It's like X but better" — marginal improvements rarely drive adoption
- The problem is real but rare — high intensity but low frequency rarely justifies a product

### 2. Feasibility

Can you actually build this? Not just technically, but practically.

**Technical feasibility:**

- Does the core technology exist and work reliably?
- What's the hardest technical problem? Is it a known-hard problem or a novel one?
- Are there dependencies on third parties, APIs, or data sources you don't control?
- What's the minimum technical stack needed? (If the answer is "a lot," that's a signal.)

**Resource feasibility:**

- What's the minimum team/effort to build an MVP?
- Does it require specialized expertise you don't have?
- Are there regulatory, legal, or compliance requirements?

**Time-to-value:**

- How quickly can you get something in front of users?
- Is there a version that delivers value in days/weeks, not months?
- What's the critical path? What has to happen first?

**Red flags:**

- "We just need to solve [very hard research problem] first"
- Multiple dependencies that all need to work simultaneously
- MVP still requires months of work — likely not minimal enough

### 3. Differentiation

What makes this genuinely different? Not better — _different_.

**Questions to ask:**

- If a user described this to a friend, what would they say? Is that description compelling?
- What's the one thing this does that nothing else does? (If you can't name one, that's a problem.)
- Is this differentiation durable? Can a competitor copy it in a week?
- Is the difference something users actually care about, or just something builders find interesting?

**Types of differentiation (strongest to weakest):**

1. **New capability:** Does something that was previously impossible
2. **10x improvement:** So much better on a key dimension that it changes behavior
3. **New audience:** Brings an existing capability to people who were excluded
4. **New context:** Works in a situation where existing solutions fail
5. **Better UX:** Same capability, dramatically simpler experience
6. **Cheaper:** Same thing, lower cost (weakest — easily competed away)

**Red flags:**

- Differentiation is entirely about technology, not user experience
- "We're faster/cheaper/prettier" without a structural reason why
- The feature that differentiates is not the feature users care most about

## Assumption Audit

For every idea direction, explicitly list assumptions in three categories:

### Must Be True (Dealbreakers)

Assumptions that, if wrong, kill the idea entirely. These need validation before building.

Example: "The external API supports batch operations" — if it doesn't, the entire design around bulk processing doesn't work.

### Should Be True (Important)

Assumptions that significantly impact success but don't kill the idea. You can adjust the approach if these are wrong.

Example: "Teams will adopt the CLI over the existing manual workflow" — if wrong, you need a different rollout strategy, but the core tool can still work.

### Might Be True (Nice to Have)

Assumptions about secondary features or optimizations. Don't validate these until the core is proven.

Example: "Teams will want to export reports to Slack" — a convenience feature, not a core value proposition.

## Decision Framework

When choosing between directions, rank on this matrix:

|                | High Feasibility | Low Feasibility |
| -------------- | ---------------- | --------------- |
| **High Value** | Do this first    | Worth the risk  |
| **Low Value**  | Only if trivial  | Don't do this   |

Then use differentiation as the tiebreaker between options in the same quadrant.

## MVP Scoping Principles

When defining MVP scope for the chosen direction:

1. **One job, done well.** The MVP should nail exactly one user job. Not three jobs done partially.
2. **The riskiest assumption first.** The MVP's primary purpose is to test the assumption most likely to be wrong.
3. **Time-box, not feature-list.** "What can we build and test in [timeframe]?" is better than "What features do we need?"
4. **The 'Not Doing' list is mandatory.** Explicitly name what you're cutting and why. This prevents scope creep and forces honest prioritization.
5. **If it's not embarrassing, you waited too long.** The first version should feel incomplete to the builder. If it doesn't, you over-built.


## Record 19; source line 56; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/accepted.md",login:false,max_output_tokens:8000})).output);


## Record 20; source line 59; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

# Accepted archive-label idea

The catalog maintainer wants contributors to recognize archived entries without
opening each entry. Success: every archived entry in the static catalog displays
the word Archived, while active entries have no label. The catalog is manually
maintained in catalog.md; no runtime application exists in this workspace.

HMW framing, contributor persona, success condition and constraints are approved.
This is a simple single-path change. The chosen direction is a textual label beside
each archived entry. Hiding archived entries was rejected because readers still need
their links. The design presentation is approved; fact-checking alternatives is not
requested. Do not introduce dependencies or automate catalog generation.

Constraints: keep existing destinations and titles. An archived entry stays visible
and clickable. Only label text is in this increment; color is undecided. Owner:
catalog maintainers; next step: choose a color after checking the site's contrast.
Assumption: authors already mark archived entries consistently. Verify that before
implementation. Not Doing: filtering, automatic archival, color changes.

Produce a small label-edit task with concrete verification and a final verification
task. Preserve the distinction between accepted requirements and future edits.


## Record 21; source line 64; message


The accepted scope is a text-only label in `catalog.md`. I’ll record the archive-marking convention as a check required before implementation and keep the undecided color choice separate from this change.


## Record 22; source line 65; custom_tool_call


exec

text(await tools.apply_patch("*** Begin Patch\n*** Add File: /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/design.md\n+# Archive labels in the static catalog\n+\n+> Status: accepted design; implementation pending\n+> Audience: the next contributor and catalog maintainers\n+> Decisions: [accepted archive-label idea](../../../../accepted.md)\n+> Plan: [implementation.md](implementation.md) · [tasks.md](tasks.md)\n+\n+## Purpose and planned behavior\n+\n+Contributors need to recognize archived entries without opening every entry. Add the word **Archived** beside each archived entry in the manually maintained `catalog.md`. Active entries must have no label.\n+\n+For example, a contributor scanning an archived entry will see its existing title, a clickable link to its existing destination, and the word Archived beside it. The entry remains visible. An active entry keeps its existing title and link without an archive label.\n+\n+Success means every archived entry displays Archived and no active entry does. This document specifies a future edit; no catalog edit or runtime behavior is delivered by these design documents. There is no runtime application in this workspace.\n+\n+## Accepted decisions and constraints\n+\n+The problem framing, contributor persona, success condition, constraints, chosen direction, and design presentation are approved. This is a simple textual change to a static document.\n+\n+- Preserve every existing title and destination.\n+- Keep archived entries visible and clickable.\n+- Change only the label text in this increment; introduce no dependencies or catalog-generation automation.\n+- Use the existing archive designation to identify entries, once its consistency has been verified. Do not infer archived status from a title or a broken link.\n+\n+## Assumptions\n+\n+Authors already mark archived entries consistently. Before editing, inspect `catalog.md` and verify that its existing markings distinguish archived entries from active ones. The catalog was not available for inspection during drafting, so its marking convention and entry inventory remain unverified.\n+\n+If the convention is inconsistent or ambiguous, the implementing contributor must obtain clarification from the catalog maintainers before labeling affected entries. Record the issue and its next step in [Task 1](tasks.md#task-1-label-archived-entries).\n+\n+## Not Doing\n+\n+- Filtering: readers must retain access to archived entries and their links.\n+- Automatic archival: this increment only labels entries already designated archived in the manually maintained catalog.\n+- Color changes: this increment changes label text only; no color has been selected.\n+\n+## Rejected Alternatives\n+\n+Hiding archived entries was rejected because readers still need their links. A visible text label preserves that access while identifying archival status.\n+\n+## Open color decision\n+\n+Color is undecided and does not block the accepted text-only edit. Catalog maintainers own the next step: choose a color after checking the site's contrast. This is future work, not part of the implementation tasks below.\n+\n+## Acceptance checks\n+\n+Inspect the complete catalog after editing: every archived entry has Archived beside it, active entries have no label, and all original entries, titles, and destinations remain intact. Preview the rendered document to confirm labels are visible and archived links remain clickable. See the [implementation verification plan](implementation.md#final-verification) for the handoff checks.\n*** Add File: /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/implementation.md\n+# Archive-label implementation plan\n+\n+> Status: planned; no implementation performed\n+> Contract: [design.md](design.md)\n+> Execution: [tasks.md](tasks.md)\n+\n+## Scope and starting point\n+\n+The contributor will edit `catalog.md`, the manually maintained static catalog, to put Archived beside entries already designated archived. Preserve titles, destinations, entry visibility, and clickability. Active entries receive no label. No dependency or generation tooling is needed.\n+\n+The accepted decisions establish this contract. Catalog content and its archive-marking convention were not supplied for inspection; the first step below must establish which entries qualify before any label edit. No application code or runtime tests are involved.\n+\n+## Label archived entries\n+\n+This is one small, complete edit to `catalog.md`, including its verification.\n+\n+1. Inspect the existing archive markings in `catalog.md` and identify all archived and active entries → verify: every entry can be classified using a consistent existing convention. If not, record the ambiguity in Task 1 and ask the catalog maintainers to resolve it before labeling affected entries.\n+2. Add the word Archived beside each archived entry's existing link, preserving the link title and destination and leaving active entries unlabeled → verify: compare every entry against the classification from step 1; archived entries all display Archived and active entries have no label.\n+3. Inspect the diff and preview `catalog.md` in the site's existing Markdown rendering workflow, if available → verify: no entry was hidden or removed, every original title and destination is unchanged, labels are visible, and archived links remain clickable. If the site's rendering workflow is unavailable, record that limit and use an available Markdown preview without claiming site rendering was verified.\n+\n+These checks validate a static document edit. Do not add generation scripts or an automated test suite for the label change.\n+\n+## Assumptions\n+\n+The plan depends on authors marking archived entries consistently. Step 1 validates this before implementation. Catalog maintainers resolve ambiguous archival status; the contributor records the outcome in Task 1.\n+\n+## Not Doing\n+\n+Filtering would interfere with continued access to archived entries. Automatic archival exceeds the manual label edit. Color changes await the maintainers' contrast check and color decision. None belongs in this increment.\n+\n+## Rejected Alternatives\n+\n+Hiding archived entries was rejected because their links must remain available. Preserve the visible catalog and add textual labels.\n+\n+## Final verification\n+\n+After the label edit, run `/kk:test` to perform applicable repository checks and the complete catalog checks above. Run `/kk:document` to update relevant documentation, `/kk:review-code` with Markdown as the change's language input, and `/kk:review-spec` to compare the result with this plan and the design → verify: record actual results and any unavailable checks in Task 2 before marking it done. Do not claim a runtime or full-suite test passed when none exists or was run.\n+\n+The post-design recommendation is `/kk:review-design archive-label`. It has not been run as part of drafting. Implementation and final verification remain future actions.\n*** Add File: /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/tasks.md\n+# Tasks: Archive labels\n+\n+> Design: [design.md](design.md)\n+> Implementation: [implementation.md](implementation.md)\n+> Status: pending\n+> Created: 2026-09-29\n+> Not Doing: filtering, automatic archival, color changes\n+\n+## Task 1: Label archived entries\n+\n+- **Status:** pending\n+- **Depends on:** —\n+- **Size:** S\n+- **Can run in parallel with:** —\n+- **Docs:** [Label archived entries](implementation.md#label-archived-entries)\n+\n+### Subtasks\n+\n+- [ ] 1.1 Inspect `catalog.md` and verify the assumption that existing archive markings consistently distinguish archived from active entries → verify: classify every entry before editing; record any ambiguity here and obtain its resolution from catalog maintainers before labeling affected entries.\n+- [ ] 1.2 Add Archived beside each archived entry's existing link in `catalog.md` → verify: every archived entry has the word and no active entry has a label.\n+- [ ] 1.3 Compare the catalog diff and preview its rendered Markdown → verify: preserve every entry, title, and destination; archived entries remain visible and clickable. Record if site rendering could not be checked.\n+\n+## Task 2: Final verification\n+\n+- **Status:** pending\n+- **Depends on:** Task 1\n+- **Size:** S\n+- **Can run in parallel with:** —\n+- **Docs:** [Final verification](implementation.md#final-verification)\n+\n+### Subtasks\n+\n+- [ ] 2.1 Run `/kk:test` for the full applicable repository test suite and the catalog acceptance checks → verify: record actual check results and any absent suite or unavailable preview; archived entries all display Archived, active entries have no label, and titles, destinations, visibility, and clickability are preserved.\n+- [ ] 2.2 Run `/kk:document` to update relevant documentation → verify: documentation describes the implemented text labels and retains color as an undecided future change owned by catalog maintainers.\n+- [ ] 2.3 Run `/kk:review-code` with Markdown as the language input → verify: record the review outcome and resolve findings relevant to the catalog edit.\n+- [ ] 2.4 Run `/kk:review-spec` against the design and implementation documents → verify: record whether the implementation meets the accepted contract; resolve deviations before marking the task done.\n+\n+## Dependency Graph\n+\n+```text\n+Task 1 ──→ Task 2\n+```\n*** End Patch"));


## Record 23; source line 68; custom_tool_call_output


Script completed
Wall time 0.1 seconds
Output:

{}

## Record 24; source line 70; custom_tool_call


exec

text((await tools.exec_command({cmd:"mkdir -p /tmp/clarify-task4/consumers/clarity-after-drafting/draft-snapshot/docs/feat/wip/archive-label",login:false,max_output_tokens:1000})).output);
text((await tools.exec_command({cmd:"cp /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/design.md /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/implementation.md /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/tasks.md /tmp/clarify-task4/consumers/clarity-after-drafting/draft-snapshot/docs/feat/wip/archive-label/",login:false,max_output_tokens:1000})).output);


## Record 25; source line 74; custom_tool_call_output


Script completed
Wall time 0.6 seconds
Output:




## Record 26; source line 78; custom_tool_call


exec

text((await tools.exec_command({cmd:"cat /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/design.md /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/implementation.md /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/tasks.md",login:false,max_output_tokens:11000})).output);


## Record 27; source line 81; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

# Archive labels in the static catalog

> Status: accepted design; implementation pending
> Audience: the next contributor and catalog maintainers
> Decisions: [accepted archive-label idea](../../../../accepted.md)
> Plan: [implementation.md](implementation.md) · [tasks.md](tasks.md)

## Purpose and planned behavior

Contributors need to recognize archived entries without opening every entry. Add the word **Archived** beside each archived entry in the manually maintained `catalog.md`. Active entries must have no label.

For example, a contributor scanning an archived entry will see its existing title, a clickable link to its existing destination, and the word Archived beside it. The entry remains visible. An active entry keeps its existing title and link without an archive label.

Success means every archived entry displays Archived and no active entry does. This document specifies a future edit; no catalog edit or runtime behavior is delivered by these design documents. There is no runtime application in this workspace.

## Accepted decisions and constraints

The problem framing, contributor persona, success condition, constraints, chosen direction, and design presentation are approved. This is a simple textual change to a static document.

- Preserve every existing title and destination.
- Keep archived entries visible and clickable.
- Change only the label text in this increment; introduce no dependencies or catalog-generation automation.
- Use the existing archive designation to identify entries, once its consistency has been verified. Do not infer archived status from a title or a broken link.

## Assumptions

Authors already mark archived entries consistently. Before editing, inspect `catalog.md` and verify that its existing markings distinguish archived entries from active ones. The catalog was not available for inspection during drafting, so its marking convention and entry inventory remain unverified.

If the convention is inconsistent or ambiguous, the implementing contributor must obtain clarification from the catalog maintainers before labeling affected entries. Record the issue and its next step in [Task 1](tasks.md#task-1-label-archived-entries).

## Not Doing

- Filtering: readers must retain access to archived entries and their links.
- Automatic archival: this increment only labels entries already designated archived in the manually maintained catalog.
- Color changes: this increment changes label text only; no color has been selected.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. A visible text label preserves that access while identifying archival status.

## Open color decision

Color is undecided and does not block the accepted text-only edit. Catalog maintainers own the next step: choose a color after checking the site's contrast. This is future work, not part of the implementation tasks below.

## Acceptance checks

Inspect the complete catalog after editing: every archived entry has Archived beside it, active entries have no label, and all original entries, titles, and destinations remain intact. Preview the rendered document to confirm labels are visible and archived links remain clickable. See the [implementation verification plan](implementation.md#final-verification) for the handoff checks.
# Archive-label implementation plan

> Status: planned; no implementation performed
> Contract: [design.md](design.md)
> Execution: [tasks.md](tasks.md)

## Scope and starting point

The contributor will edit `catalog.md`, the manually maintained static catalog, to put Archived beside entries already designated archived. Preserve titles, destinations, entry visibility, and clickability. Active entries receive no label. No dependency or generation tooling is needed.

The accepted decisions establish this contract. Catalog content and its archive-marking convention were not supplied for inspection; the first step below must establish which entries qualify before any label edit. No application code or runtime tests are involved.

## Label archived entries

This is one small, complete edit to `catalog.md`, including its verification.

1. Inspect the existing archive markings in `catalog.md` and identify all archived and active entries → verify: every entry can be classified using a consistent existing convention. If not, record the ambiguity in Task 1 and ask the catalog maintainers to resolve it before labeling affected entries.
2. Add the word Archived beside each archived entry's existing link, preserving the link title and destination and leaving active entries unlabeled → verify: compare every entry against the classification from step 1; archived entries all display Archived and active entries have no label.
3. Inspect the diff and preview `catalog.md` in the site's existing Markdown rendering workflow, if available → verify: no entry was hidden or removed, every original title and destination is unchanged, labels are visible, and archived links remain clickable. If the site's rendering workflow is unavailable, record that limit and use an available Markdown preview without claiming site rendering was verified.

These checks validate a static document edit. Do not add generation scripts or an automated test suite for the label change.

## Assumptions

The plan depends on authors marking archived entries consistently. Step 1 validates this before implementation. Catalog maintainers resolve ambiguous archival status; the contributor records the outcome in Task 1.

## Not Doing

Filtering would interfere with continued access to archived entries. Automatic archival exceeds the manual label edit. Color changes await the maintainers' contrast check and color decision. None belongs in this increment.

## Rejected Alternatives

Hiding archived entries was rejected because their links must remain available. Preserve the visible catalog and add textual labels.

## Final verification

After the label edit, run `/kk:test` to perform applicable repository checks and the complete catalog checks above. Run `/kk:document` to update relevant documentation, `/kk:review-code` with Markdown as the change's language input, and `/kk:review-spec` to compare the result with this plan and the design → verify: record actual results and any unavailable checks in Task 2 before marking it done. Do not claim a runtime or full-suite test passed when none exists or was run.

The post-design recommendation is `/kk:review-design archive-label`. It has not been run as part of drafting. Implementation and final verification remain future actions.
# Tasks: Archive labels

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-09-29
> Not Doing: filtering, automatic archival, color changes

## Task 1: Label archived entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label archived entries](implementation.md#label-archived-entries)

### Subtasks

- [ ] 1.1 Inspect `catalog.md` and verify the assumption that existing archive markings consistently distinguish archived from active entries → verify: classify every entry before editing; record any ambiguity here and obtain its resolution from catalog maintainers before labeling affected entries.
- [ ] 1.2 Add Archived beside each archived entry's existing link in `catalog.md` → verify: every archived entry has the word and no active entry has a label.
- [ ] 1.3 Compare the catalog diff and preview its rendered Markdown → verify: preserve every entry, title, and destination; archived entries remain visible and clickable. Record if site rendering could not be checked.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Run `/kk:test` for the full applicable repository test suite and the catalog acceptance checks → verify: record actual check results and any absent suite or unavailable preview; archived entries all display Archived, active entries have no label, and titles, destinations, visibility, and clickability are preserved.
- [ ] 2.2 Run `/kk:document` to update relevant documentation → verify: documentation describes the implemented text labels and retains color as an undecided future change owned by catalog maintainers.
- [ ] 2.3 Run `/kk:review-code` with Markdown as the language input → verify: record the review outcome and resolve findings relevant to the catalog edit.
- [ ] 2.4 Run `/kk:review-spec` against the design and implementation documents → verify: record whether the implementation meets the accepted contract; resolve deviations before marking the task done.

## Dependency Graph

```text
Task 1 ──→ Task 2
```


## Record 28; source line 86; message


Created [design.md](/tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/design.md), [implementation.md](/tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/implementation.md), and [tasks.md](/tmp/clarify-task4/consumers/clarity-after-drafting/workspace/docs/feat/wip/archive-label/tasks.md).

The final clarity pass required no changes. Archive-marking consistency remains unverified because `catalog.md` was unavailable; the first implementation task checks it. Color remains undecided future work.

Implementation and reviews were not run. Recommended next review: `/kk:review-design archive-label`.
