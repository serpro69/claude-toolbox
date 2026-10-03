# Tasks: Archive labels

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, color changes

The design is approved. Implementation has not begun. Catalog maintainers own the future color decision, whose next step is checking the site's contrast before choosing a color; it is outside this task list.

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#label-edit](implementation.md#label-edit), [design.md#acceptance-checks](design.md#acceptance-checks)

### Subtasks

- [ ] 1.1 Obtain and inspect the actual `catalog.md`, which was absent during drafting, and establish its archived-entry set → verify: existing archive markers consistently distinguish archived and active entries; resolve ambiguous classification with catalog maintainers before editing.
- [ ] 1.2 Add plain `Archived` text beside each archived entry's existing title/link in `catalog.md`, outside the link text → verify: every archived entry has one label, active entries have none, and every original title and link destination is unchanged.
- [ ] 1.3 Inspect the catalog diff and rendered Markdown → verify: archived entries remain visible and clickable, labels sit beside the correct entries, and the change adds no color, filtering, automation, or unrelated content. Record any unavailable site-preview check explicitly.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#final-verification](implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `$kk:test` for the completed catalog change → verify: all label acceptance checks and any existing full project test suite pass; if no suite exists, report that and the manual catalog-check results.
- [ ] 2.2 Invoke `$kk:document` for relevant documentation updates → verify: feature status reflects the implementation and the future color choice remains distinct from accepted text-label requirements.
- [ ] 2.3 Invoke `$kk:review-code` with project language input Markdown → verify: findings affecting coverage, titles, destinations, or scope are resolved and rechecked.
- [ ] 2.4 Invoke `$kk:review-spec` → verify: the catalog matches the approved design and implementation plan, including the validated archive-marker assumption and all scope exclusions.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
