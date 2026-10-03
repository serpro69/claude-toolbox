# Archive labels in the static catalog

## Status and source

The requirements, refinement choices, and design presentation are approved in
[accepted.md](../../../../accepted.md). These documents prepare the work for the
next contributor; implementation and independent review have not been performed.
See [implementation.md](implementation.md) for the edit procedure and
[tasks.md](tasks.md) for pending work.

## Problem and success condition

The catalog maintainer wants contributors to identify archived entries without
opening each entry. Every archived entry must display the word `Archived` beside
it; active entries must have no archive label. Archived entries remain visible and
clickable, with their existing titles and destinations preserved.

## Current context

The accepted source describes a manually maintained root-level `catalog.md`.
There is no runtime application in this workspace. At drafting time, only
`accepted.md` was supplied: `catalog.md`, its entry format, and its archive markers
could not be inspected. The implementation must use the actual catalog and verify
its markers before editing; this document does not infer which entries are archived.

## Accepted design

Make a direct Markdown text edit in `catalog.md`. Add the literal word `Archived`
adjacent to each entry identified as archived by the catalog's existing convention.
Place it outside the entry's link text so the title and destination remain intact.
Use consistent placement compatible with the catalog's actual layout. Existing
archive labels, if any, must not be duplicated.

Keep the existing entries and their links visible. Active entries receive no
archive label. This increment adds no styling, dependencies, generation process,
filtering, or automatic archival behavior.

## Assumptions

Authors already mark archived entries consistently. Before implementation, inspect
the entire catalog and confirm that its existing markers identify archived entries
unambiguously. If markers conflict or are absent, resolve the affected entries with
the catalog maintainers before labeling them; do not guess from entry age or title.

## Not Doing

- Filtering: readers must continue to see and open archived entries.
- Automatic archival: this is a manually maintained catalog and a label-only edit.
- Color changes: no color has been approved for this increment.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need access to their
links. A visible textual label communicates status while retaining access.

## Future edit: color

Color is undecided and is not an accepted implementation requirement. The catalog
maintainers own the next step: check the site's contrast and then choose a color.
This follow-up does not block the accepted text-only label edit and is not a task
in this increment.

## Acceptance checks

- Every entry identified as archived has one visible `Archived` label beside it.
- Active entries have no archive label.
- Original titles and link destinations are unchanged; archived links remain
  visible and clickable in the rendered catalog.
- The diff contains only the intended label text edits, with no color or automation
  changes.
