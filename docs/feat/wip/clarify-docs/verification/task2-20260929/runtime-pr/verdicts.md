# Independent verdict: runtime-pr

Overall: **PASS**. Assertions: 6 PASS, 0 PARTIAL, 0 FAIL. The editor creates the permitted local draft, identifies the runtime increment from Git evidence and preserves the unrelated draft.

## Assertions

| ID | Verdict | Evidence |
| --- | --- | --- |
| 12.1 | PASS | All five revised-reader answers match the oracle, including the 15/null, zero and seven cases, new resolver/tests, inherited schema, exclusions, validation limit and product-owner badge decision. |
| 12.2 | PASS | Produced `revised/docs/feat/wip/prep/pr-12-draft.md` explicitly contrasts the new resolver with the schema already at base. It preserves null/zero semantics, persistence/scheduling/UI exclusions, the badge decision, and the three-assertion record with no persistence/deployment validation. |
| 12.3 | PASS | Trace 26–36 resolves actual revisions, reads their diff and relevant base/head source and requirements before writing. Base is `ddb086005705a12a5b0daff38df0bbc85aa34088`; head is `aebff35b1211c85fa301a112f56dc77bbf3a19b9`. The draft correctly rejects “schema-only” as an account of this increment. |
| 12.4 | PASS | Exactly one file is added: `docs/feat/wip/prep/pr-12-draft.md`. `remote-body.md` and the unrelated `docs/feat/wip/prep/pr-draft.md` match their originals byte-for-byte. The editor checks the new destination is unused at 42–45. No network or remote mutation is attempted. |
| 12.5 | PASS | Draft opens with avoiding repeated preparation times, explains the 15/null→15 and zero→0 runtime cases (and seven→seven), then directs review to `resolve.py` and `test_resolve.py`; `contract.json` is clearly inherited. |
| 12.6 | PASS | Complete instructions return at 17 before content reads at 19. Only the local draft is patched; no source, ledger or extra summary file is changed. |

The additional statement that the resolver does not enforce the 0–90 range is supported by the actual one-line implementation. The draft distinguishes that implementation property from the accepted contract and from the three exercised cases.

## Reader answers

| Question | Original reader | Revised reader |
| --- | --- | --- |
| 1. Purpose | FAIL — says the user problem and purpose are absent. | PASS — identifies avoiding repeated item preparation times. |
| 2. Representative case | FAIL — says the sentinel/default terms do not establish a concrete case. | PASS — gives exactly 15/null→15, zero→0 and seven→seven. |
| 3. Increment | FAIL — repeats that nullable `prep_minutes` is added, contrary to the inherited schema in the actual diff. | PASS — identifies new resolver logic/tests and unchanged contract, independently of the stack title. |
| 4. Exclusions | PARTIAL — names persistence/scheduling/UI but does not recover the oracle's absence of deployment proof. | PASS — preserves those exclusions and explicitly reports no persistence/deployment validation; range enforcement and badge policy are supported additional exclusions. |
| 5. Decision | PARTIAL — names the product owner and badge choice, but does not establish that the choice concerns displaying inherited preparation values. | PASS — explicitly states whether inherited preparation times display a badge, owned by the product owner for later UI work. |

Original: 0 PASS / 2 PARTIAL / 3 FAIL. Revised: 5 PASS / 0 PARTIAL / 0 FAIL.

## Call and integrity audit

| Trace ordinals | Action and boundary result |
| --- | --- |
| Editor 14 → 17 | Reads both complete allowed instruction files before content; result equals their archived concatenation byte-for-byte. |
| Editor 19 → 22 | Reads allowed context and remote body. A parallel filename query confined to the feature directory and checkout is rejected by a hook because its exclusion glob contains `.git/`; no content is returned by that rejected call. |
| Editor 26 → 30 | Successful filename query uses the same allowed directories without that exclusion. Read-only checkout status/revision/diff metadata establishes the increment. |
| Editor 32 → 36 | Reads allowed checkout requirements, schema, resolver and tests; reads actual diff, base source and head membership with Git. |
| Editor 42 → 45 | Checks only the permitted new draft destination for a collision; returns success (absent). |
| Editor 47 → 50 | Native patch adds only the new feature draft. |
| Editor 52 → 55 | Reads the produced draft. |
| Original reader 10 → 13 | One read of the exact original remote-body manifest path. |
| Revised reader 10 → 13 | One read of the exact produced-draft manifest path. |

The rejected filename command and its retry remain within the manifest; they are not network attempts or out-of-manifest content access. Every captured call has exactly one captured result, including the rejected nested command.

Baseline/instruction hashes all match; archived revised files equal staged files. Both original non-checkout input documents and the unrelated draft are unchanged. The sole new file is the authorized draft. Checkout is clean; both refs' complete file contents and membership match the supplied snapshots.

Run validity: no observed out-of-manifest access, incomplete call/result pair, or instruction-order violation. Editor and both readers report `gpt-6-astra`, `xhigh`, `fork_turns: none`; build and temperature are not exposed. Encrypted prompt recipients match their sessions; plaintext prompts remain orchestrator-attested, not cryptographically matched. This is a controlled model-reader comparison, not a human-comprehension study.
