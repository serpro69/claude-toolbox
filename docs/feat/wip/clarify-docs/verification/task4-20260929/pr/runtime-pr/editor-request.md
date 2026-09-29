# Editorial request

/kk:clarify-docs https://example.invalid/kitchen/pull/12 for repository reviewers. Work in the current feature docs/feat/wip/prep/. context.md contains the offline read-only PR response; use it and checkout/ without network access.

Workspace: /tmp/clarify-task4/pr/runtime-pr/editor

Use only the frozen skill at /tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md and its linked shared-document-clarity.md (resolved target /tmp/clarify-task4/instructions/skills/_shared/document-clarity.md). Load the full instructions before content-level artifact or source reads. Do not use installed skills.

Allowed read manifest:
- This request file.
- /tmp/clarify-task4/instructions/skills/clarify-docs/SKILL.md
- /tmp/clarify-task4/instructions/skills/clarify-docs/shared-document-clarity.md
- /tmp/clarify-task4/instructions/skills/_shared/document-clarity.md
- /tmp/clarify-task4/pr/runtime-pr/editor/context.md
- /tmp/clarify-task4/pr/runtime-pr/editor/remote-body.md
- /tmp/clarify-task4/pr/runtime-pr/editor/docs/feat/wip/prep/pr-draft.md
- /tmp/clarify-task4/pr/runtime-pr/editor/checkout/** including .git metadata, for read-only revision and source inspection.
- Your own authorized local output, if produced.

Only a selected local output within docs/feat/wip/prep/ may be written; existing fixture sources are read-only. Use native apply_patch for authored changes. Do not modify any Git repository or metadata. All .invalid URLs and supplied platform responses are synthetic, offline, and read-only: do not attempt network calls or external writes. Do not read any other files, repository instructions, evals, oracles, sessions, other cases, or reader artifacts. Do not delegate. Work independently until the authorized task is complete or a consequential missing answer must be requested. Return the caller-facing completion or question in your final message; write no auxiliary report.

