# Tasks: Archive Command

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, networking, new dependencies, language selection, runtime scaffolding

Runtime paths are unresolved: the supplied workspace contains requirements only. Each task's named integration responsibilities must be mapped to actual runtime files in Task 1 before coding. Sizes describe expected change complexity and must be reassessed after that mapping; split any task that would become L.

## Task 1: Archive one item and safely repeat the command

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#active-and-repeated-archival](implementation.md#active-and-repeated-archival)

### Subtasks

- [ ] 1.1 Resolve the runtime prerequisite and fill the integration-target table in implementation.md with actual command, item-store, listing/link/edit, test, and usage-documentation paths. Record the selected language and exact test invocations. Do not create a runtime to fill this gap.
- [ ] 1.2 Verify unique-ID lookup, the existing archived flag, and field-preserving persistence; revisit the design if any assumption fails.
- [ ] 1.3 In the resolved archive-command tests, cover an active target with unrelated items and links, and assert that exactly its archived flag changes.
- [ ] 1.4 Implement and register the direct archive handler through the resolved command dispatch and item-store functions. Persist before reporting success.
- [ ] 1.5 Cover repeated archival and an initially archived item; both must succeed without another write or state change.
- [ ] 1.6 Run the resolved tests for this complete command path and record their results.

## Task 2: Report missing IDs and operational failures

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#missing-ids-and-operational-errors](implementation.md#missing-ids-and-operational-errors)

### Subtasks

- [ ] 2.1 Extend the resolved archive handler and its tests to report a missing ID without invoking persistence or changing any item.
- [ ] 2.2 Keep lookup failures distinct from absent IDs and ensure persistence failures never produce a success result.
- [ ] 2.3 Use existing test seams to exercise lookup/write failures. Check error reporting and preserve established storage failure semantics.
- [ ] 2.4 Run the resolved command tests, including complete collection snapshot comparisons for the missing-ID case, and record results.

## Task 3: Verify ordinary access to archived notes

- **Status:** pending
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#visibility-and-link-preservation](implementation.md#visibility-and-link-preservation)

### Subtasks

- [ ] 3.1 Add coverage in the resolved integration tests that archives a note and finds it in the ordinary list with its existing archived marker.
- [ ] 3.2 Verify the original ID and links still resolve to the same content and that the existing editing path preserves IDs and links after archival.
- [ ] 3.3 Confirm no note relocation, hiding, deletion, or unrelated item mutation occurs. Correct archive integration if this check fails.
- [ ] 3.4 Update the resolved usage documentation with actual invocation syntax, preserved visibility, idempotence, and missing-ID behavior.
- [ ] 3.5 Run the relevant integration tests and record results.

## Task 4: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#documentation-and-final-verification](implementation.md#documentation-and-final-verification)

### Subtasks

- [ ] 4.1 Invoke `$kk:test` against the implementation and run the full runtime test suite, including active, repeated, already-archived, missing-ID, visibility, link-preservation, and operational-error cases.
- [ ] 4.2 Invoke `$kk:document` to ensure relevant runtime documentation matches the delivered behavior.
- [ ] 4.3 Invoke `$kk:review-code` with the selected project language and address actionable findings.
- [ ] 4.4 Invoke `$kk:review-spec` to verify conformance to design.md and implementation.md.
- [ ] 4.5 Record actual commands, review outcomes, and remaining limitations; mark the feature done only when required checks pass.

## Dependency Graph

```text
Task 1 ---> Task 2 ---> Task 3 ---> Task 4
   |            |                    ^
   +------------+--------------------+
```
