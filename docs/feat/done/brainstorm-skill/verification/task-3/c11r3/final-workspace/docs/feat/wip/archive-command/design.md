# Archive command design

> Status: approved design; implementation not started
> Requirements: [README.md](../../../../README.md)
> Implementation: [implementation.md](implementation.md)
> Tasks: [tasks.md](tasks.md)

## Problem and intended user

The owner of a local note collection needs to retire one note while preserving access to it. Archiving must preserve its stable identity, content, links, and visibility in the ordinary list.

The README describes items with a stable ID, title, body, and archived flag. The ordinary listing includes both active and archived items, marked distinctly. Existing editing preserves IDs and links. These are requirements supplied by the README, not behavior verified against runtime code: this planning workspace contains no runtime source or selected language.

## Goals and acceptance criteria

The command accepts one existing stable ID and establishes the archived state for exactly that item. Success is measured by these observable checks:

| Scenario | Required result |
| --- | --- |
| Existing active ID | Only that item's archived flag changes to true. |
| Preservation | Its ID, title, body, links, and ordinary-list presence remain unchanged. |
| Other items | Every other item remains unchanged. |
| Already archived ID | The command leaves the collection unchanged and reports that the requested state already holds. |
| Missing ID | The command reports the missing item without changing any item. |
| Persistence failure | The command reports failure and does not report successful archival. |

No latency or volume target is introduced for this increment. The acceptance criteria concern correctness and preservation of access.

## Command behavior

Use the existing command interface's conventions to accept exactly one item ID. The executable name, argument syntax, output wording, and exit-status conventions must be established from the runtime project before implementation. This document does not select a CLI framework.

The dedicated archive operation follows this order:

1. Resolve the supplied ID through the existing local item lookup mechanism.
2. If it is missing, return a missing-item outcome without creating or saving an item.
3. If it is already archived, return an already-archived outcome without a persistence write.
4. Otherwise, update only its archived flag to true through the existing persistence mechanism.
5. Report archival success only after persistence succeeds.

The operation assigns the desired flag value; it never toggles the flag. There is no move, copy, deletion, alternate archive collection, or new list filter. Ordinary listing retains its current behavior and displays the existing archived distinction. Existing links must continue resolving to the same item.

## Integration boundaries

The implementation has three logical integration points: the command adapter that accepts an ID and reports the outcome, the dedicated archive operation, and the existing item lookup/persistence path. These are responsibilities, not instructions to create three new files or an additional framework.

Reuse existing item types, ID matching, persistence, and output conventions. Do not build a generic item-update abstraction solely for this command. No schema change is expected because the README already includes an archived flag; verify this against the eventual runtime representation before coding.

The implementation plan begins by mapping those responsibilities to actual files and functions. Concrete runtime paths cannot be supplied truthfully until that source is available. This prerequisite blocks implementation, not completion of these planning documents.

## Persistence and failure handling

Missing and already-archived cases must return before any write. For an active item, use the project's established reliable persistence path and retain every field except the archive flag. Do not reconstruct a reduced item representation that could discard fields unknown to this command.

A failed write must not be presented as success. Inspect the actual storage mechanism to determine its commit and recovery behavior, including whether it mutates shared in-memory objects before a write completes. The command must not leave a cached item falsely presenting a successful archive after persistence failed.

Concurrency and crash-consistency guarantees are not established by the README. Identify and preserve the runtime project's existing guarantees rather than assuming that replacing an entire collection is safe. If the available persistence mechanism cannot preserve unrelated changes, resolve that integration issue before implementation continues.

## Assumptions

- Stable IDs uniquely identify one item. Validate this in the eventual item model and lookup behavior; ambiguity requires resolution before coding.
- The archived flag exists in the stored representation, not just in the README. Validate this against source and representative stored items.
- The existing write mechanism can retain identity, content, links, and unrelated fields while updating the flag. Validate this with persistence-level tests.
- The ordinary listing's archived distinction derives from this flag without hiding items. Validate this through the actual listing path.

## Not Doing

- Deletion, hiding, or moving notes: each would undermine preservation or ordinary access.
- Bulk operations: this command targets one selected ID.
- Restore: reversing archival is a separate increment.
- Synchronization: the requested operation is local and offline.
- New dependencies or network access: neither is needed for the approved behavior.
- A generic update framework: reuse does not justify widening this increment.

## Rejected Alternatives

| Alternative | Evaluation and rejection rationale |
| --- | --- |
| Shared general-purpose item-update operation | Delivers the same immediate user value, but requires a broader abstraction. Its potential reuse does not justify extra work in this increment. |
| Hide archived notes from the ordinary list | Violates the owner's required continued visibility. |
| Move notes to another location or collection | Adds relocation semantics and risks link continuity without advancing the approved requirement. |

The dedicated archive-flag update is preferred because it delivers the required behavior with the smallest integration scope and explicit handling of repeated and missing IDs.

## Verification and unresolved integration details

Use local fixtures with at least one target and one unrelated item. Compare complete stored items before and after execution, exercise ordinary listing, and resolve existing links. Cover active, already-archived, missing, and failed-persistence paths. The implementation plan specifies each check.

Before coding, supply the runtime project and establish its language, command registration, ID conventions, storage semantics, test entry points, and link-resolution behavior. No external research, dependencies, or network calls are required by this design. No implementation or independent review has been performed.
