# Independent evaluation grading

Independently grade these five manual editorial evaluation runs: contract-only-pr (11), runtime-pr (12), destination-visibility (13), pr-missing-context (14), pr-unavailable-source (15).

Allowed read manifest:
- This request file.
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/contract-only-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-missing-context/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-unavailable-source/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/instructions/**

Each case includes the eval assertions and oracle under scenario/, frozen source fixtures and before/after snapshots, exact role requests and spawns, original/revised artifacts and reader answers where applicable, actual Git refs/diff where available, model/settings metadata and raw/readable editor/reader traces. Do not read live staging, session stores, unrelated repository material, or other cases.

Before assessing subject matter, read this complete rubric. Give every assertion its own PASS, FAIL, or PARTIAL verdict with concrete evidence pointers. PARTIAL and missing evidence are not passes. Judge the actual assertion without weakening it. Use the oracle for source-backed expected answers. Give ORIGINAL→REVISED comprehension scores out of five for each applicable case, and separate question-level verdicts. An answer may be explicitly unknown when the oracle requires uncertainty. Case 14 has no reader comparison. A passing baseline can still require repair of the predeclared disclosure defect; a shorter draft is never evidence of success.

Audit fidelity separately from comprehension: protected meaning, contract/runtime boundaries, review increment, missing evidence and next owner/action, destination visibility, audience-accessible references, output scope, and validation limits. For case 13 inspect the destination draft and all visible editor messages, distinguishing its explicitly allowed caller-only selected-output link from prohibited private source pointers/facts. Its original artifact intentionally contains restricted details as the defect being measured.

Audit isolation and trace completeness separately: each editor must have fully read frozen skill plus shared procedure before source reads; editors may read only their declared manifests. Each reader may read only its request and supplied artifact, with no source-only context/oracle/other version. Check tool calls and results including nested functions.exec calls. Any out-of-manifest content read, missing trace, or oracle exposure invalidates the run. Prompt restrictions are shared-filesystem controls, not OS isolation. System/AGENTS harness context remains available in fresh sessions; no inherited conversation was forked. Model and effort must agree for paired readers; temperature/build are unrecorded. Check hashes/changed-file records against snapshots, and do not infer running tests from inspecting source or supplied validation records.

The coordinator's audit is evidence to inspect, not a verdict to adopt. You have no authorship role. Do not use the installed eval-grader agent or other skills, delegate, use network, or edit inputs. You may write only /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/grading/verdicts.md using native apply_patch. Include an overall validity/verdict and explicit limitations for each case, an assertion table, comprehension comparison and separate fidelity/isolation outcomes. Return concise counts and the verdict path in your final message. These runs measure AI reader behavior only; make no human-comprehension claim.

