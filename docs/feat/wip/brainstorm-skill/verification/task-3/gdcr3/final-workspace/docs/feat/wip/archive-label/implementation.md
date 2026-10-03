# Archive-label implementation plan

> Status: pending
> Design: [design.md](design.md)
> Tasks: [tasks.md](tasks.md)

## Contributor context

The target is the manually maintained root-level `catalog.md`. There is no runtime application to modify and no dependency to add. The approved source is [accepted.md](../../../../accepted.md). `catalog.md` was not supplied in the drafting workspace; obtain the actual catalog in the implementation checkout before starting. Do not create a replacement catalog or infer its structure from this plan.

## Label edit

Deliver one complete path: a contributor sees an archived entry's status while retaining access to its existing link. Keep inspection, label edits, and their acceptance checks in one small task.

1. Inspect `catalog.md` and its existing archive convention before editing → verify: record which entries are archived and which are active using that convention, and confirm it classifies entries consistently. Resolve missing or ambiguous status with the catalog maintainers before proceeding.
2. Capture existing titles and link destinations for comparison, then add plain `Archived` text beside each archived entry's title/link, outside the existing link text and within the same entry → verify: compare every archived entry with the initial set and confirm one visible label per archived entry, with no label on active entries.
3. Check the source diff and rendered Markdown using the project's existing preview, if available → verify: all original titles and destinations match, archived entries remain visible and clickable, and the label is clearly associated with the correct entry. Confirm there are no color, filtering, automation, or unrelated edits. If the project preview is unavailable, record that limitation and use an available Markdown preview without adding tooling.

No standalone test harness is needed for this manual text edit. Verification is an exhaustive comparison against the archive set and the original titles/destinations, plus a rendered-content check. Do not report site rendering as verified unless it was actually observed.

## Final verification

Run this after the label edit; the design-drafting session does not execute it.

1. Invoke `$kk:test` for the completed change → verify: the acceptance checks in [design.md](design.md#acceptance-checks) pass and any existing project test suite passes. If no suite exists, record that explicitly and report the catalog checks instead of inventing an application test command.
2. Invoke `$kk:document` to update relevant documentation → verify: the feature documents and task state accurately describe the delivered labels, preserve the scope exclusions, and keep the color decision unapproved and assigned to catalog maintainers.
3. Invoke `$kk:review-code` with project language input **Markdown**, scoped to the catalog edit → verify: review findings affecting label coverage, unchanged titles/destinations, or scope are resolved and rechecked.
4. Invoke `$kk:review-spec` against this design and plan → verify: all accepted behavior is accounted for, the archival-status assumption was checked, and no future color decision is represented as delivered.

## Assumptions and scope

The key assumption is consistent existing archive markers; validate it before labels are added. Filtering, automatic archival, and color changes are excluded for the reasons in [design.md](design.md#not-doing). Hiding entries was rejected because their links must remain accessible.

## Future decision

After checking the site's contrast, catalog maintainers choose a color. No color is selected here, and this decision is outside the two implementation tasks below; it is not a prerequisite for the accepted text labels.
