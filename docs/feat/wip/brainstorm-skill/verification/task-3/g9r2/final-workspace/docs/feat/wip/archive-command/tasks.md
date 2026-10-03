# Tasks: Archive command

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: deletion, hiding, moving notes, bulk operations, restore, synchronization, new dependencies, network access

## Task 1: Archive one note end-to-end

- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Archive command end-to-end](./implementation.md#archive-command-end-to-end), [command contract](./design.md#command-contract)
- **Prerequisite:** Runtime source must be available. This planning workspace contains only README.md; map actual component paths before coding. Size estimates the bounded command/operation/test change and must be reassessed if source inspection exposes wider work.

### Subtasks

- [ ] 1.1 Identify the command parser, item lookup, archived field, persistence boundary, list renderer, link resolver, and existing test runner. Record actual paths and the relevant test command in the implementation notes below. Verify they support the README's stated behavior.
- [ ] 1.2 Add command/collection test cases for active, already archived, missing-ID, invalid-argument, lookup-failure, and persistence-failure paths. Verify they fail on absent archive behavior before implementing it.
- [ ] 1.3 Register `archive <id>` in the command parser and implement the dedicated archive handler. Require one ID, set only its flag, and skip saving for already archived or missing items. Verify collection snapshots preserve every other field and item.
- [ ] 1.4 Connect the handler to existing persistence and error output. Verify successful saves precede success output and lookup/save failures report errors without a success message or unrelated-data corruption.
- [ ] 1.5 Exercise archival through the ordinary list and existing link resolver. Verify retained visibility, archived marking, stable links, and identical collection state after repeat archival.
- [ ] 1.6 Update README.md and existing command help in the runtime project. Verify their examples match the actual invocation and describe idempotence, missing-ID failure, and retained visibility.

### Implementation notes

Runtime paths, language, and executable checks are unresolved until the implementation project is available. Record discovered details here during Task 1; do not invent them from the planning README.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](./implementation.md#final-verification), [acceptance and verification](./design.md#acceptance-and-verification)

### Subtasks

- [ ] 2.1 Invoke `$kk:test` to run the runtime project's full test suite and verify the archive acceptance scenarios, including repeat/missing-ID no-write behavior and storage errors. Record commands and outcomes.
- [ ] 2.2 Invoke `$kk:document` to check and update relevant implementation documentation, including README.md and command help; verify the text matches actual behavior.
- [ ] 2.3 Invoke `$kk:review-code` with the runtime project's actual language to review the implementation; resolve findings that affect the approved contract.
- [ ] 2.4 Invoke `$kk:review-spec` to compare implementation with design.md and implementation.md; resolve deviations and record remaining limitations before marking the feature done.

These tasks describe future implementation work. No code implementation or follow-up review is part of the current document-writing request.

## Dependency Graph

```text
Task 1: Archive one note end-to-end
                 |
                 v
Task 2: Final verification
```
