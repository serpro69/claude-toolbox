# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, reusable archive service, runtime selection

All implementation work is pending. The workspace contains requirements only; source targets below are component responsibilities awaiting the [source mapping prerequisite](implementation.md#source-mapping-prerequisite). Record concrete source paths and test commands when the actual runtime project is available, before coding. Size estimates reflect the expected complexity of these responsibilities and should be rechecked after mapping.

## Task 1: Archive one active item and preserve access

- **Status:** pending
- **Depends on:** —; runtime source mapping is a prerequisite
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Active item path](implementation.md#archive-an-active-item), [acceptance criteria](design.md#acceptance-and-verification)

### Subtasks

- [ ] 1.1 Map command dispatch/handler, item lookup/persistence, listing/editing/link paths, and test locations to actual files → verify: paths and test commands exist and support the documented assumptions.
- [ ] 1.2 Add a command-level acceptance test with multiple items and links → verify: it initially fails for missing archive behavior with a valid fixture.
- [ ] 1.3 Add single-ID command routing and the direct flag update using existing lookup/persistence → verify: only the selected flag changes and a normal reload retains it.
- [ ] 1.4 Exercise ordinary listing, existing links, and editing after archival → verify: the item remains visibly archived in the list and its identity and link targets are preserved.
- [ ] 1.5 Check invalid invocation through command argument validation → verify: invalid ID argument counts change no data.

## Task 2: Handle repetition and missing IDs without writes

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Repeat and missing-ID outcomes](implementation.md#repeat-and-missing-id-outcomes)

### Subtasks

- [ ] 2.1 Add the already-archived branch and coverage in the archive handler's test location → verify: repeated invocation succeeds, preserves the complete collection snapshot, and makes no persistence call.
- [ ] 2.2 Add the missing-ID branch and coverage in the same command path → verify: a clear missing-ID error is reported, all items remain unchanged, and persistence is not called.

## Task 3: Report save failure accurately

- **Status:** pending
- **Depends on:** Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Save failure outcome](implementation.md#save-failure-outcome)

### Subtasks

- [ ] 3.1 Exercise a persistence failure in an archive command test using the runtime's supported failure mechanism → verify: the command reports failure and never reports successful archival.
- [ ] 3.2 Connect the persistence error to the command outcome while retaining existing failure semantics → verify: archive failure coverage and the storage layer's existing failure checks pass.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification and documentation](implementation.md#final-verification-and-documentation)

### Subtasks

- [ ] 4.1 Run `$kk:test` against the implementation project → verify: the full existing suite and every archive acceptance scenario pass.
- [ ] 4.2 Run `$kk:document` for command documentation → verify: actual syntax and all required outcomes are documented without implying deletion or hiding.
- [ ] 4.3 Run `$kk:review-code` with the project's chosen language and implementation diff → verify: findings are resolved or explicitly recorded.
- [ ] 4.4 Run `$kk:review-spec` against the implementation and these documents → verify: implementation matches the approved behavior and task state accurately reflects completion.

## Dependency Graph

```text
Runtime source mapping
          |
          v
       Task 1 ---> Task 2 ---> Task 3
          |          |           |
          +----------+-----------+
                     |
                     v
                   Task 4
```

The graph records planned dependencies. No implementation, tests, or follow-up reviews were run while authoring this task list.
