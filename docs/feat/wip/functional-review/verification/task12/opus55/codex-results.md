# Codex comparison

All 96 declared Codex sessions are captured and independently graded. Each
side has 304 assertion observations: baseline **203 PASS / 96 FAIL / 5 PARTIAL**;
candidate **264 PASS / 30 FAIL / 10 PARTIAL**. Candidate passes every required
assertion twice for **7 of 24** case/mode combinations; baseline does so for
**3 of 24**. These are descriptive results, not feature acceptance or statistical
reliability claims. Every repetition is retained below.

Baseline is `c2d28c9e`; candidate is `581dd0e1`. Both use Codex 0.162.1,
main `gpt-6-astra`/xhigh and named reviewer `gpt-6.1-sol`/xhigh, under the
[frozen contract](run-contract.md). See the [integrity audit](audit.md).
PAL remains explicitly deferred. Required missing PAL evidence remains FAIL;
R8 is synthetic reporting only. Exact submitted handoff text remains unverified
unless the individual evidence establishes it; only R3 7.5/7.6 and I2 9.5 have
the declared receipt/use fallback.

## Every repetition

Cells are **PASS / FAIL / PARTIAL assertion counts**, linked to complete
independent verdict tables. Neither PARTIAL nor FAIL passes acceptance.

| Case | Mode | Baseline 1 | Baseline 2 | Candidate 1 | Candidate 2 |
|---|---|---|---|---|---|
| I1 | plan | [2/4/0](grades/codex-baseline-I1-plan-1.md) | [2/4/0](grades/codex-baseline-I1-plan-2.md) | [5/0/1](grades/codex-candidate-I1-plan-1.md) | [6/0/0](grades/codex-candidate-I1-plan-2.md) |
| I2 | standalone | [5/2/0](grades/codex-baseline-I2-standalone-1.md) | [6/1/0](grades/codex-baseline-I2-standalone-2.md) | [6/1/0](grades/codex-candidate-I2-standalone-1.md) | [6/1/0](grades/codex-candidate-I2-standalone-2.md) |
| I3 | standalone | [3/1/2](grades/codex-baseline-I3-standalone-1.md) | [3/2/1](grades/codex-baseline-I3-standalone-2.md) | [5/0/1](grades/codex-candidate-I3-standalone-1.md) | [4/0/2](grades/codex-candidate-I3-standalone-2.md) |
| I4 | plan | [5/3/1](grades/codex-baseline-I4-plan-1.md) | [5/3/1](grades/codex-baseline-I4-plan-2.md) | [7/1/1](grades/codex-candidate-I4-plan-1.md) | [7/1/1](grades/codex-candidate-I4-plan-2.md) |
| R1 | isolated | [5/1/0](grades/codex-baseline-R1-isolated-1.md) | [5/1/0](grades/codex-baseline-R1-isolated-2.md) | [5/1/0](grades/codex-candidate-R1-isolated-1.md) | [5/1/0](grades/codex-candidate-R1-isolated-2.md) |
| R1 | standard | [6/0/0](grades/codex-baseline-R1-standard-1.md) | [6/0/0](grades/codex-baseline-R1-standard-2.md) | [6/0/0](grades/codex-candidate-R1-standard-1.md) | [6/0/0](grades/codex-candidate-R1-standard-2.md) |
| R2 | isolated | [4/2/0](grades/codex-baseline-R2-isolated-1.md) | [4/2/0](grades/codex-baseline-R2-isolated-2.md) | [5/1/0](grades/codex-candidate-R2-isolated-1.md) | [5/1/0](grades/codex-candidate-R2-isolated-2.md) |
| R2 | standard | [5/1/0](grades/codex-baseline-R2-standard-1.md) | [5/1/0](grades/codex-baseline-R2-standard-2.md) | [6/0/0](grades/codex-candidate-R2-standard-1.md) | [5/1/0](grades/codex-candidate-R2-standard-2.md) |
| R3 | isolated | [4/4/0](grades/codex-baseline-R3-isolated-1.md) | [4/4/0](grades/codex-baseline-R3-isolated-2.md) | [5/2/1](grades/codex-candidate-R3-isolated-1.md) | [6/2/0](grades/codex-candidate-R3-isolated-2.md) |
| R3 | standard | [7/1/0](grades/codex-baseline-R3-standard-1.md) | [7/1/0](grades/codex-baseline-R3-standard-2.md) | [8/0/0](grades/codex-candidate-R3-standard-1.md) | [7/0/1](grades/codex-candidate-R3-standard-2.md) |
| R4 | isolated | [3/3/0](grades/codex-baseline-R4-isolated-1.md) | [3/3/0](grades/codex-baseline-R4-isolated-2.md) | [5/1/0](grades/codex-candidate-R4-isolated-1.md) | [5/1/0](grades/codex-candidate-R4-isolated-2.md) |
| R4 | standard | [4/2/0](grades/codex-baseline-R4-standard-1.md) | [4/2/0](grades/codex-baseline-R4-standard-2.md) | [5/0/1](grades/codex-candidate-R4-standard-1.md) | [6/0/0](grades/codex-candidate-R4-standard-2.md) |
| R5 | isolated | [4/2/0](grades/codex-baseline-R5-isolated-1.md) | [4/2/0](grades/codex-baseline-R5-isolated-2.md) | [5/1/0](grades/codex-candidate-R5-isolated-1.md) | [5/1/0](grades/codex-candidate-R5-isolated-2.md) |
| R5 | standard | [5/1/0](grades/codex-baseline-R5-standard-1.md) | [5/1/0](grades/codex-baseline-R5-standard-2.md) | [6/0/0](grades/codex-candidate-R5-standard-1.md) | [6/0/0](grades/codex-candidate-R5-standard-2.md) |
| R6 | isolated | [2/4/0](grades/codex-baseline-R6-isolated-1.md) | [3/3/0](grades/codex-baseline-R6-isolated-2.md) | [3/2/1](grades/codex-candidate-R6-isolated-1.md) | [5/1/0](grades/codex-candidate-R6-isolated-2.md) |
| R6 | standard | [4/2/0](grades/codex-baseline-R6-standard-1.md) | [4/2/0](grades/codex-baseline-R6-standard-2.md) | [4/2/0](grades/codex-candidate-R6-standard-1.md) | [4/2/0](grades/codex-candidate-R6-standard-2.md) |
| R7 | isolated | [1/6/0](grades/codex-baseline-R7-isolated-1.md) | [1/6/0](grades/codex-baseline-R7-isolated-2.md) | [6/1/0](grades/codex-candidate-R7-isolated-1.md) | [6/1/0](grades/codex-candidate-R7-isolated-2.md) |
| R7 | standard | [2/5/0](grades/codex-baseline-R7-standard-1.md) | [3/4/0](grades/codex-baseline-R7-standard-2.md) | [7/0/0](grades/codex-candidate-R7-standard-1.md) | [7/0/0](grades/codex-candidate-R7-standard-2.md) |
| R8-failure | replay | [5/0/0](grades/codex-baseline-R8-failure-replay-1.md) | [5/0/0](grades/codex-baseline-R8-failure-replay-2.md) | [5/0/0](grades/codex-candidate-R8-failure-replay-1.md) | [5/0/0](grades/codex-candidate-R8-failure-replay-2.md) |
| R8-zero | replay | [5/0/0](grades/codex-baseline-R8-zero-replay-1.md) | [4/1/0](grades/codex-baseline-R8-zero-replay-2.md) | [5/0/0](grades/codex-candidate-R8-zero-replay-1.md) | [5/0/0](grades/codex-candidate-R8-zero-replay-2.md) |
| R9-mismatch | isolated | [5/1/0](grades/codex-baseline-R9-mismatch-isolated-1.md) | [5/1/0](grades/codex-baseline-R9-mismatch-isolated-2.md) | [5/1/0](grades/codex-candidate-R9-mismatch-isolated-1.md) | [5/1/0](grades/codex-candidate-R9-mismatch-isolated-2.md) |
| R9-mismatch | standard | [6/0/0](grades/codex-baseline-R9-mismatch-standard-1.md) | [6/0/0](grades/codex-baseline-R9-mismatch-standard-2.md) | [6/0/0](grades/codex-candidate-R9-mismatch-standard-1.md) | [6/0/0](grades/codex-candidate-R9-mismatch-standard-2.md) |
| R9-recovery | isolated | [4/2/0](grades/codex-baseline-R9-recovery-isolated-1.md) | [3/3/0](grades/codex-baseline-R9-recovery-isolated-2.md) | [5/1/0](grades/codex-candidate-R9-recovery-isolated-1.md) | [5/1/0](grades/codex-candidate-R9-recovery-isolated-2.md) |
| R9-recovery | standard | [5/1/0](grades/codex-baseline-R9-recovery-standard-1.md) | [5/1/0](grades/codex-baseline-R9-recovery-standard-2.md) | [6/0/0](grades/codex-candidate-R9-recovery-standard-1.md) | [6/0/0](grades/codex-candidate-R9-recovery-standard-2.md) |

