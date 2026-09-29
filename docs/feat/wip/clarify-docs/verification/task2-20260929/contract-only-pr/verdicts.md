# Independent verdict: contract-only-pr

Overall: **PARTIAL — not a pass**. Assertions: 3 PASS, 2 PARTIAL, 0 FAIL. The edit repairs the false runtime claim, but uses a 20-minute example where the assertion and oracle require 15. No output was repaired during grading.

## Assertions

| ID | Verdict | Evidence |
| --- | --- | --- |
| 11.1 | PARTIAL | Revised reader answers 1, 3, 4 and 5 recover the required meaning. Answer 2 explicitly uses “20-minute” / `null` → 20, whereas the oracle requires default 15 / `null` → 15. See the separate reader grades below. |
| 11.2 | PASS | `revised/pr-draft.md` preserves the accepted contract, inclusive 0–90 range, null inheritance, explicit zero, contract-only diff, future runtime, persistence/scheduling/UI exclusions, product-owner badge decision, JSON-syntax-only validation, and absence of runtime tests/deployment. |
| 11.3 | PASS | Editor trace ordinals 19–28 establishes the repository/ref context, resolves `review-base` to `c903db5c033b62e6cd64f97e96b4a0de778e43fb` and `review-head` to `6cb425e8212c7cebac2c088b76f40c8165de13b9`, reads the actual diff, requirements and both runtime stubs before the edit at ordinal 34. Only `contract.json` changes; the “runtime-complete” label does not control the result. |
| 11.4 | PARTIAL | Purpose leads the draft; examples are explicitly contract semantics and runtime is future. The review path identifies `contract.json`, `requirements.md` and unchanged `resolve.py`. However, the required “default 15/null→15” example is replaced by “default of 20 minutes” / null → 20. Zero → 0 survives. |
| 11.5 | PASS | Full instruction output completes at ordinal 17 before target/source reads at 19. The only mutation is the native patch of `pr-draft.md` at 34. No network/external mutation occurs; context and checkout sources remain unchanged. |

The 20-minute example is consistent with the general contract and was introduced as an example, not as a product default. Nevertheless, it does not satisfy the exact 15-minute assertion/oracle; the grade does not substitute semantic plausibility for the written requirement.

## Reader answers

Grades compare the captured answers with `grader-inputs/oracle/expected.json`, not with what a grader could independently infer from source. Baseline failures reflect information unavailable or misleading in the original artifact, not unauthorized reader behavior.

| Question | Original reader | Revised reader |
| --- | --- | --- |
| 1. Purpose | FAIL — quotes “defaults now resolve for orders” and says the user benefit is unspecified; does not recover shared defaults avoiding repetition. | PASS — explicitly says restaurant defaults avoid repeating item preparation times and identifies the item-override contract. |
| 2. Representative case | PARTIAL — reports null propagating the restaurant value, but zero is an unexplained “discriminator”; no 15-minute example or future-runtime qualification. | PARTIAL — correctly distinguishes specified behavior from runtime and preserves zero, but answers with 20/null→20 instead of 15/null→15. |
| 3. Increment | FAIL — describes a union/schema and says implementation scope is missing; does not establish contract-only scope or the unchanged stub. | PASS — says only `contract.json` changes and describes its accepted values; answer 4 also explicitly identifies the unchanged `NotImplementedError` stub. |
| 4. Exclusions | PARTIAL — persistence, scheduling and UI are named, but future runtime integration is missing. | PASS — names runtime resolution, persistence, scheduling and UI, plus the validation limits. |
| 5. Decision | PASS — identifies the product owner's inheritance-badge decision and marks unspecified criteria. | PASS — identifies the product owner's choice whether inherited values display a badge. |

Original: 1 PASS / 2 PARTIAL / 2 FAIL. Revised: 4 PASS / 1 PARTIAL / 0 FAIL.

## Call and integrity audit

All captured calls/results were inspected, including nested commands; every call has exactly one captured result.

| Trace ordinals | Action and boundary result |
| --- | --- |
| Editor 14 → 17 | Reads the two allowed instruction files completely; result equals their archived concatenation byte-for-byte. |
| Editor 19 → 23 | Reads allowed `context.md` and `pr-draft.md`; read-only status/branch/log and filename discovery stay inside allowed `checkout/`. |
| Editor 25 → 28 | Read-only Git revisions, diff, head membership and source reads stay inside `checkout/`. |
| Editor 34 → 37 | Native patch changes only the authorized draft. |
| Editor 39 → 42 | Reads the revised authorized draft. |
| Original reader 10 → 13 | One read of its exact original-draft manifest path; no other calls. |
| Revised reader 10 → 13 | One read of its exact revised-draft manifest path; no other calls. |

Recorded baseline/instruction hashes all match. Archived revised files match the staged files. Only `pr-draft.md` differs from the original non-checkout files; there are no added files. Checkout is clean, and every file at both Git refs matches the respective supplied source snapshot, including membership.

Run validity: no observed out-of-manifest access, missing call/result pair, or instruction-order violation. All three session records report `gpt-6-astra`, `xhigh`, `fork_turns: none`; build and temperature are not exposed. Encrypted prompt records have matching recipients, but their plaintext is only orchestrator-attested and cannot be cryptographically matched by this grader. These are controlled model-reader results, not proof of human comprehension.

Additional report observation, outside the explicit assertions: `editor-response.md` uses an absolute `/tmp/.../pr-draft.md` link despite the shared procedure's instruction to exclude absolute workspace paths from change reports. This does not disclose any of this scenario's protected business facts, and does not change the narrow 11.5 scope/order grade.
