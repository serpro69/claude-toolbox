# Opus 5.5 full functional matrix

Status: **rerun complete; candidate acceptance unmet**. All **192 core sessions**
completed and were independently graded: Claude and Codex, all 24 applicable
case/mode combinations, baseline and candidate, two fresh repetitions each.
There are no unrun core cells or measured transport/finalization failures.

The CLI upgrade resolved Opus 5.5 startup: Claude Code 2.1.296 ran
`claude-opus-5-5`; Codex 0.162.1 ran `gpt-6-astra`/xhigh with the named
`gpt-6.1-sol`/xhigh reviewer. Baseline is `c2d28c9e`; candidate is `581dd0e1`.
PAL remains user-deferred, and R8 uses synthetic reporting checkpoints.

## Results

Each side/provider has 304 assertion observations. Cells below are
**PASS / FAIL / PARTIAL**; required PAL components remain in those counts.
PARTIAL never counts as PASS. All-pass combinations require every assertion to
pass in both repetitions.

| Provider | Baseline | Candidate | All-pass combinations, baseline → candidate |
|---|---|---|---|
| [Claude](claude-results.md) | 189 / 114 / 1 | 251 / 49 / 4 | 2/24 → 9/24 |
| [Codex](codex-results.md) | 203 / 96 / 5 | 264 / 30 / 10 | 3/24 → 7/24 |

The complete matrix contains **1,216 assertion observations**: 907 PASS,
289 FAIL and 20 PARTIAL across both sides/providers. These are descriptive
two-run results, not statistical reliability or untested-provider parity claims.

- Candidate R5 standard and both R8 replays pass twice on both providers.
  R8 establishes synthetic reporting behavior only.
- R6 remains a substantive gap. Claude candidate standard regresses in both
  runs by omitting a bounded follow-up for an inherited defect. Codex standard
  misses the defect on both sides; candidate isolated detection improves, but
  one final report still omits the required follow-up.
- Other failures remain outside PAL: Claude has historical/diff acquisition,
  lifecycle, verification and uncertainty-reporting gaps; Codex retains a test
  coverage explanation omission and I4 ordering/final-report failures.
- Some Codex instruction deliveries and submitted handoffs remain unverified.
  I3/I4 do not receive the receipt/use exception reserved for R3 and I2.
  Individual grades distinguish evidence gaps from demonstrated actor failures.

## Evidence and integrity

- [Frozen contract](run-contract.md), [declaration](declaration.json), and
  [freeze](freeze.json) identify the exact actor sources, fixtures, prompts,
  runtimes, permissions, capture code, assertions and grader.
- [Binding](binding.md) verifies both providers and sides; [calibration](calibration.md)
  records ten successful grader controls; [runner review](review.md) records
  approved source and passing offline regressions.
- [Runs](runs/) contain fresh prepared inputs and completed sealed captures.
- [Grading inputs](grading/) contain verified sealed packages; [grades](grades/)
  retain all 192 independent verdict tables. [Initial grades and clarification
  records](grading-revisions/) preserve the four corrected judgments; neither
  actor evidence nor the rubric changed.
- [Final audit](audit.md#final-batch-audit) verifies all 7,884 capture files,
  192 actor bundles, runtime configurations, Git references and 21,023 grading
  files. Every required assertion appears exactly once per run. No evaluator
  access was observed in the targeted trace audits; OS-wide read confinement
  and exact submitted-prompt parity are not claimed.
- All temporary evaluation trust/plugin registrations and both evaluation
  cache roots were removed. Original review fixtures remain unchanged; five
  runs add only retained report artifacts.

The serial controller is `matrix.py`. Its stdout/stderr log is
`/tmp/fr-opus55-matrix-run.log`; model transports and results are retained per
run. It exited with status 0. Failed old-CLI probes, earlier source comparisons,
and all unfavorable observations remain preserved and are not pooled with this
configuration. No actor repairs or extra success-seeking repetitions were run.

## Remaining acceptance gates

Owner: implementing agent. Task 12 acceptance remains in progress and Task 13
remains pending. This requested measurement is complete; it does not waive the
following feature gates.

| Gate | Reason | Next action and verification condition |
|---|---|---|
| Behavioral failures | Required assertions fail in the fixed candidate | Identify a bounded successor candidate; rerun affected matching pairs and require every required component twice. Preserve this batch. |
| Evidence gaps | Some instruction/handoff content is not captured | Establish the required evidence, or explicitly version the contract before fresh matching comparisons; never retroactively infer missing content. |
| Live PAL | Explicit user deferral | When resumed, restore the declared launcher and verify actual receipt/use and integration under matching configurations. Synthetic R8 results do not substitute. |
| Legacy controls and Task 13 | Separate gates outside the 192 core sessions | Run the remaining routing/pre-write controls and final feature documentation/verification before claiming feature acceptance. |
