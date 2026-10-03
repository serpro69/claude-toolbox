# Archive label implementation plan

Status: pending; documentation only.

Read the [accepted design](design.md) and track execution in [tasks](tasks.md). The sole intended content edit is to the root `catalog.md`, which is not included in this planning workspace. No application code, dependencies, test framework, or generation machinery is required.

## Label archived entries

Deliver the complete visible behavior in one small task, including inspection and verification.

1. Inspect the actual `catalog.md` and its existing archive markers. Identify the archived and active entries before changing text → verify: every entry can be classified using a consistent existing convention. If any entry is ambiguous, obtain its status from catalog maintainers before editing it; do not invent a marker or classification rule.
2. Edit `catalog.md` to add the plain text `Archived` beside each archived entry's linked title, outside the link text and consistent with the existing layout. Keep titles, destinations, archive markers, and active entries intact → verify: compare the edited file with its pre-edit version; all archived entries have the label, active entries have none, and the only differences are the intended label additions.
3. Inspect the rendered `catalog.md` using the project's existing Markdown preview → verify: every archived label is visible next to its entry, archived links remain visible and clickable, and labels do not alter link titles or destinations. Check the actual link targets against the pre-edit version; an unavailable remote destination is not a reason to change it in this increment.

No new automated tests are needed for this reversible text edit. Source comparison and rendered inspection directly check its success condition without introducing tooling. Record the observed results when completing the task; do not mark checks complete from the plan alone.

## Final verification

After the label-edit task:

1. Invoke `/kk:test` for the Markdown catalog change → verify: the project's existing full test suite, if present, completes successfully, and the catalog acceptance checks in [design.md](design.md#acceptance-checks) pass. If no suite exists, record that fact and the source/rendered checks performed; do not invent a test command.
2. Invoke `/kk:document` for the completed change → verify: relevant existing contributor guidance reflects the manual label convention where needed, these feature documents accurately record implementation and verification status, and color remains a future maintainer decision. Avoid unrelated documentation changes.
3. Invoke `/kk:review-code` with `Markdown catalog content; no runtime language` as the project input → verify: review the `catalog.md` diff for unintended title, destination, visibility, or active-entry changes; resolve applicable findings.
4. Invoke `/kk:review-spec` for `archive-label` → verify: implementation matches the accepted behavior, exclusions, and acceptance checks in these design and implementation documents; resolve discrepancies before marking the feature done.

These are instructions for the implementing contributor. None of these skills or reviews has been run during drafting.

## Assumptions

The existing archive markers consistently distinguish archived entries from active entries. The first inspection step validates this assumption before editing. The catalog's absence here means its exact formatting and marker syntax remain unverified.

## Not Doing

- Filtering: readers retain access to archived entries.
- Automatic archival: status remains manually maintained.
- Color changes: this increment changes label text only.

## Rejected Alternatives

Hiding archived entries would prevent readers from accessing their links in the catalog, so it is not part of the implementation.

## Future color work

After this increment, catalog maintainers may choose a color after checking the site's contrast. No color is selected in this plan, and no color task blocks the text label.
