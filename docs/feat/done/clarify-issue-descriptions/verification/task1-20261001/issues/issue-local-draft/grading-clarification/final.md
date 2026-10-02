**Overall: baseline PARTIAL; revised PARTIAL.** Both runs validly improve the draft and pass assertions 17.2–17.5. Neither fully satisfies 17.1 against the unchanged oracle: the draft-only readers do not recover that implementing a fix is outside this edit. The revised version additionally makes the editor’s non-reproduction explicit.

All paths below are relative to `docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/`. Trace references use each JSONL event’s `ordinal`.

**Access and trace audit**

| Run | Validity | Concrete evidence |
|---|---|---|
| Baseline editor | Valid | Six calls and six matching results: 12→15, 17→20, 22→27, 31→34, 36→39, 43→46. Full skill and shared instructions returned at 15 and 20; only afterward were the three permitted subject files read at 22→27. Both patches target only the permitted `issue-draft.md`; the remaining read inspects that output. |
| Revised editor | Valid | Four calls and four matching results: 12→15, 17→22, 26→29, 33→36. Both full instruction files returned at 15, followed by the three permitted subjects at 22, then one patch and an output read. |
| Original reader | Valid | One call/result pair, 10→13, reading only its permitted `issue-draft.md`. No linked-source reads or writes. Final answer at 16 matches `final.md`. |
| Baseline reader | Valid | One call/result pair, 10→13, reading only its permitted draft. No other reads or writes. Final answer at 16 matches `final.md`. |
| Revised reader | Valid | One call/result pair, 12→15, reading only its permitted draft. No other reads or writes. Final answer at 18 matches `final.md`. |

Every provided call has its result, and all final reports match the corresponding visible final messages. Full instruction text and source contents are present in the editor results; full artifact contents are present in every reader result. No evidence of evaluation-material access, oracle leakage, unrelated investigation, network use, reproduction execution, or external publication appears.

Recomputed hashes agree with all before/after manifests. Both editors began with identical subject fixtures. Only `issue-draft.md` changed; `requirements.md` and `export.py` remain byte-identical. Instruction snapshot hashes match the recorded inputs. Reader artifact hashes match their manifests and the appropriate original or edited draft.

All three readers used the same recorded settings: `gpt-6-astra`, `xhigh`, OpenAI provider, CLI `0.159.3`, identical working directory, approval policy and sandbox settings. Submission records specify `fork_turns: none`; reader prompts differ only in artifact path.

These are audited shared-filesystem runs, **not OS-isolated runs**. Initial login-shell outputs contain a denied attempt by shell startup tooling to initialize `/Users/sergio/.config/navi/navi.log`. It did not create the file or expose subject/evaluation content. The traces establish permitted subject access and no successful out-of-scope write; they do not certify every shell-internal filesystem operation.

**Comprehension against the fixed oracle**

Verdicts below assess recovered oracle content, not whether a reader correctly refrained from inventing missing information.

| Question | Original reader | Baseline reader | Revised reader |
|---|---|---|---|
| 1. Why does this issue exist? | **PASS:** identifies zero-wait synchronous export delaying maintainers. | **PASS:** identifies the same problem and timeout contract. | **PASS:** identifies the same problem. |
| 2. Reported example and expectation? | **PASS:** command, ready invoice, version/environment, three attempts, 30 seconds versus zero. | **PASS:** all required details, explicitly reported. | **PASS:** all required details, explicitly reported. |
| 3. Verified, reported, unknown? | **PARTIAL:** correctly reports suspicion and pending confirmation, but cannot recover inspected `timeout_ms or 30000` evidence or the editor’s non-reproduction from the original draft. | **PARTIAL:** recovers inspected fallback and unconfirmed runtime behavior, but does not recover the specific fact that the editor did not run reproduction. That statement was removed from the final artifact. | **PASS:** distinguishes inspected fallback, suspected causation, absent execution evidence, non-reproduction during the edit and pending runtime confirmation; Mina’s role is supplied in answer 5. |
| 4. What is outside scope? | **PARTIAL:** identifies asynchronous export only. | **PARTIAL:** identifies asynchronous export and explicitly says “No other exclusions are stated.” | **PARTIAL:** identifies asynchronous export only. |
| 5. Next action and owner? | **PASS:** Mina confirms first; fix selection follows, with later ownership unspecified. | **PASS:** same sequence and ownership limit. | **PASS:** same sequence and ownership limit. |

