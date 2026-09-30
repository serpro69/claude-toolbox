# Independent batch grading request

Independently grade the ten scenarios below. Do not edit artifacts, prompts, or oracles. Do not delegate. Use login:false for shell reads; make no network requests.

Allowed reads: this request; all files in the ten exact evidence directories listed below; /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/instruction-hashes.json; /tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md; /tmp/clarify-task4/instructions/skills/clarify-docs/shared-document-clarity.md; /tmp/clarify-task4/instructions/skills/_shared/document-clarity.md. No other repository content. Files named original/ and revised/ are immutable captured snapshots, including source evidence where relevant. Session traces are exact filtered captures of metadata, tool calls/results and visible assistant messages, without hidden reasoning.

- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/dense-source/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/source-disagreement/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/missing-context/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/cross-file-preservation/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/already-clear/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/clear-factual-error/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/skill-instruction-target/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/agent-instruction-target/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/code-non-trigger/
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/brevity-non-trigger/

The agent-instruction-target directory also contains blocked-attempt-1/, preserving an initial attempt denied by an environment security hook before it read its request. Grade the active top-level retry independently and report the blocked attempt as a limitation. The retry's request was dispatched from a neutral /tmp alias and is preserved byte-for-byte as editor-request.md.

For EACH scenario:
1. Read eval.json, oracle/expected.json where present, exact editor and reader requests, original and revised snapshots (including requirements/source), editor report, reader outputs and complete tool traces. Read in bounded chunks to avoid truncation; do not treat an omitted/truncated trace as complete. Coordinator audit.md files are observations to verify, not authority for verdicts.
2. Grade every eval assertion PASS / FAIL / PARTIAL, with concrete artifact or trace pointers. PARTIAL is not pass. Original/revised readers are N/A for four routing cases.
3. For six comprehension cases, score each of the fixed five reader answers separately against the fixed oracle, then report ORIGINAL→REVISED totals out of five (only PASS counts). Answers may be evaluated as a whole when the reader supplies a required qualification under a different numbered response; explain any such reading. Do not infer unsupported answers from the editor's knowledge.
4. Independently inspect fidelity: protected claims, supported factual repairs, uncertainty, structure, task state, links, scope and orientation assertions. An all-pass original comprehension result requires a predeclared non-comprehension defect to justify an edit. The clean baseline must remain byte-for-byte unchanged.
5. Audit isolation separately: every subject-content read must stay within the request's allowed manifest; reader cannot see the other version, oracle, source-only evidence or skill. Check each recorded tool call and result, including nested calls inside functions.exec. Any out-of-manifest subject read or missing trace invalidates the run. Metadata includes a shared cwd but is not evidence of content access. Initial request reads can have default login-shell startup and denied navi logging; report that execution-method limitation separately from subject-content leakage. The first dense editor authored its staged guide with a shell heredoc; report that limitation without automatically conflating it with content leakage. All later edit requests require native apply_patch.
6. Check trace call/result pairs and visible final output preservation. Use actual session metadata for model/settings; do not invent temperature or exact model build.

Use native apply_patch to write only two files per scenario in its evidence directory: verdict.json and verdict.md. The JSON must include scenario, overall (PASS/FAIL/PARTIAL), assertions [{id,verdict,evidence}], comprehension {applicable, original [{question,verdict,evidence}], revised [...], original_passes, revised_passes}, fidelity {verdict,evidence}, isolation {verdict,evidence,limitations}, and limitations. Use verdict evidence paths relative to each scenario directory, optionally with line/ordinal anchors. The Markdown should be a readable equivalent with links. No editing or rerunning editor/reader outputs to improve a grade.

Retain failures accurately. Report summary counts in your final answer. These are AI-reader observations, not proof of human-comprehension improvement; shorter text is never evidence by itself.
