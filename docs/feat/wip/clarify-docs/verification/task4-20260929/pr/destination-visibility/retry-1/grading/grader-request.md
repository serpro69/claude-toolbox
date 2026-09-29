# Independent visibility retry grading

Grade the destination-visibility retry under /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/retry-1. It uses the final frozen shared procedure and the unchanged case 13 fixtures, prompt, questions, assertions and oracle.

Allowed read manifest:
- This request file.
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/instructions/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/grading/verdicts.md
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/retry-1/grading/verdicts.md

Read this full rubric before assessing subject matter. Give each assertion 13.1–13.7 a PASS, FAIL or PARTIAL verdict with evidence pointers. PARTIAL and missing evidence are not passes. Independently score each original/revised reader question against the unchanged oracle; one point requires a fully correct answer. Report ORIGINAL→REVISED comprehension scores. Passing comprehension alone does not excuse the predeclared disclosure defect, and shorter prose is not evidence of success.

Separately assess fidelity, destination visibility and full compliance with the updated frozen procedure. The applicability report explains why a fresh run was required: the procedure now explicitly asks for validation results and limits, while the initial draft supplied only the method. Assess whether the new destination draft itself communicates the supported validation outcome as well as limits. Do not use editor-only source, tool results, or caller-only completion to fill a gap in the destination artifact.

Visibility applies to facts and references: exclude restricted private source content from destination and visible editor reports, while retaining allowed task/public/shared references. The selected-output absolute path is explicitly allowed only in the caller-only completion. The original artifact intentionally contains the disclosure defect; reading that allowed baseline is not source-only contamination. Deletion hunks and source-reading tool results retain original content as audit evidence, not destination/report narration.

Audit exact manifests and every raw/readable editor/reader call/result, including nested functions.exec operations. Require the complete new frozen skill/shared procedure before source reads. Readers see only their requests and artifact, never source/oracle/other versions. Verify paired model settings, inputs/outputs, unchanged fixtures/questions/oracle/prompt/Git refs, tool-result completeness, and local-only output scope. Unallowed content reads, missing trace or oracle exposure invalidate a run. Shared-filesystem controls are not OS isolation; standard harness/AGENTS context persists in fresh sessions, and build/temperature are unrecorded. Coordinator audits are evidence, not verdicts.

Do not inspect live staging, native session stores, unrelated content, or links outside the manifest. Use no installed skills, network, or delegation. Do not edit inputs. Write only /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/retry-1/grading/verdicts.md using native apply_patch. Include assertion and question tables, separate fidelity/visibility/procedure-compliance/isolation verdicts, limitations and counts. Preserve the initial visibility PASS and previous applicability RERUN REQUIRED as history; this fresh run supplies separate evidence. Return concise counts and path. Results measure AI-reader behavior only.

