You are executing one isolated fixture request. Use only the frozen instruction package below as the operative plugin. Do not use the installed plugin copy.

## Plugin Root
/tmp/clarify-task4/instructions

Workspace: /tmp/clarify-task4/consumers/clarity-refined-documents-only/workspace
Start the explicitly requested skill at /tmp/clarify-task4/instructions/skills/design/SKILL.md. Resolve its linked instructions and profile paths within this package. This fixture contains no external knowledge service; .invalid URLs are simulated read-only responses. No network access.

## User request
Use /kk:design to refine only implementation.md for archive-label in docs/feat/wip/archive-label/. Make its implementation steps concrete using the accepted design; leave design.md and tasks.md unchanged. Stop at handoff, before implementation or independent review.

## Allowed reads
This request; the frozen /tmp/clarify-task4/instructions/skills/ and /tmp/clarify-task4/instructions/profiles/ instruction trees (no evals present); the files listed below and any documents you create within the user-authorized output scope. Directory/filename inspection is allowed within the workspace and frozen instruction package. Nothing outside these paths is permitted, including repository files, installed instructions, other runs, oracles, eval definitions or session transcripts.
- /tmp/clarify-task4/consumers/clarity-refined-documents-only/workspace/docs/feat/wip/archive-label/design.md
- /tmp/clarify-task4/consumers/clarity-refined-documents-only/workspace/docs/feat/wip/archive-label/implementation.md
- /tmp/clarify-task4/consumers/clarity-refined-documents-only/workspace/docs/feat/wip/archive-label/tasks.md

## Allowed writes
Only the selected output documents authorized by the request, under /tmp/clarify-task4/consumers/clarity-refined-documents-only/workspace/. Use native apply_patch for authored content. Do not mutate source fixtures outside that scope.
Do not spawn other agents. You are not alone in the shared filesystem; keep every action within this manifest and do not revert other work. Complete the user request and return your result as the final response.

