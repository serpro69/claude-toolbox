#!/usr/bin/env bash
# Test suite for klaude-plugin/scripts/cpr.py (Claude Plugin Root resolver)
# and klaude-plugin/scripts/set-plugin-root.sh (SessionStart export hook)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CPR="$REPO_ROOT/klaude-plugin/scripts/cpr.py"
SET_PLUGIN_ROOT="$REPO_ROOT/klaude-plugin/scripts/set-plugin-root.sh"

# =============================================================================
# Fixture setup
# =============================================================================

FIXTURE_DIR="$(create_temp_dir "cpr-test")"
PLUGINS_JSON="$FIXTURE_DIR/installed_plugins.json"

# Create fake install directories
mkdir -p "$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3"
mkdir -p "$FIXTURE_DIR/cache/cortex-ai/cortex/0.3.0"
mkdir -p "$FIXTURE_DIR/cache/other-repo/kk-utils/1.0.0"
mkdir -p "$FIXTURE_DIR/cache/proj-a/kk/0.16.0"
mkdir -p "$FIXTURE_DIR/cache/proj-b/kk/0.17.3"
mkdir -p "$FIXTURE_DIR/cache/user/kk/0.10.0"
mkdir -p "$FIXTURE_DIR/env-root"

# Base fixture: user-scope (global) entries with no projectPath, so the
# name-matching tests resolve via the global tier regardless of cwd.
cat > "$PLUGINS_JSON" <<EOF
{
  "plugins": {
    "kk@claude-toolbox": [
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3",
        "version": "0.17.3",
        "installedAt": "2026-05-28T10:00:00.000Z"
      }
    ],
    "cortex@cortex-ai": [
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/cache/cortex-ai/cortex/0.3.0",
        "version": "0.3.0",
        "installedAt": "2026-05-20T10:00:00.000Z"
      }
    ],
    "kk-utils@other-repo": [
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/cache/other-repo/kk-utils/1.0.0",
        "version": "1.0.0",
        "installedAt": "2026-05-15T10:00:00.000Z"
      }
    ]
  }
}
EOF

# Helper: run cpr.py against the base fixture
run_cpr() {
  CPR_PLUGINS_FILE="$PLUGINS_JSON" python3 "$CPR" "$@"
}

# Helper: run cpr.py against an arbitrary plugins file
run_cpr_file() {
  local plugins_file="$1"; shift
  CPR_PLUGINS_FILE="$plugins_file" python3 "$CPR" "$@"
}

# Helper: run cpr.py and capture exit code without set -e aborting
run_cpr_rc() {
  set +e
  run_cpr "$@" >/dev/null 2>&1
  local rc=$?
  set -e
  echo "$rc"
}

# =============================================================================
# Section 1: Exact matching
# =============================================================================

log_section "Section 1: Exact Matching"

log_test "Exact match on plugin name"
actual=$(run_cpr "kk")
assert_equals "$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3" "$actual" "kk resolves to kk@claude-toolbox"

log_test "Exact match is case-insensitive"
actual=$(run_cpr "KK")
assert_equals "$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3" "$actual" "KK matches kk"

log_test "Exact match on different plugin"
actual=$(run_cpr "cortex")
assert_equals "$FIXTURE_DIR/cache/cortex-ai/cortex/0.3.0" "$actual" "cortex resolves correctly"

log_test "No substring false positive: 'kk' does not match 'kk-utils'"
actual=$(run_cpr "kk")
assert_equals "$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3" "$actual" "kk is not kk-utils"

log_test "kk-utils matches its own entry"
actual=$(run_cpr "kk-utils")
assert_equals "$FIXTURE_DIR/cache/other-repo/kk-utils/1.0.0" "$actual" "kk-utils resolves to kk-utils@other-repo"

# =============================================================================
# Section 2: Project resolution cascade (projectPath -> user -> last-installed)
# =============================================================================

log_section "Section 2: Project Resolution Cascade"

