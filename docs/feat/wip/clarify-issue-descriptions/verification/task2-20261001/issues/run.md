# Task 2 issue evaluation evidence

Final result: scenarios 18 and 19 each pass **6/6 assertions** against the final
operative instruction revision, for **12/12 final assertions**. Fresh final graders
also pass all baseline and first-revised assertions: **36/36 across the three
variants**. All fourteen editor/reader runs satisfy the accepted evidence protocol.
Initial reports, their applicability clarifications and every artifact remain
preserved separately; no observed editor nonpass was discarded.

Cases 18 and 19 use fresh default agents with `fork_turns=none` and no model or
effort overrides. Native baseline settings are `gpt-6-astra`, effort `max`.
The editor request and read/write manifest were saved before each dispatch.
Inputs are staged outside any SKILL.md ancestor under `/tmp/clarify-issue-task2/issues/`.
Eval specifications and oracles are absent from editor and reader workspaces.

Baseline instruction hashes:

- Entry point: `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`
- Shared procedure: `858630c27477ce3e2d39dc42ae72b17eab3e94ceb2f06b97ca10b2aacbe5dfb0`

Both baseline editors finished before operative Task 2 changes. Their complete
visible native traces, final messages, initial/output snapshots and hashes are
preserved in the respective `baseline/` directories. The coordinator notified the
parent with `BASELINES COMPLETE` after capture. Both produced a local draft;
observed outputs preserve the central meaning and remove restricted content.
Initial independent reader/fidelity grading confirmed these observations.

Revised instruction hashes, frozen after the parent's readiness notification:

- Entry point: `1d63b6ed88d7a96257c6ab6471d6763d9df7f33da29b49f50fa26f642584a189`
- Shared procedure: `cb06c670408be43198453ae324471661be22dfb325e862c6b25300c5ef894ecd`

The parent subsequently changed only the shared procedure's PR-validation
sentence. To establish evidence against the exact final operative revision,
fresh issue editors and fresh output readers ran again, preserving the first
revised runs unchanged. The final shared-procedure hash is
`9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539`;
the entry-point hash is unchanged. These runs are under `final-revision/` and
`readers/final-revision/`. Original readers are reused because their artifact
bytes, questions and settings are identical across comparisons.

| Scenario | Initial baseline grade | Initial first-revised grade | Final-revision grade |
| --- | --- | --- | --- |
| 18 — Linear feature | 6 PASS | 6 PASS | 6 PASS |
| 19 — destination visibility | 6 PASS | 6 PASS | 6 PASS |

Final independent reports: [scenario 18](linear-issue-feature/final-grading/report.md)
and [scenario 19](issue-destination-visibility/final-grading/report.md). Each fresh
grader re-audited all three editors and all four readers without access to prior
grading reports. They found no missing required fields, invalidating access leaks,
incomplete tool/result/final capture, forbidden actions or altered source inputs.
All eight readers receive 5/5 in the final grading (40/40 answers), subject to the
explicit original-reader applicability distinction below. Every edited reader
receives 5/5 under both initial and final grading.

The initial reports are [scenario 18](linear-issue-feature/grading/report.md) and
[scenario 19](issue-destination-visibility/grading/report.md). Both editors already
passed under the baseline instructions. The Linear original reader has one Q4
PARTIAL because the original description omits the unagreed performance/row-cap
details; both initial edited readers answer all five questions. All three initial
visibility readers answer 5/5 despite the original artifact's disclosure defect.
The reports distinguish comprehension, fidelity, orientation, disclosure and scope.
The fresh final Linear grader awards the original Q4 PASS for its artifact-supported
notification exclusion, while recording that performance/row-cap details are
unavailable along that original reading path. The initial literal-inventory PARTIAL
remains intact; questions, expected answers and reader response never changed.
This is a recorded grading applicability difference, not an editor improvement or
an oracle correction. Both graders pass every edited answer. The original Linear
orientation defect and original visibility disclosure defect remain separate
nonpasses, repaired by every editor variant. These runs establish no measured
advantage of revised instructions over the already passing baseline.

