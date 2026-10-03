# Archive label implementation

> Status: pending
> Design: [design.md](./design.md)
> Tasks: [tasks.md](./tasks.md)

## Contributor context

This is a small edit to the manually maintained root `catalog.md`. The approved source is [accepted.md](../../../../accepted.md). No runtime application exists in this workspace, and the catalog itself was not supplied. The plan therefore names the target file without inventing entry names, archive-marker syntax or test commands.

## Assumptions

Authors consistently mark archived entries. Validate this before implementation using the catalog's existing indications, as described in [the design](./design.md#assumptions).

## Label edit

One small change delivers the complete contributor-visible behavior:

1. Obtain and inspect `catalog.md`, identify its archive indication and record archived versus active entries plus existing titles and destinations → verify: every entry has an unambiguous status and the inventory covers the complete catalog. Resolve missing files or ambiguous status with a catalog maintainer before proceeding.
2. In `catalog.md`, append plain text `Archived` immediately after each archived entry's existing link, once per entry → verify: every inventoried archived entry has exactly one label, active entries have none, and all existing archive indicators remain intact.
3. Compare the edit with the original catalog and render the Markdown using the project's existing preview, if available → verify: entry count, titles and destinations are unchanged; archived entries are visible and their linked titles remain clickable. If no preview is available, record that limitation and verify the preserved Markdown link syntax directly.

No automated tests need to be authored for this static label edit. The inventory, diff and rendered output provide direct checks of the accepted behavior.

## Final verification

After the label edit is complete:

1. Invoke `$kk:test` for the complete change → verify: all applicable existing checks pass, plus the archived/active inventory and link-preservation checks above. If no test suite exists, record that and the completed manual checks; do not invent an application test suite.
2. Invoke `$kk:document` → verify: relevant catalog documentation and this feature's task status accurately describe delivered text labels and preserve color as a future decision.
3. Invoke `$kk:review-code` with Markdown as the project-language input → verify: review covers the catalog diff and any resulting documentation changes; resolve actionable findings.
4. Invoke `$kk:review-spec` → verify: implementation satisfies the design's acceptance checks and does not add excluded behavior; resolve deviations before marking tasks done.

These are instructions for future implementation. No implementation, tests or independent review were performed while drafting this plan.

## Scope and future work

See [Not Doing](./design.md#not-doing) and [Rejected Alternatives](./design.md#rejected-alternatives) for the accepted boundaries and rationale. Color selection belongs to catalog maintainers after checking site contrast. It has no task in this increment and must not block completion of the text label.
