# Task 12.13: evidence-qualified compatibility conclusions

Declared 2026-10-13 before binding or measured sessions. The user approved the
brainstorm outcome: keep missing compatibility evidence Unknown, with a concrete
next check, instead of conditional deployment approval. Replace existing common
guidance; preserve known prerequisites, scoped code conclusions and clean reviews.

## Comparison and source

Baseline: `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`. Candidate:
`bf873de63369662ebe3b0cde4226dbda1c16104b`, constructed in a temporary repository
from `cc07a614a999e8f35e2f408a505546077154031f` plus the canonical/generated
method replacements. [Provenance](source-provenance.json) records that construction;
the working repository is not committed by this operation.

Run **48 fresh sessions**: R7, R3 and R5; standard and isolated modes; Claude and
Codex; immutable baseline and candidate; two repetitions each. The adapter only
selects these existing cases. Ordinary prompts, fixtures, assertions, oracles and
revision-2 rubric remain unchanged. Source archives, excluded/retained manifests,
runtime/controller and fixture hashes are frozen before binding or measurement.
No previous result substitutes for either side. Comparison with the pre-feature
baseline does not isolate this wording's incremental causal effect.

## Runtime and boundaries

- Claude Code 2.1.296, `claude-opus-5-5`/high parent and forced named reviewer.
- Codex 0.162.1, `gpt-6-astra`/xhigh parent, immutable generated
  `gpt-6.1-sol`/xhigh reviewer; provider fallback disabled.
- Capy 0.17.0, controller Python 3.12.11, actor `python3` 3.10.12, Linux.
- Existing explicit Claude tool allowlist, `dontAsk`, normal hooks,
  `--plugin-dir`, run-local registry and `--strict-mcp-config`. Launch a separate
  hash-bound MCP configuration excluding PAL, following the reviewed
  [entry-path adapter](../entry-path-no-pal/runner.py).
- Codex retains the reviewed matrix adapter's `workspace-write`/`never` policy,
  PAL disabled, temporary project trust and revision-specific local plugin/cache
  registration, with prior-absence records and owned cleanup. No persistent
  user-setting change is intended.

Capy differs from the earlier declaration; this is a fresh matching comparison,
not a pooled extension of historical runs. The [state probe](state-probe/summary.json)
confirms empty independent stores, real indexing/retrieval, absent foreign markers
and unavailable private vaults on 0.17.0. No new package or model is introduced.

Run separate baseline/candidate loading probes on both providers. Require actual
selected bundle/agent receipt, complete common-method reads before investigation,
correct model/root identities, available Capy and absent PAL. A failed loading
probe blocks that provider's measured sessions; preserve it and stop instead of
silently changing policy, runtime, instructions or substituting a direct reviewer.

After binding passes, prepare all selected inputs before serial capture. Each run
has its own workspace, empty knowledge state and unavailable vault. Use the
inherited capture deadlines, owned process-group cleanup, redaction and seals.
Preserve partial failures and all attempts. Controller/oracle material stays out
of actor bundles, prompts and catalogs; audit actual access without claiming OS
read confinement. Never overwrite or silently skip an attempt.

## Grading and decision

Use the unchanged [revision-2 rubric](../../task2-rubric-v2.md) and
[pinned grader](../../task2b/grader.md), SHA-256
`c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`.
Independent fresh `eval-grader` roles (`gpt-6.1-sol`/xhigh) receive only sealed
manifest-listed evidence, grading instructions, assertions and expected outputs.
Run the existing positive/negative/missing-event/receipt calibration before grading.
Every original assertion is graded; private reasoning is excluded.

The bounded keep decision requires both R7 candidate repetitions in each
provider/mode to meet 14.1–14.6, retaining provider and release qualifications
through closing advice. Both R3 candidate repetitions must preserve its non-PAL
behavior/history-receipt components and demonstrated incompatibility; both R5
candidate repetitions must preserve its non-PAL ordering, coverage and justified
clean scoped approval. Reject the candidate on a failed target or regressed control;
do not start another actor iteration automatically.

PAL remains explicitly user-deferred and absent. Its required components retain
FAIL; positive local components do not change those aggregate grades. Exact
Codex handoff content remains unverified. Only existing R3 7.5/7.6 and I2 9.5
have the approved receipt/use fallback; no extension is authorized here. Other
missing receipts retain FAIL/PARTIAL as required by the unchanged rubric. Report
these limits separately from the bounded outcome; this slice cannot close full
Task 12 acceptance, legacy controls or Task 13. Owner: implementing agent.
