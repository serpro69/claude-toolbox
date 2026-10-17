# Runtime preflight result

> Task: 12.21, run 2026-10-17
> Result: BLOCKED — Claude reviewer effort is not established at the declared high setting
> Measured sessions: 0; adoption and full feature acceptance unchanged

The requested four binding probes and two Capy state probes ran. All four binding
processes exited successfully, returned the required instructions from the selected
source, used the expected model identities/named reviewer and left subject files
unchanged. Both state probes passed their empty-store, index/search, foreign-marker
and unavailable-vault checks. Temporary Codex registrations/trust were removed;
32 run-local configuration/role files are retained in a checked archive.

The preflight did **not** pass its whole declared runtime contract. Claude's parent
flag is high, but the frozen candidate reviewer defines xhigh. The launcher forces
the child model without pinning/capturing an effort override. Official precedence
and the available receipts do not establish that the child ran high. See the
[focused assessment](claude-effort-assessment.md) for exact evidence, sources,
limits and the proposed correction. This is not a claim that an unobserved effective
effort value is known.

[Independent review](preflight-review.md) returns COMMENT and confirms BLOCKED
readiness. [preflight.json](preflight.json) preserves that disposition and all
evidence hashes; the original adapter's guard must reject it. Do not change its
status to PASS on the strength of successful process exits or model-name matches.

Useful evidence remains separate:

- [Binding audits](preflight-audits/) verify source/model/role receipts and capture
  integrity, with manual access limits retained.
- [State summary](state-probe/summary.json) and adjacent raw calls/results establish
  the two state checks.
- [Runtime retention](preflight-runtime-inputs.json) binds 32 files and owned Codex
  cleanup, without copying personal authentication files or knowledge databases.
- [Review input](preflight-review-input.md) retains the Claude packet-path deviation
  and the three failed Codex metadata searches. The former does not invalidate the
  demonstrated direct-read fallback; neither is hidden as universal prompt success.

Owner of the next action is the implementing agent: review a successor launcher
that enforces and records the already-declared high effort, preserve the actor
sources, freeze its runtime/adapter identity and calibration relationship, then
run fresh affected Claude bindings. No replacement attempt, requirement waiver,
new runtime, measured actor session or historical regrade was selected here.

Five offline receipt-decoder tests pass. Source and calibration freezes still
verify. `PREFLIGHT-SHA256SUMS` retains this preflight evidence separately from the
existing preparation/calibration checksum lists. Task 12.21 remains open at its
readiness/attestation gate; the four captures and two state probes are completed
observations, not unrun work.
