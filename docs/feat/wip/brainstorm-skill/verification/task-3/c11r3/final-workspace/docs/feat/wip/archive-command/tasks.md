# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: blocked — planning approved; runtime source and language needed for implementation
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access, generic update framework

The tasks below are future work; no implementation or review has run. Component targets must be replaced with actual file/function paths once runtime source is supplied. Size estimates are provisional until then; split any slice that becomes L before implementing it.

## Task 1: Archive one active item end-to-end

- **Status:** blocked
- **Blocked:** No runtime source or selected language exists in this planning workspace.
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [integration prerequisite](implementation.md#starting-point-and-integration-prerequisite), [active-item path](implementation.md#active-item-archive-path)

### Subtasks

- [ ] 1.1 Obtain runtime source and establish its language. Map command registration, item lookup/persistence, ordinary listing, link resolution, and test facilities to actual files/functions in `implementation.md` and this task list → verify: each path exists and source or focused existing tests support the mapped behavior.
- [ ] 1.2 Validate the four assumptions in `design.md` and the persistence/cache guarantees → verify: unique-ID lookup, stored archive flag, field-preserving writes, and continued ordinary-list inclusion are supported by the runtime. Resolve any mismatch before coding.
- [ ] 1.3 Register the single-ID archive command and add its dedicated operation in the existing item-operation component, including early missing/already-archived outcomes and success only after persistence → verify: command-level invocation changes exactly the selected active item's flag and no other field or item.
- [ ] 1.4 Add the active-item preservation test through the existing storage/listing/link test facilities → verify: reloading retains ID/title/body/links, ordinary listing includes the archived target with its existing marker, and links still resolve.

## Task 2: Verify and complete repeated-command behavior

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [repeated-command path](implementation.md#repeated-command-path)

### Subtasks

- [ ] 2.1 Complete the archive operation and command handler's already-archived outcome using the runtime's output conventions → verify: an initially archived item is reported as already in the requested state without a persistence write.
- [ ] 2.2 Add a command-level consecutive-invocation test → verify: complete collection snapshots after the first and second invocation match, with unchanged ordinary visibility and working links.

## Task 3: Verify and complete missing-item and write-failure behavior

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [failure paths](implementation.md#missing-item-and-persistence-failure-paths)

### Subtasks

- [ ] 3.1 Verify the archive lookup/handler's missing-item outcome and add its regression test → verify: a missing ID is reported, no persistence write occurs, and all items remain unchanged.
- [ ] 3.2 Complete the handler's persistence-error reporting and the operation's shared-state handling → verify: an injected write failure emits no success report and does not leave cached state falsely presenting successful archival.
- [ ] 3.3 Add storage-specific failure/recovery assertions using the actual persistence mechanism and document its guarantees in `implementation.md` → verify: tests demonstrate the established consistency guarantees without introducing a new storage subsystem or dependency.

Tasks 2 and 3 are sequenced because they may change the same archive operation, handler, and command tests; their logical independence does not justify concurrent edits to unresolved source files.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [verification matrix](implementation.md#verification-matrix), [final verification](implementation.md#final-verification-and-documentation)

### Subtasks

- [ ] 4.1 Run `/kk:test` against the verification matrix, relevant existing behavior tests, and the full local test suite → verify: all acceptance checks pass and record exact commands/results or unresolved environment limitations.
- [ ] 4.2 Run `/kk:document` to update the runtime project's archive command documentation → verify: usage, preserved visibility/links, repeated commands, and missing IDs match observed behavior.
- [ ] 4.3 Run `/kk:review-code` with the runtime's established language → verify: applicable findings are resolved or explicitly recorded with disposition.
- [ ] 4.4 Run `/kk:review-spec` against `design.md`, `implementation.md`, and `tasks.md` → verify: implementation satisfies the approved behavior and scope, with no unresolved spec deviations.
- [ ] 4.5 Update task and feature status only after all required checks complete → verify: completion claims have test/review evidence and no required work remains.

## Dependency Graph

```text
Runtime source + language
          |
          v
        Task 1 --> Task 2 --> Task 3
          |          |          |
          +----------+----------+
                     |
                     v
                   Task 4
```
