# Claude comparison results — Task 12.13

All 24 Claude sessions are captured and independently graded. Each side has
84 assertion observations. The candidate fails the bounded keep criterion: both
R7 standard repetitions still overstate provider/deployment compatibility.
Source remains frozen while the declared Codex comparison completes.

| Case / mode | Baseline rep 1 (P/F/Partial) | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 |
| --- | --- | --- | --- | --- |
| R3 / standard | [7/1/0](grades/claude-baseline-R3-standard-1.md) | [7/1/0](grades/claude-baseline-R3-standard-2.md) | [8/0/0](grades/claude-candidate-R3-standard-1.md) | [8/0/0](grades/claude-candidate-R3-standard-2.md) |
| R3 / isolated | [4/4/0](grades/claude-baseline-R3-isolated-1.md) | [0/7/1](grades/claude-baseline-R3-isolated-2.md) | [6/2/0](grades/claude-candidate-R3-isolated-1.md) | [6/2/0](grades/claude-candidate-R3-isolated-2.md) |
| R5 / standard | [5/1/0](grades/claude-baseline-R5-standard-1.md) | [5/1/0](grades/claude-baseline-R5-standard-2.md) | [6/0/0](grades/claude-candidate-R5-standard-1.md) | [6/0/0](grades/claude-candidate-R5-standard-2.md) |
| R5 / isolated | [3/3/0](grades/claude-baseline-R5-isolated-1.md) | [3/3/0](grades/claude-baseline-R5-isolated-2.md) | [5/1/0](grades/claude-candidate-R5-isolated-1.md) | [5/1/0](grades/claude-candidate-R5-isolated-2.md) |
| R7 / standard | [3/4/0](grades/claude-baseline-R7-standard-1.md) | [4/3/0](grades/claude-baseline-R7-standard-2.md) | [5/2/0](grades/claude-candidate-R7-standard-1.md) | [5/2/0](grades/claude-candidate-R7-standard-2.md) |
| R7 / isolated | [1/6/0](grades/claude-baseline-R7-isolated-1.md) | [1/6/0](grades/claude-baseline-R7-isolated-2.md) | [6/1/0](grades/claude-candidate-R7-isolated-1.md) | [6/1/0](grades/claude-candidate-R7-isolated-2.md) |

Totals: baseline **43 PASS / 40 FAIL / 1 PARTIAL**; candidate **72 PASS /
12 FAIL / 0 PARTIAL**. Every assertion identity is present exactly once.

Candidate R3 and R5 meet their local conditions in both modes/repetitions.
Both isolated R7 candidates meet 14.1–14.6; required PAL absence still fails
14.7. Eight candidate failures include absent PAL; four are the two standard
R7 runs failing both 14.3 and 14.4. No failure is waived.

In [standard repetition 1](grading/claude-candidate-R7-standard-1/captured/report.md),
the report calls provider compatibility Supported while admitting the provider
contract was not inspected, then conditions full approval only on string callers.
[Standard repetition 2](grading/claude-candidate-R7-standard-2/captured/report.md)
similarly closes with “fine to deploy” for strings-only callers despite unknown
provider/deployment evidence. Both had successful complete methodology receipts;
these are observed conclusion failures, not absent instruction-delivery evidence.

These comparisons use the pre-feature baseline. They do not isolate the causal
effect of the 28-word replacement or establish model reliability from two runs.
The candidate cannot be accepted merely because its overall counts improve.
The remaining declared comparison, final audit and rejection record are pending.
