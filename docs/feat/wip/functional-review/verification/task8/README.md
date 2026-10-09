# Task 8 — execution-evidence grading

Task 8 implements and calibrates the workflow grader, and grades all 16 retained
Task 2 baselines. It does not close capture gate 2B or establish candidate
acceptance. The original fixture, oracle, prompt, rubric and capture bytes remain
unchanged; the receipt/use fallback has not been selected.

## Delivered behavior

The canonical eval-grader now requires explicit `Grading mode: workflow` for
execution evidence. Omitted mode retains component text grading. Workflow reads
are limited to supplied grading instructions/rubric, the sealed manifest and its
exact evidence files. Completed reads, actual dispatches and resulting files take
precedence over final claims. Observed violations are FAIL; missing evidence is
PARTIAL; neither passes acceptance. The review harness and implementation-eval
playbook document capture, isolation, mode selection and versioned regrading.

The offline [adapter](prepare_grading.py) verifies frozen seed and capture hashes,
preserves observable event IDs/actor edges, and copies relevant evidence into
manifest-limited packages. It excludes private reasoning and host notices. It
does not run actors, synthesize missing events or infer a total order across
concurrent reviewers. Eight tests exercise evidence boundaries and retention.

## Grader pin and provenance

- [Pin](inputs/pin.json): grader SHA-256
  `c2621b9a4f2f3e0d86cae6ec682b7ca1a2c729afb5da5cd9031873978b2dc342`;
  frozen revision-1 rubric SHA-256
  `d1e603beb45416e89e744f2a1cf9583de18d9882786441e69292232c3d2bdc27`.
- Actor baseline is unchanged
  `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; candidate code starts from repository
  `88a5b978c9d765bab429751b153c69a41132d29c` plus this Task 8 diff.
- [Seal validation](seal-validation.json) covers the 16 packages and five
  synthetic workflow controls (641 listed files). Original capture seals were
  validated before preparation. Each package retains the original manifest hash,
  source-event hashes and known completeness/redaction limits.
- [Actual baseline grader dispatches](grader-dispatches.json) and
  [calibration dispatches](calibration-dispatches.json) are controller
  transcriptions of this session's readable spawn calls and returned task IDs.
  Each grader is a fresh default agent with `fork_turns=none`, loading the pinned
  grader bytes rather than the installed legacy component-only role.
- The current collaboration runtime inherits the parent model/effort; its exact
  service model identifier is not exposed by these calls. This is instruction
  calibration and retained-trace grading, not registered-role/provider parity.
  Future comparisons must use this pinned implementation/rubric and a consistent
  declared grading runtime, or regrade both sides under a newly recorded pin.
- This host has no dedicated Read tool. The dispatches permit read-only
  `cat`/`sed` (and bounded `rg` for baseline evidence) as its read adapter. No
  filesystem allowlist is claimed. These grader prompts do not authorize live
  source/fixture reads, writes, tests or script execution.

The original preparation adapter is preserved as [adapter-source.txt](inputs/adapter-source.txt),
matching the pin. Independent review prompted stronger event/oracle allowlists
and a trusted-directory-alias correction. A fresh build with the corrected adapter
preserves **all 611 graded evidence files byte for byte**, recorded in
[equivalence evidence](adapter-fix-equivalence.json). The grader/rubric and sealed
packages were not changed or retroactively relabeled.

## Calibration and baseline results

[Calibration outputs](results/calibration.md) match all seven accepted controls:
early edit despite a reassuring final report FAIL; missing read events PARTIAL;
complete ordering PASS; complete omitted read FAIL; denied read FAIL; omitted and
explicit component modes both return the expected PASS/PARTIAL/FAIL rows. Two
initial component attempts supplied assertions by file path; they are retained
and superseded by fresh inline-input repetitions of the legacy contract.

[Baseline totals](results/summary.md): **51 PASS / 44 FAIL / 11 PARTIAL across 106
assertions in 16 runs**. Exact returned tables are retained for
[Claude R1](results/claude-r1.md), [Claude R3](results/claude-r3.md),
[Claude implementation](results/claude-implement.md) and [Codex](results/codex.md).
[Structured grades](results/grades.json) preserve composite scenario/assertion
identity, provider/mode/repetition, grader/rubric hashes and evidence citations.

Both Codex R1 standard baselines pass every assertion. Codex I1 detects the
conflict and stops, but does not durably record the blocker. Claude baselines
retain early investigation/edit findings, unsupported external corroboration,
incomplete historical comparisons and other case-specific failures. Some Claude
instruction entry-point reads and absent historical actions cannot be established
from the retained capture, so their grades remain PARTIAL. These are independent
grades under the frozen contract, not statistical model-reliability estimates.

The [input index](inputs/index.json) retains four UNRUN Codex R3-isolated/I2-
standalone records and three incomplete controller attempts. `ready-to-grade`
describes the immutable package-preparation state; the linked result tables
record its subsequent grade. No candidate workflows were run for this task.

## Verification and review

[Check summary](checks.json): all ten shell suites pass, with **644 helper
assertions**, including the existing 20 staging tests. The final
[adapter suite](adapter-tests-final.log) passes eight tests. Go tests and plugin
graph validation pass; the graph's existing cycle warning remains in its log.
[Second-generation freshness](freshness.json) verifies **725 generated files**
unchanged. The 51 frozen seed files and revision-1 rubric still match their freeze.

The first generator attempt could not write protected `.codex/agents`; approved
regeneration restored the complete output. Initial shell/Go checks could not
access existing uv/Go caches; approved retries passed. The first added stream
test exposed the platform directory alias, now covered by a regression. These
failed attempts remain in the logs; no persistent host setting changed.

[Independent review](review.md) records the isolated reviewer, corrections and
native PAL findings/coverage limits. PAL reported zero embedded/examined files,
so it does not establish corroboration or broad source coverage.

## Deferred work

Owner: implementing agent, under existing Tasks 2 gate 2B and 12. Complete the
bounded Codex capture investigation, select and record its authorized evidence
contract, and obtain the four missing baselines. If fallback is selected, add
receipt/use calibration and regrade affected retained baseline/candidate traces;
recapture both sides where evidence is insufficient. Do not amend this pin or
the original captures in place.

Task 12 also owns candidate comparisons, routing/pre-write controls and any
required recaptures of intermediate Task 4–6 runs. Verification condition: every
required candidate assertion passes twice with fresh inputs under the same
selected contract. Current FAIL/PARTIAL/UNRUN observations do not waive that gate.
Tasks 9–11 and feature completion remain open.

Reflection: separating output-text grading from observable execution exposed
both behavioral failures and capture limits. The review fixes tightened the
controller without altering already graded bytes; the recorded failed attempts
and incomplete evidence remain part of the result.
