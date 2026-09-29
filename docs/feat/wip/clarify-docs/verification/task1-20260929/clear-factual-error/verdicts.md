# clear-factual-error: independent verdicts

Date: 2026-09-29. **Assertion outcome: PASS — 4/4 assertions.**

**Run validity: PASS under the declared allowlist-and-trace protocol.** The three prompt files record separate `fork_turns: none` sessions; the original/revised reader prompts differ only in artifact paths and use the same neutral role, five questions, pointer requirement and explicit-uncertainty instruction. Their `message_plaintext` fields are orchestrator-attested copies of the live spawn inputs, not cryptographically verified decryptions; the encrypted transport fields remain preserved. The three session records identify distinct general-purpose sessions with `gpt-6-astra`/`xhigh`. Model build and temperature are not exposed.

All recorded tool calls and matching outputs were inspected. No out-of-manifest subject-matter access, oracle/other-version leakage, external lookup or reader mutation was observed. Instructions and source/artifact read outputs match the archived full contents. Original files match the corresponding `test-files/` fixtures; all `hashes.txt` entries and both instruction hashes were independently recomputed. Shared filesystem access was constrained by manifests and audited calls, not OS isolation; standard harness/repository context remained available. Shell-startup output includes a failed unrelated `navi.log` creation, with no disclosed source content.

Evidence: [manifest](manifest.json), [editor prompt](editor-prompt.json), [original reader prompt](reader-original-prompt.json), [revised reader prompt](reader-revised-prompt.json), [editor session](editor-session.json), [original reader session](reader-original-session.json), [revised reader session](reader-revised-session.json), [editor trace](editor-trace.jsonl), [original reader trace](reader-original-trace.jsonl), [revised reader trace](reader-revised-trace.jsonl), [hashes](hashes.txt).

**Trace audit.** Editor: 6 paired calls — SKILL read (14), shared read (19), the three allowed artifact/source reads (24), guide patch (35), patch wait (42), guide verification read (46). Each reader has one paired guide-only read (original 14, revised 12).

**Five-question comparison.** Original: 5 PASS. Revised: 5 PASS. The five answers do not test the maximum threshold; the predeclared correctness defect still requires and receives repair.

Answers: [original](reader-original-response.md), [revised](reader-revised-response.md). Answers are assessed for their meaning across the complete response; missing explicit requirements are not supplied from the grader's source knowledge.

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both identify a preparation default with item overrides. |
| 2 — Representative case | PASS | PASS | Both identify inherited 15, explicit zero, inherited 20 after the change and earlier order 15. Explicit zero is retained as an override. |
| 3 — Current increment | PASS | PASS | Both identify lookup and the order snapshot. |
| 4 — Exclusions | PASS | PASS | Both identify scheduling. |
| 5 — Decisions | PASS | PASS | Both preserve the product owner's unresolved inheritance badges. |

**Assertion grading.** Fidelity, correctness, orientation and preservation were compared directly with artifacts and sources, independently of reader accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 6.1 | PASS | Both reader response files retain all five oracle answers; the editor nevertheless repairs the independent reference defect. |
| 6.2 | PASS | original/requirements.md requires a 90-minute maximum and original/prep.py declares MAX_DEFAULT_MINUTES = 90. revised/guide.md's Reference section corrects 60 to 90; no new validation/enforcement claim is introduced. |
| 6.3 | PASS | Byte comparison proves revised/guide.md equals original/guide.md with only the exact reference sentence's 60 replaced by 90. Every other byte, protected behavior, identifier, heading and already-clear orientation remains unchanged. |
| 6.4 | PASS | editor-trace.jsonl loads SKILL.md (14→17) and the complete shared instructions (19→22), reads guide plus requirements and prep.py (24→29), then applies the one-sentence guide patch (35). Sources are byte-identical, inventories match and hashes.txt verifies. |

The only predeclared defect is repaired. The constant establishes the documented maximum together with accepted requirements; neither the guide nor this verdict claims that the supplied functions implement range validation.

These results describe the observed model-reader comparison; they do not prove improved comprehension for all human readers.
