# Independent grading: PR editorial evaluations 11–15

All five runs are **VALID within the recorded shared-filesystem protocol**. The assertion results are **24 PASS, 1 PARTIAL, 0 FAIL**. Cases 11, 13, 14 and 15 pass; case 12 is partial because its revised reader does not identify the newly added tests as part of the current increment. PARTIAL is not a pass.

These are observations of AI reader behavior in single runs. They do not establish improved human comprehension, statistical reliability, or runtime correctness. Document length was not scored.

## Method and evidence integrity

I read the grading request and complete frozen [entry instructions](../instructions/SKILL.md) and [shared procedure](../instructions/document-clarity.md) before assessing the artifacts. I independently inspected the five assertion sets, four oracles, frozen sources, artifacts, reader answers, exact requests/spawn texts, editor/reader metadata, and every retained tool call/result and visible assistant message. This includes shell commands, patches, and parallel calls nested inside `functions.exec`. The coordinator audits were checked against that evidence, not adopted as verdicts.

Recomputed SHA-256 values match every case's `input-hashes.json`, `output-hashes.json`, manifest input/output/request/artifact hashes, and `changes.json`. The two operative instruction files match their recorded hashes, including the shared-file alias. Original and revised reader artifacts are exact copies of their corresponding before/after selected artifacts. Scenario source captures match the before snapshots; checkout contents match the supplied head fixtures. For cases 11–13, independently computed Git blob IDs for every base/head fixture match the captured trees in `git-evidence.txt`. The actual refs/diffs agree with the editor trace results.

All 46 retained outer tool calls have matching results: 30 editor calls and 16 reader calls. Raw trace record ordinals agree with the readable traces, and final messages agree with the separate output files. No missing call result, truncated instruction/source result, additional source-only reader evidence, oracle exposure, network call, or external mutation appears. The full frozen instructions appear verbatim in each editor's instruction result, before its first subject read.

| Case | Instructions fully returned | First subject read | Editor calls | Reader request/artifact calls | Changed paths |
| --- | --- | --- | --- | --- | --- |
| 11 | ordinal 22 | 24 | 8 | original 10/19; revised 10/19 | `pr-draft.md` |
| 12 | ordinal 22 | 24 | 8 | original 10/19; revised 10/17 | `docs/feat/wip/prep/pr-12-draft.md` |
| 13 | ordinal 23 | 25 | 6 | original 10/17; revised 10/17 | `pr-draft.md` |
| 14 | ordinal 23 | 25 | 3 | not applicable | none |
| 15 | ordinal 23 | 25 | 5 | original 10/17; revised 10/19 | `drafts/pr-15.md` |

Ordinals refer to each case's `editor-trace.jsonl`, `original-trace.jsonl`, or `revised-trace.jsonl`. Editor instruction calls are ordinal 19 in every case. Each reader has exactly two read calls: its request and its artifact. Every inspected content read stays within that role's manifest.

All paired readers have distinct recorded thread IDs and matching `gpt-6-astra`, `xhigh`, `summary: none` settings. Editors have the same recorded settings. Temperature and model build are unrecorded. Fresh sessions retain standard system/AGENTS harness context; no inherited conversation was forked. This is prompt-manifest isolation on a shared filesystem, not OS isolation. Initial default-login shell startup emits an ambient logging error; it returns no additional subject-matter content. Live staging/session stores were outside the grading manifest and were not inspected. Consequently this audit checks the completeness and consistency of the retained exports, not an independently retrieved full session history. Unrelated entries in the broad instruction-hash inventory were not resolved or read.

For question scores below, one point requires a fully correct oracle-backed answer. PARTIAL receives no point. Appropriate uncertainty earns a pass when the oracle requires it; acknowledging that a baseline omits a known oracle fact does not recover that fact. Equivalent wording is accepted, but an omitted increment or decision qualifier is not supplied by the grader.

## Case 11 — contract-only-pr

