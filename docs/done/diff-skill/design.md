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

Complexity assessment has two sub-axes:

**Complexity regression** — comparative. Did the edit make the skill harder to follow than before? The LLM compares both states and flags complexity that was *introduced or worsened* by the edit. Complexity regressions affect the verdict.

**Pre-existing complexity advisory** — after-state only. Structural issues that exist in the "after" state regardless of whether the edit caused them. These are surfaced in a separate report section as improvement opportunities — they do not affect the verdict.

Complexity signals (applied to both sub-axes):

- **Instruction density** — too many rules crammed into one section
- **Cross-turn state burden** — gates and sub-phase state the LLM must track across multiple user messages
- **Inline multi-path logic** — branching workflows or conditional mode selection in SKILL.md that creates conflicting instructions in the same file, and could be extracted into dedicated reference/process files (reducing both context size and cognitive load)
- **Contradictory or tension-creating instructions** — rules that pull in opposite directions without clear precedence
- **Deep reference chains** — files linking to files linking to files, inflating the working set
- **Ambiguous conditional logic** — gates without clear evaluation criteria

A skill that's complex by necessity (like `/kk:design` with its interactive multi-turn flow) isn't wrong — but the tool flags where that complexity could be reduced.

### Verdict

The verdict combines both axes. Possible outcomes:

- **No issues** — no degradation, no complexity regressions
- **Degraded** — content was lost or weakened
- **Complexity regressed** — no content lost, but the edit made the skill harder to follow
- **Both** — degradation and complexity regression

Pre-existing complexity advisories appear in the report regardless of the verdict but do not influence it.

The tool is advisory. It produces a report and an inline summary. It is not a CI gate and does not block merges. The skill author reads the findings and decides what to act on.

## Scope — the reachable file set

The "skill" being compared is everything transitively reachable via markdown links from `SKILL.md`. SKILL.md is the manifest — it links to process files, shared instructions, reference docs. Those files may link further. The union of all reachable files at a given ref is the skill's content at that ref.

### Link walk

Start at `SKILL.md`. Extract `[text](relative/path.md)` links. Strip fragment identifiers (`#anchor`) before resolution — `[text](file.md#section)` resolves to `file.md`. Resolve each path relative to the containing file's directory. If the resolved file exists at the ref, add it to the set and recurse. A `visited` set prevents cycles.

**Skip:**
- External URLs (`http://`, `https://`)
- Anchor-only refs (`#section`)
- Links inside fenced code blocks

**Track broken links:** Files referenced by a link but absent at the ref are collected in a separate `missing_links` set (with source file, raw href, and resolved path). These are NOT silently dropped — they are fed into the judgment phase as potential "broken reference" degradations.

**Content retrieval:** For git refs, use `git show <ref>:<path>` for regular files. **Symlinks require special handling:** `git show <ref>:<path>` on a symlink returns the target path string, not the target content. Detect symlinks via `git ls-tree <ref> <path>` (mode `120000`), read the target path with `git cat-file -p <ref>:<path>`, resolve relative to the symlink's directory, then read the resolved target at the same ref. For the working tree, the `Read` tool follows symlinks transparently.

**No artificial refusal.** If a skill has an unusually large reachable set, that's a complexity finding, not a reason to refuse to run. However, after building both reachable sets, the skill estimates total combined content size (both sides together). The ~100KB threshold accounts for the fact that this content shares context with the skill's own instructions (SKILL.md, diff-process.md, capy protocol). If combined content exceeds ~100KB, the skill warns the user with size and file count, and offers to proceed or narrow scope (e.g., compare only changed files). This preserves the "no refusal" stance while failing loud about potential context-window degradation.

### Portability

The scope definition makes no assumption about `_shared/`, `agents/`, or any repo-specific directory convention. It follows links from SKILL.md — any skill directory with a SKILL.md works.

## Invocation

```
/kk:diff-skill <skill-name>
```

The skill locates `klaude-plugin/skills/<name>/SKILL.md` as a convenience shortcut. If the shortcut doesn't resolve, it asks the user for the path to the skill directory. Any user-provided path is normalized to a repo-relative path (required for `git cat-file -e <ref>:<path>` and `git show <ref>:<path>` operations). Paths outside the repo are rejected.

By default, compares `HEAD` (before) → working tree (after). The direction matters — this is an asymmetric tool, so "before" is the baseline and "after" is what's being judged. Same ergonomics as `/kk:review-code` operating on the current diff. If the user needs to compare specific refs, they state so in the prompt.

