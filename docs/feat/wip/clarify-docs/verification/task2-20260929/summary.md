# Independent task-2 behavioral grading

Date: 2026-09-29. All five scenarios were graded from the frozen instructions, eval definitions, grader-only oracles where supplied, original/revised artifacts, source snapshots, manifests, session/transport records, exact captured tool traces and editor/reader final responses. Grading made no changes to scenario outputs or assertions.

**Result: 3 scenarios PASS, 2 PARTIAL; the suite does not fully pass.** Across 24 assertions: 21 PASS, 3 PARTIAL, 0 FAIL. PARTIAL is not a pass.

| Scenario | Assertions PASS / PARTIAL / FAIL | Original reader PASS / PARTIAL / FAIL | Revised reader PASS / PARTIAL / FAIL | Overall |
| --- | --- | --- | --- | --- |
| [contract-only-pr](contract-only-pr/verdicts.md) | 3 / 2 / 0 | 1 / 2 / 2 | 4 / 1 / 0 | PARTIAL |
| [runtime-pr](runtime-pr/verdicts.md) | 6 / 0 / 0 | 0 / 2 / 3 | 5 / 0 / 0 | PASS |
| [destination-visibility](destination-visibility/verdicts.md) | 6 / 0 / 0 | 5 / 0 / 0 | 5 / 0 / 0 | PASS |
| [pr-missing-context](pr-missing-context/verdicts.md) | 3 / 0 / 0 | Not applicable | Not applicable | PASS |
| [pr-unavailable-source](pr-unavailable-source/verdicts.md) | 3 / 1 / 0 | 2 / 2 / 1 | 3 / 2 / 0 | PARTIAL |
| Total | 21 / 3 / 0 | 8 / 6 / 6 | 17 / 3 / 0 | Not fully passed |

## Exact unresolved mismatches

1. **11.1 and 11.4:** The contract-only editor chooses a 20-minute example, and its reader reports 20/null→20. The assertion/oracle explicitly require 15/null→15. General null/zero semantics and the runtime boundary are correct, but the prescribed example does not match.
2. **15.3:** The unavailable-source draft includes the PR author's concrete verification action, yet the revised reader omits that owner/action from question 5 and the owner/source gap from question 3. Correct artifact content is not substituted for missing reader answers.

A further non-assertion observation is recorded in the contract-only verdict: its final change report contains an absolute workspace link despite the shared procedure's report-path rule. This does not alter the narrowly specified scope/order assertion.

## Audit and validity

All 22 editor tool-call batches and 8 reader tool calls were inspected, including nested commands and their exact results. All 30 captured calls have exactly one result. All five editors fully load both instruction files before target/source content reads. Every reader performs exactly one read of its manifest artifact; none reads source, links, instructions or oracles. No observed call accesses out-of-manifest content, performs network/external mutation, or changes an unauthorized artifact.

The runtime editor's first filename query is rejected by a security hook because an exclusion glob includes `.git/`; the result records that rejection. Its retry stays within the same allowed directories. The rejected call does not disclose content or invalidate isolation.

All recorded baseline/instruction hashes match. Revised archive bytes match the staged files. Non-target inputs are unchanged. All three staged Git checkouts are clean, and the complete file membership/bytes at both review refs match the supplied base/head snapshots. The other two scenarios have no checkout. Mutations are limited to the two selected drafts and two authorized new drafts; missing-context writes nothing.

The captured traces show no missing call/result pair or observed isolation violation. This supports validity within the supplied evidence; it does not independently authenticate an omitted portion of an upstream session log. Prompt transports are encrypted, and the plaintext full prompts are orchestrator-attested, not cryptographically matched. Their recipients match the session records.

All editor and reader session records specify `gpt-6-astra`, reasoning effort `xhigh`, and `fork_turns: none`. Model build and temperature are not exposed. Shared-filesystem isolation relies on prompt allowlists plus trace auditing rather than separate filesystem sandboxes. These are single controlled model-reader comparisons, not evidence of general human comprehension or repeatability across model settings.
