# Archive labels in the static catalog

Status: design accepted; implementation pending.

Source: [accepted decisions](../../../../accepted.md). See the [implementation plan](implementation.md) and [task list](tasks.md).

## Problem and success condition

Contributors need to recognize archived entries without opening each entry. The catalog maintainer owns a manually maintained `catalog.md`; there is no runtime application. Success means every archived entry displays the word `Archived`, every active entry has no archive label, and all existing titles and link destinations are preserved.

The problem framing, contributor audience, success condition, constraints, simple-change classification, chosen direction and design presentation are already approved.

## Accepted design

Add a textual `Archived` label beside each archived entry in `catalog.md`. For implementation, place the suffix ` — Archived` immediately after the existing entry link, outside its link text. Preserve each entry's title, destination, position and visibility. Archived entries remain clickable. Apply the label once per archived entry; active entries receive none.

Use the catalog's existing archival markings to identify entries. Do not infer archival from a title, age or destination, and do not establish a new archive policy. Catalog maintainers continue maintaining the file by hand. No dependency or catalog-generation automation is needed.

## Current evidence and assumptions

The supplied workspace contains `accepted.md` but no `catalog.md`. Entry structure, individual archive states and the marking convention have therefore not been inspected. The file name and behavior above come from the accepted decisions.

Assumption: authors already mark archived entries consistently. Before implementation, locate `catalog.md` and verify that its markings distinguish archived from active entries without guessing. If the file or a reliable classification is unavailable, record the implementation task as blocked and have the catalog maintainers resolve it before editing labels.

## Not Doing

- Filtering: archived entries must remain visible and accessible.
- Automatic archival: maintainers retain control of entry state.
- Color changes: this increment changes label text only; a contrast check is still needed before choosing color.

Catalog-generation automation and new dependencies are also outside the accepted implementation approach.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. Keeping entries visible with a textual label meets the identification goal while preserving access.

## Future decision

Color is undecided and is not an implementation requirement for this increment. Owner: catalog maintainers. Next step: check the site's contrast, then choose a color. Completing these label tasks does not imply that color has been selected or that the contrast check has happened.

## Acceptance checks

Compare the catalog before and after editing. Every entry classified as archived must have one visible `Archived` label beside its link; active entries must have none. All original titles and destinations must match, and no entry may be removed, hidden or reordered. Inspect the rendered Markdown to confirm the labels are outside the clickable titles and archived links remain usable. No styling or automation changes belong in the diff.
