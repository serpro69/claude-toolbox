# Candidate 3 standard-mode results

Twenty fresh captures cover R1/R2/R4/R5/R6, both sides and two repetitions.
Each has raw sealed evidence in `runs/<run>/` and a hash-validated grader package
in `grading/<run>/`. [Structured grades](grades.json) preserve all 120 assertions.
Each run was graded by a fresh `eval-grader` role with no actor/author history,
using the pinned grader and revision-2 rubric. Agent names use `grade_c3_` plus
case/repetition; baseline names add `b_`.

| Case | Baseline rep 1 P/F/PARTIAL | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 |
| --- | --- | --- | --- | --- |
| R1 ownership | 2/4/0 | 2/4/0 | 5/1/0 | 6/0/0 |
| R2 retry | 2/4/0 | 2/4/0 | 4/2/0 | 3/3/0 |
| R4 persistence | 3/3/0 | 2/4/0 | 5/1/0 | 5/1/0 |
| R5 partial feature | 2/3/1 | 2/3/1 | 4/2/0 | 5/1/0 |
| R6 inherited defect | 3/3/0 | 4/2/0 | 6/0/0 | 4/2/0 |

Baseline: **24 PASS / 34 FAIL / 2 PARTIAL**. Candidate:
**47 PASS / 13 FAIL / 0 PARTIAL**. No case has two complete candidate PASSes,
so none establishes the declared two-run gate. These are descriptive results,
not statistical reliability or full-matrix/provider acceptance.

## Candidate findings and required follow-up

- R1: repetition 1 loads every detection rule and traces the correct documented
  lifecycle, but claims the full staged diff was checked after denied reads
  (e93/e102; report). Repetition 2 passes all six (contract/read e101/e105,
  complete scenario and truthful static-only report e141).
- R2: repetition 1 traces both failures but its remedy re-calls receipt on an
  already completed ID, and it overstates preference loss as catastrophic/P0
  (report). Repetition 2 never reads/carries the explicit edited-retry contract,
  omits that failure sequence and asks to decide already-specified retry semantics
  (e195). Both need contract-grounded corrections preserving completed repeats.
- R4: both identify the initial legacy-row failure, but neither reports the
  concrete one-record migration failure at the remaining legacy row and the
  fully migrated readable control (rep 1 e156; rep 2 report).
- R5: repetition 1 never reads README/tasks and proposes a future runtime-toggle
  refactor while admitting no current defect (e200). Repetition 2 correctly
  accepts the increment but recommends a test it acknowledges already exists
  (e162). Both require current-contract scope and proportionate suggestions.
- R6: repetition 1 passes all six, including source trace, inherited attribution
  and unknown historical settings (e84/e102–e106/e128; report). Repetition 2 lacks
  returned base/diff evidence after denial e95 and omits historical-setting
  uncertainty in e195 despite correct nonblocking inherited attribution.

Owner: implementing agent, Task 12. Preserve these failures. The next candidate
must address these general reasoning/reporting gaps, be separately frozen, and
rerun affected comparisons; do not patch actor reports or assertions.

## Grading consistency

The initial baseline R1 repetition 2 and R2 repetition 1 loading grades were PASS
based on Python checklist order alone. Their original graders independently
reassessed the unchanged packages and returned FAIL for seven omitted mandatory
detection lookups. The initial grades remain in grades.json. Subsequent grader
dispatches explicitly call attention to all mandatory lookups in the captured
procedure, including its ENOENT exceptions; the obligation/rubric is unchanged.
Runtime-emitted skill bodies remain in captured/events.jsonl even when omitted
by the older derived events.txt view.

PAL verification is user-deferred and no standard-mode dispatch obligation is
invented. Event-level material-access and scratch audits remain required before
using any successful observations for acceptance; no OS-wide confinement claim.
