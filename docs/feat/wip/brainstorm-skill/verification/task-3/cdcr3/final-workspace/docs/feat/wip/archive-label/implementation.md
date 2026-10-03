# Archive-label implementation plan

Status: pending. This plan documents future contributor work; no catalog change has been made.

See the [accepted design](design.md) and [tasks](tasks.md). The sole implementation target is repository-root `catalog.md`. No runtime code, dependency setup or generation pipeline is required. The supplied workspace contains only the accepted decision record, so the contributor must inspect the actual catalog before editing.

## Label edit

Deliver the full user-visible change as one small task, covering the catalog edit and its focused checks.

1. Locate `catalog.md` and inspect its existing archival markings before editing → verify: every entry can be classified as archived or active from the existing convention. If the file is absent or markings are inconsistent or ambiguous, block the task and ask catalog maintainers to resolve the classification; do not guess.
2. Record the pre-edit entry list, archive classifications, titles and destinations for comparison → verify: the baseline covers the complete catalog, including active entries. This is verification evidence, not a new generated artifact or automation system.
3. In `catalog.md`, append ` — Archived` immediately after each archived entry's existing link, outside its title; ensure there is only one label per archived entry → verify: compare against the baseline so every archived entry is labeled and every active entry has no label.
4. Inspect the complete catalog diff → verify: titles, destinations, entry count, order and visibility are preserved; the changes contain only archive-label text, with no style, dependency or generation changes.
5. Preview the Markdown using the project's existing viewer → verify: `Archived` appears beside each archived link, active entries have no label, and archived links remain clickable with their original destinations.

Use the baseline comparison and rendered inspection as the feature's acceptance checks. No test harness has been supplied, and this text-only change does not require creating one.

## Final verification

After the label-edit task is complete:

1. Invoke `/kk:test` for the full set of existing project checks → verify: record their actual results alongside the label acceptance checks. If no executable suite exists, record that fact and the manual evidence; do not claim tests ran.
2. Invoke `/kk:document` to assess relevant documentation → verify: any necessary updates describe the delivered text-only behavior and preserve color as an unresolved future decision.
3. Invoke `/kk:review-code` with Markdown as the project language/content input → verify: review covers `catalog.md` and any related implementation changes; resolve actionable findings within scope.
4. Invoke `/kk:review-spec` against these design and implementation documents → verify: all acceptance checks are satisfied and exclusions remain respected.
5. Update task status and record verification evidence → verify: no task is marked done without its checks, and the future color decision has not been reported as delivered.

These invocations are instructions for the implementation contributor. They have not been executed while drafting this plan.

## Assumptions

Authors already mark archived entries consistently. Validate this at the beginning of the label-edit task, because the intended target file is not available in the supplied workspace.

## Not Doing

Filtering would hide entries readers still need. Automatic archival would change maintainers' ownership of state. Color changes require a later contrast check and decision. Do not introduce dependencies or automate catalog generation.

## Rejected Alternatives

Hiding archived entries would prevent readers from finding needed links, so the accepted approach preserves visibility and adds text.

## Future work

Catalog maintainers own the color decision. They must check the site's contrast before choosing color; that work is separate from, and does not block completion of, this text-only increment.
