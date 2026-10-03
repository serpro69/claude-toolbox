# Archive-label implementation plan

Status: pending. This plan records the approved text-only increment; no implementation has been performed.

Read the [design](design.md) and [accepted decisions](../../../../accepted.md) first. Track execution in [tasks](tasks.md).

## Contributor context

The implementation target is the manually maintained root-level `catalog.md`. The provided workspace contains only the accepted decisions, so neither the catalog's layout nor its archive marker convention has been verified. Locate the catalog in the implementation checkout before beginning; do not create a replacement catalog from this plan. No application, package, or dependency changes are needed.

## Assumptions

Authors already mark archived entries consistently. Validate that assumption against the actual catalog and any existing authoring guidance before changing labels. If any status is ambiguous, obtain clarification from the catalog maintainers for those entries rather than inventing a classification rule.

## Label-edit slice

This is one small, complete catalog edit suitable for a single commit.

1. Inspect `catalog.md` and any existing guidance for the archive marker convention; inventory archived entries and record their current titles and destinations → verify: every target entry has an unambiguous archived status, and active entries are distinguishable under the same convention.
2. Edit `catalog.md` to put the plain word `Archived` beside each archived entry, outside its linked title; preserve existing titles, destinations, ordering, and visibility → verify: comparison against the inventory finds one label per archived entry and none on active entries, with titles and destinations unchanged.
3. Preview the catalog using the project's existing Markdown rendering method → verify: each label appears beside its intended entry, archived entries are still visible and clickable, and active entries remain unlabeled.
4. Inspect the final catalog diff → verify: the edit contains only the intended textual labels and necessary spacing; no color, filtering, archival logic, dependency, or generation changes appear.

If the repository supplies catalog validation checks, run the applicable checks and record their results. No such commands are established by the supplied source, so this plan does not invent a test runner. Do not add a new automated test framework for this label-only edit.

## Final verification

These actions are for the contributor after implementation; they have not been run during design drafting.

1. Invoke `/kk:test` for the Markdown catalog change, using the repository's applicable full suite if one exists and the acceptance checks in [design.md](design.md#acceptance-checks) → verify: record actual command results where available, plus the complete archived/active inventory comparison and rendered preview results.
2. Invoke `/kk:document` to update any relevant existing catalog authoring guidance and these feature documents as needed → verify: the written guidance reflects the implemented textual label and keeps the unresolved color decision separate. Avoid unrelated documentation expansion.
3. Invoke `/kk:review-code` with Markdown as the project language input and `catalog.md` as the implementation scope → verify: any findings about status coverage, links, titles, visibility, or scope are resolved or explicitly recorded.
4. Invoke `/kk:review-spec` against the design and implementation plan → verify: every acceptance check is satisfied, the assumption has been validated, and task status accurately records completed work.

## Scope and future edits

Filtering, automatic archival, color changes, generation automation, and new dependencies are excluded from this increment. Hiding archived entries was rejected because readers need their links.

Catalog maintainers own the future color choice. Their next step is to check the site's contrast before selecting a color. Completion of the text-only change does not imply that a color has been approved or implemented.
