# ADR 0013: Codex File Access Runs Through Hooked Tools

## Status

Accepted, 2026-11-10. Supersedes [ADR 0005](0005-codex-hook-enforcement-gap.md)
and the "Codex native reads remain advisory" limitation in
[ADR 0012](0012-permission-guard-single-declaration.md).

## Context

ADR 0005 assumed Codex had a native `read_file` tool that PreToolUse hooks
could not intercept. On that basis the Codex integration treated secrets
protection for reads as advisory: `session-start.sh` injected the secrets
globs as policy text "because read_file may bypass tool hooks", and the Codex
provider doc listed native-read protection as a parity gap.

That premise does not hold for Codex as used here. Codex has no separate
file-read tool. It reads files by running shell commands such as `cat` through
`exec_command` (also reached from code mode via `functions.exec`). Those calls
arrive at PreToolUse as the canonical `Bash` tool, which `.codex/hooks.json`
routes to `pretooluse-bash.sh` and the shared guard engine. Writes arrive as
`apply_patch` (matched through the `Edit|Write` aliases) and capy execution as
MCP calls; both are already guarded (ADR 0012).

A probe on 2026-11-10 sent Codex-shaped payloads through the real adapters:
`cat ./kubeconfig.yaml` via `pretooluse-bash.sh`, an `apply_patch` adding
`deploy/admin.kubeconfig` via `pretooluse-patch.sh`, and `cat .kube/config` via
`capy_execute` and `pretooluse-mcp.sh` were all denied as secrets; benign
equivalents were allowed. This exercises the adapters and engine, not live hook
discovery or trust in a running Codex session.

## Decision

Treat the PreToolUse guard as the enforcement boundary for Codex file access,
with the same secrets declaration as Claude Code:

- Shell reads and commands (`exec_command`, code-mode shell): `pretooluse-bash.sh`.
- File mutations (`apply_patch`): `pretooluse-patch.sh`.
- Capy execution tools: `pretooluse-mcp.sh`.

Keep the session-start protected-files text, but as defense in depth rather
than as the mitigation for an unhookable read path. It tells the model up
front which paths are off limits, so it asks the user instead of attempting
and being denied.

Drop the pending action item from ADR 0005 to add a `read_file` hook; there is
no such tool to hook.

## Consequences

- Codex reads get the same hard enforcement as Claude Code's Bash calls, with
  the same limits: the guard inspects commands statically, so dynamically
  assembled paths can escape it. The parity gap row for native reads is removed
  from the Codex provider doc.
- The guarantee depends on hooks being registered, trusted and loaded, as
  described in the Codex provider doc. A passing adapter probe does not prove
  a live session invoked them.
- Channels outside the three adapters remain unguarded: hosted web search
  (not a file-access path), MCP tools from servers other than capy, and
  specialized `apply_patch` paths that bypass hooks. A new channel needs a
  payload mapping and registration before it has guard coverage, as ADR 0012
  already states.
- If a future Codex version adds a native file-read tool, this decision must
  be revisited: either map its payload in the guard and register a hook, or
  restore the advisory-only limitation in the provider doc.
