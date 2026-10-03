# Archive command implementation plan

> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)
> Status: planned; runtime prerequisite unresolved

## Starting point

[README.md](../../../../README.md) is the only project source available in this planning workspace. It describes the item model and required behavior but supplies no executable, programming language, source files, persistence mechanism, or test harness. Do not treat any module or callable named below as an existing implementation.

Before implementation starts, identify the real runtime and record its language, paths, test harness, and command conventions in this plan. If they remain unavailable, keep the first task blocked. Selecting a language or scaffolding an entire note application requires a separate decision; it is not silently included in adding this command.

## Component map

These responsibilities describe the integration points. Replace the unresolved paths with concrete source and test paths before code changes.

| Component | Required responsibility | Source path |
| --- | --- | --- |
| Command dispatch and archive handler | Register `archive <id>`, validate argument count, map results to established output and exit conventions | Unresolved: runtime absent |
| Dedicated archive operation | Look up one ID, handle missing/already archived states, prepare only the archived-flag change | Unresolved: runtime absent |
| Collection lookup and persistence | Preserve identity and unrelated data; commit the update without partial changes | Unresolved: runtime absent |
| Listing and link resolution | Exercise existing visibility, marker, and link contracts; no behavior change intended | Unresolved: runtime absent |
| Command and collection tests | Exercise the real command path, state comparisons, and persistence failure injection | Unresolved: test harness absent |
| User documentation | Explain invocation, outcomes, preservation, and scope | `README.md` |

Responsibilities may share a module when that fits the runtime; this table does not prescribe a layered architecture or one file per row. No new package or framework is needed by the design.

## Step 1: Archive one active item end to end

Prerequisite → verify: locate the runtime, resolve the component map to real paths, and identify an existing way to run its command and collection tests. Confirm ID uniqueness, item shape, listing markers, and link resolution against those interfaces.

Command and operation → verify: register the single-ID archive command, connect it to lookup and persistence, and run it against a fixture with multiple active items. Reload the collection and confirm that exactly the selected item's archived flag changed.

Preservation and presentation → verify: compare all fields and other items against the original snapshot; run ordinary listing and resolve a pre-existing link to the selected item. Check the archived marker and unchanged identity and content. Confirm success output occurs only after the save succeeds.

This slice includes command dispatch, the dedicated operation, persistence integration, and the tests for a complete user path. Avoid introducing broader edit callbacks or rewriting the stored item schema.

## Step 2: Make repeat and invalid selections safe

Already archived selection → verify: return success describing the existing state without saving. Test both repeated invocation after Step 1 and an item that starts archived; compare complete state and observe zero additional saves.

Missing ID → verify: report a missing-item failure before attempting a save. Test with a populated collection, compare all items, and assert zero saves.

Invalid argument count → verify: reject missing and extra IDs before invoking the mutating operation. Exercise both cases through command dispatch and assert failure, unchanged collection state, and zero saves. Preserve any established ID validation conventions; do not invent a new ID format.

## Step 3: Preserve state when persistence fails

Failure-safe update → verify: prepare the flag change without mutating the original shared item, then commit through the runtime's storage mechanism. Determine how that mechanism prevents partial updates; do not assume that a failed save leaves state intact.

Failure injection → verify: force a save failure through the persistence boundary. Assert failure output, no success output, unchanged live and persisted collection state, preserved ordinary-list visibility, and working existing links. If the storage mechanism exposes multiple failure points, include those that could leave a partial change.

Retry after failure → verify: remove the injected failure and repeat the same command. It must archive the same ID once and preserve all unrelated data. A subsequent repeat must perform no additional save.

Keep this work scoped to the command's single-item update. If the runtime cannot meet the required failure contract without a broader storage redesign, stop implementation at that unresolved prerequisite and amend the plan with the concrete issue.

## Step 4: Complete documentation and verification

User-facing help and README → verify: document the actual executable invocation, one-ID selection, repeat behavior, missing-ID errors, and retained visibility and links. Check examples against the implemented command and its help output.

Regression verification → verify: run the full runtime test suite through `/kk:test`, including archival, listing, link resolution, and existing editing behavior. Record actual commands and results when a runtime exists.

Documentation completion → verify: use `/kk:document` to check relevant documentation against the delivered behavior and preserve the explicit scope exclusions.

Implementation review → verify: invoke `/kk:review-code` with the actual project language, followed by `/kk:review-spec` against these three documents. Address applicable findings and keep task status aligned with evidence.

These are future implementation activities. This planning request does not execute implementation, tests of a nonexistent runtime, or follow-up reviews.

## Assumptions

The implementation depends on unique stable IDs, a field-preserving update mechanism, failure-safe persistence, and the documented listing/link contracts. Each has an explicit check above. Runtime availability is unresolved and blocks coding. The complete assumption list is in [design.md](design.md#assumptions-and-implementation-prerequisites).

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, synchronization, network access, and new dependencies are excluded for the reasons in [design.md](design.md#not-doing).

## Rejected Alternatives

The general editing route adds unnecessary coupling; hiding and moving conflict with the selected preservation contract. See [design.md](design.md#rejected-alternatives). Lower-level lookup and persistence reuse remains compatible with the dedicated operation.
