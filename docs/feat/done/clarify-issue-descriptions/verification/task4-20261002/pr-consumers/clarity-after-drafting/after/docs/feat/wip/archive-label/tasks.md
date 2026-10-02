# Tasks: Archive labels

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-02
> Not Doing: filtering, automatic archival, color changes

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#label-edit](./implementation.md#label-edit)

### Subtasks

- [ ] 1.1 Inspect `catalog.md` before editing → verify: its author-maintained archival convention consistently distinguishes archived entries from active ones. Resolve ambiguous entries with catalog maintainers before adding labels.
- [ ] 1.2 Add `Archived` beside each archived entry's link in `catalog.md`, outside the existing link text → verify: every archived entry has the label, active entries have none, and all titles, destinations, and entries are preserved.
- [ ] 1.3 Inspect the diff and rendered `catalog.md` → verify: labels are visible beside the appropriate entries, links remain clickable with the same destinations, and edits contain only label text and necessary spacing.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#final-verification](./implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the catalog change → verify: the full applicable existing validation suite, if present, and the entry-by-entry and rendered acceptance checks pass. Record manual results and any absence of automated checks.
- [ ] 2.2 Invoke `/kk:document` to update relevant catalog guidance, if present → verify: guidance matches the text-only label and preserves the undecided color decision.
- [ ] 2.3 Invoke `/kk:review-code` with Markdown as the project language/content input → verify: actionable findings on the catalog diff are resolved.
- [ ] 2.4 Invoke `/kk:review-spec` → verify: the implementation matches the design and plan, with task status updated to reflect the actual work completed.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