# Two project-bound installs (for distinct projects) plus a global user-scope
# install. The project entries are listed in non-recency order on purpose.
CASCADE_JSON="$FIXTURE_DIR/cascade.json"
cat > "$CASCADE_JSON" <<EOF
{
  "plugins": {
    "kk@claude-toolbox": [
      {
        "scope": "project",
        "projectPath": "/tmp/proj-a",
        "installPath": "$FIXTURE_DIR/cache/proj-a/kk/0.16.0",
        "version": "0.16.0",
        "installedAt": "2026-05-20T10:00:00.000Z"
      },
      {
        "scope": "project",
        "projectPath": "/tmp/proj-b",
        "installPath": "$FIXTURE_DIR/cache/proj-b/kk/0.17.3",
        "version": "0.17.3",
        "installedAt": "2026-05-28T10:00:00.000Z"
      },
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/cache/user/kk/0.10.0",
        "version": "0.10.0",
        "installedAt": "2026-05-10T10:00:00.000Z"
      }
    ]
  }
}
EOF

log_test "Project-bound install wins when projectPath matches (proj-a)"
actual=$(run_cpr_file "$CASCADE_JSON" "kk" "/tmp/proj-a")
assert_equals "$FIXTURE_DIR/cache/proj-a/kk/0.16.0" "$actual" "proj-a resolves to its own install, not the newer proj-b"

log_test "Project-bound install wins when projectPath matches (proj-b)"
actual=$(run_cpr_file "$CASCADE_JSON" "kk" "/tmp/proj-b")
assert_equals "$FIXTURE_DIR/cache/proj-b/kk/0.17.3" "$actual" "proj-b resolves to its own install"

log_test "A nested cwd matches its project root"
actual=$(run_cpr_file "$CASCADE_JSON" "kk" "/tmp/proj-a/nested/dir")
assert_equals "$FIXTURE_DIR/cache/proj-a/kk/0.16.0" "$actual" "subdirectory of proj-a resolves to proj-a"

log_test "Falls back to the user-scope (global) entry when no project matches"
actual=$(run_cpr_file "$CASCADE_JSON" "kk" "/tmp/unrelated")
assert_equals "$FIXTURE_DIR/cache/user/kk/0.10.0" "$actual" "unrelated project gets the global install"

# No user-scope entry: the cascade must fall through to the most-recently
# installed entry regardless of project (this is the real kk@gh-arc situation).
LAST_INSTALLED_JSON="$FIXTURE_DIR/last-installed.json"
cat > "$LAST_INSTALLED_JSON" <<EOF
{
  "plugins": {
    "kk@claude-toolbox": [
      {
        "scope": "project",
        "projectPath": "/tmp/proj-a",
        "installPath": "$FIXTURE_DIR/cache/proj-a/kk/0.16.0",
        "version": "0.16.0",
        "installedAt": "2026-05-20T10:00:00.000Z"
      },
      {
        "scope": "project",
        "projectPath": "/tmp/proj-b",
        "installPath": "$FIXTURE_DIR/cache/proj-b/kk/0.17.3",
        "version": "0.17.3",
        "installedAt": "2026-05-28T10:00:00.000Z"
      }
    ]
  }
}
EOF

log_test "No project match and no user scope: falls back to last installed"
actual=$(run_cpr_file "$LAST_INSTALLED_JSON" "kk" "/tmp/unrelated")
assert_equals "$FIXTURE_DIR/cache/proj-b/kk/0.17.3" "$actual" "most-recently-installed cross-project entry wins as last resort"

# =============================================================================
# Section 3: Fuzzy matching
# =============================================================================

log_section "Section 3: Fuzzy Matching"

log_test "Fuzzy match on close name"
actual=$(run_cpr "corte")
assert_equals "$FIXTURE_DIR/cache/cortex-ai/cortex/0.3.0" "$actual" "corte fuzzy-matches cortex"

