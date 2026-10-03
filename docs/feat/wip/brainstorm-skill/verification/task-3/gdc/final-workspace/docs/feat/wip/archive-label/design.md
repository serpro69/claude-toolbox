# Archive label

> Status: accepted design; implementation pending
> Source: [accepted decisions](../../../../accepted.md)
> Plan: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Purpose and success

The catalog maintainer wants contributors to recognize archived entries without opening them. Every archived entry in the manually maintained `catalog.md` must display the exact word **Archived** beside its existing link. Active entries must have no archive label. Archived entries remain visible and clickable, with their existing titles and destinations preserved.

The problem framing, contributor persona, success condition, constraints, chosen direction and design presentation are approved. This document records those decisions for the next contributor.

## Accepted behavior

Add plain text `Archived` immediately after each archived entry's existing link. Leave the linked title and destination intact. Use the existing archive indication to identify entries; do not infer archival from an entry's age or a broken destination. Retain existing entries and archive indicators.

This is a manual Markdown edit. There is no runtime application, new dependency or catalog-generation mechanism. The available workspace contains `accepted.md`; `catalog.md` and its archive markers were not available for inspection. Exact entries and marker syntax must be established during implementation.

## Assumptions

Authors already mark archived entries consistently. Before editing, inspect the complete `catalog.md` and confirm that the existing indication distinguishes every archived entry from active entries. If the file is unavailable or an entry's status is ambiguous, obtain the catalog or resolve the status with a catalog maintainer before labeling it. Do not guess.

## Not Doing

- Filtering: readers still need access to archived entries and their links.
- Automatic archival or catalog generation: the catalog remains manually maintained.
- Color changes: only label text is approved for this increment.
- New dependencies: plain Markdown supports the accepted change.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. A visible textual label conveys status while preserving access.

## Future decision

Color is undecided. Catalog maintainers own the next step: check the site's contrast, then choose a color. This is a future edit, not an implementation requirement or a completion condition for the text label.

## Acceptance checks

Using the verified archive inventory, confirm that every archived entry has one adjacent `Archived` label and every active entry has none. Compare the edited catalog with its baseline: entry count, titles and link destinations must be identical. In the rendered Markdown, confirm that archived entries remain visible and their titles still link to the original destinations. No color styling, filtering or automation is introduced.
