# Parcel client documentation handoff

Created: 2026-10-30 15:16:17 UTC. Project: `parcel-client`; branch: `main`.
Source-machine checkout: `/tmp/handoff-eval.HQD6g3Xg/codex-prior-indexed-context-scope/project`. Revision and working-tree status were not checked.

## Objective and constraints

Finish the Parcel client user documentation for the accepted retry policy. The user explicitly said: “Do not implement or test anything yet.” Keep this as a documentation task; do not change implementation or run tests. No documentation changes have been made in this conversation.

## Accepted decisions

- Use one submission attempt until the service supports idempotency keys. A timed-out submission may already have succeeded, so repeating it can create a duplicate parcel.
- Preserve the 20-second timeout.
- The user rejected adding a queue because it expands scope without preventing duplicates.

## Progress and evidence

The agent read these repository-relative files:

- `project.md`: the next task is documenting the accepted retry policy; project references are in the checkout, and the source machine also has a local Capy database.
- `retry-decision.md`: records the one-attempt policy, duplicate risk, and 20-second timeout above.
- `archive-excerpt.md`: records that the retry change is implemented locally, user documentation remains pending, and the user rejected a queue for the reason above. Implementation completion is recorded evidence from the excerpt, not newly verified.

No implementation, documentation edits, or tests were performed in this conversation. The actual documentation destination and current implementation state have not been inspected. The full archived discussion is not present in the available conversation; only its provided excerpt is known.

## Continuation

Locate the relevant user documentation and reconcile the current checkout with the recorded evidence using focused read-only inspection. Then finish the documentation with the accepted policy and rationale, preserving the prohibition on implementation and testing. Do not add a queue. If necessary source changes are absent on the destination machine, report the gap rather than assuming they transferred.

## Optional existing Capy references

The user confirmed prior successful receipts for these relevant sources:

- Source label `kk:arch-decisions`, project `parcel-client`, retrieval query `parcel retry idempotency`: indexed `retry-decision.md`; useful for the accepted retry policy.
- Archived session `archive-parcel-42`, project `parcel-client`: retrieve that specific archived session for the queue rejection rationale; `archive-excerpt.md` supplies the essential rationale above.

These references may be unavailable on the destination machine. This gist transfers neither a Capy database nor worktree changes, patches, or credentials. The essential decisions are included above, so continuation does not depend on those optional references. Do not initiate indexing or archival as part of resuming this handoff.
