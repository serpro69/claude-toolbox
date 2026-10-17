# Task 12.12: keep the isolated-review entry-path correction

All **12 declared sessions** completed and were independently graded. The
candidate meets the bounded diagnostic conditions twice for R3, R5 and
R9-recovery. **Keep the two-word command correction.** Feature acceptance remains
incomplete; PAL-dependent assertions retain FAIL and other Task 12 gates remain.

The change supplies explicit plugin-root paths to the existing skill and isolated
workflow. Common instructions are unchanged, with no new actor phase, permission,
dependency or retry protocol. Both generation passes preserve all 902 Codex files;
these are Claude-only observations, not a new Codex behavioral result.

## Comparison and results

Baseline `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`; candidate
`51cffecec1d912896dfcb4e48dc741f93ea250e1`, from a temporary source commit after
assessment commit `c84fc0f7`. Both sides use Claude 2.1.296, Opus 5.5/high for
parent/forced child, unchanged fixtures and revision-2 grading. The
[successor contract](run-contract.md), [freeze](freeze.json) and
[source provenance](source-provenance.json) retain the complete identities.

Cells are **PASS / FAIL / PARTIAL**, linked to complete independent grades.

| Case, isolated mode | Baseline 1 | Baseline 2 | Candidate 1 | Candidate 2 |
| --- | --- | --- | --- | --- |
| R3, historical provider | [4/4/0](grades/claude-baseline-R3-isolated-1.md) | [4/4/0](grades/claude-baseline-R3-isolated-2.md) | [6/2/0](grades/claude-candidate-R3-isolated-1.md) | [6/2/0](grades/claude-candidate-R3-isolated-2.md) |
| R5, clean partial feature | [3/3/0](grades/claude-baseline-R5-isolated-1.md) | [4/2/0](grades/claude-baseline-R5-isolated-2.md) | [5/1/0](grades/claude-candidate-R5-isolated-1.md) | [5/1/0](grades/claude-candidate-R5-isolated-2.md) |
| R9, justified recovery | [4/2/0](grades/claude-baseline-R9-recovery-isolated-1.md) | [1/5/0](grades/claude-baseline-R9-recovery-isolated-2.md) | [5/1/0](grades/claude-candidate-R9-recovery-isolated-1.md) | [5/1/0](grades/claude-candidate-R9-recovery-isolated-2.md) |

Totals: baseline **20 PASS / 20 FAIL / 0 PARTIAL**; candidate **32 PASS / 8 FAIL /
0 PARTIAL**.

[Machine-readable results](results.json) contain all **80 assertion observations**.
The eight candidate FAILs are the original composite PAL requirements: R3 7.5/7.6,
R5 12.6 and R9-recovery 11.6 in both repetitions. Their named-reviewer components
are evidenced in the individual grades; no aggregate FAIL has been converted to
PASS or omitted from totals.

Both R3 candidates load instructions before investigation, acquire and materialize
the historical provider with provenance, supply it to the named reviewer, trace
the disabled-save incompatibility and report Blocked/REQUEST_CHANGES qualified
to inspected source. Both R5 candidates approve the compatible increment without
invented follow-up work. Both R9 candidates preserve required bounded recovery,
with execution and source-only evidence distinguished. Neither candidate repetition
stops at entry discovery or fails a required non-PAL control.

The baseline retains instruction-ordering failures, incomplete handoffs/reporting,
an unsupported R5 suggestion and one R9 early stop. These are observations under
this declaration. The baseline predates the whole feature; it is not the immediate
pre-correction candidate. This comparison does **not** isolate the causal effect
of two words, establish statistical reliability or supersede the full matrix.

## Runtime change and loading evidence

The [initial candidate probe](../entry-path/runtime-change.md) unexpectedly found
PAL connected, although its launcher matched the previous full matrix. It finished
without a PAL tool call before a stop request could interrupt it. Preserve that
probe and its original freeze; no measured run used that configuration.

The [reviewed successor](review.md) explicitly omits PAL from the run-local MCP
file actually selected by the CLI. Original runtime configuration remains retained
for provenance. No normal user configuration, ordinary prompt, tool permission
policy or model changed. Fresh baseline and candidate probes both passed the
[binding audit](binding-audit.json): Capy connected, PAL absent, selected-bundle
instruction receipt, linked named reviewer and unchanged subjects. Candidate
command delivery contains the two substituted paths directly. There are three
retained loading probes in total, separate from the twelve measured workflows.

## Verification and integrity

- [Initial source review](../entry-path/review.md) and [configuration review](review.md)
  both approve their scoped changes with no findings. All eleven shell suites
  pass **645 assertions**; generation/structure and Go/graph checks pass. Nineteen
  existing capture regressions and four successor adapter controls pass; the three
  initial adapter controls are also retained. See [initial checks](../entry-path/checks/)
  and [successor checks](checks/).
- [The final audit](audit.json) verifies twelve sealed captures (**582 files**),
  twelve grading packages (**1,835 files**), all eighty grade identities, frozen
  source/fixtures/controllers, runtime configurations, actor bundles, Git refs and
  staged patches. All subject files remain unchanged. Parent/child messages use
  Opus 5.5; every measured startup contains only Capy, and no PAL tool call occurs.
- All **534 tool requests**, including **93 shell requests**, were inspected for
  material access. No evaluator file-content read was observed. One baseline R5
  Glob returned external instruction filenames; subsequent reads stayed within
  its selected bundle/workspace/evidence. This metadata exposure is retained and
  does not establish OS-wide confinement. A write to an existing fixed-name temp
  file was denied; it was not read or used and remains untouched.
- [Cleanup](cleanup.json) removes **21 proven-owned directories and six newly
  created files** only after their contents/hashes are retained in
  [temporary evidence](temporary-evidence/). The pre-existing path and unproven
  parent directories remain untouched. Actual runtime inputs are retained under
  [runtime-inputs](runtime-inputs/); [source archives and manifests](source-inputs/manifest.json)
  preserve exact actor inputs beyond the temporary repositories' lifetimes.

The serial capture process exited 0, with no measured transport/finalization
failure. [Its log](checks/batch.log) retains preparation and completion order.
Independent graders used the unchanged pinned rubric/implementation and prior
[calibration](../opus55/calibration.md); exact grader service telemetry remains
unavailable. No new actor iteration, grading exception or permission expansion
followed the results.

## Remaining scope

This is a successful bounded experiment, not full feature acceptance. PAL,
unresolved dispositions from Task 12.11, legacy routing/pre-write controls and
Task 13 remain open. R7 unsupported compatibility claims retain investigation
priority; no additional operative fix is selected or started here. Owner:
implementing agent. [Final independent review](completion-review.md) approved
this completion record and bounded keep decision with no findings; Task 12.12
is complete.
