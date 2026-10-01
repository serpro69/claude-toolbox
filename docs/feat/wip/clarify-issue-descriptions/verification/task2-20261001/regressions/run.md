# Task 2 required regressions — 2026-10-01

Status: **complete — final revision passes all 13 assertions; both executions are valid**.
The final independent [verdict](final-grader-verdicts.md) reports 13 PASS, 0 FAIL,
0 PARTIAL, and 0 invalidated runs for `contract-only-pr` (11) and
`destination-visibility` (13). The first visibility failure remains preserved.

## Final instruction revision

The full frozen entry point contains 616 words, SHA256
`1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`.
The full frozen shared procedure contains 1,248 words, SHA256
`9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539`.
[Final instruction hashes](instruction-hashes-retry.json) identify the exact
canonical and frozen files. [Canonical comparison](canonical-final-check.json)
confirms that the tested files match the final operative instructions.

## Final results

| Scenario / evidence | Assertions | Execution | File effects |
| --- | --- | --- | --- |
| [Contract-only PR retry](contract-only-pr-retry/editor-trace.jsonl) | 11.1–11.5: 5/5 PASS | Valid | Only `pr-draft.md` changed; 21 non-target files, including 17 Git metadata members, unchanged. |
| [Destination visibility retry](destination-visibility-retry/editor-trace.jsonl) | 13.1–13.8: 8/8 PASS | Valid | Only `pr-draft.md` changed; 27 non-target files, including 19 Git metadata members, unchanged. |

The contract draft explains the contract-only increment, null/zero example,
unchanged runtime stub, pending badge decision and validation limits. Its revised
reader answers all five questions correctly; the original reader had one correct,
two incorrect and two partial answers. The visibility original and revised readers
both answer all five questions. Its final draft removes the restricted facts and
source pointers, retains Task 7 and both authorized links, and explicitly states
that JSON parsing passed with no runtime or deployment evidence. Its caller-only
completion links only the selected local output.

Both retries use fresh default editor and revised-reader agents with
`fork_turns=none` and no overrides. The parent authorized reuse of the unchanged
independent original readers. Their original IDs and exact traces/settings remain
recorded; no new original-reader execution is claimed. [Reuse context](final-run-context.md)
and [fixture comparison](retry-fixture-comparison.json) establish identical
original artifacts, questions and criteria. All six participant sessions use
`gpt-6-astra`, effort `max`, with matching reader settings.

The independent final grader verified all **123 input hashes**, complete file
inventories, every ZIP member and the actual archived Git objects. The recorded
base/head commits and diffs match the supplied snapshots. No file was created or
deleted in either editor workspace. Every editor loaded both exact full instruction
files before reading subject matter, and every reader opened only its assigned
draft. There was no oracle/snapshot access by editors or readers, network call,
external mutation, or successful write outside a selected draft.

All **15 participant tool calls** have complete paired results across the six
sessions, with final completions and no truncated result. See
[trace-completeness-retry.json](trace-completeness-retry.json). The contract retry's
in-scope filename listing was rejected by a hook because its exclusion glob
contained Git path text; the complete rejection is retained, and a later read-only
Git tree query supplied the listing. This caused no read, mutation or missing
source evidence and did not invalidate the run.

[Final grader prompt](final-grader-prompt.txt) and
[manifest](final-grader-manifest.json) were saved before dispatch. The grader
received no previous editor result or grading verdict. Its complete visible
[trace](final-grader-trace.jsonl), [actual settings](final-grader-settings.json),
[submission receipt](final-grader-dispatch-receipt.json), and
[completion](final-grader-completion.md) are preserved. The
[final evidence audit](final-evidence-audit.json) confirms intact first/final grader
inputs, completed grader traces, paired calls/results, and unchanged live
workspaces since their after captures.

The final grader's own source/trace display bundles were initially capped at
native results 35 and 67. Subsequent complete reads recovered all required content
before the verdict: 43 full source/artifact file displays and all 32 editor trace
records, plus independent inventory/archive checks. The
[display-recovery audit](final-grader-coverage-audit.md) and
[exact reconstruction checks](final-grader-coverage-audit.json) establish no
remaining gap. The capped attempts remain preserved; participant traces were
always complete. No extra grader turn or participant rerun was required.

## Preserved first attempt

`contract-only-pr/` and `destination-visibility/` contain the first frozen
instruction executions. Their independent [verdict](grader-verdicts.md) records
**12 PASS, 1 FAIL, 0 PARTIAL**, with both runs valid. Assertion **13.8** failed
because the visibility draft named JSON parsing without stating the supplied
successful result. This failure was reported immediately and left intact.
The original grader's [trace](grader-trace.jsonl), [settings](grader-settings.json)
and [dispatch receipt](grader-dispatch-receipt.json) remain available.

The parent clarified only the PR validation sentence, requiring the supplied
outcome in the draft. The procedure remains 1,248 words. The complete
[instruction diff](instruction-retry.diff) and [retry provenance](retry-provenance.md)
record the change. Fixtures, evals and oracles were unchanged; fresh editor and
revised-reader prompts differ only in harness paths. No baseline editor rerun or
criteria weakening was performed.

## Capture and limits

[Staging notes](staging-notes.md) explain the separate real Git repositories,
non-login shells, disabled optional locks, ZIP packaging and preserved
coordinator-only hook rejections. Workspaces sit outside every SKILL.md ancestor.
Prompts were saved through native apply_patch before submission; manifests define
allowed files and writes. Git metadata is preserved as original archive members
rather than embedded repositories.

Native JSONL exports retain complete visible tool calls/results, assistant
messages and lifecycle events. They exclude hidden reasoning and automatically
supplied system/repository boilerplate. Native task transport is encrypted;
submission receipts preserve it while pre-existing plaintext prompt files record
what was dispatched. No prompt was reconstructed after its run.

These are offline manual model evaluations using synthetic source and access
responses. They establish the observed editorial behavior and trace-audited
manifest adherence, not filesystem-enforced isolation, live connector support,
new runtime tests or improved human comprehension.