**Validity: VALID. Overall: PASS, 5/5 assertions. Comprehension: ORIGINAL 1/5 → REVISED 5/5. Fidelity: PASS. Isolation and trace completeness: PASS.**

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 11.1 | PASS | [Revised answers](../contract-only-pr/revised-output.md), Q1–Q5, recover purpose, contract example, schema-only change, future work and product-owner badge decision from the draft alone; see question table below. |
| 11.2 | PASS | [Revised artifact](../contract-only-pr/revised-artifact.md), paragraphs 1–3: null or integer 0–90, null inheritance, explicit zero, unchanged runtime stub, future runtime/persistence/scheduling/UI, open badge decision, and JSON-only validation all survive. |
| 11.3 | PASS | [Editor trace](../contract-only-pr/editor-trace.md), ordinals 24/28 and 30/34, resolves actual tagged commits, reads their contract diff, and reads requirements/contract/stub at both revisions before patching. [Git evidence](../contract-only-pr/git-evidence.txt) confirms `95c9bd2…` → `029cd45…`; the runtime-complete label does not determine scope. |
| 11.4 | PASS | [Revised artifact](../contract-only-pr/revised-artifact.md), opening: restaurant purpose precedes schema detail; 15/null and zero cases are expressly specified results. Final paragraph directs review to `contract.json` against requirements and identifies unchanged `resolve.py` as the integration boundary. |
| 11.5 | PASS | [Changes](../contract-only-pr/changes.json) and recomputed snapshot hashes show only `pr-draft.md` changed. Trace instruction result 22 precedes source call 24. Patch 47 fails without writing; corrected patch 53 succeeds; final reread 58 confirms output. No external mutation appears. |

| Question | Original | Revised | Concrete comparison |
| --- | --- | --- | --- |
| Q1: purpose | FAIL | PASS | Original Q1 cannot identify the user need. Revised Q1 recovers avoiding repeated preparation values and the item-override contract. |
| Q2: example | PARTIAL | PASS | Original Q2 gets null propagation but cannot explain zero or a concrete default, and does not establish the unimplemented runtime. Revised Q2 gives 15/null→15 and zero→0 as specified, unimplemented behavior. |
| Q3: increment | FAIL | PASS | Original Q3 repeats the claim that the schema enables order defaults. Revised Q3 says only `contract.json` changes; revised Q2/Q4 also make the runtime boundary explicit. |
| Q4: outside scope | PARTIAL | PASS | Original Q4 names persistence/scheduling/UI but omits runtime integration. Revised Q4 includes all four and the runtime/deployment validation limits. |
| Q5: decision | PASS | PASS | Both identify the product owner's inheritance-badge decision; revised Q5 states whether inherited values display a badge. |

Question evidence: [original answers](../contract-only-pr/original-output.md), [revised answers](../contract-only-pr/revised-output.md), and [oracle](../contract-only-pr/scenario/oracle/expected.json).

The editor corrects a conclusive factual error without deleting accepted requirements. The review increment is contract-only, and the requirements/stub make future runtime integration explicit. References are unrestricted target-repository evidence. No missing source owner was invented; the known product owner retains the remaining decision.

Limitations: successful JSON parsing is a supplied validation record, not a parser execution by this editor. No runtime tests or deployment occurred in this run. One original/revised AI-reader pair supports only this observed comparison; the shared protocol limitations above also apply.

## Case 12 — runtime-pr

