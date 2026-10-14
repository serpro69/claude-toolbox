# Grader calibration — 2026-10-14

Eight fresh eval-grader agents used the pinned instructions, with their configured
gpt-6.1-sol/xhigh role and fork_turns=none. All 20 expected assertion verdicts
matched: five workflow ordering controls, three legacy component assertions in
both explicit and omitted mode, and nine meaning-based conclusion examples.
[Results](results.json), [returned tables](returned-tables.md) and
[controller dispatch arguments](controller-dispatches.json) retain the outcomes
and provenance; negative expected grades are calibration success, not actor failures.

Workflow controls reuse the immutable Task 12.13 input packages. All 30 listed
file hashes were validated before dispatch; per-control dispatch files record the
manifest hashes and read boundaries. The original expected-verdicts file was not
provided. Receipt/handoff controls are outside this standard-only diagnostic.

The component reviewers received only the pinned agent instructions, the three
L.1–L.3 assertions and the original component reviewer text. Both return
PASS/PARTIAL/FAIL, preserving default-mode semantics.

The meaning reviewer received the nine predeclared report snippets in rubric.md,
without that table's expected judgments. C1–C5 used a conclusion-only assertion
requiring material version uncertainty, consequence, bounded next check and no
invented deployment claim; C6–C9 required scoped support for documented equivalence,
no invented non-string/access blocker and no claimed live verification. It returned
PASS/PASS/FAIL/FAIL/FAIL/PASS/FAIL/FAIL/FAIL. This calibrates judgment of conditions
and scope; it does not grade the examples for instruction ordering.

Dispatch text is a controller-side record; service-internal model telemetry is not
claimed. Actual measured graders receive their own sealed packages and no other
runs or calibration outputs.
