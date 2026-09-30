# Archive label design

Status: accepted design; implementation pending.

## Purpose and success

The catalog maintainer wants contributors to recognize archived entries without
opening each one. The planned change adds the word **Archived** beside every
archived entry in the manually maintained `catalog.md`. Active entries have no
label. Archived entries remain visible and clickable, with their existing titles
and destinations preserved.

For example, an entry identified as archived keeps its existing title and link and
gains the adjacent word Archived. An active entry keeps its title and link without
that label. Success means this distinction holds for every catalog entry.

## Accepted approach

This is a simple text edit to the static catalog. Contributors will add the label
beside each archived entry's link, outside the existing link title. Preserve the
catalog's surrounding format. Do not introduce dependencies or automate catalog
generation.
There is no runtime application in the supplied workspace.

The problem framing, contributor audience, success condition, constraints, chosen
direction and design presentation are approved. This document records those
requirements; it does not claim the labels have been implemented or verified.

## Assumptions

Authors already mark archived entries consistently. Before editing, the contributor
must inspect the existing catalog and confirm how those marks identify the entries
to label. Do not infer archival status from age or an entry's title. If the marks
are missing or inconsistent, ask the catalog maintainers to resolve the affected
entries before applying labels.

## Not Doing

- Filtering: archived entries must remain visible and clickable.
- Automatic archival: authors continue to maintain archival status manually.
- Color changes: this increment adds only label text; color remains undecided.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links.

## Open decision and evidence limit

Catalog maintainers own the future color decision. Their next step is to choose a
color after checking the site's contrast. That decision is outside this text-only
increment and does not block it.

Only the accepted requirements were supplied; `catalog.md` is absent from this
workspace. Its layout, archival marks and rendered result have not been inspected.
The implementing contributor must obtain the catalog before validating the
assumption or editing entries; maintainers must resolve any ambiguous status.

## Implementation handoff

Follow the [implementation plan](./implementation.md) and [task list](./tasks.md).
The label edit and final verification are both pending. The recommended design
review is `/kk:review-design archive-label`; it has not been run.
