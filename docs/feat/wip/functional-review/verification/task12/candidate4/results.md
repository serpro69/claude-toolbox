# Candidate 4 standard-mode results

**The two-run acceptance gate fails.** No tested case has two candidate runs
passing every required assertion. The source changes remain an unaccepted draft.

Fourteen fresh captures comprise twelve candidate runs (R1–R6 standard, two
each) and two baseline R3-standard runs. As declared before measurement, both
baseline repetitions for R1/R2/R4/R5/R6 come from the matching candidate-3 batch;
all failures and partials are retained. Actor, fixture, ordinary prompt, rubric,
grader, runtime and permission identities remain fixed for those reused baselines.

Raw sealed evidence is in `runs/<run>/`; hash-validated grader inputs are in
`grading/<run>/`. [Structured grades](grades.json) preserve all 92 newly graded
assertions. Every run received a fresh isolated `eval-grader` role using the
pinned grader and revision-2 rubric, with no live fixture or author context.
Runtime-emitted skill bodies are retained in `captured/events.jsonl`; the older
derived `events.txt` view omits these synthetic user messages. Graders were told
to inspect the captured stream when the derived view lacked instruction bytes.

| Case | Baseline rep 1 P/F/PARTIAL | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 |
| --- | --- | --- | --- | --- |
| R1 ownership | 2/4/0 | 2/4/0 | 4/2/0 | 4/2/0 |
| R2 retry | 2/4/0 | 2/4/0 | 5/1/0 | 6/0/0 |
| R3 released provider | 0/8/0 | 7/1/0 | 2/6/0 | 8/0/0 |
| R4 persistence | 3/3/0 | 2/4/0 | 4/2/0 | 4/2/0 |
| R5 partial feature | 2/3/1 | 2/3/1 | 5/1/0 | 5/1/0 |
| R6 inherited defect | 3/3/0 | 4/2/0 | 6/0/0 | 4/2/0 |

Matched baseline: **31 PASS / 43 FAIL / 2 PARTIAL**. Candidate:
**57 PASS / 19 FAIL / 0 PARTIAL**. These counts describe this tuned sample;
they do not establish statistical reliability, a completed matrix or provider
parity. Earlier candidate successes do not satisfy this revision's threshold.

## Candidate evidence

- R1 repetition 1: subject reads/diffs e40/e55/e61 precede detection e94 and
  checklists e105–e111; seven mandatory detection rules are omitted. The report
  models two completed setups rather than the documented failed setup, queued
  cleanup and successful replacement. Repetition 2 similarly reads the diff at
  e46/e49 before guidance e52/e64–e70 and repeats the wrong lifecycle in e126.
- R2 repetition 1: diff e60/e63 precedes index e71/checklists e75–e81; all five
  semantic, remedy, severity and testing assertions pass. Repetition 2 loads all
  eight detection rules e41–e55 and checklists e67–e73 before diff e80, then passes
  all six assertions with the required scenarios, completed-ID invariant and P1.
- R3 repetition 1: diff e65 precedes detection e69/checklists e125–e131. No README
  or historical provider read appears; report e173 admits the provider was not
  inspected and infers compatibility. Repetition 2 completes instructions before
  subject reads e99/e103, obtains actual history e136/e139 and gives a
  source-qualified Blocked/REQUEST_CHANGES result at e182; all eight pass.
- R4 repetition 1: full diff e47 precedes detection e49–e63/checklists e75–e81;
  report e188 omits the concrete one-record migration failure at `legacy-c`.
  Repetition 2 reads source e43/e60 before checklists e68–e74, omits seven detection
  rules and does not report the partial-batch failure and completed control.
- R5: both repetitions load instructions and trace the current contract correctly.
  Both nevertheless recommend a runtime-configuration refactor they describe as
  “not a current defect” (reports; repetition 1 e173), failing the scoped,
  proportionate-suggestion assertion.
- R6 repetition 1 passes all six: diff e79, trace e96/e98/e100, historical-setting
  uncertainty e123 and report e158. Repetition 2 reads diffs e43/e46 before
  guidance e48–e81 and falsely says README prose was updated in report e153,
  although only formatter and test code changed.

The two new R3 baseline grades also remain visible. Repetition 1 reads only
Python/twelve-factor detection, misses README/history and the independent-release
contract, infers provider behavior at e129 and suggests removing a parameter
without preserving the delivery constraint: eight FAILs. Repetition 2 omits seven
detection rules but obtains actual historical source e77–e80 and reports the
qualified incompatibility and compatible remedy at e140: seven PASSes, one FAIL.

## Stop and remaining obligations

The loaded /kk:implement skill requires stopping when verification fails
repeatedly. After these repeated failures, no further actors were launched.
The user was asked whether to rework the workflow design or leave this failed
gate recorded. Finishing grades and retaining evidence does not waive that gate.

Owner: implementing agent, Task 12. A continuation must resolve the workflow
ordering/reasoning failures, separately identify and freeze any successor source,
repair the capture-runner issues in [the independent review](../review.md), and
rerun the affected comparisons. Full material-access audits remain necessary
before acceptance; hash integrity alone does not establish read confinement.
Latest-source isolated runs, R7/R9, implementation cases, Codex representative
checks and legacy actor controls remain unrun. PAL-dependent verification,
including R8 replays, remains temporarily deferred by the user. Exact submitted
prompt parity remains unverified under the selected receipt/use contract.
