#!/usr/bin/env bash
# Test suite for the Codex session hook and Bash, patch and MCP adapters.
# behaviour with and without capy's own Codex hooks registered in hooks.json.
# See: https://github.com/serpro69/claude-toolbox/issues/170
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# =============================================================================
# Fixtures
# =============================================================================

# Explicit legacy fixture: the live repository may already have Capy installed.
# Derive registered/partial cases from this fixture, never the user's setup.
TOOLBOX_HOOKS=$(cat "$SCRIPT_DIR/fixtures/toolbox-only-hooks.json")

# A realistic capy entry. `capy setup --platform codex` (capy >= v0.17.1) writes
# a `bash -c` wrapper whose body invokes `capy codex-launch`; that token is what
# the toolbox scripts detect on.
capy_entry() {
  local event="$1"
  jq -n --arg event "$event" '{
    matcher: "^.*$",
    hooks: [{
      type: "command",
      command: ("bash '"'"'-c'"'"' '"'"'capy_run command capy codex-launch \"$0\" \"$1\" \"$2\" \"$3\"'"'"' '"'"'capy-codex-launch-v2'"'"' '"'"'d54275171f475eb00dbb2e4f0bb33489'"'"' '"'"'hook'"'"' '"'"'" + $event + "'"'"'")
    }]
  }'
}

# Toolbox entries plus capy entries for both events (the state after
# `capy setup --platform codex` ran and preserved toolbox's hooks).
CAPY_HOOKS=$(jq \
  --argjson ss "$(capy_entry sessionstart)" \
  --argjson pt "$(capy_entry pretooluse)" \
  '.hooks.SessionStart += [$ss] | .hooks.PreToolUse += [$pt]' <<<"$TOOLBOX_HOOKS")

# Capy registered for SessionStart only — exercises per-event detection.
PARTIAL_HOOKS=$(jq --argjson ss "$(capy_entry sessionstart)" \
  '.hooks.SessionStart += [$ss]' <<<"$TOOLBOX_HOOKS")

# Capy registered for PreToolUse only — the mirror case.
PARTIAL_PT_HOOKS=$(jq --argjson pt "$(capy_entry pretooluse)" \
  '.hooks.PreToolUse += [$pt]' <<<"$TOOLBOX_HOOKS")

