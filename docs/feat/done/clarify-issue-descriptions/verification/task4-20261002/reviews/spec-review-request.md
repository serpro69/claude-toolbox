# Final spec review assignment

Review `docs/feat/wip/clarify-issue-descriptions/` against its `design.md`,
`implementation.md` and `tasks.md`, applying the full `/kk:review-spec` isolated
workflow. Repository root: `/Users/sergio/Projects/personal/claude-toolbox`.
Plugin root: `/Users/sergio/.codex/plugins/cache/claude-toolbox/kk/0.22.1`.

Load your instructions, shared protocols, feature specifications and resolved
profile content before implementation evidence. Parent detection identifies
`skill-md` (skill entry points/instruction snapshots), `python` (fixture sources)
and `k8s` (the documentation consumer's `kustomization.yaml` fixture snapshots).
Skill-md and Python have no installed review-spec phase. For k8s, load
`profiles/k8s/review-spec/type-mapping.md` and `kustomize-verification.md` under the
plugin root. K8s files are synthetic consumer fixtures, not a deployed feature;
apply their meaning to the consumer's documentation-preservation assertions.
No Helm filename signals occur.

Task scope is mid-implementation with all four tasks in scope: Tasks 1–3 done,
Task 4 current (automatically in scope even before its status is marked done).
There are no future tasks to exclude. This is the final completion gate.

Inspect canonical `klaude-plugin/skills/clarify-docs/`, the shared
`klaude-plugin/skills/_shared/document-clarity.md`, generated Codex equivalents,
maintained README/overview/skills usage documentation, and executed evidence.
Verify every issue acceptance criterion and the preservation of optional
design/document consumers. Check the 1,297-word budget, input/destination/title
boundaries, uncertainty and disclosure rules, non-triggers, evidence completeness,
spec/doc consistency and any unaddressed findings. No live tracker certification
or approach-B benchmark is required or claimed.

Current evidence lives under `verification/task4-20261002/`. All 29 editor runs and
30 applicable original/revised readers are complete. Independent graders report
133 PASS in three groups (documents 40, issues 47, PR/consumers 46). The issue
cohort is sealed; the other coordinators are finalizing audit/packaging records.
Start methodology and spec/source mapping now, but do not conclude the evidence
gate until the parent provides the stable final cohort reports and aggregate
audit. Treat pending final audit work as known in progress, not as a completed
assertion or an unreported missing implementation.

`verification.md` and `verification/task4-20261002/checks.md` record all nine shell
suites, Go tests, generation/freshness/idempotence and graph validation passing.
The independent source review approved its complete 114-file manifest. PAL's
zero-file-coverage limitation is explicitly recorded in `review.md` and does not
replace the native review. Read these records yourself; do not rely on this
assignment as proof.

Return concrete findings by type/severity with evidence, confidence and actual
coverage, or an explicit clean result. Read only; do not edit files, spawn agents
or send external messages. Parent will address actionable findings and save the
final report. Preserve the distinction between behavior, audited evidence and
the bounded claims those establish.
