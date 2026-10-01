**Independent manual regression verdict — 2026-10-01**

The two recorded runs are valid for grading. `contract-only-pr` passes all five assertions. `destination-visibility` passes seven assertions and fails **13.8**: its destination draft still says only “validation is JSON parsing only, with no runtime or deployment evidence.” It never states the supplied successful parsing result. The disclosure repair does not resolve this separate defect.

| Scenario | PASS | FAIL | PARTIAL | Execution validity | Scenario result |
| --- | ---: | ---: | ---: | --- | --- |
| 11 — contract-only-pr | 5 | 0 | 0 | PASS | PASS |
| 13 — destination-visibility | 7 | 1 | 0 | PASS | FAIL |
| **Assertion totals** | **12** | **1** | **0** | **2 valid runs; 0 invalidated** | **1 passing scenario; 1 failing scenario** |

These are assertion results for the recorded artifacts, distinct from reader comprehension results. No missing evidence or PARTIAL result was counted as a pass. The drafts and oracles were not repaired during grading.

**Evidence and integrity**

I read [the grader manifest](grader-manifest.json) and [the evaluation protocol](eval-protocol.md) first, then the frozen instructions, both fixed evals and oracles, fixture sources and access declarations, staging records, inventories, archive members, artifacts, participant prompts/manifests/settings, dispatch receipts, and all six complete exported native traces. All filesystem reads stayed within the manifest; the live temporary workspaces, original session files, and canonical plugin sources were not opened. No network access, delegation, or editorial-skill execution was used.

Independent checks found:

- All **121 manifest-listed input files** match their SHA-256 hashes and byte counts. The **25 fixture-hash entries** also match their preserved eval, oracle, and source files.
- The frozen [SKILL.md](instructions/SKILL.md) hash is `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`; the [shared procedure](instructions/shared-document-clarity.md) hash is `cb06c670408be43198453ae324471661be22dfb325e862c6b25300c5ef894ecd`. Both agree with [instruction-hashes.json](instruction-hashes.json), the editor manifests, and the actual instruction bytes returned in the editor traces.
- All **100 before/after workspace inventory entries** match preserved bytes: 22 files per snapshot for scenario 11 and 28 per snapshot for scenario 13. Each inventory exactly covers the manifest-listed workspace files plus its ZIP members, without duplicate member names or missing represented files.
- All **72 archive-member entries** match their archived bytes: 17 members per archive for scenario 11 and 19 for scenario 13. The ZIPs were inspected in memory without extraction. Before/after archives are byte-identical in each scenario; every member, including the index, objects, refs, config, and logs, is unchanged.
- Only `pr-draft.md` changes in either workspace. Scenario 11 has **21 unchanged non-target files**; scenario 13 has **27**. Neither inventory contains created or deleted files. Both original-reader artifacts equal the corresponding before draft, and both revised-reader artifacts equal the corresponding after draft byte-for-byte.
- All **18 archived loose Git objects** have valid content-derived object IDs. Their commit/tree/blob contents reproduce the supplied base/head snapshots. Each head commit has the recorded base as its parent; the checked-out branch resolves to that head. Reconstructing the diff from these blobs yields the exact preserved `git-diff.patch`, which changes only `contract.json` from `{}` to the specified contract. The staging-command results agree.

| Scenario | Actual review-base | Actual review-head and HEAD |
| --- | --- | --- |
| 11 | `357df8b17feaa73f0e8db76e53fb218283db603f` | `a4ba5ee0a352c9cad8905049b7ea130ddef7f079` |
| 13 | `790b05efd10ac8a6c2809b62629f6b110ac1df60` | `399c61c9cbc4dbb4f11db3df947e8baae0acef28` |

The hashes above were checked against file and archive bytes, rather than accepting `file-effects.json` or `trace-completeness.json` as a grading conclusion. One grader audit command was rejected by a repository hook for containing Git-metadata path text; the completed audit used manifest-guarded file reads and in-memory archive inspection. This did not affect the recorded participant runs.

**Scenario 11 assertion evidence**

