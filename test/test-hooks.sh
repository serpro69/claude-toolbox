#!/usr/bin/env bash
# Hook transport contract: silence on allow, JSON + stderr + exit 2 on deny.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GUARD="$REPO_ROOT/klaude-plugin/scripts/guard/guard.sh"
CAPY_SH="$REPO_ROOT/.claude/scripts/capy.sh"
guard_test_dir=$(create_temp_dir "guard-hooks")
TEMP_DIRS+=("$guard_test_dir")
mkdir -p "$guard_test_dir/project" "$guard_test_dir/home"
TEST_PYTHON=$(command -v python3)
INTERPRETER_FIXTURE="$REPO_ROOT/test/fixtures/guard/interpreter.sh"

# Keep the caller's installed config, root and interpreter overrides out of
# these tests. No settings/config files are present in this fake installation.
guard_env=(env -u KK_GUARD_INTERPRETERS
  HOME="$guard_test_dir/home"
  KK_GUARD_PROJECT_ROOT="$guard_test_dir/project"
  KK_GUARD_RULES="$REPO_ROOT/klaude-plugin/scripts/guard/guard-rules.json"
  KK_GUARD_PROJECT_CONFIG="$guard_test_dir/missing-project.json"
  KK_GUARD_USER_CONFIG="$guard_test_dir/missing-user.json")
read_payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Read",tool_input:{file_path:"README.md"},cwd:$cwd}')
secret_payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Read",tool_input:{file_path:".env"},cwd:$cwd}')

run_guard() {
  local payload="$1"
  shift
  exit_code=0
  printf '%s' "$payload" | "${guard_env[@]}" "$@" bash "$GUARD" \
    >"$guard_test_dir/stdout" 2>"$guard_test_dir/stderr" || exit_code=$?
  output=$(cat "$guard_test_dir/stdout")
  stderr_output=$(cat "$guard_test_dir/stderr")
}

assert_allow() {
  assert_equals "0" "$exit_code" "Allowed call exits 0"
  assert_equals "" "$output" "Allowed call has no stdout"
  assert_equals "" "$stderr_output" "Allowed call has no stderr"
}

assert_deny() {
  assert_equals "2" "$exit_code" "Denied call exits 2"
  assert_json_valid "$output" "Deny is valid JSON"
  assert_json_field "$output" '.hookSpecificOutput.hookEventName' "PreToolUse" "Event is PreToolUse"
  assert_json_field "$output" '.hookSpecificOutput.permissionDecision' "deny" "Decision is deny"
  reason=$(printf '%s' "$output" | jq -r '.hookSpecificOutput.permissionDecisionReason')
  [[ "$reason" == *"$1"* ]] || { log_fail "Reason does not contain $1: $reason"; return 1; }
  log_pass "Reason names $1"
  assert_equals "$reason" "$stderr_output" "The same nonempty reason reaches stderr"
}

# =============================================================================
# Section 1: guard.sh — Allow cases
# =============================================================================
log_section "Section 1: guard.sh — Allow cases"
for command in "ls /tmp" "cat app.log" "cat node_modules/foo" "cat build/out.txt"; do
  log_test "Allow: $command"
  payload=$(jq -nc --arg command "$command" '{tool_name:"Bash",tool_input:{command:$command}}')
  run_guard "$payload"
  assert_allow
done
log_test "Allow: ordinary Read"
run_guard "$read_payload"
assert_allow
log_test "Unknown tools are dispatched by the engine"
run_guard '{"tool_name":"FutureTool","tool_input":{}}'
assert_allow
log_test "Engine receives exact payload bytes, including trailing newlines"
payload=$'{"tool_name":"Read","tool_input":{"file_path":"README.md"}}\n\n'
printf '%s' "$payload" >"$guard_test_dir/expected"
run_guard "$payload" KK_GUARD_INTERPRETERS="$INTERPRETER_FIXTURE" \
  GUARD_FIXTURE_MODE=payload GUARD_EXPECTED_INPUT="$guard_test_dir/expected"
assert_allow
log_test "Valid config warning is forwarded without an allow decision"
run_guard "$read_payload" KK_GUARD_INTERPRETERS="$INTERPRETER_FIXTURE" GUARD_FIXTURE_MODE=warning
assert_equals "0" "$exit_code" "Warning exits 0"
assert_equals '{"systemMessage":"invalid test config"}' "$output" "Warning is unchanged"

