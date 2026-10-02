# Independent PR and optional-consumer verification

**46 PASS, 0 FAIL, 0 PARTIAL. All ten scenarios pass.** PR cases 11–15 contribute 26 assertions; the five current design/document consumers contribute 20. Fixed assertion IDs and meanings are preserved in each verdict file. No required fixes remain.

| Scenario | Assertions | Verdict |
| --- | ---: | --- |
| [clarity-after-drafting](../clarity-after-drafting/verdicts.json) | 5 | PASS |
| [clarity-preserves-profile](../clarity-preserves-profile/verdicts.json) | 5 | PASS |
| [clarity-refined-documents-only](../clarity-refined-documents-only/verdicts.json) | 4 | PASS |
| [clarity-unchanged-document](../clarity-unchanged-document/verdicts.json) | 3 | PASS |
| [clarity-unchanged-resume](../clarity-unchanged-resume/verdicts.json) | 3 | PASS |
| [contract-only-pr](../contract-only-pr/verdicts.json) | 5 | PASS |
| [destination-visibility](../destination-visibility/verdicts.json) | 8 | PASS |
| [pr-missing-context](../pr-missing-context/verdicts.json) | 3 | PASS |
| [pr-unavailable-source](../pr-unavailable-source/verdicts.json) | 4 | PASS |
| [runtime-pr](../runtime-pr/verdicts.json) | 6 | PASS |

The audit covered 18 fresh sessions, 86 retained top-level tool calls and their results, all visible assistant commentary/final messages, exact read/write manifests, fixed reader questions, artifacts, source evidence and settings. Every run used the default role with `fork_turns=none`, `gpt-6-astra` at `max` effort, and no override or delegation. Each original/revised reader saw only its own named artifact, with identical settings and no writes. All revised readers answer the five fixed questions correctly. Case 13's original reader also passes all five, as required; the other original-reader defects are baseline observations, not acceptance requirements.

Before/after hashes were recomputed independently. Native patches reproduce the final changed artifacts exactly. Decoding the portable Git metadata, verifying object hashes and following the commit trees confirms the actual PR increments: cases 11 and 13 change only `contract.json`; case 12 changes `resolve.py` and adds `test_resolve.py`. All corresponding source snapshots match those objects. No successful out-of-manifest subject read, unauthorized write, network call, external mutation, source execution or oracle leak appears in the audited editor/reader records.

Case 13's destination and every editor commentary/final message were checked for restricted facts and pointers, including uncited paraphrases. Legitimate task/public/shared references remain, the successful JSON-parsing outcome is in the draft itself, and only the caller's completion message contains the permitted selected-output absolute link.

Evidence limits and resolved capture findings:

- [Drafting record 29](../clarity-after-drafting/editor/behavior-records.json) contains a 721-token truncation inside `frameworks.md`. The other required instruction files in that response are complete. The full framework file returns at record 37, before subject action; no instruction coverage remains missing.
- The initial short pre-dispatch excerpts omitted prompt echoes for the refinement editor, unavailable-source editor and original contract reader. Supplemental lossless extracts of existing native records resolve these gaps: [478 before dispatch 508](../clarity-refined-documents-only/editor/prompt-provenance.json), [388 before 408](../pr-unavailable-source/editor/prompt-provenance.json), and [653 before 669](../contract-only-pr/original-reader/prompt-provenance.json). The runtime editor's earlier echo at [229 before 250](../runtime-pr/editor/prompt-provenance.json) also supplements its short excerpt.
- All 18 [supplemental prompt records](../prompt-provenance-index.json) were independently decoded and compared byte-for-byte with saved prompts, including trailing newlines. Their hashes, call/output IDs, ordinal/timestamp order, dispatch receipt and child/session linkage agree. Editor eval prompts remain unchanged. Encrypted native transport was not decrypted; acceptance follows the retained-plaintext/hash/receipt protocol.
- [Contract capture attempt 1](../contract-only-pr/capture-attempt-1/README.md) remains invalid and excluded: its saved prompt had an extra trailing LF. The fresh retry is the accepted run. [Initial staging failure](../staging-note.md) occurred before behavioral dispatch and is also excluded.
- Two Git-exclusion filename globs were blocked before execution; permitted in-scope listings succeeded. A consumer's `git status` returned “not a git repository”; no repository content was returned. These events remain recorded in the respective verdicts.
- The audit establishes consistency of the complete retained visible export. System/developer boilerplate and hidden reasoning are excluded by protocol; original native logs were not reopened. Shared filesystem access is not OS isolation or a system-call audit. The source revision and all 36 instruction-file hashes are recorded, with no instruction-hash mismatch.
- Synthetic offline responses do not certify live connectors or improved human comprehension. Current consumer cases assess ordinary drafting and optional follow-up recommendations, without an automatic clarification pass.

No tested instructions, assertions, fixtures, prompts, traces or artifacts were changed by this grader. Only the ten verdict files and this summary were authored.

