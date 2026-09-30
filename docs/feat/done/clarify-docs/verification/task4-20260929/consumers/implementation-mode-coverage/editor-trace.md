# Visible session trace

Raw trace.jsonl is authoritative. This rendering expands JSON-wrapped command output where parsing is possible. Hidden reasoning and system boilerplate are excluded.

## Record 1; source line 1; session_meta


{
  "id": "01a0ee98-e993-7332-b072-70875a10ef97",
  "parent_thread_id": "01a0ee8a-00f7-7212-b97d-013f6c8d4960",
  "timestamp": "2026-09-29T19:16:33.815Z",
  "cwd": "/home/sergio/Projects/personal/claude-toolbox",
  "originator": "codex-tui",
  "cli_version": "0.159.0",
  "source": {
    "subagent": {
      "thread_spawn": {
        "parent_thread_id": "01a0ee8a-00f7-7212-b97d-013f6c8d4960",
        "depth": 2,
        "agent_path": "/root/consumer_evals/consumer_mode_editor",
        "agent_nickname": "Peirce",
        "agent_role": null
      }
    }
  },
  "thread_source": "subagent",
  "agent_path": "/root/consumer_evals/consumer_mode_editor",
  "model_provider": "openai"
}

## Record 2; source line 8; turn_context


{
  "turn_id": "01a0ee98-e9c4-7292-acce-e87467db9a1a",
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
Task name: /root/consumer_evals/consumer_mode_editor
Sender: /root/consumer_evals
Payload:



## Record 4; source line 11; custom_tool_call


exec

const r = await tools.exec_command({cmd:"cat /tmp/clarify-task4/consumers/implementation-mode-coverage/editor-request.md", max_output_tokens:12000});
text(r.output);


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

Workspace: /tmp/clarify-task4/consumers/implementation-mode-coverage/workspace
Start the explicitly requested skill at /tmp/clarify-task4/instructions/skills/implement/SKILL.md. Resolve its linked instructions and profile paths within this package. This fixture contains no external knowledge service; .invalid URLs are simulated read-only responses. No network access.

## User request
Using the supplied /kk:implement and /kk:document instructions, trace the remaining completion workflow for each case in completion-cases.md. Identify the automatic calls and clarity-pass count, and explain how a separate explicit documentation request would affect the standalone case. This is a read-only routing check; do not execute tests, reviews, documentation or implementation.

## Allowed reads
This request; the frozen /tmp/clarify-task4/instructions/skills/ and /tmp/clarify-task4/instructions/profiles/ instruction trees (no evals present); the files listed below and any documents you create within the user-authorized output scope. Directory/filename inspection is allowed within the workspace and frozen instruction package. Nothing outside these paths is permitted, including repository files, installed instructions, other runs, oracles, eval definitions or session transcripts.
- /tmp/clarify-task4/consumers/implementation-mode-coverage/workspace/completion-cases.md

## Allowed writes
None. Remain read-only.
Do not spawn other agents. You are not alone in the shared filesystem; keep every action within this manifest and do not revert other work. Complete the user request and return your result as the final response.



## Record 6; source line 19; message


I’m using the supplied `/kk:implement` and `/kk:document` instructions to trace the completion paths. I’ll keep this read-only and report the automatic calls and clarity-pass counts for each case.


## Record 7; source line 20; custom_tool_call


exec

const results = await Promise.allSettled([
  tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/implement/SKILL.md", login:false, max_output_tokens:20000}),
  tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/document/SKILL.md", login:false, max_output_tokens:20000})
]);
for (let i=0;i<results.length;i++) text({i,result:results[i]});


## Record 8; source line 24; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

{"i":0,"result":{"status":"fulfilled","value":{"chunk_id":"778536","wall_time_seconds":0.000011162,"exit_code":0,"original_token_count":1998,"output":"---\nname: implement\ndescription: |\n  TRIGGER when: user asks to implement, fix, build, or work on something — whether from a\n  docs/feat/wip plan OR a standalone task (bug fix, GitHub issue, one-off change).\n  Examples: \"work on task 1\", \"fix this bug\", \"implement feature X from the issue\".\n  Provides structured execution with profile detection, dependency handling, review checkpoints.\n---\n\n# Implementing Work\n\n## Conventions\n\n- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).\n- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When the sub-task's target files activate a profile that contributes an `implement/` subdirectory (e.g., `${TOOLBOX_PLUGIN_ROOT}/profiles/k8s/implement/`), its `index.md` lists per-task gotchas the skill must consult BEFORE writing. See Step 2.\n\n## Modes\n\nTwo modes, determined automatically: **plan mode** when the user references a docs/feat/wip feature or task number; **standalone mode** otherwise (bug fix, GitHub issue, one-off change). When ambiguous, ask.\n\n- **Plan mode:** Read [plan-mode.md](plan-mode.md) for entry, iteration, and completion procedures.\n- **Standalone mode:** Read [standalone-mode.md](standalone-mode.md) for entry procedure.\n\nBoth modes share the same execution core (Step 2 onward) — profile detection, dependency handling, verification, review.\n\n## Required Outputs\n\nAfter each execution + review cycle, verify all outputs:\n\n- [ ] Implementation addresses the requirement (plan mode: matches plan)\n- [ ] Verification/tests pass\n- [ ] Code review completed (via `/kk:review-code` — which owns indexing its own `kk:review-findings`)\n- [ ] New project conventions indexed as `kk:project-conventions` (skip if none established)\n- [ ] (Plan mode only) `tasks.md` updated to `done`\n\n**Indexing ownership:** Review skills (`/kk:review-code`, `/kk:review-spec`) index their own findings. This skill only indexes `kk:project-conventions` for non-obvious patterns discovered during implementation. Do NOT duplicate review indexing here.\n\n### Review Mode\n\nBy default, review checkpoints use **isolated mode** (`kk:review-code:isolated`, `kk:review-spec:isolated`). This is mandatory because the implementing session has authorship bias — the same model that wrote the code produces weaker reviews of it. Isolated mode spawns an independent sub-agent with no prior exposure to the implementation.\n\nThe user can override at any checkpoint (\"use standard review for this one\") to fall back to in-session `/kk:review-code`.\n\n## Workflow\n\n**Mandatory order — understand before executing.** The flow below is strictly sequential. Do not read source files to modify, write code, edit files, run tests, or otherwise act on any task until you have loaded full context (design, implementation plan, task list in **plan mode**, or full problem understanding in **standalone**) and completed profile detection and loaded all resolved profile content. The only early contact with the codebase is the task's target filenames — enough to drive profile detection, not enough to pattern-match implementation.\n\n## The Process\n\n### Step 1: Load Context\n\nDetermine mode (see §Modes), then read the appropriate mode file and follow its entry procedure:\n\n- **Plan mode:** Read [plan-mode.md](plan-mode.md) — loads tasks.md, design.md, implementation.md, identifies next task.\n- **Standalone mode:** Read [standalone-mode.md](standalone-mode.md) — parses the problem, explores relevant code, forms an approach.\n\nAfter completing the mode's entry procedure, continue with Step 2.\n\n### Step 2: Execute\n\n**Mandatory order — instructions before action.** Steps 1–3 load instructions; step 4 is the first step that touches subject matter. Do not write code, edit files, or otherwise act until steps 1–3 have been performed in order. If a later step reveals that an instruction was missed, return to step 1.\n\n1. (Plan mode only) Update `tasks.md`: set the task's status to `in-progress`.\n2. **Profile-aware per-task gotchas (pre-write).** Run the `shared-profile-detection.md` procedure against the target files (and any diff-so-far). Detection itself always runs, however small or \"just markdown\" the task looks — that judgment is unreliable (a one-paragraph edit to a `SKILL.md` activates the `skill-md` profile), and whether detection fires is unknowable until it has run. For each active profile, load `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/implement/index.md`; if the read fails with ENOENT, that profile contributes no implement guidance — move on. Otherwise read the always-load + any matching conditional content. Apply those gotchas to the upcoming edits — they exist to prevent mistakes the post-write reviewer would otherwise catch. When no active profile contributes `implement/`, only the content load is skipped — never the detection.\n3. **Dependency-handling (pre-write).** Whenever the task introduces or changes a dependency — new import, version bump, unfamiliar call, **and per the widened trigger also: a Kubernetes API version, a CRD, a Helm chart or chart dependency, or a container image tag/digest** — apply the `/kk:dependency-handling` skill BEFORE writing the call. Do not guess signatures, API versions, or configuration; look them up via capy/context7 per that skill's rules. Per-profile lookup cascades live in each profile's `overview.md` (e.g., `${TOOLBOX_PLUGIN_ROOT}/profiles/k8s/overview.md` §Looking up Kubernetes dependencies).\n4. Make the changes. (Plan mode: follow the plan exactly.)\n5. (Plan mode only) Check off subtasks (`- [x]`) in `tasks.md` as you complete them.\n6. Run verifications; run `/kk:test` skill.\n\n### Step 3: Report and Review\n\n- Show what was implemented\n- Show verification output\n- Load `kk:review-code:isolated` skill — this handles both sub-agent and pal codereview internally with independent reviewers. Do NOT run a separate `pal` codereview call, as it is already included in the isolated workflow.\n- Based on user and code-review feedback: apply changes if needed and finalize\n- (Plan mode only) Update `tasks.md`: set the task's status to `done`\n\n**After finalizing**, verify all items in the **Required Outputs** section above:\n\n- [ ] Implementation addresses the requirement (plan mode: implementation matches plan)\n- [ ] Verification/tests pass, `/kk:test` completed\n- [ ] Code review completed (Explicitly via `/kk:review-code:isolated` skill — which owns indexing its own `kk:review-findings`)\n- [ ] New project conventions indexed as `kk:project-conventions` (skip if none established)\n- [ ] (Plan mode only) `tasks.md` updated to `done`\n\nIf any item is unchecked, go back and complete it. Do NOT proceed to the next task with incomplete outputs.\n\n### Step 4: Continue (plan mode only)\n\nFollow the iteration procedure in [plan-mode.md](plan-mode.md) — move to next task, repeat Steps 1–3.\n\n### Step 5: Complete (plan mode only)\n\nFollow the completion procedure in [plan-mode.md](plan-mode.md) — final validation, documentation, reflection.\n\n## When to Stop and Ask for Help\n\n**STOP executing immediately when:**\n\n- Hit a blocker (missing dependency, test fails, instruction unclear)\n- (Plan mode) Plan has critical gaps preventing starting\n- You don't understand a requirement or instruction is ambiguous\n- Verification fails repeatedly\n\n**IMPORTANT! Always ask for clarification rather than guessing.**\n\n## When to Revisit Earlier Steps\n\n**Return to Step 1 when:**\n\n- Partner updates the plan or clarifies the problem\n- Fundamental approach needs rethinking\n\n**IMPORTANT! Don't force through blockers** — stop and ask.\n\n## Remember\n\n- Review plan critically first\n- Follow plan steps exactly\n- Don't skip verifications\n- Use skills when applicable (`/kk:dependency-handling`, `/kk:test`, `/kk:review-code:isolated`) (Plan mode: also when the plan says to do so)\n- Between batches: just report and wait\n- Stop when blocked, don't guess\n"}}}
{"i":1,"result":{"status":"fulfilled","value":{"chunk_id":"211bf2","wall_time_seconds":0.000011321,"exit_code":0,"original_token_count":1155,"output":"---\nname: document\ndescription: |\n  After implementing a new feature or fixing a bug, make sure to document the changes.\n  Use when writing documentation, after finishing the implementation phase for a feature or a bug-fix.\n---\n\n# Documentation Process\n\n## Conventions\n\n- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).\n- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When an active profile contributes a `document/` subdirectory (e.g., `${TOOLBOX_PLUGIN_ROOT}/profiles/k8s/document/`), its `index.md` lists a doc rubric — required topics the documentation for that artifact type must cover. See the Workflow below for the load order.\n\n## Workflow\n\n**Mandatory order — instructions before action.** The flow below is strictly sequential. Do not read feature-tree content, write, or edit documentation files until the shared protocols, including [shared-document-clarity.md](shared-document-clarity.md), and all resolved profile content are in context. Bounded signal inspection for profile detection is the only content-read exception.\n\nRead the shared protocols in Conventions and [shared-document-clarity.md](shared-document-clarity.md) before the steps below, even when the invocation ultimately needs no edits.\n\n1. **Minimal-scope listing.** List the feature directory (filenames and metadata only — no file-content reads). This is the input profile detection needs, and nothing more; content-level reading happens after profile content is loaded.\n2. **Detect active profiles.** Run the `shared-profile-detection.md` procedure against the filename list from Step 1.\n3. **Load profile content.** For each active profile that contributes a `document/` subdirectory, load `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/document/index.md` and read its always-load + any matching conditional content. The rubric named there specifies topics the documentation must cover for that profile's artifacts.\n4. **Read the feature-tree content** the documentation will cover. This is the first step that touches subject-matter content; the profile rubric is now loaded and frames what to look for.\n5. **Apply the doc guidelines below.** Write or update documentation applying the rubric's required topics where applicable.\n6. **Clarify completed outputs.** Apply the loaded shared procedure once after all selected documentation updates, using the reader, destination, requirements and applicable source understanding from this invocation. Select only its drafted or updated outputs; leave unrelated documents outside the edit scope. Retain every applicable profile-rubric topic, including explicit N/A reasons and inherited-source citations. If there are no outputs to edit, skip the pass. Use the procedure directly without invoking `/kk:clarify-docs` or another writing skill; produce no extra summary file. In the change report, state that the fidelity check was in-session and further project-prescribed review remains with the caller; do not claim independent verification.\n\n## Guidelines\n\n1. **Discover the project's documentation structure.** List top-level doc directories and doc-related files at the repo root (e.g., `docs/`, `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`). Scan for architecture guides, testing guides, API docs, user guides, and contributing docs — common locations include `docs/contributing/architecture.md`, `docs/contributing/testing.md`, but every project organizes differently. Update whichever docs are relevant to the change — don't limit yourself to a fixed set of paths.\n2. If the code change included prior decision-making out of several alternatives, document an ADR at `/docs/adr` for any non-trivial/non-obvious decisions that should be preserved.\n3. **Profile-aware rubric.** For each active profile, apply the doc rubric its `document/index.md` specifies (loaded in Step 3 of the Workflow). Each required topic must be addressed in one of three ways: (a) write the topic if the feature touches it, (b) state `N/A — <reason>` in a single line if the feature does not touch the topic, or (c) cite the inherited source explicitly if the feature assumes the topic but inherits it from elsewhere (e.g., NetworkPolicy defined in a platform repo). Silent omission is the failure mode — an explicit `N/A` communicates consideration; an absent heading communicates nothing.\n\n**Capy search:** Before writing docs, search `kk:arch-decisions` and `kk:project-conventions` for decisions that should be reflected in documentation — decisions not obvious from code alone.\n"}}}

## Record 9; source line 26; custom_tool_call


exec

const r = await tools.exec_command({cmd:"cat /tmp/clarify-task4/instructions/skills/implement/plan-mode.md /tmp/clarify-task4/instructions/skills/implement/standalone-mode.md /tmp/clarify-task4/instructions/skills/implement/shared-capy-knowledge-protocol.md /tmp/clarify-task4/instructions/skills/implement/shared-profile-detection.md /tmp/clarify-task4/instructions/skills/document/shared-document-clarity.md",login:false,max_output_tokens:25000});
text(r.output);


## Record 10; source line 29; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

# Plan Mode

Applies when the user references a docs/feat/wip feature or task number.

## Entry Procedure

1. Read the feature's `tasks.md` file to get the task list and current progress
2. Read the entire `design.md` and `implementation.md` files to **understand the full feature context**
3. Identify the next pending task (one whose dependencies are all done)
4. **Capy search:** Search `kk:arch-decisions`, `kk:project-conventions`, `kk:lang-idioms`, and `kk:review-findings` for context relevant to the identified task. Run it for every task, however small — whether the knowledge base holds something relevant is unknowable until searched, and an empty result costs nothing
5. Review critically — identify any questions or concerns about the plan
6. If concerns: Raise them with your human partner before starting

After completing the entry procedure, return to SKILL.md Step 2 (Execute).

## Iteration

After each execution + review cycle (SKILL.md Steps 2–3):

- Verify the completed task's **Required Outputs** are all checked
- Move to the next pending task in `tasks.md`
- Return to the Entry Procedure above to load context for the new task
- Repeat until all tasks are completed

## Completion

After all tasks are complete and verified:

- Use `/kk:test` skill to verify and validate functionality
- Use `/kk:document` skill to create or update any relevant docs
- **Reflect:** briefly note where the implementation diverged from the plan, what turned out harder or simpler than expected, and any surprises that future work in this area should know about. Keep it short — a paragraph, not an essay. Index non-obvious learnings as `kk:project-conventions` or `kk:arch-decisions` if they weren't already captured during per-task cycles.
- Update the feature status in `tasks.md` header to `done`
# Standalone Mode

Applies for bug fixes, GitHub issues, one-off tasks, and any work without docs/feat/wip infrastructure.

## Entry Procedure

1. Parse the user's request — what is the problem or requirement?
2. If the user references a GitHub issue, fetch it (`gh issue view`)
3. **Capy search:** Search `kk:arch-decisions`, `kk:project-conventions`, `kk:lang-idioms`, `kk:review-findings`, and `kk:debug-context` for relevant prior context
4. Identify questions or ambiguities — ask before assuming
5. Investigate the relevant code — read files, trace call paths, reproduce the bug if applicable
6. Identify the set of files that will need changes
7. State the approach briefly if the fix is non-trivial (more than a few lines across 1–2 files). For trivial fixes, skip the approach statement only — "trivial" never exempts a fix from SKILL.md Step 2's pre-write steps (profile detection, dependency handling), which run for every fix however small.

After completing the entry procedure, return to SKILL.md Step 2 (Execute).
# Capy Knowledge Base Protocol

If `capy` MCP tools are not available in this session, skip all search and index steps below and proceed normally.

## Source Label Taxonomy

All plugin-managed labels use the `kk:` namespace prefix.

| Label                    | Contents                                                              |
| ------------------------ | --------------------------------------------------------------------- |
| `kk:arch-decisions`      | Architecture decisions, design rationale, trade-offs                  |
| `kk:review-findings`     | Code review patterns, recurring issues, anti-patterns                 |
| `kk:lang-idioms`         | Language best practices, idiomatic patterns from external sources     |
| `kk:project-conventions` | Discovered project patterns, naming conventions, structural decisions |
| `kk:test-patterns`       | Testing approaches, edge cases, test infrastructure decisions         |
| `kk:debug-context`       | Root causes, tricky bugs and their fixes, environment gotchas         |

## Search Conventions

- Use 2-4 specific terms per query — not vague keywords
- Always scope with `source` filter to relevant `kk:*` labels
- Use `source: "kk:"` only for broad cross-domain searches (e.g., CoVe verification)
- Default `limit: 3` per query unless more context is needed
- **Cold-start fallback:** If no results, proceed with standard guidelines — empty results are normal for new projects

## Index Conventions

- Only index non-obvious learnings not derivable from reading the code or git history
- Keep content concise — summarize the insight, don't dump raw output
- Always use a `kk:` prefixed label from the taxonomy above
- One concept per `capy_index` call — don't bundle unrelated learnings
- Skip indexing if the insight is already captured in design docs or CLAUDE.md
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


## Record 11; source line 33; custom_tool_call


exec

const r = await tools.exec_command({cmd:"cat /tmp/clarify-task4/consumers/implementation-mode-coverage/workspace/completion-cases.md",login:false,max_output_tokens:12000});
text(r.output);


## Record 12; source line 36; custom_tool_call_output


Script completed
Wall time 0.3 seconds
Output:

# Completion cases

1. Plan mode: all tasks in the selected feature are complete and verified. Determine
   what the plan completion procedure prescribes, including documentation.
2. Standalone mode: a one-off correction has passed execution, tests and isolated
   code review. No user or repository instruction requests documentation separately.
3. Mid-plan: Task 1 has passed execution, tests and review, but Task 2 is pending.
   Determine whether finishing Task 1 alone invokes documentation completion.

For each, name the owning instruction file and count automatic shared clarity passes
when documentation outputs are actually drafted. Do not execute the routes.


## Record 13; source line 41; message


| Case | Remaining automatic workflow | Automatic clarity passes |
|---|---|---|
| **1. Plan complete** | [plan-mode.md](/tmp/clarify-task4/instructions/skills/implement/plan-mode.md) prescribes `/kk:test` → `/kk:document` → brief reflection → mark the feature header `done`. | **1** when documentation outputs are drafted or updated; **0** if there are no outputs to edit. |
| **2. Standalone complete** | [implement/SKILL.md](/tmp/clarify-task4/instructions/skills/implement/SKILL.md) requires checking the remaining Required Outputs, then ends. Its continuation and completion steps apply only to plan mode; [standalone-mode.md](/tmp/clarify-task4/instructions/skills/implement/standalone-mode.md) adds no documentation completion call. | **0**. Documentation is not automatically invoked in this case. |
| **3. Task 1 complete; Task 2 pending** | [plan-mode.md](/tmp/clarify-task4/instructions/skills/implement/plan-mode.md) prescribes checking Task 1’s Required Outputs, selecting Task 2, reloading context and repeating execution, testing and review. Feature completion—including documentation—waits until all tasks are complete and verified. | **0** from finishing Task 1 alone. |

A **separate explicit documentation request** for the standalone correction would invoke [document/SKILL.md](/tmp/clarify-task4/instructions/skills/document/SKILL.md). That invocation applies the shared clarity procedure **once after all selected documentation updates**, regardless of the number of files; it skips the pass when there are no outputs to edit.

The document skill uses the shared procedure directly: it does **not** invoke `/kk:clarify-docs` or another writing skill. Its fidelity check is in-session; further project-required review remains with the caller.

No routes were executed.