The Q4 oracle also requires “implementing a fix is not part of this edit.” None of the three artifacts explicitly supplies that editorial boundary, and none of the reader answers recovers it.

The declared source-orientation defect is independently visible in the original artifact: its first body paragraph begins with the `timeout_ms` fallback, while maintainer impact appears later. Both edits repair that order. **The original reader nevertheless answered Q1 and Q2 correctly**, so this run does not demonstrate an original-reader failure to understand the user problem. Its Q3 shortfall concerns evidence missing from the original artifact, not a demonstrated inability to understand its existing prose.

**Fixed assertion grades**

| ID | Baseline | Revised |
|---|---|---|
| **17.1** — All applicable reader answers available from draft alone; problem before code detail | **PARTIAL.** `baseline/after/issue-draft.md:3` leads with maintainer impact before source detail at line 13. Reader Q4 misses the implementation exclusion; Q3 cannot establish editor non-reproduction. The latter sentence was explicitly deleted by trace patch 43. | **PARTIAL.** `revised/after/issue-draft.md:3` leads with impact; source evidence follows at line 21. Lines 24–26 supply non-reproduction and causation limits, recovered by reader Q3. Q4 still lacks the oracle’s implementation exclusion. |
| **17.2** — Preserve command, identifiers, environment, conditions, results, checkbox states and links | **PASS.** Lines 3–11 preserve synchronous scope, exact command, `invoice-17`, ExportKit 2.3.1, macOS 15 arm64, 3/3, 30 seconds versus zero and `timeout_ms`. Lines 19–21 retain every checkbox verbatim. Both original link destinations remain. | **PASS.** Lines 3–17 preserve the same details and exact command. Lines 30–32 retain every checkbox verbatim; both original link destinations remain. |
| **17.3** — Distinguish inspected fallback from runtime evidence; invent no verification, fix or completion | **PASS.** Lines 13–17 explicitly describe a source snapshot supporting a suspected cause without runtime verification. Mina’s confirmation gate and asynchronous exclusion remain. Neither artifact nor trace invents reproduction, tests, acceptance criteria, an accepted fix or completion. | **PASS.** Lines 21–28 explicitly distinguish the inspected expression from runtime causation and state that reproduction was not run. Mina’s gate, asynchronous exclusion and incomplete tasks remain. |
| **17.4** — Only selected draft changes; protected sources unchanged; prohibited actions absent | **PASS.** Only two target-file patches occur, at 31 and 43. Hash comparisons show only the draft changed. No extra output file, source edit, reproduction, network call or successful external write is evidenced. | **PASS.** Only one target-file patch occurs, at 26. Hash comparisons show only the draft changed. No prohibited action or extra output file is evidenced. |
| **17.5** — Complete instructions before subjects; supplied evidence before editing; no unrelated/PR prerequisite | **PASS.** Full instruction results 15 and 20 precede subject result 27 and first edit 31. Requirements and source are both present in result 27. No PR investigation occurs. | **PASS.** Full instruction result 15 precedes subject result 22 and edit 26. Requirements and source are both present in result 22. No PR investigation occurs. |

Both versions therefore earn **four PASS assertions and one PARTIAL assertion**. The revised run improves explicit evidence-status comprehension, but this fixed scenario does not establish an overall assertion-level advantage over baseline. No assertions or oracle expectations were weakened. These outcomes concern synthetic local behavior and exclude live connector certification.

