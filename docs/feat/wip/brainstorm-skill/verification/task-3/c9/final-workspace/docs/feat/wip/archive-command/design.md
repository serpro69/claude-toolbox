# Archive command design

Status: approved design; implementation pending.

Related documents: [implementation plan](implementation.md), [task list](tasks.md).

## Problem and current state

The collection owner needs to retire one note while retaining access to its content and references. The [project README](../../../../README.md) describes notes with a stable ID, title, body, and archived flag. Ordinary listing already includes both active and archived notes, marked distinctly. Existing editing preserves IDs and links.

This planning workspace contains no runtime source, selected programming language, command parser, persistence implementation, or test harness. Those mechanisms have not been inspected or verified. This design specifies the archive behavior and its integration responsibilities without claiming that particular source files or functions exist.

## User and success criteria

The user is the owner of a local note collection. Success is observable through these acceptance criteria:

1. Selecting an existing active ID marks exactly that item archived.
2. The note retains its ID, title, body, and links; every other item remains unchanged.
3. Ordinary listing still includes the note and uses its existing archived-state distinction.
4. References to the note continue to resolve using the same ID.
5. Repeating archival is a successful no-op that changes nothing further.
6. A missing ID reports failure without modifying any item.

## Command contract

The conceptual command is `archive <id>`: exactly one selected note ID, interpreted using the tool's existing identity rules. The executable name, argument-parser implementation, output wording, and numeric exit codes are integration details to align with the eventual runtime's conventions. They do not alter the following outcomes.

| Input or condition | Result | Persisted change |
| --- | --- | --- |
| Existing active ID | Success after the update is persisted | Only the selected note's archived flag becomes true |
| Existing archived ID | Successful no-op | None; no write is required |
| Unknown ID | Report the missing ID as a failure | None |
| Missing argument or more than one ID | Report a usage failure before mutation | None |
| Lookup or persistence failure | Report failure; do not announce success | Do not intentionally modify unrelated fields or notes |

Errors follow the tool's eventual command-error conventions. The command never creates a missing note, falls back to another ID, or applies an operation to multiple items.

## Chosen design

Use a dedicated archive operation that performs a direct update of the selected note's archived flag. A command handler validates the single-ID input and resolves the note through the tool's identity and storage boundary. If the ID does not exist, the handler reports failure before any update. If the note is already archived, it returns success without writing.

For an active note, preserve all existing fields and links while changing only the archived flag. Persist that update using the runtime's storage mechanism, then report success. The command must not reconstruct a partial note that drops unknown or unrelated fields. Storage failures must remain failures at the command boundary.

Keep listing and reference resolution behavior intact. Archive state is neither a filter for ordinary listing nor a change in identity. The command does not rename, relocate, remove, or rewrite the note's references.

## Assumptions

- **Required:** Stable IDs identify notes uniquely. Validate this against the selected runtime before implementing lookup; ambiguous identity must not cause updates to multiple notes.
- **Required:** The persistence boundary can update archive state while preserving all other fields and links. Verify this using complete before/after collection comparisons.
- **Required:** Ordinary listing and ID-based references behave as described in README.md. Establish these baseline behaviors in the eventual runtime and test them after archival.
- **Integration constraint:** No runtime language or source layout is selected in this workspace. Map the plan's logical components to concrete files during implementation; these documents do not authorize or provide a runtime scaffold.

## Not Doing

- **Deletion:** Retirement must retain the note's data.
- **Hiding:** Ordinary listing must continue to include archived notes.
- **Moving notes:** Archival must preserve location-dependent access and existing references.
- **Bulk operations:** This increment accepts exactly one ID.
- **Restore:** Reversing archive state is outside this increment.
- **Synchronization:** The operation is local and offline.
- **New dependencies:** The change requires no additional packages or services.
- **Network access:** No external lookup or remote mutation is needed.

## Rejected Alternatives

- **Route archival through the broader editing workflow:** This could reuse editing behavior, but couples a single-state command to unrelated editing rules. A dedicated operation has a narrower behavioral contract and can still reuse storage primitives.
- **Hide or move archived notes:** These approaches conflict with the required ordinary visibility and reference preservation.

## Verification and limitations

Use command-level tests with a temporary collection containing an active target, an already archived note, an unrelated active note, and a reference to the target. Compare complete collection state before and after each scenario, exercise ordinary listing, and resolve the preserved reference.

Test active archival, repeated archival, unknown IDs, missing and extra arguments, and injected lookup/persistence failures. Assert that successful no-ops and rejected inputs do not write. The implementation plan expands the expected observations.

No runtime behavior, storage guarantees, or tests have been verified by writing this design. Crash recovery and concurrent-writer semantics depend on the eventual storage implementation; this feature does not introduce a new storage protocol or claim guarantees beyond it. Implementation must document the actual failure behavior without reporting an unsuccessful write as success.
