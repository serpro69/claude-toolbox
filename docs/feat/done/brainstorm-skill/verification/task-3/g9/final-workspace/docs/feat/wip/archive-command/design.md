# Archive command design

> Status: approved design; implementation pending
> Source: [README.md](../../../../README.md)
> Plan: [implementation.md](./implementation.md)
> Tasks: [tasks.md](./tasks.md)

## Problem and intended outcome

The collection owner needs to retire one note while preserving access to it. Archival marks the selected note as archived without deleting, hiding, or relocating it. Success means exactly the selected item changes state; its content, identity, links, and ordinary list visibility remain intact. Repeating the action changes nothing further. An unknown ID produces an error without modifying the collection.

## Current state and evidence

The README establishes that each item has a stable ID, title, body, and archived flag. Ordinary listing already includes active and archived items and marks them distinctly. Existing editing preserves IDs and links.

This planning workspace contains only the README. It has no runtime source, selected language, command parser, storage implementation, or executable test suite. The components below describe implementation responsibilities, not verified files or APIs. No storage schema change or new dependency is needed by this design.

## Command contract

`archive <id>` denotes the proposed subcommand and its single argument; it is not a claim about an existing executable name. Treat the ID as the tool's existing stable identifier. Do not add fuzzy matching, title lookup, or multi-item selection.

| Input or state | Result | Mutation |
| --- | --- | --- |
| Exactly one ID resolving to an active note | Report successful archival | Set only that item's `archived` flag to `true` |
| Exactly one ID resolving to an archived note | Report successful completion, indicating it is already archived | None; skip persistence for this no-op |
| Exactly one ID resolving to no note | Report that the ID was not found | None |
| Missing ID or more than one ID argument | Report an invocation error | None; reject before mutation |
| Lookup or persistence fails | Report failure; do not claim successful archival | Lookup failure causes no mutation; persistence failure must not leave a partially applied operation |

Use the runtime's established output and exit-status conventions when available: successful archival and the already-archived result are successes; invocation, missing-ID, lookup, and persistence errors are failures. Literal message wording is not part of the feature contract. Report success only after a required update has completed.

## State and integration

The command adapter validates argument count and passes one ID to an archive operation. That operation resolves the note, handles missing and already-archived outcomes, and asks the existing persistence boundary to apply the single-field update. It must preserve all other logical data, including any additional fields present in the eventual runtime, and must not modify another note.

The implementation can reuse storage or editing helpers only if they satisfy this narrow mutation contract. It must not replace a note from a reduced projection that loses fields. No new timestamp, archive record, identifier, location, or link rewrite is introduced.

The existing ordinary listing and link resolution remain the access paths. An archived note is still listed with the existing archived marker, and existing links continue to resolve to the same note. The archive command requires no new list filter or archive-only view.

## Failure handling

Distinguish a missing ID from an operational lookup failure. Neither may reach the write path. Validate invocation before attempting an update. For a real state transition, use the persistence boundary's mechanism for preventing partial updates and surface any error to the caller. Do not add a generic retry loop or silently fall back to deletion, relocation, or another representation.

The exact persistence mechanism cannot be selected or verified from the README. Confirm it when source becomes available. Do not infer concurrency or crash-durability guarantees from this document; any conflict with the preservation contract must be resolved before implementation is accepted.

## Assumptions

- **Must be true:** stable IDs resolve individual notes unambiguously using the runtime's existing identifier rules. Verify this at the lookup boundary.
- **Must be true:** persistence can update the archived flag while preserving other fields, links, and items, and can avoid partially applied updates on failure. Inspect the concrete mechanism and verify failure behavior when source exists.
- **Must be true:** ordinary listing and link resolution already retain access to archived notes as stated in the README. Verify these behaviors through integration tests.
- **Should be true:** the future runtime has output, error, and test conventions that can be reused. Record the actual conventions in the implementation plan before coding; do not invent current file paths or APIs.

## Not Doing

- **Deletion:** retiring a note must preserve its content and identity.
- **Hiding:** ordinary listing must continue to include archived notes.
- **Moving notes:** changing their location adds unnecessary risk to access and links.
- **Bulk operations:** this increment selects exactly one ID.
- **Restore:** reversing archival is a separate capability.
- **Synchronization:** this is a local operation with no network access.
- **New dependencies:** the operation uses the existing item model and runtime facilities.

These are scope exclusions, not scheduled follow-up tasks.

## Rejected Alternatives

| Alternative | Potential benefit | Reason rejected |
| --- | --- | --- |
| Route the command through general editing | Might reuse command behavior | No runtime evidence establishes that general editing can change only the archived flag without additional effects. Dedicated archive semantics make the required guarantees explicit; compatible internal helpers can still be reused. |
| Hide archived notes from ordinary listing | Could shorten the visible list | Violates the required continued visibility. |
| Move notes into a separate archive location | Could physically separate retired notes | Adds unnecessary storage changes and risks existing links; the archived flag already represents the required state. |

The chosen direct flag update provides the requested user value with the smallest change to the documented model. Differentiation from other note tools is not a selection criterion for this maintenance feature.

## Acceptance and validation

Verification must cover the command boundary, persisted state, ordinary listing, and link access. Compare the entire logical collection before and after each operation, allowing only the selected active note's flag to change. An already-archived or missing-ID operation permits no differences.

The detailed scenario matrix is in [implementation.md](./implementation.md#verification-scenarios). These are planned checks, not tests run in this documentation-only workspace. No implementation or independent review has been performed.
