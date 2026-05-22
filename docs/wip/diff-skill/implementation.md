# Implementation: diff-skill

> Design: [./design.md](./design.md)
> Tasks: [./tasks.md](./tasks.md)

## Reader orientation

This skill is pure markdown — no compiled code, no scripts, no dependencies. The "implementation" is a set of instructions that an LLM follows at invocation time, using `Bash` (for git commands) and `Read` (for working-tree files) to gather content, and `Write` to produce the report.

Familiarity needed:

- How the repo lays out skills — see `CLAUDE.md` § "Skill & Command Naming Conventions"
- How existing skills structure `SKILL.md` + a process file + `_shared` symlinks — read `klaude-plugin/skills/merge-docs/` as the closest shape (simple, single-mode skill with one process file)
- The `docs/wip/` ↔ `docs/done/` lifecycle for feature docs

Treat the design document as the source of truth. If a task description disagrees with the design, the design wins and the task needs updating.

## Files to create

```
klaude-plugin/skills/diff-skill/
├── SKILL.md                                       (new)
├── diff-process.md                                (new)
└── shared-capy-knowledge-protocol.md              (symlink → ../_shared/capy-knowledge-protocol.md)

docs/reviews/diff-skill/                           (directory created on first skill run, not at implementation time)

test/test-plugin-structure.sh                      (update EXPECTED_SKILLS array)
klaude-plugin/README.md                            (update skill table)
```

No commands directory for v1 — the skill is invoked directly as `/kk:diff-skill`.

## SKILL.md authoring

Model after `klaude-plugin/skills/merge-docs/SKILL.md` — the closest comparable skill (simple, single-mode, one process file).

**Required frontmatter:** `name: diff-skill`, multi-line `description` within the 1,024-char soft budget (see `CLAUDE.md` § "Skill description budget"). Lead with trigger keywords: "Compare two versions of a skill's instructions to detect degradations and complexity increases."

**Required sections:**

- **Overview** — goal + two judgment axes (asymmetric degradation + complexity). Lift from design.md §Goal and §Judgment axes, keep concise.
- **Conventions** — reference `shared-capy-knowledge-protocol.md` (same pattern as `merge-docs/SKILL.md`).
- **Required Outputs** — checklist: report written to file, inline summary presented, capy indexing done if findings exist.
- **Invocation** — the `/kk:diff-skill <skill-name>` form with defaults described.
- **Workflow** — mandatory-order directive at the top (per `CLAUDE.md` § "Skill workflow ordering"). Short phase list pointing to `diff-process.md` for details.

Step → verify: All internal `[text](path)` links resolve to files in the skill directory. `grep -oP '\[.*?\]\(\.?/?\K[^)]+' SKILL.md` returns only files that exist.

## diff-process.md authoring

The detailed workflow the LLM follows step-by-step at invocation time. Model the structure after `merge-docs/merge-process.md` — numbered steps with a copyable progress checklist at the top.

### Phase 1: Parse invocation

Extract `<skill-name>` from the invocation. Locate SKILL.md:
- Try `klaude-plugin/skills/<name>/SKILL.md` as a convenience shortcut
- If not found, ask the user for the full path

Determine comparison refs: default is working tree vs. `HEAD`. If the user specified refs in natural language, parse them.

Step → verify: `SKILL.md` path is resolved and both refs are valid.

### Phase 2: Validate

- For git refs: `git rev-parse <ref>` to confirm the ref resolves
- Confirm `SKILL.md` exists at both refs: `git cat-file -e <ref>:<path>` for git refs, filesystem check for working tree
- Error with a clear message if either side is missing

Step → verify: Both refs resolve and SKILL.md exists at both.

### Phase 3: Build reachable file sets

For each ref, build the set of all files transitively reachable via markdown links from SKILL.md.

**Algorithm:**
1. Start with `frontier = {SKILL.md path}`, `visited = {}`
2. Pop a file from frontier, add to visited
3. Retrieve content: `git show <ref>:<path>` for git refs, `Read` for working tree
4. Extract markdown links: `[text](relative/path.md)` patterns, excluding links inside fenced code blocks and external URLs/anchors
5. Resolve each link relative to the containing file's directory
6. If the resolved path exists at the ref and is not in visited, add to frontier
7. Repeat until frontier is empty

Symlinks: follow transparently. For git refs, `git show <ref>:<symlink>` returns the target content. For working tree, `Read` follows symlinks by default.

Files that exist on one side but not the other: note as absent, include in the judgment input (the LLM decides if the absence is a degradation, neutral relocation, or addition).

Step → verify: Two file sets produced, one per ref. Each set is a map of `{path → content}`.

### Phase 4: Judgment

Present the LLM with:
1. Full content of all reachable files at ref-a (the "before" state)
2. Full content of all reachable files at ref-b (the "after" state)
3. List of files present on only one side

Frame the judgment with explicit asymmetric + complexity instructions (lift from design.md §Judgment axes):

**Degradation axis:** "Only regressions count. Additions, clarifications, and strengthenings are NOT degradations. A degradation is: load-bearing instruction lost, weakened constraint, dropped verification, narrowed scope, broken reference, or required output lost. For each finding, state what was lost, where, and why it matters."

**Complexity axis:** "Evaluate the 'after' state for LLM-executability. Flag: instruction density, cross-turn state burden, inline multi-path logic that could be extracted into separate files, contradictory instructions, deep reference chains, ambiguous conditional logic. These are improvement opportunities, not failures."

For content that was relocated (moved between files, inlined, or extracted): check whether the substance survived. If yes, neutral. If substance was lost in the move, degradation.

Step → verify: Each finding has a clear what/where/why-it-matters description and is classified as degradation, complexity, or neutral.

### Phase 5: Write report

- Create `docs/reviews/diff-skill/` if absent (`mkdir -p`)
- Compute filename: `<skill-name>-<short-sha-a>-<short-sha-b>.md` (7-char SHAs, `WORKTREE` for working tree)
- Write the report following the template in design.md §Report §Structure
- Use `Write` tool

Step → verify: Report file exists at the expected path and follows the template structure.

### Phase 6: Present inline summary

Print a short block (under 10 lines) in the conversation:
- Verdict (combining both axes)
- Finding counts per axis
- Pointer to the full report file

Step → verify: Summary is under 10 lines and contains the report file path.

### Phase 7: Index to capy

If degradations or significant complexity findings exist, index a summary under source label `kk:diff-skill-findings`. Follow the protocol in `shared-capy-knowledge-protocol.md`.

Skip indexing on clean results — nothing durable to record.

Step → verify: Capy index call made if findings exist, skipped if clean.
