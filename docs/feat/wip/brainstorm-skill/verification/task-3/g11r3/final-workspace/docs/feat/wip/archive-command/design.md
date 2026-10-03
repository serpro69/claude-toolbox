# Archive command design

Status: approved for planning; implementation not started.

Source: [README.md](../../../../README.md). See the [implementation plan](implementation.md) and [task list](tasks.md).

## Problem and intended user

The owner of a local note collection needs to retire one note while retaining access to it. Archival must preserve the note's identity, content, links, and place in ordinary listing.

The collection already has stable item IDs, titles, bodies, and archived flags. README.md states that listing includes active and archived items with distinct markings, and editing preserves IDs and links. This planning workspace contains no runtime source or selected implementation language. These are documented requirements, not mechanisms verified in code.

## Success criteria

- Selecting one existing active ID marks exactly that item archived.
- The selected item's ID, title, body, links, and collection membership are preserved. Every other item is unchanged.
- Ordinary listing still includes the item, marked archived, and its links continue to work.
- Repeating the command produces the same archived state without another save or other state changes.
- A missing ID is reported without changing any item.
- The operation runs locally, offline, without new dependencies.

## Chosen approach

Use a dedicated archive operation that directly updates the selected item's archived flag. Its responsibilities are input validation, exact ID lookup, distinguishing missing/already-archived/active items, persisting the one permitted change, and reporting the outcome.

The design introduces no generic mutation framework. The eventual command should use the collection's storage boundary rather than creating a second collection or moving notes between locations. Storage, language, and host CLI details must be resolved against the runtime before implementation; none exists in this workspace.

## Command contract

The conceptual invocation is `archive <id>`. The host executable and concrete argument parser remain unspecified. The command accepts exactly one ID, using the collection's existing ID representation and lookup semantics; it must not introduce ID rewriting.

| Input state | Behavior | Outcome |
| --- | --- | --- |
| Existing active item | Persist only its archived flag as true | Success: archived |
| Existing archived item | Return without saving or changing collection state | Success: already archived |
| Missing ID | Report the missing item; do not save | Failure: item not found |
| Missing argument or more than one ID | Reject the invocation before mutation | Failure: invalid invocation |
| Persistence failure | Report failure; never report a successful archive | Failure: could not persist |

Outcome names express semantics, not mandated message strings or numeric exit codes. Use the eventual CLI's conventions. An already archived item is a successful no-op, allowing safe retries.

## Preservation and persistence

Lookup completes before mutation. For an active item, the only requested durable change is the archived flag from false to true. Preserve all other item data, including fields beyond the four described in README.md if the eventual runtime contains them. Do not modify another item, remove the selected item, or alter references to it.

Success is reported only after persistence succeeds. The implementation must inspect and document the chosen storage boundary's failure guarantees. This design does not claim that an absent storage implementation already provides atomic writes or rollback. A deterministic failure before commit must leave durable state unchanged; uncertainty about partially committed writes must be resolved before implementation is considered complete. Do not conceal a persistence failure with a success message.

## Listing, links, and editing

Ordinary listing retains both active and archived items, with its existing distinction between them. Archival must not add a default filter or change the selected item's location or ID. Preserve links both within the selected note and from other notes to it. Editing remains available with the preservation behavior documented in README.md.

## Assumptions

1. Stable IDs uniquely identify items within the collection. Validate against the eventual model and lookup implementation; duplicate matches must not result in modifying multiple items.
2. The eventual storage boundary can persist the archived flag while preserving the rest of the collection. Validate its update and failure behavior before relying on it.
3. The listing and editing behavior in README.md is the intended runtime baseline. Verify this through integration tests once runtime source exists; this workspace cannot establish it experimentally.

## Not Doing

- Deletion, hiding, or moving notes: each conflicts with the agreed preservation and access behavior.
- Bulk operations: this increment acts on exactly one selected ID.
- Restore: reversing archival is outside the requested command.
- Synchronization: the operation is confined to the local collection.
- New dependencies or network access: existing capabilities must support offline operation.
- A generic item-update framework: its broader reuse is unnecessary for the selected increment.

## Rejected Alternatives

| Alternative | User value and feasibility | Reason rejected |
| --- | --- | --- |
| Route archive and editing through a new shared item-update operation | Same archive outcome, with potential reuse but broader integration work | The direct operation meets the requirement with a smaller change |
| Hide archived notes from ordinary listing | Could shorten the list but removes ordinary access | Violates the explicit visibility requirement |
| Move archived notes elsewhere | Could physically separate retired notes but changes their location | The owner explicitly rejected moving notes and requires preserved access and links |

## Acceptance scenarios

| ID | Scenario | Required observation |
| --- | --- | --- |
| A1 | Archive an active item among multiple items | Exactly the selected archived flag changes; all other data remains equal |
| A2 | List and follow links after A1 | The same ID appears with archived marking; incoming and outgoing links still resolve |
| A3 | Archive an already archived item, including a repeat of A1 | Successful no-op; no persistence call and no state changes |
| A4 | Archive a missing ID | Item-not-found outcome; no persistence call and identical collection state |
| A5 | Invoke with no ID or multiple IDs | Invalid-invocation outcome before mutation; identical collection state |
| A6 | Fail persistence before commit | Failure outcome, no success output, and unchanged durable collection |
| A7 | Edit an archived item through the ordinary editing path | Editing remains available and retains the stable ID and working links |
| A8 | Execute the command with network access unavailable | The relevant A1–A7 paths require no network and introduce no dependency |

Use distinctive titles, bodies, links, and unrelated items so preservation assertions can detect accidental replacement, deletion, or broad updates.

## Implementation readiness

Before coding, identify or establish the authorized host runtime, command entry point, storage boundary, listing/link/editing paths, and test harness. Record their concrete file paths in the implementation plan. This planning task does not select a language, create a runtime, implement the command, run tests, or execute a follow-up review.
