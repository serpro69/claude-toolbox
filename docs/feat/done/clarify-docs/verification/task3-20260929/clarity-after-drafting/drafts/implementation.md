# Archive label implementation plan

Add a visible Archived label to each archived entry in `catalog.md`, preserving
existing links and titles. This plan is for the next contributor; no catalog edits
have been made. See the [accepted design](./design.md) for scope and rationale.

## Label edit

Target: `catalog.md`. It is not present in the supplied workspace, so the contributor
must obtain the maintained catalog before starting. No application code or new
dependency is required.

1. Inspect the existing archival marks and determine which entries are archived
   and which are active → verify: every entry's status can be determined from the
   authors' consistent markings. If that assumption fails, have catalog maintainers
   resolve ambiguous entries before editing; do not guess their status.
2. Add the word Archived beside each archived entry's link, outside its title,
   following the existing catalog format → verify: each archived entry displays
   Archived and each active entry has no archive label.
3. Inspect the diff and render the catalog using its existing viewing path →
   verify: original titles and destination strings are unchanged, archived entries
   remain visible and clickable, and the only feature change is label text. Inspect
   the link targets as well as their visible titles; a label must not replace a link.

No rendering command is prescribed because the catalog and its tooling were not
supplied. Use the maintained catalog's existing viewer and record how it was checked.

## Final verification

After the label edit, complete [Task 2](./tasks.md#task-2-final-verification).

- Invoke `/kk:test` for the full available suite and applicable edge cases → verify:
  record the actual checks and outcomes. If the catalog has no automated suite,
  report that limit and use the entry-by-entry rendered and diff checks above.
- Invoke `/kk:document` for relevant contributor documentation → verify: documentation
  describes the implemented text label and keeps color marked as undecided.
- Invoke `/kk:review-code` with Markdown as the language input → verify: review the
  catalog diff and address applicable findings.
- Invoke `/kk:review-spec` → verify: the implementation satisfies every accepted
  label, visibility, title and destination requirement without introducing excluded
  behavior.

These are future implementation checks. Drafting this plan does not complete them.

## Assumptions

Archival status is already marked consistently. Validate this before editing as
specified in [Label edit](#label-edit). The absent catalog prevents validation now.

## Not Doing

Filtering would hide entries readers still need. Automatic archival would change
the manual maintenance process. Color changes require a later decision by catalog
maintainers after checking the site's contrast. None is part of the label edit;
there is no task to automate catalog generation or add dependencies.

## Rejected Alternatives

Hiding archived entries would remove access to links readers still need, so the
accepted approach keeps entries visible and adds text beside them.
