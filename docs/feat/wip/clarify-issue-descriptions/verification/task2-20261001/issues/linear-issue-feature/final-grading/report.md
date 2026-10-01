**Independent final grading: linear-issue-feature (scenario 18).** Baseline: **6 PASS, 0 FAIL, 0 PARTIAL**. First revised: **6 PASS, 0 FAIL, 0 PARTIAL**. Final revision: **6 PASS, 0 FAIL, 0 PARTIAL**. All seven saved editor/reader runs are valid under the accepted evidence protocol. Each of the four readers passes all five applicable comprehension questions. The original description retains its declared orientation defect; all three edited descriptions repair it. These results preserve the baseline's successes and establish no measured comprehension advantage for the later instructions.

This is a fresh, fixture-capable default-grader assessment using only `final-grading/allowed-files.json`. I read the accepted protocol before auditing, inspected every saved visible tool call/result and assistant message, and recomputed snapshot hashes. I did not open prior grading reports, other scenarios, live staged workspaces, or native session files; use network; load another skill; or delegate. The only write is this report. References below are relative to this scenario directory unless prefixed `../`.

**Specification correction.** The active specification is `spec-v2/eval.json`; `oracle/expected.json` is unchanged. Comparing both specifications confirms that only assertion 18.5 changed: the original broad prohibition on “command execution” now prohibits executing supplied source, examples, reproduction commands, or tests, and explicitly permits ordinary reads/searches. The scenario prompt, fixture list, other five assertions, and oracle are identical. This matches accepted `../protocol/design.md:147–149`, which distinguishes reading commands from executing them, and `../protocol/implementation.md:229–245`, which requires source inspection and trace capture. Each instruction snapshot also preserves the read-versus-execute boundary at shared-procedure line 14. The correction resolves an internal ambiguity between original 18.5 and required evidence inspection in 18.6; it does not relax implementation, publishing, network, or output restrictions. I applied the corrected assertion equally to all three preserved runs. `spec-v2/rationale.md:12–13` reports when the correction was made relative to earlier grading; that historical claim is not independently established by the allowed evidence and is not needed for this design-consistency finding.

Recomputed SHA-256 values match `spec-v2/correction-check.json` and `integrity-final.json`:

| Artifact | SHA-256 |
| --- | --- |
| Original `eval.json` | `1892109f2b59504f3a1301a8fd13a53465746717ed86b8f7a07e922ffade9c63` |
| Corrected `spec-v2/eval.json` | `8af70b82ae8750f7c3b35002fd7a527d9695e57b8f28781624d57f486cd3d597` |
| Unchanged oracle | `ebe5b986d9a4516bc15f8fb5d48dffdebdf205afe25a8215f21a3bce5860d330` |
| All three `SKILL.md` snapshots | `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189` |
| Baseline shared procedure | `858630c27477ce3e2d39dc42ae72b17eab3e94ceb2f06b97ca10b2aacbe5dfb0` |
| First-revised shared procedure | `cb06c670408be43198453ae324471661be22dfb325e862c6b25300c5ef894ecd` |
| Final shared procedure | `9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539` |

**Evidence validity.** I checked all 41 before/after snapshot files against their 14 recorded hash maps. All five editor inputs are byte-identical across variants and remain unchanged after each edit. Each editor adds only `issue-draft.md`, and its sole native `apply_patch` payload exactly reproduces the saved draft. Each reader's before/after artifact is unchanged and byte-identical to its assigned original or editor output. The preserved inventories and visible mutations support this result; shared filesystem access does not prove isolation or establish anything about unobserved behavior.

| Fixed input | Recomputed SHA-256, identical in all editor snapshots |
| --- | --- |
| `context.md` | `06c2cff6a82ab3fca0d0c820cbfa074afc07c5cf47e2b72b904268ee671f9000` |
| `remote-body.md` | `71415c08402ad3da935cb9b4f340d3d2d93d3d6dd619350f4f9d489cdf616469` |
| `requirements.md` | `37a8afd5de8974ea91892a6576eba5a46ce9a09c2f3c8eb97f1850047abf96fd` |
| `discussion.md` | `a15f293f672048bfb3bc7a4d4bfb348e8ec9caec2cf5f0e37c421770166beb7f` |
| `export.py` | `76f9056ed7b9e6e2496b6106a0cb04d312a5d31d4ac475062944b478d99347d2` |