Both initial reports labeled experiment provenance INCOMPLETE because encrypted
dispatch messages could not be independently bound to saved plaintext. Separate,
pre-saved applicability follow-ups supplied the accepted protocol without changing
any original report, grade or artifact. Both graders then found no missing,
inconsistent or reconstructed mandatory evidence. Their
[Linear clarification](linear-issue-feature/grading-clarification/clarification.md)
and [visibility clarification](issue-destination-visibility/grading-clarification/clarification.md)
explain that cryptographic transport proof exceeds the specified capture/trace
protocol. The stronger transport limitation remains explicit.

The parent independently corrected assertion 18.5's ambiguous blanket phrase
“command execution” to distinguish editorial reads/searches from execution of
supplied source, examples, reproduction commands or tests. The correction preceded
receipt of any grading outcomes. The original frozen spec remains `eval.json`;
the [corrected spec](linear-issue-feature/spec-v2/eval.json),
[rationale](linear-issue-feature/spec-v2/rationale.md) and
[change check](linear-issue-feature/spec-v2/correction-check.json) are separate.
Only 18.5 changed; the scenario request, oracle, reader questions, fixtures and
instructions did not change for this correction. Corrected spec SHA-256:
`8af70b82ae8750f7c3b35002fd7a527d9695e57b8f28781624d57f486cd3d597`.
The initial Linear grader had interpreted the phrase as subject-command execution
and awarded PASS, explicitly recording that an absolute no-shell reading would
conflict with necessary evidence reads. Fresh final graders audited all preserved
variants against the corrected/current specs, with no access to prior grades.

Every submission's exact plaintext prompt was authored with `apply_patch` before
dispatch. Native dispatch receipts record its hash, save time, submitted settings,
call ID and resulting agent path. Native payload encryption prevents an independent
ciphertext/plaintext equality proof; it does not replace the saved exact prompt.
The accepted protocol snapshot is [implementation.md](protocol/implementation.md).
`dispatches.jsonl` and `dispatch-receipts.json` index fresh agent submissions;
each clarification has its separate follow-up dispatch record. Scenario-level
`dispatches-final.jsonl` and receipts contain only editor/reader submissions.

All source fixtures, initial/output artifacts, hashes, settings, raw calls/results
and visible final messages are preserved per run. [Integrity checks](integrity-final.json)
verify identical source inputs, exact fixed reader questions, unchanged reader
artifacts and final instruction identity. The first `integrity-check.json` files
retain their pre-correction observations. Exported editor/reader results contain
no truncation marker. Native filtering copied raw JSONL records and omitted hidden
reasoning; one-off capture helpers remain outside the repository under `/tmp/`.

The completed evidence covers **18 fresh default-agent sessions**: six editors,
eight readers and four graders, plus two saved follow-up turns to the initial
graders. [Session index](session-index.json) records all twenty captured turns,
actual settings and trace hashes. Every session uses `gpt-6-astra`, effort `max`,
without an override; fresh sessions use `fork_turns=none`. All 102 exported outer
tool calls have matching results and all twenty captured turns contain visible
final messages. The two follow-up traces begin after their original captured
completion timestamps and do not overwrite or duplicate the original traces.
The final graders' own visible commands were checked against their manifests:
only declared evidence/protocol reads, bounded metadata checks and their authorized
report writes occur; neither reads an earlier grade. The visibility grader's
absence check for `spec-v2/` implements the conditional instruction in its prompt.
The [grader coverage audit](grader-coverage.md) records three capped grader batches:
required content was retained or reread before verdict, and remaining omitted
background is outside the requested protocol section. Participant traces are
complete; no additional grading turn or participant rerun was needed.

[Observed verdicts](observed-verdicts.json) keeps initial and final results distinct.
The work here changes only this evidence directory and its `/tmp/` staging; parent
task status and operative instruction changes remain the parent's responsibility.

Synthetic tracker responses establish no live connector compatibility. Shared
filesystem access is controlled by manifests and audited traces, not OS isolation.
Native JSONL exports exclude hidden reasoning and system boilerplate while keeping
complete raw tool calls/results and visible assistant messages.
