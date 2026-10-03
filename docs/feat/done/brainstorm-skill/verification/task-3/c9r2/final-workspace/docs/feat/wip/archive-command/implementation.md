# Implementation plan: Archive command

> Status: pending; target runtime source required
> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)
> Source: [README.md](../../../../README.md)

## Starting point and source mapping

Only README.md describes the note tool in this workspace. No language, executable name, implementation files, storage backend, or test runner has been selected. Do not treat the component names below as existing files, and do not create an entire note application to satisfy this feature plan.

Before changing runtime code, obtain the actual note-tool source and record the concrete files and entry points for these responsibilities in this plan and the task subtasks:

| Responsibility | Required integration |
| --- | --- |
| CLI command registration and argument handling | Register `archive <id>`, require exactly one valid ID, and follow existing output and exit-status conventions |
| Note lookup | Resolve the established stable ID; distinguish absence from a storage error |
| Note mutation | Change only the selected note's archived flag |
| Persistence | Save the update safely and report success only after confirmed persistence |
| Ordinary listing and editing | Preserve inclusion, archived marking, IDs, and links |
| Tests and fixtures | Exercise the real command against isolated local collections, including storage failures |

Step → verify: inspect the target source and fill in this mapping with real paths and relevant test commands. If source remains unavailable, keep implementation blocked; do not invent paths or a language.

## Archive one note end-to-end

Extend the existing CLI registration and handler for the proposed subcommand. Reuse the tool's ID parser, lookup path, error conventions, and storage access. Avoid creating a second note model or archive store.

Create a focused command test using an isolated collection with an active selected note, another note, and links to the selected note. Establish expected output and storage state before implementing the handler.

After successful lookup, prepare and persist the selected note with its archived flag set to true. Leave its ID, title, body, links, and all other notes untouched. Report success only after the storage boundary returns success.

Step → verify: execute the command test and reopen the collection. Check that only the selected flag changed, the success result identifies its ID, and no note body is printed.

For an already archived note, return success without modifying the collection. This is a no-op, not an error.

Step → verify: run the command twice against the same note, compare all persisted note fields after each invocation, and verify that the second invocation does not request another write.

## Preserve access and existing behavior

The existing listing path already includes archived notes according to the README. Retain that policy and its distinct archived marker. Preserve the selected note's identity so existing links and editing continue to work.

Use regression tests before making any listing or editing changes. If the target code contradicts the README, identify and resolve that mismatch explicitly within these requirements; do not silently hide, move, or duplicate notes.

Step → verify: archive a linked note, run the ordinary list command without special flags, and confirm the note remains visible and marked archived. Follow the existing link-resolution and editing paths and confirm stable IDs, preserved links, and no unintended unarchive operation.

## Handle invalid requests and storage failures

Reject missing IDs, extra positional arguments, and IDs invalid under the established grammar before any write. Report a well-formed unknown ID as not found. Preserve the distinction between a missing item and a failed collection read.

Step → verify: command-level tests for each rejected input assert a nonzero status, an appropriate diagnostic, and an unchanged collection.

Inspect the persistence boundary before choosing a failure-safe update mechanism. Use the backend's existing safe-update facility if it provides the required guarantee. The plan deliberately does not select a file-replacement algorithm or database transaction before the storage backend is known.

Step → verify: inject a read failure and a save failure using the actual storage test seam. Assert a nonzero status, no success message, and an intact collection that can be reopened. If partial writes are possible, add an interruption test at the relevant boundary and address it before shipping.

## Assumptions

Carry forward the design's testable assumptions: IDs are unique, storage can safely update a flag, and listing and editing match the README. Validate them while mapping the source and through the tests above. If an assumption fails, revise the affected design detail before implementation continues.

## Not Doing

Bulk archival, restoration, synchronization, dependencies, and network access are excluded for the reasons recorded in [design.md](./design.md#not-doing). Building the underlying note tool is also outside this addition; obtaining its source is an implementation prerequisite.

## Rejected Alternatives

Hiding or moving notes violates preserved visibility and access. A separate archive record adds a consistency boundary without user value for this increment. Follow the [direct flag-update design](./design.md#rejected-alternatives).

## Final verification and documentation

Update the target tool's CLI help and user documentation with the final executable syntax, preserved list visibility, repeated-command behavior, and missing-ID handling. Keep examples focused on one note.

Step → verify: run the documented archive example against an isolated collection, compare help text with actual argument behavior, and confirm the note remains visible afterward.

After the feature is implemented, use `/kk:test` for the target project's full suite and the feature checks above; `/kk:document` for relevant documentation; `/kk:review-code` with the actual implementation language; and `/kk:review-spec` against these three documents. These are future tasks, not reviews or implementation authorized by the current documentation request.

Step → verify: record actual test commands and results, reconcile actionable review findings, and check every acceptance criterion before marking the feature complete. No such execution has occurred in this planning workspace.