**Validity: VALID. Overall: PARTIAL, 5 PASS and 1 PARTIAL assertion. Comprehension: ORIGINAL 0/5 → REVISED 4/5. Protected-claim fidelity: PASS. Increment explanation completeness: PARTIAL. Isolation and trace completeness: PASS.**

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 12.1 | PARTIAL | [Revised answer Q3](../runtime-pr/revised-output.md) correctly identifies the new resolver and inherited schema but omits the newly added tests from the increment. The [oracle](../runtime-pr/scenario/oracle/expected.json) requires both runtime resolver and tests. Q4 mentions recorded tests, which does not establish that they are new in this diff. Four questions fully pass. |
| 12.2 | PASS | [Revised artifact](../runtime-pr/revised-artifact.md): new runtime selection versus contract already at base is explicit; null/zero semantics, three exercised cases, persistence/scheduling/UI exclusions, product-owner badge decision, and lack of persistence/deployment validation remain. It also accurately distinguishes selection from range enforcement. |
| 12.3 | PASS | [Editor trace](../runtime-pr/editor-trace.md), ordinals 29/34, 36/44 and 50/54, reads actual IDs, whole diff, requirements, both resolver revisions, head tests and inherited base contract before patch 56. [Git diff](../runtime-pr/git-diff.txt) establishes resolver replacement plus a newly added test file despite the schema-only title. |
| 12.4 | PASS | [Changes](../runtime-pr/changes.json) and before/after hashes show one new `docs/feat/wip/prep/pr-12-draft.md`; `remote-body.md`, colliding unrelated `pr-draft.md` and sources are byte-identical. Trace 50 checks output absence before writing. No network or remote write appears. |
| 12.5 | PASS | [Revised artifact](../runtime-pr/revised-artifact.md), opening and “Current increment and review path”: restaurant purpose and 15/null, zero, and seven examples precede the `resolve.py` → `test_resolve.py` review path; `contract.json` is explicitly inherited. This passes the orientation assertion without supplying the missing “tests are new” assertion to the reader. |
| 12.6 | PASS | [Editor trace](../runtime-pr/editor-trace.md), instruction result 22 precedes source call 24. Only the selected local draft is authored; [changes](../runtime-pr/changes.json) show no source, ledger, or extra summary edits. |

| Question | Original | Revised | Concrete comparison |
| --- | --- | --- | --- |
| Q1: purpose | FAIL | PASS | Original Q1 cannot identify the benefit. Revised Q1 gives shared restaurant defaults without repeated item values. |
| Q2: example | FAIL | PASS | Original Q2 cannot define sentinel/default routing. Revised Q2 gives all three runtime results: 15, 0 and 7. |
| Q3: increment | FAIL | PARTIAL | Original Q3 presents the inherited contract as added. Revised Q3 corrects resolver/schema scope but never identifies the added tests as a new part of this increment. |
| Q4: outside scope | PARTIAL | PASS | Original Q4 recovers persistence/scheduling/UI but omits the oracle's absence of deployment proof. Revised Q4 includes those exclusions, range limits, and unrecorded deployment validation. |
| Q5: decision | PARTIAL | PASS | Original Q5 says the product owner must “choose badges,” without recovering that the decision concerns displaying badges on inherited values. Revised Q5 states that decision expressly. |

Question evidence: [original answers](../runtime-pr/original-output.md), [revised answers](../runtime-pr/revised-output.md), and [oracle](../runtime-pr/scenario/oracle/expected.json). The original score counts only fully recovered oracle answers; its two partial answers are not passes.

The reader omission is supported by a narrow ambiguity in the artifact: its review path names `test_resolve.py`, and its validation section explains the three assertions, but it never expressly says that this PR **adds** those tests. Review-path presence alone cannot establish new-versus-inherited scope. This is incomplete increment communication, not loss of the test cases or validation limits protected by assertion 12.2, and not a wrong runtime claim. A sentence explicitly identifying the newly added tests would address the ambiguity; no input was changed during grading.

Other fidelity checks pass: requirements still constrain allowed minutes while the implementation selects values without enforcing that range; the artifact preserves that distinction. It retains the open product-owner decision, uses accessible repository references, respects the collision and local output scope, and attributes passing assertions to the supplied validation record.

Limitations: the editor inspected test source but did not execute those assertions. The fixture's reported passing result is not newly demonstrated runtime or deployment proof. This is one AI-reader pair, and the shared protocol limitations above apply.

## Case 13 — destination-visibility

