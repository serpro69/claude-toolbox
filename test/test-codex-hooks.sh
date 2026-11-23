#!/usr/bin/env bash
# Test the released Codex guard with and without Capy hooks in a repository.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fixture=$(create_temp_dir "codex-adapter-cases")
TEMP_DIRS+=("$fixture")

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

# Install the guard plugin beside a disposable project with optional hooks.
make_project() {
  local root
  root=$(mktemp -d "$fixture/workspace.XXXXXXXX")
  git -C "$root" init -q
  mkdir -p "$root/.codex" "$root/.claude" "$root/home" "$root/sub"
  cp -R "$REPO_ROOT/kodex-guard" "$root.plugin"
  if [[ $# -gt 0 ]]; then
    printf '%s\n' "$1" >"$root/.codex/hooks.json"
  fi
  echo "$root"
}

run_adapter() {
  local root=$1 adapter=$2 payload=$3 command
  command=$(jq -er --arg adapter "$adapter" '
    .hooks.PreToolUse[] | select(.matcher == ({
      bash:"Bash", patch:"Edit|Write", mcp:"^mcp__[^[:space:]]+__capy_(execute|execute_file|batch_execute)$"
    }[$adapter])) | .hooks[] | select(.type == "command") | .command
  ' "$root.plugin/hooks/hooks.json")
  set +e
  PRE_OUTPUT=$(cd -- "${4:-$root/sub}" && env -u KK_GUARD_PROJECT_CONFIG HOME="$root/home" \
    KK_GUARD_USER_CONFIG="$root/no-user-config" \
    PLUGIN_ROOT="$root.plugin" bash -c "$command" <<<"$payload" 2>"$root/stderr")
  PRE_EXIT=$?
  set -e
  PRE_ERROR=$(cat "$root/stderr")
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
  assert_equals "$reason" "$PRE_ERROR" "$message: stderr contains only the guard reason"
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
  assert_equals "" "$PRE_ERROR" "$message: no stderr (pass-through)"
}

# =============================================================================
# Project configurations for adapter routing
legacy_root=$(make_project "$TOOLBOX_HOOKS")
capy_root=$(make_project "$CAPY_HOOKS")
nofile_root=$(make_project)
broken_root=$(make_project '{"hooks": {"SessionStart": [')

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

log_test "A SessionStart registration alone keeps HTTP routing"
partial_root=$(make_project "$PARTIAL_HOOKS")
run_pretooluse "$partial_root" "curl -s https://example.com"
assert_denied "curl" "partial curl (no capy PreToolUse entry)"

log_test "A PreToolUse registration defers HTTP routing"
partial_pt_root=$(make_project "$PARTIAL_PT_HOOKS")
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

log_test "Patch deletion outside temporary roots reports only the policy denial"
# Payloads are inspected, never applied; the target need not exist.
run_adapter "$capy_root" patch "$(patch_payload "$capy_root" $'*** Begin Patch\n*** Delete File: /work/guard-project/src/old.py\n*** End Patch')"
assert_denied "filesystem: apply_patch deletes a file" "patch deletion"

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
scripts="$capy_root.plugin/scripts"
PRE_OUTPUT=$({ printf '%s' "$safe_bash"; printf '\0'; } | \
  (cd "$capy_root/sub" && bash "$scripts/pretooluse-bash.sh") 2>"$capy_root/stderr")
PRE_EXIT=$?
set -e
PRE_ERROR=$(cat "$capy_root/stderr")
assert_denied "kk guard: failure" "raw NUL"

log_test "Missing wrapper and closed stdin block in every adapter"
missing_root=$(make_project "$TOOLBOX_HOOKS")
mv "$missing_root.plugin/scripts/guard/guard.sh" "$missing_root/guard.saved"
for adapter in bash patch mcp; do
  run_adapter "$missing_root" "$adapter" "$safe_bash"
  assert_equals "2" "$PRE_EXIT" "$adapter missing wrapper exits 2"
  assert_not_equals "" "$PRE_ERROR" "$adapter missing wrapper has stderr"
  if [[ "$PRE_ERROR" == *"adapter could not run; nothing was executed; repair the hook"* ]]; then
    log_pass "$adapter missing wrapper reports adapter failure"
  else
    log_fail "$adapter missing wrapper should report adapter failure"
  fi
  set +e
  (cd "$capy_root/sub" && bash "$scripts/pretooluse-$adapter.sh") <&- >"$capy_root/out" 2>"$capy_root/stderr"
  status=$?
  set -e
  assert_equals "2" "$status" "$adapter closed stdin exits 2"
  assert_not_equals "" "$(cat "$capy_root/stderr")" "$adapter closed stdin has stderr"
  if [[ "$(cat "$capy_root/stderr")" == *"adapter could not run; nothing was executed; repair the hook"* ]]; then
    log_pass "$adapter closed stdin reports adapter failure"
  else
    log_fail "$adapter closed stdin should report adapter failure"
  fi
done

log_section "Plugin workspace selection"
other=$(make_project "$CAPY_HOOKS")
mkdir "$other/sub/protected"
touch "$other/sub/only-in-other.txt"
jq -n --arg glob "/$other/sub/protected/**" '{version:1,secrets:[$glob]}' >"$legacy_root/.claude/kk-guard.json"
printf '%s\n' '{"version":1,"secrets":["./**/only-in-other.txt"]}' >"$other/.claude/kk-guard.json"
run_pretooluse "$legacy_root" "cat protected/fixture.txt" "$other/sub"
assert_denied "protected" "Bash resolves operands in the other repo using the launch repo's policy"
run_pretooluse "$legacy_root" "cat only-in-other.txt" "$other/sub"
assert_allowed "The operand repo does not supply project policy"
run_adapter "$legacy_root" patch "$(patch_payload "$other" $'*** Begin Patch\n*** Add File: protected/fixture.txt\n+test\n*** End Patch')"
assert_denied "protected" "Patch uses launch policy and payload cwd"
run_adapter "$legacy_root" mcp "$(jq -nc --arg cwd "$other/sub" \
  '{tool_name:"mcp__test__capy_execute",cwd:$cwd,tool_input:{cwd:$cwd,language:"shell",code:"cat protected/fixture.txt"}}')"
assert_denied "protected" "Capy uses launch policy and the requested operand directory"
run_pretooluse "$legacy_root" "curl https://example.com" "$other/sub"
assert_denied "curl" "Only the launch workspace can delegate HTTP routing"
run_pretooluse "$other" "curl https://example.com" "$legacy_root/sub"
assert_allowed "A capy registration in the launch workspace delegates routing"

plain="$fixture/plain"
mkdir -p "$plain/.claude"
touch "$plain/plain-marker.txt"
printf '%s\n' '{"version":1,"secrets":["./**/plain-marker.txt"]}' >"$plain/.claude/kk-guard.json"
run_adapter "$legacy_root" bash "$(jq -nc --arg cwd "$plain" \
  '{tool_name:"Bash",cwd:$cwd,tool_input:{command:"cat plain-marker.txt"}}')" "$plain"
assert_denied "plain-marker.txt" "Outside Git the launch directory anchors policy"
invalid="$fixture/invalid-worktree"
mkdir "$invalid"
printf 'gitdir: ./missing-metadata\n' >"$invalid/.git"
run_adapter "$legacy_root" bash "$safe_bash" "$invalid"
assert_equals "2" "$PRE_EXIT" "Indeterminate Git workspace fails closed"
assert_output_contains "could not run" "cat '$legacy_root/stderr'" "Indeterminate workspace is reported as an adapter failure"
if [[ -e "$legacy_root.plugin/scripts/guard/__pycache__" ]]; then
  log_fail "Running the plugin modified its guard bundle"
else
  log_pass "Hook execution left the plugin bundle free of bytecode"
fi

# =============================================================================
# Summary
# =============================================================================

print_summary