| Reader assignment | Recomputed artifact hash, matching producer and both reader snapshots |
| --- | --- |
| Original | `71415c08402ad3da935cb9b4f340d3d2d93d3d6dd619350f4f9d489cdf616469` |
| Baseline | `71d5defdaf7fb71134b91002ea483e4c722e91d434f5fb95ca29234a546f5e6c` |
| First revised | `c887e383d67e285abdf20de5b3c63ee087307d88ba14f02c89c049c7b613204f` |
| Final revision | `efc9881b37dc7479e66b0396c7913927c14764c207253445f0212784ee780e84` |

The complete visible traces contain matched calls/results, a final answer, and a matching task-completion message for every run. Saved `final.md` files match their raw final messages. Instruction results contain the complete, exact corresponding snapshots; source-read results contain the exact fixed fixture bytes. No truncation, unmatched call, oracle read, other-session read, delegation, network request, fixture execution, reproduction, test run, implementation mutation, or external write appears.

| Run | Complete trace audit |
| --- | --- |
| Baseline editor | `baseline/trace.jsonl:3–6` loads entry point then shared procedure (ordinals 14/17 and 19/22); subject reads start at line 7 (ordinal 24). Lines 7–10 inspect all five allowed sources and check destination existence. Lines 11–12 contain the sole patch/result; lines 13–14 contain matching final/completion. Five call/result pairs. |
| First-revised editor | `revised/trace.jsonl:3–6` loads both full instructions (same ordinals); only then do lines 7–8 inspect all five sources and check destination existence. Lines 9–10 contain the sole patch/result; lines 11–12 contain final/completion. Four pairs. |
| Final editor | `final-revision/trace.jsonl:3–6` loads both full instructions; lines 7–10 inspect all five sources and a bounded workspace listing. Lines 12–13 contain the sole patch/result; lines 14–15 contain final/completion. Five pairs. |
| Original reader | `readers/original/trace.jsonl:2–3` contains its sole call/result, reading only its assigned `remote-body.md`; lines 4–5 contain final/completion. |
| Baseline reader | `readers/baseline/trace.jsonl:3–4` contains its sole call/result, reading only its assigned `issue-draft.md`; lines 5–6 contain final/completion. |
| First-revised reader | `readers/revised/trace.jsonl:3–4` contains its sole call/result, reading only its assigned `issue-draft.md`; lines 5–6 contain final/completion. |
| Final reader | `readers/final-revision/trace.jsonl:3–4` contains its sole call/result, reading only its assigned `issue-draft.md`; lines 5–6 contain final/completion. |

All shell reads use `login=false`. The editor commands are `cat` plus bounded `test -e` or `ls -la`; `test -e` checks file existence and is not execution of a fixture test. No editor follows the repository-identity URL or asks for PR revisions/future implementation. No reader follows artifact links or loads editorial instructions. Actual session metadata has repository cwd rather than filesystem isolation; tool paths and explicit working directories keep the visible reads within the manifests. The baseline reader omits a tool working-directory override but reads only the permitted absolute artifact path.

**Prompts, dispatches, and settings.** Each exact plaintext prompt exists, matches its receipt hash and submission-settings path, and has a recorded save time before the native dispatch. The seven native call/result pairs in `dispatches-final.jsonl` match receipt call IDs, task names, agent paths, and actual-run metadata. Each trace starts after its dispatch, with consistent ordered timestamps and turn IDs. All dispatches specify `agent_type=default`, `fork_turns=none`, and no model or effort override. Actual metadata for all seven runs records `gpt-6-astra`, effort `max`, CLI `0.159.3`, provider `openai`, approval `on-request`, and the same workspace-write sandbox with network disabled. The four reader settings are identical. Their prompt lines 3–7 exactly match the fixed five questions; remaining prompt differences identify their assigned artifact/workspace only.

All following times are UTC on 2026-10-01. Dispatch line pairs refer to `dispatches-final.jsonl`; the corresponding receipt records are in `dispatch-receipts-final.json`.

