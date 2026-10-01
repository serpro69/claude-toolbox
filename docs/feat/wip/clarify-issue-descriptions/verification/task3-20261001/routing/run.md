# Task 3 routing evidence — 2026-10-01

The accepted final runs pass **14/14 assertions** across scenarios 23/24 and existing regressions 9/10. See [current verdicts](current-verdicts.json). Original/revised readers are N/A because none of these requests asks for editorial work. Implementation correctness is outside this routing grade.

The initial baseline passed eight assertions. The first final-instruction attempt received **12 PASS and 2 PARTIAL**: the grader treated denied login-shell startup log writes as an unresolved isolation qualification in 23.4/24.4. Those results remain intact. Fresh 23/24 runs used the same instructions, fixtures, assertions and permissions with a neutral `login:false` shell instruction; a fresh independent grader passed all eight. Existing 9/10 had already passed with that shell setup.

## Results and retained attempts

| Scenario | Baseline | First final attempt | Accepted final evidence |
| --- | --- | --- | --- |
| 23 — implement | [4 PASS](issue-implement-non-trigger/baseline/verdicts.json) | [3 PASS, 1 PARTIAL](issue-implement-non-trigger/final/verdicts.json) | [4 PASS](issue-implement-non-trigger/clean-shell/verdicts.json) |
| 24 — fix | [4 PASS](issue-fix-non-trigger/baseline/verdicts.json) | [3 PASS, 1 PARTIAL](issue-fix-non-trigger/final/verdicts.json) | [4 PASS](issue-fix-non-trigger/clean-shell/verdicts.json) |
| 9 — code question | Not required | [3 PASS](code-non-trigger/final/verdicts.json) | Same run |
| 10 — response brevity | Not required | [3 PASS](brevity-non-trigger/final/verdicts.json) | Same run |

All issue editors changed only their permitted Python source and left issue.md byte-for-byte unchanged. None selected the editorial skill, read its instruction body/shared procedure, changed the issue title, created an editorial artifact, or published remotely. The code question correctly explained null inheritance from the restaurant default without writes. The brevity case answered in one sentence with zero tools and no file changes.

Independent, fixture-capable default graders produced the [baseline](baseline-grader/verdicts.json), [first final](final-grader/verdicts.json), and [clean-shell](clean-shell-grader/verdicts.json) verdicts. Each assertion has separate evidence. The differing baseline/final interpretation of denied startup writes is preserved rather than reconciled by changing either result.

## Instruction identity

| Snapshot | Entry SHA-256 | Shared procedure SHA-256 |
| --- | --- | --- |
| [Baseline](instructions/baseline/identity.json) | `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189` | `9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539` |
| [Final](instructions/final/identity.json) | `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189` | `519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681` |

Snapshots identify working-tree content over revision `f516712109b59314e656a3e535e5a099110b28c9`; they do not imply a clean checkout. Baselines completed before operative Task 3 instructions changed. The description already excluded implement/fix intent, so baseline passes document an existing safeguard. The final description is unchanged; the final procedure adds issue-gap handling. Neither procedure was loaded by these editors.

## Method and records

Each editor was a fresh default agent with `fork_turns=none`, no model/effort override, an offline workspace outside any SKILL.md ancestor, the unchanged natural eval request, and a task skill catalog exposing only the exact normalized clarify-docs description. Instruction paths were available if selected, but bodies were not preloaded. No classification-only prompt or explicit instruction to reject editorial selection was added. Issue captures were immutable; ordinary source edits/checks were allowed. Specifications/oracles stayed in grader evidence, outside editor staging.

Actual recorded model/settings for all editors and graders: `gpt-6-astra`, effort `xhigh`, default role, network disabled. Shared filesystem access was audited, not treated as isolation. The [execution protocol](protocol/execution-and-evidence.md) and [eval README](protocol/evals-README.md) are preserved.

Each run directory retains the exact pre-dispatch prompt and hash, allowed manifest, source identity, submission settings, native dispatch call/result and receipt, before/after artifacts and hashes, native visible tool/message trace, inbound user/task records, actual settings, completion report, access/file-effect audit and independent verdicts. `native-integrity.json` compares retained editor records byte-for-byte with the original native rollout. Native sources are identified by path/hash in metadata. No editor tool result is missing or truncated.

All initial dispatches have pre-saved plaintext and native receipts. A capacity-rejected clean-fix dispatch is preserved separately in [rejected dispatches](rejected-dispatches.jsonl); it started no editor and was retried unchanged after a slot was released. A later [administrative baseline-grader turn](baseline-grader/slot-management.md) only consumed a queued notification and performed no grading or tools; original grading evidence is unchanged.

## Recovery and limitations

Initial issue runs triggered an attempted `/home/sergio/.config/navi/navi.log` write during login-shell startup. The environment denied the writes and reported no file creation. The first final grader retained this as two PARTIAL assertions. Clean-shell reruns and their grading used `login:false` throughout and contain no such attempts. This was the only substantive setup change; separate stage paths preserved prior attempts.

Both reruns first tried unavailable `python`, then succeeded with `python3`. The fix rerun's initial listing command contained a negative __pycache__ glob rejected by a hook before execution; direct permitted-file reads succeeded. Failed attempts and successful recovery remain in the full traces.

Workspace paths retain scenario identifiers such as `issue-implement-non-trigger`, which can weakly cue the expected route. These are not fully blind runs. The accepted protocol requires natural work requests, description-only selection, and no classification-only/explicit rejection cue; assertions were not relaxed.

Dispatch transport is encrypted. Exact plaintext was saved before submission; prompt hashes, timestamps, receipts, returned agent paths and matching dispatch/inbound ciphertext establish consistent linkage. Graders cannot independently decrypt plaintext equivalence. Tool/message captures omit hidden reasoning and system/developer boilerplate. Fresh agents still receive the repository AGENTS.md/environment bootstrap, and native cwd remains the repository; explicit project accesses were audited against workspace manifests. These are not operating-system-level filesystem/network audits and do not certify live trackers or general implementation correctness.
