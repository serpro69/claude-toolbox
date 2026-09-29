# Independent task-2 retry-1 grading

Date: 2026-09-29. **Both retry scenarios PASS: 9/9 assertions PASS, 0 PARTIAL, 0 FAIL.** All ten revised-reader answers pass the retry oracles. These are separate attempts; [the first-run results](../task2-20260929/summary.md) remain 21/24 assertions PASS and 3 PARTIAL.

| Scenario | Assertions PASS / PARTIAL / FAIL | Original reader PASS / PARTIAL / FAIL | Revised reader PASS / PARTIAL / FAIL | Overall |
| --- | --- | --- | --- | --- |
| [contract-only-pr](contract-only-pr/verdicts.md) | 5 / 0 / 0 | 1 / 2 / 2 | 5 / 0 / 0 | PASS |
| [pr-unavailable-source](pr-unavailable-source/verdicts.md) | 4 / 0 / 0 | 4 / 1 / 0 | 5 / 0 / 0 | PASS |
| Total | 9 / 0 / 0 | 5 / 3 / 2 | 10 / 0 / 0 | PASS |

## Differences from the first attempt

The contract-only fixture now supplies the exact 15-minute example in requirements at both base/head; assertions and oracle are unchanged. The new editor and reader both use that example and correctly retain contract-only scope. The unavailable-source reader question now explicitly asks for missing evidence and its owner; the oracle collects that obligation under question 3 while preserving all protected claims. The new reader recovers the PR author and all required evidence. Skill instructions are byte-identical to the first attempt.

The retry therefore supports success under these clarified fixture/question conditions. It does not convert the first attempt into a pass, establish repeatability on identical inputs, or show an improvement caused by changed skill instructions. Both attempts' outputs, traces and grades remain available.

The contract-only final report again uses an absolute workspace output link despite the shared procedure's blanket report-path wording. Its verdict retains this observation and distinguishes the caller-facing output link from a restricted source pointer in the PR body; the higher-priority harness prefers clickable absolute file links. Clarifying those destination rules remains a follow-up, outside these unchanged assertions.

## Audit and validity

Reviewed all supplied instructions, eval/oracle files, original/revised artifacts, snapshots, manifests, sessions, prompt records, exact tool traces and editor/reader final responses. All ten editor call batches and four reader calls have one matching result each. Instructions finish before source reads in both editors. Each reader reads exactly its manifest artifact and no additional material. All observed reads/writes stay within the allowlists, with no network/external mutation or delegation.

One contract-editor batch exits 1 because its final `rg` finds no inbound references; preceding Git/source results are complete. This is not missing evidence or an isolation failure. All recorded hashes match, revised archives equal staged files, authorized mutations are the only changes, and the contract checkout is clean with exact base/head snapshot membership/content.

All six editor/reader sessions specify `gpt-6-astra`, `xhigh`, `fork_turns: none`; model build and temperature are not exposed. Prompt recipients match the session records, but encrypted payloads cannot be cryptographically matched to the orchestrator-attested plaintext. The audit establishes no observed manifest/order violation within the supplied trace export; it does not independently authenticate omitted upstream session events. Shared-filesystem allowlists and one model-reader sample per version limit generalization to human comprehension or repeated runs.
