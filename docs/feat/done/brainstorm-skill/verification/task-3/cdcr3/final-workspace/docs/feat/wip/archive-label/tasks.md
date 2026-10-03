# Tasks: Archive labels

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, color changes

Refinement and design presentation are approved. Implementation has not begun. Color remains a future decision owned by catalog maintainers, whose next step is checking the site's contrast before choosing it. No new dependency or catalog-generation automation is part of these tasks.

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label edit](implementation.md#label-edit), [Accepted design](design.md#accepted-design)

### Subtasks

- [ ] 1.1 Locate `catalog.md` and validate consistent archive markings → verify: every entry has an unambiguous archived/active classification; otherwise block this task until catalog maintainers resolve the missing file or unclear markings.
- [ ] 1.2 Record the existing entries, classifications, titles and destinations → verify: the comparison baseline covers the complete catalog.
- [ ] 1.3 Append ` — Archived` beside each archived entry's link in `catalog.md`, outside its title → verify: each archived entry has exactly one label and active entries have none.
- [ ] 1.4 Compare the diff with the baseline and preview rendered Markdown → verify: all titles and destinations match, entries retain their order and visibility, archived links remain clickable, and only label text has changed.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#final-verification), [Acceptance checks](design.md#acceptance-checks)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the full existing suite and catalog acceptance checks → verify: record actual results; if no suite exists, document manual checks without claiming automated tests ran.
- [ ] 2.2 Invoke `/kk:document` for relevant documentation → verify: any necessary updates preserve the distinction between delivered text labels and undecided color.
- [ ] 2.3 Invoke `/kk:review-code` with Markdown as the project language/content input → verify: actionable findings are resolved within the accepted scope.
- [ ] 2.4 Invoke `/kk:review-spec` for this feature → verify: the implementation satisfies the design and implementation plan, including exclusions.
- [ ] 2.5 Record verification evidence and update task status → verify: all preceding checks are complete before marking the feature done; color remains assigned to catalog maintainers for a later contrast-informed decision.

## Dependency Graph

```text
Task 1: Label entries ──→ Task 2: Final verification
```
