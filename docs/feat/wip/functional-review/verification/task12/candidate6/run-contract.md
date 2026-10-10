# Candidate 6: R5-only follow-up

Declared before binding or measurement. The user agreed to the R5-only follow-up
and asked to commit the prior work first; commit `17344213` preserves candidate 5
and its failed diagnostic. This declaration covers one bounded R5-standard batch,
not expansion to other cases. PAL remains user-deferred.

## Fixed comparison

- Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`.
- Candidate: `ab7daa7f2833abefc64dedc08e8e44790ce5a0ee`, committed only in the
  temporary source repository used to build the filtered instruction bundle.
- Four fresh runs: baseline/candidate, R5 standard, two repetitions each.
  Do not replace an unfavorable repetition with a historical result.
- Original R5 subject, ordinary prompt, six required assertions, revision-2
  rubric and grader are unchanged. Grader SHA:
  `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
- Require PASS on all six candidate assertions in both repetitions. Failures and
  partial evidence stay open. This is a diagnostic checkpoint, not a reliability
  estimate or full-matrix/provider acceptance.

## Configuration and evidence

Inherit [candidate 5's runtime/evidence declaration](../candidate5/run-contract.md):
Claude 2.1.272 with `claude-opus-4-8[1m]`/high, Capy 0.16.8, controller Python
3.12.11, actor Python 3.10.12, Linux; unchanged actor arguments, tool policy and
reviewer role. Native isolated grader roles remain declared `gpt-6.1-sol`/xhigh,
with exact service telemetry unavailable. Codex 0.162.1 is recorded but not run.

Reuse the reviewed `rework/driver.py`, `runtime.py` and `capture.py` unchanged.
Prepare all four inputs before any measured capture and run serially, preserving
ownership, deadlines, sealed failure propagation, credential redaction and
packet snapshots. Freeze the new declaration, contract, source identities and
controller dependencies before launch. Keep old controllers, freezes and grades.

Run a separate candidate binding probe. The prior baseline binding remains
applicable because its source, runner, runtime and policy are unchanged; fresh
baseline measurements still validate their own bundle/configuration/empty state
immediately before transport. Every measured run gets a fresh subject workspace,
empty Capy store and unavailable private vault. No probe state becomes a seed.

Validate raw/derived seals before fresh independent grading. Actual completed
Read results establish packet receipt and ordering; creation, manifests and
actor claims do not. Audit subject/bundle stability, scoped tool accesses and
owned packet directories. Exact submitted reviewer prompts and OS-wide read
confinement remain unverified. No PAL tool call or corroboration is claimed.

## Change and acceptance boundary

Early selection now identifies the Git diff only; task scope belongs to
post-checklist investigation. Clean reviews finish with their scoped verdict and
coverage, without a mandatory remediation menu or unsupported future-work option.
Actual findings, material unknowns, required prerequisites and edit authorization
retain their existing rules. The shared timing note applies specifically to code
review; review-spec's scope payload remains unchanged.

Source approval and static checks do not establish behavior. Report all four
results and retained failures before deciding on further iteration or expansion.
Candidate-5 R1/R3 observations remain tied to their original source; this R5-only
batch does not relabel them as measurements of candidate 6.
