# Tasks: Archive label

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, color changes

The design and refinement choices are accepted. Implementation has not begun. `catalog.md` is not present in the planning workspace; the implementing contributor must inspect the actual file before editing. Future color selection belongs to catalog maintainers after a site contrast check and is outside these tasks.

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label archived entries](implementation.md#label-archived-entries)

### Subtasks

- [ ] 1.1 Inspect `catalog.md` and validate the assumption that authors mark archived entries consistently → verify: each entry has an unambiguous archived or active classification under the existing convention; refer ambiguous cases to catalog maintainers before editing.
- [ ] 1.2 Add plain text `Archived` beside every archived linked title in `catalog.md`, outside the link text → verify: all archived entries have the label, active entries have none, and a comparison with the pre-edit file shows unchanged titles, destinations, archive markers, and unrelated content.
- [ ] 1.3 Inspect the rendered `catalog.md` → verify: labels appear beside archived entries, all archived links remain visible and clickable, and the diff contains only the intended label additions. Record the checks performed.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `/kk:test` for the catalog change → verify: the existing full test suite passes if one exists, and the [acceptance checks](design.md#acceptance-checks) pass. If no suite exists, record that and the source/rendered checks without adding test infrastructure.
- [ ] 2.2 Invoke `/kk:document` → verify: relevant existing documentation explains the manual label convention where needed, these documents reflect completed work and actual verification, and color remains future work.
- [ ] 2.3 Invoke `/kk:review-code` with project input `Markdown catalog content; no runtime language` → verify: review the catalog diff and resolve applicable findings concerning labels, titles, destinations, and visibility.
- [ ] 2.4 Invoke `/kk:review-spec` for `archive-label` → verify: the implementation satisfies the design and implementation plan, preserves scope exclusions, and has no unresolved discrepancies before setting feature status to `done`.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
