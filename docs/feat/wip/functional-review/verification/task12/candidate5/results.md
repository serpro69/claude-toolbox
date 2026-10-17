# Candidate 5 diagnostic: R1/R3 pass twice; R5 still fails

The focused rework improves the measured results but **does not clear the
diagnostic gate**. Candidate: **37 PASS / 3 FAIL / 0 PARTIAL**. Fresh matching
baseline: **20 PASS / 18 FAIL / 2 PARTIAL**. All forty assertions per side retain
their original meaning and required status; no fixture, rubric or threshold was
weakened. Counts describe this development sample, not statistical reliability.

| Standard case | Baseline rep 1 P/F/PARTIAL | Baseline rep 2 | Candidate rep 1 | Candidate rep 2 | Two-run candidate gate |
| --- | --- | --- | --- | --- | --- |
| R1 ownership/lifecycle | 3/3/0 | 3/3/0 | 6/0/0 | 6/0/0 | PASS |
| R3 released-provider compatibility | 5/3/0 | 6/2/0 | 8/0/0 | 8/0/0 | PASS |
| R5 clean partial feature | 1/4/1 | 2/3/1 | 4/2/0 | 5/1/0 | FAIL |

All twelve declared captures completed with runtime exit zero. Each used a fresh
workspace and isolated knowledge state; no earlier baseline was reused because
the capture runner changed. [The declaration](run-contract.md) and [freeze](freeze.json)
precede measured execution. The [structured grades](grades.json) and individual
tables under [results/](results/) retain all eighty independent assertion grades.
Each run used a fresh native `eval-grader` role and the unchanged pinned workflow
grader/revision-2 rubric. Grader roles had only sealed, manifest-listed inputs.

## What improved

Both R1 candidate runs loaded all common/detection/checklist instructions before
investigation and traced the documented failed-A, successful-B, queued-cleanup-A
sequence through the unchanged consumer. They identified the ownership regression,
preserved the ownership guard in their correction, and distinguished the passing
existing tests from a reproduction denied by the tool policy.

Both R3 candidate runs obtained actual historical provider source, traced values
being stored before the new client raises, and identified the current hard
independent-release violation. Their Blocked/REQUEST_CHANGES conclusions were
qualified to inspected source, without certifying production. Ordinary disabled
saves remained preserved in their proposed corrections.

The original missing-detection-file failure did not recur in any candidate run:
all six candidates successfully read packets containing every Known-profile rule.
Packet receipt and original source-byte identity were audited, not inferred from
the actor's loading claim. Packet creation still does not enforce action ordering.

## Remaining failures, classified without changing grades

**Procedural — R5 repetition 1, assertion 12.1.** Full task requirements were read
at e52/e53 before checklist contents returned at e64/e66. This was neither
task-status bookkeeping nor a declared bounded routing predicate. The packet
mechanism eliminated omitted instruction bodies but did not prevent this early
subject read.

**Recommendation quality — R5 repetitions 1 and 2, assertion 12.4.** Both reviews
correctly approved the scoped, disabled-feature increment and recognized pending
Task 2. Both nevertheless offered a flag-import/refactor change for future
testability while explicitly acknowledging no current defect. Repetition 1 puts
it in e148; repetition 2 offers it as Next Steps option 3 in e150. Optional wording
does not satisfy the existing requirement to avoid unnecessary work.

There are no additional failed candidate behavioral assertions in this diagnostic.
These categories explain the three failures; they do not downgrade them or create
a revised acceptance policy. R1/R3 passing does not make R5 or the full matrix pass.

## Integrity, access and cleanup

[Integrity audit](integrity-audit.json) validates 486 captured-file and 1,289
grading-file hashes, all capture-to-grading manifest links, unchanged subject files
and all twelve post-run actor bundles. It verifies the complete returned packet
parts against immutable snapshots and original instruction sources. Both separate
binding probes passed; the candidate's reported alias discrepancy was an expected
symlink, verified as identical resolved content.

[Access audit](access-audit.json) records scoped file tools and inspection of every
shell request. No evaluator-material access or PAL tool call was observed. The
nineteen uniquely owned packet directories from binding and measured runs were
checked against their captured creation manifests and removed: 79 verified files.
[Cleanup evidence](packet-cleanup.json) retains those manifests; original packet
bytes and actual Read results remain in sealed captures. No unrelated paths were
removed. Actor workspaces and source snapshots remain available for audit.

These observations do not establish OS-wide confinement or exact submitted
reviewer-prompt parity. No isolated-mode, Codex or full-matrix acceptance is claimed.
Source reviews and [static checks](../rework/README.md) pass independently of the
failed behavioral gate. Live PAL verification remains user-deferred.

## Disposition and next action

The declared diagnostic is captured, graded and audited. No expansion or further
candidate iteration was launched after its failed gate. Task 12 remains
in-progress; Task 13 remains pending. The repeated R5 recommendation failure also
meets /kk:implement's instruction to stop when verification fails repeatedly.

Owner: implementing agent, Task 12. Preserve the runner fixes, packet preparation
and these results. A proposed follow-up should address the two remaining R5 paths:
requirements reading before checklist completion, and the clean-review Next Steps
branch offering unsupported work. It needs a separately identified candidate and
fresh affected comparisons before any matrix expansion; do not repair the actor
reports, relax assertions, or count these failures as passes.
