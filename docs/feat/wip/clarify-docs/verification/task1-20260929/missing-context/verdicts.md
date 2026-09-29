# missing-context: independent verdicts

Date: 2026-09-29. **Assertion outcome: PASS — 5/5 assertions.**

**Run validity: PASS under the declared allowlist-and-trace protocol.** The three prompt files record separate `fork_turns: none` sessions; the original/revised reader prompts differ only in artifact paths and use the same neutral role, five questions, pointer requirement and explicit-uncertainty instruction. Their `message_plaintext` fields are orchestrator-attested copies of the live spawn inputs, not cryptographically verified decryptions; the encrypted transport fields remain preserved. The three session records identify distinct general-purpose sessions with `gpt-6-astra`/`xhigh`. Model build and temperature are not exposed.

All recorded tool calls and matching outputs were inspected. No out-of-manifest subject-matter access, oracle/other-version leakage, external lookup or reader mutation was observed. Instructions and source/artifact read outputs match the archived full contents. Original files match the corresponding `test-files/` fixtures; all `hashes.txt` entries and both instruction hashes were independently recomputed. Shared filesystem access was constrained by manifests and audited calls, not OS isolation; standard harness/repository context remained available. Shell-startup output includes a failed unrelated `navi.log` creation, with no disclosed source content.

Evidence: [manifest](manifest.json), [editor prompt](editor-prompt.json), [original reader prompt](reader-original-prompt.json), [revised reader prompt](reader-revised-prompt.json), [editor session](editor-session.json), [original reader session](reader-original-session.json), [revised reader session](reader-revised-session.json), [editor trace](editor-trace.jsonl), [original reader trace](reader-original-trace.jsonl), [revised reader trace](reader-revised-trace.jsonl), [hashes](hashes.txt).

**Trace audit.** Editor: 5 paired calls — complete instruction read (14), allowed guide/requirements reads plus the expressly allowed missing retention.md lookup (19), guide patch (30), patch wait (37), guide verification read (41). Each reader has one paired guide-only read (10).

**Five-question comparison.** Original: 2 PASS, 2 PARTIAL, 1 FAIL. Revised: 5 PASS. The baseline's unqualified runtime claims and claim that no decisions remain are repaired; the correct explicit unknown is retained.

Answers: [original](reader-original-response.md), [revised](reader-revised-response.md). Answers are assessed for their meaning across the complete response; missing explicit requirements are not supplied from the grader's source knowledge.

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both identify a downloadable record of completed orders for owners. |
| 2 — Representative case | PARTIAL | PASS | Original Q2 gives CSV/link behavior without its unverified contract status. Revised Q2 explicitly identifies the accepted contract and unavailable implementation. |
| 3 — Current increment | PARTIAL | PASS | Original Q3 describes CSV creation as delivered behavior. Revised Q3 names the request-to-CSV-and-link contract. |
| 4 — Exclusions | PASS | PASS | Both identify scheduled exports; revised Q2 also records the lack of runtime evidence. |
| 5 — Decisions | FAIL | PASS | Original Q5 repeats that none remain. Revised Q5 identifies the missing retention decision, data steward and dependency before cleanup documentation. |

**Assertion grading.** Fidelity, correctness, orientation and preservation were compared directly with artifacts and sources, independently of reader accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 3.1 | PASS | reader-revised-response.md answers all five from revised/guide.md: purpose, one CSV plus link as an accepted unverified contract, on-demand scope, scheduled-export exclusion and unknown retention. |
| 3.2 | PASS | editor-trace.jsonl ordinals 14→17 load both complete instructions. Ordinals 19→24 read guide.md and requirements.md and attempt retention.md, receiving No such file or directory, before the documented limitation is written at ordinal 30. |
| 3.3 | PASS | revised/guide.md explicitly says implementation was not supplied, retention duration is not established and cleanup timing is unresolved. Comparison with requirements.md reveals no invented duration, verified execution or settled cleanup behavior. |
| 3.4 | PASS | The final paragraph of revised/guide.md states retention.md is unavailable and the data steward must supply the retention decision before cleanup behavior can be documented. |
| 3.5 | PASS | Only guide.md is patched. The original/revised inventories contain just guide.md and requirements.md; requirements.md is byte-identical and hashes.txt verifies. No retention.md, ledger or summary is created. |

The failed retention lookup is an intended in-manifest observation, not a source-access violation. The original heading survives, and no links, task state or executable examples are altered.

These results describe the observed model-reader comparison; they do not prove improved comprehension for all human readers.