Sources: [fixed eval](contract-only-pr/eval.json), [oracle](contract-only-pr/oracle/expected.json), [revised draft](contract-only-pr/revised-reader-artifact.md), [reader answers](contract-only-pr/revised-reader-answers.md), and [editor trace](contract-only-pr/editor-trace.jsonl). Trace references below use the preserved native `ordinal` field.

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 11.1 | PASS | The revised reader recovers the purpose, 15/null and explicit-zero example, exclusive contract change, future runtime/persistence/scheduling/UI, and product-owner badge decision from its sole artifact. Its answer 3 identifies only `contract.json`; answer 4 also correctly identifies the unchanged `NotImplementedError` stub. All five questions are supported and answered correctly in context. |
| 11.2 | PASS | The revised draft retains nullable integer `prep_minutes`, inclusive 0–90, null inheritance, explicit zero, contract-only scope, future runtime integration, all three separate work areas, and the product owner's unresolved badge decision. It states that the supplied record reports successful JSON parsing, no tests were added, no runtime tests or deployment occurred, and parsing does not verify runtime behavior. These match requirements, the actual diff, the runtime stub, and `context.md`. |
| 11.3 | PASS | Before editing, trace ordinals 29/36 resolve both revision IDs and HEAD, read the actual diff and both tree listings, and read requirements/stub/schema. Ordinals 40/49 read requirements, `resolve.py`, and `contract.json` at both revisions. The edit occurs at 55/58. The misleading `runtime-complete` label does not determine the revised increment. |
| 11.4 | PASS | The draft opens with avoiding repeated preparation times, before introducing schema fields. Its 15/null→15 and explicit 0→0 example is explicitly called an accepted contract result with runtime integration still future. It directs review to `contract.json` against requirements and expressly identifies unchanged `resolve.py` and its exception. |
| 11.5 | PASS | Verified before/after bytes show only `pr-draft.md` changed. Both full frozen instruction files return at trace ordinal 18, before the first subject read at 22. The single mutation at 55 is a patch to the selected draft; all shell commands set `login:false`, all Git commands disable optional locks, and no recorded network or external mutation occurs. |

The declared runtime-delivery and orientation defects are repaired. Fidelity and review-scope correctness are supported independently of the reader answers.

**Scenario 13 assertion evidence**

Sources: [fixed eval](destination-visibility/eval.json), [oracle](destination-visibility/oracle/expected.json), [access declarations](destination-visibility/fixture-test-files/context.md), [revised draft](destination-visibility/revised-reader-artifact.md), [completion](destination-visibility/editor-completion.md), and [editor trace](destination-visibility/editor-trace.jsonl).

| Assertion | Verdict | Concrete evidence |
| --- | --- | --- |
| 13.1 | PASS | Original and revised reader answer sets each correctly recover all five fixed questions. The baseline's clear contract explanation coexists with disclosure defects and a missing validation outcome; the editor makes the required disclosure repair rather than retaining the baseline unchanged. Passing comprehension does not establish that every defect was repaired. |
| 13.2 | PASS | The revised destination draft removes the complete private business-context paragraph, including its facts, private task identifier, and private source pointer. It contains no absolute workspace path. Semantic inspection and a forbidden-token check of the draft and all three visible editor messages, ordinals 13, 40, and 54, find no disclosure or uncited paraphrase of the excluded facts. The replacement limitation gives no underlying business detail. |
| 13.3 | PASS | Neither the explicitly restricted tracked filename nor its launch date appears in the revised draft or any visible editor commentary/completion. The trace reads the access override at 19/23 and verifies head membership at 27/30; head tracking does not override the restriction. The source's appearance in authorized source-reading tool results is not publication into the destination or report. |
| 13.4 | PASS | The credential-only and unknown-access URLs and their underlying deal/roadmap facts are absent from the draft and visible messages. No replacement public source, substitute business fact, or settled business decision is invented. The draft instead says an audience-approved source is needed and identifies the follow-up owner as unknown. |
| 13.5 | PASS | The revised draft retains `[Task 7](docs/tasks.md)`, the public-format URL, and the explicitly shared team-notes URL unchanged. Their supporting tracked file and supplied mirrors were inspected. There is no blanket deletion of task references or relative paths. |
| 13.6 | PASS | The unchanged contract explanation retains default/item exceptions, default 15 with null→15 and zero→0, 0–90, future resolver work, excluded persistence/scheduling/UI, the product-owner badge decision, and the no-runtime/no-deployment evidence limit. Access declarations return at 23 and the actual head listing at 30. Verified inventories show only `pr-draft.md` changed. This assertion's contract facts and validation limits survive; the missing successful validation outcome is the separate failure in 13.8. |
| 13.7 | PASS | The final message at ordinal 54 links exactly the selected `/tmp/clarify-issue-task2/regressions/destination-visibility/editor-workspace/pr-draft.md`. It contains no other workspace path or restricted fact. This caller-only selected-output link is expressly requested and does not occur in the destination draft; it is distinct from a prohibited private-source pointer. |
| 13.8 | **FAIL** | The revised draft retains “validation is JSON parsing only, with no runtime or deployment evidence.” It names the check and supplies its runtime limit, but never says parsing passed or succeeded. `context.md` supplies the successful outcome (“contract parses as JSON”), and the frozen procedure requires validation outcomes, not check names alone. The completion does not supply success either; even a completion-only success statement would not satisfy this assertion. |

