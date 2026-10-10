# Candidate 5: focused structural rework diagnostic

Declared before binding and measured runs. The user accepted focused rework
after the candidate-4 stop and commit `87a26bb7`. This declaration authorizes
one bounded R1/R3/R5 standard-mode diagnostic, preserving all previous evidence.
Do not expand to the remaining matrix unless every candidate assertion passes
in both fresh repetitions. If this checkpoint fails, retain the result and
report the specific remaining cause before another candidate iteration.

## Identities and unchanged requirements

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate: `be1a283cf872ec97fe569c9fd481bbe623cc8214`, a temporary source-repo
  commit containing canonical/generated packet preparation and scenario guidance.
- Same subject fixtures and ordinary prompts as the prior batch. New packet
  authoring evals do not change the three diagnostic fixtures or enter actor inputs.
- Same revision-2 rubric and grader SHA
  `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
- Same actor CLI policy/model arguments: Claude 2.1.272,
  `claude-opus-4-8[1m]`/high; named reviewer uses the unchanged role declaration.
  Capy 0.16.8, controller Python 3.12.11, actor Python 3.10.12, Linux.
  Codex 0.162.1 is recorded for freeze integrity but has no diagnostic actor run.
- Independent native `eval-grader` roles, `gpt-6.1-sol`/xhigh as declared by the
  role; exact service telemetry unavailable. Same pinned instructions for both sides.
- All assertions remain required; no threshold, severity or verdict reinterpretation.
  Diagnostic summaries classify actual failure causes as procedural, behavioral,
  or reporting/recommendation issues. Those labels never change original grades.

## Successor capture and isolation

Use `rework/driver.py` and its frozen runtime/capture helpers. Prepare the entire
selected case batch before launch, then capture serially. Signal handlers record
requests; the Linux reader terminates the owned process group before reaping
its leader, records timeout/interruption, and seals evidence. Runtime failures
propagate after sealing and stop the batch. The runtime deadline is 1,800 seconds
per actor, with a five-second termination grace. These limits apply to both sides.
Old frozen adapters and their evidence are unchanged.

The actor arguments/tool policy match the original capture helper (offline
regression checked). The capture configuration changed, so **do not reuse prior
baselines**: twelve new runs comprise baseline/candidate × R1/R3/R5 × two
repetitions. Each owns fresh subject, Capy and unavailable-vault state. Source
bundles exclude evaluator material and are checked again immediately before launch.
Binding probes use separate workspaces and never seed measured runs.

The successor also snapshots requested instruction-packet part files from their
unique `/tmp/kk-review-instructions-*` directory, bounded to 13 KB, alongside
the unchanged payload mechanism. Snapshot presence is not receipt. A complete
successful Read with returned bytes establishes loading; unread/truncated parts
remain missing. Retain packet creation, manifest and Read events and audit them
against the frozen original instruction bodies. Exact reviewer prompt parity and
OS-wide read confinement remain unverified.

## Verification and reporting

Require the separate revision-binding probe before measured runs. Confirm loaded
entry point/common/agent bytes against the retained bundle and inspect packet
creation plus actual reads. Capture/grade every declared attempt without hints
or requirement-changing replies. Validate sealed raw/derived files before fresh
independent grading, and audit accesses and temporary packet ownership before
counting successful observations for acceptance.

The earlier grader calibration remains applicable because neither grader nor
rubric changed; an offline adapter regression additionally establishes preservation
of packet Read results and linkage. That regression does not prove live binding.
Review source approvals, static checks, binding and behavioral grades are separate
claims. No statistical reliability or full provider parity is inferred.

PAL-dependent verification remains user-deferred: no live PAL probe, R8 replay,
corroboration or PAL receipt claim. Normal configured services and actor policy
remain the same on both sides. The new probe cleanup is verified offline only.
Full latest-source isolated/implementation cases, Codex representatives and legacy
actor controls remain Task 12 obligations outside this diagnostic checkpoint.