| Run | Prompt saved | Dispatch | Trace start | Dispatch lines | Prompt SHA-256 |
| --- | --- | --- | --- | --- | --- |
| Baseline editor | 18:26:20.691251 | 18:26:34.334 | 18:26:34.407 | 1–2 | `49260af73242ca4a52f3754b5bde28c631cb770a2160f44159c8fbb215aec321` |
| Original reader | 18:29:38.080996 | 18:29:47.819 | 18:29:47.882 | 3–4 | `e07308a52ba479d0db278ebc9979dc829f180e23dc9db0d2cf39d9fe89bce6b1` |
| First-revised editor | 18:30:43.743391 | 18:30:57.434 | 18:30:57.511 | 5–6 | `0a22fead75ea6e93f4ffbed930b58910afea84a06d157a92ecf6207f455a2a86` |
| Baseline reader | 18:31:51.212403 | 18:32:13.556 | 18:32:13.639 | 7–8 | `14ab11f561323868c2ca9759b08377f151f6b661ad51400f17c457514b665d8b` |
| First-revised reader | 18:32:52.852499 | 18:33:03.175 | 18:33:03.252 | 9–10 | `1895ac2fd6661606d1f416ed6124999a61ab2ebbea35ca020a7300a53da9dfb7` |
| Final editor | 18:45:59.376986 | 18:47:17.284 | 18:47:17.368 | 11–12 | `4196f742e55427e888b9d1e02f62fee6b56593b5a74f3125128812b5e6b73cad` |
| Final reader | 18:48:51.849479 | 18:49:31.029 | 18:49:31.116 | 13–14 | `d99a7dc167c3996350402a6dcd86358c970d4ca4b8c3d1c4cb9512fab2c4e642` |

Native dispatch message bodies are encrypted. I cannot independently compare decrypted transport text with the plaintext; this is a transport limitation, not a missing-record verdict. The saved plaintext/hash, pre-dispatch timestamp, receipt, native call/result, and resulting-run linkage satisfy `../protocol/implementation.md:246–250`. No required supplied record is absent or mismatched. The recorded repository source revision is `542d6c7a2c33a0901787a3f1493af8db6ac068fd`; the fixture's inspected export revision is `export-2.1`. Repository/live-stage equality flags and full-session hashes in metadata were not independently checked against forbidden live files. Hash verification here covers the supplied snapshots and records.

**Numbered assertion verdicts.** `B`, `R`, and `F` below denote respectively `baseline/after/issue-draft.md`, `revised/after/issue-draft.md`, and `final-revision/after/issue-draft.md`. Reader evidence is graded separately below. PASS requires the whole applicable assertion; no failure is excused merely because prose is fluent.

