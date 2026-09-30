# Independent verdict: pr-unavailable-source

Overall: **PARTIAL — not a pass**. Assertions: 3 PASS, 1 PARTIAL, 0 FAIL. The produced artifact preserves the required uncertainty and PR-author next action, but the captured revised reader does not recover every oracle element.

## Assertions

| ID | Verdict | Evidence |
| --- | --- | --- |
| 15.1 | PASS | Only `drafts/pr-15.md` is added. `remote-body.md` and `context.md` remain byte-identical; no network/external mutation appears in the trace. |
| 15.2 | PASS | Draft explicitly says runtime delivery/validation need verification and revisions, diff, source and test output are unavailable. It attributes the prior delivery/tests statements to the original description, warns that branch names do not establish scope, and requires the PR author to provide revisions, diff and test output. |
| 15.3 | PARTIAL | Revised reader answers 1, 2 and 4 match. Answer 3 correctly says increment is uncertain but omits unavailable source and the PR author as the evidence owner. Answer 5 names only the product-owner badge decision and confirmed contract, omitting the oracle's PR-author obligation to establish actual runtime increment/validation. No answer identifies that owner. The artifact contains it; the reader result does not. |
| 15.4 | PASS | Confirmed purpose, default-15/null→15 and explicit zero→zero intended contract, persistence/scheduling exclusions and open product-owner badge decision survive. Complete instructions finish at 17 before evidence reads at 19. |

## Reader answers

| Question | Original reader | Revised reader |
| --- | --- | --- |
| 1. Purpose | PASS — defaults avoid repeating preparation times. | PASS — same confirmed purpose. |
| 2. Representative case | PARTIAL — gives the exact intended 15/null and zero mappings, but does not establish that runtime is unverified; answer 3 repeats the shipping/passing-tests claims without that qualification. | PASS — gives the exact mappings, distinguishes confirmed contract from unverified runtime. |
| 3. Increment | FAIL — reports “We ship runtime resolution” and “all tests pass,” rather than the oracle's unknown increment pending actual evidence. | PARTIAL — uncertainty, exact revisions and diff are correct; missing source availability and PR-author ownership are not recovered. |
| 4. Exclusions | PASS — persistence and scheduling are later. | PASS — persistence and scheduling are outside this PR/later work. |
| 5. Decision / unresolved work | PARTIAL — preserves the product-owner badge decision but lacks the PR-author runtime/validation verification obligation. | PARTIAL — preserves the badge decision but still omits the PR-author verification obligation. Statement that the contract is confirmed does not supply that missing owner/next action. |

Original: 2 PASS / 2 PARTIAL / 1 FAIL. Revised: 3 PASS / 2 PARTIAL / 0 FAIL. The grade distinguishes source-backed artifact fidelity from the narrower captured reader outcome; it does not infer the missing answer from the grader's access to the draft.

## Call and integrity audit

| Trace ordinals | Action and boundary result |
| --- | --- |
| Editor 14 → 17 | Reads both complete allowed instruction files; decoded result equals the archived concatenation byte-for-byte. |
| Editor 19 → 22 | Reads only permitted context and remote body, then checks the authorized destination; it does not exist. The conditional read would also be within the allowlist. |
| Editor 26 → 29 | Native patch adds only `drafts/pr-15.md`. |
| Editor 31 → 34 | Reads the permitted output draft. |
| Original reader 10 → 13 | One read of the exact original remote-body manifest path. |
| Revised reader 10 → 13 | One read of the exact revised-draft manifest path. |

Every captured call has exactly one result. No checkout exists or is invented, no source/test execution occurs, and no URL is fetched. The editor proceeds with supported edits using the authorized destination.

All recorded baseline/instruction hashes match; archived revised files equal staged files. Original inputs are unchanged, and the only added file is the authorized draft.

Run validity: no observed out-of-manifest access, incomplete call/result pair, or instruction-order violation. Editor and both reader session records report `gpt-6-astra`, `xhigh`, `fork_turns: none`; build and temperature are not exposed. Encrypted prompt recipients match their sessions; full plaintext is orchestrator-attested, not cryptographically matched. These reader results are one model sample per version, not proof of improved human comprehension.
