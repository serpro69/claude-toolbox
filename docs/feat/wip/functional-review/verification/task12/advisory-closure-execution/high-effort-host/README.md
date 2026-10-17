# Claude effort correction: ready for approved probes

> Task: 12.21 continuation, 2026-10-17
> Source: independently approved; nine successor and 26 predecessor tests pass
> Runtime preflight: BLOCKED — explicit external-payload approval needed
> Replacement host probes: 0; measured comparison: 0; adoption unchanged

The [successor launcher](successor.py) now enforces
`CLAUDE_CODE_EFFORT_LEVEL=high` at the actual Claude process boundary for baseline
and candidate, in both binding and later measured launches. The inherited
transport records that same mapping in `command.json`; prepared launch metadata
also names the setting. Actor instructions remain byte-identical, including the
candidate reviewer's xhigh frontmatter. The environment override addresses that
precedence without editing the frozen actor source.

## Reviewed and verified

- [Run contract](run-contract.md) fixes the scope, configuration, original evidence
  identities, calibration reuse and completion criteria before any replacement.
- [Source review](source-review.md) approves the host-execution successor with no
  findings, following the [full launcher review](../high-effort/source-review.md).
- [Nine successor tests](checks/successor-tests.txt) cover actual launch environment
  and command receipts, conflicting ambient effort, exception restoration,
  binding/measured routing, original-freeze preservation, source drift, preparation
  validation on both sides, Codex noninterference, runtime retention and preflight
  refusal. Their external process boundary is mocked; they launch no actors.
- [Twenty-six predecessor regressions](../high-effort/checks/predecessor-tests.txt)
  pass. Preparation, calibration and original preflight checksum manifests still
  verify. No operative plugin change requires regeneration or a full suite rerun;
  the previously assigned hook-fixture failure remains outside this change.

The immutable host [execution freeze](execution-freeze.json) is
`be7d605b7aabe88855051362a3f92bc99a0cf56a6fe22b0805adfc1763830764`.
It derives from the original execution freeze `edc9cc7798bc3b2f7759a0c707db26abe2ead848bf51b6ec9de8535497a5dd85`.
The 25 calibration sessions, two Codex bindings and two state probes retain their
original identities and complete checks. Independent source review approved
this limited reuse because their applicable code/configuration is unchanged.
No old Claude binding is evidence of the corrected effort configuration.

## Attempts and current blocker

The earlier [sandbox-limited attempt](../high-effort/README.md) could not start
normally: SessionStart reported EROFS, Capy startup failed and API retries followed.
The parent interrupted it; the returned exit was 130 without controller completion
or finalization. Its exact partial evidence and separate incomplete manifest remain.
No instruction receipt or graceful-cleanup claim follows from that attempt.

The host successor changes only its owned workspace root in Python; its separate
declaration selects normal authenticated session/hook/network execution for both
sides. The exact [baseline launch request](baseline-launch-request.json) was
rejected before process creation by automatic approval review. Its
[recorded reason](approval-result.json) is that the request may send private
plugin/repository content to the authenticated Claude/API destination and that
the user's general continuation did not specifically authorize that payload.
No alternative route was attempted, no candidate probe was launched, and no
successor PASS attestation exists.

## Concrete next action

Owner: implementing agent after explicit user approval. The requested approval
covers sending the frozen filtered plugin instructions and synthetic fixture to
the authenticated Anthropic Claude API for **two fresh binding probes**, baseline
and candidate, with normal host session/hook access, isolated Capy state and PAL
excluded. It does not select the 64 measured sessions.

After approval, reverify freeze/calibration, execute the retained baseline request,
then the equivalent candidate request serially. Retain each actual request and
response identity; stop on failure without an implicit retry. Run `successor.py
audit` and `retain`, inspect actual access/receipts, obtain independent capture
review, and only then write/verify a successor preflight attestation. Successful
process exits alone do not satisfy the gate. Internal effort telemetry and
unavailable exact transport fields remain outside the claim.

Task 12.21.4 remains open. Original preflight stays BLOCKED. Behavioral measurement,
adoption, original acceptance, deferred PAL, other investigations and Task 13
retain their existing status. The user's next approval is the only immediate
external authorization needed; launcher implementation/review is complete.