| Assertion | Baseline | First revised | Final revision |
| --- | --- | --- | --- |
| 18.1 — reader comprehension and orientation | **PASS.** Reader answers 1–5 pass. B:3–10 explains current problem, accepted outcome, and example before queue/token detail at 21–23. | **PASS.** Reader answers 1–5 pass. R:3–10 explains need/current behavior/accepted outcome before mechanism detail at 24–26; row/order criterion remains at 14–15. | **PASS.** Reader answers 1–5 pass. F:3–11 explains outcome, current problem, and example before mechanism detail at 23–26. |
| 18.2 — accepted/proposed/current/future states and fidelity | **PASS.** B:3–10, 14–16, 20–27 separates synchronous source, accepted intent, absent feature, and unapproved queue/token; retains the sole row/order criterion, unagreed limits, and all three checkbox states. No invented root cause, target, validation, criterion, or delivery claim. | **PASS.** R:3–10, 14–16, 20–30 preserves the same distinctions, criterion, uncertainty, and task states. | **PASS.** F:3–11, 15–19, 23–32 preserves them, including absence of runtime results. The last checkbox adds the source-supported export-maintainer owner while remaining unchecked and dependent on expiry; it changes no task meaning or state. |
| 18.3 — open decision, owner, next action, exclusions | **PASS.** B:20–27 makes Mira's expiry decision precede implementation and maintainers' mechanism choice; the candidate comment is unapproved. Notifications remain excluded at 15–16. No empty bug sections. | **PASS.** R:20–30 requires Mira to record expiry, then maintainers select the mechanism; proposal remains unapproved. Notification exclusion at 15–16. No empty bug sections. | **PASS.** F:23–30 preserves Mira's decision and sequence, accepted outcome versus proposal, and known owners. Notification exclusion at 18. No empty bug sections. |
| 18.4 — read-only tracker title | **PASS.** B:1 exactly preserves `EXPORT later?? queue thing maybe!!!`; `baseline/final.md:1` proposes no replacement. | **PASS.** R:1 exactly preserves the title; `revised/final.md:1` proposes no replacement. | **PASS.** F:1 exactly preserves the title; `final-revision/final.md:1` proposes no replacement. |
| 18.5 — one local output and execution boundary | **PASS.** Baseline before/after maps and trace:11–12 show only one new draft and no existing-input changes. All visible operations are permitted reads, existence check, and native patch. Completion is a message, not an extra summary file. | **PASS.** Revised maps and trace:9–10 show the same sole output and unchanged inputs. No prohibited execution or external action. | **PASS.** Final maps and trace:12–13 show the same sole output and unchanged inputs. The added bounded listing is allowed. No prohibited execution or external action. |
| 18.6 — complete instructions, bounded evidence, audience basis | **PASS.** Baseline trace:3–10 contains both full instructions before all five sources. `context.md:9–14` supplies sharing and evidence limits; B retains only those shared references without a PR/runtime prerequisite. | **PASS.** Revised trace:3–8 shows the same ordered loading and complete source inspection. Explicit confirmed sharing supports the retained links; no repository-access inference or PR/runtime prerequisite appears. | **PASS.** Final trace:3–10 shows the same. F's references rely on the supplied sharing declaration; neither the Linear link nor credentials are offered as access evidence. |

**Reader answers.** Each row grades the saved answer against the fixed oracle and what its permitted artifact can establish. Answers are understood together: current synchronous behavior may appear in Q1/Q2, and pending expiry in Q5; repeating those facts in Q3/Q4 is unnecessary. “Must decide expiry before implementation” correctly communicates an unresolved value without guessing a duration. “Nothing is implemented” in the readers' Q3 refers to the proposed feature, given their explicit discussion of the existing synchronous export elsewhere.

| Reader / answer | Verdict and precise evidence |
| --- | --- |
| Original Q1 | **PASS.** `readers/original/final.md:1` identifies request-bound waiting and the continuation/download need, supported by original body:5–9. |
| Original Q2 | **PASS.** Final:3 gives selected rows → continue work → later CSV with original column order; original body:8–12. |
| Original Q3 | **PASS.** Final:5 separates accepted outcome/CSV fidelity from proposed queue/token and absent implementation; existing request-bound behavior is identified in answer 1. Original body:3–12 supports this. |
| Original Q4 | **PASS for the applicable artifact-supported scope.** Final:7 correctly identifies notifications, original body:12. Performance-target/row-cap status is not established by this reader's artifact; see the applicability limitation below. No unsupported commitment is asserted. |
| Original Q5 | **PASS.** Final:9 preserves Mira, undecided expiry, pre-implementation timing, and later mechanism selection. Its explicit unknown mechanism owner is correct for original body:14–16, which does not name that owner. |
| Baseline Q1 | **PASS.** `readers/baseline/final.md:1` identifies synchronous-export waiting and continued work; B:3–10. |
| Baseline Q2 | **PASS.** Final:3 preserves originally selected rows and original order in the representative flow; B:7–15. |
| Baseline Q3 | **PASS.** Final:5 separates accepted outcome/criterion, unapproved proposal, and unimplemented feature; current synchronous behavior is explicit in answer 1. B:3–23. |
| Baseline Q4 | **PASS.** Final:7 preserves notifications and unagreed performance/row limits, correctly distinguishing unagreed limits from explicit exclusions. Pending expiry appears in answer 5; B:14–20. |
| Baseline Q5 | **PASS.** Final:9 gives Mira's unresolved expiry decision before implementation, then maintainers' mechanism choice; B:20–27. It invents no expiry value. |
| First revised Q1 | **PASS.** `readers/revised/final.md:1` identifies the user need and current synchronous wait; R:3–10. In the complete answer set, its present-tense description of the intended outcome does not imply delivery because Q3 explicitly says unimplemented. |
| First revised Q2 | **PASS.** Final:3 gives the selected-row flow and original-order criterion; R:7–15. |
| First revised Q3 | **PASS.** Final:5 preserves accepted intent/sole criterion, unapproved mechanism, and no implementation; current synchronous behavior appears in Q1. R:3–10, 14–26. |
| First revised Q4 | **PASS.** Final:7 preserves notifications and unagreed performance/row limits; Q5 explicitly preserves unagreed expiry duration. R:14–21. |
| First revised Q5 | **PASS.** Final:9 identifies Mira, unknown duration, recording the decision before implementation, and subsequent maintainers' mechanism choice; R:20–22. |
| Final Q1 | **PASS.** `readers/final-revision/final.md:1` identifies synchronous waiting and desired continuation/download; F:3–11. |
| Final Q2 | **PASS.** Final:3 describes the correct selected-row/original-order flow and distinguishes current synchronous generation; F:7–16. |
| Final Q3 | **PASS.** Final:5 preserves accepted outcome/sole criterion, Arun's unapproved queue/token proposal, and unavailable implementation/tests; Q2 supplies current behavior. F:3–8, 15–16, 23–32. |
| Final Q4 | **PASS.** Final:7 preserves notification exclusion and unagreed targets/caps without claiming they are expressly excluded; pending expiry appears in Q5. F:18–19, 25–26. |
| Final Q5 | **PASS.** Final:9 identifies Mira's unresolved expiry decision before implementation, followed by export-maintainer mechanism selection; F:25–30. No expiry value is invented. |

