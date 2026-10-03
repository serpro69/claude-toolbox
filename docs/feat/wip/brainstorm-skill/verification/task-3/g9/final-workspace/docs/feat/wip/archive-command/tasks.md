# Tasks: Archive command

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, new runtime development

The design is approved; implementation has not started. This planning workspace contains only a README, so runtime file paths, language, and executable test commands must be resolved against the actual note tool before implementation. Component names below are responsibilities, not claims that source files exist here.

## Task 1: Archive one note end-to-end

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [single-note archive path](./implementation.md#single-note-archive-path), [command contract](./design.md#command-contract)

### Subtasks

- [ ] 1.1 Map command dispatch, note lookup/update, listing, link resolution, tests, and help documentation to concrete runtime files and symbols; record the mapping and focused test commands in `implementation.md`. Verify the storage update preserves unrelated fields and prevents partial updates. If source remains unavailable, report that prerequisite rather than inventing file paths or building a runtime.
- [ ] 1.2 Add the command adapter and archive operation as one working path: accept exactly one stable ID, resolve it, update only the active target's archived flag, and report successful completion after persistence. Verify the reloaded collection differs only in the intended flag.
- [ ] 1.3 Handle already-archived, unknown-ID, and argument-count outcomes in the command and operation. Verify repeats succeed without a write, unknown IDs report an error without mutation, and invalid invocation never reaches mutation.
- [ ] 1.4 Integrate lookup and persistence error handling using the runtime's existing safeguards. Verify failures produce a failed command outcome without a success message, and simulated persistence failure leaves no partially applied operation.
- [ ] 1.5 Add command and integration tests covering the [verification matrix](./implementation.md#verification-scenarios), including full-record preservation, unaffected notes, ordinary list visibility, and working links after archival. Verify against isolated fixture storage.
- [ ] 1.6 Update the runtime's command help and usage documentation using the actual executable name. Verify examples and outcome descriptions against the implemented command; retain the approved exclusions.

This is one vertical slice through command input, state change, persistence, and observable behavior. Its size assumes a narrow change to an existing note tool. If mapping reveals that assumption is false, revise the plan before expanding scope; do not turn an L-sized change into a single task.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [final verification](./implementation.md#final-verification), [acceptance and validation](./design.md#acceptance-and-validation)

### Subtasks

- [ ] 2.1 Invoke `$kk:test` after implementation to run focused archive scenarios and the runtime's full test suite. Record actual commands and outcomes; confirm existing listing and editing checks pass.
- [ ] 2.2 Invoke `$kk:document` to verify relevant runtime documentation and reconcile these feature documents with the completed implementation.
- [ ] 2.3 Invoke `$kk:review-code` with the actual runtime language to review the implementation, and resolve findings.
- [ ] 2.4 Invoke `$kk:review-spec` to verify the implementation against `design.md` and `implementation.md`, including single-item mutation, idempotency, missing-ID handling, preserved visibility, and working links.
- [ ] 2.5 Mark tasks done only after their checks pass; record any unavailable checks or unresolved prerequisite accurately.

These checks belong to future implementation work. The current request authorizes writing the three planning documents only; it does not run implementation or a follow-up review.

## Dependency Graph

```text
Task 1: Archive one note end-to-end
  |
  v
Task 2: Final verification
```