# Build a disposable project root containing both scripts, marker files for
# each injected source, and the given hooks.json content (omit for no file).
make_project() {
  local root
  root=$(create_temp_dir "codex-hooks")
  mkdir -p "$root/.codex/scripts" "$root/.capy" "$root/.claude" "$root/home" "$root/sub"
  cp "$REPO_ROOT/.codex/scripts/session-start.sh" \
    "$REPO_ROOT/.codex/scripts/"pretooluse-*.sh "$root/.codex/scripts/"
  cp -R "$REPO_ROOT/.codex/scripts/guard" "$root/.codex/scripts/"
  echo "capy-agents-marker-content" >"$root/.capy/AGENTS.md"
  echo "extra-marker-content" >"$root/.claude/CLAUDE.extra.md"
  if [[ $# -gt 0 ]]; then
    printf '%s\n' "$1" >"$root/.codex/hooks.json"
  fi
  echo "$root"
}

session_context() {
  bash "$1/.codex/scripts/session-start.sh" </dev/null | jq -r '.hookSpecificOutput.additionalContext'
}

# run_adapter <project_root> <adapter> <payload>; inspect, never execute payloads.
run_adapter() {
  set +e
  PRE_OUTPUT=$(printf '%s' "$3" | HOME="$1/home" \
    KK_GUARD_PROJECT_CONFIG="$1/no-project-config" KK_GUARD_USER_CONFIG="$1/no-user-config" \
    bash "$1/.codex/scripts/pretooluse-$2.sh" 2>"$1/stderr")
  PRE_EXIT=$?
  set -e
  PRE_ERROR=$(cat "$1/stderr")
}

run_pretooluse() {
  run_adapter "$1" bash "$(jq -n --arg c "$2" --arg cwd "${3:-$1}" \
    '{tool_name: "Bash", cwd: $cwd, tool_input: {command: $c}}')"
}

assert_denied() {
  local needle="$1" message="$2"
  assert_equals "2" "$PRE_EXIT" "$message: exit code is 2"
  assert_not_equals "" "$PRE_ERROR" "$message: stderr names the reason"
  assert_json_valid "$PRE_OUTPUT" "$message: deny output is valid JSON"
  assert_json_field "$PRE_OUTPUT" '.hookSpecificOutput.permissionDecision' "deny" "$message: permissionDecision is deny"
  local reason
  reason=$(echo "$PRE_OUTPUT" | jq -r '.hookSpecificOutput.permissionDecisionReason')
  if [[ "$reason" == *"$needle"* ]]; then
    log_pass "$message: reason mentions '$needle'"
  else
    log_fail "$message: reason should mention '$needle' (got: $reason)"
  fi
}

assert_allowed() {
  local message="$1"
  assert_equals "0" "$PRE_EXIT" "$message: exit code is 0"
  assert_equals "" "$PRE_OUTPUT" "$message: no stdout (pass-through)"
}

# =============================================================================
# Section 1: session-start.sh — legacy (capy hooks not registered)
# =============================================================================

log_section "Section 1: session-start.sh — legacy (capy hooks not registered)"

log_test "Toolbox-only hooks.json injects .capy/AGENTS.md"
legacy_root=$(make_project "$TOOLBOX_HOOKS")
ctx=$(session_context "$legacy_root")
if [[ "$ctx" == *"capy-agents-marker-content"* ]]; then
  log_pass ".capy/AGENTS.md is injected"
else
  log_fail ".capy/AGENTS.md should be injected when capy hooks are not registered"
fi
if [[ "$ctx" != *"Capy guidance and HTTP routing are delivered by the capy hooks"* ]]; then
  log_pass "deferral note is absent"
else
  log_fail "deferral note should not appear when capy hooks are not registered"
fi

log_test "Missing hooks.json falls back to legacy injection"
nofile_root=$(make_project)
ctx=$(session_context "$nofile_root")
if [[ "$ctx" == *"capy-agents-marker-content"* ]]; then
  log_pass ".capy/AGENTS.md is injected without hooks.json"
else
  log_fail ".capy/AGENTS.md should be injected when hooks.json is absent"
fi

log_test "Malformed hooks.json falls back to legacy injection"
broken_root=$(make_project '{"hooks": {"SessionStart": [')
ctx=$(session_context "$broken_root")
if [[ "$ctx" == *"capy-agents-marker-content"* ]]; then
  log_pass ".capy/AGENTS.md is injected with malformed hooks.json"
else
  log_fail ".capy/AGENTS.md should be injected when hooks.json is malformed"
fi

# =============================================================================
# Section 2: session-start.sh — capy hooks registered
# =============================================================================

log_section "Section 2: session-start.sh — capy hooks registered"

log_test "Capy SessionStart entry suppresses .capy/AGENTS.md injection"
capy_root=$(make_project "$CAPY_HOOKS")
ctx=$(session_context "$capy_root")
if [[ "$ctx" != *"capy-agents-marker-content"* ]]; then
  log_pass ".capy/AGENTS.md is not injected"
else
  log_fail ".capy/AGENTS.md should not be injected when capy's SessionStart hook is registered"
fi

log_test "Deferral note replaces the injection"
if [[ "$ctx" == *"Capy guidance and HTTP routing are delivered by the capy hooks"* && "$ctx" == *".codex/hooks.json"* ]]; then
  log_pass "deferral note names hooks.json as the source"
else
  log_fail "deferral note should state that capy hooks own guidance and routing"
fi

log_test "Provider instructions and extras are preserved in both modes"
for root in "$legacy_root" "$capy_root"; do
  ctx=$(session_context "$root")
  if [[ "$ctx" == *"Provider: Codex"* && "$ctx" == *"Tool-Name Mapping"* ]]; then
    log_pass "provider block present ($(basename "$root"))"
  else
    log_fail "provider block missing ($(basename "$root"))"
  fi
  if [[ "$ctx" == *"extra-marker-content"* ]]; then
    log_pass ".claude/CLAUDE.extra.md present ($(basename "$root"))"
  else
    log_fail ".claude/CLAUDE.extra.md missing ($(basename "$root"))"
  fi
  if [[ "$ctx" == *"Protected files:"* && "$ctx" == *"./**/.env"* && "$ctx" == *"~/.ssh/**"* ]]; then
    log_pass "current secrets declaration in advisory ($(basename "$root"))"
  else
    log_fail "protected-files advisory missing ($(basename "$root"))"
  fi
done

log_test "Output is valid SessionStart JSON in both modes"
for root in "$legacy_root" "$capy_root"; do
  out=$(bash "$root/.codex/scripts/session-start.sh" </dev/null)
  assert_json_valid "$out" "session-start.sh output is valid JSON ($(basename "$root"))"
  assert_json_field "$out" '.hookSpecificOutput.hookEventName' "SessionStart" "hookEventName is SessionStart ($(basename "$root"))"
done

# =============================================================================
# Section 3: pretooluse-bash.sh — legacy (capy hooks not registered)
# =============================================================================

log_section "Section 3: pretooluse-bash.sh — legacy (capy hooks not registered)"

log_test "Legacy: curl is denied"
run_pretooluse "$legacy_root" "curl -s https://example.com"
assert_denied "curl" "legacy curl"

log_test "Legacy: wget is denied"
run_pretooluse "$legacy_root" "wget https://example.com/file.tar.gz"
assert_denied "wget" "legacy wget"

log_test "Legacy: inline HTTP is denied"
run_pretooluse "$legacy_root" "python3 -c \"import requests; requests.get('https://example.com')\""
assert_denied "requests.get(" "legacy inline HTTP"

log_test "Legacy: shared guard applies"
run_pretooluse "$legacy_root" "cat .env"
assert_denied "kk guard: secrets" "legacy secrets"

log_test "Legacy: safe command passes through"
run_pretooluse "$legacy_root" "ls /tmp"
assert_allowed "legacy safe command"

log_test "Missing hooks.json keeps HTTP routing"
run_pretooluse "$nofile_root" "curl -s https://example.com"
assert_denied "curl" "no hooks.json curl"

log_test "Malformed hooks.json keeps HTTP routing"
run_pretooluse "$broken_root" "curl -s https://example.com"
assert_denied "curl" "malformed hooks.json curl"

# =============================================================================
# Section 4: pretooluse-bash.sh — capy hooks registered
# =============================================================================

log_section "Section 4: pretooluse-bash.sh — capy hooks registered"

log_test "Capy PreToolUse entry lets curl through to capy's hook"
run_pretooluse "$capy_root" "curl -s https://example.com"
assert_allowed "capy curl"

log_test "Capy PreToolUse entry lets wget through"
run_pretooluse "$capy_root" "wget https://example.com/file.tar.gz"
assert_allowed "capy wget"

log_test "Capy PreToolUse entry lets inline HTTP through"
run_pretooluse "$capy_root" "python3 -c \"import requests; requests.get('https://example.com')\""
assert_allowed "capy inline HTTP"

log_test "Shared guard still applies when capy hooks are registered"
run_pretooluse "$capy_root" "cat .env"
assert_denied "kk guard: secrets" "capy secrets"
run_pretooluse "$capy_root" "grep -r secret .terraform/"
assert_denied ".terraform" "capy denylist terraform"

log_test "Safe command still passes through"
run_pretooluse "$capy_root" "ls /tmp"
assert_allowed "capy safe command"

# =============================================================================
# Section 5: per-event detection
# =============================================================================

log_section "Section 5: per-event detection"

log_test "Capy SessionStart-only entry defers guidance but keeps HTTP routing"
partial_root=$(make_project "$PARTIAL_HOOKS")
ctx=$(session_context "$partial_root")
if [[ "$ctx" != *"capy-agents-marker-content"* ]]; then
  log_pass "guidance deferred (SessionStart entry present)"
else
  log_fail "guidance should be deferred when capy's SessionStart entry is present"
fi
run_pretooluse "$partial_root" "curl -s https://example.com"
assert_denied "curl" "partial curl (no capy PreToolUse entry)"

log_test "Capy PreToolUse-only entry defers HTTP routing but keeps guidance injection"
partial_pt_root=$(make_project "$PARTIAL_PT_HOOKS")
ctx=$(session_context "$partial_pt_root")
if [[ "$ctx" == *"capy-agents-marker-content"* ]]; then
  log_pass "guidance still injected (no capy SessionStart entry)"
else
  log_fail "guidance should still be injected when only capy's PreToolUse entry is present"
fi
run_pretooluse "$partial_pt_root" "curl -s https://example.com"
assert_allowed "partial-pt curl (capy PreToolUse entry present)"

# =============================================================================
# Section 6: shared guard channels and failure boundaries
# =============================================================================

log_section "Section 6: shared guard channels and failure boundaries"

log_test "Subdirectory Bash cwd retains the project policy anchor"
run_pretooluse "$capy_root" "cat ../.env" "$capy_root/sub"
assert_denied "kk guard: secrets" "subdirectory secret"
run_pretooluse "$capy_root" "cat ../README.md" "$capy_root/sub"
assert_allowed "subdirectory ordinary read"

log_test "Former substring false positives are allowed"
for command in 'cat .env.example' 'cat build/out.txt' "find . -not -path './.git/*'"; do
  run_pretooluse "$legacy_root" "$command"
  assert_allowed "$command"
done

patch_payload() {
  jq -n --arg cwd "$1/sub" --arg patch "$2" \
    '{tool_name: "apply_patch", cwd: $cwd, tool_input: {command: $patch}}'
}

log_test "Patch checks secrets, ordinary edits and selfmod from a subdirectory"
run_adapter "$capy_root" patch "$(patch_payload "$capy_root" $'*** Begin Patch\n*** Update File: ../.env\n@@\n-a\n+b\n*** End Patch')"
assert_denied "kk guard: secrets" "patch secret"
safe_patch=$(patch_payload "$capy_root" $'*** Begin Patch\n*** Add File: src/a.py\n+print(1)\n*** End Patch')
run_adapter "$capy_root" patch "$safe_patch"
assert_allowed "patch ordinary edit"
run_adapter "$capy_root" patch "$(patch_payload "$capy_root" $'*** Begin Patch\n*** Update File: ../.codex/hooks.json\n@@\n-a\n+b\n*** End Patch')"
assert_denied "kk guard: selfmod" "patch selfmod"

log_test "MCP code uses the project root independently of hook cwd"
mcp_payload=$(jq -n --arg cwd "$capy_root/sub" '{tool_name:"mcp__custom__capy_execute", cwd:$cwd, tool_input:{language:"shell",code:"cat .env"}}')
run_adapter "$capy_root" mcp "$mcp_payload"
assert_denied "kk guard: secrets" "MCP secret"
safe_mcp=$(jq '.tool_input.code = "go test ./..."' <<<"$mcp_payload")
run_adapter "$capy_root" mcp "$safe_mcp"
assert_allowed "MCP ordinary command"
run_adapter "$capy_root" mcp "$(jq '.tool_name = "mcp__custom__capy_execute_file" | .tool_input.path = ".env"' <<<"$safe_mcp")"
assert_denied "kk guard: secrets" "MCP file input"
run_adapter "$capy_root" mcp "$(jq '.tool_name = "mcp__custom__capy_batch_execute" | .tool_input = {commands:[{command:"ls"},{command:"cat .env"}]}' <<<"$safe_mcp")"
assert_denied "kk guard: secrets" "MCP later batch command"

safe_bash=$(jq -n --arg cwd "$capy_root" '{tool_name:"Bash",cwd:$cwd,tool_input:{command:"ls"}}')
log_test "All adapters fail closed without a working interpreter"
for adapter in bash patch mcp; do
  case "$adapter" in
    bash) payload="$safe_bash" ;;
    patch) payload="$safe_patch" ;;
    mcp) payload="$safe_mcp" ;;
  esac
  KK_GUARD_INTERPRETERS=/nonexistent run_adapter "$capy_root" "$adapter" "$payload"
  assert_denied "kk guard: failure" "$adapter bad interpreter"
  run_adapter "$capy_root" "$adapter" 'not JSON'
  assert_denied "kk guard: failure" "$adapter malformed payload"
