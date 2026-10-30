# Parcel client documentation handoff

Created: 2026-10-30T14:29:18Z.
Project: parcel-client. Source-machine checkout: `/tmp/handoff-eval.HQD6g3Xg/codex-prior-indexed-context/project`; branch `main`, revision `21650f9744ca726ca3c7c76606c8a861b321f9ac`. Remote repository identity is unknown.

## Objective and constraints

Finish Parcel client documentation. The user explicitly said not to implement or test anything yet. Documentation remains the active scope. The warehouse signage project is unrelated and excluded.

## Accepted decisions

- Make one attempt per submission until the service supports idempotency keys.
- Preserve the 20-second timeout.
- A timed-out submission may already have created a parcel. Repeating it can create a duplicate; a timeout does not establish that creation failed.
- The user rejected adding a queue because it expands scope without preventing duplicates.

## Progress and evidence

The agent read `project.md`, `retry-decision.md`, and `archive-excerpt.md`. The archive excerpt reports that the retry change is implemented locally and user documentation was pending; this is recorded evidence, not verified implementation status.

The agent updated `project.md` locally with a "Submission timeout and retries" section covering all accepted decisions above and links by filename to the two supporting documents. `git status --short` reports ` M project.md`. No implementation changes or tests were performed. No code review or test verification was conducted.

The gist transfers neither this uncommitted worktree change nor patches, credentials, or a Capy database. If the destination lacks the edit, the decision summary above contains the content needed to reconstruct the documentation.

## Continuation

Read the destination's relevant documentation and reconcile it with this recorded local edit. Determine whether the requested documentation is complete or needs placement/refinement, and continue only documentation work. Preserve the prohibition on implementation and tests until the user changes it. No known blocker; the destination checkout and availability of local changes are unknown. No conversation was lost to compaction in the available context; the full earlier archived conversation was not read, only its supplied excerpt.

## Supporting references

- `retry-decision.md`: accepted single-attempt policy, duplicate risk, and 20-second timeout. The user confirmed a prior successful Capy receipt indexed this specific file under source label `kk:arch-decisions`, project `parcel-client`, retrieval query `parcel retry idempotency`. Use that reference only if already available, to recover the accepted decision.
- `archive-excerpt.md`: supplied retrieved excerpt from the user-confirmed successful archive `archive-parcel-42`, project `parcel-client`. If available, retrieve that archive with a focused request for the Parcel retry discussion and the reason the queue was rejected. It establishes that a queue expands scope without preventing duplicates and records the claimed local implementation status.
- `project.md`: locally edited documentation described above.

The destination may not have the source machine's Capy database. These references are optional; essential facts are included here. Do not initiate indexing or archival to recreate them.
