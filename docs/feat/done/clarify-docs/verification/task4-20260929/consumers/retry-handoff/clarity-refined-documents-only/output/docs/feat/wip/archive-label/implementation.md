# Implementation

Add the text `Archived` beside each archived entry in `catalog.md` so readers can
recognize its status and still follow its link. Follow the accepted
[label contract](design.md#label-contract): retain every entry's title and link,
and leave active entries unchanged. This is a plan for manual editing; it adds no
runtime application.

## Implementation steps

[Task 1](tasks.md#task-1-inspect-existing-archive-state) is done. The next pending
task is [Task 2: Add text labels](tasks.md#task-2-add-text-labels).

1. Use the archive state confirmed in Task 1 to identify the archived entries in
   `catalog.md` → verify: every entry selected for a label is marked archived;
   active entries are excluded from the edit.
2. Add the literal text `Archived` beside each archived entry, keeping the label
   separate from its existing title and link → verify: each archived entry has
   the label, and its title, link text and link destination match the original.
3. Compare `catalog.md` before and after the edit → verify: the only changes are
   the labels; active entries remain unchanged, and no entries or links are
   removed.
4. Continue with [Task 3: Final verification](tasks.md#task-3-final-verification)
   after Task 2 is complete. Run `/kk:test`, `/kk:document`, `/kk:review-code` and
   `/kk:review-spec` as listed there → verify: applicable checks pass and the
   documentation matches the label contract.

## Assumptions

Entries already identify their archive state. The task record reports that
Task 1 verified this. This refinement uses the accepted design and task record;
`catalog.md` was not supplied for inspection, so the steps above describe planned
changes and checks rather than verified implementation results.

## Not Doing

Filtering, automatic archival and color changes are outside this text-label scope.

## Rejected Alternatives

Hiding archived entries would remove links readers still need.

## Open decision

Catalog maintainers will choose a color after checking contrast. Adding the text
labels does not depend on that decision; do not add color changes in this task.
