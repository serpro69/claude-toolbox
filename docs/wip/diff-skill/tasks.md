# Tasks: diff-skill

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-05-22
> Not Doing: cross-rename syntax, mechanical extraction pass, confidence levels, behavioral evals, CI integration, multi-skill invocation, auto-fix suggestions, extension points

## Task 1: Skill directory and SKILL.md
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#skillmd-authoring](./implementation.md#skillmd-authoring)

### Subtasks
- [ ] 1.1 Create directory `klaude-plugin/skills/diff-skill/`
- [ ] 1.2 Create symlink `shared-capy-knowledge-protocol.md → ../_shared/capy-knowledge-protocol.md` — verify with `readlink` and `cat` through the symlink
- [ ] 1.3 Author `SKILL.md` with YAML frontmatter (`name: diff-skill`, multi-line `description` under 1,024 chars), overview (two judgment axes), conventions (capy protocol reference), required outputs checklist, invocation section, and workflow with mandatory-order directive pointing to `diff-process.md`. Model after `merge-docs/SKILL.md`
- [ ] 1.4 Verify all internal `[text](path)` links in SKILL.md resolve to files in the skill directory

## Task 2: Author diff-process.md
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#diff-processmd-authoring](./implementation.md#diff-processmd-authoring)

### Subtasks
- [ ] 2.1 Write progress checklist at top (7 phases) and Phase 1 "Parse invocation" — skill-name extraction, SKILL.md path resolution (convenience shortcut + fallback), ref defaults (working tree vs HEAD)
- [ ] 2.2 Write Phase 2 "Validate" — `git rev-parse` for refs, `git cat-file -e` for SKILL.md existence at both refs, clear error messages
- [ ] 2.3 Write Phase 3 "Build reachable file sets" — link-walk algorithm (frontier/visited), markdown link extraction excluding fenced code blocks and external URLs, relative path resolution, symlink handling, absent-file tracking
- [ ] 2.4 Write Phase 4 "Judgment" — two-axis framing (degradation + complexity), relocation handling, explicit asymmetric instructions for the LLM
- [ ] 2.5 Write Phase 5 "Write report" — directory creation, filename convention, report template
- [ ] 2.6 Write Phase 6 "Present inline summary" — under 10 lines, verdict + counts + report path
- [ ] 2.7 Write Phase 7 "Index to capy" — conditional indexing under `kk:diff-skill-findings`, skip on clean results

## Task 3: Wire into plugin manifest and tests
- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#files-to-create](./implementation.md#files-to-create)

### Subtasks
- [ ] 3.1 Add `diff-skill` to `EXPECTED_SKILLS` array in `test/test-plugin-structure.sh` and update the skill count in the log message from 10 to 11
- [ ] 3.2 Add `diff-skill` row to the Skills table in `klaude-plugin/README.md` — one-sentence description matching the tone of surrounding rows
- [ ] 3.3 Run `bash test/test-plugin-structure.sh` and confirm all assertions pass
- [ ] 3.4 Verify the Skills-table row count is correct via a scoped check (grep per-skill name within the Skills section, not a repo-wide count)

## Task 4: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 4.1 Run `/kk:test` skill to verify the full test suite passes
- [ ] 4.2 Run `/kk:document` skill to update any relevant docs
- [ ] 4.3 Run `/kk:review-code` skill with markdown/shell input to review the new skill files
- [ ] 4.4 Run `/kk:review-spec` skill to verify SKILL.md + diff-process.md match design.md and implementation.md

## Dependency Graph

```
Task 1 → Task 2 → Task 3 → Task 4
```
