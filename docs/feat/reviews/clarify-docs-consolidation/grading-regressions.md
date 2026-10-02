# Independent regression grading

The candidate receives **13 PASS, 1 PARTIAL, 0 FAIL** across the 14 assertions. `already-clear` passes all four assertions; `cross-file-preservation` passes all five. `source-disagreement` passes four assertions and partially meets 2.4: it identifies the conflict and owner, but states the reconciliation objective without specifying a concrete next action.

All three trials have usable visible evidence. Their recorded editor and reader operations respect the assigned subject-file boundaries; the archived documents and runtime manifest agree. These are three manual trials, not evidence of general reliability or measured human-comprehension improvement.

## Scope and method

I read each case's `eval.json` and `oracle/expected.json` before inspecting its artifacts and evidence. I used only the grading request's permitted common files, fixtures, snapshots, editor traces/completions, and original/candidate reader traces/completions. I did not invoke a skill, execute fixture source, use an external service, or change an input. This report is the only file written.

Evidence paths below are relative to this report unless stated otherwise. Fixture references point to `klaude-plugin/skills/clarify-docs/evals/<case>/test-files/` in the repository. Trace line numbers refer to physical JSONL records; tool ordinals are included where useful. Archived `.txt` document names were mapped back to their runtime Markdown filenames when checking links.

The reader grades assess agreement with the oracle, rather than merely whether a reader faithfully repeated its assigned document. An answer may draw clarification from another numbered answer in the same response; this is applied consistently to the timing mismatch and planned-preview status.

## already-clear — PASS

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 5.1 — All five reader answers pass on original and final guide | PASS | Both `evidence/consolidation_reader_original_clear.txt` and `evidence/consolidation_reader_candidate_clear.txt`, answers 1–5, give the default/exception purpose, complete 15-to-20 example including explicit zero and old-order 15, lookup plus order snapshot, scheduling exclusion, and product-owned badge decision. |
| 5.2 — Guide remains byte-for-byte unchanged because baseline requirements pass | PASS | Original fixture and `snapshots/candidate-already-clear.txt` are identical 729-byte files with SHA-256 `470c0b18bdf8a3dc89435eaad523af08a28e9559c4a96c3d8be968022ade55de`. Lines 2–8 introduce purpose and behavior before implementation names at lines 10–11; lines 11–12 state exclusion and decision. Requirements and inspected source agree with those claims. |
| 5.3 — Inspect requirements/source and applicability before no-op | PASS | Editor trace `evidence/consolidation_candidate_clear.jsonl` line 7 returns both full instructions; line 9 returns the complete guide, requirements, and source. The applicability checks at line 10 precede the no-edit completion at line 11. No inference from the final answer alone was needed. |
| 5.4 — No file added or changed; response explicitly reports no edit needed | PASS | The trace contains three read-only calls and no mutation. `manifest.json` has identical original/final workspace file sets and hashes for `guide.md`, `requirements.md`, and `prep.py`. `evidence/consolidation_candidate_clear.txt` explicitly says “No edits needed.” |

| Reader question | Original | Candidate | Oracle comparison |
| --- | --- | --- | --- |
| 1. Purpose | PASS | PASS | One restaurant default with item exceptions. |
| 2. Representative case | PASS | PASS | Inherited 15 becomes 20 after the change; explicit zero stays zero; the earlier order retains 15. |
| 3. Current increment | PASS | PASS | Current-value lookup and snapshot at order creation. |
| 4. Exclusion | PASS | PASS | Scheduling. |
| 5. Decision | PASS | PASS | Product owner decides inheritance badges. |

The no-op is justified by the artifact and source comparison, not just by passing reader questions. No new private facts, references, summary artifact, or structural change was introduced.

## source-disagreement — PARTIAL

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 2.1 — Distinguish accepted next-day intent from current immediate behavior; other answers match | PASS | Candidate reader answer 2 states required 15 until the next day, inspected immediate 20, and retained old-order 15. Answers 1, 3, 4, and 5 cover purpose, lookup/snapshot scope, scheduling exclusion, and both owners. The mismatch is explicit in answers 2 and 5, even though answer 3 does not repeat it. |
| 2.2 — Retain mandatory next-day requirement and describe immediate implementation without settling conflict | PASS | `snapshots/candidate-source-disagreement.txt` lines 10–14 retain “must wait until the next day” alongside the immediate implementation and concrete 15-to-20 example. Lines 6–8 preserve missing/null inheritance, explicit zero, and unchanged snapshots. The artifact does not waive the requirement or claim the implementation already meets it. |
| 2.3 — Requirements and implementation inspected before revision | PASS | `evidence/consolidation_candidate_disagreement.jsonl` line 7 returns both complete instructions; line 9/ordinal 30 returns full `requirements.md` and `prep.py`; the first edit is line 10/ordinal 34. The inspected example explicitly returns new lookup 20 and old order 15. |
| 2.4 — Record discrepancy, feature-maintainer owner, concrete reconciliation next step, and no claimed code/requirement fix | PARTIAL | Snapshot lines 10–17 identify the mismatch and feature maintainer; lines 20–21 state inspection only and no source execution. However, “owns reconciling the required delay with the implementation and the current exclusion of scheduling” states responsibility and the desired resolution, without naming the next action that will resolve it. The completion repeats the same objective. Neither claims a code or requirement fix. |
| 2.5 — Only guide changes | PASS | The sole mutation is the `guide.md` patch at trace line 10. Manifest workspace file sets match; `requirements.md` and `prep.py` retain their original hashes. The final guide hash matches the archived snapshot. |

