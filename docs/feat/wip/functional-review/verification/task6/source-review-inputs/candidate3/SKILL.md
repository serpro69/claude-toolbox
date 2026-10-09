---
name: implement
description: |
  TRIGGER when: user asks to implement, fix, build, or work on something — whether from a
  docs/feat/wip plan OR a standalone task (bug fix, GitHub issue, one-off change).
  Examples: "work on task 1", "fix this bug", "implement feature X from the issue".
  Provides structured execution with profile detection, dependency handling, review checkpoints.
---

# Implementing Work

**Start with instruction reads.** After this entry point loads, your next tool calls read the three shared protocols below and the selected mode procedure. Do not batch them with repository searches or source/document reads. Reading only this SKILL.md does not open investigation. Complete the profile-loading checkpoint before any full task/specification/source read, content search, test or edit; a filename-only scope operation is not that checkpoint.

## Conventions

- **Read capy knowledge base conventions** at [shared-capy-knowledge-protocol.md](shared-capy-knowledge-protocol.md).
- **Always read change context** at [shared-change-context.md](shared-change-context.md), including when no profile matches. It defines the factual record used before editing and refreshed for independent review.
- **Read profile detection** at [shared-profile-detection.md](shared-profile-detection.md). When the sub-task's target files activate a profile that contributes an `implement/` subdirectory (e.g., `${TOOLBOX_PLUGIN_ROOT}/profiles/k8s/implement/`), its `index.md` lists per-task gotchas the skill must consult BEFORE writing. See Step 2.

## Modes

Two modes, determined automatically: **plan mode** when the user references a docs/feat/wip feature or task number; **standalone mode** otherwise (bug fix, GitHub issue, one-off change). When ambiguous, ask.

- **Plan mode:** Read [plan-mode.md](plan-mode.md) for entry, iteration, and completion procedures.
- **Standalone mode:** Read [standalone-mode.md](standalone-mode.md) for entry procedure.

Both modes share the same execution core (Step 2 onward) — instruction loading, investigation and change context, implementation, verification, review.

## Required Outputs

After each execution + review cycle, verify all outputs:

- [ ] Implementation addresses intended outcomes, preserved contracts and hard task/delivery requirements
- [ ] Verification/tests pass for the claimed scope; unverified conditions are explicit
- [ ] Code review completed (via `/kk:review-code` — which owns indexing its own `kk:review-findings`)
- [ ] Refreshed context and evidence supplied to review; findings resolved or permitted follow-up recorded durably
- [ ] Code completion distinguished from release/migration/activation conditions
- [ ] New project conventions indexed as `kk:project-conventions` (skip if none established)
- [ ] (Plan mode only) `tasks.md` updated to `done`

**Indexing ownership:** Review skills (`/kk:review-code`, `/kk:review-spec`) index their own findings. This skill only indexes `kk:project-conventions` for non-obvious patterns discovered during implementation. Do NOT duplicate review indexing here.

### Review Mode

By default, review checkpoints use **isolated mode** (`/kk:review-code:isolated`, `/kk:review-spec:isolated`). This is mandatory because the implementing session has authorship bias — the same model that wrote the code produces weaker reviews of it. Isolated mode spawns an independent sub-agent with no prior exposure to the implementation.

The user can override at any checkpoint ("use standard review for this one") to fall back to in-session `/kk:review-code`.

## Workflow

**Mandatory order — instructions before action.** The flow below is strictly sequential. Load this skill, the selected mode procedure, shared protocols and every resolved profile instruction before source/requirement investigation, edits (including task-status edits), tests or implementation decisions. Entry procedures collect minimal task/file metadata solely to select scope and profile guidance; they do not analyze requirement prose. After basic instructions load, the sole early-content exception is routing for a declared detection or conditional-load predicate: inspect at most approximately 16 KiB per candidate file, log the predicate/path, and conservatively load an instruction when its conditional is undecidable within that bound. Routing permits no behavioral analysis, full-diff read, findings, edits or tests.

