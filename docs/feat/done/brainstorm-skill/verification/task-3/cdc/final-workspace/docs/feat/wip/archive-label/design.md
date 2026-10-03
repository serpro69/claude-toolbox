# Archive labels in the static catalog

Status: approved design; implementation pending.

Source: [accepted decisions](../../../../accepted.md). See the [implementation plan](implementation.md) and [tasks](tasks.md).

## Problem and success condition

The catalog maintainer wants contributors to recognize archived entries without opening each entry. The catalog is manually maintained in `catalog.md`; there is no runtime application in this workspace.

Success means every archived entry displays the exact word **Archived** beside the entry, while active entries have no archive label. Archived entries remain visible and clickable, with their existing titles and link destinations preserved.

The problem framing, contributor persona, constraints, simple-change classification, chosen direction, and design presentation are already approved.

## Accepted behavior

Add a plain textual `Archived` label beside each archived entry in `catalog.md`. Keep the label outside the existing linked title so that both the title and destination remain unchanged. Match the catalog's surrounding Markdown layout without adding styling or generation machinery.

Do not hide entries or change their ordering as part of adding labels. Leave active entries without a label. This is a manual catalog edit, with no dependencies or application code.

## Assumptions

Authors already mark archived entries consistently. Before editing, inspect `catalog.md` and its authoring guidance to establish which existing marker identifies an archived entry and confirm that it is used consistently. Do not infer archival from an entry's age, title, or a broken link.

Only `accepted.md` is present in the supplied workspace; `catalog.md` and its actual marker convention have not been inspected. If the markers are missing or ambiguous in the implementation checkout, resolve the affected entries with the catalog maintainers before labeling them.

## Not Doing

- Filtering: readers still need to see and follow archived entries.
- Automatic archival: this increment labels existing archive status rather than deciding or changing it.
- Color changes: the color decision is unresolved and outside this text-only increment.
- Catalog generation automation or new dependencies: the catalog remains manually maintained.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. The chosen textual label exposes status while retaining access.

## Future decision

Label color is undecided. **Owner:** catalog maintainers. **Next step:** check the site's contrast before choosing a color. This is future work, not an approved color requirement or a condition for completing the text-only increment.

## Acceptance checks

- Establish an inventory of archived entries using the verified existing marker convention.
- Confirm each archived entry displays one `Archived` label beside its title and that active entries display none.
- Compare titles and link destinations before and after the edit; they must match.
- Preview the Markdown and confirm archived entries remain visible and their existing links are clickable.
- Confirm the change introduces no filtering, archival automation, color styling, dependencies, or catalog generation.