log_test "Fuzzy match warns on stderr (fail loud — may be the wrong plugin)"
set +e
stderr=$(run_cpr "corte" 2>&1 >/dev/null)
set -e
assert_output_contains "fuzzy" "echo '$stderr'" "fuzzy match emits a warning on stderr"

log_test "Exact match is silent on stderr"
set +e
stderr=$(run_cpr "kk" 2>&1 >/dev/null)
set -e
assert_output_not_contains "Warning" "echo '$stderr'" "exact match emits no warning"

log_test "No match for completely unrelated name"
rc=$(run_cpr_rc "zzzzz")
assert_not_equals "0" "$rc" "zzzzz should not match anything"

# =============================================================================
# Section 4: Error handling
# =============================================================================

log_section "Section 4: Error Handling"

log_test "No arguments exits non-zero"
rc=$(run_cpr_rc)
assert_not_equals "0" "$rc" "No arguments should fail"

log_test "Usage message on no arguments"
set +e
stderr=$(CPR_PLUGINS_FILE="$PLUGINS_JSON" python3 "$CPR" 2>&1)
set -e
assert_output_contains "Usage:" "echo '$stderr'" "Shows usage on no args"

log_test "Missing plugins file exits non-zero"
rc=$(set +e; CPR_PLUGINS_FILE="/nonexistent/file.json" python3 "$CPR" "kk" >/dev/null 2>&1; echo $?)
assert_not_equals "0" "$rc" "Missing plugins file should fail"

log_test "Malformed JSON exits non-zero"
BROKEN_JSON="$FIXTURE_DIR/broken.json"
echo "not json" > "$BROKEN_JSON"
rc=$(set +e; CPR_PLUGINS_FILE="$BROKEN_JSON" python3 "$CPR" "kk" >/dev/null 2>&1; echo $?)
assert_not_equals "0" "$rc" "Malformed JSON should fail"

log_test "Plugin not found shows error on stderr"
set +e
stderr=$(CPR_PLUGINS_FILE="$PLUGINS_JSON" python3 "$CPR" "nonexistent" 2>&1 >/dev/null)
set -e
assert_output_contains "Error:" "echo '$stderr'" "Shows error for unknown plugin"

# =============================================================================
# Section 5: Install path validation
# =============================================================================

log_section "Section 5: Install Path Validation"

MISSING_DIR_JSON="$FIXTURE_DIR/missing-dir.json"
cat > "$MISSING_DIR_JSON" <<EOF
{
  "plugins": {
    "ghost@repo": [
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/does-not-exist",
        "version": "1.0.0",
        "installedAt": "2026-05-28T10:00:00.000Z"
      }
    ]
  }
}
EOF

log_test "Entry with non-existent installPath is skipped"
rc=$(set +e; CPR_PLUGINS_FILE="$MISSING_DIR_JSON" python3 "$CPR" "ghost" >/dev/null 2>&1; echo $?)
assert_not_equals "0" "$rc" "Non-existent installPath should not be returned"

# A project-bound match whose installPath is missing must fall through to the
# next tier (here, the valid user-scope entry) rather than returning nothing.
FALLTHROUGH_JSON="$FIXTURE_DIR/fallthrough.json"
cat > "$FALLTHROUGH_JSON" <<EOF
{
  "plugins": {
    "kk@claude-toolbox": [
      {
        "scope": "project",
        "projectPath": "/tmp/proj-a",
        "installPath": "$FIXTURE_DIR/cache/gone/kk/9.9.9",
        "version": "9.9.9",
        "installedAt": "2026-05-28T10:00:00.000Z"
      },
      {
        "scope": "user",
        "installPath": "$FIXTURE_DIR/cache/user/kk/0.10.0",
        "version": "0.10.0",
        "installedAt": "2026-05-10T10:00:00.000Z"
      }
    ]
  }
}
EOF

log_test "Missing project-bound installPath falls through to a valid lower tier"
actual=$(run_cpr_file "$FALLTHROUGH_JSON" "kk" "/tmp/proj-a")
assert_equals "$FIXTURE_DIR/cache/user/kk/0.10.0" "$actual" "missing tier-1 path falls through to the user-scope install"

