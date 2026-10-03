# Tasks: Archive command

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: blocked — target note-tool runtime source and language are not present in the planning workspace
> Created: 2026-10-03
> Not Doing: bulk archival, restore, synchronization, new dependencies, network access, building the underlying note tool

The design is approved. Implementation has not started. Component names below identify responsibilities, not known source files. Replace them with actual paths after obtaining the target runtime. Size estimates must be checked against that mapping; split any task that would become L into smaller end-to-end paths.

## Task 1: Archive one existing note and repeat safely

- **Status:** blocked
- **Blocked:** The target note-tool runtime, language, and test runner are not available.
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [source mapping](./implementation.md#starting-point-and-source-mapping), [archive path](./implementation.md#archive-one-note-end-to-end)

### Subtasks

- [ ] 1.1 Obtain the target note-tool source and map the CLI registration, lookup, note mutation, persistence, and test entry points in implementation.md; replace component references in these subtasks with actual paths. Verify that the implementation surface and relevant test commands exist before editing runtime code.
- [ ] 1.2 In the CLI command tests, add an isolated collection with two notes and links to the selected note. Assert that `archive <id>` persists only the selected flag change and returns success after saving.
- [ ] 1.3 Extend command registration and its handler to resolve one ID and persist the selected flag through the existing storage boundary. Reuse established argument and error conventions, including basic failure propagation; do not introduce another store or note model.
- [ ] 1.4 Handle an already archived note as a successful no-op. Verify a repeated command preserves every persisted field and requests no additional write.
- [ ] 1.5 Run the focused command tests and reopen the collection to verify persistence, unchanged content and links, and unchanged unrelated notes.

## Task 2: Preserve ordinary access after archival

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [preserve access](./implementation.md#preserve-access-and-existing-behavior)

### Subtasks

- [ ] 2.1 Extend ordinary-list regression tests to archive a note and then list without special flags. Verify the note remains present with the existing archived marker.
- [ ] 2.2 Extend existing link-resolution and editing tests to cover an archived note. Verify unchanged identity and links and no unintended unarchive operation.
- [ ] 2.3 If runtime behavior conflicts with the documented contract, make the smallest necessary correction in the affected listing or editing component. Verify the new cases and existing active-note cases together.

## Task 3: Reject invalid requests and survive storage failure

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [invalid inputs and failures](./implementation.md#handle-invalid-requests-and-storage-failures)

### Subtasks

- [ ] 3.1 Extend command tests for a missing argument, extra arguments, invalid ID syntax under the existing grammar, and an unknown well-formed ID. Verify nonzero statuses, distinct usage/not-found diagnostics, and no collection writes.
- [ ] 3.2 Inspect the existing storage update boundary and validate its failure guarantees. Add fault injection for failed reads and saves; verify errors remain distinguishable from missing IDs and that no success message is emitted.
- [ ] 3.3 Correct any failure path that can damage or partially update the collection. Where partial writes are possible, exercise interruption at the relevant boundary and verify that the collection can be reopened intact.
- [ ] 3.4 Run successful, repeated, rejected, and failing archive cases together to verify that error handling preserves the valid path.

## Task 4: Final verification and user documentation

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [final verification](./implementation.md#final-verification-and-documentation), [acceptance criteria](./design.md#acceptance-criteria)

### Subtasks

- [ ] 4.1 Run `/kk:test` against the actual note-tool runtime, covering the full project suite and each archive acceptance criterion. Record the real commands and outcomes.
- [ ] 4.2 Run `/kk:document` to update CLI help and relevant user documentation with actual syntax, preserved visibility, idempotency, and errors. Verify examples against an isolated collection.
- [ ] 4.3 Run `/kk:review-code` with the implementation's actual language and resolve actionable findings.
- [ ] 4.4 Run `/kk:review-spec` against design.md, implementation.md, and tasks.md; reconcile deviations and verify every acceptance criterion before marking the feature done.

## Dependency Graph

```text
Target runtime available
          |
          v
        Task 1 ---> Task 2 ---> Task 3
          |          |           |
          +----------+-----------+
                     |
                     v
                   Task 4
```
