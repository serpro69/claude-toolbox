# Archive command design

Status: approved design; implementation pending.

Source: [README.md](../../../../README.md). Related: [implementation plan](implementation.md), [tasks](tasks.md).

## Problem and user

The collection owner needs to retire an individual note while preserving access to it. The collection already distinguishes active and archived items in its ordinary listing. Each item has a stable ID, title, body, and archived flag; editing preserves IDs and links.

Archiving must change the item's state without deleting, hiding, or moving it. This increment adds a direct archive command for one selected ID.

## Current state and constraints

This planning workspace contains requirements in README.md, with no runtime source, selected language, persistence format, or test framework. Existing listing and editing behavior are specified requirements, not inspected implementations. The design therefore defines behavior and component responsibilities without claiming concrete source files or APIs exist.

Work stays offline and adds no dependencies. Keep the current item representation, stable IDs, links, and ordinary listing behavior.

## Command behavior

The command accepts exactly one item ID through the eventual command interface. Resolve the ID before changing state. Reject malformed invocation through that interface's existing argument-validation convention, without mutation.

| Initial condition | Result | Persistence effect |
| --- | --- | --- |
| ID exists and item is active | Report successful archival | Save only the selected item's archived flag as true |
| ID exists and item is archived | Report successful no-op | Do not perform another persistence write |
| ID does not exist | Report a clear missing-ID error | Change no item and perform no write |
| Saving fails | Report failure; do not claim archival succeeded | Follow the persistence mechanism's failure semantics |

Successful archival preserves the selected item's ID, title, body, and links, and preserves every other item. The implementation may physically rewrite a storage container if its format requires it, but the logical data difference must be only the selected flag. It must not generate a replacement ID or move the note.

The ordinary list continues to include the selected item, visibly marked archived using its established representation. Existing links still resolve to the same item, and existing editing behavior remains intact.

Exact command spelling, diagnostics, and exit-status conventions should follow the eventual application. The required distinction is success, successful no-op, missing item, or save failure; this design does not introduce a new output format.

## Implementation approach

Use the direct command path: validate input, resolve the ID, return the missing-item or already-archived outcome when applicable, otherwise update the flag and save. Reuse existing item lookup and persistence facilities if present when implementation begins. A new general archive service or abstraction is unnecessary for this single caller.

## Acceptance and verification

1. Given at least two active items, archive one selected ID. A before/after comparison differs only in that item's archived flag.
2. Reload through the normal read path and confirm that the archived state persists.
3. List the collection through its ordinary interface: the archived item remains present with its archived marking, and other entries retain their state.
4. Resolve existing links to and from the selected item; they retain their original targets. Exercise the existing edit path and confirm identity and links remain stable.
5. Repeat archival of the same ID: it succeeds without any further data change or persistence write.
6. Archive an absent ID: report the missing ID and retain an identical collection snapshot, with no write attempted.
7. Cause saving to fail using the eventual test framework's supported failure mechanism: the command reports failure rather than success.

These are planned checks. No runtime tests or independent review have been performed.

## Assumptions

- The eventual storage mechanism can persist a flag change while preserving all other logical data and link identities. Validate this with a complete before/after collection comparison and a normal reload.
- The normal list and edit paths satisfy README.md's existing behavior. Confirm this against the implementation before adding the command; do not silently compensate by changing their semantics.
- A stable ID uniquely identifies one item. Confirm the lookup contract before implementation; ambiguous lookup must not archive multiple items.

## Not Doing

- Deletion: archival must retain the item and its contents.
- Hiding: ordinary listing must continue to show archived items.
- Moving notes: relocation is unnecessary and risks link preservation.
- Bulk operations: this increment targets exactly one ID.
- Restore: reversing archival is a separate behavior outside this increment.
- Synchronization: the requested workflow is local and offline.
- New dependencies or a reusable archive service: the direct path requires neither.
- Runtime or persistence selection: the workspace has no implementation to anchor those choices.

## Rejected Alternatives

- A separate reusable archive operation: it provides the same immediate behavior while adding structure for callers that are not required.
- Hiding or moving archived notes: both depart from the required preservation of ordinary visibility and working links.

## Implementation handoff

Before coding, identify the actual runtime project and map command dispatch, ID lookup, persistence, ordinary listing/editing, link resolution, and tests to concrete source paths. If no runtime exists, runtime selection and bootstrap need a separate scope decision; do not assume a language or invent source files in this plan. Persistence failure recovery and concurrent-writer guarantees remain properties of that eventual mechanism and are not established by this planning workspace.
