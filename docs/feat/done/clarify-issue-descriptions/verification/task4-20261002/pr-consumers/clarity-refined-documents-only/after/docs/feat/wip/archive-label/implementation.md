# Implementation

Follow the accepted [label contract](design.md#label-contract): manually add
`Archived` beside each archived entry in `catalog.md`, preserving its title and
link. Leave active entries unchanged. [Task 1](tasks.md#task-1-inspect-existing-archive-state)
is complete; the next work is Task 2.

## Task 2: Add text labels

1. Locate the entries in `catalog.md` that already identify themselves as archived,
   using the archive markings checked in Task 1. Use those markings to select the
   entries to edit → verify: every selected entry has an existing archive marking,
   and no active entry is selected.
2. Add the plain-text label `Archived` beside each selected entry's title and link,
   outside the link itself. Keep the existing title text, link destination and
   archive marking → verify: every archived entry displays `Archived` next to its
   unchanged title and link.
3. Compare `catalog.md` with its pre-edit version → verify: the changes only add
   the labels; every original entry remains in place, all titles and link
   destinations are preserved, and active entries are unchanged.

## Task 3: Final verification

After Task 2, follow the existing [final verification task](tasks.md#task-3-final-verification):
run `/kk:test`, `/kk:document`, `/kk:review-code` and `/kk:review-spec`
→ verify: the applicable checks pass and documentation matches the label contract.
Report any checks that could not run. This is planned work for implementation;
the current refinement stops at handoff.

## Assumptions

Entries already identify their archive state; Task 1 checked this. The implementer
can therefore select archived entries from existing markings without inventing a
new classification rule.

## Not Doing

- Filtering: retain the catalog entries and their destinations.
- Automatic archival: this change is a manual text edit with no runtime app.
- Color changes: catalog maintainers own the color decision and will check contrast
  before choosing a color. Text labels do not depend on that choice.

## Rejected Alternatives

Hiding archived entries would remove links readers still need.
