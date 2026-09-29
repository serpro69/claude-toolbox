# Independent retry grading and applicability review

Grade the runtime-pr retry under /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/retry-1 independently. Also assess whether the focused shared-instruction change invalidates any of the other four previously passing PR evaluations.

Allowed read manifest:
- This request file.
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/contract-only-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-missing-context/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-unavailable-source/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/instructions/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/grading/verdicts.md

Read this entire rubric before subject matter. Each case includes scenario assertions/oracle, before/after/source snapshots, requests/manifests, actual model/settings metadata, real Git evidence, reader answers and full raw/readable tool traces. The retry has its own frozen instructions and their exact diff against the initial shared procedure. Do not read live staging, native session stores, other repository files or other cases.

For runtime-pr retry, give every assertion 12.1–12.6 PASS, FAIL or PARTIAL with evidence pointers. PARTIAL and missing evidence are not passes. Score all five original and revised reader answers against the unchanged oracle and report ORIGINAL→REVISED scores; one point requires a fully correct answer. Explicit unknowns are correct only where supported. Do not weaken expectations or use shorter prose as evidence. Check fidelity, review increment, protected semantics, validation limits, destination collision and local-only write scope independently from comprehension.

Audit each retry editor/reader read and write against its exact manifest. Confirm full frozen instructions precede subject reads, reader isolation from source/oracle/other versions, unchanged oracle/questions/fixtures/Git refs, hashes, tool call/result completeness and matching paired model settings. Missing traces or unallowed content reads invalidate the run. Shared filesystem controls are not OS isolation. Standard harness/AGENTS instructions remain in fresh sessions. Model build and temperature are unrecorded. Coordinator audits are evidence to inspect, not verdicts to adopt.

For prior contract-only-pr, destination-visibility, pr-missing-context and pr-unavailable-source, compare the exact old/new instruction text and the preserved initial evidence. Give each its own applicability verdict: RETAIN PASS, RERUN REQUIRED, or UNCERTAIN, with concrete rationale and evidence. Do not claim those four cases executed the updated instructions. If the change adds a relevant unmet obligation or undermines previous behavior, require a fresh run rather than assuming transfer. Distinguish a narrow correction from unrelated behavior, and preserve the initial runtime PARTIAL result as history.

Use no other skills, network or delegation. Do not edit any inputs. Write only /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/retry-1/grading/verdicts.md with native apply_patch. Include assertion and question tables, separate fidelity/isolation verdicts, prior-case applicability table, limitations, and concise counts. Return counts/path in final. Results describe observed AI reader behavior, not human comprehension.

