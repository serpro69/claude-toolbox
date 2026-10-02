# Archive labels

> Status: accepted decisions documented; implementation pending
> Source: [accepted.md](../../../../accepted.md)
> Plan: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Problem and success condition

Catalog maintainers want contributors to recognize archived entries without opening each entry. The catalog is maintained manually in `catalog.md`; there is no runtime application in this workspace.

Success means every archived entry displays the word `Archived`, active entries have no label, and every existing entry remains visible with its original title and link destination.

## Accepted design

Add the plain textual label `Archived` beside each archived entry's existing link, outside the link text so the title stays unchanged. Retain the entry and its clickable link. Use the catalog's existing archival markers to identify which entries need the label, after verifying that those markers are consistent.

This is a small manual Markdown edit. It requires no dependencies or catalog generation. The problem framing, contributor audience, success condition, constraints, chosen direction, and design presentation are already approved.

## Assumptions

Authors already mark archived entries consistently. Before editing, inspect `catalog.md` and identify the convention that distinguishes archived entries from active ones. If the convention is absent or ambiguous, resolve that ambiguity with catalog maintainers before assigning labels; do not infer archival status from titles or link destinations.

The catalog itself was not available in the supplied drafting scope. Its exact layout and archival markers still need verification during implementation.

## Not Doing

- Filtering: readers still need access to the existing catalog entries and links.
- Automatic archival: this increment labels entries whose archival status authors already maintain.
- Color changes: no color has been chosen; the approved increment adds text only.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. Keeping entries visible with a textual label provides status information while preserving access.

## Future color decision

Color remains undecided. Catalog maintainers own the next step: choose a color after checking the site's contrast. That future decision does not block the text-only change and is not an implementation task in this increment.

## Acceptance checks

Compare every entry against the verified archival convention. Each archived entry must show `Archived`; each active entry must have no label. Check both Markdown and its rendered presentation to confirm the label is beside the entry and its original title and clickable destination are preserved. The diff must contain only the intended label text and necessary spacing.
