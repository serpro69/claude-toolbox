# Archive labels in the static catalog

> Status: accepted design; implementation pending
> Audience: the next contributor and catalog maintainers
> Decisions: [accepted archive-label idea](../../../../accepted.md)
> Plan: [implementation.md](implementation.md) · [tasks.md](tasks.md)

## Purpose and planned behavior

Contributors need to recognize archived entries without opening every entry. Add the word **Archived** beside each archived entry in the manually maintained `catalog.md`. Active entries must have no label.

For example, a contributor scanning an archived entry will see its existing title, a clickable link to its existing destination, and the word Archived beside it. The entry remains visible. An active entry keeps its existing title and link without an archive label.

Success means every archived entry displays Archived and no active entry does. This document specifies a future edit; no catalog edit or runtime behavior is delivered by these design documents. There is no runtime application in this workspace.

## Accepted decisions and constraints

The problem framing, contributor persona, success condition, constraints, chosen direction, and design presentation are approved. This is a simple textual change to a static document.

- Preserve every existing title and destination.
- Keep archived entries visible and clickable.
- Change only the label text in this increment; introduce no dependencies or catalog-generation automation.
- Use the existing archive designation to identify entries, once its consistency has been verified. Do not infer archived status from a title or a broken link.

## Assumptions

Authors already mark archived entries consistently. Before editing, inspect `catalog.md` and verify that its existing markings distinguish archived entries from active ones. The catalog was not available for inspection during drafting, so its marking convention and entry inventory remain unverified.

If the convention is inconsistent or ambiguous, the implementing contributor must obtain clarification from the catalog maintainers before labeling affected entries. Record the issue and its next step in [Task 1](tasks.md#task-1-label-archived-entries).

## Not Doing

- Filtering: readers must retain access to archived entries and their links.
- Automatic archival: this increment only labels entries already designated archived in the manually maintained catalog.
- Color changes: this increment changes label text only; no color has been selected.

## Rejected Alternatives

Hiding archived entries was rejected because readers still need their links. A visible text label preserves that access while identifying archival status.

## Open color decision

Color is undecided and does not block the accepted text-only edit. Catalog maintainers own the next step: choose a color after checking the site's contrast. This is future work, not part of the implementation tasks below.

## Acceptance checks

Inspect the complete catalog after editing: every archived entry has Archived beside it, active entries have no label, and all original entries, titles, and destinations remain intact. Preview the rendered document to confirm labels are visible and archived links remain clickable. See the [implementation verification plan](implementation.md#final-verification) for the handoff checks.
