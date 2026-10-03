# Tasks: Archive label

> Design: [design.md](./design.md)
> Implementation: [implementation.md](./implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, catalog generation, color changes, new dependencies

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label edit](./implementation.md#label-edit), [Acceptance checks](./design.md#acceptance-checks)

### Subtasks

- [ ] 1.1 Obtain and inspect root `catalog.md`; inventory archived and active entries using the existing archive indication → verify: all entries have an unambiguous status, and baseline titles and destinations are recorded. Resolve missing catalog or ambiguous status with a catalog maintainer before editing.
- [ ] 1.2 Add plain text `Archived` immediately after each archived entry's existing link in `catalog.md` → verify: exactly one label per archived entry, no label on active entries, and existing archive indicators preserved.
- [ ] 1.3 Compare the complete catalog against the baseline and inspect rendered Markdown where a preview is available → verify: entry count, titles and destinations are unchanged; archived entries stay visible and clickable; no color, filtering or automation changes appear. Record any preview limitation and inspect link syntax directly.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](./implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `$kk:test` for the complete change → verify: applicable existing checks pass and all archive-label acceptance checks are recorded; if no suite exists, record the manual checks instead.
- [ ] 2.2 Invoke `$kk:document` → verify: relevant documentation and task status match the delivered text label; color remains a future maintainer decision after checking site contrast.
- [ ] 2.3 Invoke `$kk:review-code` with Markdown as the project-language input → verify: the complete implementation diff is reviewed and actionable findings are resolved.
- [ ] 2.4 Invoke `$kk:review-spec` → verify: implementation matches the accepted design and plan, including preserved titles, links and visibility; resolve deviations before marking tasks done.

## Dependency Graph

```text
Task 1 ──→ Task 2
```
