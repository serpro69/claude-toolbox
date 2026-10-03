# Archive command design

Status: designed; implementation not started.

Source: [README.md](../../../../README.md). Related: [implementation plan](implementation.md) and [tasks](tasks.md).

## Problem and outcome

The owner of a local note collection needs to retire one note while retaining access to it. Archival changes the note's existing archived flag; it preserves the note's content, identity, links, and visibility in the ordinary list.

Success means every acceptance case below passes: one selected note becomes archived, repeated calls preserve that state, and an unknown ID produces an error without changing any item.

## Current state and evidence

The README describes notes with a stable ID, title, body, and archived flag. The ordinary list includes active and archived notes and distinguishes their states. Editing already preserves IDs and links.

These are requirements supplied by the README, not behavior verified against running code. This planning workspace contains no runtime source or selected programming language. No concrete command entry point, persistence API, or test runner can be identified here. Before implementation, bind the responsibilities in the implementation plan to the actual application files and existing conventions.

## Command contract

`archive <id>` is conceptual command notation; use the host application's actual invocation and ID conventions when binding the implementation.

| Input/state | Outcome | Allowed changes |
| --- | --- | --- |
| Existing active note | Success; the selected note is archived | Only that note's archived flag changes to true |
| Existing archived note | Success; the note remains archived | None |
| Unknown ID | Clear missing-ID error; unsuccessful command result | None, across the entire collection |
| Missing or malformed argument | Existing command-validation error convention | None |

Success output identifies the selected note by its stable ID and confirms its archived state. An already archived note may be described as unchanged. No interactive confirmation is needed for this command. Use the application's established success/error channel and status conventions; do not invent numeric status codes before inspecting the host application.

## State transition and integration

1. Validate that the invocation identifies exactly one note using existing ID rules.
2. Resolve that ID through the collection's existing lookup mechanism.
3. If no note exists, return the missing-ID error before invoking any mutation.
4. If the note is already archived, return success without a persistence write.
5. Otherwise, use the existing persistence mechanism to change only its archived flag to true.
6. Report success only after persistence succeeds. Report persistence failures through existing error handling.

The command adapter owns argument parsing and result presentation. The archive operation owns lookup and the single-note state transition. Existing storage owns persistence; the archive command adds no storage system or new dependency. These are logical responsibilities and need not become separate modules if the host application's structure is simpler.

Do not reconstruct or replace a note from only its displayed fields: preserve all other stored fields as well as its title, body, ID, and links. Reuse existing mutation conventions that retain them. Leave the list's inclusion rules intact and use its existing archived-state representation. No file relocation, ID rewriting, link rewriting, or deletion participates in archival.

## Acceptance criteria

| Case | Verification |
| --- | --- |
| Archive an active note | Reload it through normal collection access; archived is true |
| Preserve note data | Compare the note before and after; every field other than archived is equal |
| Preserve unrelated notes | Compare the rest of the collection before and after; all notes are equal |
| Preserve links | Existing incoming and outgoing links still resolve to the same IDs after archival |
| Preserve visibility | The ordinary list includes the archived note using its existing archived marker |
| Repeat archival | Both calls succeed; the second changes no stored state and performs no write |
| Unknown ID | Command reports missing ID; the entire collection is unchanged and no write occurs |
| Invalid invocation | Existing argument-validation behavior rejects it before mutation |
| Persistence failure | Command reports failure and does not report successful archival |

Use the application's established storage guarantees for write failure and durability. The design does not claim a new transaction mechanism, concurrency model, or crash-recovery guarantee.

## Assumptions

- The destination application provides stable-ID lookup and a persistence operation that can retain all fields except the targeted flag. Validate by inspecting their contracts before coding; a mismatch requires revising this plan.
- The README's description of ordinary listing and link preservation matches the destination application. Validate with integration tests; discrepancies must be resolved before declaring archival complete.
- Existing error and argument conventions can represent success, missing IDs, invalid invocations, and persistence failures. Confirm concrete messages and status handling when binding to the application.
- The owner operates on an existing local collection. This increment does not introduce another writer or storage protocol.

## Not Doing

- Bulk archival: the requested operation selects exactly one note.
- Restore: reversing archival is outside this increment.
- Synchronization: this is a local collection operation.
- Deletion: archival must retain every note and its content.
- Hiding archived notes: ordinary-list access must remain available.
- Moving notes or rewriting IDs and links: the existing identity and access paths must remain stable.
- New dependencies or network access: the existing flag and local persistence are sufficient.
- Selecting a language or building an application scaffold: runtime source must be supplied before implementation; this request produces planning documents only.

## Rejected Alternatives

| Alternative | Trade-off and rejection rationale |
| --- | --- |
| Route archival through a generic edit command | Might reuse command-level editing, but introduces coupling to an unverified interface. Use a dedicated archive operation while reusing existing lower-level persistence conventions where appropriate. |
| Hide archived notes from ordinary listing | Would reduce visible active-note clutter, but violates the explicit visibility requirement. |
| Move notes into a separate archive location | Could group retired notes physically, but adds unnecessary identity and link-preservation work. The existing flag expresses the entire requested transition. |

The selected direct flag update has the highest fit with the owner's job and existing data model. It is a small local behavior change, with no new dependency or storage boundary.

## Implementation readiness

The user approved this design direction and presentation. The remaining prerequisite is locating the actual application checkout and recording its command, storage, listing, link-resolution, and test files. No runtime implementation or independent review has been performed as part of this planning work.
