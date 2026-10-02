# Archive-label tasks

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Status: in-progress
> Not Doing: filtering, automatic archival, color changes

## Task 1: Inspect existing archive state

**Status:** done
**Depends on:** —
**Size:** S
**Can run in parallel with:** —

- [x] Verify catalog.md marks archived entries consistently.

## Task 2: Add text labels

**Status:** pending
**Depends on:** Task 1
**Size:** S
**Can run in parallel with:** —

- [ ] Add Archived labels following [the plan](implementation.md) → verify: archived entries retain their titles and links; active entries stay unchanged.

## Task 3: Final verification

**Status:** pending
**Depends on:** Task 2
**Size:** S
**Can run in parallel with:** —

- [ ] Run /kk:test, /kk:document, /kk:review-code and /kk:review-spec → verify: checks pass and documentation matches the label contract.

## Dependency Graph

```text
Task 1 → Task 2 → Task 3
```
