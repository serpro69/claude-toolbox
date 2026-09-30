You are executing one isolated fixture request. Use only the frozen instruction package below as the operative plugin. Do not use the installed plugin copy.

## Plugin Root
/tmp/clarify-task4/instructions

Workspace: /tmp/clarify-task4/consumers/clarity-after-drafting/workspace
Start the explicitly requested skill at /tmp/clarify-task4/instructions/skills/design/SKILL.md. Resolve its linked instructions and profile paths within this package. This fixture contains no external knowledge service; .invalid URLs are simulated read-only responses. No network access.

## User request
Use /kk:design to document the accepted archive-label idea in docs/feat/wip/archive-label/. The accepted decisions are in accepted.md; all refinement choices and the design presentation are approved, so proceed with drafting without reopening them. This is for the next contributor. Do not implement or run the recommended review.

## Allowed reads
This request; the frozen /tmp/clarify-task4/instructions/skills/ and /tmp/clarify-task4/instructions/profiles/ instruction trees (no evals present); the files listed below and any documents you create within the user-authorized output scope. Directory/filename inspection is allowed within the workspace and frozen instruction package. Nothing outside these paths is permitted, including repository files, installed instructions, other runs, oracles, eval definitions or session transcripts.
- /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/accepted.md

## Allowed writes
Only the selected output documents authorized by the request, under /tmp/clarify-task4/consumers/clarity-after-drafting/workspace/. Use native apply_patch for authored content. Do not mutate source fixtures outside that scope.
Observation-only recording: immediately after all selected draft documents exist and before any final clarity pass, copy those draft files preserving relative paths into /tmp/clarify-task4/consumers/clarity-after-drafting/draft-snapshot/. These copies are evidence, not extra product outputs; do not reread or edit the copies.

Do not spawn other agents. You are not alone in the shared filesystem; keep every action within this manifest and do not revert other work. Complete the user request and return your result as the final response.

