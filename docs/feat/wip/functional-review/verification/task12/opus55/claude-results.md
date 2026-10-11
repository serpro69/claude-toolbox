# Claude comparison: Opus 5.5

All 96 declared Claude sessions are captured and independently graded. Each
side has 304 assertion observations: baseline **189 PASS / 114 FAIL / 1 PARTIAL**;
candidate **251 PASS / 49 FAIL / 4 PARTIAL**. Candidate passes every required
assertion in both repetitions for **9 of 24** case/mode combinations; baseline
does so for **2 of 24**. These descriptive counts do not establish statistical
reliability or feature acceptance. The [Codex comparison](codex-results.md) is
reported separately under its declared runtime.

Baseline is `c2d28c9e`; candidate is `581dd0e1`. Both use Claude Code 2.1.296,
`claude-opus-5-5`/high for main and child, frozen fixtures and revision-2 grading.
See the [contract](run-contract.md), [capture audit](audit.md) and individual
grades below. PAL remains explicitly deferred; missing required PAL evidence
is retained as FAIL. R8 results are synthetic report replays only.

Two initial baseline verdicts were corrected by their original graders after
examining overlooked, already-sealed raw Skill-delivery/startup events. The
[initial grades and correction requests](grading-revisions/) are preserved;
neither rubric nor actor evidence changed. Both corrections benefit baseline.

## Every repetition

Cells are **PASS / FAIL / PARTIAL assertion counts**, linked to the complete
independent verdict table. A PARTIAL never counts as PASS.

