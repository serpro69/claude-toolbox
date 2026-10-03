# Archive command design

> Status: approved for planning; implementation pending
> Requirements: [README.md](../../../../README.md)
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)

## Problem and user

The collection owner needs to retire one note while retaining access to it. The archive command marks the selected note as archived without deleting it, hiding it from the ordinary list, moving it, or changing its content or links.

The problem framing and the design below were confirmed with the user before these documents were written.

## Current state

The requirements describe items with a stable ID, title, body, and archived flag. Ordinary listing includes active and archived items and marks them distinctly. Existing editing preserves IDs and links.

This planning workspace contains only `README.md`; it has no runtime source or selected language. These statements describe the required host behavior, not inspected implementation. No command dispatcher, storage API, executable name, or test runner has been verified. The implementation plan must resolve those integration points in the eventual host project before coding.

## Scope and success criteria

The command accepts exactly one existing stable item ID for its successful archive path. Its observable outcomes are:

| Initial condition | Result | Permitted state change |
| --- | --- | --- |
| Selected item exists and is active | Report newly archived | Set only that item's archived flag to true |
| Selected item already is archived | Report already archived as a successful no-op | None |
| ID does not exist | Report missing item as an unsuccessful lookup | None |

Success requires all of the following:

- Exactly the selected item changes on the active-item path.
- Its stable ID, title, body, links, and any other stored fields are preserved.
- Every other item remains unchanged.
- The archived item remains in ordinary listing with the existing archived marker.
- Existing links continue to resolve to the same item and content.
- Repeating the command produces no further state change.
- A missing ID changes no item.

Use the host's established argument, output, and error conventions. The command takes one ID; it introduces no multi-ID or selector syntax. Exact executable spelling, numeric exit codes, and message wording must be mapped to host conventions during implementation rather than invented here. Their semantic distinction—newly archived, already archived, or missing—is fixed by this design.

## Chosen behavior and integration

Use a direct archive-flag update in the archive command handler. Resolve the selected ID through the existing collection lookup. Check for a missing item before attempting any mutation. For an already archived item, return the no-op outcome without issuing another update. For an active item, update its archived flag using the host's existing persistence mechanism and report success only after that mechanism confirms success.

Preserve the existing item identity and location. Reuse ordinary listing and existing link resolution. Archive does not introduce a second collection, new listing filter, link rewriting, or an alternative storage format.

If the host update fails, report failure using its existing error convention. Do not emit a successful archive result for a failed update. The design relies on the host's persistence guarantees; identifying an inability to update one item without collateral changes is a prerequisite failure to resolve before implementation, not permission to replace storage.

## Alternatives and decision

This is a simple, single-purpose change with one confirmed caller. Constraint mapping favors the smallest approach satisfying preservation and visibility requirements.

| Direction | User value | Feasibility | Differentiation for this increment |
| --- | --- | --- | --- |
| Direct flag update | Meets the complete requested behavior | Smallest implementation and integration surface | Keeps the behavior in its sole caller |
| Reusable archive operation called by the command | Same immediate behavior | Adds a separate operation boundary | Could serve future callers, but none are in scope |

The user selected the direct update. No new API, library, framework, or dependency is recommended.

## Assumptions

- **Must be true:** An ID resolves to at most one item. Validate this against the host's item lookup and representative fixtures before wiring the command.
- **Must be true:** The host can update the selected item's archived flag while preserving all other item fields and collection entries. Validate with full before/after collection comparisons.
- **Must be true:** Ordinary listing includes archived items and distinguishes them. Validate the existing behavior before integration and through the archive-to-list acceptance test.
- **Must be true:** Stable IDs and unchanged item location preserve existing link resolution. Exercise a link to the selected item before and after archiving.
- **Should be true:** The host has established command, persistence-error, and testing conventions that can be reused without dependencies. Record the actual integration paths and commands once host source is available.

These are explicit implementation checks. No runtime behavior has been independently verified in this planning workspace.

## Not Doing

- **Deletion:** The item and its content must be retained.
- **Hiding:** Ordinary listing must continue to show the archived item.
- **Moving notes:** Keeping location and identity intact preserves access and avoids another archive store.
- **Bulk operations:** This increment acts on one ID only.
- **Restore:** Reversing archived state is a separate user operation outside this increment.
- **Synchronization:** The workflow is local and offline.
- **New dependencies and network access:** Neither is needed for an existing flag update.
- **Runtime or storage replacement:** The plan integrates with a host project; it does not select a language or build a new note application.

## Rejected Alternatives

- **Reusable archive operation:** Adds a boundary without a confirmed second caller; direct command handling is sufficient for the agreed scope.
- **Hiding archived notes:** Conflicts with required ordinary-list visibility.
- **Moving notes to another location or collection:** Conflicts with the agreed preservation approach and introduces avoidable link and identity risk.

## Verification and completion

Use a small collection containing an active target, an already archived note, and an unrelated note, with a resolvable link to the target. Compare full collection snapshots, not just the flag, to detect unintended changes. Exercise successful archive, repeated archive, and missing-ID paths through the public command boundary. Check ordinary listing and link access after the successful archive. Verify that a failed persistence operation cannot produce a success report using the host's existing testing facilities.

Implementation is complete when these acceptance checks pass in the host project, its relevant regression suite remains green, and documentation describes the actual command syntax and outcomes. Writing this design does not constitute runtime validation or independent design review.
