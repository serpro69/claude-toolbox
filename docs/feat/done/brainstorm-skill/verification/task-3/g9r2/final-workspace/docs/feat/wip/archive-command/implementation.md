# Archive command implementation plan

> Status: pending
> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)

## Starting point

Read the [README](../../../../README.md) and the [approved contract](./design.md#command-contract). The README is the only runtime description available. No code or tests are implemented by this planning work.

The implementation should reuse the eventual note tool's item model, ID lookup, local persistence, command conventions, ordinary listing, and link resolution. Do not select a language, add dependencies, or design a replacement store to fill gaps in this workspace.

## Runtime mapping prerequisite

Before implementation, identify the actual files and functions for these responsibilities and record their paths in Task 1's implementation notes:

| Responsibility | Planned touch or inspection |
| --- | --- |
| Command registration and argument parsing | Register `archive <id>` and require one ID |
| Archive handler or item operation | Implement the dedicated flag-update contract |
| Item lookup and persistence | Reuse existing interfaces; inspect missing-ID and save-failure semantics |
| Item model | Confirm the existing flag; no new field is needed |
| Ordinary listing and link resolution | Inspect and exercise preservation behavior |
| Command and collection tests | Add focused behavior tests using existing test infrastructure |
| README and command help | Document invocation, no-op behavior, errors, and visibility |

Only README.md is a known implementation-documentation path. Naming hypothetical source files here would misrepresent the repository. If runtime source is still absent when implementation begins, obtain the runtime project or its location before coding. A new application scaffold is outside this plan.

## Archive command end-to-end

Each step is paired with a concrete verification. Keep the complete command, its preservation checks, and its failure behavior in one bounded implementation slice.

1. **Map runtime components and existing conventions** → verify: record real source/test paths, the relevant test command, ID-lookup semantics, and save-failure behavior; confirm the archived field and ordinary-list support exist as described.
2. **Add behavioral cases in the existing command/collection test suite** → verify: new cases exercise the absent archive behavior and fail for the intended reason, rather than fixture or runner errors. Cover active, already archived, missing, malformed invocation, and storage-error outcomes.
3. **Register the command and implement the dedicated operation** → verify: exactly one ID is accepted, an active item's flag becomes true, and complete before/after snapshots prove all other fields and items are unchanged. Missing and already archived IDs must not reach the save operation.
4. **Integrate persistence and error reporting** → verify: success follows successful persistence; lookup and save failures produce errors without success output. Exercise failure through the project's existing test seam and confirm the valid collection remains usable. Use existing safe-save behavior; revise the approach if it cannot support the required integrity.
5. **Exercise the command through ordinary listing and link resolution** → verify: after archival, the selected item remains listed with its existing archived marking and links still resolve to the same content. Repeat the command and compare the entire collection again to prove the no-op behavior.
6. **Update README.md and command help in the implementation project** → verify: the documented single-ID invocation matches the parser, and the text explains retained visibility, idempotence, missing-ID failure, and excluded bulk/restore behavior.

Do not add an archive-specific listing, metadata migration, new storage abstraction, or timestamp. Reuse helpers where their semantics fit, without relying on a general edit operation to preserve unsubmitted fields implicitly.

## Verification scenarios

| Scenario | Observable result |
| --- | --- |
| Archive active item A alongside item B | A.archived is true; A's other values and all of B remain identical |
| List and follow links after archival | A remains visible and marked archived; its links still resolve |
| Archive A again | Success; identical collection; no persistence call |
| Archive an absent ID | Missing-item error; identical collection; no persistence call |
| Invoke with zero or multiple IDs | Usage error; no item mutation |
| Lookup fails | Operation error distinguishable from a missing item; no write |
| Persistence fails | No success output; collection integrity and unrelated data preserved through the existing save mechanism |

Use isolated test collections and existing failure-injection facilities. Prefer assertions on observable collection behavior; checking that repeated/missing-ID requests bypass saving specifically verifies the no-write contract.

## Assumptions

The [design assumptions](./design.md#assumptions) must be checked during runtime mapping and behavior tests: stable-ID lookup is available, a flag-only update preserves other data, and persistence has a suitable failure boundary. Missing source is a prerequisite to implementation, not a reason to fabricate interfaces or test commands.

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, and network access are excluded for the [reasons in the design](./design.md#not-doing). No deferred feature is required to complete this increment.

## Rejected Alternatives

General-edit routing depends on unverified partial-update semantics. Hiding contradicts required listing behavior, and relocation adds link and storage risks. The [design decision](./design.md#alternatives-and-decision) records the comparison.

## Final verification

After implementation, run the project's full test suite through `$kk:test`, update relevant documentation through `$kk:document`, review with `$kk:review-code` using the actual project language, and check conformance through `$kk:review-spec`. Record the executed checks and results in tasks.md. These are future implementation tasks; no implementation or follow-up review is authorized as part of this document-writing turn.
