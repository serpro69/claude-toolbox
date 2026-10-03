# Archive command implementation plan

Status: pending implementation. [Design](design.md) · [Tasks](tasks.md)

## Starting point

Only README.md provides the feature baseline. There is no runtime source, selected language, storage implementation, or runnable test harness in this workspace. Implementation must begin by resolving those concrete targets; this plan does not present proposed components as existing code.

Use a dedicated archive operation that directly updates one archived flag. Retain the host application's existing command conventions and storage capabilities, work offline, and add no dependencies.

## Target map

The names below identify responsibilities. They are placeholders to replace with actual repository file paths and language-appropriate symbols before source edits begin.

| Target | Responsibility and proposed symbol |
| --- | --- |
| `COMMAND_SOURCE` | Command registration, one-ID argument validation, result presentation, and proposed `archiveById` operation |
| `STORE_SOURCE` | Existing lookup and persistence boundary used by `archiveById`; extend only if necessary for the flag update |
| `COMMAND_TESTS` | Command-level tests exercising invocation through persisted state and reported outcome |
| `COLLECTION_TESTS` | Listing, incoming/outgoing link, and editing integration checks |
| `USER_DOCS` | The eventual host project's archive command reference; README.md is the current requirement source |

Each implementation slice should fit within one or two production components plus focused tests. If the eventual target map reveals broader work, split it into smaller complete behavior slices before starting; do not build separate model, persistence, and command layers in isolation.

## 1. Establish targets and archive one active item

1. Resolve the implementation language, authorized runtime location, command registration point, item lookup/persistence boundary, and test harness. Replace the target-map placeholders with actual file paths and record baseline listing, links, and editing behavior. If there is still no authorized runtime, stop implementation at that explicit prerequisite rather than inventing one. → verify: each target resolves to a real file or a clearly identified new file within the authorized implementation scope, and the available test harness can exercise a command against a disposable local collection.
2. Inspect ID uniqueness and the storage update/failure contract before choosing the mutation call. Determine whether the store saves an item or rewrites a collection and how unrelated fields remain intact. → verify: the design's ID and persistence assumptions have evidence in source or targeted storage checks; any unresolved failure behavior is recorded before coding the archive path.
3. In `COMMAND_TESTS`, cover A1, A2, A4, and A5 with a collection containing an active target, an archived item, an unrelated active item, and links in both directions. Assert full collection snapshots except for the permitted flag change. → verify: the active archive scenario fails because the command is absent, while fixtures demonstrate the baseline listing and link behavior.
4. In `COMMAND_SOURCE`, register the archive command, require exactly one ID, resolve it, reject a missing ID without saving, and implement the active-item path through `STORE_SOURCE`. Persist only the required state change and report success after the save succeeds. → verify: A1, A2, A4, and A5 pass through the command entry point, including durable state checks after reopening the collection.
5. Add A7 coverage in `COLLECTION_TESTS` to confirm that archival preserves the existing editing path. → verify: an archived item remains editable with the same ID and working links; no new listing filter or separate archive location is introduced.

## 2. Make repeated archival a successful no-op

1. Extend `COMMAND_TESTS` with A3 for an item initially archived and for two consecutive invocations against an initially active item. Observe calls at the existing persistence boundary without adding a mocking dependency. → verify: the tests detect an unnecessary second save or any secondary state change.
2. In `COMMAND_SOURCE`, return the successful already-archived outcome before mutation or persistence when the flag is already true. → verify: A3 passes, the first active-to-archived transition saves once, the repeat saves zero times, and A1/A4/A5 remain correct.

## 3. Report persistence failures accurately

1. Exercise the existing storage failure mechanism, or introduce a narrow test seam in `STORE_SOURCE` if the runtime requires one, to force a failure before commit. Avoid creating a general storage framework for this test. → verify: A6 reliably reaches the failure path without depending on network access or machine-specific filesystem permissions.
2. In `COMMAND_SOURCE`, propagate the failure to the command outcome and suppress successful-archive feedback. Avoid mutating shared in-memory item state before a failed save if that would leave subsequent commands with a false archived state. → verify: A6 observes no success output and unchanged durable state; subsequent listing agrees with persisted state.
3. Check the actual storage contract for interrupted or partial writes. Use its established safe update path, and document the resulting guarantee. If it cannot preserve item data for this operation, resolve that prerequisite before marking this slice complete. → verify: relevant storage failure checks support the documented guarantee; the plan does not substitute an untested rollback claim for evidence.

## 4. Final verification and documentation

1. Run the focused command and collection checks for A1–A8 and the host project's required regression checks through `$kk:test`. → verify: results cover selected-only mutation, preserved access, retries, invalid/missing IDs, persistence errors, editing, and offline operation.
2. Use `$kk:document` to update `USER_DOCS` with the actual invocation, result meanings, ordinary-list visibility, and stated exclusions. → verify: documented examples match the implemented interface and do not imply deletion, hiding, moving, bulk operations, restore, or synchronization.
3. Invoke `$kk:review-code` with the implementation's actual language and `$kk:review-spec` against this design and plan. → verify: the reviews complete and actionable findings are resolved or explicitly recorded before completion.

These are future implementation checks. The current request authorizes writing the three planning documents only and explicitly excludes implementation and follow-up review execution.

## Assumptions

- IDs identify one item uniquely. Verify at the model and lookup boundary before implementing selection.
- Storage can preserve all other item data while persisting the archived flag. Verify both successful writes and failure handling.
- Listing, links, and editing follow README.md's baseline. Establish executable integration checks when runtime source is available.

## Not Doing

- Deletion, hiding, and moving: conflict with preserved access and identity.
- Bulk operations: the command accepts one selected ID.
- Restore and synchronization: outside this increment.
- New dependencies and network access: the command must work offline with existing capabilities.
- A generic item-update framework: unnecessary for the chosen direct operation.

## Rejected Alternatives

- A new shared item-update operation for editing and archival: broader coordination without an improved archive outcome.
- Hiding archived items: violates ordinary-list visibility.
- Moving notes: explicitly rejected by the owner; retain their existing location and access paths.
