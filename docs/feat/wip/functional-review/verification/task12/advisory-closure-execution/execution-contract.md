# Advisory-closure execution preparation and calibration

> Task: 12.20, selected 2026-10-17
> Authority: prepare/review/freeze the adapter and run fresh calibration
> Binding, state probes, measured actors and adoption: not selected

The immutable [preparation contract](../advisory-closure/run-contract.md) and
freeze SHA-256 `2850e0416ef0277109849e206e11851f10d92fdcfd6954d8ecf5d68127e95bea`
remain authoritative. This adapter does not change any fixture, assertion,
candidate instruction, model choice or bounded KEEP/REJECT/INCONCLUSIVE criterion.

## Adapter and input identity

Use installed Python 3.12.11, with its directory first on PATH so inherited
`python3` calls use the same interpreter. `runner.py restore` verifies the
preparation seal and restores inputs to a new owned directory under `/tmp`.
Restored controller and evaluation files are checked before import; snapshots
retain their original source archive, identity, filtered trees, modes and links.
No installed plugin or historical scratch workspace supplies actor instructions.

The adapter imports the archived R7/Opus55 transports and configures only this
comparison's paths, source identities, cases and case-specific rubric routing.
It preserves existing permission policy, PAL exclusion, owned-process cleanup,
source/prompt validation and capture sealing. New execution files are separate
from the preparation archive and old controllers. An execution freeze pins these
new files, the complete calibration input set, restored inputs through the
preparation seal, runtime identities, source snapshots, prompts and both rubrics.

`list`, `freeze`, `verify` and calibration packaging are offline. `prepare` requires
passing preflight; all 64 workspaces/evidence directories must be fresh. `run`
requires the complete prepared batch and rejects any existing attempt artifact,
including a partial unsealed attempt. Capture is serial and stops on failure or
interruption. It never overwrites, silently skips or automatically retries a run.
`grade --job <id>` exports the correct rubric and unchanged assertions from sealed
capture evidence. Standard results never establish isolated/PAL coverage.

`binding --provider <provider> --side <side>` requires the execution freeze and
successful fresh calibration. It is implemented for later use, not invoked in
Task 12.20. Full preflight additionally requires all four binding seals and their
matching launch identities, two distinct state probes with retained evidence,
and an independent preflight review. The required `preflight.json` contains
execution/calibration hashes, binding-manifest hashes, and `state` and
`independent_review` records (`path`, `sha256`, `status: PASS`). The state record
also lists raw probe `evidence` path/hash pairs; its summary uses the existing
two-row state-probe schema. A self-declared runtime exit is not semantic binding
approval; the independent review must inspect actual instruction/model receipt.

## Fresh calibration declaration

Run **25 independent fresh eval-grader sessions**, all using configured
`gpt-6.1-sol` / xhigh roles, `fork_turns: none`, the unchanged pinned grader body
and workflow mode. The historical frontmatter in that body does not select the
runtime model; role dispatch settings do. No actor or PAL process is launched.

- Five unchanged ordering controls: ordered, early edit, missing events,
  requested-only reads and complete omission. Five assertions.
- Eight unchanged R6 semantic/trigger controls. Twenty-eight assertions.
- Twelve new disposition controls, each with three mutually exclusive outcome
  assertions. Thirty-six assertions. They exercise supported KEEP, failed
  follow-up, missing capture, absent/child-only advisory, tolerated default
  omission, unsupported safety claim, missing trigger, missing default evidence,
  rejection despite another missing capture, PARTIAL target evidence and an
  incorrect checked-in configuration claim.

Total: **69 assertion judgments**, plus the existing explicit conditional-trigger
values. Expected outcomes are controller-only in `calibration/expected-verdicts.json`.
They are frozen before dispatch and never listed in a grader's permitted evidence.
Each grader receives only its own sealed packet, pinned methodology and exact
manifest-listed evidence. For conditional 22.3/22.6 rows, its evidence column must
state `trigger=present`, `trigger=absent` or `trigger=unobservable`. The controller
parses those literal observations; it does not infer them from expected answers.

The new disposition packets are synthetic complete batch summaries, not actual
actor records. Their rubric explicitly distinguishes a described missing capture
(which can deterministically yield INCONCLUSIVE) from a missing calibration input
(which may require PARTIAL). The final-report evidence still overrides a stipulated
PASS when the supplied report violates the component rules. Every original 22.4
failure remains failed even in a permitted bounded KEEP example.

Source review and offline verification precede the execution freeze and first
calibration dispatch. Retain all dispatch parameters, packet/manifest hashes,
agent IDs and verbatim returns. Controller reconciliation requires exact assertion
coverage and expected verdict/trigger matches; missing, duplicate or mismatched
returns cannot pass. No grader is reused for another control. No automatic retry
or post-result criterion change follows a mismatch; retain it and obtain an
independent assessment before any separately identified successor.

The frozen dispatch plan includes each exact spawn request, required Plugin Root,
workflow mode, prompt hash, methodology hash and fixed role configuration. Record
the actual request and returned canonical agent identity; reconciliation checks
them against the plan and rejects reused identities. Standalone reconciliation
and verification recheck frozen dependencies and calibration inputs before reading
expected answers. Role configuration records the selected public role/model/effort;
it does not claim independent service-internal telemetry or captured read receipts.

These sessions use the collaboration eval-grader role through its existing
read-only workflow. Tool-level prompt/settings and returned verdict provenance
are retained; encrypted transport messages, internal service telemetry and OS
filesystem isolation are not claimed. Payloads explicitly prohibit directory
scans, live source reads, expected-answer access and repairs. Inspect available
grading access evidence before claiming anything beyond this boundary.

## Completion boundary

Task 12.20 completes after reviewed adapter code, offline checks, a verified
execution freeze, matching fresh calibration results and independent completion
review. No calibration PASS establishes actor efficacy, successful binding/state
isolation, adoption, original feature acceptance or Task 13 completion. The next
unrun prerequisites remain the four binding and two state probes and reviewed
preflight; measured execution still needs selection.
