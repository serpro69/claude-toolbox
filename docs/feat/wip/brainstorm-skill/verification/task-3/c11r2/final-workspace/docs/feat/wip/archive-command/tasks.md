# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access, runtime or storage replacement

The design is approved. No runtime source, selected language, or test runner exists in this planning workspace. Task 1 cannot begin coding until the host source is available. Concrete file and symbol mappings must replace the logical targets below during that task; no implementation files are claimed to exist today.

## Task 1: Archive an active note and retain list and link access

- **Status:** blocked
- **Blocked:** Host runtime source and its integration paths are not available in this workspace.
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#slice-1-archive-an-active-item-and-retain-access](implementation.md#slice-1-archive-an-active-item-and-retain-access), [integration prerequisite](implementation.md#starting-point-and-integration-prerequisite)

### Subtasks

- [ ] 1.1 Record actual paths and symbols for command registration, the archive handler, ID lookup, persistence, listing, link resolution, command tests, and user documentation in `implementation.md` and this task. Verify the targets exist or identify proposed new handler/test paths following the host's conventions; record exact test commands.
- [ ] 1.2 Validate unique ID lookup and field-preserving item updates using the mapped host implementation and fixtures. Verify that no storage replacement, new dependency, or network access is required before marking this task unblocked.
- [ ] 1.3 Add a failing public-command acceptance case in the mapped command/integration test files for an active target, an unrelated note, an already archived note, and a link to the target. Verify that the initial failure concerns missing archive behavior.
- [ ] 1.4 Register the single-ID archive command in the mapped dispatcher and implement its mapped handler with direct flag update, safe missing/already archived branches, and host-standard outcomes. Verify that only the selected item's archived flag changes and all other fields and items are preserved.
- [ ] 1.5 Exercise the existing list and link components through integration tests. Verify that the target remains visibly marked archived in ordinary listing and the existing link still resolves to the same ID and content.
- [ ] 1.6 Test persistence failure using existing facilities. Verify that a failed update cannot emit the newly archived success outcome.

## Task 2: Make retry and missing-ID outcomes explicit and verifiable

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#slice-2-confirm-repeat-and-missing-id-outcomes](implementation.md#slice-2-confirm-repeat-and-missing-id-outcomes)

### Subtasks

- [ ] 2.1 Add focused coverage in the mapped command tests for an initially archived note; adjust the mapped archive handler if needed. Verify successful already archived output, identical before/after collection state, and no additional persistence update.
- [ ] 2.2 Archive an initially active note twice in an acceptance test. Verify newly archived then already archived outcomes, unchanged state after the second call, retained listing visibility, and working links.
- [ ] 2.3 Add the absent-ID command test with several existing notes. Verify missing-item output through the host error convention and unchanged collection state.
- [ ] 2.4 Assert distinguishable newly archived, already archived, and missing outcomes using the actual host output and status conventions. Verify all focused archive acceptance cases pass together.

## Task 3: Final verification and documentation

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#final-verification-and-documentation](implementation.md#final-verification-and-documentation), [design.md#scope-and-success-criteria](design.md#scope-and-success-criteria)

### Subtasks

- [ ] 3.1 Invoke `/kk:test` for the host's full suite and archive acceptance cases. Verify flag preservation, unrelated items, retry behavior, missing IDs, ordinary listing, links, and failure reporting.
- [ ] 3.2 Invoke `/kk:document` to update the mapped host command reference. Verify the documented syntax and outcomes match tested behavior, including preserved list visibility and access.
- [ ] 3.3 Invoke `/kk:review-code` with the actual project language. Resolve applicable findings and verify the final change uses existing dependencies and preserves the agreed scope.
- [ ] 3.4 Invoke `/kk:review-spec` against `design.md`, `implementation.md`, and `tasks.md`. Verify implementation meets every acceptance criterion and resolve any material mismatch.
- [ ] 3.5 Record the executed commands, results, and review disposition in this file. Mark tasks done only when the required checks pass and no implementation prerequisite remains unresolved.

These review and verification steps belong to future implementation. They have not been run while authoring the planning artifacts.

## Dependency Graph

```text
Host runtime available
          |
          v
Task 1 (blocked) ---> Task 2
          |             |
          +------+------+ 
                 |
                 v
               Task 3
```
