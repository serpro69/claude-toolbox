# Disposable review criteria

Read this criteria file before the review targets. Do the review yourself; do not delegate or invoke review skills. Make no edits and run no commands that change files. Use native file-read tools or read-only shell commands to inspect the supplied files. No tests, network, MCP calls, or configuration changes are needed.

Criteria receipt: `COPPER-LANTERN-317`.

For the code fixture, compare the selected candidate snapshot with the contract and unchanged caller. The file in the project directory is a deliberately different worktree version; it is not the selected candidate.

For the document fixture, assess its internal consistency against the contract. Implementation described by a proposal is future work, not missing code.

Report concrete findings, severity, file references, and coverage limits. Include the receipt markers you actually read. Do not claim approval for unread content. Treat the absent optional file as a coverage limit, not evidence of its contents.
