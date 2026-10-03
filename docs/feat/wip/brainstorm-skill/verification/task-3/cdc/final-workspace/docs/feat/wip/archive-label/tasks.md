# Tasks: Archive labels

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, color changes, catalog generation automation, new dependencies

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label-edit slice](implementation.md#label-edit-slice), [Assumptions](design.md#assumptions)

### Subtasks

- [ ] 1.1 Locate `catalog.md` in the implementation checkout and verify its existing archive markers are consistent → verify: build an unambiguous archived-entry inventory, recording current titles and destinations; resolve uncertain status with catalog maintainers before editing.
- [ ] 1.2 Add the plain word `Archived` beside each archived entry in `catalog.md`, outside its existing linked title → verify: every inventoried archived entry has one label, active entries have none, and titles, destinations, ordering, and visibility are preserved.
- [ ] 1.3 Preview the Markdown and inspect the catalog diff → verify: labels sit beside the intended entries, archived links remain clickable, and the change includes no color, filtering, automatic archival, dependencies, or generation automation.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#final-verification), [Acceptance checks](design.md#acceptance-checks)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the Markdown catalog change; run the applicable full repository suite if present and complete the inventory and rendered-preview checks → verify: record actual results and confirm every design acceptance check passes.
- [ ] 2.2 Invoke `/kk:document` for relevant catalog guidance and feature status → verify: documentation matches the text-only behavior and preserves the separate future color decision.
- [ ] 2.3 Invoke `/kk:review-code` with Markdown as the language input for the catalog edit → verify: resolve or explicitly record review findings.
- [ ] 2.4 Invoke `/kk:review-spec` against the design and implementation plan → verify: confirm requirement coverage, validated archive markers, and accurate task completion state.

## Dependency Graph

```text
Task 1 ──→ Task 2
```

Color selection remains future work owned by catalog maintainers, whose next step is checking the site's contrast. It is not part of either task.
