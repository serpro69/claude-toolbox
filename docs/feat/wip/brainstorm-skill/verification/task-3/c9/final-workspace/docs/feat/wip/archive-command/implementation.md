# Archive command implementation plan

Status: pending; planning only.

Contract: [design](design.md). Execution tracking: [tasks](tasks.md).

## Starting point and integration map

The only runtime description is [README.md](../../../../README.md). There is no selected language, runtime source, executable, or test harness in this workspace. Do not interpret the component names below as existing files. Once the runtime is available, identify or create the narrow archive integration in its normal source layout and record concrete file paths in tasks.md before changing code. This mapping is part of implementation preparation, not permission to invent a new application architecture.

| Component or artifact | Required work |
| --- | --- |
| Command registration and argument handling | Register `archive` with exactly one ID argument and normal help/error conventions |
| Archive operation | Resolve the ID, distinguish active/archived/missing outcomes, and update only archive state |
| Note lookup and persistence boundary | Reuse identity and storage primitives; preserve all other data and surface storage errors |
| Ordinary listing and reference resolution | Preserve current behavior; exercise both after archival |
| Command-level test suite and temporary collection fixtures | Observe command outcomes, complete persisted state, listing, references, and write calls |
| README.md and command help | Document invocation, retained visibility/content, idempotence, and missing-ID behavior |

No new dependency, remote service, network access, data field, or schema migration is planned. The archived flag already exists in the stated data model.

## Step 1: Archive one active note end to end

Establish the eventual runtime's ID matching, command result conventions, storage update mechanism, and test entry points. Record the source/test paths and project language in tasks.md. Preserve existing conventions instead of selecting an unrelated command framework.

Create a temporary collection with an active target, an unrelated note, and a reference to the target. Add a command-level acceptance test that initially demonstrates the absent archive behavior. Register the command, require one ID, resolve the target, and persist an update that changes only its archived flag. Return success only after persistence reports success. Keep listing and reference behavior intact. Update command help and README.md for this user-facing path in the same slice.

**Step → verify:** Invoke archival for the target. Compare complete persisted state: exactly the target's archived flag changes. Confirm the target remains in ordinary listing with the existing archived marker and its reference still resolves. Confirm the unrelated note and all other target fields are identical. The same fixture must establish that listing and reference resolution worked before archival.

## Step 2: Make repeats and rejected requests harmless

Extend the same command operation and its acceptance tests. Return success immediately for an already archived note. Reject an unknown ID before mutation. Validate missing and extra arguments before lookup/update dispatch; do not interpret multiple arguments as a bulk operation.

Document the no-op and error outcomes in help/README.md without changing the existing listing contract. Use the runtime's normal success/failure signaling; exact message wording is not the feature contract.

**Step → verify:** Execute the command twice for the same note and assert the second call succeeds, does not write, and leaves complete state unchanged. Repeat with a note already archived in the initial fixture. Test an unknown ID, no ID, and two IDs: each fails, writes nothing, and leaves every item unchanged. Check that argument errors do not accidentally dispatch a target update.

## Step 3: Verify storage failure reporting

Exercise the archive path with controlled lookup and persistence failures through the runtime's existing test seams. Propagate failures to the command result without printing success. If an update is prepared in memory before persistence, ensure a failed attempt does not leave the running command's collection state falsely marked as a successful update; use a candidate update or the established rollback mechanism as appropriate.

Inspect the actual persistence mechanism before claiming rollback, atomicity, crash safety, or concurrent-writer guarantees. Reuse its established behavior and document any relevant limitation. This task does not add a replacement storage protocol.

**Step → verify:** A lookup failure performs no write. A simulated failure before a persistence commit reports failure and leaves the persisted fixture unchanged. No failure reports successful archival. Check that unrelated items remain untouched. Record the scope of the storage guarantees demonstrated by these tests.

## Step 4: Final verification and documentation

Run the project's established complete test suite through `/kk:test`, including the archive command scenarios below. Use `/kk:document` to check README.md and command help against the finished behavior. Invoke `/kk:review-code` with the selected project language, followed by `/kk:review-spec` against this directory. Resolve findings before marking the feature done.

These are future implementation activities. Creating these planning artifacts does not execute tests, implementation, or independent review.

**Step → verify:** Record actual test results and review outcomes in tasks.md. Confirm every acceptance criterion in design.md has observed evidence; all implementation tasks remain pending until their work is performed.

## Acceptance matrix

| Scenario | Command observation | Data and integration observation |
| --- | --- | --- |
| Active target | Success after persistence | Only target archive flag changes; listing and reference continue to work |
| Repeated command | Success | No additional write or state change |
| Initially archived target | Success | No write or state change |
| Unknown ID | Missing-ID failure | No write; full collection unchanged |
| No ID | Usage failure | No mutation dispatched |
| Two IDs | Usage failure | No mutation dispatched; no bulk behavior |
| Lookup failure | Failure, no success acknowledgment | No write |
| Persistence failure before commit | Failure, no success acknowledgment | Persisted fixture unchanged; no misleading successful in-memory state |

Use test mechanisms native to the eventual runtime. Do not add a test library solely for this increment. Test names and execution commands must be recorded once that runtime exists, rather than invented in this language-neutral plan.

## Assumptions, exclusions, and rationale

Validate the [design assumptions](design.md#assumptions) while mapping the runtime. The [Not Doing](design.md#not-doing) boundaries apply to every step. The dedicated flag update was selected over routing through editing; hiding or moving notes was rejected because access and references must remain intact. See [Rejected Alternatives](design.md#rejected-alternatives).
