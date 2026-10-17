# Claude high-effort preflight successor

Task 12.21 continuation, selected by the user on 2026-10-17. Correct and review
the launcher, freeze this successor, run two fresh Claude bindings serially and
obtain independent preflight review. The 64 measured sessions remain unselected.
Preserve the blocked predecessor, all captures and frozen source bytes.

## Changed runtime boundary

Set `CLAUDE_CODE_EFFORT_LEVEL=high` in the actual Claude subprocess environment
on both source sides, for bindings and later measured launches. The existing
transport's `MODEL_ENV` mapping supplies both `Popen` and `command.json`; scope
the additional key with restoration on success or exception. Keep the parent
`--effort high`, model forcing, permissions, prompts and PAL exclusion unchanged.
Preparation also records the choice and binds it into `prepared.json`.

The [official subagent documentation](https://code.claude.com/docs/en/sub-agents#choose-an-effort-level)
states that this variable overrides agent-definition and per-invocation effort.
The [environment reference](https://code.claude.com/docs/en/env-vars) documents
precedence over CLI effort, with configured caps still applicable. Checked on
2026-10-17. Context7 has no exact 2.1.296 version. The installed, hash-pinned
2.1.296 binary contains the effort environment override diagnostics; fresh
bindings validate accepted launch/input configuration. Capture the selected
process environment; do not claim service-internal effort telemetry.

## Freeze and calibration relationship

The predecessor freeze remains
`edc9cc7798bc3b2f7759a0c707db26abe2ead848bf51b6ec9de8535497a5dd85`.
The successor independently pins its adapter, tests, declaration, predecessor
metadata and inherited evidence. Before every operation it verifies original
source/fixture/controller identities. Run fresh affected Claude baseline/candidate
bindings with the new freeze and fresh workspaces under
`/tmp/fr-advisory-high-effort-host-20261017`; never substitute the old Claude captures.

Reuse the 25 fresh calibration sessions with their original identities: the
grader configuration, sealed packets, assertions, rubric, dispatches, returns
and reconciliation code are unchanged. Verify their complete original contract.
This actor-only environment correction cannot change those already captured
synthetic grader inputs. No regrading, new calibration result or changed grading
threshold is claimed. Independent source review must assess this relationship
before freezing or launching.

Codex launching and Capy state policy are unchanged. Retain both Codex bindings
and both independent state probes under their predecessor freeze, with every
manifest/raw-evidence hash pinned by the successor. They are explicitly inherited
observations, not fresh successor runs. Review this limited reuse, original
instruction/model/role receipts, xhigh Codex configuration and state results.

## Verification and completion

Before launch, test the real inherited Claude launch function at its subprocess
boundary: the environment and retained command must both contain high, including
when ambient effort differs. Test restoration after failure, binding and measured
capture routing, source-drift refusal and no-overwrite behavior. Mock external
process execution, not the behavior asserted. Run predecessor adapter/receipt
regressions and frozen-input/calibration verification. No operative plugin file
changes, dependency upgrade or generation is required.

Audit fresh complete parent/child instruction receipts, selected model/root,
unchanged subjects, command effort settings, actual access and PAL absence.
Retain all attempts. A failed binding stops the affected sequence; do not retry
implicitly or weaken the loading requirements. Preserve runtime configuration
files without credentials, personal history or knowledge stores. No persistent
Codex registration is needed for these Claude-only bindings.

Independent review follows the captures and audits. Only an approved review and
all required checked evidence permit a new `preflight.json` and successful guard.
The predecessor attestation stays BLOCKED. A successor PASS establishes readiness
for a later selected comparison, not behavioral improvement, adoption, full
feature acceptance or Task 13 completion. Exact unavailable transport fields and
service-internal effort remain unclaimed; no receipt/use fallback is expanded.

## Explicit host-execution successor

The preceding `../high-effort/` baseline attempt could not start normally inside
the outer Codex sandbox: the SessionStart hook reported EROFS for Claude's
normal session-env directory, Capy startup failed, and only API retries followed.
The parent interrupted it; the tool returned 130 without a controller completion
record. Preserve its exact partial events/command and parent-labeled incomplete
manifest. The candidate probe was not launched and no loading PASS is claimed.

This separately reviewed declaration selects normal host execution for the two
fresh Claude bindings via the tool's sandbox escalation. It permits normal
authenticated Claude session/hook/network operation; the actor's own tool policy,
setting sources, models, effort, source bundles, Capy isolation and PAL exclusion
remain unchanged. No user security setting is edited. Both sides use this same
context. The only Python delta from the reviewed predecessor is the fresh owned
workspace root. Its failed paths/freeze are never reused. Preserve separate freeze,
review, tests and capture identities before the replacement attempt. The user
authorized this next-step implementation and affected probes; no measured batch
is selected. An approval rejection must be reported, not bypassed.
