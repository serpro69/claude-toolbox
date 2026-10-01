**PASS — regression 15: all four assertions pass.** Evidence below refers to the [scenario directory](/home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task3-20261001/pr-regressions/pr-unavailable-source).

| Assertion | Verdict | Concrete evidence |
|---|---|---|
| 15.1 | PASS | `editor/trace.jsonl:9–10` records the sole write: adding `drafts/pr-15.md`. Recomputed before/after hashes confirm both inputs unchanged and only that draft added. No network or external mutation appears. |
| 15.2 | PASS | `editor/after/drafts/pr-15.md` explicitly marks delivery and passing tests unverified; lists unavailable commit IDs, diff, source and test output; rejects branch names as proof of increment; assigns the PR author exact revisions, diff and test-output delivery. |
| 15.3 | PASS | `readers/revised/final.md`, also preserved in native trace line 4, answers all five oracle questions correctly. The comparison below distinguishes repaired understanding from artifact fidelity. |
| 15.4 | PASS | Draft paragraphs 1, 3 and 5 preserve confirmed purpose, `15/null→15`, explicit `0→0`, persistence/scheduling exclusion and the product owner’s unresolved badge decision. Full instruction results at editor trace lines 4 and 6 precede subject reads at lines 7–8. |

| Fixed oracle question | Original reader | Revised reader |
|---|---|---|
| Purpose | PASS: restaurant defaults avoid repeated preparation times. | PASS: same purpose. |
| Representative case | PARTIAL: correct intended null/zero contract, but no runtime-unverified qualification. | PASS: intended contract is explicit; answer 3 establishes unverified delivery. |
| Increment, evidence and owner | FAIL: says the increment ships runtime resolution and cannot identify the evidence owner. | PASS: actual increment remains unknown; PR author supplies exact revisions, diff and test output. The draft separately identifies source as unavailable. |
| Excluded work | PASS: persistence and scheduling deferred. | PASS: explicitly outside this PR. |
| Open decision | PASS: product owner owns badges. | PASS: preserves decision and owner. |

The original reader largely comprehends its supplied artifact, but that artifact contains the predeclared fidelity defect: unsupported delivery and test-success claims. The revised artifact repairs those claims using `editor/before/context.md`, without changing confirmed intent or settling the badge decision. The completion message accurately reports the remaining verification gap; no unsupported factual addition was found.

**Evidence audit: PASS within the supplied protocol.**

- Recomputed hashes match both frozen instruction files, all fixture records, manifests, prompts and before/after artifacts. Instructions contain the recorded 616 and 1,297 words. Original reader input equals the remote capture; revised reader input equals the produced draft. Both reader artifacts remain unchanged.
- All editor reads and its destination-existence check match its manifest. Readers each read only their permitted artifact. Shell reads use `login=false`; no oracle access, other-session access, delegation, fixture execution or extra report write appears.
- Editor has four paired calls/results across 12 retained records; each reader has one pair across five records. Every coverage-map record hash matches its retained native line. Instruction and artifact results match complete file contents; saved finals match native finals. No native truncation or unmatched call was found.
- Reader prompts are identical after substituting the artifact path. Both recorded runs use fresh `default` agents, `fork_turns: none`, `gpt-6-astra`, `xhigh`, and equal recorded turn settings. Their read-output limits differ—5,000 versus 6,000 tokens—but both artifacts were returned completely.
- All five dispatch receipts match native call IDs, timestamps, settings and results; plaintext prompt hashes match and recorded save times precede submission. Dispatch lines 3–6 contain **two capacity failures**, not completed reader runs. Lines 1–2, 7–8 and 9–10 link successful editor/original/revised dispatches to their corresponding metadata and completed traces.

Native dispatch message payloads are encrypted. Exact saved plaintext, matching hashes, receipts and run linkage are present, so this is the protocol’s **opaque-transport limitation**, not missing or reconstructed prompt evidence. I could not independently decrypt transport or recount excluded records in original session rollouts; completeness is supported by the supplied coverage maps and internally consistent native records. These synthetic offline results do not certify a live connector or improved human comprehension.