**Phases:** load basic instructions and scope metadata → detect profiles and load their content → investigate requirements/source and establish change context → implement and verify → refresh evidence and review → assess completion. Detailed investigation has one entry point in Step 2; mode entry procedures do not duplicate it.

## The Process

### Step 1: Load Instructions and Mode Context

Read the shared protocols in Conventions, determine mode (see §Modes), then read the appropriate mode file and follow its entry procedure:

- **Plan mode:** Read [plan-mode.md](plan-mode.md) — locates the feature documents and selects task/target metadata for routing.
- **Standalone mode:** Read [standalone-mode.md](standalone-mode.md) — selects request/target metadata without investigation.

After completing the mode's entry procedure, continue with Step 2.

Scope routing returns filenames/metadata only. For symbol lookup use a filename-only search (`Grep` with `output_mode: files_with_matches`, or `rg -l`), never matching source lines. In plan mode extract only the task headings/status/dependency/target-path fields specified by the mode procedure; do not use a full `Read`/`cat` of `tasks.md` as metadata, even when it is short. If a target is unclear, route a conservative file list rather than investigating it early.

### Step 2: Execute

1. **Detect and load profiles.** Run `shared-profile-detection.md` against candidate target filenames and any diff-so-far, however small the task. Read every Known profiles detection rule; reconcile expected versus returned rules, even when an extension seems obvious. Resolve the plugin root from the loaded skill location (parent of `skills/`) or the hook-exported root; do not use profile-directory discovery as a substitute for the Known profiles list. For each active profile, read `${TOOLBOX_PLUGIN_ROOT}/profiles/<name>/implement/index.md`; ENOENT means no implement guidance for that profile. Read every always-load, matching and conservatively selected instruction. An index or requested read alone is not a loaded checklist. Then emit the checkpoint below, naming returned paths and each conditional decision. No full task/specification/source read or content search may share a call with these instruction reads. A failed/missing read keeps this gate closed; an empty profile set skips content loading, never detection.

   ```text
   Instruction-loading checkpoint:
   - Shared protocols and selected mode: [returned paths]
   - Detection rules: [expected and returned paths reconciled]
   - Active profiles and implement instructions: [returned paths; conditional decisions]
   - Unread required instructions: [none, or stop and resolve]
   ```
2. **Load applicable dependency instructions.** For an introduced/changed dependency — import, version, unfamiliar call, Kubernetes API, CRD, Helm chart/dependency or container image — apply `/kk:dependency-handling` before writing the call. Use its lookup cascade and the active profile's `overview.md`; do not guess signatures or configuration. Revisit this gate if investigation discovers a dependency change.
3. **Investigate and establish change context.** This is the common investigation entry point for both modes. First load full requirement context: in plan mode read the entire `tasks.md`, `design.md` and `implementation.md`; in standalone mode examine the request and any referenced issue (`gh issue view`). Search the mode's declared Capy sources for relevant context, even for trivial work. Then read relevant source/current diff, trace affected entry points and unchanged callers through state and response contracts, and reproduce the problem where useful. Apply the shared change-context contract: establish intended outcomes and their authority, preserved behavior, actual scope/baselines and applicable delivery constraints before implementation edits. On resume, compare current repository state with earlier context and supersede stale evidence. If requirement loading or source exploration adds a target or reveals a new profile/conditional, pause that investigation to re-detect and load its guidance before proceeding.

   Check whether the proposed approach satisfies the requirement and delivery policy. A concrete conflict requires the affected flow, trade-off and smallest viable alternatives before dependent edits; pending future work is no excuse for breaking a current flow. Reuse accepted decisions and existing authorization. Resolve only consequential ambiguity or a requirement exception with the user; routine choices create no new approval gate. State a brief approach for non-trivial work. Keep trivial changes proportionate, without irrelevant release gates or duplicate tests.

   In plan mode, set the task to `in-progress` and record observations under its labeled **Execution context**, following [plan-mode.md](plan-mode.md). Standalone context remains conversational unless material work must be deferred.
