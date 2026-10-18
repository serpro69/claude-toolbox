# Closure candidate rollback

> Task 12.23 · 2026-10-18 · Complete; verification passed; independent review APPROVE

[Independent review](review.md) approves the bounded rollback with no remaining
findings. The saved patch's final context line was corrected during review.

The user explicitly requested reverting the rejected closure candidate. The
[rollback patch](rollback.patch) restores only the standard and isolated closing
instructions in `klaude-plugin/skills/review-code/` and their generated Codex
copies. All four files byte-match source parent
`11b2c6efb0638605bb6acd3eb184edb9abd10f56`.
The broader functional-review implementation remains in place.

The rollback restores the preceding clean-review closure and supported-action
wording. It removes this candidate's explicit separate-follow-up clause. The
common functional method, instruction-loading order, evidence limits, authorization
rules and other review behavior remain outside the reverted patch.

## Verification

[Source verification](source-verification.json) and [check results](verification.json)
record:

- Exact source-parent equality for all four operative files; the frozen candidate
  patch also passes a forward dry-run check against the restored tree. The saved
  rollback patch matches exact Git diff bytes and passes a reverse-apply dry run.
- `make generate-kodex`: generator tests and all 252 structure assertions pass
  with Python 3.12.11. A second generation leaves all 958 generated file/link hashes
  identical, with no generated-agent changes.
- `make plugin-graph`: Go tests pass; no broken edges or orphans. Its cycle warning
  is nonfatal.
- `git diff --check`: passes.

[Generation output](generation.log) and [graph output](graph.log) retain the
successful executions. Earlier environment failures are recorded separately in
the check results: protected generated output required granted write access,
the default Python 3.10 lacked a TOML parser, and graph compilation needed a writable
temporary Go cache. No repository workaround or dependency change was introduced.

## Evidence and scope

The original [candidate patch](../advisory-closure/candidate.patch),
[source provenance](../advisory-closure/source-provenance.json), comparison
captures, grades and seals remain unchanged. The comparison seal also references
four mutable feature handoffs. Their exact completion-time bytes were archived
under `handoff-before/` before live status updates.
[Handoff provenance](handoff-provenance.json) binds those copies to the unchanged
original seal. All 35 original hashes still verify using 31 original artifacts
and the four archived handoffs; the old seal does not hash the newly edited live
handoffs.

Profile: skill-md, activated by the nearest-ancestor SKILL.md for all four operative
files. Universal, Claude Code and kk-specific implementation/review guidance
was loaded. No dependency, description, naming or runtime configuration changes.
PAL remains deferred. This rollback neither claims behavioral improvement nor
changes the comparison's REJECT disposition. Original Task 12 acceptance and
Task 13 remain open; no actor rerun or next wording experiment is selected.

The source rollback was exact and small. Most ancillary work preserved historical
handoff hashes and resolved test-environment limitations; it did not expand the
operative change.
