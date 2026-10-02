# Task 3 gap scenarios — 2026-10-01

All 15 final assertions pass. Baseline: 14 PASS, 1 FAIL, 0 PARTIAL. The preserved failure is 20.3: the baseline editor emitted an inline proposed draft before asking for a destination. The assertion was not changed. All six editor runs and three reader runs are valid; three independent fixture-capable graders supplied the per-assertion verdicts.

| Scenario | Baseline | Final | Observed outcome |
| --- | --- | --- | --- |
| 20, pasted input without destination | 3 PASS / 1 FAIL | 4 PASS | Both read all supplied context and leave files unchanged. Baseline offers an inline draft; final asks only for the destination. |
| 21, unavailable supporting source | 7 PASS | 7 PASS | Both create only the requested qualified draft and retain reported behavior, unknown cause, source-retrieval owner and unassigned reproduction owner. |
| 22, unavailable body | 4 PASS | 4 PASS | Both explain the missing body and request accessible text without creating an output. |

Scenario 21's original, baseline-revised and final-revised readers each answer all five supported questions correctly. Both editors repair the speculation-first orientation defect. These runs establish no reader-score improvement or general causal advantage over baseline. Reader comparison is N/A for 20/22 because no destination/body exists respectively.

Instruction identity: entry point is unchanged at SHA256 `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`. Shared procedure baseline is `9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539` (1,248 words); final is `519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681` (1,297 words). Final snapshots were frozen after parent readiness and after all baseline editor traces were captured. [final-canonical-identity.json](final-canonical-identity.json) confirms the final snapshots match operative files.

Each scenario's `baseline/` and `final/` folders contain exact pre-dispatch prompts, manifests/settings, before/after artifacts and hashes, complete native tool/message traces, completion reports and dispatch receipts. Scenario 21's `readers/` contains the isolated artifacts and reader answers. Independent verdicts and grader traces are in [graders/20](graders/20/verdicts.json), [graders/21](graders/21/verdicts.json) and [graders/22](graders/22/verdicts.json). [summary.json](summary.json) preserves combined assertion results.

All twelve participants are fresh `default` agents with `fork_turns=none`, no overrides, and actual `gpt-6-astra` / `xhigh` settings. Exact plaintext prompts were saved and hashed before dispatch. Native transport is encrypted; receipts and complete participant traces provide linkage while decryption remains unavailable. Shared filesystem access was audited against exact manifests, without claiming OS isolation or live-connector certification.

See [audit.md](audit.md) and [native-export-audit.json](native-export-audit.json) for coverage. All editor/reader tool outputs are complete; grader 20's one capped display was fully recovered in its next read and retained. Its first dispatch was rejected by the agent-thread limit before any agent started; both rejection and successful retry receipts are preserved. No assertions were relaxed, no fixtures/instructions were changed by this evaluation coordinator, and no unresolved evidence gap remains.
