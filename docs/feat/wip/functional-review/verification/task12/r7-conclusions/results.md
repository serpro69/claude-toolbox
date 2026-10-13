# Matched comparison results

Effective PASS / FAIL / PARTIAL counts. All 48 fresh captures and 336 original assertion observations are retained. [Explicit grading corrections](grade-corrections/README.md) override only the named rows; original grades are unchanged.

| Provider / side | PASS | FAIL | PARTIAL |
| --- | ---: | ---: | ---: |
| claude-baseline | 43 | 40 | 1 |
| claude-candidate | 72 | 12 | 0 |
| codex-baseline | 52 | 32 | 0 |
| codex-candidate | 75 | 9 | 0 |

| Run | PASS / FAIL / PARTIAL | Non-PASS assertion IDs |
| --- | --- | --- |
| [claude-baseline-R3-isolated-1](grades/claude-baseline-R3-isolated-1.md) | 4 / 4 / 0 | 7.1, 7.5, 7.6, 7.7 |
| [claude-baseline-R3-isolated-2](grades/claude-baseline-R3-isolated-2.md) | 0 / 7 / 1 | 7.1 (PARTIAL), 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8 |
| [claude-baseline-R3-standard-1](grades/claude-baseline-R3-standard-1.md) | 7 / 1 / 0 | 7.7 |
| [claude-baseline-R3-standard-2](grades/claude-baseline-R3-standard-2.md) | 7 / 1 / 0 | 7.7 |
| [claude-baseline-R5-isolated-1](grades/claude-baseline-R5-isolated-1.md) | 3 / 3 / 0 | 12.1, 12.4, 12.6 |
| [claude-baseline-R5-isolated-2](grades/claude-baseline-R5-isolated-2.md) | 3 / 3 / 0 | 12.1, 12.4, 12.6 |
| [claude-baseline-R5-standard-1](grades/claude-baseline-R5-standard-1.md) | 5 / 1 / 0 | 12.4 |
| [claude-baseline-R5-standard-2](grades/claude-baseline-R5-standard-2.md) | 5 / 1 / 0 | 12.4 |
| [claude-baseline-R7-isolated-1](grades/claude-baseline-R7-isolated-1.md) | 1 / 6 / 0 | 14.1, 14.2, 14.3, 14.4, 14.5, 14.7 |
| [claude-baseline-R7-isolated-2](grades/claude-baseline-R7-isolated-2.md) | 1 / 6 / 0 | 14.1, 14.2, 14.3, 14.4, 14.5, 14.7 |
| [claude-baseline-R7-standard-1](grades/claude-baseline-R7-standard-1.md) | 3 / 4 / 0 | 14.2, 14.3, 14.4, 14.6 |
| [claude-baseline-R7-standard-2](grades/claude-baseline-R7-standard-2.md) | 4 / 3 / 0 | 14.2, 14.3, 14.4 |
| [claude-candidate-R3-isolated-1](grades/claude-candidate-R3-isolated-1.md) | 6 / 2 / 0 | 7.5, 7.6 |
| [claude-candidate-R3-isolated-2](grades/claude-candidate-R3-isolated-2.md) | 6 / 2 / 0 | 7.5, 7.6 |
| [claude-candidate-R3-standard-1](grades/claude-candidate-R3-standard-1.md) | 8 / 0 / 0 | — |
| [claude-candidate-R3-standard-2](grades/claude-candidate-R3-standard-2.md) | 8 / 0 / 0 | — |
| [claude-candidate-R5-isolated-1](grades/claude-candidate-R5-isolated-1.md) | 5 / 1 / 0 | 12.6 |
| [claude-candidate-R5-isolated-2](grades/claude-candidate-R5-isolated-2.md) | 5 / 1 / 0 | 12.6 |
| [claude-candidate-R5-standard-1](grades/claude-candidate-R5-standard-1.md) | 6 / 0 / 0 | — |
| [claude-candidate-R5-standard-2](grades/claude-candidate-R5-standard-2.md) | 6 / 0 / 0 | — |
| [claude-candidate-R7-isolated-1](grades/claude-candidate-R7-isolated-1.md) | 6 / 1 / 0 | 14.7 |
| [claude-candidate-R7-isolated-2](grades/claude-candidate-R7-isolated-2.md) | 6 / 1 / 0 | 14.7 |
| [claude-candidate-R7-standard-1](grades/claude-candidate-R7-standard-1.md) | 5 / 2 / 0 | 14.3, 14.4 |
| [claude-candidate-R7-standard-2](grades/claude-candidate-R7-standard-2.md) | 5 / 2 / 0 | 14.3, 14.4 |
| [codex-baseline-R3-isolated-1](grades/codex-baseline-R3-isolated-1.md) | 5 / 3 / 0 | 7.5, 7.6, 7.7 |
| [codex-baseline-R3-isolated-2](grades/codex-baseline-R3-isolated-2.md) | 4 / 4 / 0 | 7.1, 7.5, 7.6, 7.7 |
| [codex-baseline-R3-standard-1](grades/codex-baseline-R3-standard-1.md) | 7 / 1 / 0 | 7.7 |
| [codex-baseline-R3-standard-2](grades/codex-baseline-R3-standard-2.md) | 7 / 1 / 0 | 7.7 |
| [codex-baseline-R5-isolated-1](grades/codex-baseline-R5-isolated-1.md) ([correction](grade-corrections/codex-baseline-R5-isolated-1.md)) | 5 / 1 / 0 | 12.6 |
| [codex-baseline-R5-isolated-2](grades/codex-baseline-R5-isolated-2.md) | 3 / 3 / 0 | 12.1, 12.5, 12.6 |
| [codex-baseline-R5-standard-1](grades/codex-baseline-R5-standard-1.md) | 5 / 1 / 0 | 12.5 |
| [codex-baseline-R5-standard-2](grades/codex-baseline-R5-standard-2.md) | 6 / 0 / 0 | — |
| [codex-baseline-R7-isolated-1](grades/codex-baseline-R7-isolated-1.md) | 1 / 6 / 0 | 14.1, 14.2, 14.3, 14.5, 14.6, 14.7 |
| [codex-baseline-R7-isolated-2](grades/codex-baseline-R7-isolated-2.md) | 2 / 5 / 0 | 14.2, 14.3, 14.4, 14.5, 14.7 |
| [codex-baseline-R7-standard-1](grades/codex-baseline-R7-standard-1.md) | 3 / 4 / 0 | 14.2, 14.3, 14.4, 14.5 |
| [codex-baseline-R7-standard-2](grades/codex-baseline-R7-standard-2.md) | 4 / 3 / 0 | 14.2, 14.3, 14.5 |
| [codex-candidate-R3-isolated-1](grades/codex-candidate-R3-isolated-1.md) | 5 / 3 / 0 | 7.5, 7.6, 7.7 |
| [codex-candidate-R3-isolated-2](grades/codex-candidate-R3-isolated-2.md) | 6 / 2 / 0 | 7.5, 7.6 |
| [codex-candidate-R3-standard-1](grades/codex-candidate-R3-standard-1.md) | 8 / 0 / 0 | — |
| [codex-candidate-R3-standard-2](grades/codex-candidate-R3-standard-2.md) | 8 / 0 / 0 | — |
| [codex-candidate-R5-isolated-1](grades/codex-candidate-R5-isolated-1.md) | 5 / 1 / 0 | 12.6 |
| [codex-candidate-R5-isolated-2](grades/codex-candidate-R5-isolated-2.md) | 5 / 1 / 0 | 12.6 |
| [codex-candidate-R5-standard-1](grades/codex-candidate-R5-standard-1.md) | 6 / 0 / 0 | — |
| [codex-candidate-R5-standard-2](grades/codex-candidate-R5-standard-2.md) | 6 / 0 / 0 | — |
| [codex-candidate-R7-isolated-1](grades/codex-candidate-R7-isolated-1.md) | 6 / 1 / 0 | 14.7 |
| [codex-candidate-R7-isolated-2](grades/codex-candidate-R7-isolated-2.md) | 6 / 1 / 0 | 14.7 |
| [codex-candidate-R7-standard-1](grades/codex-candidate-R7-standard-1.md) | 7 / 0 / 0 | — |
| [codex-candidate-R7-standard-2](grades/codex-candidate-R7-standard-2.md) ([correction](grade-corrections/codex-candidate-R7-standard-2.md)) | 7 / 0 / 0 | — |

Reject: both Claude candidate R7 standard repetitions fail 14.3/14.4. All four Codex and both Claude isolated R7 candidates meet 14.1–14.6; their required isolated PAL assertion still fails. All R5 candidate non-PAL rows pass. R3 retains the demonstrated incompatibility and named-reviewer historical use, but Codex candidate isolated repetition 1 omits the explicit Blocked classification from its final parent report (7.7 FAIL). Baseline R3 reports also omit it; this comparison does not establish a regression caused by the wording.

Candidate totals: 147 PASS / 21 FAIL / 0 PARTIAL. Of 21 failures, 16 are required PAL omissions, four are the Claude R7 target rows and one is the Codex R3 reporting gap. Baseline totals: 95 PASS / 72 FAIL / 1 PARTIAL. These counts are descriptive; comparison against the pre-feature baseline does not isolate incremental causality or establish reliability. Full-feature acceptance remains open.
