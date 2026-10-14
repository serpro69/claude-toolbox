# Task 12.14: R7 validity audit

Audited 2026-10-14 before successor measurements; starting source `6bc277ea`.
Historical observations and grades remain unchanged.

## Fixture evidence

The original `functional-missing-baseline` eval (14) changes `build_payload`
to strip surrounding whitespace. Its request recorder always returns success.
No supported-input contract, provider contract or deployed revision is supplied.
Changed request values and non-string exceptions are demonstrable. Supported
non-string callers, significant server whitespace semantics and an incompatible
deployment are not. The whitespace consequence is hypothetical.

## Report evidence

- [Claude standard 1](../r7-conclusions/runs/claude-candidate-R7-standard-1/report.md)
  returns COMMENT and initially withholds deployment confirmation, then labels
  provider compatibility Supported from the client sending a subset of values.
  Closing full approval depends on string-only callers; provider semantics remain
  expressly unseen.
- [Claude standard 2](../r7-conclusions/runs/claude-candidate-R7-standard-2/report.md)
  also returns COMMENT and discloses unavailable tests/provider evidence. It
  qualifies the narrower-values argument as client-only, but closes with “fine
  to deploy” after a string-caller check that does not settle provider semantics.
- [Codex standard 1](../r7-conclusions/runs/codex-candidate-R7-standard-1/report.md)
  withholds readiness, limits tests to local behavior and requests provider and
  deployment-baseline evidence. This meets the old rubric; it does not prove all
  requested checks are operationally material.

The claims are actual report text, and historical 14.3/14.4 FAILs remain valid
under the pinned rubric. Their operational significance is uncertain because the
fixture does not establish a consequential provider distinction. A conditional
sentence alone does not establish overconfidence: read its antecedent, conclusion,
scope and unresolved material facts together.

## Successor measurement

R7M adds `clear_name`, which sends null. The explicit protocol makes the unknown
version material: v1 rejects null without mutation; v2 restores the account default.
This establishes conditional incompatibility, not an observed v1 deployment or
a violated independent-delivery policy. R3 instead has a known required baseline.

R7B moves normalization into the client. An explicit string-only input contract
and identical provider normalization establish equivalent stored labels on both
supported versions. Unknown deployment inventory is immaterial to that equivalence.
Scoped approval is useful; live-verification claims would remain unsupported.

Both cases use the same ordinary prompt and protocol table. READMEs state product
requirements, not reviewer answers. Separate identities preserve old fixtures.
The [rubric](rubric.md) fixes examples and mapping before measurement. Four
unchanged-skill sessions test discriminating judgment, not improvement,
reliability or full-feature acceptance.
