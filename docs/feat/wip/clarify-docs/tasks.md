# Tasks: comprehension-focused editing

> Design: [design.md](design.md)
> Implementation: [implementation.md](implementation.md)
> Issue: [#156](https://github.com/serpro69/claude-toolbox/issues/156)
> Status: in-progress — Tasks 1–2 done; Tasks 3–5 pending
> Created: 2026-09-29
> Not Doing: global brevity prompts, product/code changes, automatic publication, bulk cleanup, new profiles, eval harness, automatic standalone-implementation completion

## Review reconciliation

**Status:** done — findings assessed, design corrections applied, checks and independent follow-up review passed

[Assessment of both reports](review-assessment.md) records eight distinct issues
from nine findings, their evidence and dispositions. Task 1 implementation is now
complete. The optional isolated runtime verifier remains an explicitly owned
[deferred item](implementation.md#deferred-work), not a v1 acceptance requirement.

## Task 1: Clarify an existing local document from requirements and source

**Status:** done
**Depends on:** —
**Size:** M
**Can run in parallel with:** —
**Docs:** [Standalone editing](implementation.md#1-standalone-editing-of-local-documentation)

- [x] Create `klaude-plugin/skills/clarify-docs/SKILL.md`, `_shared/document-clarity.md` and the per-skill shared symlink. Define bounded inputs, mandatory instruction loading, source understanding, editing and verification → verify: a selected local document completes the workflow with all reader answers and protected meaning intact; new mandatory shared instructions meet the 1,000-word target / 1,200-word ceiling and the measured count is recorded.
- [x] Implement evidence-grounding rules for requirements versus current implementation, missing context and already-clear material → verify: supplied source is inspected when needed; disagreements remain explicit; an already-clear fixture has no gratuitous changes.
- [x] Add self-contained evals under `clarify-docs/evals/` for dense prose, source disagreement, missing context, cross-file preservation, no-op behavior and non-triggers → verify: expected claims stay outside staged `test-files/`; instruction targets receive an explicit `/kk:implement` suggestion without edits or automatic handoff.
- [x] Register the skill in `test/test-plugin-structure.sh`; document local use in `docs/user-guide/skills.md` and update `README.md` plus the other [named inventories](implementation.md#1-standalone-editing-of-local-documentation) → verify: current description-budget guidance is checked and maintained counts/catalogs reflect the new utility without inserting a mandatory pipeline stage.
- [x] Regenerate Codex output and run relevant structure/graph checks and behavioral evals → verify: generated entry point/shared references resolve and recorded eval results distinguish comprehension from fidelity.

**Verification:** [Task 1 evidence](verification.md) records 40/40 applicable
assertions passing across ten current scenarios, separate reader/fidelity grading,
the 820-word shared-instruction budget, stable generation and isolated review.
Two earlier partial source-disagreement attempts are preserved. Eight of nine shell
suites passed; two unchanged hook-test failures are documented with a follow-up
owner and next step. No claim of a fully green repository suite is made.

## Task 2: Clarify PR drafts without leaking private context

**Status:** done
**Depends on:** Task 1
**Size:** M
**Can run in parallel with:** Task 3
**Docs:** [PR drafts and visibility](implementation.md#2-pr-drafts-and-audience-boundaries)

- [x] Extend `clarify-docs/SKILL.md` and the shared procedure for local PR drafts and read-only remote inputs, with explicit output location rules → verify: editing produces a local draft and makes no external write.
- [x] Ground PR explanations in the actual base/head, diff, requirements and relevant code; distinguish current behavior from future integration → verify: contract-only and runtime fixtures produce accurate, distinct explanations and focused review paths.
- [x] Apply the design's ordered destination-visibility rules in the shared procedure → verify: declared-private and tracked-but-restricted fixtures do not leak, shared task references remain usable, and credential-only or unknown external access is not treated as audience access.
- [x] Add PR and privacy evals plus user-guide examples; regenerate Codex output → verify: assertions pass, shared prose stays single-sourced and structural checks remain green.

**Verification:** [Task 2 evidence](verification.md#task-2-verification) records
24/24 applicable assertions and 20/20 revised-reader answers passing across five
scenarios, with the first partial attempts preserved. Shared instructions total
1,000 words; generation is stable and isolated review is complete. Eight of nine
shell suites pass; the two pre-existing hook assertions still fail. Caller-only
absolute output links have a documented instruction-precedence limitation for
Task 4 to clarify; destination drafts contain no prohibited workspace pointers.

## Task 3: Apply the shared pass after design and documentation drafting

**Status:** pending
**Depends on:** Task 1
**Size:** M
**Can run in parallel with:** Task 2
**Docs:** [Workflow integration](implementation.md#3-reuse-in-existing-writing-workflows)

- [ ] Add `shared-document-clarity.md` symlinks in `design/` and `document/`; load the procedure in both `SKILL.md` files before subject-matter action → verify: summaries and detailed workflows agree on ordering.
- [ ] Update `design/idea-process.md` to edit the completed design/implementation/task artifacts and `design/existing-task-process.md` to edit only refined documents → verify: required sections, decisions, task state and links survive; unchanged resumes produce no rewrite.
- [ ] Add the post-draft pass to `document/SKILL.md` while retaining applicable profile rubrics → verify: one pass over invocation outputs, with no extra summary file or dropped required topic.
- [ ] Add consumer integration evals and user-guide coverage; retain `/kk:implement`'s existing plan-mode call chain → verify: instructions precede reads, editing follows drafting, and no recursive/duplicate pass or new standalone completion call appears; per-entry-point review limits are explicit.
- [ ] Regenerate Codex output and run structure/graph checks → verify: all consumer symlinks resolve and generated workflows match canonical behavior.

Task 2 and Task 3 can proceed independently after Task 1's shared contract is stable.
Coordinate shared-procedure changes; logical parallelism does not imply concurrent
edits to the same file are safe.

## Task 4: Execute comprehension and fidelity evaluations

**Status:** pending
**Depends on:** Task 1, Task 2, Task 3
**Size:** M
**Can run in parallel with:** —
**Docs:** [Fresh-reader protocol](implementation.md#fresh-reader-protocol)

- [ ] Create `verification.md` and `verification/<run-id>/<scenario>/` evidence as runs begin → verify: the index records date, model/version/settings, staged revision or hashes, artifact links and authored-versus-executed status for every scenario.
- [ ] Stage and execute the editor plus separate original/revised reader sessions and independent grading according to the protocol → verify: readers have no inherited author context or oracle, source-access traces are available, and each assertion has an evidence-backed PASS/FAIL/PARTIAL.
- [ ] Apply baseline-aware acceptance and fix discovered problems → verify: all applicable comprehension, correctness, fidelity, visibility, structure and orientation assertions pass; clear-prose fixtures still permit factual/privacy repairs; only a baseline meeting every applicable requirement requires no-op; affected evals are rerun after fixes.
- [ ] Record isolation limits and human-comprehension limits → verify: shared-filesystem leakage or missing evidence cannot yield a valid run, and AI-reader results are reported only as the evidence actually collected.

**Owned follow-up:** the feature maintainer must clarify caller-only output links
versus prohibited source pointers and add coverage, as described in the
[report-path limitation](verification.md#report-path-limitation).

## Task 5: Final verification and documentation

**Status:** pending
**Depends on:** Task 1, Task 2, Task 3, Task 4
**Size:** S
**Can run in parallel with:** —
**Docs:** [Release checks](implementation.md#release-checks)

- [ ] Run `/kk:test` for the full repository shell/Go checks, generation and graph validation → verify: required checks pass and repeat generation produces no further changes.
- [ ] Check Task 4's `verification.md` evidence against the final diff → verify: all applicable assertions pass at the applicable revision; rerun only evals invalidated by subsequent changes.
- [ ] Run `/kk:document` to finalize relevant user guidance and inventory updates → verify: standalone and automatic entry points, source prerequisites, output boundaries and limitations are clear.
- [ ] Run `/kk:review-code` with the active skill-markdown profile and `/kk:review-spec` against this design and implementation plan → verify: findings are fixed or durably recorded with an owner and next step; no unaddressed acceptance failure is labeled complete.
- [ ] Update feature status and record verification limits → verify: authored evals are not reported as executed and no claim of improved human comprehension exceeds the collected evidence.

## Dependency Graph

```text
Task 1 ─┬─→ Task 2 ─┬─→ Task 4 ─→ Task 5
        └─→ Task 3 ─┘
```
