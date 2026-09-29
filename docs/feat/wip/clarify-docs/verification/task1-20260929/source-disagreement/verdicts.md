# source-disagreement: independent verdicts

Date: 2026-09-29. **Assertion outcome: PARTIAL — 4 PASS, 1 PARTIAL; acceptance is not established.**

**Run validity: PASS under the declared allowlist-and-trace protocol.** The three prompt files record separate `fork_turns: none` sessions; the original/revised reader prompts differ only in artifact paths and use the same neutral role, five questions, pointer requirement and explicit-uncertainty instruction. Their `message_plaintext` fields are orchestrator-attested copies of the live spawn inputs, not cryptographically verified decryptions; the encrypted transport fields remain preserved. The three session records identify distinct general-purpose sessions with `gpt-6-astra`/`xhigh`. Model build and temperature are not exposed.

All recorded tool calls and matching outputs were inspected. No out-of-manifest subject-matter access, oracle/other-version leakage, external lookup or reader mutation was observed. Instructions and source/artifact read outputs match the archived full contents. Original files match the corresponding `test-files/` fixtures; all `hashes.txt` entries and both instruction hashes were independently recomputed. Shared filesystem access was constrained by manifests and audited calls, not OS isolation; standard harness/repository context remained available. Shell-startup output includes a failed unrelated `navi.log` creation, with no disclosed source content.

Evidence: [manifest](manifest.json), [editor prompt](editor-prompt.json), [original reader prompt](reader-original-prompt.json), [revised reader prompt](reader-revised-prompt.json), [editor session](editor-session.json), [original reader session](reader-original-session.json), [revised reader session](reader-revised-session.json), [editor trace](editor-trace.jsonl), [original reader trace](reader-original-trace.jsonl), [revised reader trace](reader-revised-trace.jsonl), [hashes](hashes.txt).

**Trace audit.** Editor: 5 paired calls — complete instruction reads (14), three allowed artifact/source reads (20), guide patch (31), patch wait (38), guide verification read (42). Each reader has one paired guide-only read (10); neither follows the newly added source links outside its reader manifest.

**Five-question comparison.** Original: 2 PASS, 2 PARTIAL, 1 FAIL. Revised: 4 PASS, 1 PARTIAL. The revised artifact supports the complete oracle, but the observed revised reader response does not fully demonstrate the prescribed numerical case.

Answers: [original](reader-original-response.md), [revised](reader-revised-response.md). Answers are assessed for their meaning across the complete response; missing explicit requirements are not supplied from the grader's source knowledge.

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both responses identify defaults with item exceptions. |
| 2 — Representative case | FAIL | PARTIAL | Original Q2 presents next-day activation as current. Revised Q2 covers default 15 and snapshots, and Q3 supplies the timing conflict, but neither answer follows the required 15→20 change through immediate 20 versus required delayed activation. |
| 3 — Current increment | PARTIAL | PASS | Original Q3 names lookup/snapshots without the mismatch. Revised Q3 explicitly distinguishes required next-day activation from current immediate lookup. |
| 4 — Exclusions | PASS | PASS | Both responses identify scheduling. |
| 5 — Decisions | PARTIAL | PASS | Original Q5 mentions only badges. Revised Q5 includes Product's badge decision and the feature maintainer's reconciliation action. |

**Assertion grading.** Fidelity, correctness, orientation and preservation were compared directly with artifacts and sources, independently of reader accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 2.1 | PARTIAL | reader-revised-response.md Q2 stops at default 15; Q3 explains immediate lookup versus required next-day activation, but no answer works through 15→20. The full case exists in revised/guide.md paragraphs 2–3, which establishes artifact support, not the missing observed reader answer. |
| 2.2 | PASS | revised/guide.md retains the mandatory next-day requirement and explicitly describes the immediate value returned by the inspected effective_minutes implementation. It calls their difference unresolved and permits only later implementation work or an approved requirement change. |
| 2.3 | PASS | editor-trace.jsonl ordinals 14→18 load both complete instructions, 20→25 inspect guide.md, requirements.md and prep.py, then 31 patches guide.md. |
| 2.4 | PASS | revised/guide.md names the feature maintainer and the concrete next step: reconcile next-day activation with the scheduling exclusion and identify implementation work or an approved requirement change. It explicitly says next-day activation is not implemented; editor-response.md reports the gap. |
| 2.5 | PASS | The sole recorded mutation is guide.md. Original/revised prep.py and requirements.md are byte-identical; file inventories and hashes.txt agree. |

The predeclared defect is corrected in the artifact without deleting the accepted intent. Zero overrides and existing immutable snapshots remain supported. No requirement decision, implementation repair or resolved badge choice is claimed. To establish acceptance, a fresh comparison must demonstrate the full predeclared case; this report does not fill in the reader's missing answer.

These results describe the observed model-reader comparison; they do not prove improved comprehension for all human readers.
