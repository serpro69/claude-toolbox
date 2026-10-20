# Isolated review agents retention

Archive the entire `docs/feat/done/isolated-review-agents/` directory, including
`.sessions/doc-design-session-v2.txt` (28,536 bytes).
Keep both generations of design/implementation/task records and `review/` in Git.

The v2 task record explicitly supersedes the v1 delta: v1 Tasks 1–7 were complete,
while its final verification remained pending. V2 is marked done and records
manual configuration/spec verification and a corrected stale reconciliation/
annotation description. Preserve that distinction; do not recast the old v1
pending record as a fresh passing test result.

The decision history moves from reconciliation/disposition to annotated findings
and keeps reviewer failure handling. Current reviewer roles, shared guidance and
isolated workflows remain maintained in the plugin and generated counterparts.
Historical skill names in these records retain their original meaning.

No executable runner or fixture dependency lives in the saved session.
Locator:
`payload/docs/feat/done/isolated-review-agents/.sessions/doc-design-session-v2.txt`.
The session is a later cleanup candidate; v1/v2 decisions and written review
reports should remain accessible in Git.
