# Run-contract amendment — 2026-10-09

> Status: user-approved sequencing change; capture investigation and any successor rubric remain pending
> Original declaration: [run-contract.md](run-contract.md)
> Current plan: [tasks.md](../tasks.md)
> Resolution procedure: [evaluation.md](../evaluation.md#codex-handoff-capture-resolution)

## Authority and reason

On 2026-10-09, after discussing the four missing Codex captures, the user approved
separating implementation readiness from full verification, one bounded capture
investigation, and a conditional fallback to observable reviewer receipt/use if
plaintext remains unavailable. The request was to update the documents; no new
probe, capture, grade or operative implementation is claimed here.

The actor baseline is preserved at
`c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`. It remains runnable after candidate
development starts. Requiring every seed capture before any operative edit adds
a sequencing restriction without strengthening that revision binding.

This amendment governs subsequent work together with the unchanged portions of
the original contract. It supersedes the original requirement to hold operative
changes until all seed baselines are captured, including the stop-development
language in the historical [Task 2 capture record](task2/README.md). That record
and the original run contract remain intact because evidence manifests cover
their bytes. Historical statements describe the decision in effect at capture,
not the current task dependency.

## Implementation and acceptance gates

- **Task 2 gate 2A: done.** Final R1/R3/I1/I2 fixtures, frozen inputs and 16 baseline
  captures are retained: 12 Claude and four Codex. Task 3 may start; Tasks 3–11
  follow their existing dependencies without waiting for gate 2B.
- **Task 2 gate 2B: open.** Codex R3 isolated and I2 standalone remain UNRUN,
  two repetitions each. The implementing agent owns the bounded investigation,
  evidence-contract selection and four fresh baseline captures, plus any required
  baseline recaptures. Candidate counterparts remain Task 12 work. Task 12 and
  feature completion still depend on this gate.
- **Behavioral acceptance: pending.** Capture completion permits grading; it does
  not assert passing behavior. Baseline failures remain comparison data. Every
  required candidate assertion must still pass in two fresh runs.

Task 2 stays in progress until 2B closes. Its existing task/subtask identifiers,
captured results and unrun records remain traceable.

## Bounded investigation and conditional fallback

Follow [the resolution procedure](../evaluation.md#codex-handoff-capture-resolution):
identify a supported alternative, justify it, and run at most one additional
fresh marker probe. If no viable alternative exists, record that outcome without
another run. Do not repeat the already-failed surfaces unchanged. Probe success
requires readable submitted content linked to the actual receiving child and
observable reads of the referenced evidence.

If successful, retain the exact-handoff assertions. Otherwise the user-authorized
fallback requires a separately versioned rubric/assertion mapping for independently
observed receipt and use of the required evidence by both reviewers. It must
explicitly leave exact submitted prompt content unverified. A parent summary,
file availability or correct finding alone cannot satisfy it. Missing receipt/use
evidence still leaves the gate open.

Before any affected batch, record the selected path, probe result, assertion
mapping, configuration and hashes in a successor amendment. For the fallback,
preserve the original assertion/oracle bytes and freeze revision 2 separately;
update the final eval definitions and generated copies without changing subject
fixtures or ordinary prompts. Until then, revision 1 remains the grading contract;
this amendment does not silently reinterpret its exact-handoff assertions.

Both sides and providers use the same revised behavioral assertions. Retained
traces may be regraded if sufficient; otherwise recapture affected comparisons.
Any runtime/model/policy or material capture-configuration change requires matching
fresh baseline/candidate runs under the revised declaration. Preserve all earlier
attempts and record exact prompt content as unverified wherever the fallback is used.

## Preserved controls and next action

Provider selection/coverage, model declarations, two-run acceptance, fixture
isolation, independent review, historical-source provenance and evidence-backed
grading remain required. Preserve [the original freeze](task2-frozen.json),
[revision-1 rubric](task2-rubric.md), sealed captures and evidence manifests.
No ciphertext is treated as plaintext and no unavailable assertion becomes PASS.

The implementing agent can start Task 3 now. Separately, execute Task 2.5 and
record its bounded outcome, then complete 2.6 and 2.3. Investigation is deferred
from the implementation gate because of the observed runtime limitation; closure
requires an explicit evidence path and gradable captures before Task 12, followed
by passing candidate results before feature completion.
