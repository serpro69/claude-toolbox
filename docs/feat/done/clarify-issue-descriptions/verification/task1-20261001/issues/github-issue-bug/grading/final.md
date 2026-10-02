The revised version **PASSes all seven assertions**. The baseline **FAILs overall**: it replaces the protected title and only partially satisfies reference preservation. Both editor runs and all three reader runs have valid visible access and tool-trace evidence.

All paths below are relative to `issues/github-issue-bug/`.

| Run | Access and trace validity | Evidence |
|---|---|---|
| Baseline editor | **VALID** | `baseline/trace.jsonl` contains five matched calls/results and a final response. Lines 3–4 load both complete instruction files; subject reads begin at lines 5–6. Reads cover exactly the six permitted fixtures, a permitted directory listing, and its own output. |
| Revised editor | **VALID** | `revised/trace.jsonl` contains five matched calls/results and a final response. Lines 3–4 load both complete instruction files before the six permitted subject reads at lines 5–6. It lists the destination, creates one output, then corrects links in that newly created output. |
| Original reader | **VALID** | `readers/original/trace.jsonl:2–3` contains its sole call/result: reading the permitted `remote-body.md`. No linked source, other file, write, or network access appears. |
| Baseline reader | **VALID** | `readers/baseline/trace.jsonl:2–3` contains its sole call/result: reading the permitted draft. No other subject access or mutation appears. |
| Revised reader | **VALID** | `readers/revised/trace.jsonl:2–3` contains its sole call/result: reading the permitted draft. No other subject access or mutation appears. |

I checked the actual calls and results, rather than relying on the editors’ completion claims. Instruction and fixture content appears completely in the corresponding results, with no truncation. Reader results contain their complete permitted artifacts, and their saved answers match the trace finals. No evaluation metadata or oracle reads appear.

Recomputed hashes match both editors’ before/after manifests. Every pre-existing subject file remains byte-identical, including the remote capture, sources, context, and colliding draft. Each editor creates exactly `docs/feat/wip/replay/issue-42-draft.md`; neither deletes files. Reader artifact hashes match their manifests and the corresponding original/editor outputs.

The initial login shells emit a denied shell-startup logging diagnostic. This is not a subject-content read or successful outside-scope write; it supplies no evaluation material. These are shared-filesystem runs audited through visible evidence, not OS-isolated executions.

All three readers have identical actual settings: `gpt-6-astra`, `xhigh`, OpenAI provider, default role, CLI `0.159.3`, identical working directory, approval policy, and sandbox configuration. Submission records specify `fork_turns: none`. Their tool-output budgets differ, but every artifact was returned in full.

**Reader comprehension against the fixed oracle**

| Oracle question | Original | Baseline | Revised |
|---|---|---|---|
| 1. Why does this issue exist? | **PASS** — identifies duplicate receipts and operator uncertainty about repeated processing. | **PASS** — same purpose, with timeout/version context. | **PASS** — same purpose, preserving the distinction between receipts and actual duplicate processing. |
| 2. Reported example and expectation? | **PASS** — supplies command, environment, seed, timeout, frequency, and two versus one receipts. | **PASS** — identifies the same case and expected result across answers 1–2; abbreviates the command to its options. | **PASS** — supplies command, environment, seed, first-receipt timeout, frequency, and expected result. |
| 3. Verified, reported, or unknown? | **PARTIAL against the full oracle** — correctly identifies reported observation, suspected causes, pending reproduction, and untested 1.5.0. It cannot supply the inspected-source behavior or revision limits absent from its artifact. | **PASS** — explains suppression through `seen_receipts`, distinguishes 1.5.0 inspection from 1.4.2 reporting, and preserves unresolved cause/fix status. | **PASS** — makes those distinctions and explicitly states that reproduction was not independently verified and no tests ran. |
| 4. Outside scope? | **PASS** — UI excluded; no delivered fix. | **PASS** — UI excluded; no delivered fix or accepted implementation/new threshold. | **PASS** — preserves those exclusions and status. |
| 5. Next step and owner? | **PASS** — Bea repeats 1.4.2 with receipt logging. | **PASS** — same owner/action; task remains open. | **PASS** — same owner/action; distinguishes completed environment capture from outstanding reproduction. |

These grades use `readers/{original,baseline,revised}/final.md` and their matching trace finals.

The original reader demonstrates **no misunderstanding of the information actually present**. Its partial third answer reflects missing source context in the original artifact. Both edits repair the declared ordering defect—implementation speculation preceding purpose and reproduction—and explain the current source’s revision and evidentiary limits. This supports an orientation and information-completeness improvement, not a claim that the original reader failed to understand the operator problem.

**Fixed assertions**

| ID | Baseline | Revised |
|---|---|---|
| **16.1** | **PASS.** The draft leads with duplicate receipts and operator impact, then reproduction, before “Investigation and limits.” Its reader answers the five applicable questions correctly. | **PASS.** “Problem” and “Reported reproduction” precede “Evidence and investigation.” Its reader answers all five questions, including source limits. |
| **16.2** | **PASS.** The draft retains the exact command, `job-42`, QueueKit 1.4.2, Linux x86_64, 250 ms, 2 of 5, and one expected versus two observed. It identifies causes as leads and explicitly rejects extrapolating 1.5.0 inspection into proof of 1.4.2 behavior or a fix. | **PASS.** The same protected details and qualifications remain, with explicit reported-observation and no-tests language. |
| **16.3** | **PARTIAL.** No privacy-driven audience question or caveat appears; restricted facts and pointers are absent from the draft and final report. However, the editor replaces supplied local references with constructed remote URLs ending in `/blob/5c814d7/requirements.md` and `/replay.py`. The fixture does not establish that remote path mapping. Accessible reference retention is therefore not fully demonstrated; this is not a claim that a live link was tested and failed. | **PASS.** No privacy-driven question/caveat or restricted disclosure appears. The two adjusted relative links resolve within the saved snapshot to the supplied requirements and source files. |
| **16.4** | **PASS.** Recomputed snapshots show exactly one new draft and unchanged protected files. The trace contains no network request, publishing, reproduction execution, implementation edit, or extra report/ledger. | **PASS.** Same result. Its additional write corrects links only in its newly created draft. |
| **16.5** | **PASS.** Full skill/procedure results precede all subject content. The trace inspects context, requirements, and current source without PR setup or a whole-feature audit. | **PASS.** The same ordering and bounded inspection are evidenced directly. |
| **16.6** | **FAIL.** The output replaces `REPLAY broken?? retries????` with `Duplicate receipts when replaying a completed job on QueueKit 1.4.2`. `baseline/trace.jsonl:10–13` proves the replacement was authored and retained. | **PASS.** The draft preserves the supplied title verbatim; no replacement is proposed in the artifact or visible messages. |
| **16.7** | **PASS.** Bea’s pending 1.4.2 reproduction, receipt logging, undecided cause, UI exclusion, and both original checkbox states remain. No acceptance criterion, confirmed cause, test pass, or completion is invented. | **PASS.** The same facts and task states remain; no unsupported completion or implementation claim appears. |

**Overall:** baseline **FAIL** — five PASS, one PARTIAL, one FAIL. Revised **PASS** — seven PASS. These are synthetic offline behavioral results; they provide no live connector certification.
