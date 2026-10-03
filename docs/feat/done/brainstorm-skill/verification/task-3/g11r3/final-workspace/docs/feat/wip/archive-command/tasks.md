# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving, bulk operations, restore, synchronization, new dependencies, network access, generic item-update framework

This is a planning artifact. No implementation or follow-up review is authorized by its creation. `COMMAND_SOURCE`, `STORE_SOURCE`, `COMMAND_TESTS`, `COLLECTION_TESTS`, and `USER_DOCS` are proposed responsibility labels defined in the [target map](implementation.md#target-map), not existing files. Task 1 must resolve them before implementation begins.

## Task 1: Archive one selected active item while preserving access

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Establish targets and archive one active item](implementation.md#1-establish-targets-and-archive-one-active-item)

### Subtasks

- [ ] 1.1 Resolve the authorized runtime, language, command entry point, storage boundary, and test harness; replace the implementation plan's target-map labels with concrete paths. Verify that the paths and test entry points exist or are explicitly authorized new files. Do not create a runtime merely to fill this planning gap.
- [ ] 1.2 Inspect ID uniqueness and persistence guarantees in the runtime's model and `STORE_SOURCE`. Record evidence for the corresponding design assumptions before implementing selection and save behavior.
- [ ] 1.3 Add command-to-storage tests in `COMMAND_TESTS` for A1/A4/A5: an active ID changes only its flag, a missing ID reports failure without saving, and missing/multiple arguments fail before mutation. Verify that the active path fails before implementation for the expected missing behavior.
- [ ] 1.4 Register the command and implement the proposed `archiveById` active-item path in `COMMAND_SOURCE`, using the existing lookup and save boundary in `STORE_SOURCE`. Verify A1/A4/A5, including the reopened durable collection and unchanged unrelated items.
- [ ] 1.5 Add A2/A7 checks in `COLLECTION_TESTS` for ordinary-list visibility, archived marking, working incoming/outgoing links, and continued editing with stable IDs. Verify the complete archive-and-access path without adding filters or moving notes.

## Task 2: Make repeat requests successful without another write

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Make repeated archival a successful no-op](implementation.md#2-make-repeated-archival-a-successful-no-op)

### Subtasks

- [ ] 2.1 Extend `COMMAND_TESTS` with A3 for an initially archived item and a second invocation after a successful archive. Verify that the assertions detect another persistence call or any further state change.
- [ ] 2.2 Add the already-archived early return to `archiveById` in `COMMAND_SOURCE`, producing a successful no-op outcome. Verify one save for the initial transition and zero saves for subsequent requests, with collection snapshots unchanged on repetition.
- [ ] 2.3 Run the focused active, missing-ID, and invalid-invocation checks alongside A3. Verify that the early return does not change those outcomes.

## Task 3: Report failed persistence without false success

- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Report persistence failures accurately](implementation.md#3-report-persistence-failures-accurately)

### Subtasks

- [ ] 3.1 Add deterministic A6 failure coverage in `COMMAND_TESTS`, using `STORE_SOURCE`'s existing failure seam or a narrowly scoped seam if needed. Verify that the failure occurs before commit without new dependencies or network access.
- [ ] 3.2 Ensure `COMMAND_SOURCE` reports the persistence error and emits no successful-archive result. Verify unchanged durable state and consistent subsequent listing after the failed operation.
- [ ] 3.3 Validate and document `STORE_SOURCE`'s actual partial-write/interruption behavior. Use its established safe update path and resolve any preservation gap before completion; verify the stated guarantee against relevant storage checks.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification and documentation](implementation.md#4-final-verification-and-documentation)

### Subtasks

- [ ] 4.1 Invoke `$kk:test` after implementation for the full host-project test suite and A1–A8. Verify preserved data and access, retries, errors, editing, and offline operation.
- [ ] 4.2 Invoke `$kk:document` to update `USER_DOCS` with the implemented command and outcomes. Verify alignment with the actual interface and exclusions.
- [ ] 4.3 Invoke `$kk:review-code` with the implementation's actual language. Resolve or record actionable findings before marking the task complete.
- [ ] 4.4 Invoke `$kk:review-spec` against design.md and implementation.md. Verify every acceptance scenario and scope boundary has matching implementation evidence.

## Dependency Graph

```text
Task 1 --> Task 2 --> Task 3 --> Task 4
   |          |                   ^
   |          +-------------------|
   +------------------------------+
```

Tasks are sequential because they extend the same command and its tests. This dependency graph is the planning baseline and is not rewritten during implementation.
