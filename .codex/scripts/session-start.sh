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

## Sub-agents

Five custom agents available in .codex/agents/:
- code-reviewer: Reviews diffs for SOLID violations, security risks, code quality
- spec-reviewer: Compares implementation against design docs
- design-reviewer: Evaluates design docs for completeness and soundness
- eval-grader: Grades skill eval assertions against reviewer output
- profile-resolver: Resolves active profiles and checklist-load decisions for a diff
All agents run in read-only sandbox mode.

## capy — context-window protection

BLOCKED in shell: curl, wget, fetch('http, requests.get(, requests.post(, http.get(, http.request(
Use capy MCP tools instead: capy_fetch_and_index, capy_execute.

Shell is ONLY for short-output commands (git, mkdir, rm, mv, ls, npm install, pip install).
For everything else: capy_batch_execute or capy_execute(language: "shell", code: "...").

Tool hierarchy:
1. capy_batch_execute(commands, queries) — primary, runs all + auto-indexes
2. capy_search(queries) — follow-up queries on indexed content
3. capy_execute / capy_execute_file — sandbox execution
4. capy_fetch_and_index + capy_search — web content
5. capy_index — store content for later search
CONTEXT_EOF

# Inject repo-root-dependent paths
CONTEXT="${CONTEXT}

## Profile and shared-instruction paths

Profiles are at: ${REPO_ROOT}/klaude-plugin/profiles/
Shared skill instructions are at: ${REPO_ROOT}/klaude-plugin/skills/_shared/"

# Emit the JSON structure codex expects
printf '%s\n' "$(jq -n \
  --arg ctx "$CONTEXT" \
  '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $ctx
    }
  }')"
