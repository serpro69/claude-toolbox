# Task 3 PR regressions — 2026-10-01

Final-instruction runs: **7 PASS, 0 FAIL, 0 PARTIAL**.

| Scenario | Assertions | Evidence |
| --- | --- | --- |
| 14 `pr-missing-context` | 3 PASS | [Run](pr-missing-context/run.md), [independent grade](pr-missing-context/grading/report.md) |
| 15 `pr-unavailable-source` | 4 PASS | [Run](pr-unavailable-source/run.md), [independent grade](pr-unavailable-source/grading/report.md) |

Frozen [instruction metadata](instruction-revision.json) records entry hash
`1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189` and shared hash
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681` (1,297 words).
The snapshots match the final canonical instructions. Existing scenario specs
and oracle were copied unchanged. These old cases required no baseline editor
run; case 15 retains the required original/revised reader comparison.

Six successful fresh default agents (two editors, two readers, two independent
fixture-capable graders) used `fork_turns: none`, no overrides, and recorded
`gpt-6-astra`/`xhigh` settings. At most one child ran at a time. Only declared test
files were staged under `/tmp/clarify-issue-task3/pr-regressions/`, outside any
`SKILL.md` ancestor; readers received one artifact apiece. No evaluator/oracle
content reached editors or readers. No PR checkout was fabricated for unavailable
source. [Dispatch records](dispatches.jsonl) and [receipts](dispatch-receipts.json)
preserve six successful dispatches and five thread-capacity failures, including
one failed root-coordinator attempt. Failed dispatches are infrastructure attempts,
not behavioral runs.

Every editor, reader and grader has exact pre-dispatch plaintext/settings/manifests
and hashes, complete retained native tool/result/visible-message records, source
rollout linkage, and coverage/read audits. Inputs/outputs are snapshotted and
hashed. Case 14 files are unchanged; case 15 adds only the authorized draft.
Hidden reasoning is excluded. Encrypted native transport is recorded explicitly;
plaintext evidence was saved before submission, not reconstructed. One grader
batch display was truncated and recovered with bounded rereads; original
editor/reader evidence is complete and untruncated. See its
[audit](pr-unavailable-source/grading/audit.json).

This is trace-audited shared-filesystem staging, not process-level isolation. The
case-14 no-write manifest constrains the behavior being tested. These offline
synthetic runs do not certify a live connector or improved human comprehension.
One-off capture/export helpers remain under `/tmp`; no repository runner was added.
