# Archive command implementation plan

> Status: pending implementation
> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)
> Evidence: [README.md](../../../../README.md)

## Starting point and implementation targets

The workspace has no runtime source or selected language. Do not treat the responsibilities below as existing files, functions, or tested capabilities. Before implementation starts, locate the actual note-tool repository and map these responsibilities to its concrete paths and symbols in this document. Selecting or building an entire runtime is outside this increment.

| Responsibility | Change or inspection required |
| --- | --- |
| Command registration and dispatch | Add the proposed `archive <id>` subcommand using existing command conventions; accept exactly one ID. |
| Note archive operation | Resolve the ID, return missing/already-archived outcomes, and apply the single-field transition for an active note. |
| Existing persistence boundary | Reuse lookup and update facilities; establish field preservation and failure behavior before relying on them. |
| Ordinary listing and link resolution | Preserve existing behavior; exercise both after archival. |
| Command and integration tests | Add isolated collection fixtures and assertions for the scenarios below using the existing test framework. |
| Runtime README or command help | Document syntax, repeated-command behavior, unknown-ID errors, and continued visibility using the actual executable name. |

The only existing source document here is `README.md`. Runtime files and executable test commands remain unresolved because they cannot be inferred from that document. Implementation must record this mapping before edits; this plan deliberately does not select a language, framework, or dependency.

## Single-note archive path

One implementation slice delivers the whole command, including error paths and preservation checks. The sequence below is internal to that slice, not separate horizontal-layer tasks.

1. Map the concrete command, lookup, persistence, listing, link, and test locations. Inspect conventions for identifiers, errors, and successful completion; confirm persistence can prevent partial updates. Record concrete file paths and focused test commands here. **Verify:** each responsibility maps to an actual symbol or explicit new component, and the persistence mechanism supports the design's preservation contract. Resolve any incompatible assumption before proceeding.
2. Establish a fixture with an active target, an archived note, an unrelated active note, and links to the target. Capture complete logical records, including additional fields supported by the runtime. **Verify:** existing ordinary listing includes all fixture notes with correct archived markers, and links resolve before any command runs.
3. Add command routing and the archive operation together. Validate exactly one ID, perform exact lookup using existing identifier rules, return successful completion without a write for an archived note, and update only the active target's flag. **Verify:** command-level checks distinguish a real transition from an already-archived no-op; reload persisted data and compare the whole collection against its prior state.
4. Implement failure reporting within the same path. Reject invalid argument counts before mutation, distinguish an unknown ID from a lookup error, and report write failures without claiming success. Use existing persistence safeguards rather than introducing a storage redesign. **Verify:** invocation and lookup failures make no writes; a simulated update failure leaves no partially applied change and returns failure.
5. Exercise ordinary listing and existing links after archival. Reuse existing behavior without introducing a new filter, location, or identity. **Verify:** the target remains visible with its archived marker, and every pre-existing fixture link resolves to the same ID and content.
6. Add runtime-facing usage and help documentation in the existing documentation location once it is known. **Verify:** examples use the real executable and agree with the tested command behavior; no example implies deletion, hiding, restore, or bulk support.

## Verification scenarios

Use the runtime's existing test framework and isolated storage. Do not test against an owner's real collection. A logical-state comparison allows existing physical storage encoding but must detect lost fields, altered links, or changes to other records.

| Scenario | Observable check |
| --- | --- |
| Archive one active ID | Successful completion; reloaded target has `archived = true`; every other target field and every other item is unchanged. |
| Repeat archival of the same ID | Successful completion; state exactly matches the state after the first command; persistence update is not invoked. |
| Archive a note already archived before the test | Successful completion without any state change or write. |
| Unknown ID | Missing-ID error and failed command outcome; all items unchanged; no update invoked. |
| No ID or multiple ID arguments | Invocation error and failed command outcome; no mutation attempted. |
| Similar titles or identifiers | Only the exactly resolved stable ID can change; the command does not select by title or fuzzy match. |
| Ordinary list after archival | All previously listed items remain listed; the target uses the existing archived marker. |
| Existing links after archival | Links still reach the same target ID, title, and body. |
| Additional runtime metadata | Fields beyond the README's minimum model remain unchanged. |
| Lookup failure | Operational error is distinguishable from an unknown ID; no mutation occurs. |
| Persistence failure | Failed command outcome and no success message; no partial state change or damage to another item. |

Keep tests focused on user-visible outcomes and data preservation. A storage-spy assertion is useful only for proving that repeated or rejected commands do not attempt an update. No benchmark, new testing dependency, or network access is needed.

## Final verification

After the implementation slice, run the focused command and integration checks, followed by the actual runtime's full suite. **Verify:** all acceptance scenarios pass and existing listing/editing behavior remains covered.

At that future implementation stage, use `$kk:test` for test verification, `$kk:document` for relevant documentation, `$kk:review-code` with the selected runtime language, and `$kk:review-spec` to check conformance to these documents. **Verify:** record real outcomes and resolve any findings before marking implementation done. These are future tasks; no follow-up review is authorized or executed by the present documentation request.

## Assumptions

The design assumes unambiguous stable-ID lookup, a field-preserving persistence update with failure safeguards, and listing/link behavior consistent with the README. Each must be checked against the eventual runtime. The current workspace cannot establish storage atomicity, command conventions, or test commands. Refer to [the design assumptions](./design.md#assumptions) for validation obligations.

## Not Doing

Deletion, hiding, moving notes, bulk operations, restore, synchronization, and new dependencies are excluded for the reasons in [design.md](./design.md#not-doing). No excluded capability is deferred into this task list. Choosing a language or creating a complete note tool is also outside this feature plan.

## Rejected Alternatives

The approved operation directly changes the existing flag. General editing is not the command contract because its suitability is unverified; compatible helpers may be reused internally. Hiding and relocation conflict with preservation requirements. See the [decision comparison](./design.md#rejected-alternatives).
