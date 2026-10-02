# Verification

Status: complete; Tasks 1–3 finished 2026-10-01 and Task 4 finished 2026-10-02.

## Task 4 — complete extension verification

The maintained discovery and usage docs now cover issue inputs, local destinations,
evidence limits, audience restrictions and the implementation boundary. The
optional clarification workflow remains unchanged.

Final behavioral result: **133/133 assertions PASS**, with no FAIL, PARTIAL or
unrun cases. All 24 standalone scenarios and five current design/document consumer
scenarios have fresh editor runs, plus all 30 applicable original/revised readers.
Three independent fixture-capable graders audited the fixed assertions, artifacts,
prompts, manifests and complete visible traces. The
[aggregate verdicts](verification/task4-20261002/aggregate-verdicts.json) verify
every assertion ID exactly once within its skill/scenario and confirm that the
canonical eval and oracle hashes remain unchanged.

| Cohort | Scenarios | Assertions | Evidence |
| --- | ---: | ---: | --- |
| Existing local documents and routing, IDs 1–10 | 10 | 40 PASS | [Index and reader results](verification/task4-20261002/documents/README.md) |
| Existing PRs, IDs 11–15, plus current optional consumers | 10 | 46 PASS | [Index and independent grading](verification/task4-20261002/pr-consumers/README.md) |
| New issue cases, IDs 16–24 | 9 | 47 PASS | [Index and independent grading](verification/task4-20261002/issues/README.md) |

The [root evidence audit](verification/task4-20261002/checks/evidence-audit.json)
parsed 704 JSON files and 1,735 JSONL records across the completed packages,
rechecked all 12 verdict-file hashes, and found no malformed records, privileged
context records or ignored evidence files. The issue cohort's separate seal also
matches all 310 recorded file hashes and sizes. Each cohort links its own full
participant/grader access audit and source/fixture checks.

[Repository checks](verification/task4-20261002/checks.md) pass:
all nine shell suites, all Go tests, generation/freshness/idempotence and graph
validation. The network-dependent cases ran without skips. The initial sandbox
generation failure and approved successful rerun are preserved. The independent
source review [approves all 114 files](verification/task4-20261002/review.md)
without actionable findings; PAL's file-coverage limitation and conditional link
comment are retained with source-grounded context. The final
[spec review](verification/task4-20261002/reviews/spec-reviewer.md) is **CONFORMANT**,
with no findings, ambiguities or unverified acceptance items across all four tasks.
No systemic findings or intentional deviations require indexing.

The run starts at revision `9a501e1108b9083b83adbc6b550a18d0ff7b2b40` with the
operative 1,297-word procedure unchanged from Task 3. Evaluation coordinators own
separate `issues/`, `documents/` and `pr-consumers/` evidence trees. Exact prompts
are saved before dispatch; editors/readers receive only declared fixtures and
instruction files, with oracle access reserved for independent graders.

Invalid prompt-newline attempts and an interrupted first document grader are
preserved and excluded from acceptance. Instruction/metadata display truncations
were recovered by complete reads; earlier native prompt records closed short-window
capture gaps without reconstructing prompts. Repository exports retain visible
tool/message evidence and native provenance hashes while excluding harness
boilerplate and hidden reasoning. Git metadata is preserved losslessly in trackable
exports. No assertions, fixtures or operative instructions were changed to obtain
these results.

These are offline synthetic scenarios with model readers and audited manifests on
shared storage. They establish the stated scenario contracts, not OS isolation,
live tracker certification or general human-comprehension gains. Encrypted transport
remains opaque; exact pre-dispatch plaintext, hashes and receipts supply the
provenance required by the plan.

Task 4 is complete and the feature is archived under `docs/feat/done/`.
The final task needed no operative instruction, fixture or assertion changes.
Most verification effort went into exact prompt capture and portable, complete
evidence: newline mismatches, truncated displays and short capture windows needed
explicit recovery or fresh runs. These reinforced the existing evidence protocol;
they did not establish a new project convention or change the selected design.

