# Source-disagreement retry 2: independent verdicts

Date: 2026-09-29. **Assertion outcome: PASS — 5/5 assertions.** This is a fresh attempt with stronger implementation evidence; both preceding PARTIAL reports remain unchanged.

**Run validity: PASS under the declared allowlist-and-trace protocol.** The [original reader prompt](reader-original-prompt.json) and [revised reader prompt](reader-revised-prompt.json) are identical apart from artifact paths. Both use a neutral reader role, the same five fixed questions, source pointers and explicit uncertainty. Neither contains the oracle, source-only evidence or information about earlier attempts. The [editor prompt](editor-prompt.json) carries the same request and scope as retry1, with no retry feedback. All three prompts record `fork_turns: none`; their [session](editor-session.json) [records](reader-original-session.json) ([revised](reader-revised-session.json)) identify distinct general-purpose `gpt-6-astra`/`xhigh` sessions. Build and temperature are not exposed.

The plaintext prompt records are orchestrator-attested copies of live spawn inputs. The [eval](grader-inputs/eval.json) and [oracle](grader-inputs/oracle/expected.json) are byte-identical to retry1, including all expected answers, protected claims and assertions. Their archived mtimes are 13:06:42 UTC, before the editor's first recorded tool call at 13:07:07 UTC, consistent with the predeclared snapshots described in [run-notes.md](run-notes.md).

The filesystem is shared: enforcement consists of explicit allowlists plus inspection of every recorded call/output pair, not OS isolation. Standard harness/repository context remains available. No out-of-manifest subject-matter access, oracle leakage, other-version read, network access or reader mutation was observed. Shell startup reported an unsuccessful unrelated `navi.log` creation without source disclosure.

**Trace and artifact audit.**

| Evidence | Finding |
| --- | --- |
| [Editor trace](editor-trace.jsonl) | All 5 calls have matching outputs: both complete instructions at ordinals 14→18; guide, requirements and prep.py at 20→25; guide-only patch at 31; yielded-patch completion at 38; final guide read at 42. Full source inspection precedes editing. |
| [Original reader trace](reader-original-trace.jsonl) | One complete call/output pair at ordinal 10, reading only its original guide. |
| [Revised reader trace](reader-revised-trace.jsonl) | One complete call/output pair at ordinal 14, reading only its revised guide after editing finished. |
| [Manifest](manifest.json), [hashes](hashes.txt), original/revised files | All hashes independently verify. Original guide and requirements match retry1; instructions are byte-identical with matching hashes. During this attempt only guide.md changes; prep.py and requirements.md remain byte-identical and no artifact is added. |
| Raw read contents | Every instruction, source and artifact output contains the complete exact archived file content. No relevant output is truncated. |

**Independent source check.** Inspection of [original/prep.py](original/prep.py) shows that `default_change_example()` creates an inherited order at 15, assigns 20 to the restaurant default, and returns a fresh lookup alongside the previously stored order value. The lookup and creation functions are unchanged from retry1. I independently ran `python3 -B original/prep.py` against this archived file: exit 0, output `{'new_lookup': 20, 'old_order': 15}`. This corroborates the concrete fixture behavior without relying on the primary session's execution claim. The editor's trace shows source inspection, not test execution; this check does not imply production verification.

**Five-question comparison.** Original: **2 PASS, 2 PARTIAL, 1 FAIL**. Revised: **5 PASS**. Evidence: [original response](reader-original-response.md), [revised response](reader-revised-response.md), fixed [oracle](grader-inputs/oracle/expected.json).

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both identify restaurant defaults with item exceptions. |
| 2 — Default change and existing orders | FAIL | PASS | Original Q2 wrongly presents next-day activation as current. Revised Q2 explicitly distinguishes required delayed activation from immediate 20 and confirms the existing snapshot retains 15. |
| 3 — Current increment | PARTIAL | PASS | Original Q3 omits the timing mismatch. Revised Q3 identifies lookup and order snapshots, with the mismatch explicitly supplied in Q2. |
| 4 — Exclusions | PASS | PASS | Both identify scheduling. Revised Q4 also preserves the unresolved relationship between that exclusion and next-day activation. |
| 5 — Decisions | PARTIAL | PASS | Original Q5 includes only badges. Revised Q5 includes the feature maintainer's reconciliation and Product's badge decision. |

**Assertion grading.** Fidelity, preservation and factual correctness were checked against the artifacts and source independently of answer accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 2.1 | PASS | reader-revised-response.md Q2 gives required next-day intent, actual immediate 20 and the existing order's retained 15. The remaining four answers match the fixed oracle. revised/guide.md paragraphs 2–3 explicitly support the full case without another reader source. |
| 2.2 | PASS | revised/guide.md retains the mandatory next-day requirement and the mandatory unchanged-snapshot requirement, describes immediate lookup as current, and says the accepted requirement remains unmet. Missing/null inheritance and explicit zero survive. No authority is silently selected and no requirement is erased. |
| 2.3 | PASS | editor-trace.jsonl ordinals 20→25 contain the complete requirements and implementation, including default_change_example, after complete instruction loading and before the ordinal 31 patch. |
| 2.4 | PASS | The guide names the feature maintainer, records the unresolved timing disagreement, and specifies reconciliation with the accepted delay and clarification of scheduling scope as the next step. Neither guide nor editor-response.md claims that requirements or code were fixed. Product's unresolved badge decision remains explicit. |
| 2.5 | PASS | The sole mutation updates guide.md. Independent byte comparisons, verified hashes and matching original/revised inventories confirm unchanged requirements.md and prep.py and no added summary, ledger or source file. |

The original heading is retained; there are no existing cross-file links or task states to lose. Snapshot behavior is now supported by the explicit fixture operation rather than inferred from an asserted requirement. No unsupported behavior, approval or product decision is added.

This pass applies to the strengthened source-evidence fixture. It does not convert the earlier attempts to passes, demonstrate that the unchanged skill succeeds with their smaller evidence sets, or establish improved comprehension for all human readers.
