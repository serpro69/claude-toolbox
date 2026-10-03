# Archive command implementation plan

> Status: planned; runtime source and language required before implementation
> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)

## Starting point and integration prerequisite

The workspace currently contains requirements in [README.md](../../../../README.md), with no runtime source or selected language. The file/component targets below are logical targets to resolve against the eventual implementation project. They are not claims that files or functions already exist.

Before making code changes, record actual file/function paths and executable verification commands in this document and the corresponding task. If runtime source remains unavailable, keep Task 1 blocked and request it; do not invent a language, storage format, framework, or parallel implementation of the note collection.

| Logical target | Information to establish from source |
| --- | --- |
| Command registration and handler | Entry point, argument validation, output conventions, and failure status conventions. |
| Item representation and lookup | Archived flag representation, ID type/matching, uniqueness, and lookup error handling. |
| Item persistence | Existing update API, preservation of all fields, commit behavior, cache behavior, and concurrency guarantees. |
| Ordinary listing and link resolution | Existing archived marker, inclusion behavior, and how stable IDs connect links to items. |
| Tests and user documentation | Local fixture helpers, command/integration test locations, relevant test commands, and command documentation location. |

Step → verify: map these targets to actual source and record the relevant test commands; verify that each referenced path exists and each mapped behavior has evidence in source or a focused existing test. Confirm that implementation needs no added dependency or network access.

## Active-item archive path

This is the first complete user-facing slice. Keep command parsing, the dedicated archive operation, persistence, and its tests together rather than delivering isolated layers.

1. In the existing command registration/handler, register the archive action with exactly one ID, following the established interface. Step → verify: the command is reachable, valid input reaches the archive operation, and invalid argument count cannot initiate a write.
2. Add the dedicated archive operation in the nearest existing item-operation component. Resolve the ID, handle missing and already-archived outcomes before mutation, and assign the archived flag to true for an active target. Step → verify: a focused test targets one of two items and observes exactly one changed flag.
3. Persist through the existing item-write path, preserving the complete item representation. Expose an archive success outcome only after successful persistence. Step → verify: reload the stored collection and compare complete records; only the selected item's flag differs.
4. Exercise the ordinary listing and link resolver through their existing interfaces. Step → verify: the archived target remains visible with the established archived marker, and links resolve to the same stable ID and retained content.

The operation's name and placement should follow project conventions. Avoid exporting a new generic update interface solely to serve this command. Do not change listing or editing semantics to make archival work.

## Repeated-command path

Strengthen the first slice with explicit no-op behavior for an archived target.

1. Use the pre-write archived check to return an already-archived outcome and report it using existing output conventions. Step → verify: begin with an archived target and compare complete collection snapshots before and after invocation; they are identical.
2. Exercise two consecutive invocations against an initially active target. Step → verify: the second leaves the collection identical to the state after the first, retains link/list behavior, and bypasses persistence writes where the storage test seam can observe them.

Do not toggle the flag or rewrite an item merely to repeat a successful command.

## Missing-item and persistence-failure paths

1. Return the missing-item outcome from lookup without creating a placeholder or invoking persistence. Step → verify: invoke a nonexistent ID, confirm the missing-item report, compare complete collection snapshots, and assert no write through the available test seam.
2. Translate actual storage failures through the existing command error path. Step → verify: inject a failure through the project's existing test facilities and confirm no success message is emitted.
3. Preserve the storage mechanism's recovery and in-memory consistency guarantees. Step → verify: after the injected failure, inspect the persisted collection and any shared cached item; no cached item may falsely represent a successful archival. Document storage-specific recovery expectations before this check is finalized.

The design does not assume a particular transaction API or atomic file-replacement strategy. Choose the appropriate existing mechanism only after inspecting the actual source; do not add dependencies or a separate storage subsystem.

## Verification matrix

| Check | Fixture and observation |
| --- | --- |
| Exact target | Two active items with distinct IDs; archive one and compare complete records. |
| Content preservation | A target with nonempty title/body and working links; compare all fields other than its flag and resolve the links afterward. |
| Ordinary visibility | Invoke the real listing path after archival; target remains present with its existing archived distinction. |
| Already archived | Start archived; invocation performs no further state change or persistence write. |
| Repetition | Archive an active target twice; the second invocation preserves the first result exactly. |
| Missing ID | Invoke a nonexistent ID; report it and preserve all items without a write. |
| Persistence failure | Inject a write failure; report failure without false success or misleading cached state. |
| Existing behavior | Run relevant existing listing, editing, identity/link, and persistence tests, then the project's full local test suite. |

Do not add tests that merely restate implementation internals. Prefer command-to-storage assertions for the user contract; use targeted operation or storage tests where they provide reliable observation of no writes and injected failures.

## Assumptions and scope

The [design assumptions](design.md#assumptions) must be checked against the supplied runtime before implementation: unique IDs, a stored archived flag, field-preserving persistence, and list inclusion driven by that flag.

The [scope exclusions](design.md#not-doing) apply to every slice: no deletion, hiding, moving, bulk operations, restore, synchronization, dependencies, network access, or generic update framework. The [rejected alternatives](design.md#rejected-alternatives) record why the dedicated operation was selected. These exclusions are not deferred tasks in this plan.

## Final verification and documentation

Step → verify: run `/kk:test` using the runtime project's actual local commands and the matrix above; record results and any environment limitations.

Step → verify: use `/kk:document` to add the archive command to the runtime project's user documentation, covering preserved ordinary-list visibility, repeated invocation, and missing IDs; check those statements against observed command behavior.

Step → verify: after implementation, invoke `/kk:review-code` with the established language and `/kk:review-spec` against these three planning documents; resolve applicable findings before marking the feature complete.

These are future implementation tasks. This planning delivery does not implement the command or run a follow-up review.