log_test "Invalid project config warns through the real engine without an allow decision"
run_guard "$read_payload" KK_GUARD_PROJECT_CONFIG="$REPO_ROOT/test/fixtures/guard/project-config/invalid.json"
assert_equals "0" "$exit_code" "Invalid optional config does not block a benign read"
assert_json_valid "$output" "Config warning is valid JSON"
assert_equals '["systemMessage"]' "$(printf '%s' "$output" | jq -c 'keys')" "Only systemMessage is emitted"
assert_equals "true" "$(printf '%s' "$output" | jq '.systemMessage | contains("project-config/invalid.json")')" "Warning names invalid config"
assert_equals "" "$stderr_output" "Warning does not masquerade as a denial"

# =============================================================================
# Section 2: guard.sh — Deny cases
# =============================================================================
log_section "Section 2: guard.sh — Deny cases"
log_test "Plugin-only Read of .env denies with no settings or guard configs"
run_guard "$secret_payload"
assert_deny "secrets"

log_test "Project override adds a secret through the wrapper"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Read",tool_input:{file_path:"private.txt"},cwd:$cwd}')
run_guard "$payload" KK_GUARD_PROJECT_CONFIG="$REPO_ROOT/test/fixtures/guard/project-config/additions.json"
assert_deny "secrets"
log_test "Missing project override leaves that ordinary file readable"
run_guard "$payload" KK_GUARD_PROJECT_CONFIG="$guard_test_dir/no-config.json"
assert_allow

log_test "Invalid config retains baseline denial and its diagnostic"
run_guard "$secret_payload" KK_GUARD_PROJECT_CONFIG="$REPO_ROOT/test/fixtures/guard/project-config/invalid.json"
assert_deny "secrets"
assert_equals "true" "$(printf '%s' "$output" | jq '.systemMessage | contains("project-config/invalid.json")')" "Deny retains the config diagnostic"

log_test "User override allows only the configured dry run through the wrapper"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Bash",tool_input:{command:"git clean -nd"},cwd:$cwd}')
run_guard "$payload" KK_GUARD_USER_CONFIG="$REPO_ROOT/test/fixtures/guard/user-config/scoped.json"
assert_allow

log_test "Plugin-only Bash cat .env denies"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Bash",tool_input:{command:"cat .env"},cwd:$cwd}')
run_guard "$payload"
assert_deny "secrets"

log_test "Bash redirect into settings denies"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Bash",tool_input:{command:"echo x > .claude/settings.json"},cwd:$cwd}')
run_guard "$payload"
assert_deny "selfmod"

log_test "Destructive rule preserves the complete deny transport"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Bash",tool_input:{command:"git clean -fd"},cwd:$cwd}')
run_guard "$payload"
assert_deny "destructive"

log_test "Literal temporary cleanup stays silent"
payload=$(jq -nc --arg cwd "$guard_test_dir/project" \
  '{tool_name:"Bash",tool_input:{command:"rm -rf /tmp/kk-guard-cleanup-probe"},cwd:$cwd}')
run_guard "$payload"
assert_allow

# =============================================================================
# Section 3: guard.sh — Fail-closed cases
# =============================================================================
log_section "Section 3: guard.sh — Fail-closed cases"
for interpreters in /nonexistent ""; do
  log_test "No interpreter: '$interpreters'"
  run_guard "$read_payload" KK_GUARD_INTERPRETERS="$interpreters"
  assert_deny "interpreter"
done
log_test "Empty rules file"
run_guard "$read_payload" KK_GUARD_RULES=/dev/null
assert_deny "failure"
for payload in 'not JSON' '' '{}'; do
  log_test "Malformed payload: '$payload'"
  run_guard "$payload"
  assert_deny "failure"
done
log_test "Unknown tool still reaches declaration loading"
run_guard '{"tool_name":"FutureTool"}' KK_GUARD_RULES=/dev/null
assert_deny "failure"