## Task 3 — incomplete inputs and execution non-triggers

Final behavioral verdicts: **36/36 assertions PASS**, covering five new issue
scenarios and four required regressions. The operative shared procedure now matches
the complete preflight candidate byte-for-byte at **1,297 words**, within the
unchanged ceiling. SHA256:
`519f3fa45ae1954154aa292eff8e14abdcfadfb6b2e924214c2092b03a66d681`.
The entry point and its description are unchanged. The only operative addition is
the prepared 49-word distinction between missing body, missing supporting source
and unresolved destination; existing routing and output safeguards are retained.

| Scenario | Accepted final result | Evidence |
| --- | --- | --- |
| 20 issue-pasted-missing-destination | PASS 4/4 | [Gap grades](verification/task3-20261001/gaps/summary.json) |
| 21 issue-unavailable-source | PASS 7/7 | [Gap grades](verification/task3-20261001/gaps/summary.json) |
| 22 issue-unavailable-body | PASS 4/4 | [Gap grades](verification/task3-20261001/gaps/summary.json) |
| 23 issue-implement-non-trigger | PASS 4/4, clean-shell retry | [Routing runs](verification/task3-20261001/routing/run.md) |
| 24 issue-fix-non-trigger | PASS 4/4, clean-shell retry | [Routing runs](verification/task3-20261001/routing/run.md) |
| 9 code-non-trigger | PASS 3/3 | [Routing runs](verification/task3-20261001/routing/run.md) |
| 10 brevity-non-trigger | PASS 3/3 | [Routing runs](verification/task3-20261001/routing/run.md) |
| 14 pr-missing-context | PASS 3/3 | [PR runs](verification/task3-20261001/pr-regressions/run.md) |
| 15 pr-unavailable-source | PASS 4/4 | [PR runs](verification/task3-20261001/pr-regressions/run.md) |

[Gap runs](verification/task3-20261001/gaps/run.md),
[routing runs](verification/task3-20261001/routing/run.md) and
[PR runs](verification/task3-20261001/pr-regressions/run.md) retain the exact
pre-dispatch prompts, allowed-file manifests, instruction/fixture hashes,
before/after artifacts, actual model/settings, complete visible native traces,
dispatch linkage, fresh-reader answers and independent per-assertion grades.
Readers for scenario 21 and the revised PR 15 each recover all five supported
answers. Grader display caps followed by complete recovery are recorded separately
from participant trace completeness; missing evidence is not counted as passing.

All five new baseline editors finished before operative editing. Baseline 20.3
failed because the response offered an inline draft before destination selection;
the final run asks without drafting. Its unchanged assertion and original failure
are preserved. The other baseline assertions pass, establishing existing safeguards
without claiming a general causal advantage from these individual runs.

The first final routing grade has two PARTIALs, 23.4/24.4, because login-shell
startup attempted a denied unrelated log write. Fresh editors with neutral
non-login-shell setup and fresh independent grading pass all eight assertions.
Their fixtures, skill descriptions, instruction hashes and assertions are unchanged.
The first attempts, differing baseline assessment, failed dispatches and routine
tool failures remain available; the accepted final count uses the clean retries.

The [isolated source review](verification/task3-20261001/review.md) approves all
49 changed source/generated files with no P0–P3 findings. PAL returned no defects
but reported zero embedded/checked files; it supplies no independently established
file-backed corroboration. The review relies on the independent code-reviewer,
with the external requests/responses retained. No systemic findings or new project
conventions require indexing.

[Repository checks](verification/task3-20261001/checks.md) pass: all nine shell
suites, all Go packages, generation, exact canonical/generated parity, idempotence
and graph validation. This run also passes the three network-dependent template-sync
cases that prior tasks skipped. The existing graph cycle warning remains; no broken
links or orphan failures were introduced. New eval IDs 20–24 are unique and their
manifests/oracles validate. No source changes followed the reviewed revision.

