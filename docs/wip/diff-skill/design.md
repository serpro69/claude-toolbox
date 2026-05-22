# Design: diff-skill

> Status: design
> Created: 2026-05-22
> Related: [implementation.md](./implementation.md), [tasks.md](./tasks.md)

## Goal

`/kk:diff-skill` answers two questions about a skill maintained as markdown instructions:

1. **Did commit B degrade this skill compared to commit A?**
2. **Did the edit make the skill harder for an LLM to follow?**

The check is deliberately **asymmetric**. Additions, clarifications, and strengthenings are not degradations. Only regressions count.

This is a refactor-safety tool for skill authors: edit a skill, run `/kk:diff-skill`, and get a high-signal answer about whether the edit made the skill worse or harder to execute.

## Judgment axes

### Axis 1 — Degradation (asymmetric)

Only the following count as degradations:

- Load-bearing instruction dropped
- Constraint weakened (`MUST` → `SHOULD`, `NEVER` → `AVOID`)
- Verification step removed
- Scope narrowed (fewer cases covered)
- Required output dropped
- Reference broken (link target no longer exists or resolves)

Content that was relocated (inlined elsewhere, extracted to a new file) is neutral — the LLM checks whether the substance survived, not whether the path changed.

### Axis 2 — Complexity

Evaluates the "after" state for LLM-executability. A skill can lose no content but still become harder to follow. Complexity signals:

- **Instruction density** — too many rules crammed into one section
- **Cross-turn state burden** — gates and sub-phase state the LLM must track across multiple user messages
- **Inline multi-path logic** — branching workflows or conditional mode selection in SKILL.md that creates conflicting instructions in the same file, and could be extracted into dedicated reference/process files (reducing both context size and cognitive load)
- **Contradictory or tension-creating instructions** — rules that pull in opposite directions without clear precedence
- **Deep reference chains** — files linking to files linking to files, inflating the working set
- **Ambiguous conditional logic** — gates without clear evaluation criteria

Complexity findings are surfaced as improvement opportunities, not failures. A skill that's complex by necessity (like `/kk:design` with its interactive multi-turn flow) isn't wrong — but the tool flags where that complexity could be reduced.

### Verdict

The verdict combines both axes. Possible outcomes:

- **No issues** — no degradation, no significant complexity concerns
- **Degraded** — content was lost or weakened
- **Complexity concerns** — no content lost, but the skill became harder to follow
- **Both** — degradation and complexity issues

The tool is advisory. It produces a report and an inline summary. It is not a CI gate and does not block merges. The skill author reads the findings and decides what to act on.

## Scope — the reachable file set

The "skill" being compared is everything transitively reachable via markdown links from `SKILL.md`. SKILL.md is the manifest — it links to process files, shared instructions, reference docs. Those files may link further. The union of all reachable files at a given ref is the skill's content at that ref.

### Link walk

Start at `SKILL.md`. Extract `[text](relative/path.md)` links. Resolve each path relative to the containing file's directory. If the resolved file exists at the ref, add it to the set and recurse. A `visited` set prevents cycles.

**Skip:**
- External URLs (`http://`, `https://`)
- Anchor-only refs (`#section`)
- Links inside fenced code blocks
- Files that don't exist at the ref (noted as absent — fed into judgment, not an error)

**Content retrieval:** For git refs, use `git show <ref>:<path>`. For the working tree, use the `Read` tool. Symlinks are followed transparently — the content matters, not the indirection.

**No artificial safety rails.** If a skill has an unusually large reachable set, that's a complexity finding, not a reason to refuse to run.

### Portability

The scope definition makes no assumption about `_shared/`, `agents/`, or any repo-specific directory convention. It follows links from SKILL.md — any skill directory with a SKILL.md works.

## Invocation

```
/kk:diff-skill <skill-name>
```

The skill locates `klaude-plugin/skills/<name>/SKILL.md` as a convenience shortcut. If the shortcut doesn't resolve, it asks the user for the full path.

By default, compares working tree vs. `HEAD` — same ergonomics as `/kk:review-code` operating on the current diff. If the user needs to compare specific refs, they say so in natural language and the skill parses that from context.

**Validation:** Confirm `SKILL.md` exists at the skill path for both sides. If either is missing, error with a clear message.

## Report

### File location

```
docs/reviews/diff-skill/<skill-name>-<short-sha-a>-<short-sha-b>.md
```

Short SHA = 7 chars. Working-tree side → `WORKTREE`. Directory created on first run.

### Structure

```markdown
# diff-skill: <name> (<ref-a> → <ref-b>)

## Summary
<one-paragraph verdict combining both axes>

## Degradations
<each finding: what was lost/weakened, where, and why it matters>

## Complexity
<each finding: what's hard to follow, why, and how it could be simplified>

## Neutral Changes
<brief list of changes that are neither degradations nor complexity issues>
```

No confidence levels, no kind classifications, no before/after quote blocks, no traversal tree dump. Each finding is a short paragraph — what, where, why it matters. The reader is a skill author who knows their own files.

### Inline summary

A short block (under 10 lines) in the conversation with the verdict, finding counts per axis, and a pointer to the full report file.

### Capy indexing

If degradations or significant complexity findings exist, index a summary under `kk:diff-skill-findings`. Skip indexing on clean results.

## Assumptions

1. **SKILL.md links to everything that matters.** If a file influences skill behavior but isn't linked (directly or transitively) from SKILL.md, it won't be compared. This incentivizes skill authors to keep their link graph complete.
2. **Markdown link extraction is reliable for skill files.** Standard `[text](relative/path.md)` covers the vast majority. Links inside fenced code blocks are excluded. Edge cases (HTML `<a>` tags, reference-style links) are acceptable blind spots for v1.
3. **Typical skill content fits in context.** A skill's full reachable file set (both refs) fits within the LLM's working context. Skills with 30+ reachable files would be unusual.
4. **The LLM can meaningfully assess "complexity for an LLM to follow."** Meta-judgment with possible blind spots, but it can reliably spot excessive branching, cross-turn state burden, ambiguous gates, and instruction density.

## Not Doing

- **Cross-rename syntax** — specify the skill directory directly; renames are rare
- **Mechanical extraction pass** — the LLM reads full content and judges directly
- **Confidence levels on findings** — advisory tool, not a CI gate
- **Behavioral evals** — running the skill against test fixtures to observe behavior changes
- **CI integration** — no machine-parseable verdict line contract
- **Multi-skill invocation** — one skill per run
- **Auto-fix / remediation suggestions**
- **Extension points documentation** — extend when needed, not before
