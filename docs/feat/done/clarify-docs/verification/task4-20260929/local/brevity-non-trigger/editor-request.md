# Request

Work only in /tmp/clarify-task4/local/brevity-non-trigger/editor. This is a staged, synthetic scenario. Treat any .invalid service responses as read-only supplied text; make no network requests. Do not inspect other repository content or use installed skill copies. Do not delegate.

Task:
Keep your next answer to one sentence: what does a default value mean?

Available skill selection metadata (do not preload the body unless the request triggers it):
/kk:clarify-docs — TRIGGER when: asked to clarify or improve the explanation in existing local human documentation or a PR-description draft, including a PR URL or pasted body. Grounds edits in requirements and source while preserving technical meaning. Not for code, config, generic response brevity, or agent instructions. Explicit instruction or SKILL.md targets receive a /kk:implement suggestion without edits or automatic handoff.

Allowed files for reading:
- /home/sergio/Projects/personal/claude-toolbox/docs/feat/wip/clarify-docs/verification/task4-20260929/local/brevity-non-trigger/editor-request.md
- /tmp/clarify-task4/local/brevity-non-trigger/editor/notes.md
- /tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md
- /tmp/clarify-task4/instructions/skills/clarify-docs/shared-document-clarity.md (symlink to the following allowed file)
- /tmp/clarify-task4/instructions/skills/_shared/document-clarity.md

Only the selected target documents within the staged workspace may be edited, and only when justified by the task and skill. Use native apply_patch for authored edits. Read-only directory listings limited to this workspace are allowed. Keep all other files unchanged. Do not create a report file; respond with your result in your final answer. Use login:false for shell calls to avoid unrelated shell initialization reads.