## Interpretation and remaining work

R1 and R9-mismatch standard pass on both sides. Candidate R5, R7, both R8
replays and R9-recovery standard pass every assertion twice. The candidate's
R7 reports distinguish a local Git base from deployment compatibility, retain
Unknown where evidence is absent, and request bounded contract/revision evidence.

R2 standard still omits the explanation of test gaps in one candidate run.
R6 standard misses the inherited empty detailed-input defect in both baseline
and candidate runs. Candidate isolated R6 reviewers find it, but repetition 1
surfaces it in the final report without the required bounded follow-up.
Repetition 2 omits the advisory from its final report, so that conditional
follow-up requirement does not apply. The individual grades retain this distinction.

Some candidate runs lack captured SKILL.md delivery despite completed common
and profile instruction reads. These are PARTIAL evidence gaps, not proof of
an actual skipped load. I3 makes the exact requested correction in both runs,
but its submitted reviewer handoff arguments remain unavailable; its receipt/use
evidence cannot receive the exception declared only for R3 and I2.

I4 preserves the hard specification and protected files, reopens the failed
implementation item, records an explicit repair owner and separates the allowed
activation prerequisite. Its first candidate run begins a source read before
task/design/implementation context loading completes. Its second final response
omits the production-state qualification. Both I4 reviewer handoffs remain
PARTIAL because actual submitted arguments are not captured; no I4 receipt/use
fallback is declared.

The [preserved initial I3 grades and clarification requests](grading-revisions/)
record two corrections by the original graders: baseline repetition 2's
pre-edit assessment and candidate repetition 1's handoff each changed from PASS
to PARTIAL. Inputs and rubric remained unchanged. Raw captured protocol results
were also used where paginated/derived copies shortened successful reads.

Owner: implementing agent. Capture, grading and final audits are complete. Any
later actor repair or evidence-contract amendment needs a separately identified
comparison and fresh affected pairs. Legacy routing controls, live PAL checks
and Task 13 remain separate gates; this matrix does not establish feature
acceptance or statistical reliability.
