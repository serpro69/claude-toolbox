# Independent retry-1 verdict: pr-unavailable-source

Overall: **PASS**. Assertions: 4 PASS, 0 PARTIAL, 0 FAIL. The new revised reader recovers the evidence gap and its owner. The first run's PARTIAL verdict remains unchanged.

## Scenario change

Operative skill instructions, editor inputs and assertions are unchanged. Reader question 3 now explicitly asks what evidence and owner are needed to establish an unknown increment. The oracle locates the PR-author evidence/action expectation there instead of also including it in answer 5; all protected claims remain required. Original and revised readers receive the same revised questions. This changes the measurement prompt, so the retry must not be presented as an identical-method replication or evidence of an improved skill version.

## Assertions

| ID | Verdict | Evidence |
| --- | --- | --- |
| 15.1 | PASS | Only `drafts/pr-15.md` is added; remote body and context are unchanged. No network or external mutation appears in the trace. |
| 15.2 | PASS | “Scope and review” says exact commit IDs, diff and source are unavailable and delivered changes cannot yet be confirmed. “Validation” attributes shipping/passing-tests claims to the original, marks them unverified and requires the PR author to supply relevant source/test output with revisions/diff. |
| 15.3 | PASS | All revised-reader answers match the revised oracle. Answer 3 explicitly identifies unknown scope, unverified runtime/tests, the PR author and exact base/head revisions, diff, source and test output. |
| 15.4 | PASS | The draft retains confirmed purpose, 15/null→15 and zero→0 intended contract, persistence/scheduling exclusions and the product-owner badge decision. Complete instructions finish at 17 before evidence reads at 19. |

## Reader answers

| Question | Original reader | Revised reader |
| --- | --- | --- |
| 1. Purpose | PASS — restaurant defaults avoid repeated preparation times. | PASS — same purpose for callers. |
| 2. Representative case | PASS — exact intended 15/null and zero mappings; notes no verifying execution example, and answer 3 explicitly marks actual behavior unverified. | PASS — exact confirmed-contract mappings; answer 3 explicitly preserves the unverified-runtime qualification. |
| 3. Increment, evidence and owner | PARTIAL — quotes the runtime claim but qualifies actual behavior/coverage as unverified and asks for implementation/test evidence. Exact revisions/diff and PR-author ownership remain missing; owner is explicitly unspecified. | PASS — unknown actual increment; exact revisions, diff, source, test output and PR-author responsibility are all explicit, with reported branch names kept distinct from evidence. |
| 4. Exclusions | PASS — persistence and scheduling remain later work. | PASS — same explicit exclusions. |
| 5. Decision | PASS — badge choice open and owned by product owner, matching the revised oracle for this question. | PASS — product owner must resolve/record badge behavior; options and criteria are correctly left unknown. |

Original: 4 PASS / 1 PARTIAL / 0 FAIL. Revised: 5 PASS / 0 PARTIAL / 0 FAIL. The original reader's increased skepticism comes from this new captured answer and changed question; no earlier grade is rewritten.

## Call and integrity audit

| Trace ordinals | Action and boundary result |
| --- | --- |
| Editor 14 → 17 | Reads both allowed instruction files completely; decoded output equals their archived concatenation. |
| Editor 19 → 22 | Reads permitted context and remote body; conditional destination check/read is restricted to the allowed output path. No existing destination content returns. |
| Editor 26 → 29 | Native patch adds only the authorized draft. |
| Editor 31 → 34 | Reads that draft for verification. |
| Original reader 10 → 13 | Exactly one read of its original remote-body manifest path. |
| Revised reader 10 → 13 | Exactly one read of its revised-draft manifest path. |

Each captured call has exactly one result. No source checkout, source/test execution, network request, delegation or out-of-manifest content access is attempted.

All baseline/instruction hashes match. Archived revised artifacts equal staged files. Context and remote body remain byte-identical; `drafts/pr-15.md` is the sole added file.

Run validity: supported within the captured evidence. All three sessions specify `gpt-6-astra`, `xhigh`, `fork_turns: none`; build and temperature are not exposed. Encrypted prompt recipients match session identities, but the full plaintext is orchestrator-attested rather than cryptographically matched. Shared-filesystem isolation relies on allowlists and audit; one model-reader sample per version does not establish general human comprehension.
