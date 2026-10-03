# Brainstorm design review resolutions

> Reviewed: 2026-10-03
> Baseline: `ecee358` — Design brainstorm skill
> Scope: corroborate the two user-supplied reviews and revise the design package; skill implementation and evaluation execution remain pending.
> Documents: [design](design.md), [implementation](implementation.md), [tasks](tasks.md)

## Finding-by-finding disposition

| Finding | Verdict and corroboration | Resolution |
| --- | --- | --- |
| Review 1 F1: implicit selection with both skills available | **Valid, P2.** Baseline scenarios 1–7 expose only `brainstorm`; scenario 9 exposes `brainstorm` and `design` but explicitly invokes the latter. Neither proves implicit selection across the competing descriptions. | Scenario 1 now uses an ordinary technical-idea prompt with all relevant neighbors; scenario 9 uses an ordinary written-planning prompt with the same catalog. Both require canonical/generated loading traces and output-boundary evidence. |
| Review 2 P2: scenario 9 exercises explicit invocation | **Valid coverage gap; duplicate of part of F1.** The assertion that an explicit invocation “cannot fail” or “proves nothing” is too strong: it can still catch failure to honor a requested workflow, its gates, or its outputs. It does not establish description-based selection. No harness-specific determinism claim is needed for this conclusion. | Convert scenario 9 to implicit written planning and retain explicit invocation as scenario 11. |
| Review 2 P2: no positive implicit trigger; model is another neighbor | **Valid competing-catalog gap; premise partly overstated.** The baseline does not prescribe explicit invocations for every positive scenario; the exact prompts do not yet exist. Its decisive weakness is exposing only `brainstorm`. `/kk:model`'s actual description also covers domain concepts and questions before design, making it a relevant neighbor to expose. | Scenario 1 exposes `brainstorm`, `design`, `model`, and `implement`; scenario 12 guards requests for a durable domain kit. Discovery wording in design is explicitly in scope, with model-description changes allowed only on demonstrated routing collisions. Neighboring procedures stay unchanged. |
| Review 2 P2: multi-turn runbook unspecified | **Valid, P2.** The baseline names no filename or stable format. The inspected oracle inventory is JSON-only, with several naming patterns; no explicit multi-turn reply-script contract was found. The existing clarify-docs README supplies a manual staging/evidence precedent, not the missing turn protocol. | Specify `oracle/runbook.md`, fixed sections, ordered reply conditions, exact user replies, stopping rules, turn bounds, grading, and evidence. Require a self-contained `brainstorm/evals/README.md`; keep the existing `eval.json` schema and use manual execution. |
| Review 2 P3: knowledge-store search ambiguous | **Valid ambiguity, P3.** Read-only search is compatible with statelessness, but the baseline combines general read-only research with “no memory integration” without resolving whether search is included. Permitting it is a design option, not a necessary fix. | Explicitly exclude knowledge-store/session-vault searches in this version, preserving file/web research and the agreed absence of a memory integration. No Capy symlink is needed under this choice. |
| Review 2 P3: do not reopen decisions constrains unchanged design | **Valid, P3.** The baseline's cross-workflow instruction conflicts with preserving design's framing, foundation, and classification confirmations in `idea-process.md`. | Require a useful recap of settled decisions, rationale, and open assumptions. State that it supplies context without waiving the next workflow's gates. |
| Review 2 P3: omitted Codex README count | **Valid, P3.** `kodex-plugin/README.md` says “10 workflow skills.” `cmd/generate-kodex/main.go` regenerates skills, profiles, agents, and plugin metadata, not that README. A 14-to-15 replacement would miss it. | Add the hand-authored README to documentation and count reconciliation, checking the actual catalogs after the new skill exists. This plan correction does not prematurely change a live count to 15. |
| Review 2 P3: Task 1 size understates verification work | **Valid workload concern, P3.** The original task bundles ten authored scenarios and four existing regressions, with both source variants requested, while describing fixtures as mechanical. The work includes substantial test design and execution. An L task would violate repository task conventions, so merely retagging is insufficient. | Split into four M-sized tasks: core interview with three baseline scenarios; four evidence/revision cases; five routing cases plus four existing regressions; final documentation/checks. The revised baseline is 32 scenario/variant runs, excluding reruns. |

All eight entries have a documented resolution; the first three overlap in routing coverage rather than representing three unrelated defects. This confirms design-plan issues, not observed failures of an implemented brainstorm skill.

## Evidence anchors

- [Design discovery wording and conversational example](../../../../klaude-plugin/skills/design/SKILL.md).
- [Design confirmation gates](../../../../klaude-plugin/skills/design/idea-process.md).
- [Model discovery description and durable-kit outputs](../../../../klaude-plugin/skills/model/SKILL.md).
- [Existing manual eval guidance](../../../../klaude-plugin/skills/clarify-docs/evals/README.md).
- [Codex README](../../../../kodex-plugin/README.md) and [generation entry point](../../../../cmd/generate-kodex/main.go).
- [Shared Capy protocol](../../../../klaude-plugin/skills/_shared/capy-knowledge-protocol.md), inspected to distinguish search from indexing; it is not adopted by the new skill.

No reported issue is silently deferred. The future skill, fixtures, runbooks, and their execution remain explicit pending work in [tasks.md](tasks.md); this review-resolution pass changes the plan, not those runtime artifacts.

## Review of the revisions

An isolated code reviewer checked the four revised documents and supporting repository contracts. It found one additional P2 plan gap: execution of the four legacy design regressions lacked explicit ownership of the setup/reply scripts required by the new no-improvisation policy. This is addressed in implementation.md and Task 3.4–3.5: prepare bounded evaluator-only runbooks for all four regressions, including design selection, variant handling, fixture mappings, permitted writes, and stopping rules, then execute them without changing their original prompts or assertions.

The external PAL review with `gemini-3.1-pro-preview` returned no additional findings on the initial revision. Its no-issue response supplies no actionable review signal; the isolated review above identified the concrete follow-up correction. No systemic P0/P1 finding required knowledge-base indexing.

The isolated reviewer subsequently approved the targeted correction: legacy runbook preparation is owned by Task 3.4, execution by Task 3.5, and the 32-run baseline remains consistent. That follow-up reviewed the changed planning sections; it did not execute the future evaluations.

Validation of this documentation revision passed: `git diff --check`, 36 local file/heading links, scenario IDs 1–12, four pending task blocks, contiguous subtask IDs, and per-subtask verification markers. Runtime skills were not changed, generated, or evaluated in this correction pass.