These are offline synthetic cases on shared storage, audited by manifests and
traces rather than OS isolation. Native dispatch encryption limits independent
ciphertext/plaintext comparison; exact pre-dispatch plaintext and receipts remain.
Routing workspace names retain scenario labels and are not fully blind. Natural
requests and description-only skill selection remain intact. No live tracker
certification or general human-comprehension improvement is claimed.

Task 4 retains maintained usage documentation, the full behavioral matrix and final
spec review. No completed-feature history or automatic consumer invocation changed.

## Task 2 — feature proposals and intended audiences

Final behavioral verdicts: **25/25 assertions PASS**, covering both new issue
scenarios and the two required PR regressions. The final operative procedure is
1,248 words; the complete candidate is 1,297, within the unchanged 1,297-word
ceiling. Operative SHA256:
`9d102673879354a1f32caade6b9e0d8f04c8308487ea399285beccd6d55b8539`.
The entry point is unchanged. Both new scenarios also pass against the baseline;
these runs establish preservation and coverage, not a measured advantage over it.

| Scenario | Final result | Evidence |
| --- | --- | --- |
| 18 linear-issue-feature | PASS 6/6 | [Final independent grade](verification/task2-20261001/issues/linear-issue-feature/final-grading/report.md) |
| 19 issue-destination-visibility | PASS 6/6 | [Final independent grade](verification/task2-20261001/issues/issue-destination-visibility/final-grading/report.md) |
| 11 contract-only-pr | PASS 5/5 | [Final PR grade](verification/task2-20261001/regressions/final-grader-verdicts.md) |
| 13 destination-visibility | PASS 8/8 | [Final PR grade](verification/task2-20261001/regressions/final-grader-verdicts.md) |

[Issue runs](verification/task2-20261001/issues/run.md) and
[PR runs](verification/task2-20261001/regressions/run.md) index exact prompts,
settings, manifests, instruction/source hashes, before/after artifacts, native
visible traces, fresh-reader answers and independent grades. Grader read-coverage
audits distinguish capped batches followed by complete recovery reads from actual
missing required evidence. Shared storage is audited against manifests, not
described as filesystem isolation; encrypted transport remains a stated limitation.
Exact plaintext captured before dispatch, hashes and linked receipts establish
the required prompt provenance without claiming cryptographic transport proof.

The first PR visibility attempt failed unchanged assertion 13.8: it named JSON
parsing without stating the supplied successful outcome. A same-word-count PR
sentence now explicitly requires supplied outcomes in the draft. The complete
candidate was updated and checked before the operative change; fresh editors,
readers and graders reran all four scenarios on the final revision. The first
failure and all original artifacts remain preserved.

Independent code review found one P2 in new assertion 18.5: its broad command
prohibition could reject ordinary evidence reads. The
[versioned correction](verification/task2-20261001/eval-correction.md) explicitly
permits read/search operations while prohibiting execution of supplied source,
examples, reproduction commands or tests. Fixtures, questions and oracle answers
are unchanged. Fresh final graders applied the corrected assertion to all saved
variants without seeing earlier verdicts. The original Linear reader's scope
answer received different applicability assessments across graders; both reports
remain, and no editor assertion depends on that disagreement.

[Final source review](verification/task2-20261001/review-final.md): APPROVE, no
remaining findings. The external PAL reviewer failed after four 503 responses;
the isolated workflow's independent-reviewer fallback was used. No systemic P0/P1
finding or uncaptured project convention needs indexing.

[Repository checks](verification/task2-20261001/checks.md): all nine shell suites
and Go command-package tests pass; generation, final idempotence and graph checks
pass. Three unrelated network-dependent template-sync cases remain skipped for
Task 4 to rerun. Initial cache-access and Python/TOML failures and successful
retries are retained. Canonical/generated output matches, with no agent-file diff.

Tasks 3–4 retain gap/non-trigger scenarios, maintained usage documentation, the
complete behavioral matrix and final spec review. Task 1's bug routing, evidence,
output and audience rules are unchanged, so cases 16/17 were not rerun in Task 2.
Synthetic tracker fixtures do not certify live integrations.