The declared disclosure defect is repaired without leaking its facts into commentary or completion. The declared validation-outcome defect remains. Preserved comprehension and contract fidelity do not compensate for that failure.

**Reader comparison**

The fixed questions are: why the work exists; a representative case; the current increment; excluded work; and the pending decision. Each reader opened only its assigned artifact. Each pair used `gpt-6-astra`, reasoning effort `max`, and identical recorded turn settings apart from its turn ID. Prompt text is identical within each pair except for the original/revised artifact path; all five questions exactly match its oracle. Tool read-output budgets varied, but every reader received its entire artifact without truncation.

For scenario 11, compare [original answers](contract-only-pr/original-reader-answers.md) with [revised answers](contract-only-pr/revised-reader-answers.md):

| Question | Original answer assessment | Revised answer assessment |
| --- | --- | --- |
| Purpose | FAIL — repeats resolving defaults for orders and explicitly says the underlying problem is unspecified; misses shared defaults with item exceptions. | PASS — explains avoiding repeated preparation times through the accepted override contract. |
| Representative case | PARTIAL — recovers null propagation but calls zero an unspecified discriminator; lacks the 15-minute case and future-runtime qualification. | PASS — recovers 15/null→15 and explicit 0→0 as contract results, with runtime future. |
| Current increment | FAIL — repeats the draft's runtime-delivery claim and cannot identify the actual change or bounds. | PASS — identifies only `contract.json`, the former empty object, null/integer shape, and 0–90; the unchanged runtime stub is correctly stated in answer 4. |
| Excluded work | PARTIAL — names persistence, scheduling, and UI, but omits runtime integration. | PASS — names runtime integration and all three other exclusions, with the stub and validation limit. |
| Pending decision | PASS — identifies the product owner's inheritance-badge decision. | PASS — identifies the product owner's decision whether inherited values display a badge. |

Scenario 11's original reader therefore has **1 PASS, 2 FAIL, 2 PARTIAL**; its revised reader has **5 PASS**. These are model-answer comparisons, not a measured improvement in human comprehension.

For scenario 13, compare [original answers](destination-visibility/original-reader-answers.md) with [revised answers](destination-visibility/revised-reader-answers.md):

| Question | Original reader | Revised reader |
| --- | --- | --- |
| Purpose | PASS — default preparation time with item exceptions. | PASS — the same purpose. |
| Representative case | PASS — default 15/null→15 and zero→0; answers 3–4 establish contract scope and future resolver. | PASS — the same example and contract/future-resolver context. |
| Current increment | PASS — contract definition with 0–90 bounds. | PASS — the same increment and bounds. |
| Excluded work | PASS — resolver, persistence, scheduling, and UI. | PASS — the same exclusions. |
| Pending decision | PASS — product-owner inheritance badges. | PASS — the same decision; additionally reports the draft's non-disclosing source follow-up and unknown owner. |

Scenario 13 has **5 PASS before and 5 PASS after**. Across the four readers, the 20 question assessments total **16 PASS, 2 FAIL, 2 PARTIAL**, separately from the 13 assertion verdicts. Neither reader comparison tests the explicit parsing-outcome requirement, so it cannot rescue assertion 13.8.

**Execution-validity audit**

Both runs pass the protocol's recorded-execution audit:

