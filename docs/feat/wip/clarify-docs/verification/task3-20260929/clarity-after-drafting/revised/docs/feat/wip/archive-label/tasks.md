# Tasks: Archive label

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending
> Created: 2026-09-29
> Not Doing: filtering, automatic archival, color changes

These tasks describe future work. The catalog is absent from the supplied workspace;
obtain `catalog.md` before Task 1. Catalog maintainers resolve ambiguous archival
status and own the separate color decision after checking the site's contrast.

## Task 1: Add archive labels to the catalog

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label edit](./implementation.md#label-edit)

### Subtasks

- [ ] 1.1 Inspect `catalog.md` and verify that authors mark archived entries
  consistently. Resolve ambiguous entries with catalog maintainers before editing
  → verify: the existing marks identify every archived and active entry without
  guessing.
- [ ] 1.2 Add Archived beside each archived entry's existing link in `catalog.md`,
  outside the title and in the existing catalog format → verify: every archived
  entry displays Archived; active entries have no archive label.
- [ ] 1.3 Check the diff and rendered catalog → verify: all existing titles and
  destinations are preserved, archived entries stay visible and clickable, and
  only label text changes. Record the viewer used and the outcome.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](./implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the full available suite and edge cases → verify:
  record actual results, including the entry-by-entry label and link checks; if no
  automated suite exists, state that limit.
- [ ] 2.2 Invoke `/kk:document` to update relevant documentation → verify: it
  describes the implemented text label and retains color as an unresolved future
  decision owned by catalog maintainers.
- [ ] 2.3 Invoke `/kk:review-code` with Markdown as the language input → verify:
  address applicable findings about the catalog changes.
- [ ] 2.4 Invoke `/kk:review-spec` → verify: the implementation matches the design
  and implementation plan, including labels, visible links, unchanged titles and
  destinations, and scope exclusions.

## Dependency Graph

```text
Task 1 --> Task 2
```