## Task 1 — original completion record

Task 1 completed 2026-10-01, before Tasks 2–4 began. Repository start:
`283f8da4606db7b1ad109b597f193bc9c0399377`.

The [budget preflight](verification/budget/decision.md) covers all planned rules
before operative edits. The operative shared procedure is 1,191 words; the complete
candidate is 1,297, within the explicitly recorded 1,297-word ceiling. The entry
point is 616 words with a 449-character description.

| Scope | Authored | Executed / outcome |
| --- | --- | --- |
| 16 github-issue-bug | Yes | Revised PASS 7/7; baseline 5 PASS, 1 PARTIAL, 1 FAIL |
| 17 issue-local-draft | Yes | Revised and baseline PASS 5/5 under independently corrected oracle v2; initial PARTIAL retained |
| Existing dense-source | Existing | Clean retry VALID, PASS 5/5 |
| Existing runtime-pr | Existing | Clean retry VALID, PASS 6/6 |
| 18–24 and complete regression matrix | No new scenarios yet | Pending Tasks 2–4 |

Run records: [issues](verification/task1-20261001/issues/run.md),
[regressions](verification/task1-20261001/regressions/run.md),
[repository checks](verification/task1-20261001/checks.md),
[isolated code review](verification/task1-20261001/review.md).
All editor/reader/grader prompts are captured before dispatch. Isolation is an
allowed-file manifest plus trace audit on shared storage, not an OS sandbox.
Synthetic tracker responses provide no live connector certification.
All **23 applicable behavioral assertions pass** on the unchanged final operative
instruction hashes. Fresh revised readers recover all five answers in each case.

The GitHub baseline replaced the protected tracker title and used an unestablished
remote-reference mapping. The revised run preserves the title, accessible links,
older-version uncertainty, reproduction details and local collision protection.
Explicitly restricted facts stay absent from both its draft and completion report.

Scenario 17 initially required reader narration of the editor's own actions.
Independent code review and grader clarification identified this as an oracle
defect: issue scope and evidence limits belong in the draft; prohibited editor
actions are checked in the trace. The [versioned correction](verification/task1-20261001/oracle-correction.md)
changes only two expected answers. Original prompts, artifacts, traces, questions
and assertions are unchanged, and the original PARTIAL report remains available.
A fresh independent grader audited the corrected oracle against both versions.

The first PR smoke run refreshed its staged Git index during `git status`, so its
passing prose assertions did not establish a compliant read-only run. Retry harness
settings disable optional Git writes. Both smoke cases also use non-login shells
on retry to remove denied ambient logging attempts. Failed/qualified attempts are
retained alongside clean retries; none is silently replaced.
The final independent grader validates both clean retries, all 78 manifest hashes,
complete traces, instruction ordering, reader parity and oracle isolation. Runtime's
27 existing files, including its 20 Git metadata files, remain byte-identical;
exactly one draft was created. Dense-source changes only its selected guide.

All nine shell suites and all Go command-package tests pass. Three unrelated
network-dependent template-sync cases are skipped and recorded for Task 4's final
verification. Generation and graph validation pass. The initial isolated reviews
found no operative-code issues; the later P2 oracle finding is corrected with no
deferred review fix. No new project convention or systemic P0/P1 finding needs indexing.

Active implementation profiles: `skill-md` (entry point and skill-root adjacency),
`python` (new fixture source extensions). Loaded all three skill-md implement
checklists; Python contributes no implement phase. Neither active profile has a
test phase in the installed plugin. No dependency is added or changed.

Task 1 also applies coherent common audience wording and early context investigation
from the complete candidate. Dedicated proposal/audience/gap/non-trigger verification
and maintained usage docs remain assigned to Tasks 2–4; this does not complete them.
No frozen completed-feature documentation was edited.

Optional prose review: `/kk:clarify-docs docs/feat/wip/clarify-issue-descriptions/verification.md`.
This suggestion does not invoke clarification automatically.