# =============================================================================
# Section 6: set-plugin-root.sh (SessionStart export)
# =============================================================================

log_section "Section 6: set-plugin-root.sh"

KK_PATH="$FIXTURE_DIR/cache/claude-toolbox/kk/0.17.3"

log_test "Writes export line resolved via cpr.py"
ENV_FILE="$FIXTURE_DIR/env-out-1.sh"
: > "$ENV_FILE"
CPR_PLUGINS_FILE="$PLUGINS_JSON" CLAUDE_ENV_FILE="$ENV_FILE" bash "$SET_PLUGIN_ROOT" "" >/dev/null 2>&1
assert_output_contains "export TOOLBOX_PLUGIN_ROOT=\"$KK_PATH\"" "cat '$ENV_FILE'" "cpr.py-resolved path is exported"

log_test "Passes \$CLAUDE_PROJECT_DIR through to cpr.py"
ENV_FILE="$FIXTURE_DIR/env-out-proj.sh"
: > "$ENV_FILE"
CPR_PLUGINS_FILE="$CASCADE_JSON" CLAUDE_PROJECT_DIR="/tmp/proj-b" CLAUDE_ENV_FILE="$ENV_FILE" bash "$SET_PLUGIN_ROOT" "" >/dev/null 2>&1
assert_output_contains "export TOOLBOX_PLUGIN_ROOT=\"$FIXTURE_DIR/cache/proj-b/kk/0.17.3\"" "cat '$ENV_FILE'" "CLAUDE_PROJECT_DIR selects the project-bound install"

log_test "Falls back to \$1 when cpr.py cannot resolve"
ENV_FILE="$FIXTURE_DIR/env-out-2.sh"
: > "$ENV_FILE"
CPR_PLUGINS_FILE="/nonexistent/file.json" CLAUDE_ENV_FILE="$ENV_FILE" bash "$SET_PLUGIN_ROOT" "$FIXTURE_DIR/env-root" >/dev/null 2>&1
assert_output_contains "export TOOLBOX_PLUGIN_ROOT=\"$FIXTURE_DIR/env-root\"" "cat '$ENV_FILE'" "argument fallback is exported"

log_test "Unset CLAUDE_ENV_FILE exits cleanly without error"
rc=$(set +e; env -u CLAUDE_ENV_FILE CPR_PLUGINS_FILE="$PLUGINS_JSON" bash "$SET_PLUGIN_ROOT" "" >/dev/null 2>&1; echo $?)
assert_equals "0" "$rc" "no ambiguous-redirect error when CLAUDE_ENV_FILE is unset"

log_test "Neither cpr.py nor \$1 resolves: nothing written"
ENV_FILE="$FIXTURE_DIR/env-out-3.sh"
: > "$ENV_FILE"
CPR_PLUGINS_FILE="/nonexistent/file.json" CLAUDE_ENV_FILE="$ENV_FILE" bash "$SET_PLUGIN_ROOT" "/nonexistent/dir" >/dev/null 2>&1
assert_output_not_contains "TOOLBOX_PLUGIN_ROOT" "cat '$ENV_FILE'" "no export line when no valid root found"

log_test "Exits cleanly when the env file append fails (unwritable target)"
# CLAUDE_ENV_FILE points into a directory that does not exist, so the `>>`
# redirect fails. The hook must still exit 0 — a non-zero exit is read as a
# hook failure, not a no-op.
rc=$(set +e; CPR_PLUGINS_FILE="$PLUGINS_JSON" CLAUDE_ENV_FILE="$FIXTURE_DIR/no-such-dir/env.sh" bash "$SET_PLUGIN_ROOT" "" >/dev/null 2>&1; echo $?)
assert_equals "0" "$rc" "append failure does not produce a non-zero hook exit"

# =============================================================================
# Summary
# =============================================================================

print_summary