done

log_test "Raw NUL bytes stay invalid through the Bash adapter"
set +e
PRE_OUTPUT=$({ printf '%s' "$safe_bash"; printf '\0'; } | \
  bash "$capy_root/.codex/scripts/pretooluse-bash.sh" 2>"$capy_root/stderr")
PRE_EXIT=$?
set -e
PRE_ERROR=$(cat "$capy_root/stderr")
assert_denied "kk guard: failure" "raw NUL"

log_test "Missing wrapper and closed stdin block in every adapter"
missing_root=$(make_project "$TOOLBOX_HOOKS")
mv "$missing_root/.codex/scripts/guard/guard.sh" "$missing_root/guard.saved"
for adapter in bash patch mcp; do
  run_adapter "$missing_root" "$adapter" "$safe_bash"
  assert_equals "2" "$PRE_EXIT" "$adapter missing wrapper exits 2"
  assert_not_equals "" "$PRE_ERROR" "$adapter missing wrapper has stderr"
  set +e
  bash "$capy_root/.codex/scripts/pretooluse-$adapter.sh" <&- >"$capy_root/out" 2>"$capy_root/stderr"
  status=$?
  set -e
  assert_equals "2" "$status" "$adapter closed stdin exits 2"
  assert_not_equals "" "$(cat "$capy_root/stderr")" "$adapter closed stdin has stderr"
done

log_test "Missing declaration retains the static session advisory"
mv "$missing_root/.codex/scripts/guard/guard-rules.json" "$missing_root/rules.saved"
ctx=$(session_context "$missing_root")
if [[ "$ctx" == *"Protected files:"* && "$ctx" == *".env"* ]]; then
  log_pass "fallback policy advisory present"
else
  log_fail "fallback policy advisory missing"
fi

# =============================================================================
# Summary
# =============================================================================

print_summary
