# dense-source: independent verdicts

Date: 2026-09-29. **Assertion outcome: PASS — 5/5 assertions.**

**Run validity: PASS under the declared allowlist-and-trace protocol.** The three prompt files record separate `fork_turns: none` sessions; the original/revised reader prompts differ only in artifact paths and use the same neutral role, five questions, pointer requirement and explicit-uncertainty instruction. Their `message_plaintext` fields are orchestrator-attested copies of the live spawn inputs, not cryptographically verified decryptions; the encrypted transport fields remain preserved. The three session records identify distinct general-purpose sessions with `gpt-6-astra`/`xhigh`. Model build and temperature are not exposed.

All recorded tool calls and matching outputs were inspected. No out-of-manifest subject-matter access, oracle/other-version leakage, external lookup or reader mutation was observed. Instructions and source/artifact read outputs match the archived full contents. Original files match the corresponding `test-files/` fixtures; all `hashes.txt` entries and both instruction hashes were independently recomputed. Shared filesystem access was constrained by manifests and audited calls, not OS isolation; standard harness/repository context remained available. Shell-startup output includes a failed unrelated `navi.log` creation, with no disclosed source content.

Evidence: [manifest](manifest.json), [editor prompt](editor-prompt.json), [original reader prompt](reader-original-prompt.json), [revised reader prompt](reader-revised-prompt.json), [editor session](editor-session.json), [original reader session](reader-original-session.json), [revised reader session](reader-revised-session.json), [editor trace](editor-trace.jsonl), [original reader trace](reader-original-trace.jsonl), [revised reader trace](reader-revised-trace.jsonl), [hashes](hashes.txt).

**Trace audit.** Editor: 6 paired calls — SKILL read (14), shared read (19), three allowed artifact/source reads (24), guide patch (35), patch wait (42), guide verification read (48). Original and revised readers: one paired guide-only read each (10).

**Five-question comparison.** Original: 5 PASS. Revised: 5 PASS. The baseline already answered the five questions; the justified improvement is repair of the three predeclared orientation defects, not a demonstrated increase in answer accuracy.

Answers: [original](reader-original-response.md), [revised](reader-revised-response.md). Answers are assessed for their meaning across the complete response; missing explicit requirements are not supplied from the grader's source knowledge.

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both responses identify one restaurant default with item exceptions. |
| 2 — Representative case | PASS | PASS | Both describe inherited 15, explicit zero, later inherited 20 and unchanged earlier orders; the revision makes the complete sequence explicit. |
| 3 — Current increment | PASS | PASS | Both identify resolution/lookup and copying the value into new orders. |
| 4 — Exclusions | PASS | PASS | Both identify scheduling. |
| 5 — Decisions | PASS | PASS | Both preserve the product owner's inheritance-badge decision. |

**Assertion grading.** Fidelity, correctness, orientation and preservation were compared directly with artifacts and sources, independently of reader accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 1.1 | PASS | The revised guide's opening, three example bullets, scheduling paragraph and maintainer paragraph support all five answers without another source; reader-revised-response.md answers all five. |
| 1.2 | PASS | Compared revised/guide.md with original/requirements.md and original/prep.py: missing/null inheritance, explicit zero, live lookup, saved order values, prep_minutes/effective_minutes/create_order, scheduling exclusion and product-owned badge uncertainty survive. New-order 20 and zero-order 0 follow the inspected functions; no unsupported behavior was added. |
| 1.3 | PASS | editor-trace.jsonl ordinals 14→17 load the complete SKILL.md, 19→22 the complete shared procedure, 24→29 guide plus both sources, then 35 applies the edit. |
| 1.4 | PASS | revised/guide.md opens with the owner purpose and saved-copy behavior; storage identifiers occur only in the closing maintainer paragraph. Unexplained materialization/snapshot jargon is removed, and the three bullets explicitly follow inherited item, zero override and existing order across 15→20. |
| 1.5 | PASS | The sole mutation in editor-trace.jsonl is guide.md. Original/revised inventories match; requirements.md and prep.py are byte-identical and hashes.txt verifies. No ledger or summary artifact appears. |

The original guide puts storage before purpose, explains materialization after using it and leaves the numerical results implicit. The revised artifact repairs those predeclared defects. Its heading is retained; no cross-file links, task state or executable examples were changed.

These results describe the observed model-reader comparison; they do not prove improved comprehension for all human readers.