**Validity: VALID. Overall: PASS, 7/7 assertions. Comprehension: ORIGINAL 5/5 → REVISED 5/5. Revised fidelity and visibility: PASS; original visibility: FAIL by the predeclared defect. Isolation and trace completeness: PASS.**

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 13.1 | PASS | [Original answers](../destination-visibility/original-output.md) and [revised answers](../destination-visibility/revised-output.md), Q1–Q5, both match the oracle. The original's restricted business paragraph still requires repair, as independently established by the access declarations. |
| 13.2 | PASS | [Revised artifact](../destination-visibility/revised-artifact.md) removes the private aggregator paragraph and contains no absolute workspace path, private source pointer, task identifier, or underlying restricted fact. [All visible editor messages](../destination-visibility/editor-messages.md) contain none of those facts/pointers. The sole absolute path is the caller-authorized selected-output link. |
| 13.3 | PASS | [Context](../destination-visibility/before/context.md) explicitly restricts a tracked planning file; trace 31/34 confirms head membership. Neither its filename nor its restricted launch fact appears in the revised artifact or visible editor messages. Tracking does not override the restriction. |
| 13.4 | PASS | [Revised artifact](../destination-visibility/revised-artifact.md) excludes both credential-only and unknown-access external references and their facts. It substitutes only a non-disclosing limitation, not a public replacement or business decision. |
| 13.5 | PASS | Revised artifact lines 9–10 retain Task 7, `docs/tasks.md`, the public format URL and explicitly shared team URL. Trace 25/29 reads the access declarations and mirrors; 31/34 confirms tracked tasks and their content. |
| 13.6 | PASS | Revised artifact lines 3–7 preserve contract range/semantics, future runtime and other exclusions, product-owner decision, and JSON-only validation. [Editor trace](../destination-visibility/editor-trace.md), 25/29 and 31/34, checks declarations and head membership. [Changes](../destination-visibility/changes.json) plus recomputed hashes show only `pr-draft.md` changes. |
| 13.7 | PASS | [Final completion](../destination-visibility/editor-output.md) links the selected local `pr-draft.md` by its absolute path as explicitly requested. It contains no other workspace path or restricted fact. The destination artifact contains no absolute path. |

| Question | Original | Revised | Concrete comparison |
| --- | --- | --- | --- |
| Q1: purpose | PASS | PASS | Both recover restaurant default plus item exceptions. Revised Q1 correctly limits its additional business-context knowledge. |
| Q2: example | PASS | PASS | Both give 15/null→15 and zero→0 as contract semantics, with runtime future. |
| Q3: increment | PASS | PASS | Both identify contract/schema scope and 0–90, with JSON-only validation. |
| Q4: outside scope | PASS | PASS | Both name resolver/runtime, persistence, scheduling and UI. |
| Q5: decision | PASS | PASS | Both identify the product owner's inheritance-badge decision. |

Question evidence: the two answer files linked above and the [oracle](../destination-visibility/scenario/oracle/expected.json).

This run demonstrates a disclosure repair with unchanged measured comprehension. Deleting citations alone would not suffice: the edit removes the facts as well. Every oracle-listed forbidden value is absent from the revised destination and visible editorial commentary/final messages. The source-reading results and the deletion hunk retain original restricted content as audit evidence; they are not additional editorial narration or a retained destination disclosure. The caller-only output link is explicitly allowed and cannot authorize links to private sources. Legitimate tracked/public/shared references remain intact, and the open badge decision remains open.

Limitations: audience access is established by synthetic offline declarations and mirrors, not live URL access. Unlike case 11, this editor actually parses head `contract.json` at trace 43/47; the result explicitly says runtime was not tested. No runtime or deployment proof follows. The original artifact intentionally contains restricted material, so its presence in the original reader's allowed artifact does not constitute oracle or source-only contamination. Shared protocol limitations apply.

## Case 14 — pr-missing-context

