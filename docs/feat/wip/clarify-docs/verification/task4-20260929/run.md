# Task 4 combined-revision evaluation

Date: 2026-09-29. Starting repository revision:
`9a7ad32eef89a3b8c9b366292ac1f4776c7d005f`.
Status: complete. All 20 scenarios have passing applicable evidence: 87 assertions
and 70 revised-reader answers. No assigned scenario is authored-but-unrun.
Group records: [local](local/run.md), [PR](pr/run.md), [consumers](consumers/run.md).

Scope: 15 standalone `/kk:clarify-docs` cases and five `/kk:design` or
`/kk:document` consumer cases. Fourteen have fresh original/revised readers; six
test routing or missing-destination behavior without a reader comparison.
The implementation-mode case inspects instructions, not a completed lifecycle.

The frozen instruction tree was copied from canonical `klaude-plugin/`, with
all eval directories excluded, to `/tmp/clarify-task4/instructions/` before
editors ran. It includes the caller-only output-link clarification. Group hash
manifests identify the tested instruction bytes. Reconstruct the initial tree from
the canonical plugin in the commit containing this report, restoring the saved
[shared procedure](instructions/initial/document-clarity.md) and
[WIP process](instructions/initial/existing-task-process.md), then verify the
hashes. Later oracle and eval-README additions are outside the snapshot.
No installed, older clarity skill substitutes for this copy.

Three execution coordinators own disjoint local, PR and consumer groups. Each
editor, original reader and revised reader is a separate general-purpose session
with `fork_turns="none"`. Independent general-purpose graders inspect the oracle,
source evidence, outputs and actual tool traces. None uses the fixture-prohibited
`eval-grader` role. Exact plaintext requests are stored before dispatch, alongside
the one-line spawn text and actual session IDs. Extracted traces retain tool
calls/results and visible messages, including `phase=final_answer`; hidden
reasoning and system boilerplate are omitted.

The initial runtime-PR reader omitted newly added tests from the current increment.
The draft listed their review path without saying they were new. A focused shared
instruction correction now explicitly identifies newly added tests in PR increments
and asks for validation results with their limits;
the procedure is **1,000 words** (initial run: 999). The runtime retry uses fresh
sessions with unchanged prompt, fixtures, questions and oracle. Initial evidence
remains preserved. This PR-only clarification does not change the local-document
or non-PR consumer instructions that their initial runs exercise. Independent PR
grading assesses applicability of the other PR results. It requires a fresh
destination-visibility run too: the initial passing draft described JSON parsing
without its success outcome. The other three PR cases remain applicable. The
earlier visibility pass remains a valid result under its original instructions.
That visibility rerun again put the success outcome only in the private completion
message. The final PR wording now explicitly places validation outcomes and limits
in the draft; completion messages do not substitute. Another fresh visibility run
tests that correction. When it still omitted the outcome, the final wording
explicitly distinguished passed, failed or unavailable from a check name.
Assertion 13.8 and its oracle validation defect were added before the final editor;
fixtures, reader questions and user prompt stayed unchanged.
The [final visibility grade](pr/destination-visibility/retry-3/grading/verdicts.md)
passes all eight assertions and full procedure compliance. Each attempt retains
its actual frozen instructions and hashes. The final shared procedure remains
1,000 words, SHA256 `5908c353733671baffd74e0e8e17bfac2b9c3eb62bd3423643896613b7590e35`.
These PR-only deltas do not invalidate non-PR reader or consumer runs.

The unchanged WIP resume named Task 2 but omitted `/kk:implement` from its handoff.
The WIP process now requires both the next pending task and the invocation when
the caller asks to stop at handoff, without starting implementation. Refined and
unchanged resumes are rerun with fresh editors and reader pairs. The fresh-idea,
documentation-profile and implementation-route cases exercise unchanged branches;
consumer grading records their applicability to this targeted correction. The
[fresh WIP retries](consumers/retry-handoff/run.md) pass all seven assertions;
[final applicability grading](consumers/final-applicability/run.md) also verifies
the local-source oracle corrections and text-preserving JSON-shape normalization.

Observed session metadata reports `gpt-6-astra`, reasoning `xhigh`, Codex CLI
`0.159.0`. Model build and temperature are unavailable and are not inferred.
Readers use the same model/settings and fixed questions; they see only their own
artifact and explicitly allowed audience reading path. The after-drafting case
uses completed pre-pass drafts as its original, because its input contains
requirements rather than an existing document. The other cases use their original
selected artifacts.

Isolation is an allowed-file manifest plus an audit of actual tool access on the
shared filesystem, not an OS sandbox. Standard harness/repository instructions
remain present in fresh sessions. Missing trace evidence or out-of-manifest
subject-content access invalidates a run. Groups preserve any failed attempts
and execution-method limitations. No result establishes general human
comprehension or repeatability; no word-count reduction serves as acceptance.

Repository checks are recorded in [checks.md](checks.md). Task 5's release
verification and final feature documentation remain pending.
