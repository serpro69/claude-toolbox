# Tasks: clarify issue descriptions

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#157](https://github.com/serpro69/claude-toolbox/issues/157)
> Status: done (all four tasks complete, 2026-10-02)
> Created: 2026-09-30
> Not Doing: remote publication/comments, issue implementation/reproduction, invented decisions/criteria, tracker-title editing, mandatory integrations/live certification, separate issue guide/new skill/profile, automatic clarification, bulk rewrites/extra summaries, completed-design edits

## Task 1: Clarify bug reports into local drafts

- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Slicing strategy:** Risk-First budget preflight, followed by the complete bug-report path.
- **Docs:** [Budget preflight](implementation.md#budget-preflight), [bug-report slice](implementation.md#task-1-clarify-bug-reports-locally), [request contract](design.md#request-and-output-contract)

### Subtasks

- [x] 1.1 Draft complete non-operative procedure and entry-point candidates for Tasks 1–3 under this feature's `verification/budget/`, including all planned rules and existing safeguards; remove duplication → verify: count the entire procedure and mandatory dependencies, record coverage and candidate hashes in `decision.md`, retain 1,200 if sufficient or explicitly raise the ceiling to the measured candidate count with justification, all before operative edits or candidate behavioral grading.
- [x] 1.2 Author `github-issue-bug` and `issue-local-draft` under `klaude-plugin/skills/clarify-docs/evals/`, with isolated grader oracles → verify: scenario IDs 16/17 are unique, scenario 16 covers a private same-repository issue without a caller-declared audience and protects the original title, manifests are self-contained, and baseline runs record observed routing/evidence/file effects.
- [x] 1.3 Apply the candidate's entry-point changes to `klaude-plugin/skills/clarify-docs/SKILL.md` for issue-description inputs, read-only tracker titles, and explicit implement/fix non-triggers → verify: preserve existing scope/loading rules and recheck current description guidance and measured length.
- [x] 1.4 Apply the candidate's issue evidence, bug-report preservation, and bounded GitHub same-repository audience default to `klaude-plugin/skills/_shared/document-clarity.md` → verify: scenarios 16/17 preserve reported versus verified behavior, reproduction details, local output, and collision protection; scenario 16 needs no audience question solely for privacy, retains accessible R references, and excludes explicitly restricted tracked facts.
- [x] 1.5 Extend `clarify-docs/evals/README.md` with offline issue staging → verify: both scenarios run without live tracker access, oracle leakage, or PR base/head setup.
- [x] 1.6 Check operative and complete-candidate instruction counts against the recorded ceiling; run `make generate-kodex` and `make plugin-graph`, inspect generated changes, and run `dense-source`/`runtime-pr` smoke regressions → verify: both counts fit, structural checks pass, all applicable behavioral assertions pass with recorded evidence.

Completed 2026-10-01. [Verification and evidence](verification.md): 23 behavioral
assertions pass across the two new scenarios and two regressions; required reviews,
generation and repository checks are recorded. Original failures and the independently
reviewed oracle correction remain available.

## Task 2: Clarify unimplemented features for the intended audience

- **Status:** done
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Proposal slice](implementation.md#task-2-clarify-proposals-for-their-actual-audience), [audience rules](design.md#audience-and-incomplete-context)

### Subtasks

- [x] 2.1 Author `linear-issue-feature` and `issue-destination-visibility` evals, IDs 18/19 → verify: baseline evidence records existing behavior; oracles separate accepted intent, proposals, unknown decisions, and actual audience access; scenario 18 forbids title changes or replacement-title suggestions.
- [x] 2.2 Apply the preflight candidate's shared-procedure feature/other-issue guidance → verify: scenario 18 preserves existing criteria and unknowns without demanding implementation, inventing criteria, or imposing bug-report sections.
- [x] 2.3 Scope PR-head visibility to its existing audience, retain Task 1's same-repository default, and apply common sharing rules outside that default → verify: scenario 19's declared different audience overrides the default, retains shared references, and excludes restricted facts/pointers from the draft and report, including uncited paraphrases.
- [x] 2.4 Regenerate Codex output, count operative and complete-candidate instructions against the recorded ceiling, and run structure/graph checks plus `contract-only-pr`/`destination-visibility` regressions → verify: both counts fit and all applicable assertions pass; repeat the full preflight before any ceiling increase and rerun 16/17 when changed rules affect them.

Completed 2026-10-01. [Verification and evidence](verification.md#task-2--feature-proposals-and-intended-audiences):
25 final behavioral assertions pass; generated output, structure/graph checks,
all shell suites and Go tests pass (three unrelated network cases remain skipped).
The independent source review approves the final change; PAL was unavailable.
The first PR validation-outcome failure, the corrected eval wording and complete
trace/coverage audits are preserved. Operative/candidate counts are 1,248/1,297
against the unchanged 1,297-word ceiling. Task 3 is next.

## Task 3: Handle incomplete inputs and execution non-triggers

- **Status:** done
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Gap and routing slice](implementation.md#task-3-handle-gaps-and-keep-execution-requests-out), [eval matrix](implementation.md#evaluation-matrix)

### Subtasks

- [x] 3.1 Author `issue-pasted-missing-destination`, `issue-unavailable-source`, and `issue-unavailable-body` evals, IDs 20–22 → verify: respectively ask before writing, produce a qualified draft, and request missing body text without fabricated output.
- [x] 3.2 Apply the preflight candidate's remaining entry-point/shared gap-handling rules, refining them where the cases reveal omissions → verify: accessible context is investigated first; input captures and unrelated files remain unchanged; unresolved claims retain next steps and known/unknown ownership.
- [x] 3.3 Author separate `issue-implement-non-trigger` and `issue-fix-non-trigger` evals, IDs 23/24, with ordinary execution requests and small source fixtures; expose only the skill description for selection → verify: normal fixture handling does not load editorial instructions, edit issue text, or create an editorial draft; do not prime the agent with classification-only prompts.
- [x] 3.4 Regenerate and run instruction-size/structure/graph checks and applicable existing missing-context/non-trigger regressions → verify: all assertions pass with complete traces and the complete procedure fits the recorded ceiling; repeat the full preflight before any ceiling increase.

Completed 2026-10-01. [Verification and evidence](verification.md#task-3--incomplete-inputs-and-execution-non-triggers):
36 final assertions pass across five new scenarios and four regressions. The
operative procedure equals the complete 1,297-word candidate; the ceiling and entry
point are unchanged. Generation/parity/idempotence, graph validation, all nine shell
suites and all Go tests pass, including the previously skipped network cases.
Independent source review approves; PAL's file-coverage limitation is recorded.
The baseline inline-draft failure and first routing PARTIALs remain preserved;
clean-shell retries pass without changing fixtures, assertions or skill instructions.
Task 4 is next.

## Task 4: Document and verify the complete extension

- **Status:** done
- **Depends on:** Task 1, Task 2, Task 3
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [Final verification](implementation.md#task-4-document-usage-and-verify-the-complete-extension), [evidence protocol](implementation.md#execution-and-evidence-protocol), [repository checks](implementation.md#repository-checks)

### Subtasks

- [x] 4.1 Run `/kk:document` to update `README.md`, `docs/getting-started/overview.md`, and `docs/user-guide/skills.md` → verify: documented issue examples, local output, gaps, disclosure, and implementation boundaries match the design and preserve optional clarification.
- [x] 4.2 Execute all nine new scenarios, all fifteen current standalone scenarios, and the five current design/document consumer scenarios listed in the implementation plan → verify: every applicable assertion passes on the final instructions, with fresh-reader comparison where applicable and no leaked or incomplete traces.
- [x] 4.3 Maintain this feature's `verification.md` and `verification/<run-id>/` evidence as runs occur → verify: exact prompts/settings, hashes/manifests, traces, reader answers, failures and per-assertion verdicts are linked; authored-but-unrun cases remain explicitly incomplete.
- [x] 4.4 Run `/kk:test` over all shell suites, generation, graph validation, and Go tests → verify: each outcome is recorded, generation is idempotent, and intended generated changes are distinguished from drift.
- [x] 4.5 Run `/kk:review-code` for Markdown skill instructions, JSON eval specifications, and generated Codex content → verify: resolve findings or record remaining work durably with owner and next action; do not relax acceptance to close the task.
- [x] 4.6 Run `/kk:review-spec` against all three design artifacts → verify: implementation, docs, generated output, and executed evidence cover every issue acceptance criterion before marking the feature complete.

Completed 2026-10-02. [Final verification](verification.md#task-4--complete-extension-verification):
all 29 scenarios and 133 fixed assertions pass, with 29 fresh editors, 30 readers
and independent grading. All nine shell suites (604 assertions), all Go tests,
generation/freshness/idempotence and graph validation pass. Source review approves
all 114 files; final spec review is conformant with no findings or unverified
acceptance items. Usage documentation is updated and optional clarification is
preserved. No operative instructions, fixtures or assertions changed in Task 4.

## Dependency Graph

```text
Task 1 ──→ Task 2 ──→ Task 3 ──→ Task 4
   └───────────────────────────→ Task 4
             └─────────────────→ Task 4
```
