# Corrected Claude bindings: effort verified, loading gate open

> Task: 12.21 continuation, 2026-10-17
> Captures: baseline and candidate complete, once each; both exit 0
> Readiness: BLOCKED — candidate omits eight required detection-file receipts
> Independent completion review: verification correction APPROVED; readiness BLOCKED
> Measured sessions: 0; adoption and original acceptance unchanged

The [explicit authorization](authorization.md) resolved the earlier host/API
approval blocker. Both fresh host bindings ran under execution freeze
`be7d605b7aabe88855051362a3f92bc99a0cf56a6fe22b0805adfc1763830764`.
Their command records set `CLAUDE_CODE_EFFORT_LEVEL=high`, retain parent
`--effort high`, and force `claude-opus-5-5` for both named reviewers. Hooks pass,
Capy connects, and the expected selected roots/models are observed. This closes
the previous launch-configuration evidence gap; service-internal effort telemetry
is not claimed.

The [baseline audit](audits/binding-claude-baseline.json) passes the declared
source/role/full-read conditions. The [candidate audit](audits/binding-claude-candidate.json)
retains FAIL: its parent returns seven complete methodology Reads and its child
returns all five required sources, but no `profiles/*/DETECTION.md` is read.
All eight known profiles are missing: go, python, java, js_ts, kotlin, k8s,
k8s-operator and skill-md. Registered entry-point delivery is present in both.

This is a demonstrated loading omission, not merely missing raw capture. The
candidate [final report](binding-claude-candidate/report.md) explicitly says
it stopped before diff selection and omitted all eight detection reads. Frozen
`packet-preparation.md` step 1 and its direct-read fallback, plus SKILL.md phase 1,
include those files in the bootstrap before diff selection. The original audit
therefore correctly refuses this candidate's declared receipt condition.

Actual [baseline](baseline-access-events.json) and [candidate](candidate-access-events.json)
tool inventories contain 7 and 15 calls respectively: only Skill, instruction
Reads, the requested root-print command and one named reviewer per side. No
subject/evaluator read, application call, packet creation or PAL access is
observed. Subjects remain unchanged. Candidate dispatch omitted the literal
Plugin Root heading but supplied selected absolute paths and returned the child
instructions; no exact-prompt fallback is expanded.

[Integrity checks](checks/post-capture-integrity.json) verify all 31 baseline
and 35 candidate capture files and unchanged original preparation/preflight seals.
[Runtime retention](runtime-inputs.json) preserves ten verified configuration
files without personal authentication files or knowledge stores. No temporary
Codex registration was created. Owned probe workspaces remain for later evidence
housekeeping; this task does not delete repository history or personal runtime
state. Earlier interrupted and rejected attempts remain intact.

## Reviewed verification correction

The [initial independent review](completion-review-initial.md) confirmed the
effort evidence and missing detections, and found a P2 guard gap: checking only
audit hashes/names could admit a failed audit under a later overall PASS claim.
The [separate verification successor](guarded_successor.py) now recomputes the
pinned receipt audit against each sealed capture and requires the retained audit
to equal the complete successful result before the original preflight gate.
No captured actor/runtime/prompt/source identity changed.

[Five regression tests](checks/guard-tests.txt) pass, including the actual failed
candidate, valid baseline, empty/failed audits, dependency drift and CLI adapter
selection/restoration. The initial JSON tuple/array comparison failure is retained
in the adjacent initial-test log and corrected before freeze. The
[final independent review](completion-review.md) approves this correction with
no remaining source findings and explicitly retains BLOCKED readiness.

The [guard freeze](guard-freeze.json) is
`f7d0a820204eaa899a2b9ed6840325cf93190fa07aeb4a072aee56fb0ba96fb1`.
The [actual guard invocation](checks/preflight-guard.txt) exits 1 for the missing
candidate detection instructions. [preflight.json](preflight.json) preserves the
BLOCKED attestation and binds captures, audits, review, calibration and retained
configuration. Future preparation/measurement must use `guarded_successor.py`;
the frozen original launcher remains historical. No failure has become a PASS.

## Concrete follow-up

Owner: implementing agent. Reconcile the binding prompt's stopping instruction
with its required bootstrap inventory, then prepare and independently review a
bounded successor declaration before another affected capture. Preserve actual
selected-source requirements, source bytes, this failure and all original grades.
Do not turn corrected effort or successful process exits into preflight PASS.
This probe-loading miss alone does not establish a functional-review defect or
justify another operative skill instruction change.

No replacement prompt or further actor run is selected here. Task 12.21.4 stays
open; the 64-session comparison, adoption, original acceptance, deferred PAL,
other investigations and Task 13 retain their existing status.