**Separate fidelity, orientation, disclosure, and output assessment.** Fidelity passes for all three edited artifacts: title, source/requirements/discussion references, row/column criterion, accepted/proposed/unimplemented distinctions, uncertainty, ownership, and checklist status survive. Final F:30 clarifies an owner already supplied by `discussion.md:6`, so preserving task meaning does not require literal preservation of the old checkbox wording.

Orientation **fails for the original description**, which opens with queue/token speculation at `baseline/before/remote-body.md:3–4` before the user problem and accepted outcome at 5–9. This is the unchanged oracle's declared defect. Orientation passes for B, R, and F at the lines cited for 18.1. The fixed tracker title remains unchanged even though it mentions a queue; exempting that read-only title from body-order assessment follows the title boundary, not a new exception.

Disclosure passes for every draft and completion message. `context.md:9–12` expressly authorizes the intended audience's access to requirements, discussion, and source. Drafts retain those relative references and no private source pointers, absolute workspace paths, or unsupported restricted facts. All three `final.md:1` messages link only their selected local output by absolute path; this is permitted by the supplied shared procedure:82–86 and accepted design:179–184. Completion messages disclose no additional private facts or pointers. This scenario contains no restricted-source negative fixture, so it cannot establish broader leak resistance.

Output scope passes for all variants: immutable title/body capture and all four other inputs remain unchanged, and only the authorized local draft is added. The visible completion messages report the path and pending decision briefly, without a separate ledger, extra summary artifact, remote update, or implementation.

**Applicability and limits.** Bug reproduction/environment and PR increment/runtime validation remain N/A for this unimplemented feature proposal, as fixed in `oracle/expected.json:8`; absence of those sections/evidence is not a failure. Runtime-test absence in F is a supported limitation, not a new validation prerequisite. The original-only reading path omits requirements' “no performance target or row cap” statement and discussion's maintainer ownership; the original reader cannot recover those source-only facts. Its supported notification answer and honest unknown owner remain passes, with no claim that it recovered the full source-enriched oracle wording. Edited artifacts do supply those facts. This applicability concern is recorded without changing any fixture, question, answer, or oracle.

No editor assertion or reader answer is graded FAIL/PARTIAL. The original orientation defect remains an explicit nonpass, separate from comprehension. No observed protocol defect invalidates a run. Encrypted dispatch transport and the inability to certify unobserved filesystem/session behavior remain limitations. Synthetic evidence does not certify a live Linear/GitHub connector, passing runtime behavior, universal human comprehension, or a causal benefit from the revised instructions. The final instruction change from the first revision is confined to PR-validation wording; this issue scenario already passes under the baseline and first-revised snapshots.
