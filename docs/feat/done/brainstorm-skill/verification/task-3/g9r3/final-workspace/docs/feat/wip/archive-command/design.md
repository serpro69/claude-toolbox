# Archive command design

> Status: approved design; implementation pending
> Source: [README](../../../../README.md)
> Implementation: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Problem and user

The collection owner needs to retire one note while preserving access to it. Archiving marks an item as archived while keeping its content, stable identity, links, and visibility in the ordinary list.

The approved framing is: how might we help the collection owner mark a note as archived without losing information or removing it from the ordinary list?

## Current state

The README describes a local collection whose items have a stable ID, title, body, and archived flag. Ordinary listing includes both active and archived items and marks them distinctly. Existing editing preserves IDs and links.

This planning workspace contains only the README. It supplies no runtime source, selected language, command entry point, persistence implementation, or test runner. References below to command dispatch, lookup, and persistence are integration responsibilities to locate before implementation, not claims about files or APIs already inspected.

## Success criteria

- Archiving an existing active ID changes exactly that item's archived flag to true.
- The selected item's ID, title, body, and links retain their previous values and behavior.
- Other items retain all their previous values.
- The archived item remains visible in the ordinary list with the existing archived marking.
- Repeating the command succeeds without further updates.
- A missing ID reports failure and changes no item.

## Command contract

The proposed command form is `archive <id>`. The executable name and its registration syntax follow the actual note tool once its source is available.

The command accepts exactly one stable ID. It follows existing ID syntax and matching rules; it introduces no title matching, partial matching, or new normalization. Missing or extra positional arguments are usage errors handled before mutation.

| Input and current state | Required behavior | Result |
| --- | --- | --- |
| Existing active ID | Set only that item's archived flag to true and persist | Success after persistence succeeds |
| Existing archived ID | Preserve state; do not issue another update | Success identifying the already-archived state |
| Unknown ID | Change nothing | Error identifying the missing ID |
| Missing or extra argument | Change nothing | Usage error |
| Lookup or persistence failure | Report the failure; never claim archival succeeded | Failure |

Successful outcomes use a successful exit status and a concise result identifying the selected ID. Errors use a failure status and the tool's established error output conventions. Exact message wording and numeric failure codes should follow existing conventions; no new output format is required.

## State and persistence

The command validates its arguments, resolves the exact ID, and checks the archived flag. If the item is already archived, it returns without a write. Otherwise, it updates the flag using the existing storage mechanism and reports success only after that mechanism confirms persistence.

The command must preserve the item record and its relationships. It must not recreate the note, change its ID, alter its title or body, move it, remove it, or change how ordinary listing selects records. Do not introduce additional archive timestamps or metadata fields in this increment. This is a state update within the existing item model, with no planned schema migration.

Lookup and persistence error behavior must be checked against the actual storage implementation before coding. Reuse its established failure guarantees. If it cannot perform the required update without damaging existing data or preserving the other fields, resolve that mismatch before implementation; this plan does not invent a transaction facility or claim crash-recovery guarantees absent from the README.

## Alternatives and decision

| Approach | User value | Feasibility | Practical difference |
| --- | --- | --- | --- |
| Direct archive-flag update | Meets every confirmed success criterion | Uses the existing state field and storage path | One invocation completes archival |
| Confirmation before update | Adds an opportunity to catch the wrong selection | Requires prompting and cancellation handling | Adds interaction to every archival |

The user chose the direct update. It provides the agreed behavior with fewer interactions and no extra state model.

## Assumptions

- **Must be true:** the eventual runtime has a way to resolve a stable ID to exactly one item. Validate the existing lookup contract and duplicate-ID handling before wiring the command.
- **Must be true:** the existing storage mechanism can persist the archived flag while preserving all other item data and links. Validate its update and failure behavior before selecting the concrete call path.
- **Must be true:** actual ordinary listing includes archived items with a distinct marking, and links resolve by preserved identity as described in the README. Check these behaviors in integration tests.
- **Should be true:** the tool provides reusable command dispatch and output conventions. Identify their concrete locations before implementation; if they are absent, clarify where this feature is to be integrated rather than building an unrelated tool.

These are testable expectations about the eventual runtime. They are not evidence that its source has been inspected.

## Not Doing

- **Deletion:** archiving must retain the item.
- **Hiding:** ordinary list visibility is part of the acceptance contract.
- **Moving notes:** changing their location is unnecessary and risks disrupting links.
- **Bulk operations:** this increment accepts one ID only.
- **Restore:** reversing archival is outside the requested operation.
- **Synchronization:** this is an offline local change.
- **New dependencies or network access:** the existing item model and local storage are sufficient for the approved behavior.
- **New archive metadata or a schema migration:** the archived flag already represents the required state.

## Rejected Alternatives

- **Confirmation prompt:** adds interaction and cancellation behavior that the chosen direct command does not need.
- **Hiding archived notes:** violates the required ordinary-list visibility.
- **Moving notes to a separate archive:** introduces relocation and link risks without helping the required flag update.

## Verification

Use a temporary collection with an active target, an already-archived item, an unrelated active item, and a link to the target. Capture the collection state before each operation and compare it afterward.

Verify the complete command path: successful persistence after reopening the store, exact field preservation, unchanged neighboring items, retained ordinary-list visibility and archived marking, and working links. Invoke the command twice and verify both stored state and absence of a second update. Exercise unknown IDs and invalid argument counts against the same preservation assertions.

Inject lookup and persistence failures through the actual runtime's supported test seams. Confirm failures are reported without success output and that stored data obeys the established storage guarantees. No tests or implementation are run during this planning task.
