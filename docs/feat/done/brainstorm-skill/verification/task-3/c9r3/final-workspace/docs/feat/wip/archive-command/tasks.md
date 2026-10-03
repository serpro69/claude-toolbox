# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: blocked — runtime source and language are unavailable
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, network access, new dependencies

The approved design is ready for planning. Coding begins only after the runtime and test harness are identified and the implementation plan's component map names real paths. Component names below identify responsibilities, not files claimed to exist. Size estimates must be revisited once paths are known; split any task that would become L into smaller complete user paths.

## Task 1: Archive one active note end to end

- **Status:** blocked
- **Blocked:** No runtime source, selected language, or test harness exists in this planning workspace.
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#step-1-archive-one-active-item-end-to-end](implementation.md#step-1-archive-one-active-item-end-to-end)

### Subtasks

- [ ] 1.1 Resolve the implementation plan's component map to the actual command dispatch, archive operation, collection persistence, and test paths before editing code. Verify the runtime's ID, listing, and link contracts against the README.
- [ ] 1.2 Register the archive handler and implement the dedicated single-ID flag update through the collection persistence boundary. Verify an active item can be archived through the real command interface and reloaded with its archived flag set.
- [ ] 1.3 Add command-path coverage with several items and an existing link. Verify the selected flag is the only changed data, other items are identical, ordinary listing retains the item with its archived marker, and the link resolves to the same content and ID.
- [ ] 1.4 Verify success is emitted only after the persistence boundary confirms the update, using the test harness's observable output and save result.

## Task 2: Handle repeat and invalid selections without writes

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#step-2-make-repeat-and-invalid-selections-safe](implementation.md#step-2-make-repeat-and-invalid-selections-safe)

### Subtasks

- [ ] 2.1 Add the archive operation's already-archived success path. Verify both a repeated command and an initially archived item preserve the entire state and perform no additional save.
- [ ] 2.2 Add the lookup failure result and command error mapping for a missing ID. Verify a populated collection remains identical and the persistence boundary is never called to save.
- [ ] 2.3 Add archive-handler argument-count checks for missing and extra arguments. Verify both fail before mutation and perform zero saves; retain established ID validation conventions.
- [ ] 2.4 Verify successful, already-archived, missing-ID, and usage outcomes remain distinguishable through the runtime's existing output and exit conventions.

## Task 3: Fail archival without leaving partial state

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#step-3-preserve-state-when-persistence-fails](implementation.md#step-3-preserve-state-when-persistence-fails)

### Subtasks

- [ ] 3.1 Establish the collection persistence boundary's failure contract and prepare the archive update without changing the shared original item before commit. Verify the selected mechanism prevents partial changes.
- [ ] 3.2 Inject a persistence failure through the command path. Verify failure output, no success output, and unchanged live and persisted state for every item, including the selected archived flag.
- [ ] 3.3 Verify ordinary listing and link resolution still work after the failed attempt. Remove the injected failure, retry successfully, then repeat again and verify no additional save.
- [ ] 3.4 If the failure contract requires a broader storage redesign, record the concrete blocker and revise the plan before extending implementation scope.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#step-4-complete-documentation-and-verification](implementation.md#step-4-complete-documentation-and-verification)

### Subtasks

- [ ] 4.1 Run `/kk:test` for the full runtime suite, including archive outcomes, failure injection, ordinary listing, links, and existing editing behavior. Record actual commands and results.
- [ ] 4.2 Run `/kk:document` to update `README.md` and relevant command help with the real invocation, one-ID behavior, repeat and error outcomes, and preservation guarantees. Verify examples against the implemented command.
- [ ] 4.3 Run `/kk:review-code` with the selected project's actual language and address applicable findings.
- [ ] 4.4 Run `/kk:review-spec` against `design.md`, `implementation.md`, and `tasks.md`; resolve discrepancies and update completion state only when evidence supports it.

These unchecked tasks describe future work. No implementation or follow-up review is part of the current document-writing request.

## Dependency Graph

```text
Runtime source and test harness available
                  |
                  v
               Task 1 ---> Task 2 ---> Task 3 ---> Task 4
                  |                      ^          ^
                  +----------------------+          |
                  +---------------------------------+
                             Task 2 ----------------+
```

Tasks 2 and 3 are sequenced because they touch the same narrow operation and command tests. Task 4 depends on all implementation tasks.
