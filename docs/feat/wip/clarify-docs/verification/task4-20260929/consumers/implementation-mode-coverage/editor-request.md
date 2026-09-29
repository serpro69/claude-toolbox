You are executing one isolated fixture request. Use only the frozen instruction package below as the operative plugin. Do not use the installed plugin copy.

## Plugin Root
/tmp/clarify-task4/instructions

Workspace: /tmp/clarify-task4/consumers/implementation-mode-coverage/workspace
Start the explicitly requested skill at /tmp/clarify-task4/instructions/skills/implement/SKILL.md. Resolve its linked instructions and profile paths within this package. This fixture contains no external knowledge service; .invalid URLs are simulated read-only responses. No network access.

## User request
Using the supplied /kk:implement and /kk:document instructions, trace the remaining completion workflow for each case in completion-cases.md. Identify the automatic calls and clarity-pass count, and explain how a separate explicit documentation request would affect the standalone case. This is a read-only routing check; do not execute tests, reviews, documentation or implementation.

## Allowed reads
This request; the frozen /tmp/clarify-task4/instructions/skills/ and /tmp/clarify-task4/instructions/profiles/ instruction trees (no evals present); the files listed below and any documents you create within the user-authorized output scope. Directory/filename inspection is allowed within the workspace and frozen instruction package. Nothing outside these paths is permitted, including repository files, installed instructions, other runs, oracles, eval definitions or session transcripts.
- /tmp/clarify-task4/consumers/implementation-mode-coverage/workspace/completion-cases.md

## Allowed writes
None. Remain read-only.
Do not spawn other agents. You are not alone in the shared filesystem; keep every action within this manifest and do not revert other work. Complete the user request and return your result as the final response.

