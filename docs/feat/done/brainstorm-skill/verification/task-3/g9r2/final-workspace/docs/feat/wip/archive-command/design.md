# Archive command design

> Status: approved for planning; implementation pending
> Source: [README](../../../../README.md)
> Implementation: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Problem and outcome

The collection owner needs to retire one note while retaining access to its content and links. Archiving must preserve ordinary-list visibility and must not delete or move the note.

Success means selecting one existing stable ID marks exactly that item archived. Its title, body, ID, and links remain unchanged; ordinary listing still shows it with the existing archived distinction. Repeating the operation changes nothing further. A missing ID is reported without changing any item.

## Current state and evidence

The README establishes that items already have a stable ID, title, body, and archived flag. Ordinary listing already includes active and archived items and distinguishes their states. Editing preserves IDs and links.

This planning workspace contains no runtime source, selected language, command parser, persistence implementation, or test runner. Component names below describe responsibilities, not discovered modules. The implementation plan requires mapping these responsibilities to actual files before coding; it does not introduce a runtime or storage technology.

## Command contract

The command shape is `archive <id>`, under the eventual tool's existing executable and command conventions. It accepts exactly one ID and follows the existing ID-resolution rules. This design does not invent a new ID format or executable name.

| Input and state | Result | Permitted state change |
| --- | --- | --- |
| Existing active ID | Successful archival | Only that item's archived flag becomes true |
| Existing archived ID | Successful no-op | None; skip persistence |
| Missing ID | Missing-item error identifying the supplied ID | None |
| Missing argument or multiple IDs | Usage error | None |
| Lookup or persistence failure | Operation error; no success message | No unrelated item changes; preserve existing storage integrity guarantees |

Success output identifies the selected item. Repeated archival should make the already-archived result understandable while retaining success semantics. Errors use the project's error-output and exit-status conventions once those exist; exact message wording and numeric status codes are not specified here.

## Chosen behavior and integration

1. Validate that exactly one ID was supplied before attempting an update.
2. Resolve that ID through the collection's existing lookup behavior. A lookup failure must remain distinguishable from an absent item.
3. Report a missing item without initiating a write.
4. Return a successful no-op if the selected item is already archived.
5. Persist a targeted update setting its archived flag to true. Do not rebuild the note from partial input or route it through title/body editing.
6. Report success only after persistence succeeds.

Reuse the collection's existing persistence mechanism. The direct update is a behavioral requirement, not a demand for a new low-level storage API. If storage rewrites a collection file, preserve every other record and field and use its existing safe-save mechanism. An in-memory mutation must not be presented as committed when persistence fails.

Ordinary listing retains its existing inclusion and marking behavior. Links continue to resolve through the same stable IDs. No visibility filter, relocation, new metadata, archive timestamp, or content rewrite is part of this operation.

## Alternatives and decision

| Approach | User value | Feasibility | Distinguishing benefit |
| --- | --- | --- | --- |
| Dedicated archive-flag update — selected | Meets all preservation and idempotence requirements | Bounded change using existing item state | Explicit control over the sole permitted field change |
| Route through general editing | Could provide the same behavior | Depends on an unseen editing interface | Potential reuse if editing already supports safe partial updates |

### Rejected Alternatives

- **General editing as the archive operation:** its partial-update behavior cannot be established from this workspace. Use a dedicated archive operation while reusing appropriate lookup and persistence utilities.
- **Hiding archived notes:** violates the requirement that ordinary listing retain them.
- **Moving notes elsewhere:** adds storage changes and risks link stability without serving the required flag-only behavior.

## Assumptions

- The eventual implementation can resolve a single item through its stable ID. Verify the lookup interface and its missing-item result before implementing the handler.
- Its persistence mechanism can save an archived-flag change while preserving all other item and collection data. Verify this with before/after collection comparisons.
- The existing save mechanism provides an appropriate failure boundary for a one-item update. Inspect that mechanism and exercise a save failure; if it cannot preserve collection integrity, revise the implementation approach before claiming completion.

## Not Doing

- **Deletion:** archival preserves the item and its content.
- **Hiding:** archived items remain in ordinary listing.
- **Moving notes:** stable locations and links do not need a new archive store.
- **Bulk operations:** the command selects exactly one ID.
- **Restore:** reversing archival is outside this increment.
- **Synchronization:** this is an offline operation on a local collection.
- **New dependencies or network access:** the existing item model and local operations are sufficient.

## Acceptance and verification

Use an isolated collection with at least two items, including links to the selected item. Compare complete item values before and after each operation, not only the archived flag.

1. Archive an active ID: only its flag changes, and the other item is identical.
2. Run ordinary listing: the selected item remains present with the existing archived distinction.
3. Resolve its existing links: their targets and content remain valid.
4. Repeat archival: the entire collection is unchanged and no save is requested.
5. Supply an absent ID: an error is reported, the collection is unchanged, and no save is requested.
6. Supply zero or multiple IDs: a usage error occurs before mutation.
7. Exercise lookup and save failures: an operation error is reported without success output or corruption of unrelated items.

The plan remains language-neutral. Implementation file paths and executable test commands must come from the runtime project, not guesses made in this documentation-only workspace.
