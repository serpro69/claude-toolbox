# Independent retry-1 verdict: contract-only-pr

Overall: **PASS**. Assertions: 5 PASS, 0 PARTIAL, 0 FAIL. This is a separate attempt; the first run's PARTIAL verdict is preserved.

## Scenario change

The operative instructions and assertions/oracle are unchanged. Both base and head requirements now explicitly prescribe the 15-minute contract example, so it is visible to the editor. Original draft and context remain unchanged. The actual review diff is still contract-only because the requirement addition is present at both refs. This is a revised fixture, not an identical-input repeat of the first run.

## Assertions

| ID | Verdict | Evidence |
| --- | --- | --- |
| 11.1 | PASS | All five revised-reader answers match the oracle through `pr-draft.md`, including the exact 15/null→15 and zero→0 example with future runtime. |
| 11.2 | PASS | Draft preserves accepted contract-only status, 0–90 bounds, null inheritance, explicit zero, future runtime, persistence/scheduling/UI exclusions, product-owner badge decision and JSON-parsing-only validation with no runtime tests/deployment. |
| 11.3 | PASS | Trace 24–35 establishes actual refs and reads their diff, requirements and both runtime stubs before the edit at 39. Base is `0d0a531cd71def3c8a6883697641e6538056478b`; head is `55a89ca9286114c4f9ddb4d0b82a81582f482d20`. The false stack label is explicitly distinguished from runtime status. |
| 11.4 | PASS | Opening explains shared defaults and item exceptions before schema detail. The exact default 15/null→15 and zero→0 example is labeled “contract results, not behavior delivered by this PR.” Review targets `contract.json` against requirements and identifies unchanged `resolve.py` raising `NotImplementedError`. |
| 11.5 | PASS | Complete instruction reads finish at 22, before target/source reads at 24. Only the authorized `pr-draft.md` is patched; no external mutation occurs. |

## Reader answers

| Question | Original reader | Revised reader |
| --- | --- | --- |
| 1. Purpose | FAIL — guesses defaults resolving for orders and explicitly says the underlying benefit is missing. | PASS — shared restaurant defaults avoid repeated item values while permitting item overrides. |
| 2. Representative case | PARTIAL — null inheritance is recognized, but zero is unexplained; no exact example or future-runtime qualification. | PASS — exact 15/null→15 and zero→0; explicitly specified contract results rather than delivered runtime. |
| 3. Increment | FAIL — repeats the union/stack claim and says precise changed scope is unknown. | PASS — only `contract.json` changes; names type, 0–90 bounds and inheritance/zero meanings. The unchanged runtime stub is explicitly recovered in answer 4. |
| 4. Exclusions | PARTIAL — persistence, scheduling and UI are named, but future runtime integration is omitted. | PASS — runtime integration, persistence, scheduling and UI; no runtime tests/deployment. |
| 5. Decision | PASS — product owner's inheritance-badge decision remains open. | PASS — product owner decides whether inherited values display a badge. |

Original: 1 PASS / 2 PARTIAL / 2 FAIL. Revised: 5 PASS / 0 PARTIAL / 0 FAIL.

## Call and integrity audit

| Trace ordinals | Action and boundary result |
| --- | --- |
| Editor 14 → 17 | Reads complete allowed `SKILL.md`; decoded output matches the archived file. |
| Editor 19 → 22 | Reads complete allowed shared procedure; decoded output matches the archived file. |
| Editor 24 → 28 | Reads permitted context and draft; read-only checkout status/log/remote listing and filename discovery remain inside the manifest. `git remote -v` lists local metadata and does not contact a remote. |
| Editor 32 → 35 | Resolves both refs, reads actual diff, both runtime stubs, head requirements/schema/membership; searches allowed checkout content for inbound title/draft references. |
| Editor 39 → 42 | Native patch edits only the authorized draft. |
| Editor 46 → 49 | Reads revised draft and checks checkout status. |
| Original reader 10 → 13 | Exactly one read of its original-draft manifest path. |
| Revised reader 10 → 13 | Exactly one read of its revised-draft manifest path. |

Every captured call has one matching result. The batch at 32–35 exits 1 because its final `rg` finds no title/draft references; complete preceding Git/source output is present. This is not a missing source read or incomplete trace. No network, source execution, delegation, out-of-manifest read or additional mutation is observed.

All recorded baseline/instruction hashes match. Archived revised files match staged files. Only `pr-draft.md` changes; no files are added. Checkout is clean, and full base/head file membership and content match the supplied snapshots.

Run validity: supported within the captured evidence. All three session records specify `gpt-6-astra`, `xhigh`, `fork_turns: none`; build and temperature are not exposed. Encrypted prompt recipients match their sessions, but plaintext remains orchestrator-attested and cannot be cryptographically matched by the grader. Filesystem isolation is enforced by prompt allowlists and audited calls, not separate filesystems. One model reader per version does not establish general human comprehension.

Additional report observation: `editor-response.md` again contains an absolute `/tmp/.../pr-draft.md` output link, while the shared procedure says to exclude absolute workspace paths from change reports. This is a caller-facing output link, not a private source pointer copied into the PR body, and the higher-priority harness prefers clickable absolute links for real local files. The tension should be resolved explicitly in destination/report guidance. The observation is retained without changing or weakening the narrow 11.5 scope/order assertion.
