# Archive label design

Status: accepted design; implementation pending.

Source: [accepted decisions](../../../../accepted.md). See the [implementation plan](implementation.md) and [tasks](tasks.md).

## Purpose and success condition

Contributors need to recognize archived catalog entries without opening each entry. Every archived entry must display the word `Archived` beside its title; active entries must have no label.

The catalog is manually maintained in `catalog.md`. There is no runtime application. The accepted approach is a small text edit, with no dependencies or catalog-generation automation.

## Accepted behavior

- Add the plain text `Archived` beside each archived entry's existing linked title, outside the link text.
- Preserve the existing titles and link destinations. Archived entries remain visible and clickable.
- Leave active entries unlabeled.
- Preserve existing archive markers and unrelated catalog content. Use those markers to identify archived entries after verifying they are consistent.

The contributor should follow the catalog's existing layout when placing the label. The required visible text is `Archived`; this increment does not introduce color or styling rules.

## Current evidence and implementation boundary

This workspace contains `accepted.md`; `catalog.md` is not supplied. Its layout, archive markers, and entry count have therefore not been inspected. The accepted requirements are sufficient to draft this plan, but the contributor must inspect the actual catalog before making the edit. This document does not claim that any entries have already been labeled or verified.

## Assumptions

Authors already mark archived entries consistently. Before implementation, inspect `catalog.md` and establish which existing marker identifies archived entries and whether it classifies all entries unambiguously. If markers are missing or conflicting, have the catalog maintainers resolve those entries before applying labels; do not infer archival from age, link availability, or titles.

## Not Doing

- Filtering: archived entries must remain visible with their links available.
- Automatic archival: catalog maintainers continue to decide and record archive status manually.
- Color changes: color is undecided and outside this text-only increment.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. A visible text label preserves access while communicating archive status.

## Future decision

Catalog maintainers own the color decision. Their next step is to choose a color after checking the site's contrast. This is future work, not an accepted color requirement, an implementation task here, or a condition for completing the text label.

## Acceptance checks

Compare the actual catalog before and after the edit. Every entry classified as archived by the verified existing markers must show `Archived`; every active entry must remain unlabeled. Confirm that all pre-existing titles and link destinations are identical, and inspect the rendered catalog to confirm archived links remain visible and clickable. The diff must contain only the intended label additions.
