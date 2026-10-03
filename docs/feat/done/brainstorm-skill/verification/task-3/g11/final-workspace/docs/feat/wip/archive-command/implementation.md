# Archive command implementation plan

Status: approved plan; implementation pending.

Related: [design](design.md), [task list](tasks.md). Requirements: [README.md](../../../../README.md).

## Source mapping prerequisite

No runtime source, language, storage format, or test framework exists in this workspace. The following names identify responsibilities, not existing files. Before implementation, locate the actual application and record its concrete source paths in this plan and the task list.

| Responsibility | Intended work |
| --- | --- |
| Command dispatch and archive handler | Accept one ID, resolve it, branch on current state, save only when needed, and report the outcome |
| Existing item lookup and persistence | Reuse their contracts; preserve identity and unrelated data; expose save failure to the handler |
| Ordinary listing, editing, and link resolution | Exercise their existing behavior as integration checks; no semantic change is planned |
| Command and persistence test locations | Add behavior checks for archive success, repetition, missing IDs, and save failure |
| User-facing command documentation | Describe usage and outcomes using the application's eventual conventions |

Map these responsibilities to actual files and the existing test commands → verify: each mapped path exists in the implementation project, and its current behavior supports the assumptions in [design.md](design.md#assumptions). If no runtime exists, resolve runtime selection and bootstrap separately before starting these tasks. Do not introduce a language or framework merely to fill this table.

## Archive an active item

1. Add a behavior test using two or more items and existing links, invoking the command with one active ID → verify: the test fails because archival is unavailable, rather than because its fixture or invocation is invalid.
2. Wire a single-ID archive command into command dispatch, following existing argument and diagnostic conventions → verify: the selected existing ID reaches the handler; malformed invocation is rejected without mutation.
3. In the direct handler, resolve the item and update its archived flag; reuse persistence without replacing identity, moving the note, or changing other logical data → verify: a complete collection comparison shows exactly one flag change, and normal reload retains that state.
4. Exercise ordinary listing, link resolution, and editing against the archived item → verify: it remains listed with its archived marking, links retain their targets, and editing preserves its ID and links.

Keep the handler small. Do not introduce a general archive service, alternate item representation, or listing filter.

## Repeat and missing-ID outcomes

1. Add repeated-command coverage for an already archived item and return a successful no-op before invoking persistence → verify: a second archive invocation produces no data difference and makes zero persistence calls. Observe the write boundary using the eventual test framework; do not rely only on file timestamps.
2. Add missing-ID coverage and return a clear error before any mutation or persistence → verify: the complete collection snapshot is identical and no write is attempted.
3. Confirm one invocation cannot archive multiple items → verify: the selected-ID case changes only its target, and invalid argument counts are rejected by command validation.

## Save failure outcome

1. Exercise a save failure through the existing test framework's supported failure mechanism → verify: the command reports failure and emits no success outcome.
2. Preserve the storage layer's established failure and recovery behavior → verify: its existing failure checks continue to pass. Do not claim transactional rollback, crash safety, or concurrency guarantees unless the actual mechanism provides and verifies them.

## Final verification and documentation

1. Run `$kk:test` with the identified runtime and test setup → verify: all acceptance scenarios in the design and the existing suite pass, including list/edit/link preservation checks.
2. Run `$kk:document` to update command documentation → verify: examples use the actual invocation and explain one-item archival, successful repetition, preserved visibility, and missing-ID behavior.
3. Run `$kk:review-code` with the implementation language and actual diff → verify: actionable review findings are resolved or explicitly recorded.
4. Run `$kk:review-spec` against the implementation and these three planning documents → verify: behavior and task state agree with the approved scope.

These are future implementation tasks. The present request produces only the three planning documents and does not execute implementation, tests, or follow-up review.

## Assumptions

- Stable IDs identify one item, and storage can preserve all unrelated logical data. Validate lookup behavior, full snapshots, and reload before considering the core task complete.
- Ordinary listing, editing, and links already meet README.md's contract. Verify their existing paths during the archive acceptance test.
- An actual runtime project will be supplied or separately established before implementation. Validate the source mapping prerequisite rather than treating the responsibility table as a list of existing files.

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, and synchronization are excluded for the reasons in [the design](design.md#not-doing). New dependencies, a reusable archive service, and runtime selection are also outside this plan. These are scope exclusions, not deferred tasks within this increment.

## Rejected Alternatives

- Separate reusable archive operation: unnecessary abstraction for one caller.
- Hiding or moving notes: conflicts with the visibility and link-preservation requirements.