The remaining gap in 2.4 is narrower than a missing owner or hidden disagreement. A concrete next step could assign the maintainer to review how delayed activation can satisfy the accepted timing rule within the scheduling exclusion, then record the reconciliation decision. That would identify work to do without choosing the outcome on the maintainer's behalf.

| Reader question | Original | Candidate | Oracle comparison |
| --- | --- | --- | --- |
| 1. Purpose | PASS | PASS | Both identify defaults with item exceptions. |
| 2. 15-to-20 update | FAIL | PASS | Original answer presents next-day activation as current behavior and misses inspected immediate lookup; candidate distinguishes both and preserves old-order 15. |
| 3. Current increment | PARTIAL | PASS | Original names lookup and snapshots but exposes no timing mismatch anywhere in its response. Candidate names the increment and makes the mismatch explicit in answers 2 and 5. |
| 4. Exclusion | PASS | PASS | Both exclude scheduling. |
| 5. Decision | PARTIAL | PASS | Original names only the product badge decision. Candidate also names the feature maintainer's timing reconciliation responsibility. |

Reader evidence: `evidence/consolidation_reader_original_disagreement.txt` and `evidence/consolidation_reader_candidate_disagreement.txt`. The original reader faithfully reflected a deficient document; its failing oracle comparison is not evidence that it ignored its instructions. The candidate reader's five answers match the oracle, while assertion 2.4 imposes the additional concrete-next-step requirement that remains incomplete.

## cross-file-preservation — PASS

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 4.1 — Five reader answers supported, with planned versus implemented status retained | PASS | Candidate reader answers 1–5 identify catching CSV errors, planned two-valid/one-invalid/zero-write preview, preview-only increment with column acceptance complete and counts unchecked, future disabled apply, product-owned duplicate policy, and support approval. `snapshots/candidate-cross-design.txt` lines 27–29 explicitly limit runtime claims; `snapshots/candidate-cross-tasks.txt` preserves the recorded state. |
| 4.2 — Required sections, MUST/MAY, acceptance date, support gate, and product ownership | PASS | Final design retains `Context`, `Decision`, `Deployment gate`, and `Consequences` at lines 3, 10, 18, and 22. Lines 12–16 preserve Mira, 2026-09-01, mandatory `id,name`, optional diagnostics, and the fact that diagnostics do not authorize apply. Lines 20 and 24–25 retain the support gate and product-owned duplicate decision. |
| 4.3 — Preserve every status, checkbox, and dependency exactly | PASS | Ordered status values remain `in-progress`, `pending`; dependency lines remain `—`, `Task 1`; ordered checkbox states remain `[x]`, `[ ]`, `[ ]`. Task identities are unchanged. Checkbox descriptions receive formatting and a requirement-backed zero-write clarification, but no checkbox state, status, or dependency changes. |
| 4.4 — Inbound and cross-file links resolve; entry and requirements unchanged | PASS | Both original inbound destinations and both original cross-file destinations resolve using the runtime names; see the link audit below. Manifest hashes for `entry.md` and `requirements.md` are unchanged. The new Task 2 and Context links also resolve. |
| 4.5 — Explain preview before admission-observation terminology; three-row case stays planned | PASS | Design lines 5–8 begin with operator purpose, explain the planned preview plainly, and give two valid/one invalid/zero written. The unexplained admission-observation terminology is removed. The count checkbox remains unchecked at tasks line 9; design lines 27–29 expressly avoid claiming verified runtime behavior. |

| Reader question | Original | Candidate | Oracle comparison |
| --- | --- | --- | --- |
| 1. Purpose | PASS | PASS | Catch CSV mistakes before apply. |
| 2. Representative case | PASS | PASS | Two valid, one invalid, zero written. Original answer 3 supplies the incomplete-count status; candidate answer 2 directly labels the case planned. |
| 3. Current increment | PASS | PASS | Preview only; column acceptance complete; counts pending. |
| 4. Exclusion | PASS | PASS | Apply disabled/future, Task 2 pending and dependent on Task 1. |
| 5. Decision/gate | PASS | PASS | Product duplicate-row policy and support walkthrough approval before enablement. |

Reader evidence: `evidence/consolidation_reader_original_cross.txt` and `evidence/consolidation_reader_candidate_cross.txt`. The candidate makes planned status and the opening explanation more direct, but this trial does not demonstrate a gain in the number of correct reader answers: the original answer set already supports all five.

### Link and task audit

