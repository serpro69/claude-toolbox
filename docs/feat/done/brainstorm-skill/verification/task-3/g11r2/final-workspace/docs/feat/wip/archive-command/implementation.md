# Implementation Plan: Archive Command

Design: [design.md](design.md). Work tracking: [tasks.md](tasks.md).

## Starting Point and Integration Targets

README.md is the only project source in this workspace. No language, runtime files, or executable tests are present. The responsibilities below identify what to locate in the eventual runtime; they do not invent an application structure.

| Responsibility | Concrete target to record before coding | Expected change |
| --- | --- | --- |
| Command dispatch and archive handler | Runtime command file and handler function | Accept one ID and implement direct archive behavior |
| Item lookup and persistence | Existing item representation and lookup/write functions | Reuse them; adjust only if necessary to preserve fields |
| Ordinary listing and link/edit access | Existing list, link resolution, and editing entry points | Preserve behavior; add focused regression coverage |
| Command and integration tests | Existing test files and exact invocation | Cover observable behavior and state preservation |
| User documentation | Runtime usage documentation | Explain one-item archival, visibility, repeat behavior, and missing IDs |

All targets are unresolved because runtime source has not been supplied. Resolve them within Task 1 before its implementation work. If no suitable runtime exists, stop implementation at that prerequisite; selecting a language or creating a new application requires separate scope.

## Active and Repeated Archival

1. Identify the runtime integration targets and record their actual file paths, functions, and test commands in this table. Inspect the item representation and persistence boundary for preservation behavior. → verify: every target resolves to inspected source, and the archived flag already exists.
2. Add focused coverage using a local collection with a target and unrelated items. Capture all item fields and relevant links before mutation. → verify: the test distinguishes exactly one archived-flag change from deletion, relocation, or unrelated-field changes.
3. Wire the archive handler into normal command dispatch. Look up one ID; for an active item, persist an update that changes only its archived flag. Report success after the write completes. → verify: dispatching the command archives exactly the selected item and preserves all other data.
4. Handle an already-archived item as a successful no-op before persistence. → verify: both a repeated invocation and an initially archived item cause no further write or data change, using the runtime's existing persistence test seam.

## Missing IDs and Operational Errors

1. Add missing-ID handling through the runtime's established error-reporting path. A lookup error must not be misreported as absence. → verify: an unknown ID reports failure, does not call persistence, and leaves a complete collection snapshot unchanged.
2. Propagate lookup and persistence errors without a success response. Preserve the storage mechanism's existing failure semantics; do not promise new rollback or crash guarantees. → verify: inject representative failures through existing test seams and check the reported outcome and permitted writes.

## Visibility and Link Preservation

1. Exercise archival through command dispatch and then list the collection normally. → verify: the item is present, marked archived by the existing presentation, and unrelated list entries remain present.
2. Follow links to the original item and access its existing editing path after archival. → verify: the same stable ID resolves, the original content is available, and the normal edit path continues to preserve IDs and links.
3. Confirm that no archive-specific filter, relocation, or link rewrite was introduced. → verify: inspect the resulting change and compare stored data against the pre-command snapshot.

## Documentation and Final Verification

1. Update the runtime's usage documentation with its actual command syntax and the specified outcomes. → verify: examples match the tested dispatch path and do not imply deletion, hiding, restore, or bulk support.
2. Run the runtime's complete existing test suite and the focused archival cases through `$kk:test`. → verify: record the actual commands and results in tasks.md; do not substitute a guessed command for unavailable runtime evidence.
3. Run `$kk:document`, `$kk:review-code` with the selected project language, and `$kk:review-spec` during implementation closeout. → verify: record outcomes, resolve actionable findings, and confirm conformance with all design success criteria.

These are future implementation checks. Creating this plan does not execute tests or independent review.

## Assumptions

The design's assumptions about unique IDs, an existing archived flag, local persistence, ordinary-list visibility, and link/edit preservation must be checked against the runtime at the specified steps. A mismatch is a reason to revisit the plan before coding around it.

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, synchronization, networking, new dependencies, language selection, and runtime scaffolding are excluded for the reasons recorded in [design.md](design.md#not-doing).

## Rejected Alternatives

Separate decision/execution adds unnecessary structure. Hiding violates list visibility. Moving notes adds avoidable location and link risks. See the [design decision](design.md#design-decision).
