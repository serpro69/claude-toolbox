# cross-file-preservation: independent verdicts

Date: 2026-09-29. **Assertion outcome: PASS — 5/5 assertions.**

**Run validity: PASS under the declared allowlist-and-trace protocol.** The three prompt files record separate `fork_turns: none` sessions; the original/revised reader prompts differ only in artifact paths and use the same neutral role, five questions, pointer requirement and explicit-uncertainty instruction. Their `message_plaintext` fields are orchestrator-attested copies of the live spawn inputs, not cryptographically verified decryptions; the encrypted transport fields remain preserved. The three session records identify distinct general-purpose sessions with `gpt-6-astra`/`xhigh`. Model build and temperature are not exposed.

All recorded tool calls and matching outputs were inspected. No out-of-manifest subject-matter access, oracle/other-version leakage, external lookup or reader mutation was observed. Instructions and source/artifact read outputs match the archived full contents. Original files match the corresponding `test-files/` fixtures; all `hashes.txt` entries and both instruction hashes were independently recomputed. Shared filesystem access was constrained by manifests and audited calls, not OS isolation; standard harness/repository context remained available. Shell-startup output includes a failed unrelated `navi.log` creation, with no disclosed source content.

Evidence: [manifest](manifest.json), [editor prompt](editor-prompt.json), [original reader prompt](reader-original-prompt.json), [revised reader prompt](reader-revised-prompt.json), [editor session](editor-session.json), [original reader session](reader-original-session.json), [revised reader session](reader-revised-session.json), [editor trace](editor-trace.jsonl), [original reader trace](reader-original-trace.jsonl), [revised reader trace](reader-revised-trace.jsonl), [hashes](hashes.txt).

**Trace audit.** Editor: 7 paired calls — complete instructions (14), all four allowed documents including inbound-link evidence (19), two-file patch (28), patch wait (35), verification read (39), in-scope tasks relocation patch (46), final tasks read (51). Each reader has one paired call reading exactly its three allowed documents (14).

**Five-question comparison.** Original: 5 PASS. Revised: 5 PASS. The original response's Q3 states counting is unfinished, qualifying its present-tense Q2 example. The repair addresses the predeclared admission-observation jargon while making planned status explicit; answer accuracy alone does not establish preservation.

Answers: [original](reader-original-response.md), [revised](reader-revised-response.md). Answers are assessed for their meaning across the complete response; missing explicit requirements are not supplied from the grader's source knowledge.

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both identify catching CSV errors before applying imports. |
| 2 — Representative case | PASS | PASS | Both give three input rows, two valid, one invalid and zero writes; original Q3 marks counting unfinished, and revised Q2 explicitly calls this planned. |
| 3 — Current increment | PASS | PASS | Both distinguish preview-only delivery, column parsing complete and counts pending. The revised response additionally distinguishes recorded progress from inspected implementation. |
| 4 — Exclusions | PASS | PASS | Both identify disabled/future apply and Task 2's dependency. |
| 5 — Decisions | PASS | PASS | Both identify Product's duplicate-row policy and support approval before enablement; neither invents approval status. |

**Assertion grading.** Fidelity, correctness, orientation and preservation were compared directly with artifacts and sources, independently of reader accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 4.1 | PASS | The two reader responses recover all five answers through design.md, tasks.md and entry.md. Revised design Context and Task 1 explicitly label the contract planned and source unavailable, with parsing recorded complete and counting pending. |
| 4.2 | PASS | Direct comparison with requirements.md confirms all four required sections, MUST id,name, MAY diagnostics, diagnostics' non-authorization, Mira's 2026-09-01 acceptance, support-owner walkthrough approval gate and Product's open duplicate policy survive. |
| 4.3 | PASS | An ordered byte-string comparison of every Status, Depends on and checkbox line in original/tasks.md versus revised/tasks.md is equal, including in-progress/pending, the em-dash first dependency, Task 1 dependency and all three checkboxes. |
| 4.4 | PASS | entry.md links to tasks.md#task-1-preview and design.md#deployment-gate; design.md links to the task anchor and tasks.md links to the gate. All four targets resolve to retained headings. entry.md and requirements.md are byte-identical; hashes.txt verifies. |
| 4.5 | PASS | revised/design.md opens with plain preview purpose and removes admission-observation terminology. Both selected documents give the two-valid/one-invalid/zero-written planned example; Task 1 leaves the counts checkbox unchecked and explicitly says counting is pending. |

Only design.md and tasks.md change. The second patch moves resume guidance into the existing Task 1 anchor, preserving the entry path. Source-only requirements remain outside both reader traces. No implementation completeness or approval is inferred from fluent prose.

These results describe the observed model-reader comparison; they do not prove improved comprehension for all human readers.