log_test "Raw NUL bytes stay malformed instead of disappearing in shell buffering"
printf '\0%s' "$read_payload" >"$guard_test_dir/nul-payload"
exit_code=0
"${guard_env[@]}" bash "$GUARD" <"$guard_test_dir/nul-payload" \
  >"$guard_test_dir/stdout" 2>"$guard_test_dir/stderr" || exit_code=$?
output=$(cat "$guard_test_dir/stdout")
stderr_output=$(cat "$guard_test_dir/stderr")
assert_deny "not valid JSON"

for mode in crash stdin-error emitter-error signal malformed malformed-deny empty-deny no-stderr multi-json allow-decision; do
  log_test "Engine failure: $mode"
  run_guard "$secret_payload" KK_GUARD_INTERPRETERS="$INTERPRETER_FIXTURE $TEST_PYTHON" \
    GUARD_FIXTURE_MODE="$mode" GUARD_TEST_PYTHON="$TEST_PYTHON"
  assert_deny "failure"
done
log_test "Broken interpreter shim falls back to a working interpreter"
run_guard "$read_payload" KK_GUARD_INTERPRETERS="$INTERPRETER_FIXTURE $TEST_PYTHON" GUARD_FIXTURE_MODE=broken
assert_allow
log_test "Interpreter available only through PATH works"
run_guard "$read_payload" KK_GUARD_INTERPRETERS=python3
assert_allow
log_test "Wrapper stdin read failure cannot allow a partial payload"
exit_code=0
"${guard_env[@]}" bash "$GUARD" <&- >"$guard_test_dir/stdout" 2>"$guard_test_dir/stderr" || exit_code=$?
output=$(cat "$guard_test_dir/stdout")
# cat's OS error is also present; require the blocking reason itself.
stderr_output=$(tail -n 1 "$guard_test_dir/stderr")
assert_deny "cannot read hook payload"
log_test "Missing jq cannot turn a malformed engine response into allow"
mkdir "$guard_test_dir/path"
for utility in bash dirname mktemp cat rm; do
  ln -s "$(command -v "$utility")" "$guard_test_dir/path/$utility"
done
run_guard "$read_payload" PATH="$guard_test_dir/path" \
  KK_GUARD_INTERPRETERS="$INTERPRETER_FIXTURE" GUARD_FIXTURE_MODE=malformed
assert_deny "malformed engine output"

# =============================================================================
# Section 4: capy.sh — Graceful degradation
# =============================================================================

log_section "Section 4: capy.sh — Graceful degradation"

log_test "capy.sh exits 0 when capy binary is not found"
# Use a temporary empty dir as PATH so capy can't be found.
# Must use full path to bash since PATH is restricted.
capy_test_dir=$(create_temp_dir "capy-path")
bash_bin=$(command -v bash)
set +e
output=$(env PATH="$capy_test_dir" HOME="/nonexistent" "$bash_bin" "$CAPY_SH" hook pretooluse 2>/dev/null </dev/null)
exit_code=$?
set -e
assert_equals "0" "$exit_code" "Exit code is 0 when capy not found"

# =============================================================================
# Section 5: file-tool latency
# =============================================================================
log_section "Section 5: file-tool latency"
log_test "100 Read calls: always report p95, enforce <60 ms only outside CI"
# A single timing process works on macOS too (BSD date has no %N). The timing
# includes the complete wrapper and engine, with no interpreter startup per tick.
# Linux, 2026-10-25: p95 25.72 ms (100 Read calls, system Python 3.10.12).
"${guard_env[@]}" "$TEST_PYTHON" -I - "$GUARD" "$read_payload" <<'PY'
import os
import subprocess
import sys
import time

samples = []
for _ in range(100):
    start = time.perf_counter()
    result = subprocess.run(["bash", sys.argv[1]], input=sys.argv[2].encode(),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    samples.append((time.perf_counter() - start) * 1000)
    if result.returncode != 0 or result.stdout or result.stderr:
        sys.exit("Read latency probe failed the allow contract: %r" % (result,))
p95 = sorted(samples)[94]
print("Read wrapper p95 (100 samples): %.2f ms" % p95, flush=True)
if "CI" not in os.environ and p95 >= 60:
    sys.exit("Read p95 exceeds the local 60 ms limit")
PY
log_pass "Read latency probe passed"

print_summary