| Original link origin | Preserved runtime target | Final heading establishing anchor |
| --- | --- | --- |
| `entry.md` line 2, preview task | `tasks.md#task-1-preview` | `Task 1: Preview`, tasks line 3 |
| `entry.md` line 2, gate | `design.md#deployment-gate` | `Deployment gate`, design line 18 |
| Original design line 14, task state | `tasks.md#task-1-preview` | `Task 1: Preview`, tasks line 3; link retained at design line 27 |
| Original tasks line 7, deployment gate | `design.md#deployment-gate` | `Deployment gate`, design line 18; link retained at tasks line 12 |

The added `tasks.md#task-2-apply` and `design.md#context` targets also resolve. Task 1 still has no dependency, completed column acceptance, and incomplete counts. Task 2 is still pending, depends on Task 1, and retains its unchecked product-policy prerequisite. No implementation source was provided or inferred.

## Execution and evidence audit

| Check | Result and evidence |
| --- | --- |
| Full instruction reads before subject matter | PASS. All three editor traces return both entire instruction files at JSONL line 7. Their contents exactly match `instructions/candidate-SKILL.txt` and `instructions/candidate-procedure.txt`, including the latter's final paragraph. The instruction hashes match the manifest. Subject results arrive later: line 9 for clear/disagreement, line 10 for cross-file. |
| Full supplied subject reads before decisions/edits | PASS. Clear and disagreement each read all three permitted files in full. Cross-file reads design, tasks, entry, and requirements in full. Source strings in the traces exactly match the original fixtures. No partial `head`, search-only source inspection, or truncated instruction/source result substitutes for a complete read. |
| Visible trace completeness | PASS within the provided trace format. Clear has 3 call/result pairs, disagreement 5, and cross-file 5. Each of the six reader traces has 2 pairs. Every call has a matching result and each trace ends with its final response. All nine `.txt` completion files equal the corresponding recorded final response plus one archival newline. Hidden reasoning and harness boilerplate are intentionally excluded by the protocol. |
| Editor path isolation | PASS for visible agent operations. Reads target the assigned request, the two staged instructions, and the assigned workspace files. The only write calls are one patch to disagreement `guide.md` and one patch to cross-file `design.md`/`tasks.md`. No repository, oracle, other-case, or installed-skill subject read appears. |
| Reader isolation | PASS for visible agent operations. Every reader reads its own request, then only its assigned guide or assigned design/tasks/entry set. Requests contain the fixed oracle questions, not oracle answers. No reader reads requirements, implementation, instructions, or another version. Every reader is read-only. |
| Source execution and external services | PASS. Editor and reader shell commands are file-display commands (`cat`, or final `nl -ba`); edits use `apply_patch`. No fixture execution, import, tests, network call, external service, or publishing action appears. The disagreement guide correctly records that source assertions were not run. |
| Writable-file scope and no additions | PASS. Manifest original/final workspace filename sets match in all three cases. Clear has no changed hashes; disagreement changes only guide; cross-file changes only design and tasks. This matches every visible mutation. |
| Candidate verification checklist | OBSERVED. All editors record the five checks in order: reader tasks, repeated explanations, history/evidence, protected meaning, structure/visibility. See clear trace line 10, disagreement line 14, and cross-file line 15. They include document/line references, though not every bullet has its own line number. These statements were checked against artifacts rather than accepted as independent proof. No extra ledger or summary file appears. |
| Model metadata | CONSISTENT. All nine traces identify `gpt-6-astra` with `max` effort. The manifest records `fork_turns: none`; build and temperature are not exposed. The trace format does not independently establish hidden prompt contents or operating-system confinement. |

Initial login-shell calls emit a failed startup logging warning concerning a file outside the staged workspaces. The visible evidence shows no successful outside write or subject data obtained from that path. I treat that warning as harness startup noise, not as an agent-requested out-of-manifest source read. The isolation finding is explicitly limited to the recorded operations and manifests, as the protocol requires; it is not an operating-system access audit.

### Hash confirmation

Every original fixture file matches its `manifest.json` original-workspace entry. Every final snapshot matches its candidate-workspace entry. The final edited-document hashes are:

| Runtime file | Final SHA-256 |
| --- | --- |
| already-clear `guide.md` | `470c0b18bdf8a3dc89435eaad523af08a28e9559c4a96c3d8be968022ade55de` |
| source-disagreement `guide.md` | `4c28bf41c8a9a70436f5f6a0da961d30a62c2a818e6eb39db46fd7122b475f02` |
| cross-file-preservation `design.md` | `31d60658ade0cb918401beb23ee16d5029f08d152e044d1fd18262e8ea4b2a93` |
| cross-file-preservation `tasks.md` | `da4589166028409974f7d045f3015762aacbe91d54bdcae65cd4a721965ffc3c` |

The unchanged cross-file inputs retain `entry.md` SHA-256 `75d00778ce1cdd9846663a991c6691f977bf9ad31919492d7de7f50204a055fa` and `requirements.md` SHA-256 `71d7a96c2a4a85a23f2c2a15d5f03f9e51f01f4cec01c382cbcb643c2be6fab4`. Final hashes for unchanged, unarchived source inputs are taken from the runtime manifest; their original fixture contents and editor read results were checked directly.