**Report slug:** The `<skill-name>` used in report filenames is the `name` field from SKILL.md's YAML frontmatter if present, otherwise the parent directory basename of SKILL.md (e.g., `review-code` for `klaude-plugin/skills/review-code/SKILL.md`).

**Validation:** Confirm `SKILL.md` exists at the resolved repo-relative path for both sides. If either is missing, error with a clear message.

## Report

### File location

```
docs/reviews/diff-skill/<skill-name>-<short-sha-a>-<short-sha-b>.md
```

Short SHA = 7 chars. Working-tree side → `WORKTREE`. Directory created on first run. Reports are committed — they serve as review history for the skill's evolution. The `docs/reviews/` convention is new; it sits outside the `docs/wip/` → `docs/done/` lifecycle because reviews are point-in-time snapshots, not living feature docs.

### Structure

```markdown
# diff-skill: <name> (<ref-a> → <ref-b>)

## Summary
<one-paragraph verdict combining both axes>

## Degradations
<each finding: what was lost/weakened, where, and why it matters>

## Complexity Regressions
<each finding: what became harder to follow due to this edit, and how it could be simplified>

## Pre-existing Complexity
<improvement opportunities that exist in the after-state regardless of this edit>

## Neutral Changes
<brief list of changes that are neither degradations nor complexity issues>
```

No confidence levels, no kind classifications, no before/after quote blocks, no traversal tree dump. Each finding is a short paragraph — what, where, why it matters. The reader is a skill author who knows their own files.

### Inline summary

A short block (under 10 lines) in the conversation with the verdict, finding counts per axis, and a pointer to the full report file.

### Capy indexing

If any degradation or complexity findings exist, index a summary under `kk:review-findings` (the shared label for review patterns and recurring issues). Skip indexing on clean results.

## Evaluation scenarios

The skill's value is in LLM judgment quality — whether it correctly classifies degradations, neutral changes, and complexity issues. At least two eval scenarios should be authored under `klaude-plugin/skills/diff-skill/evals/`:

**Eval 1: Known degradation.** A deliberately degraded version of an existing skill (e.g., `merge-docs` with a `MUST` weakened to `SHOULD`, a required-output bullet removed, and a link broken). The skill should flag all three as degradations.

**Eval 2: Clean refactor.** A restructured version of a skill where content is moved between files but no substance is lost. The skill should report no degradations. Complexity findings are acceptable if the restructuring genuinely increased complexity.

These follow the eval conventions in `CLAUDE.md` §Skill evaluations — `eval.json` with assertions, real test fixtures under `test-files/`.

## Assumptions

1. **SKILL.md links to everything that matters.** If a file influences skill behavior but isn't linked (directly or transitively) from SKILL.md, it won't be compared. This incentivizes skill authors to keep their link graph complete.
2. **Markdown link extraction is reliable for skill files.** Standard `[text](relative/path.md)` covers the vast majority. Links inside fenced code blocks are excluded. Edge cases (HTML `<a>` tags, reference-style links) are acceptable blind spots for v1.
3. **Link targets in skill files use relative paths.** The link-walk extracts and resolves relative markdown links. `${CLAUDE_PLUGIN_ROOT}` tokens in file content are not resolved (they're substituted at plugin-load time, not by `git show` or `Read`), but these tokens appear in prose and examples, not in link targets. If a link target contains an unresolvable token, it will be tracked as a missing link.
4. **Typical skill content fits in context.** A skill's full reachable file set (both refs combined, plus skill instructions) fits within the LLM's working context. The ~100KB threshold is a heuristic; skills with 30+ reachable files would be unusual.
5. **The LLM can identify complexity regressions when given both states.** Validated by the eval scenarios — the LLM should detect at least 3 of the 6 complexity signal types when they appear in test fixtures. Meta-judgment has inherent blind spots on the LLM's own failure modes, but structured signal types make the task concrete rather than open-ended.

## Not Doing

- **Cross-rename syntax** — specify the skill directory directly; renames are rare
- **Mechanical extraction pass** — the LLM reads full content and judges directly
- **Confidence levels on findings** — advisory tool, not a CI gate
- **Behavioral evals** — running the skill against test fixtures to observe behavior changes
- **CI integration** — no machine-parseable verdict line contract
- **Multi-skill invocation** — one skill per run
- **Auto-fix** — the tool does not apply fixes or generate patches; findings include explanatory context ("how it could be simplified") but not executable remediation
- **Extension points documentation** — extend when needed, not before
