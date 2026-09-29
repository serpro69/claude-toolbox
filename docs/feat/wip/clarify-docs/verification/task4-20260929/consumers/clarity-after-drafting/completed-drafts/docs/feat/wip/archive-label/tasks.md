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
