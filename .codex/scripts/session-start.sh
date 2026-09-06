#!/usr/bin/env bash
# SessionStart hook for Codex — injects provider context into the session.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

read -r -d '' CONTEXT <<'CONTEXT_EOF' || true
Provider: Codex (OpenAI).

## Tool-Name Mapping

Skills reference Claude Code tool names. Apply this mapping:
- Read → read_file
- Write → write_file
- Edit → apply_patch
- Bash → shell
- Grep → use shell with grep
- Glob → use shell with find
- WebSearch → web_search
- WebFetch → no equivalent; use capy_fetch_and_index via MCP
- Agent/Task → spawn subagents via natural language
- Skill → use $mention or /skills
CONTEXT_EOF

AGENTS_EXTRA_MD=""
if [[ -f "${REPO_ROOT}/.claude/CLAUDE.extra.md" ]]; then
  AGENTS_EXTRA_MD=$(cat "${REPO_ROOT}/.claude/CLAUDE.extra.md")
fi

# TODO: dynamically discover and append to AGENTS_EXTRA_MD
# any other existing ${REPO_ROOT}/.claude/CLAUDE.xxx.md files

AGENTS_CAPY_MD=""
if [[ -f "${REPO_ROOT}/.capy/AGENTS.md" ]]; then
  AGENTS_CAPY_MD=$(cat "${REPO_ROOT}/.capy/AGENTS.md")
fi

CONTEXT="${CONTEXT}

${AGENTS_EXTRA_MD}

${AGENTS_CAPY_MD}"

# Emit the JSON structure codex expects
printf '%s\n' "$(jq -n \
  --arg ctx "$CONTEXT" \
  '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $ctx
    }
  }')"
