# Seed workflow grading procedure — revision 2

Selected under the user-approved gate 2B receipt/use fallback on 2026-10-10.
Revision 1 and its captures/grades remain immutable. Use the same revision-2
assertions and pinned grader on both providers and both comparison sides.

All assertions remain required. PASS needs affirmative evidence of the whole
assertion; FAIL needs observed contrary behavior or a required action demonstrably
omitted from a complete relevant trace; PARTIAL means missing, truncated or
ambiguous evidence prevents establishment. A baseline FAIL is comparison data
and does not prevent capture completion. An opaque handoff does not by itself
prove the actor omitted required context. Two fresh candidate runs must pass
every required assertion for acceptance; neither FAIL nor PARTIAL passes it.

## Changed evidence contract

Only R3 assertions 7.5/7.6 and I2 assertion 9.5 select receipt/use in place of
exact submitted-prompt inspection. Require the actual named-reviewer and PAL
invocation identities, linked successful source reads or source-embedding
evidence, immutable content hashes/provenance, and each required reviewer's
observable use of the material context. Exact submitted prompt text, private
inherited context and byte-for-byte prompt parity remain **unverified**.

For R3, the parent must still materialize the historical source outside the
reviewed worktree with repository/full revision/original path/hash/line-span
provenance. Both independent reviewers must receive and use that source and
provenance. Standard mode retains its direct-history-read requirement.

For I2, both independent reviewers must receive and use the finished diff,
requested semantics, unchanged callers and attributed verification results.
Source or criteria availability on disk alone is insufficient. A correct finding,
parent handoff claim, requested read without returned content, or returned
content belonging to an unlinked actor cannot establish receipt/use.

A PAL file count is not a standalone proof of which files arrived. Pair it with
the recorded call, actual immutable referenced inputs and source/result evidence.
Distinguish newly embedded files from already supplied continuation context.
Zero embedding with no independently established earlier receipt remains a gap;
it does not prove omission. An explicit complete source-delivery failure or a
complete workflow that never invoked a required reviewer can substantiate FAIL.
Never change the baseline's actor instructions/calls to manufacture receipt.

All other assertions retain their existing obligations and evidence standards.
In particular, R1 isolated dispatch requirements are not silently reinterpreted.

## Unchanged evidence rules

Instruction ordering is per actor: completed instruction reads precede the first
prohibited source read/edit. Preserve the stated bounded routing and task-status
bookkeeping exceptions. Preserve actual parent/child edges without inventing a
total order between reviewers. Final self-attestation is not ordering evidence.

Completion and integrity use initial/final files and attributed user decisions.
I1 receives no requirement-changing reply. Findings use sealed source/report
evidence and the supplied oracle, never live fixture inspection. Audit actor
reads for grader material; an observed leak invalidates acceptance. Exclude
private reasoning and credentials without fabricating replacement events.

The grader may read only its pinned instructions/rubric, supplied manifest and
exact manifest-listed evidence. Cite event IDs or artifact locations for every
verdict. Preserve the original revision-1 grading results; write new grades with
the revision-2 identity. Regrade affected retained runs when evidence suffices,
otherwise recapture affected baseline/candidate pairs under matching declared
configuration. A runtime/model/policy change must never be hidden in a comparison.

## Gate 2B versus Task 12

Gate 2B requires the investigation outcome, selected/frozen contract and four
fresh Codex R3-isolated/I2-standalone baselines (two each), plus any required
baseline recaptures. Capture needs evidence sufficient to grade the applicable
workflow; successful behavior is not required. Any unobservable required evidence
remains an open capture limitation, never an invented FAIL. Task 12 owns candidate
counterparts, affected prior-trace regrading/recapture and final two-PASS acceptance.