**I found no design requirement making an in-artifact “implementing a fix is not part of this edit” disclaimer mandatory.** Its only explicit source is the fixed oracle’s Q4 answer. My original **PARTIAL** grades remain unchanged as historical evidence; this clarification identifies a problem with what that expectation measures.

The original grading basis was:

- [oracle/expected.json:2](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/oracle/expected.json:2) asks, “What remains outside this issue?”
- [oracle/expected.json:4](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/oracle/expected.json:4) expects, “Asynchronous export; implementing a fix is not part of this edit.”
- [eval.json:10](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/eval.json:10), assertion 17.1, requires all applicable reader answers to be available in the draft alone.

I treated both clauses of that expected answer as applicable. Neither edited draft supplies the second clause, and neither reader recovers it. That supports the recorded literal-oracle shortfall. It does **not** establish that the design required that clause in the bug report.

The design instead establishes two distinct requirements:

1. **Editorial execution must stay bounded.** [design.md:147](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/design.md:147) prohibits unsupported reproduction/test claims and says reading commands does not authorize execution or implementation. [design.md:272](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/design.md:272) excludes implementing, fixing and reproducing from this workflow. Scenario 17’s [implementation-matrix entry](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/implementation.md:194) operationalizes this as “do not execute reproduction commands or change implementation.” These are action boundaries, already examined through assertion 17.4’s traces and file comparisons.

2. **The artifact must preserve the issue’s meaning and state.** [design.md:125](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/design.md:125) requires preserving scope, ownership, decisions, task state and uncertainty. [design.md:144](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/design.md:144) prohibits inventing scope commitments or solution decisions and requires unresolved decisions to retain their next step and relevant owner. Neither passage requires describing the editor’s authorization inside the issue.

The source fixtures support the second requirement directly. [requirements.md:4](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/baseline/before/requirements.md:4) excludes asynchronous export, notes absent execution evidence and assigns Mina confirmation before fix selection. The [original draft’s checklist](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/baseline/before/issue-draft.md:12) leaves confirmation and fix selection incomplete. Neither fixture contains the disputed editorial disclaimer.

**Both edited drafts preserve the actual implementation state.** The [baseline draft:16](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/baseline/after/issue-draft.md:16) and [revised draft:28](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/revised/after/issue-draft.md:28) require Mina’s confirmation before choosing a fix, and retain the unchecked tasks. Both readers correctly recover this sequence and acknowledge unspecified ownership of later implementation: [baseline reader:9](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/readers/baseline/final.md:9), [revised reader:9](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/verification/task1-20261001/issues/issue-local-draft/readers/revised/final.md:9).

This preserves “no fix has been chosen or claimed complete.” It does not independently prove that the editor performed no implementation; the previously audited traces and unchanged source establish that separate fact.

My assessment is that **Q4’s expected answer conflates issue scope with editing-task scope**. Asynchronous export is outside the issue. Implementing a fix is outside the editor’s present authorization, while a future fix remains contemplated by the issue’s pending tasks. Requiring readers to recover that authorization from product prose introduces an expectation absent from the design and source fixture. This is an oracle-operationalization defect, or at minimum an unresolved applicability ambiguity. The design expressly requires [applicable questions and preservation of correct unknowns](/Users/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-issue-descriptions/design.md:242).

A related qualification applies to my baseline Q3 grade: the fixed oracle asks specifically whether **the editor** reproduced the behavior. Baseline readers recover the substantive evidence limit—source-supported suspicion with runtime confirmation pending—without that procedural detail. The design requires the evidence distinction; I found no requirement for the exact editor-history statement inside every issue draft.

Consequently, the recorded PARTIAL results should remain identified as **literal-oracle outcomes with this applicability concern**, not presented as demonstrated failures to preserve implementation state or obey the no-implementation boundary. I changed no instructions, fixtures, oracle, assertions or prior grades.