4. **Implement.** Follow the established requirements and plan, if present. An observation or passing test does not authorize rewriting a requirement. Keep task/subtask progress accurate as work completes.
5. **Verify outcomes.** Invoke `/kk:test` and load its resolved instructions before running verification; running a test command alone does not execute that skill's workflow. Use relevant focused checks for intended behavior, preserved contracts and applicable compatibility cases. Record commands, actual results, baselines and limits. Green tests support only the scenarios exercised; they do not prove deployment readiness.

### Step 3: Report and Review

1. **Refresh the handoff.** Reconcile current diff scope, candidate state, requirements, baseline identities and verification references against the repository after edits, fixes or resume. Replace stale claims with dated evidence. Include task scope (done/current/pending tasks in plan mode), factual change context, affected paths, attributed test results and explicit unknowns. Do not pass implementation-session history, author conclusions as certification, or a preselected verdict.
2. **Review.** Invoke `/kk:review-code` in isolated mode (or the registered `/kk:review-code:isolated` command where available) and follow its full instruction-loading workflow. If the harness has no invocation tool, read that skill's entry point and isolated procedure explicitly. Do not replace it with a direct code-reviewer spawn: the isolated workflow owns both independent-agent and PAL paths, resolved criteria and evidence preparation. Supply the refreshed context and evidence to that workflow, which prepares the same relevant source/historical evidence for both reviewers and handles further evidence requests; do not issue a duplicate PAL review. If the user selected standard review, supply the same factual record to `/kk:review-code`. Missing specification or deployment evidence narrows conclusions; it does not reduce review to code quality alone.
3. **Resolve and reverify.** Apply required corrections, refresh affected context and tests, and obtain review of the changed evidence before finalizing. Index new non-obvious project conventions if any; review skills own their findings indexing.
4. **Assess completion.** Report requirement coverage, verification and review outcomes, with code completion separate from release, migration or activation conditions. A known unmet hard task/delivery requirement prevents `done` unless explicit user authorization changes it or accepts an exception; record the source, rationale and prerequisites. Unknown evidence essential to acceptance remains open. An external deployment prerequisite may outlive code completion only when consistent with the agreed contract; describe release readiness as conditional or unknown.

   Record every deferred material action durably with owner (or explicitly unassigned), reason, concrete next action and verification condition: the current task's Execution context in plan mode; existing tracking or a concise repository-local review note in standalone mode. A final-chat caveat alone is insufficient. Only then mark the plan task `done` if the contract and all **Required Outputs** are satisfied; otherwise keep required work open. Do not continue with incomplete outputs.

### Step 4: Continue (plan mode only)

Follow the iteration procedure in [plan-mode.md](plan-mode.md) — move to next task, repeat Steps 1–3.

### Step 5: Complete (plan mode only)

Follow the completion procedure in [plan-mode.md](plan-mode.md) — final validation, documentation, reflection.

## When to Stop and Ask for Help

**STOP executing immediately when:**

- An external blocker cannot be resolved within the authorized scope
- (Plan mode) Plan has critical gaps preventing starting
- You don't understand a requirement or instruction is ambiguous
- Verification fails repeatedly

Ask for the missing decision or capability rather than inventing a requirement. Continue independent authorized work while dependent work waits; ordinary fixable test failures should be corrected and reverified.

## When to Revisit Earlier Steps

**Return to Step 1 when:**

- Partner updates the plan or clarifies the problem
- Fundamental approach needs rethinking

**IMPORTANT! Don't force through blockers** — stop and ask.

## Remember

- Review plan critically first
- Follow the agreed plan; record explicit authorization for any requirement change
- Don't skip verifications
- Use skills when applicable (`/kk:dependency-handling`, `/kk:test`, `/kk:review-code:isolated`) (Plan mode: also when the plan says to do so)
- Between batches: just report and wait
- Stop when blocked, don't guess
