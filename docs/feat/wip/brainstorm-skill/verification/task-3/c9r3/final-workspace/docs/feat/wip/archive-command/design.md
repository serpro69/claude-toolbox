# Archive command design

> Status: approved for implementation planning
> Source: [README.md](../../../../README.md)
> Plan: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)
> Created: 2026-10-03

## Problem and intended user

The collection owner needs to retire an individual note while preserving access to it. Archiving must distinguish the note's state without deleting information, breaking links, or removing it from the ordinary list.

The README defines items with stable IDs, titles, bodies, and an archived flag. Ordinary listing already includes active and archived items with distinct markers, and editing preserves IDs and links. This planning workspace contains no runtime source and has no selected language. These are documented requirements, not independently verified runtime behavior.

## Success criteria

- Selecting one existing active ID marks exactly that item archived.
- Its ID, title, body, links, and list visibility remain unchanged.
- Every other item remains unchanged.
- Repeating archival leaves the collection in the same state and performs no additional save.
- A missing ID produces a failure without changing any item.
- Invalid argument counts fail before mutation.
- A failed save is reported as a failure; success is reported only after the update is committed.

## Command contract

The proposed subcommand is `archive <id>`, where `<id>` is exactly one stable item ID. The executable name and ID syntax must follow the eventual note tool's conventions; neither is established by this workspace.

| Input or condition | State change | Outcome |
| --- | --- | --- |
| One existing active ID | Set that item's archived flag to true | Success after persistence succeeds |
| One existing archived ID | None; no save | Success identifying the already archived state |
| One missing ID | None | Missing-item failure |
| Missing or extra arguments | None | Usage failure before mutation |
| Persistence fails | No partial update | Persistence failure; never report success |

Use the eventual tool's established output and exit-status conventions. Success must be distinguishable from failure, and output must identify the requested ID. This design does not invent numeric error codes or exact message text in the absence of a runtime convention.

## State transition and responsibilities

The command validates argument count and delegates a single ID to a dedicated archive operation. That operation looks up the item using its existing identity rules. A missing item ends the operation without a write. An already archived item ends successfully without a write.

For an active item, prepare an update that changes only the archived flag. Preserve the original item until persistence succeeds; avoid changing a shared in-memory item before a save that might fail. Commit one update through the collection's persistence boundary, then report success. The implementation must establish a failure-safe update mechanism for its selected storage before shipping this path.

Reuse lower-level lookup and persistence facilities where available. Archival does not invoke broad editing behavior, replace identities, relocate items, or rewrite links. No new data field or data-format migration is required by the design.

Ordinary listing retains its existing inclusion and marker behavior. The command must not introduce a default filter that suppresses archived items. Existing editing and link resolution retain their current contracts.

## Assumptions and implementation prerequisites

- Stable IDs uniquely identify items. Verify this in the runtime's lookup behavior before implementing the command.
- The selected update mechanism can change the archived flag while preserving all unrelated fields, references, and other items. Validate this with before/after state comparisons.
- The persistence boundary can prevent partial changes on failure, including changes to a live in-memory collection. Establish and test that guarantee before declaring the command complete.
- A runtime, language, source layout, and test harness will be available to implement against. None exists in this planning workspace, so actual module paths remain unresolved.
- The README's listing and link-preservation behavior will be present in that runtime. Verify integration through its real listing and link-resolution interfaces.

## Not Doing

- Deletion: retired notes must remain available.
- Hiding: archived notes must remain in the ordinary list.
- Moving notes: changing their location adds unnecessary preservation and link risks.
- Bulk operations: this increment selects exactly one ID.
- Restore: reversing archival is a separate capability.
- Synchronization: the operation concerns the local collection only.
- Network access: the command must work offline.
- New dependencies: the increment uses the eventual runtime's existing facilities.

## Rejected Alternatives

| Alternative | Rationale |
| --- | --- |
| Route archival through the general editing operation | Same user-visible result, but unnecessary coupling to broader editing behavior. Shared lower-level persistence remains appropriate. |
| Hide archived notes | Violates ordinary-list visibility. |
| Move archived notes | Unnecessary for a flag update and conflicts with the selected preservation contract. |

The dedicated flag update provides the requested value with the narrowest operation. Both the dedicated and editing approaches could support the same visible result; simplicity determines the choice.

## Verification

Use a collection containing multiple items and at least one link to the selected item. Snapshot the logical collection before each operation and compare it afterward. Verify the persisted representation as well as the live collection when the runtime exposes both.

Cover active-to-archived success, repeated archival, an item that starts archived, a missing ID, missing and extra arguments, and an injected persistence failure. Assert that only the selected archived flag changes on success and that no state changes on the other paths. Observe the persistence boundary to prove no save occurs for already archived, missing-ID, or invalid-input paths.

After successful archival, list through the ordinary interface and resolve the existing link. The item must remain visible with its archived marker, and its link must resolve to the same stable ID and content. Run existing editing checks to catch regressions in identity or link preservation.

Planning validation checks document consistency and local links only. Runtime tests and independent reviews have not been performed.
