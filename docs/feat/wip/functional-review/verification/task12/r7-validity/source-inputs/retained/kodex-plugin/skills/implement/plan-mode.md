# Plan Mode

Applies when the user references a docs/feat/wip feature or task number.

## Entry Procedure

After the basic instructions in SKILL.md load, collect only minimal task/file metadata to drive profile detection. Full document reading, knowledge search and requirement/source analysis belong to the common investigation phase.

1. Locate the feature's `tasks.md`, `design.md` and `implementation.md` through file listings.
2. Extract only task headings, status/dependency fields and candidate target filenames to select the requested/next ready task and its profile inputs; include diff filenames when resuming. Do not open full documents or analyze requirement prose here. If target metadata is insufficient, start with a conservative candidate file list from the affected directories, then refine it after instruction loading.

**Knowledge sources for the common investigation phase:** `kk:arch-decisions`, `kk:project-conventions`, `kk:lang-idioms`, and `kk:review-findings`. Search for each task, however small; an empty result is normal. The common phase reads the complete feature documents before implementation, including intended outcomes, preserved behavior, delivery requirements and prior accepted decisions.

Explicit behavioral conditions in the task list and implementation plan are commitments too. Do not demote them to optional suggestions merely because a design document names another hard requirement. Without an existing accepted decision settling a conflict, keep both conditions visible, propose alternatives and wait for the user's resolution under the common investigation procedure.

After completing the entry procedure, return to SKILL.md Step 2 (Execute).

## Execution context and specification integrity

The common investigation phase records observations in a labeled **Execution context** subsection of the current task in `tasks.md`. Each material observation or action includes its date, status (observed, inferred, unresolved, proposed or explicitly accepted), source location/revision and relevant evidence limits. Record verification, review outcomes and permitted follow-up there as they occur; each deferred action needs an owner (or unassigned), reason, next action and verification condition.

On resume or after fixes, refresh against current state. Correct or supersede an old observation with a dated source-backed note, preserving its provenance. Do not silently rewrite `design.md`, `implementation.md` or acceptance criteria to fit the code. An observation is not an accepted decision. A requirement change or exception needs explicit user authorization, recorded with its source, rationale and prerequisites before dependent work proceeds. Use the existing document format; do not create a parallel task system.

## Iteration

After each execution + review cycle (SKILL.md Steps 2–3):

- Verify the completed task's **Required Outputs** are all checked
- Move to the next ready task in `tasks.md` only within the user's requested scope; a request for one task ends after its execution/review cycle
- Return to the Entry Procedure above to load context for the new task
- Repeat until all tasks are completed

## Completion

After all required feature tasks and acceptance gates are complete and verified (not merely the current requested task):

- Use `$kk:test` skill to verify and validate functionality
- Use `$kk:document` skill to create or update any relevant docs
- **Reflect:** briefly note where the implementation diverged from the plan, what turned out harder or simpler than expected, and any surprises that future work in this area should know about. Keep it short — a paragraph, not an essay. Index non-obvious learnings as `kk:project-conventions` or `kk:arch-decisions` if they weren't already captured during per-task cycles.
- Update the feature status in `tasks.md` header to `done`
