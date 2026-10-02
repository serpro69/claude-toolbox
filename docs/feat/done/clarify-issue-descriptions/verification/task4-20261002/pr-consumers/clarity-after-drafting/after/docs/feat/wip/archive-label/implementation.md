# Archive-label implementation plan

> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)
> Status: pending; this document plans the work

## Contributor context

The only implementation target is the manually maintained `catalog.md`. There is no runtime application or new dependency to build. This plan is based on [accepted.md](../../../../accepted.md); the catalog's contents and any existing validation commands were not available during drafting.

## Label edit

Deliver the complete visible-label change in one small task.

1. Locate `catalog.md` and identify the author-maintained convention for archival status before editing → verify: every entry can be classified as archived or active without guessing. If an entry is ambiguous, resolve it with catalog maintainers before labeling it.
2. Add the plain word `Archived` beside each archived entry's existing link, outside its link text → verify: every archived entry has the label, active entries have none, and the diff preserves every existing title, destination, and entry.
3. Inspect the catalog in its normal rendered Markdown presentation → verify: labels appear beside the correct entries, all entries remain visible, and links retain their original clickable destinations. Confirm there are no color or styling changes.

Use an entry-by-entry comparison against the verified archival convention as the primary acceptance check. No new runtime tests or generation tooling are needed for this manual text edit.

## Final verification

After the label edit is complete, perform the following contributor checks. These are future implementation tasks, not checks performed while drafting this plan.

1. Invoke `/kk:test` for the catalog change → verify: the full applicable existing validation suite passes, if one exists, and the entry-by-entry and rendered checks above pass. If no automated suite exists, record that fact alongside the manual results; do not invent a command or add a suite for this edit.
2. Invoke `/kk:document` to update relevant catalog guidance, if present → verify: any guidance about the label matches the accepted text-only behavior, and color remains recorded as undecided.
3. Invoke `/kk:review-code` with Markdown as the project language/content input → verify: the catalog diff satisfies the acceptance checks and any actionable findings are resolved.
4. Invoke `/kk:review-spec` → verify: the finished catalog and task state agree with the design and this plan, including the scope exclusions.

## Assumptions

Archived entries already have consistent author-maintained markers. The first step validates this before any label is added. Actual catalog formatting and validation tooling remain to be inspected in the implementation checkout.

## Not Doing

- Filtering: entries and their links must remain available.
- Automatic archival: maintainers continue to determine archival status.
- Color changes: catalog maintainers will choose a color after checking the site's contrast; that future work is outside this plan.

## Rejected Alternatives

Hiding archived entries would remove access that readers still need. Preserve them and add the accepted textual label instead.
