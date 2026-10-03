# Archive-label implementation plan

The [design](design.md) records the approved requirements; [tasks](tasks.md) tracks
execution. All implementation work is pending. The work has two small tasks: the
complete catalog edit and final verification.

## Context for the contributor

`catalog.md` at the repository root is the intended implementation file. It is
manually maintained Markdown, with no runtime application or new dependency needed.
It was not supplied in this workspace, so no entry list, marker syntax, rendering
command, or automated test command has been verified. Locate the real catalog
before editing; do not create a replacement from these planning documents.

## Assumptions

Existing archive markers classify entries consistently. Validate this against the
actual catalog before adding labels. Unclear classifications require resolution
with catalog maintainers, not an invented archival rule.

## Label edit

This is one complete user-facing slice affecting `catalog.md`.

1. Locate `catalog.md` and inspect its full entry list and existing archive markers
   → verify: identify the archived and active sets using a consistent existing
   convention. Resolve ambiguous entries before making the label edit.
2. Add `Archived` beside each archived entry, outside its existing link text; retain
   any already-correct label without duplication → verify: compare the resulting
   entries with the original classification; every archived entry has one label
   and every active entry has none.
3. Inspect the diff and render the Markdown using the project's existing preview,
   if available, or the normal catalog viewer → verify: titles and destination
   strings match the original, all entries remain visible, and archived links
   remain clickable. The diff should contain only label text edits.

Use the real catalog as the verification surface. Do not introduce a test harness,
generated catalog, dependencies, or a runtime application for this edit.

## Final verification

These are instructions for the future implementation phase; none are executed by
this design task.

1. Invoke `$kk:test` for the complete change → verify: repeat the full-catalog
   acceptance checks in [design.md](design.md#acceptance-checks), and run the
   project's existing applicable full test suite if one exists. Record the checks
   actually performed; no suite is established by the supplied workspace.
2. Invoke `$kk:document` → verify: any relevant documentation and task state reflect
   the completed label edit, while color remains undecided and separately owned.
3. Invoke `$kk:review-code` with Markdown as the project language/content input
   → verify: review the final diff for label completeness and preservation of
   titles, destinations, and visibility; resolve applicable findings.
4. Invoke `$kk:review-spec` → verify: the implementation satisfies the approved
   design and plan, and all task completion claims have supporting evidence.

## Not Doing

- Filtering: archived entries must remain accessible in the catalog.
- Automatic archival: authors continue maintaining archive status manually.
- Color changes: a separate future edit requires a contrast check and a maintainer
  color decision.

## Rejected Alternatives

Hiding archived entries would remove access to links readers still need, so the
accepted plan keeps entries visible and adds text beside them.

## Follow-up ownership

Catalog maintainers own choosing a color after checking the site's contrast. That
future edit is outside this implementation plan and has no approved color value.
