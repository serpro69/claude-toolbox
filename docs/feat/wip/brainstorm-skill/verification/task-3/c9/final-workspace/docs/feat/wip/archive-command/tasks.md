# Tasks: Archive command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access

The design is approved; implementation has not started. This workspace has no runtime source or selected language. Component names below identify responsibilities, not existing files. During Task 1, map them to the eventual runtime's concrete source/test paths and record its test commands before code changes. Each task is a complete behavior slice, including its verification and relevant user documentation.

## Task 1: Archive one active note while preserving access

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md — Step 1](implementation.md#step-1-archive-one-active-note-end-to-end)

### Subtasks

- [ ] 1.1 Identify the runtime language, command dispatch, note lookup/persistence, listing/reference components, and command test harness; record concrete files and test commands here. Verify stable IDs uniquely select notes and archive updates can preserve all other fields.
- [ ] 1.2 Add an acceptance fixture with an active target, unrelated note, and working reference to the target; establish baseline ordinary listing and reference resolution.
- [ ] 1.3 Register the single-ID archive command and implement the dedicated flag update through the persistence boundary. Report success only after persistence succeeds.
- [ ] 1.4 Verify through the command entry point that only the target's archive flag changes; its ID, title, body, links, ordinary visibility, and reference resolution remain intact, and the unrelated note is unchanged.
- [ ] 1.5 Update README.md and command help with single-note archival and retained visibility/content; check the documented example against the acceptance fixture.

## Task 2: Handle repeats and invalid selections without changes

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md — Step 2](implementation.md#step-2-make-repeats-and-rejected-requests-harmless)

### Subtasks

- [ ] 2.1 Extend the archive operation so an already archived target succeeds without a persistence write.
- [ ] 2.2 Ensure unknown IDs report failure before mutation, and missing/extra arguments fail validation without dispatching an update.
- [ ] 2.3 Verify repeated archival and an initially archived target both preserve complete collection state and perform no extra write.
- [ ] 2.4 Verify unknown IDs, no ID, and two IDs fail with no write or item changes; ensure there is no implicit item creation or bulk behavior.
- [ ] 2.5 Update README.md and help with repeat and missing-ID behavior; check the text against observed command outcomes.

## Task 3: Report lookup and persistence failures correctly

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md — Step 3](implementation.md#step-3-verify-storage-failure-reporting)

### Subtasks

- [ ] 3.1 Exercise failures through the lookup/persistence test seams and ensure the archive command propagates them as failures without success acknowledgment.
- [ ] 3.2 Ensure a failed persistence attempt does not leave a misleading successful archive state in memory; follow the existing storage update/rollback conventions.
- [ ] 3.3 Verify lookup failures perform no write and simulated pre-commit persistence failures leave persisted state unchanged, with unrelated items untouched.
- [ ] 3.4 Record the storage guarantees actually supported and tested; do not claim unverified crash or concurrent-writer behavior.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md — Step 4](implementation.md#step-4-final-verification-and-documentation)

### Subtasks

- [ ] 4.1 Invoke `/kk:test` for the full runtime test suite, including every archive acceptance-matrix scenario; record actual results.
- [ ] 4.2 Invoke `/kk:document` to check README.md and help for accurate invocation, visibility, no-op behavior, errors, and exclusions.
- [ ] 4.3 Invoke `/kk:review-code` with the runtime's selected language and resolve implementation findings.
- [ ] 4.4 Invoke `/kk:review-spec` against design.md, implementation.md, and tasks.md; resolve mismatches and record outcomes.
- [ ] 4.5 Mark the feature complete only when all acceptance criteria have observed evidence and the preceding tasks are done.

## Dependency Graph

```text
Task 1 ----> Task 2 ----> Task 3 ----> Task 4
   |                       ^            ^
   +-----------------------+            |
   +------------------------------------+
              Task 2 -------------------+
```