**Validity: VALID. Overall: PASS, 3/3 assertions. Comprehension comparison: NOT APPLICABLE. Fidelity and scope restraint: PASS. Isolation and trace completeness: PASS.**

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 14.1 | PASS | [Editor trace](../pr-missing-context/editor-trace.md): full instruction result 23 precedes context/body reads 25/29, which precede the final question at 34. The available evidence is inspected before clarification. |
| 14.2 | PASS | [Final question](../pr-missing-context/editor-output.md) asks where to save the draft. [Changes](../pr-missing-context/changes.json) are empty; both frozen before/after hashes match. No write tool call or output draft/summary/external write appears. |
| 14.3 | PASS | Final question requests target repository, actual base/head revisions, review diff and test results. It explicitly says the context cannot substantiate runtime completion or passing tests and leaves the immutable capture unchanged. |

The editor treats absent destination and source context as consequential gaps, rather than treating the pasted capture as a selected editable draft. No runtime, increment, or validation claim is invented. The requested next action is concrete; the supplied context identifies the author as able to provide the evidence. The capture remains intact.

Limitations: no revised artifact or reader pair exists by design, so this is evidence of correct clarification/scope handling, not a comprehension improvement. No repository, revisions, diff, source, or tests were available or verified. Shared protocol limitations apply.

## Case 15 — pr-unavailable-source

**Validity: VALID. Overall: PASS, 4/4 assertions. Comprehension: ORIGINAL 4/5 → REVISED 5/5. Fidelity: PASS. Isolation and trace completeness: PASS.**

| Assertion | Verdict | Evidence |
| --- | --- | --- |
| 15.1 | PASS | [Changes](../pr-unavailable-source/changes.json) and recomputed hashes show only `drafts/pr-15.md` created; `remote-body.md` and context remain byte-identical. [Trace](../pr-unavailable-source/editor-trace.md) checks destination absence at 25, creates the file at 34, and rereads at 39. No network/external mutation appears. |
| 15.2 | PASS | [Revised artifact](../pr-unavailable-source/revised-artifact.md), paragraphs 2–3, explicitly lacks commit IDs/diff/source/test results, rejects branch names as increment evidence, and keeps runtime/passing-tests claims unverified. It requires the PR author to provide exact revisions, diff and test output for review. |
| 15.3 | PASS | [Revised answers](../pr-unavailable-source/revised-output.md), Q1–Q5, recover confirmed purpose/example, unknown actual increment and concrete owner/evidence action, exclusions and open badge decision. These match the [oracle](../pr-unavailable-source/scenario/oracle/expected.json). |
| 15.4 | PASS | Revised artifact retains product-owner-confirmed purpose and contract example, explicit-zero semantics, persistence/scheduling exclusion and open product-owner badge decision. Full frozen instructions return at trace 23 before evidence reads at 25. |

| Question | Original | Revised | Concrete comparison |
| --- | --- | --- | --- |
| Q1: purpose | PASS | PASS | Both recover avoiding repeated preparation times through restaurant defaults. |
| Q2: example | PASS | PASS | Both give 15/null→15 and zero→0 as intended/confirmed contract and acknowledge runtime uncertainty. |
| Q3: increment/evidence/owner | PARTIAL | PASS | Original Q3 recognizes absent verification but cannot identify the PR author or required exact revisions/diff/test output. Revised Q3 provides those and explicitly says the actual changes cannot yet be established. |
| Q4: outside scope | PASS | PASS | Both recover deferred persistence and scheduling. |
| Q5: decision | PASS | PASS | Both identify the open badge decision and product owner. |

Question evidence: [original answers](../pr-unavailable-source/original-output.md), [revised answers](../pr-unavailable-source/revised-output.md), and the oracle linked above.

The editor performs the authorized, supported local work while preserving the evidence gap. It distinguishes confirmed intent from unknown delivery, does not invent a checkout/diff, and names the PR author's next action and the product owner's separate pending decision. The unrestricted body/context authorize the factual content; no private source or workspace path enters the draft.

Limitations: exact source revisions, diff, implementation and test output remain unavailable. The run cannot prove the actual increment, runtime delivery or test results; those unknowns are the correct preserved outcome. The observed improvement concerns the reader's ability to recover the evidence/owner gap, not successful implementation verification. Shared protocol limitations apply.
