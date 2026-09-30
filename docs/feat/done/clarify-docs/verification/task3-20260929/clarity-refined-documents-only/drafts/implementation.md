# Implementation

Implement the [label contract](design.md#label-contract) by manually adding the
text “Archived” beside each archived entry in `catalog.md`. For an archived
entry, readers should still see the same title and be able to follow the same
link after the label is added. Active entries must stay unchanged.

## Assumptions

Entries already identify archive state. [Task 1](tasks.md#task-1-inspect-existing-archive-state)
records that this was checked. The catalog itself is not supplied with these
planning documents, so its markup, entry list and archive-state markers have not
been inspected during this refinement. The implementer must inspect `catalog.md`
before editing; if it is unavailable or its archive state is unclear, record the
blocker and resolve it with the catalog maintainers before labeling entries.

## Implementation steps

These steps expand the pending [Task 2](tasks.md#task-2-add-text-labels). They do
not repeat or change Task 1's completed status.

1. Inspect `catalog.md` and record which entries are archived, using the existing
   archive-state markers. Retain the pre-edit file for comparison. → verify:
   archived and active entries can be distinguished from existing information;
   do not infer archive state from an entry's title or destination.
2. Add the literal text “Archived” beside every archived entry using the
   catalog's existing markup. Keep each title and link intact. Leave active
   entries unchanged. → verify: every archived entry displays the label beside
   its title, and its title text and link destination match the pre-edit file.
3. Compare the full edited catalog with the pre-edit file. → verify: the change
   adds labels only to archived entries; active entries are unchanged, no entry
   has been hidden or removed, and no titles or links have changed. Inspect the
   rendered Markdown as well to confirm that the labels appear beside the
   corresponding entries.

Once Task 2 is implemented, follow the existing
[Task 3](tasks.md#task-3-final-verification) verification sequence. No catalog
edits or implementation checks have been performed as part of this refinement.

## Not Doing

- Filtering: readers must retain access to archived entries and their links.
- Automatic archival: this change manually labels entries whose archive state
  already exists.
- Color changes: the text-label change does not depend on a color choice.

## Rejected Alternatives

Hiding archived entries would remove links readers still need.

## Open decision

Catalog maintainers will choose a color after checking contrast. That decision
remains pending and does not block the text labels; do not introduce a color
choice while implementing this plan.