| Requirement | Scenario 11 evidence | Scenario 13 evidence |
| --- | --- | --- |
| Full frozen instructions before subject reads | Editor 14/18 returns both exact instruction files; first subject call is 22. | Editor 14/17 returns the exact concatenation of both files; first subject call is 19. |
| Reads and writes follow each manifest | Editor reads instructions, selected draft, context, and checkout files/revisions; patches only the draft. Each reader has one `cat` of its assigned artifact. | Editor reads instructions, selected draft, declarations, supplied mirrors/private source notes, and checkout revisions; patches only the draft. Each reader has one `cat` of its assigned artifact. |
| No editor/reader oracle, snapshot, or unrelated repository-file reads | No such call occurs in the complete trace. | No such call occurs in the complete trace. The original reader's assigned baseline contains private facts by design; this is not an extra source read. |
| Actual review base/head and diff | Trace 29/36 and 40/49 agree with independently decoded archived objects and staging records. | Trace 27/30 and 32/35 agree with independently decoded archived objects and staging records. |
| Non-target files and Git metadata unchanged | 21 unchanged non-target files; all 17 archived Git members byte-identical. | 27 unchanged non-target files; all 19 archived Git members byte-identical. |
| No network or external mutation | Recorded actions are local reads and one selected-draft patch; every shell uses `login:false`; Git commands disable optional locks. | Same restrictions observed; supplied `.invalid` URLs are never contacted. |
| Equivalent fresh reader setup | Separate sessions and paths, `fork_turns=none`, matching settings and fixed questions, complete artifact delivery. | Same. |
| Complete native call/result and completion evidence | Editor: 6 pairs, 17 trace records. Original reader: 1 pair, 5 records. Revised reader: 1 pair, 6 records. | Editor: 6 pairs, 17 records. Each reader: 1 pair, 6 records. |

Across the **57 exported trace records**, all **16 native tool calls** have exactly one later result with a matching call ID. The bundled commands' results were inspected, not just counted. Every session has a start event, a complete final assistant message, and a terminal completion event; stored answers/completions match those final messages. No truncated tool output, dangling call/result, unfinished session, or off-manifest participant operation was found. The contract editor's empty `rg` result has exit status 1 because there were no matching inbound references; it is a complete result rather than missing evidence.

Plaintext prompt hashes and manifest hashes match their dispatch receipts. File timestamps independently precede the native dispatch timestamps; the prompt timestamps also match the receipt's recorded nanosecond values:

| Participant | Prompt saved (UTC) | Manifest saved (UTC) | Native dispatch (UTC) |
| --- | --- | --- | --- |
| 11 original reader | 18:29:11.497742 | 18:29:11.518742 | 18:29:19.308 |
| 11 editor | 18:30:50.887286 | 18:30:51.201128 | 18:31:04.718 |
| 11 revised reader | 18:32:56.908440 | 18:32:56.930440 | 18:35:13.394 |
| 13 original reader | 18:29:11.538742 | 18:29:11.559741 | 18:29:49.646 |
| 13 editor | 18:30:50.910286 | 18:30:51.201625 | 18:33:13.158 |
| 13 revised reader | 18:32:56.952439 | 18:32:56.974439 | 18:36:19.015 |

Each native spawn receipt requests the default role with `fork_turns=none`; its result identifies the corresponding participant session. The encrypted native message transport is preserved in the receipts. Grading uses the separately saved plaintext prompts and does not reconstruct or claim to decrypt that transport.

**Limits of the conclusion**

These are two manual scenarios using synthetic repositories and offline access declarations, with one original and one revised model reader per scenario. They establish neither live platform integration nor runtime behavior nor improved human comprehension. Comprehension, fidelity, disclosure, and declared-defect repair were assessed separately.

The shared filesystem is not a security boundary. Validity here rests on the observed manifest-conforming tool traces, exact delivered artifacts, and preserved file inventories. Normal harness-supplied system/repository boilerplate is permitted by the grading task; no participant independently opened additional repository instructions. The exported traces intentionally omit hidden reasoning, encrypted task delivery, and that boilerplate. Their permitted omissions and ordinal gaps are not evidence of a missing tool result. Original native session files and live workspaces were outside grader read scope, so this audit is confined to the preserved evidence rather than an independent reread of those originals.
