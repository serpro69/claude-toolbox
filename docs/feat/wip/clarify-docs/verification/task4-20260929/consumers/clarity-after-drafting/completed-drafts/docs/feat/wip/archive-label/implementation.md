# Archive-label implementation plan

> Status: planned; no implementation performed
> Contract: [design.md](design.md)
> Execution: [tasks.md](tasks.md)

## Scope and starting point

The contributor will edit `catalog.md`, the manually maintained static catalog, to put Archived beside entries already designated archived. Preserve titles, destinations, entry visibility, and clickability. Active entries receive no label. No dependency or generation tooling is needed.

The accepted decisions establish this contract. Catalog content and its archive-marking convention were not supplied for inspection; the first step below must establish which entries qualify before any label edit. No application code or runtime tests are involved.

## Label archived entries

This is one small, complete edit to `catalog.md`, including its verification.

1. Inspect the existing archive markings in `catalog.md` and identify all archived and active entries → verify: every entry can be classified using a consistent existing convention. If not, record the ambiguity in Task 1 and ask the catalog maintainers to resolve it before labeling affected entries.
2. Add the word Archived beside each archived entry's existing link, preserving the link title and destination and leaving active entries unlabeled → verify: compare every entry against the classification from step 1; archived entries all display Archived and active entries have no label.
3. Inspect the diff and preview `catalog.md` in the site's existing Markdown rendering workflow, if available → verify: no entry was hidden or removed, every original title and destination is unchanged, labels are visible, and archived links remain clickable. If the site's rendering workflow is unavailable, record that limit and use an available Markdown preview without claiming site rendering was verified.

These checks validate a static document edit. Do not add generation scripts or an automated test suite for the label change.

## Assumptions

The plan depends on authors marking archived entries consistently. Step 1 validates this before implementation. Catalog maintainers resolve ambiguous archival status; the contributor records the outcome in Task 1.

## Not Doing

Filtering would interfere with continued access to archived entries. Automatic archival exceeds the manual label edit. Color changes await the maintainers' contrast check and color decision. None belongs in this increment.

## Rejected Alternatives

Hiding archived entries was rejected because their links must remain available. Preserve the visible catalog and add textual labels.

## Final verification

After the label edit, run `/kk:test` to perform applicable repository checks and the complete catalog checks above. Run `/kk:document` to update relevant documentation, `/kk:review-code` with Markdown as the change's language input, and `/kk:review-spec` to compare the result with this plan and the design → verify: record actual results and any unavailable checks in Task 2 before marking it done. Do not claim a runtime or full-suite test passed when none exists or was run.

The post-design recommendation is `/kk:review-design archive-label`. It has not been run as part of drafting. Implementation and final verification remain future actions.
