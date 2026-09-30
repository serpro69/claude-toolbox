# Source-disagreement retry 1: independent verdicts

Date: 2026-09-29. **Assertion outcome: PARTIAL — 4 PASS, 1 PARTIAL. Acceptance is not established.** The previous attempt's verdict is preserved.

**Run validity: PASS under the declared allowlist-and-trace protocol, with attested prompt and declaration provenance.** The [reader prompts](reader-original-prompt.json) ([revised](reader-revised-prompt.json)) are identical apart from the artifact path. Both ask the same concrete 15-to-20 question, require source pointers and explicit uncertainty, and exclude other files, skills, network, writes and agents. All three prompts record `fork_turns: none`; the three session records identify distinct general-purpose `gpt-6-astra`/`xhigh` sessions. Build and temperature are not exposed.

The plaintext prompts are orchestrator-attested copies of live spawn inputs. The orchestrator also attests that question 2 changed before the editor started. The archived `grader-inputs/` copies were exported afterward: their mtimes are 12:55:17 UTC, after the editor's 12:55:08 patch. These copies therefore do not independently timestamp the prior declaration. Comparing them with the first attempt's snapshots confirms that only question 2 changed; all assertions, expected answers, protected claims and other questions are unchanged. See [run notes](run-notes.md).

Shared filesystem access was constrained by explicit manifests and audited calls, not OS isolation. Standard harness/repository context remained available. No out-of-manifest subject-matter access, oracle leakage, other-version access, external lookup or reader mutation was observed. Shell startup reported failed unrelated `navi.log` creation, without source disclosure.

**Trace and integrity audit.**

| Evidence | Result |
| --- | --- |
| [Editor trace](editor-trace.jsonl) | All 5 calls have matching outputs: complete SKILL read at ordinal 14, complete shared instructions at 19, guide/requirements/source at 24, guide-only patch at 33, final guide read at 38. Source reads finish before editing. |
| [Original reader trace](reader-original-trace.jsonl) | One complete call/output pair, reading only the original guide at ordinal 14. |
| [Revised reader trace](reader-revised-trace.jsonl) | One complete call/output pair, reading only the revised guide at ordinal 10. |
| [Manifest](manifest.json), [hashes](hashes.txt), original/revised artifacts | Every recorded hash verifies. Originals match both the first attempt and original fixtures. Both instruction hashes match the first attempt. Only guide.md differs; prep.py and requirements.md remain byte-identical, with no added artifact. |
| Raw read outputs | Every instruction, source and original/revised artifact read contains the full exact corresponding archived content. No relevant output is truncated. |

**Five-question comparison.** Original: **2 PASS, 2 PARTIAL, 1 FAIL**. Revised: **4 PASS, 1 PARTIAL**. Evidence is in the [original response](reader-original-response.md), [revised response](reader-revised-response.md) and fixed [oracle](grader-inputs/oracle/expected.json).

| Question | Original | Revised | Observed evidence |
| --- | --- | --- | --- |
| 1 — Purpose | PASS | PASS | Both identify restaurant defaults with item exceptions. |
| 2 — Default change and existing orders | FAIL | PARTIAL | Original Q2 presents next-day activation as current. Revised Q2 correctly gives required delay versus immediate 20, but describes unchanged existing snapshots only as a requirement and says actual handling elsewhere is unknown. It does not establish the oracle's earlier order retaining 15. |
| 3 — Current increment | PARTIAL | PASS | Original Q3 omits the mismatch. Revised Q3 identifies lookup/snapshots, with the timing mismatch explicitly supplied in revised Q2. |
| 4 — Exclusions | PASS | PASS | Both identify scheduling. |
| 5 — Decisions | PARTIAL | PASS | Original Q5 mentions only badges. Revised Q5 identifies Product's badge decision and the feature maintainer's timing/scope reconciliation. |

**Assertion grading.** Fidelity and preservation were checked directly against requirements, source and before/after artifacts, independently of answer accuracy.

| ID | Verdict | Concrete evidence |
| --- | --- | --- |
| 2.1 | PARTIAL | Revised Q2 resolves the earlier omission about the default changing to 20, but stops short of confirming the previous order stays at 15. The same gap exists in revised/guide.md's snapshot paragraph and editor-response.md: existing-order behavior is qualified as unverified. The mandatory unchanged-snapshot requirement is retained, but a requirement alone does not demonstrate the expected current-behavior answer. |
| 2.2 | PASS | revised/guide.md's paired bullets preserve the mandatory next-day requirement and describe immediate lookup from the inspected implementation. The discrepancy remains explicit; the editor neither silently selects an authority nor declares a requirement change. Missing/null inheritance, explicit zero and the mandatory unchanged-snapshot requirement are also preserved. |
| 2.3 | PASS | editor-trace.jsonl loads both complete instructions before ordinal 24 reads guide.md, requirements.md and prep.py. Those outputs precede the ordinal 33 patch. |
| 2.4 | PASS | The final guide names the feature maintainer and a concrete next step: determine how to meet next-day activation with scheduling excluded, or obtain an explicit requirement/scope change. It says the discrepancy is unresolved and does not claim implementation or requirements were fixed. Product's badge decision stays open. |
| 2.5 | PASS | The only mutation call patches guide.md. Direct byte comparisons and verified hashes show unchanged prep.py and requirements.md; original/revised file inventories are identical. No ledger, summary or extra source file is introduced. |

The added caveat about unspecified handling elsewhere does not invent an implementation, but it also does not supply the scoped behavioral conclusion this oracle requires: changing the restaurant default leaves a previously copied 15 unchanged. The grader does not infer that missing reader answer from its own knowledge of the source. The original heading remains; there are no task states or existing links to lose. No unsupported requirement decision is made.

This is a separate partial attempt under a refined question. It neither replaces the first result nor proves improved comprehension for all human readers.
