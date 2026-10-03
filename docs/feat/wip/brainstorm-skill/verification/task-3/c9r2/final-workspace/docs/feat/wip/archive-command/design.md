# Design: Archive command

> Status: approved design; implementation pending
> Source: [README.md](../../../../README.md)
> Implementation: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Problem and intended outcome

The collection owner needs to retire an individual note while preserving access to it. Add an archive command that changes the existing archived flag without deleting, relocating, or hiding the note.

Success means that a selected note becomes archived, its ID, title, body, and links remain intact, and ordinary listing still includes it with the existing archived marker. Repeating the operation leaves the same state. An unknown ID is reported without changing any note.

## Current state and evidence

The README describes notes with stable IDs, titles, bodies, and an archived flag. Ordinary listing already includes active and archived notes and marks them distinctly. Editing preserves IDs and links.

This planning workspace contains only that description: there is no runtime source, selected implementation language, storage backend, or test framework. The mechanisms below are requirements for the eventual implementation, not claims about existing code. Source-file mapping must be established against the actual note tool before implementation begins.

## Command contract

The proposed subcommand syntax is `archive <id>`. The executable name and concrete argument parser remain unspecified.

| Input or condition | Result | State change |
| --- | --- | --- |
| One existing active note ID | Success identifying the archived note | Its archived flag becomes true |
| One existing archived note ID | Success identifying the already archived note | None |
| Unknown ID | Clear not-found error and nonzero exit status | None |
| Missing ID, extra arguments, or an ID rejected by the tool's established ID grammar | Usage error and nonzero exit status | None |
| Storage failure | Clear failure and nonzero exit status; no success message | Collection must remain intact |

The command accepts exactly one ID. Follow the eventual tool's established ID grammar and output conventions; do not invent a new ID format. Success output should identify the note by ID without printing its body. Exact message text and numeric failure codes should follow the existing CLI conventions when source is available.

## State transition and persistence

Resolve the ID using the tool's existing note lookup. If the note is absent, stop before mutation. If its archived flag is already true, return success without further changes or an unnecessary write.

For an active note, prepare an update that changes only the archived flag. Save it through the tool's storage boundary and report success only after that boundary confirms persistence. A failed save must not leave the collection damaged or partially rewritten. The implementation must establish how its backend provides this guarantee before using it.

The note remains in its original collection and retains the same ID, title, body, and links. Ordinary listing retains its existing inclusion rules and archived marker. Editing must continue to address the note through its unchanged ID and preserve the archived state unless an existing, explicitly documented editing behavior says otherwise; any conflicting behavior must be resolved before shipping this command.

No additional archive table, copy, directory, or metadata record is introduced.

## Acceptance criteria

1. Archiving an active note changes only that note's archived flag, including after reopening the collection.
2. Archiving the same note again succeeds and leaves the persisted collection unchanged.
3. An unknown ID produces a not-found error and changes no item.
4. Missing or invalid arguments produce a usage error without writing the collection.
5. A storage failure produces an error without a success message or damaged collection.
6. Ordinary listing still includes the archived note and marks it distinctly.
7. The selected note's ID, title, body, and links remain unchanged; other notes remain unchanged.
8. The tool's existing editing path continues to preserve IDs and links after archival.

## Assumptions

- Stable IDs uniquely identify notes. Validate this against the eventual lookup and storage model before wiring the command.
- The storage layer can persist a flag change without altering unrelated data and can preserve the collection on failure. Verify this through storage inspection and fault-injection tests.
- Existing listing and editing behavior matches the README. Verify it against the target implementation and regression tests rather than treating the description as runtime evidence.

## Not Doing

- Bulk archival: this increment selects exactly one note.
- Restore: changing an archived note back to active is a separate capability.
- Synchronization: the described collection is local and this command does not introduce synchronization.
- New dependencies or network access: the operation uses the tool's existing local facilities.
- Building a complete note tool: this plan describes an addition to the tool whose runtime must be supplied separately.

## Rejected Alternatives

| Alternative | Assessment | Reason rejected |
| --- | --- | --- |
| Hide archived notes from ordinary listing | Reduces visible clutter but removes ordinary access | Conflicts with the required listing behavior |
| Move notes to a separate archive | Separates archived content but changes its location and may require link handling | Conflicts with preserving the current access path and links |
| Store a separate archive record | Adds independent archival metadata but requires another consistency boundary | The existing flag already expresses the required state |

Updating the existing flag delivers the owner's requested behavior with the smallest change to the described data model.

## Verification boundary

This document records an approved design. No runtime implementation, tests, or independent review have been performed in this planning workspace.
