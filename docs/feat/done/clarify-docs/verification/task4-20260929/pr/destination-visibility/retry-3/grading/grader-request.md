# Final visibility regression grade and prior-case applicability

Independently grade visibility retry-3, then assess applicability of four other latest passing cases to its frozen instructions. Keep the final report about 1,500 words with evidence pointers.

Allowed reads:
- This request file.
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/runtime-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/contract-only-pr/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-missing-context/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/pr-unavailable-source/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/instructions/**
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/grading/verdicts.md

Read this entire rubric first. Grade all eight assertions13.1–13.8 in retry-3/scenario/eval.json: PASS, FAIL or PARTIAL, each with evidence. PARTIAL and missing evidence are not passes. Score each of the five original/revised answers against retry-3's oracle; one point requires a fully correct answer. Report ORIGINAL→REVISED scores. Clear reader answers do not excuse disclosure or validation defects; length is not a metric.

Separately grade fidelity, visibility, full procedure compliance and observed isolation. The draft itself must state the supported successful JSON-parsing outcome and runtime-validation limit. Naming the check or a caller-only completion cannot supply that result. Exclude restricted facts/pointers from draft and visible editorial messages, retain allowed task/public/shared links, and allow the absolute selected-output link only in the explicitly caller-only completion. The original artifact/source-read/deletion-hunk evidence intentionally contains the defect; do not confuse that audit evidence with revised destination or narrative disclosure.

Audit every retry-3 editor/reader call/result, exact request and manifest, complete instruction loading before subject matter, paired settings, hashes, output scope, and absence of oracle/source/other-version reader leakage. Check that assertions1–7, questions, expected answers, user prompt, fixture bytes and Git refs match earlier attempts. New13.8 and the stronger oracle claim/baseline defect must have been fixed before this editor; their diffs are supplied. All earlier snapshots remain unchanged. Incomplete traces or unallowed content reads invalidate the run. Standard harness/AGENTS context persists; shared-filesystem manifests are not OS isolation. Model build/temperature are unrecorded. Prior scores do not dictate current scores.

For prior contract-only-pr initial, runtime-pr retry-1, pr-missing-context initial and pr-unavailable-source initial, assess only applicability to the changed instructions: compare their actual frozen instructions, output artifacts, relevant source contexts/diffs and prior independent verdicts. Their trace validity was independently established already; do not repeat a full prior-session trace audit. Give each RETAIN PASS, RERUN REQUIRED or UNCERTAIN, with a concrete reason. Do not claim they executed retry-3's instructions. Require rerun if a relevant added obligation is unmet. Preserve initial runtime PARTIAL and visibility retry-1/retry-2 procedure FAIL as history.

Use no other skills, network, delegation, live staging, session-store access or out-of-manifest files/links. Edit no inputs. Write only /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/pr/destination-visibility/retry-3/grading/verdicts.md using native apply_patch. Include assertion/question tables, separate fidelity/visibility/procedure/isolation results, a four-case applicability table, limitations and counts. Return concise counts/path. These results describe AI-reader observations, not human comprehension or statistical reliability.