| Case | Mode | Baseline 1 | Baseline 2 | Candidate 1 | Candidate 2 |
|---|---|---|---|---|---|
| I1 | plan | [4/2/0](grades/claude-baseline-I1-plan-1.md) | [2/4/0](grades/claude-baseline-I1-plan-2.md) | [6/0/0](grades/claude-candidate-I1-plan-1.md) | [6/0/0](grades/claude-candidate-I1-plan-2.md) |
| I2 | standalone | [5/2/0](grades/claude-baseline-I2-standalone-1.md) | [5/2/0](grades/claude-baseline-I2-standalone-2.md) | [5/2/0](grades/claude-candidate-I2-standalone-1.md) | [5/2/0](grades/claude-candidate-I2-standalone-2.md) |
| I3 | standalone | [5/1/0](grades/claude-baseline-I3-standalone-1.md) | [4/1/1](grades/claude-baseline-I3-standalone-2.md) | [4/1/1](grades/claude-candidate-I3-standalone-1.md) | [5/0/1](grades/claude-candidate-I3-standalone-2.md) |
| I4 | plan | [5/4/0](grades/claude-baseline-I4-plan-1.md) | [6/3/0](grades/claude-baseline-I4-plan-2.md) | [7/2/0](grades/claude-candidate-I4-plan-1.md) | [8/1/0](grades/claude-candidate-I4-plan-2.md) |
| R1 | isolated | [3/3/0](grades/claude-baseline-R1-isolated-1.md) | [3/3/0](grades/claude-baseline-R1-isolated-2.md) | [4/2/0](grades/claude-candidate-R1-isolated-1.md) | [5/1/0](grades/claude-candidate-R1-isolated-2.md) |
| R1 | standard | [4/2/0](grades/claude-baseline-R1-standard-1.md) | [4/2/0](grades/claude-baseline-R1-standard-2.md) | [5/1/0](grades/claude-candidate-R1-standard-1.md) | [6/0/0](grades/claude-candidate-R1-standard-2.md) |
| R2 | isolated | [1/5/0](grades/claude-baseline-R2-isolated-1.md) | [1/5/0](grades/claude-baseline-R2-isolated-2.md) | [5/1/0](grades/claude-candidate-R2-isolated-1.md) | [5/1/0](grades/claude-candidate-R2-isolated-2.md) |
| R2 | standard | [5/1/0](grades/claude-baseline-R2-standard-1.md) | [5/1/0](grades/claude-baseline-R2-standard-2.md) | [6/0/0](grades/claude-candidate-R2-standard-1.md) | [6/0/0](grades/claude-candidate-R2-standard-2.md) |
| R3 | isolated | [4/4/0](grades/claude-baseline-R3-isolated-1.md) | [2/6/0](grades/claude-baseline-R3-isolated-2.md) | [2/6/0](grades/claude-candidate-R3-isolated-1.md) | [0/7/1](grades/claude-candidate-R3-isolated-2.md) |
| R3 | standard | [7/1/0](grades/claude-baseline-R3-standard-1.md) | [7/1/0](grades/claude-baseline-R3-standard-2.md) | [8/0/0](grades/claude-candidate-R3-standard-1.md) | [8/0/0](grades/claude-candidate-R3-standard-2.md) |
| R4 | isolated | [2/4/0](grades/claude-baseline-R4-isolated-1.md) | [0/6/0](grades/claude-baseline-R4-isolated-2.md) | [5/1/0](grades/claude-candidate-R4-isolated-1.md) | [5/1/0](grades/claude-candidate-R4-isolated-2.md) |
| R4 | standard | [4/2/0](grades/claude-baseline-R4-standard-1.md) | [4/2/0](grades/claude-baseline-R4-standard-2.md) | [6/0/0](grades/claude-candidate-R4-standard-1.md) | [6/0/0](grades/claude-candidate-R4-standard-2.md) |
| R5 | isolated | [3/3/0](grades/claude-baseline-R5-isolated-1.md) | [3/3/0](grades/claude-baseline-R5-isolated-2.md) | [4/2/0](grades/claude-candidate-R5-isolated-1.md) | [5/1/0](grades/claude-candidate-R5-isolated-2.md) |
| R5 | standard | [5/1/0](grades/claude-baseline-R5-standard-1.md) | [4/2/0](grades/claude-baseline-R5-standard-2.md) | [6/0/0](grades/claude-candidate-R5-standard-1.md) | [6/0/0](grades/claude-candidate-R5-standard-2.md) |
| R6 | isolated | [3/3/0](grades/claude-baseline-R6-isolated-1.md) | [4/2/0](grades/claude-baseline-R6-isolated-2.md) | [3/3/0](grades/claude-candidate-R6-isolated-1.md) | [5/1/0](grades/claude-candidate-R6-isolated-2.md) |
| R6 | standard | [6/0/0](grades/claude-baseline-R6-standard-1.md) | [6/0/0](grades/claude-baseline-R6-standard-2.md) | [5/1/0](grades/claude-candidate-R6-standard-1.md) | [5/1/0](grades/claude-candidate-R6-standard-2.md) |
| R7 | isolated | [1/6/0](grades/claude-baseline-R7-isolated-1.md) | [1/6/0](grades/claude-baseline-R7-isolated-2.md) | [5/2/0](grades/claude-candidate-R7-isolated-1.md) | [5/1/1](grades/claude-candidate-R7-isolated-2.md) |
| R7 | standard | [3/4/0](grades/claude-baseline-R7-standard-1.md) | [4/3/0](grades/claude-baseline-R7-standard-2.md) | [5/2/0](grades/claude-candidate-R7-standard-1.md) | [6/1/0](grades/claude-candidate-R7-standard-2.md) |
| R8-failure | replay | [5/0/0](grades/claude-baseline-R8-failure-replay-1.md) | [5/0/0](grades/claude-baseline-R8-failure-replay-2.md) | [5/0/0](grades/claude-candidate-R8-failure-replay-1.md) | [5/0/0](grades/claude-candidate-R8-failure-replay-2.md) |
| R8-zero | replay | [4/1/0](grades/claude-baseline-R8-zero-replay-1.md) | [4/1/0](grades/claude-baseline-R8-zero-replay-2.md) | [5/0/0](grades/claude-candidate-R8-zero-replay-1.md) | [5/0/0](grades/claude-candidate-R8-zero-replay-2.md) |
| R9-mismatch | isolated | [4/2/0](grades/claude-baseline-R9-mismatch-isolated-1.md) | [3/3/0](grades/claude-baseline-R9-mismatch-isolated-2.md) | [5/1/0](grades/claude-candidate-R9-mismatch-isolated-1.md) | [5/1/0](grades/claude-candidate-R9-mismatch-isolated-2.md) |
| R9-mismatch | standard | [5/1/0](grades/claude-baseline-R9-mismatch-standard-1.md) | [6/0/0](grades/claude-baseline-R9-mismatch-standard-2.md) | [6/0/0](grades/claude-candidate-R9-mismatch-standard-1.md) | [6/0/0](grades/claude-candidate-R9-mismatch-standard-2.md) |
| R9-recovery | isolated | [4/2/0](grades/claude-baseline-R9-recovery-isolated-1.md) | [4/2/0](grades/claude-baseline-R9-recovery-isolated-2.md) | [4/2/0](grades/claude-candidate-R9-recovery-isolated-1.md) | [5/1/0](grades/claude-candidate-R9-recovery-isolated-2.md) |
| R9-recovery | standard | [5/1/0](grades/claude-baseline-R9-recovery-standard-1.md) | [5/1/0](grades/claude-baseline-R9-recovery-standard-2.md) | [6/0/0](grades/claude-candidate-R9-recovery-standard-1.md) | [6/0/0](grades/claude-candidate-R9-recovery-standard-2.md) |

## Interpretation and remaining work

The candidate's complete two-repetition passes are I1 plan; R2, R3, R4, R5,
R9-mismatch and R9-recovery standard; and both R8 replays. This batch's R5
improvement does not alter any historical failed grade.

R6 standard regresses in both repetitions: candidate reports the inherited
defect but omits a bounded follow-up, whereas baseline passes. R3 isolated is
also worse in this batch, with failed history/evidence acquisition and an early
stop. R7 still contains unsupported compatibility claims. I2 leaves test
verification unestablished; I3 lacks an observable pre-edit assessment; I4
omits the final unverified-production qualification in both runs and skips
execution in one. Individual tables distinguish confirmed failures from
unobserved components.

Several Claude isolated/implementation traces interpret a denied shell command
as general Bash unavailability and fail to obtain diffs or run tests. The
frozen policy permits specific Git/Python commands; an unattempted Git command
must not be described as a denied Git request. The policy was not changed
during this comparison. PAL deferral is additional to these failures.

Owner: implementing agent. The separate Codex matrix and final audit are now
complete. Any later repair needs its own candidate identity and fresh affected
pairs, preserving all present results. Legacy routing controls, live PAL checks
and Task 13 remain separate gates; Task 12 acceptance is not complete.
