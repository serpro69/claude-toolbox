# Request

Work only in /tmp/clarify-task4/local/agent-routing/editor. This is a staged, synthetic scenario. Treat any .invalid service responses as read-only supplied text; make no network requests. Do not inspect other repository content or use installed skill copies. Do not delegate.

Task:
/kk:clarify-docs AGENTS.md for clarity.

The explicitly requested skill is provided at:
/tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md

Allowed files for reading:
- /tmp/clarify-task4/local/agent-routing-request.md
- /tmp/clarify-task4/local/agent-routing/editor/AGENTS.md
- /tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md
- /tmp/clarify-task4/instructions/skills/clarify-docs/shared-document-clarity.md (symlink to the following allowed file)
- /tmp/clarify-task4/instructions/skills/_shared/document-clarity.md

Only the selected target documents within the staged workspace may be edited, and only when justified by the task and skill. Use native apply_patch for authored edits. Read-only directory listings limited to this workspace are allowed. Keep all other files unchanged. Do not create a report file; respond with your result in your final answer. Use login:false for shell calls to avoid unrelated shell initialization reads.

