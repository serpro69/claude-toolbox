# Archive command implementation plan

> Status: pending
> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)

## Source availability and integration mapping

The planning workspace contains only [README.md](../../../../README.md). There is no selected language or runtime source. Do not interpret the component names below as existing paths, and do not create a new note application to fill that gap.

Before starting Task 1, locate the actual note-tool checkout and record the concrete files, symbols, and test commands in this plan and the task list:

| Integration responsibility | What to locate | Expected use |
| --- | --- | --- |
| Command entry point | Parser, dispatcher, command registration, and help conventions | Register `archive <id>` and validate one argument |
| ID lookup | Stable-ID lookup and missing-item reporting | Resolve one existing item using current matching rules |
| Item state | Existing archived field and item-update interface | Change only the archived flag |
| Persistence | Existing save/update mechanism and failure semantics | Persist the change before reporting success |
| Output | Success messages, error reporting, and exit conventions | Report changed, already archived, and failed outcomes |
| Ordinary listing and links | Listing behavior and link-resolution implementation | Verify preserved visibility, marking, and access |
| Tests | Command harness, temporary stores, fixtures, and fault-injection seams | Exercise end-to-end behavior and failures |

This mapping is an implementation prerequisite, not a separate architectural layer to build. If the source or any essential guarantee is unavailable, record the concrete blocker before coding. Do not guess a language, filename, library, schema change, or persistence API.

## Slice 1: Archive an existing note

Implement a complete command path for an existing ID, including repeat invocation and regression coverage.

1. Map the integration responsibilities above and validate the design assumptions against the runtime → verify: every responsibility has an actual file/symbol reference or an explicit blocker; the existing listing and link behavior matches the README.
2. Add a command-level regression scenario using a temporary collection with a target, neighboring items, and a link to the target → verify: the scenario detects the missing archive behavior before implementation while existing commands still work.
3. Register `archive <id>` in the existing dispatcher and resolve the ID through the current lookup path → verify: a command invocation reaches the correct item using the established ID rules.
4. For an active item, persist only the archived-flag change through the existing update mechanism → verify: reopening the collection shows exactly that change; target content, ID, links, and all neighboring records match their snapshots.
5. For an already-archived item, return a successful result without another write → verify: repeated invocation preserves the stored snapshot and the update seam records no further write.
6. Report the selected ID and outcome after the operation completes → verify: the first invocation reports archival, the repeated invocation reports the already-archived state, and both return success.
7. Add the command to the existing help surface and update the README usage documentation → verify: help and docs describe one-ID archival, continued visibility, and repeat behavior consistently.

Keep production changes within command dispatch/handling and the existing item-update path where possible. Listing and link-resolution components are regression-test targets; the archive feature must not change their established semantics.

## Slice 2: Report invalid requests and storage failures

Complete the unsuccessful command paths and their preservation checks.

1. Validate exactly one ID using the existing parser conventions → verify: missing and extra arguments produce usage errors and leave all records unchanged.
2. Handle a missing ID through the existing error-reporting path → verify: an unknown ID produces a failure status and a diagnostic identifying it, with no changed items and no persistence call.
3. Propagate lookup failures without attempting an update → verify: an injected lookup error returns failure and produces no success output or update call.
4. Handle persistence failure before producing a success result → verify: an injected write failure returns failure, produces no success output, and leaves stored data consistent with the existing persistence guarantees.
5. Update error-path documentation in the README where needed → verify: documented outcomes match the command tests and do not suggest deletion, hiding, or automatic retries.

If storage investigation exposes data-corruption risks or an inability to preserve other fields, stop this slice and resolve the design mismatch. Do not silently expand the feature into a storage rewrite or make unverified atomicity claims.

## Acceptance matrix

| Scenario | Observable verification |
| --- | --- |
| Active ID | Exactly the selected archived flag changes; result reports success |
| Reload after success | Archived state survives reopening through the real storage mechanism |
| Existing or repeated archived ID | Success; identical record state; no further update |
| Ordinary list after archival | Target remains present and uses the existing archived marking |
| Link to archived target | Link resolves to the same stable ID and retained content |
| Unknown ID | Failure identifies missing ID; no item or store update |
| Missing or extra argument | Usage failure before mutation |
| Lookup error | Failure without update or success output |
| Persistence error | Failure without success output; established storage guarantees hold |
| Existing commands | Existing listing and editing regression tests remain green |

Use the runtime's existing test framework and runner. Record concrete focused and full-suite commands after source mapping; inventing commands before a language or harness exists would make this plan misleading. Tests must exercise the command and persistent state, with a write spy or equivalent existing seam where needed to prove repeated archival avoids another update.

## Assumptions

The runtime has reusable command dispatch, stable-ID lookup, an archived flag, local persistence, and listing/link behavior consistent with the README. Task 1 validates these assumptions and records the concrete integration map. See [design assumptions](./design.md#assumptions) for the individual checks.

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access, new archive metadata, and schema migration are outside this increment. The reasons are recorded in [the design](./design.md#not-doing).

## Rejected Alternatives

Confirmation prompts add an interaction absent from the chosen direction. Hiding breaks ordinary-list visibility; moving notes adds relocation and link risks. See [the decision](./design.md#alternatives-and-decision).

## Final verification and documentation

After both implementation slices are complete:

- Run the focused archive scenarios and the complete existing suite using `$kk:test` → verify: all acceptance-matrix rows pass, including listing, editing, and link regressions.
- Use `$kk:document` to check README/help accuracy and finalize relevant feature documentation → verify: behavior, constraints, integration references, and actual test commands match the implementation.
- Use `$kk:review-code` with the runtime's identified language → verify: actionable implementation findings are resolved or explicitly dispositioned.
- Use `$kk:review-spec` against all three planning documents → verify: the implementation satisfies the approved contract and task state is accurate.

These are future implementation tasks. The current request authorizes writing the plan only; it does not execute implementation, tests, or a follow-up review.
