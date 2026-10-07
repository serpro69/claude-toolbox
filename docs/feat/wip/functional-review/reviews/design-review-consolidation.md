# Consolidated design-review assessment

> Date: 2026-10-07
> Reviewed artifact: design package at b5401c30
> Inputs: two independent review reports supplied by the user in this conversation
> Scope: assess and repair the design/plan; operative implementation remains pending
> Revised package: [design](../design.md), [implementation](../implementation.md), [evaluation](../evaluation.md), [tasks](../tasks.md)

## Result

All 15 submitted observations were checked against the documents and relevant repository mechanisms. Fourteen warrant a design clarification or planned verification change; five of those recommendations need qualification. The remaining observation is a confirmed pre-existing registry collision, handled through explicit result identity without unrelated renumbering.

The P1 about evaluation binding is valid: a comparison against mixed instruction revisions would not support acceptance. The historical-source and grader-contract findings are also substantive. The reviews identified specification gaps, not proof that the implementation is currently defective: this feature has not been implemented.

The changes below fix the design-level gaps. They do not claim completed launcher probes, grader calibration, operative skill changes or a fresh independent design review.

## Consolidated findings and disposition

| ID | Original finding | Assessment | Resolution |
| --- | --- | --- | --- |
| D01 | Review A F1: independent historical-source access, P2 | Accepted. Revision labels and current files do not give shell-less reviewers the missing historical body. | [Readable historical evidence](../design.md#readable-historical-evidence) assigns parent materialization, provenance, evidence requests and equivalent PAL continuation input. R3 now requires a released implementation outside candidate files and PR hunks. Task 5 owns integration. |
| D02 | Review A F2: execution-evidence grader contract, P2 | Accepted. The existing grader explicitly excludes the needed trace/artifact inputs; a final claim cannot establish tool order. | [Workflow grading](../evaluation.md#execution-evidence-contract) adds an explicit mode with sealed tool events, dispatches and resulting files. Default component grading is preserved. Task 8 includes lying-final/missing-trace controls. |
| D03 | Review A F3: producer can finish before consumers, P2 | Accepted. The old Task 3/5 schedule could not substantiate completed isolated handoff. | New Task 6 depends on completed isolated consumers in Task 5; full comparison Task 12 is downstream of both. Parallelism is limited to independent later fixture groups. |
| D04 | Review B: baseline/candidate loading unspecified, P1 | Accepted. Root injection binds later reads, not necessarily the entry point or selected role. Intermediate baselines were also ambiguous. | [Provider-specific binding](../evaluation.md#bind-the-actual-instructions), loading probes and a single immutable c2d28c9e actor baseline. Tasks 1–2 precede all operative edits and capture all four invocation shapes. |
| D05 | Review B: ADR/AGENTS routing contradiction, P2 | Accepted with context. Existing content-based profile detection already strains the absolute wording, but that does not justify silently extending it. | Task 3 explicitly amends ADR 0004 and AGENTS.md before workflow edits, with a bounded predicate-only exception and conservative loading when undecidable. |
| D06 | Review B: seed fixture location/reuse unspecified, P2 | Accepted. Re-authoring a different fixture would invalidate paired comparisons. | Task 2 creates complete final eval directories, including metadata and oracles. Later tasks reuse them. [Fixture lifecycle](../evaluation.md#fixture-lifecycle-and-staging) defines history and hash continuity. |
| D07 | Review B: compatibility status/verdict mapping, P2 | Gap accepted; proposed blanket mapping narrowed. An incompatibility is not automatically P0/P1, and Unknown cannot always leave the verdict unchanged. | [Verdict table](../design.md#compatibility-and-release-assessment) distinguishes demonstrated defects, external prerequisites, material unknowns and unassessed environments. R3/R7 assert those distinctions. |
| D08 | Review B: no R8 injection mechanism, P2 | Gap accepted; choose a scoped phase replay. A disabled server tests failure only; an empty live manifest may be rejected and does not deterministically simulate underfed success. | [R8 replay](../evaluation.md#r8-controlled-report-phase-replay) supplies a controller-labeled synthetic result at the annotation/report checkpoint. It is explicitly a phase test; live PAL integration is separately required. |
| D09 | Review B: nondeterminism and undefined required assertions, P2 | Gap accepted; no eval schema expansion is necessary. A required flag duplicates a simpler all-assertions rule. Repetition is not statistical proof. | Every new assertions[] entry is required. Two fresh runs per side/mode, both passing for candidate acceptance; retain failures and state observed-twice limits. [Acceptance contract](../evaluation.md#comparison-identity-and-acceptance). |
| D10 | Review B: Task 4 undersized, P2 | Accepted. Plumbing, independent grading, many fixtures and a complete matrix were not one medium slice. | Split launch/baseline work, staging, grading, bounded fixture groups and matrix execution. The new 13-task graph also fixes D03. Task 5 remains M: four operative instruction files, no new evidence service or reviewer permission. |
| D11 | Review B: no always-loaded instruction budget, P2 | Useful preventive constraint; classify P3 rather than a demonstrated medium defect. Exact ceilings are a design choice, not a measured performance result. | 800 words for change-context.md and 1,200 for functional-review.md, complete-file counts. Deduplicate/move optional examples first; never truncate normative rules or hide excess in another always-loaded file. Structure checks enforce the chosen ceilings. |
| D12 | Review B: existing duplicate implement eval ID 4, P3 | Observation confirmed; unrelated renumbering rejected for this feature. Two existing scenarios use that ID, but their directory names differ. | New IDs exceed the existing maximum; aggregation keys include skill + eval name + assertion ID. Preserve historical IDs. Explicit maintenance note below supplies any future cleanup path. |
| D13 | Review B: PAL code-review branch does not exist, P3 | Accepted wording/implementation gap. The existing procedure is flat and also serves document review. | Say introduce explicit code/document branches, then extend only the code branch. Tasks 5/13 verify /kk:review-design compatibility. |
| D14 | Review B: implement writes its own specification, P3 | Risk accepted; editing a plan is not inherently wrong, and append-only prose alone would not establish authority. | Default to a labeled task Execution context for observations, proposals and decisions. Specification changes require explicit authorization/provenance. I4 checks that acceptance criteria are not silently rewritten. |
| D15 | Review B: no shared-file/symlink structure assertion, P3 | Accepted low-cost protection. Graph validation catches broken links but does not fully pin intended sharing and exact symlink targets. | Tasks 4/6 add canonical source/consumer checks as each consumer exists, plus generated parity and instruction budgets. Do not register a future link before its file exists. |

## Evidence and qualifications

- [code-reviewer](../../../../../klaude-plugin/agents/code-reviewer.md) has read/search tools and no shell. Its current payload supplies a diff and optional spec, so historical materialization is a genuine missing responsibility.
- [eval-grader](../../../../../klaude-plugin/agents/eval-grader.md) grades output text and explicitly excludes conversation history and live fixtures. The new workflow mode accepts selected observable events/artifacts, not private model reasoning or unrestricted source access.
- [ADR 0004](../../../../adr/0004-skill-workflow-ordering.md) and [AGENTS.md](../../../../../AGENTS.md) use absolute early-content prohibitions. The design must amend their contract explicitly while preserving the core ordering rule.
- [set-plugin-root.sh](../../../../../klaude-plugin/scripts/set-plugin-root.sh) prefers the registry resolver; [cpr.py](../../../../../klaude-plugin/scripts/cpr.py) already accepts CPR_PLUGINS_FILE, exercised by [test-cpr.sh](../../../../../test/test-cpr.sh). This is why a launch flag plus a shell root assertion is not enough for this repository.
- Official [Claude plugin loading](https://code.claude.com/docs/en/plugins/loading#name-conflicts) supports a revision-local --plugin-dir path subject to managed-policy precedence. The [Codex local-plugin documentation](https://developers.openai.com/plugins/build/plugins#install-a-local-plugin-manually) describes marketplace/project configuration and cache loading; generated role files also need explicit [project agent discovery](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).
- The local Claude CLI exposes --plugin-dir. A Codex CLI was not available on PATH in this revision session. No runtime eval was attempted; the design now specifies a launch probe and refuses to count a run whose binding is unproven.
- The [JS/TS](../../../../../klaude-plugin/skills/implement/evals/js-ts-standalone-loads-implement-guidance/eval.json) and [Python](../../../../../klaude-plugin/skills/implement/evals/python-new-file-loads-core/eval.json) scenarios both use ID 4. This is pre-existing and need not be repaired to identify new results unambiguously.

## Fresh-read follow-up

A subsequent fresh read of all five documents found two evaluation-isolation gaps. Both are now corrected in the design package; they are not deferred findings:

- The complete actor plugin tree included eval metadata and oracle files because the generator recursively copies skill directories. The launch contract now uses filtered actor bundles with unchanged operative bytes, explicit exclusion/retained-file manifests, cache scans and no links back to unfiltered input. Normal plugin packaging is unchanged. Task 1 verifies those controls before measured runs.
- Fresh sessions did not establish independent persistent state. The contract now requires a fresh subject repository and Capy store for every run, fixed empty or declared seed state, an unavailable synthetic-run vault, and a cross-probe marker check. In-run indexing remains enabled, but results cannot become another run's prior knowledge. Tasks 1, 2 and 12 capture and verify that isolation.

The core functional-review design and the original D01–D15 dispositions remain sound with these corrections. Implementation can start at Task 1; proving the specified runtime loading/isolation controls remains its acceptance criterion, not a claim that those probes have already passed.

## Deferred maintenance, outside feature scope

Owner: repository maintainer. Optional cleanup: make legacy numeric implement eval IDs unique by renumbering one duplicate and all of its assertion IDs, then update references and retained-result mappings. Deferred because this task repairs the functional-review design and historical result identifiers should not be changed casually. The concrete compatibility measure for this feature is composite result identity; this maintenance item is not a hidden acceptance dependency.

## Verification for this revision

Passed local Markdown target/anchor and whitespace checks across all five documents; validated 13 pending S/M tasks, dependency and parallel-marker consistency, per-subtask verification clauses, and one disposition for each D01–D15. The implementation producer depends on its isolated consumers, and final verification depends on every preceding task. Only the design package changed. Behavioral, generated-output and operative structure tests belong to the pending implementation tasks and were not run in this documentation revision.
