# Task 4 PR evaluations — 2026-09-29

All five assigned scenarios have executed and their latest applicable results are
**26 PASS, 0 PARTIAL, 0 FAIL**. Final procedure compliance, fidelity, visibility and
observed isolation pass; the final grader retains the four other latest passing
cases as applicable. No assigned scenario is authored-but-unrun. This group owns evidence only; the main agent owns operative
instruction changes and permanent assertion13.8.

| Scenario | Latest evidence | Assertion result | Original → revised answers | Final-instruction applicability |
| --- | --- | --- | --- | --- |
| Contract-only PR | [Initial run](contract-only-pr/run.md) | 5 PASS | 1/5 → 5/5 | RETAIN PASS |
| Runtime PR | [Corrected-instruction retry](runtime-pr/retry-1/run.md) | 6 PASS | 0/5 → 5/5 | RETAIN PASS |
| Destination visibility | [Explicit-outcome retry](destination-visibility/retry-3/run.md) | 8 PASS | 5/5 → 5/5 | Direct final-snapshot execution |
| Missing context | [Initial run](pr-missing-context/run.md) | 3 PASS | Not applicable | RETAIN PASS |
| Unavailable source | [Initial run](pr-unavailable-source/run.md) | 4 PASS | 4/5 → 5/5 | RETAIN PASS |

Each run index links its exact manifests/requests, thread IDs, before/after artifacts,
reader answers, raw/readable traces, input/output/instruction hashes, actual Git
evidence and independent verdicts. Initial repository HEAD is
`9a7ad32eef89a3b8c9b366292ac1f4776c7d005f`. Actual recorded model/settings are
`gpt-6-astra`, `xhigh`, `summary: none`; model build and temperature are unrecorded.

## Preserved attempts and instruction changes

- [Initial independent grade](grading/verdicts.md): 24 PASS, 1 PARTIAL, 0 FAIL across
  the original 25 assertions; all five runs valid. Runtime12.1 was PARTIAL because
  the reader omitted newly added tests from the current increment.
- [Runtime retry grade](runtime-pr/retry-1/grading/verdicts.md): 6 PASS, 0/5 → 5/5.
  Shared instructions explicitly identify new tests and validation results. Its
  applicability review retained three earlier cases and required a visibility rerun.
- [Visibility retry-1 grade](destination-visibility/retry-1/grading/verdicts.md):
  7 PASS, 5/5 → 5/5, but full updated-procedure compliance FAIL because validation
  success appears only in the completion, outside the destination reading path.
- [Visibility retry-2 grade](destination-visibility/retry-2/grading/verdicts.md):
  7 PASS, 5/5 → 5/5, but full procedure compliance FAIL; explicit destination-placement
  wording still did not produce a validation outcome. Other four latest passes were
  independently retained as applicable to that snapshot.
- [Visibility retry-3 rationale](destination-visibility/retry-3/rationale.md): the
  instruction now distinguishes passed, failed or unavailable from a check name.
  New assertion13.8 and a stronger validation claim/baseline defect were authored
  before the fresh editor. Original assertions1–7, reader questions/expected answers,
  fixtures, Git refs and user prompt remain unchanged. Older snapshots are retained.

The final shared instruction SHA256 is
`5908c353733671baffd74e0e8e17bfac2b9c3eb62bd3423643896613b7590e35`.
Earlier snapshots and exact diffs live with their attempts; no unsuccessful sample
was overwritten, regraded under changed expectations, or repeated merely for luck.
The [final independent report](destination-visibility/retry-3/grading/verdicts.md)
establishes current applicability without claiming that earlier cases executed
this last instruction version.

## Evidence and limits

[Evidence handling](evidence-notes.md) explains native transcript exports, encrypted
dispatch metadata, pre-dispatch plaintext requests, source snapshots and shared-
filesystem limits. The [initial integrity checks](integrity-checks.json) record
artifact hashes and matched tool call/result pairs; per-attempt manifests record
the corresponding later inputs and outputs. [All-attempt integrity checks](all-attempt-integrity-checks.json)
verify all nine before/after snapshots and every editor/reader call/result pair.
The [final evidence SHA256 inventory](evidence-sha256.json) covers all persisted
evidence files except that inventory itself.

These are nine editor attempts across five scenarios, sixteen fresh reader sessions
and five independent grader sessions. Only the final visibility reader pair ran
concurrently, after the parent authorized two child slots. Readers received one
artifact each, no oracle or source-only editor context. Manifests and observed traces
are shared-filesystem controls, not OS isolation; standard harness/AGENTS context
remains injected. Initial shell startup emits a harmless failed ambient log message.

Results describe AI-reader answers and observed fidelity/visibility behavior, not
human-comprehension improvement or statistical reliability. No word-count reduction
is counted as success. Synthetic offline PR responses do not demonstrate live
platform access, and inspected/reported validation is distinguished from executed
checks. The missing-context case intentionally has no output draft or reader pair.
