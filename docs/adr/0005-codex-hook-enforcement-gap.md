# ADR 0005: Codex Hook Enforcement Gap

## Status

Accepted

## Context

Claude Code enforces capy routing and file-path security policies via two
mechanisms: PreToolUse hooks (which intercept tool calls before execution)
and context injection (which provides advisory guidance). Both mechanisms
cover all tool types — Bash, Read, Write, Edit, WebFetch, etc.

Codex's hook system (experimental, behind `[features] codex_hooks = true`)
supports PreToolUse hooks, but with a significant limitation documented in
the Codex docs:

> Currently `PreToolUse` only supports Bash tool interception. The model can
> still work around this by writing its own script to disk and then running
> that script with Bash, so treat this as a useful guardrail rather than a
> complete enforcement boundary.

This means:

- `read_file`, `write_file`, `apply_patch`, `web_search`, and MCP tool
  calls **cannot be intercepted** by hooks.
- File-path denylist enforcement on `read_file` is not possible via hooks.
- WebFetch-equivalent blocking is moot (codex has no `web_fetch` tool),
  but `web_search` cannot be hooked either.
- MCP tool routing (e.g., blocking direct capy tool misuse) cannot be
  enforced.

The Codex docs explicitly mark this as "Work in progress" — expanded tool
coverage is expected in future releases.

## Decision

Accept the enforcement gap as a known limitation. Mitigate with a
two-layer approach:

1. **Hook enforcement (where available):** PreToolUse on Bash covers
   shell commands — curl/wget blocking, inline-HTTP patterns, and
   file-path denylist on shell commands (`cat .env`, `grep -r .terraform/`,
   etc.). This is the hard boundary.

2. **Advisory enforcement (everything else):** The SessionStart hook
   injects capy routing rules and file-path denylist guidance into the
   session context as `additionalContext`. The model is instructed to
   follow these rules. This is a soft boundary — the model may not
   always comply, but in practice LLM compliance with system-level
   instructions is high.

We do NOT:
- Build workarounds (e.g., wrapping `read_file` in a custom MCP tool
  that enforces the denylist). This adds complexity for a gap that codex
  itself will close.
- Block codex support on this gap. The advisory layer provides sufficient
  protection for the use cases we care about.
- Pretend the gap doesn't exist. It's documented in design.md §7.3,
  in the codex plugin README, and in this ADR.

## Consequences

- **Positive:** Codex support ships now rather than waiting for full hook
  coverage. Users get immediate value from skills, sub-agents, and capy
  MCP tools.
- **Positive:** The two-layer design is forward-compatible. When codex
  expands hook coverage, adding enforcement hooks for new tool types is
  additive — no architectural changes needed.
- **Negative:** A determined model (or a prompt injection) can bypass the
  advisory layer for non-Bash tools. This is the same risk profile as any
  system-prompt-based instruction.
- **Negative:** Parity gap with Claude's enforcement. Claude users have
  hard enforcement on all tools; codex users have hard enforcement on
  Bash only. This should be documented prominently so users understand
  the difference.
- **Action item:** When codex expands PreToolUse to cover `read_file`,
  `write_file`, `apply_patch`, and `web_search`, add corresponding hook
  entries to `.codex/hooks.json` and update this ADR's status.
