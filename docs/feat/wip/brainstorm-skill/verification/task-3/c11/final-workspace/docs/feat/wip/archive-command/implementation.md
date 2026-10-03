# Archive command implementation plan

Status: planned; runtime implementation is outside this documentation task.

References: [design](design.md), [task list](tasks.md), and [source requirements](../../../../README.md).

## Before implementation: bind to the destination application

Only README.md exists as application context in this workspace. Do not assume a language, repository layout, storage engine, command framework, or test runner. Obtain the actual application checkout before implementing Task 1, inspect its conventions, and replace the role names below with real file paths in this plan and the task list.

| File/component role | Work to bind to actual source |
| --- | --- |
| Command entry point and argument parser | Register the one-ID archive command using established invocation and result conventions |
| Note lookup and mutation component | Add the logical `ArchiveNote(id)` operation, or the equivalent naming/style already used by the application |
| Note persistence component | Reuse a field-preserving local write; add a narrow operation only if existing mutation APIs cannot express it safely |
| Ordinary list and link resolver | Exercise their existing behavior through integration tests; change them only if necessary to satisfy the documented contract |
| Command/domain tests | Cover successful archival, repeated calls, missing IDs, and invalid arguments |
| Collection integration tests | Cover reloading, unchanged fields and unrelated notes, link resolution, and list visibility |

The logical operation name is proposed, not an existing symbol. Keep implementation within the existing module boundaries rather than creating a module for every role. Confirm whether a stable-ID mutation can race with other writers; use the existing storage contract rather than introducing a separate concurrency system. If that contract cannot preserve the design's invariants, revise the affected plan before coding.

Binding step → verify: every role has an actual file path or a justified existing equivalent, focused test commands are recorded, and the selected storage operation preserves all fields outside archived. No dependency addition or runtime bootstrap is part of this plan.

## Slice 1: archive one active note

This slice delivers a complete command path from one valid ID to a persisted archived note.

1. In the bound command test file, add an active-note scenario with another unrelated note and links to/from the selected note → verify: the test fails because archival is not available, rather than because the fixture or invocation is invalid.
2. In the bound command entry point, accept exactly one existing-format ID and route it to the archive operation → verify: a valid invocation reaches the operation with that ID; malformed or absent input follows existing validation without mutation.
3. In the bound lookup/mutation component, resolve the note before writing and set only archived to true through existing persistence. Preserve all other fields; never move, hide, delete, or recreate the note → verify: reloading shows the flag change while the selected note's other fields and the entire unrelated-note snapshot remain equal.
4. In the bound integration test files, call normal listing and link resolution after archival → verify: the selected note remains in the ordinary list with its existing archived marker and both link directions still resolve to the same IDs.
5. Report the selected ID and archived state only after persistence succeeds → verify: command output reflects the completed state, and a simulated storage error produces an unsuccessful result without a success message.

A lookup miss must never fall through to a write even in this first slice. Slice 2 makes the retry and missing-ID contracts explicit and regression-tested.

## Slice 2: retries and absent IDs

This slice completes the command's deterministic edge behavior through the same entry point.

1. In the bound command/domain tests, call archive twice on the same note → verify: both calls succeed, all stored state after the second matches the first, and the second call does not invoke persistence.
2. In the archive operation, return success immediately for an already archived note → verify: the retry scenario passes without duplicate side effects.
3. In the bound command tests, supply an unknown but syntactically valid ID → verify: the command identifies the missing ID, fails through established conventions, invokes no mutation, and leaves the full collection snapshot unchanged.
4. Complete the not-found branch and test existing argument validation for zero or multiple IDs → verify: each invalid invocation fails before mutation; accepting multiple IDs must not become bulk archival.

Use meaningful observable assertions plus a persistence spy where needed to distinguish no-op success from an unnecessary rewrite. Avoid tests that only restate helper implementation details.

## Final verification

1. Run `/kk:test` against the completed destination implementation, including its established full suite and the acceptance cases in [design.md](design.md#acceptance-criteria) → verify: all command and collection behavior passes, with exact commands and outcomes recorded in tasks.md.
2. Run `/kk:document` to update the destination application's relevant command documentation → verify: usage describes one-ID archival, repeated-call success, missing-ID errors, preserved content/links, and ordinary-list visibility.
3. Run `/kk:review-code` with the actual project language and implementation scope → verify: review findings are resolved or explicitly recorded for a decision.
4. Run `/kk:review-spec` against these three planning documents and the implementation → verify: every acceptance criterion is accounted for and any approved deviations are reflected consistently.

These are future implementation checks. The current request authorizes writing these planning documents only and explicitly excludes implementing the command or executing follow-up review.

## Assumptions

The destination lookup, persistence, listing, links, and error conventions must satisfy the testable assumptions in [design.md](design.md#assumptions). Resolve them during source binding and targeted integration tests. No runtime API, filename, or test command has been verified in this workspace.

## Not Doing

Bulk archival, restore, synchronization, deletion, hiding archived notes, note relocation, ID/link rewriting, new dependencies, network operations, and language/runtime scaffolding are excluded for the reasons in [design.md](design.md#not-doing).

## Rejected Alternatives

A generic edit-command route lacks a verified integration contract; hiding violates visibility; moving notes adds unnecessary identity and link risks. See the complete rationale in [design.md](design.md#rejected-alternatives). Reusing existing persistence beneath the dedicated archive operation remains appropriate.
