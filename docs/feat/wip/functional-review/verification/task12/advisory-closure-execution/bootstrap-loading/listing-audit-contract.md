# Verification-only correction for instruction filename discovery

On 2026-10-18 both explicitly authorized Claude bindings completed with exit 0.
Baseline passed the original auditor. Candidate's complete instruction Reads
include all eight previously missing detection files; the original auditor stops
on two successful Glob calls listing selected-plugin instruction filenames.
[The original failure](original-audit-failure.json) and all capture bytes remain
unchanged. No actor is rerun and no capture is relabeled with new runtime code.

Independent `/kk:review-code:isolated` assessment classified those calls as
contract-allowed metadata operations: the frozen prompt requires direct Reads
for instruction bytes but does not prohibit instruction filename discovery, and
the frozen transport permits Glob. The reviewer identified a P2 auditor defect
at its blanket rejection of every other tool. This correction changes verifier
classification, not actor inputs, permissions, expected receipts or acceptance.

## Narrow acceptance and retained provenance

The successor auditor preserves the original Claude audit procedure and adds one
branch for Glob. Only the exact patterns `agents/*.md` and
`skills/{_shared,review-code}/*.md` are supported, with the explicit base equal to
the launch's selected plugin root. Require a successful paired result, affirmative
complete-count metadata, no truncation, matching text/metadata filenames and
counts, distinct normalized paths in the pattern's permitted instruction
directories, and existing files contained by the frozen instruction snapshot.
Reject traversal, other bases/patterns, subject/evaluator locations, missing or
inconsistent results and other unexpected tools. This narrow verifier need not
support every possible safe Glob. No listing counts toward a required Read.

Return listing call/result IDs, actor, pattern and source-relative paths as
separate audit provenance. Keep the original required parent/child inventory,
byte-completeness, named-child linkage, model/service/root checks and shell-access
review unchanged. Original successful baseline audit stays byte-identical;
candidate receives a new audit only after independent source review and freeze.

## Separate verifier identity and completion

`listing_guard.py` is the successor entry point. Its separate `verifier-freeze.json`
pins its code, auditor, tests and this declaration, and binds the actual bootstrap
execution freeze `4a0c926f6af7a70e5b12fc175e670b7d68715ccb0295d8a94b8ba2dd7ebecdec`.
Recompute both sealed captures and compare retained audit content before the
original review/calibration/state/retention gate. Preserve exact-prompt, effort
telemetry and confinement limits. Existing audit files can only be validated,
never overwritten. Every required source/model/effort/access check remains.

Tests must show the actual candidate passes only the new metadata classification,
the baseline result is unchanged, and missing required Reads still fail. Include
outside/traversal/evaluator paths, unsupported tools, failed/truncated/unpaired
results, mismatched counts and changed verifier dependencies. Source review
precedes freeze and revised audit. Independent final evidence review and a
successful strict guard are required before closing 12.21.4. Calibration and
actor captures retain their original identities; no behavioral grade changes.
