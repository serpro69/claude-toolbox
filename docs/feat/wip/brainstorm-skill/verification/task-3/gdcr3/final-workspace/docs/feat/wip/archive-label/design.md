# Archive labels in the static catalog

> Status: approved design; implementation pending
> Decision source: [accepted.md](../../../../accepted.md)
> Plan: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)

## Problem and success condition

The catalog maintainer wants contributors to recognize archived entries without opening each entry. Every archived entry must display the word **Archived** beside it. Active entries must have no archive label.

The catalog is manually maintained in `catalog.md`; there is no runtime application. This is a small text edit for a contributor who may be unfamiliar with the catalog. The framing, contributor persona, success condition, constraints, chosen approach, and design presentation are already approved.

## Accepted behavior

Add the plain text `Archived` beside each archived entry's existing title/link, using the surrounding Markdown layout to keep the association clear. Keep the label outside the existing link text so the title stays unchanged. Archived entries remain visible and clickable. Preserve every existing title and link destination, including those of active entries.

The increment changes label text only. It introduces no dependencies, generation scripts, runtime components, or new archival policy. Catalog maintainers continue to own the catalog and determine which entries are archived.

## Assumptions

Authors already mark archived entries consistently. Before implementing, inspect `catalog.md` and identify the existing convention and complete archived-entry set. Verify that the convention distinguishes archived and active entries without guessing from entry age or link status. If it is missing or ambiguous, resolve that classification with the catalog maintainers before applying labels.

Only `accepted.md` was available in the drafting workspace. The catalog's actual layout, archive markers, entry count, and rendering configuration have not been inspected. The implementation plan therefore requires that inspection before editing and does not invent marker syntax or test commands.

## Not Doing

- Filtering: archived entries must remain discoverable and their links accessible.
- Automatic archival: maintainers retain manual control of archival status.
- Color changes: this increment approves label text only; no color has been chosen.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. A textual label makes archive status visible while preserving access, with a small manual edit that fits the existing catalog.

## Future decision

Catalog maintainers own the next color decision: choose a color after checking the site's contrast. This is a future decision, not an accepted color requirement or an implementation task in this increment.

## Acceptance checks

1. Every entry identified as archived through the existing convention displays `Archived` beside its title/link in the rendered catalog.
2. Active entries display no archive label.
3. Entry titles and link destinations match the pre-edit catalog; archived links remain clickable and entries remain visible.
4. The diff contains only the necessary label text and local spacing, with no filtering, archival automation, or color changes.
