# Issue evaluation execution evidence

Final revised result: scenario 16 passes 7/7 assertions, and scenario 17 passes
5/5 against the corrected oracle. Baseline scenario 16 fails (protected title and
unsupported reference mapping); baseline scenario 17 also passes the corrected
oracle. The initial scenario 17 PARTIAL verdicts and the subsequent oracle audit
remain preserved separately below. No editor/reader run or skill instruction was
changed to obtain the corrected-oracle result.

Scenarios 16 (`github-issue-bug`) and 17 (`issue-local-draft`) were staged separately
outside any skill ancestor. The editors and readers are fresh general-purpose
sessions with no inherited conversation (`fork_turns=none`) and no model override.
Actual captured settings are `gpt-6-astra`, effort `xhigh`; each session's metadata
records its ID, native rollout path, call/result counts and final-message presence.
Live connector certification is excluded: all provider material is synthetic and
network access is forbidden.

The scenario specification and fixed oracle were copied before execution into
each scenario evidence directory. They were never staged with editor/reader files.
Editor and reader prompts and allowed-file manifests were saved before submission.
The initial fixtures and hashes are under each editor run's `before/` and
`before-sha256.json`; output snapshots and hashes are under `after/` and
`after-sha256.json`. Instruction snapshots are under `instructions/`.

Both baseline editors finished before operative edits and before revised editors
were launched. The coordinator sent `BASELINES COMPLETE` after preserving their
complete tool-call/result/message traces. Both produced editable artifacts.

Fresh original readers have completed for both scenarios. Their identical five
questions are the fixed oracle questions, and only their declared description
artifact is readable. Their answers can be shared across baseline/revised
comparisons because artifact bytes, questions, and settings are identical.

The first revised editors ran against the frozen Task 1 instructions:

- `SKILL.md`: `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`
- `shared-document-clarity.md`: `858630c27477ce3e2d39dc42ae72b17eab3e94ceb2f06b97ca10b2aacbe5dfb0`

All four editors, six readers, and the two initial independent fixture-capable graders
completed. Their full reports are [scenario 16 grading](github-issue-bug/grading/final.md)
and [scenario 17 grading](issue-local-draft/grading/final.md).

| Scenario | Baseline | First revised instructions |
| --- | --- | --- |
| 16 — GitHub bug | 5 PASS, 1 PARTIAL, 1 FAIL; overall FAIL | 7 PASS; overall PASS |
| 17 — selected local draft | 4 PASS, 1 PARTIAL; overall PARTIAL | 4 PASS, 1 PARTIAL; overall PARTIAL |

Scenario 16 baseline replaces the protected title (16.6 FAIL) and constructs remote
reference paths whose mapping is not established by the fixture (16.3 PARTIAL).
The revised draft preserves the title and uses links resolving to the supplied
accessible sources. Every other fixed assertion passes in both runs.

Scenario 17's revised draft still omits the oracle's explicit scope boundary that
implementing a fix is outside this edit; its draft-only reader answers Q4 with
only the asynchronous-export exclusion. Assertion 17.1 is PARTIAL. The revised
draft repairs Q3 evidence status: its reader distinguishes source inspection,
unverified causation, absent execution evidence, and no reproduction during the
edit. The baseline Q3 remains PARTIAL because the editor removed its explicit
non-reproduction statement. The coordinator reported the non-passing revised run
to the parent for instruction correction and a fresh run. These attempts and
unchanged oracles are retained; no assertion has been weakened.

The parent held instruction changes and reruns pending an oracle-validity audit:
Q4 asks for issue scope, while its expected answer also requires a statement about
the editorial task's action boundary. The independent scenario 17 grader received
a saved follow-up request to identify any design/fixture requirement for that
in-artifact disclaimer and assess the preserved pending confirmation/fix state.
The request, expanded read manifest, and supporting design/implementation snapshots
are in `issue-local-draft/grading-clarification/`. Initial grades remain unchanged.

The [independent clarification](issue-local-draft/grading-clarification/clarification.md)
found no design or source-fixture requirement for the disputed disclaimer: only
the fixed Q4 expected answer adds it. The grader identifies a conflation between
issue scope (asynchronous export is excluded) and editor authorization (no
implementation actions). Both drafts and readers preserve Mina's pending
confirmation, unchosen fix, and incomplete tasks; the audited traces separately
establish no implementation actions. The same clarification notes that baseline
Q3 preserves substantive runtime uncertainty without necessarily narrating the
editor's own history. Thus the initial PARTIAL remains a literal-oracle outcome
with a documented applicability concern, not a demonstrated failure to preserve
implementation state or obey the no-implementation boundary. No instructions,
fixtures, oracle, or previous grades were modified by this audit.

After a separate independent code review confirmed the oracle defect, the parent
corrected only expected answers Q3 and Q4. The [versioned corrected oracle](issue-local-draft/oracle-v2/expected.json)
and [correction rationale](issue-local-draft/oracle-v2/rationale.md) were saved before
dispatch; corrected-oracle SHA256 is
`2b846fd825b6e64138b1108afa52a4805dee45bc1f5f6fd9fc01cf0a59d59381`.
Questions, assertions, fixtures, instructions, prompts, output artifacts, reader
answers, and traces remain unchanged. A fresh general-purpose grader with no
access to prior reports completed an independent regrade of those same runs under
`issue-local-draft/grading-oracle-v2/`. No editor/reader rerun was performed because
their inputs and questions did not change; the initial literal-oracle result is
retained separately rather than overwritten.

The [corrected-oracle report](issue-local-draft/grading-oracle-v2/final.md) awards
both baseline and revised versions 5/5 PASS. Its fresh grader re-audited all
editor/reader traces, settings, manifests and hashes, with no previous verdicts or
original-oracle access. Every edited-reader answer passes; original Q3 remains
PARTIAL because the original artifact lacks inspected-source evidence. That
limitation remains distinct from misunderstanding. The new grading session has
six matched calls/results and a captured final; its exact pre-dispatch prompt,
oracle hash, dispatch record, complete native trace and actual metadata are saved.

Both original readers already understand the user problem and reported example.
Their source-evidence answers are incomplete because those details are missing
from the original artifacts. Both editors repair source-first ordering; this is
an observed orientation improvement, not an invented original-reader failure.

All ten editor/reader access audits are valid: complete tool calls/results and
finals, instructions loaded before subject content, only declared subject reads,
and no oracle leakage. No successful out-of-scope writes, reproduction, network
calls, or publication appear. Login-shell startup emits a denied logging diagnostic;
the evidence does not claim complete syscall-level filesystem isolation.

`dispatches.jsonl` preserves native spawn call/result records. Native transport
messages are encrypted; `dispatch-receipts.json` records the pre-existing exact
plaintext prompt files, SHA256 hashes, and save-before-dispatch timestamps for all
12 submissions. `integrity-check.json` independently verifies snapshot hashes,
instruction hashes, identical initial fixtures, question identity, and completed
tool-call/result capture.

The shared filesystem is not OS isolation. Raw traces must be audited against
allowed-file manifests before a pass is claimed. `capture-evidence.py` preserves
native tool records and visible assistant messages, excluding hidden reasoning and
system boilerplate. Its first extraction did not recognize the transport's
`phase=final_answer` field; that extraction was corrected from the same unchanged
native rollouts before reporting baseline completion. No editor run was rerun or
discarded because of that extraction correction.
