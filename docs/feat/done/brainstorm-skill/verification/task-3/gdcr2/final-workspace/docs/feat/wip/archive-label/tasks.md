# Tasks: Archive labels

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: pending
> Created: 2026-10-03
> Not Doing: filtering, automatic archival, color changes

Requirements and the design presentation are approved. No implementation or
independent review has run. `catalog.md` was not supplied in the drafting workspace;
the implementing contributor must locate it and validate the archive markers first.

## Task 1: Label archived catalog entries

- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Label edit](implementation.md#label-edit)

### Subtasks

- [ ] 1.1 Locate root-level `catalog.md` and inspect all existing archive markers
  → verify: archived and active entries can be classified consistently. Resolve
  any ambiguity with the catalog maintainers before labeling.
- [ ] 1.2 Add one visible `Archived` label beside each archived entry in
  `catalog.md`, outside its link text → verify: every archived entry is labeled,
  active entries have no archive label, and labels are not duplicated.
- [ ] 1.3 Inspect the diff and rendered catalog → verify: original titles and
  destination strings are unchanged, archived entries remain visible and clickable,
  and the diff contains only label text changes.

## Task 2: Final verification

- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#final-verification)

### Subtasks

- [ ] 2.1 Invoke `$kk:test` → verify: complete the full-catalog acceptance checks
  and any existing applicable full test suite; record actual results without
  inventing a suite or introducing a harness for this edit.
- [ ] 2.2 Invoke `$kk:document` → verify: relevant docs and task state describe the
  completed text-only behavior and retain the separate, undecided color follow-up.
- [ ] 2.3 Invoke `$kk:review-code` with Markdown as the project language/content
  input → verify: resolve applicable findings on the completed catalog diff.
- [ ] 2.4 Invoke `$kk:review-spec` → verify: implementation conforms to the approved
  design and implementation plan, with evidence for completed tasks.

## Dependency Graph

```text
Task 1 ──→ Task 2
```

Color is future work owned by catalog maintainers: check the site's contrast, then
choose a color. It is not a dependency or task in this increment.
