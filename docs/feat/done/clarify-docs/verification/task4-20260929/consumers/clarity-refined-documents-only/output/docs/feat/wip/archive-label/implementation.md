# Implementation

Add the text `Archived` beside each archived entry in `catalog.md` so readers can
recognize its status and still follow its link. Keep every entry's existing title
and link, and leave active entries unchanged. This is planned manual editing;
there is no runtime application to implement.

The [accepted label contract](design.md#label-contract) governs the work.
[Task 1](tasks.md#task-1-inspect-existing-archive-state) is done; the label edits
and final verification in Tasks 2 and 3 remain pending.

## Implementation steps

1. **Identify the entries to label in `catalog.md`.** Use the existing archive
   state checked in Task 1 to distinguish archived entries from active entries.
   Record the existing titles and link destinations for comparison after editing.
   → **Verify:** each intended edit corresponds to an entry already marked as
   archived; the active entries are excluded from the edit set.
2. **Add the labels for Task 2.** Manually insert `Archived` beside each archived
   entry, preserving its title, link and existing archive state. For example, an
   archived entry keeps its title linked to the same destination and gains the
   adjacent text label; an active entry receives no change.
   → **Verify:** compare `catalog.md` before and after editing. Every archived
   entry has the label, titles and links are preserved, and active entries are
   unchanged. Check the rendered catalog to confirm labels appear beside their
   entries and links remain usable.
3. **Complete Task 3 after the edits.** Follow the existing
   [final verification task](tasks.md#task-3-final-verification): run `/kk:test`,
   `/kk:document`, `/kk:review-code` and `/kk:review-spec`.
   → **Verify:** the applicable checks pass and documentation matches the label
   contract, including unchanged active entries and retained titles and links.

## Assumptions

Entries already identify archive state; Task 1 records that this was checked.
This refinement uses the accepted design and task record. `catalog.md` was not
available within the permitted source scope, so the checks above are planned
verification, not evidence that the labels have been added or tested. The
implementer must inspect the catalog when carrying out the steps.

## Not Doing

Filtering, automatic archival and color changes are outside the accepted scope.
This work adds manual text labels while preserving access to existing entries.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links.

## Open decision

Catalog maintainers will choose a color after checking contrast. The text labels
do not depend on that choice; it remains open and does not block these steps.
