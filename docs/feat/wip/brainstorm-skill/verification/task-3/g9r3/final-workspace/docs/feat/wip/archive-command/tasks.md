# Tasks: Archive command

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access, new archive metadata, schema migration

The design is approved. All implementation tasks remain pending. This workspace has no runtime source or selected language. Before coding, Task 1 must identify the actual tool's integration points and update the component references below with concrete files and symbols. Source availability is a prerequisite, not authorization to build a replacement note tool.

## Task 1: Archive an existing note and preserve access

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [integration mapping](./implementation.md#source-availability-and-integration-mapping), [existing-note slice](./implementation.md#slice-1-archive-an-existing-note)

### Subtasks

- [ ] 1.1 Locate the actual tool's command dispatcher, ID lookup, item-update/persistence interface, listing/link components, and test harness; record concrete file/symbol references and runnable test commands in these documents → verify: every integration responsibility is mapped or explicitly blocked before coding.
- [ ] 1.2 Add a command integration scenario with an active target, neighboring items, and a link to the target using the existing temporary-store harness → verify: it detects the missing archive behavior and snapshots the fields that must be preserved.
- [ ] 1.3 Register `archive <id>` in the existing dispatcher and implement the active-item flag update through the current persistence path → verify: after reopening the collection, exactly the target's archived flag has changed, with identical IDs, titles, bodies, links, and neighboring items.
- [ ] 1.4 Add the already-archived branch to the command handler and report successful changed/already-archived outcomes using current output conventions → verify: repeated invocation succeeds, leaves the full collection unchanged, and issues no further update.
- [ ] 1.5 Exercise ordinary listing and existing link resolution after archival → verify: the item remains listed with its existing archived marking and links still resolve to its preserved content.
- [ ] 1.6 Update command help and `README.md` usage documentation → verify: both describe one-ID archival, retained visibility, and idempotent repeat behavior accurately.

## Task 2: Reject invalid requests and report failures

- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [failure slice](./implementation.md#slice-2-report-invalid-requests-and-storage-failures), [command contract](./design.md#command-contract)

### Subtasks

- [ ] 2.1 Validate exactly one ID in the command parser/handler using existing conventions → verify: missing and extra arguments produce usage errors before mutation, and all collection snapshots remain unchanged.
- [ ] 2.2 Handle unknown IDs through the established lookup/error path → verify: the command returns failure, identifies the missing ID, and changes no item or persisted data.
- [ ] 2.3 Propagate lookup and persistence errors in the command handler before any success message → verify: injected failures return failure without success output; lookup failure performs no update, and write failure preserves the storage mechanism's established guarantees.
- [ ] 2.4 Check `README.md` and command help against the tested error behavior → verify: documentation matches the implemented outcomes and introduces no excluded operation.

## Task 3: Final verification

- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [acceptance matrix](./implementation.md#acceptance-matrix), [final verification](./implementation.md#final-verification-and-documentation)

### Subtasks

- [ ] 3.1 Invoke `$kk:test` for the focused archive scenarios and full existing suite using the commands recorded in Task 1 → verify: the entire acceptance matrix passes, including ordinary listing, editing, links, repeated invocation, and unsuccessful requests.
- [ ] 3.2 Invoke `$kk:document` to finalize README/help and relevant feature documentation → verify: documented behavior and concrete integration references match the implementation.
- [ ] 3.3 Invoke `$kk:review-code` with the project's language identified in Task 1 → verify: actionable findings are resolved or explicitly dispositioned.
- [ ] 3.4 Invoke `$kk:review-spec` against `design.md`, `implementation.md`, and `tasks.md` → verify: implemented behavior matches the approved design and task statuses reflect completed work.

These verification subtasks apply after implementation. No implementation or follow-up review is run as part of writing this plan.

## Dependency Graph

```text
Task 1 ──→ Task 2 ──→ Task 3
   └────────────────→ Task 3
```
