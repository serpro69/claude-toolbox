# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: bulk archival, restore, synchronization, deletion, hiding archived notes, note relocation, ID/link rewriting, new dependencies, network operations, language/runtime scaffolding
> Implementation prerequisite: supply the actual application checkout and bind the component roles below to real file paths and focused test commands. This workspace contains no runtime source or selected language.

## Task 1: Archive one active note while preserving access

- **Status:** blocked
- **Blocked:** Actual application source is not available in this planning workspace. Resolve the implementation prerequisite before coding.
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [source binding](implementation.md#before-implementation-bind-to-the-destination-application), [active-note path](implementation.md#slice-1-archive-one-active-note)

### Subtasks

- [ ] 1.1 Inspect the destination application's command entry point, note lookup/mutation, persistence, listing, link resolver, and tests. Record actual paths and focused verification commands in implementation.md and these subtasks before editing runtime files. Verify that existing mutation preserves every field outside archived.
- [ ] 1.2 Add a failing end-to-end test in the bound command/integration test files for archiving an active note, including unrelated-note and link fixtures. Verify the failure reflects the missing behavior.
- [ ] 1.3 Wire one-ID argument handling in the bound command entry point to the proposed `ArchiveNote(id)` operation or its project-conventional equivalent. Validate input and resolve the ID before writing; a miss must never mutate. Verify valid routing and rejection of missing/malformed arguments.
- [ ] 1.4 Implement the active-to-archived transition in the bound note mutation component using existing local persistence. Verify reloading changes only archived, preserves all unrelated notes, and reports success only after persistence completes.
- [ ] 1.5 Add a storage-failure case in the bound command tests. Verify an unsuccessful result and absence of a success message.
- [ ] 1.6 Exercise normal listing and incoming/outgoing link resolution in the bound integration tests. Verify archived visibility with the existing marker and unchanged stable-ID targets.

## Task 2: Make retries and missing IDs predictable

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [retry and absent-ID path](implementation.md#slice-2-retries-and-absent-ids)

### Subtasks

- [ ] 2.1 Add a repeat-invocation case in the bound command/domain test file. Verify two successful results, equal stored state after both calls, and no persistence call on the second invocation.
- [ ] 2.2 Complete the already-archived branch in the bound archive operation. Verify it returns success without invoking persistence.
- [ ] 2.3 Add an unknown-ID case and complete missing-ID presentation in the bound archive operation/command adapter. Verify a clear unsuccessful result, no write invocation, and an unchanged full collection snapshot.
- [ ] 2.4 Add zero-ID and multiple-ID command cases using existing validation conventions. Verify neither mutates any item and multiple IDs do not activate bulk behavior.

## Task 3: Final implementation verification and documentation

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [verification plan](implementation.md#final-verification), [acceptance criteria](design.md#acceptance-criteria)

### Subtasks

- [ ] 3.1 Run `/kk:test` on the destination application: its full existing suite plus successful archival, preserved fields/links/listing, retries, missing IDs, invalid arguments, and persistence failure. Record exact commands and outcomes here.
- [ ] 3.2 Run `/kk:document` to update relevant destination command documentation. Verify examples and error behavior agree with design.md.
- [ ] 3.3 Run `/kk:review-code` with the actual implementation language and scope. Resolve findings or record decisions explicitly.
- [ ] 3.4 Run `/kk:review-spec` against the implementation and these documents. Verify acceptance coverage and synchronize any approved deviations.

These tasks describe future implementation work. None has been executed by the design-documentation request; follow-up reviews are not run during this request. Size estimates describe the expected bounded changes, excluding mechanical fixtures and registration. Reassess after source binding and split any task that would become L into smaller complete behavior paths.

## Dependency Graph

```text
Application checkout and source binding
                  |
                  v
                Task 1 -------> Task 3
                  |               ^
                  v               |
                Task 2 -----------+
```
