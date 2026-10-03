# Archive command implementation plan

> Status: pending; host runtime required before coding
> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)

## Starting point and integration prerequisite

Only [README.md](../../../../README.md) exists as project source in this planning workspace. There is no selected language, runtime implementation, or test runner. Do not treat proposed components below as existing files or introduce a runtime just to fill that gap.

Before Task 1 can proceed, obtain the eventual host source and record its real paths in this plan and the corresponding tasks. This is a prerequisite within the first user-facing slice, not a separate infrastructure feature. Resolve these targets:

| Logical target | Required mapping and responsibility |
| --- | --- |
| Command registration and argument parsing | Existing dispatcher path and extension point for one ID |
| Archive command handler | Existing or new host-conventional file that owns lookup, branching, update, and outcome reporting |
| Item lookup and persistence | Existing functions and paths for ID lookup and single-item updates; reuse without replacing storage |
| Ordinary listing and link resolution | Existing paths used for compatibility checks; archive must preserve their specified behavior |
| Command and integration tests | Host test files, fixture facilities, and exact focused test commands |
| User documentation | Host command-reference path and executable syntax; use this workspace's README only if it is the host's actual documentation |

Mapping integration points → verify: every recorded existing file and symbol is present, any proposed new path follows the host layout, the relevant tests can be identified, and no new dependency or network access is needed. If an assumption in [design.md](design.md#assumptions) fails, resolve the mismatch before coding instead of silently expanding this feature.

## Slice 1: Archive an active item and retain access

This slice delivers the owner's complete successful path, including visibility and links.

1. Record the host integration mappings above and identify the existing single-item mutation guarantees → verify: the host can update the archived flag without reconstructing or dropping other fields, and existing IDs are unique for lookup purposes.
2. Add an acceptance test in the mapped command/integration test files using an active target with title, body, a resolvable link, and unrelated collection entries → verify: it fails specifically because the archive command is absent or does not yet perform the required archive action.
3. Register the archive command in the mapped dispatcher, following existing single-ID parsing and error conventions → verify: one ID reaches the handler, and the parser rejects unsupported argument shapes without mutation according to host conventions.
4. Implement direct handler logic: resolve the ID, branch on missing/already archived/active, and update only the active target's archived flag through existing persistence → verify: the command reports successful archival only after a successful update, and a full collection comparison shows only the intended flag changed.
5. Exercise ordinary listing and link access through the existing integration points → verify: the archived item is still listed with the existing archived marker, and its previous link resolves to the same ID and content.
6. Cover persistence failure with the existing test facilities → verify: a failed update does not produce the newly archived success outcome. Do not add a fault-injection dependency.

Missing and already archived branches must be safe from the first implementation; Slice 2 supplies focused regression coverage and confirms their output contract. Do not temporarily implement a toggle, deletion, or unchecked update.

## Slice 2: Confirm repeat and missing-ID outcomes

This slice completes the command's predictable behavior for retries and failed lookups.

1. In the mapped handler and command tests, exercise an item that is already archived → verify: the result identifies an already archived successful no-op, the complete collection remains identical, and the handler does not issue another persistence update.
2. Run archive twice on an initially active item → verify: the first result is newly archived, the second is already archived, and the state after the second invocation equals the state after the first.
3. Invoke archive with an absent ID → verify: the result identifies a missing item through the host's error convention and the complete collection remains unchanged.
4. Capture observable output and status semantics in the tests → verify: callers can distinguish newly archived, already archived, and missing without depending on newly invented machine-readable formats.
5. Repeat listing and link checks after the no-op path → verify: repeat operations preserve access as well as state.

## Acceptance checks

| Case | Observable check |
| --- | --- |
| Active target among several notes | Only the target's archived flag changes |
| Preserved data | ID, title, body, links, and every other field are identical before and after |
| Unrelated notes | Full item representations remain unchanged |
| Ordinary list after archive | Target remains present and marked archived |
| Link after archive | Existing link reaches the same item and content |
| Already archived target | Successful no-op with no additional update |
| Archive repeated after success | State equals the first invocation's resulting state |
| Absent ID | Missing-item result and no item changes |
| Persistence failure | Failure reported; no success report |

The focused tests must exercise public command behavior and preservation requirements. Use the host's existing test runner and test facilities. Exact command strings are deliberately unresolved until source is available; record them during the integration mapping instead of presenting invented executable checks as runnable.

## Assumptions

Implementation depends on unique stable IDs, field-preserving single-item updates, ordinary-list visibility for archived items, unchanged link resolution, and host conventions usable offline without dependencies. Validate each as described in [design.md](design.md#assumptions) during Slice 1. Runtime and persistence capabilities are currently unverified.

## Not Doing

Deletion, hiding, and moving notes conflict with preservation and visibility. Bulk operations and restore are outside the single-ID increment. Synchronization, network access, and new dependencies are unnecessary. Runtime and storage replacement are outside the integration plan. These are exclusions, not deferred tasks.

## Rejected Alternatives

A reusable archive operation adds structure for an unconfirmed additional caller. Hiding or moving notes violates the selected access-preservation approach. The handler therefore owns the direct update while reusing existing lookup and persistence mechanisms.

## Final verification and documentation

Run the focused archive acceptance cases and the host's full suite through `/kk:test` → verify: the approved behavior and existing command/list/link behavior pass together.

Use `/kk:document` to update the host's command reference with actual syntax and the three outcomes → verify: examples match the tested command and clearly state that archived notes remain listed and accessible.

Use `/kk:review-code` with the actual host language and `/kk:review-spec` against these three planning artifacts → verify: relevant findings are resolved and implementation matches the approved scope. These are future implementation tasks; no review or test execution is performed as part of writing this plan.

Finish by recording the actual verification commands and results in `tasks.md`. Any unresolved prerequisite or failing acceptance check keeps implementation incomplete.
