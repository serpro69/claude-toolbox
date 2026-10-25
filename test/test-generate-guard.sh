#!/usr/bin/env bash
# Exercise generator behavior independently of committed generated snapshots.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fixture=$(create_temp_dir "guard-generator")
TEMP_DIRS+=("$fixture")
mkdir -p "$fixture/scripts" "$fixture/klaude-plugin/scripts/guard" "$fixture/.claude" "$fixture/docs/user-guide"
cp "$REPO_ROOT/scripts/generate-guard.sh" "$fixture/scripts/"
cp -p "$REPO_ROOT/klaude-plugin/scripts/guard/"* "$fixture/klaude-plugin/scripts/guard/"
cp "$REPO_ROOT/.claude/settings.json" "$fixture/.claude/settings.json"
cp "$REPO_ROOT/docs/user-guide/configuration.md" "$fixture/docs/user-guide/configuration.md"

log_test "Only permissions.deny changes, with deterministic unique ordering"
jq '.permissions.deny = ["obsolete"] | .custom = {"preserved": true}' \
  "$fixture/.claude/settings.json" >"$fixture/settings-before.json"
cp "$fixture/settings-before.json" "$fixture/.claude/settings.json"
bash "$fixture/scripts/generate-guard.sh"
assert_equals "$(jq -c 'del(.permissions.deny)' "$fixture/settings-before.json")" \
  "$(jq -c 'del(.permissions.deny)' "$fixture/.claude/settings.json")" "All unrelated settings survive"
assert_equals "$(jq -c '.secrets | unique | map("Read(" + . + ")")' "$fixture/klaude-plugin/scripts/guard/guard-rules.json")" \
  "$(jq -c '.permissions.deny' "$fixture/.claude/settings.json")" "Deny is the sorted secrets projection"

log_test "Generation is idempotent and alternate output leaves inputs alone"
bash "$fixture/scripts/generate-guard.sh" "$fixture/second"
for file in .claude/settings.json .codex/rules/default.rules docs/user-guide/configuration.md \
  .codex/scripts/guard/guard.sh .codex/scripts/guard/guard.py \
  .codex/scripts/guard/guard-rules.json .codex/scripts/guard/LICENSE.md; do
  cmp "$fixture/$file" "$fixture/second/$file"
  log_pass "Identical second render: $file"
done

log_test "Docs generation preserves text outside the markers"
awk '/^<!-- BEGIN GUARD-RULES -->$/ { inside=1; next } /^<!-- END GUARD-RULES -->$/ { inside=0; next } !inside' \
  "$REPO_ROOT/docs/user-guide/configuration.md" >"$fixture/docs-before"
awk '/^<!-- BEGIN GUARD-RULES -->$/ { inside=1; next } /^<!-- END GUARD-RULES -->$/ { inside=0; next } !inside' \
  "$fixture/docs/user-guide/configuration.md" >"$fixture/docs-after"
cmp "$fixture/docs-before" "$fixture/docs-after"
log_pass "Unmarked prose is preserved"

log_test "Union tokens and multiple records keep their own examples"
rules="$fixture/klaude-plugin/scripts/guard/guard-rules.json"
jq '.destructive.filesystem[0].codex = [
  {pattern:["rm",["-r","-rf"]], match:["rm -r x","rm -rf x"], not_match:["rm -f x"]},
  {pattern:["rm","-f"], match:["rm -f x"], not_match:["rm -r x"]}
]' "$rules" >"$fixture/variant.json"
cp "$fixture/variant.json" "$rules"
bash "$fixture/scripts/generate-guard.sh" "$fixture/variant"
if command -v codex >/dev/null 2>&1; then
  log_info "$(codex --version)"
  for option in -r -rf -f; do
    decision=$(codex execpolicy check --rules "$fixture/variant/.codex/rules/default.rules" -- rm "$option" x)
    assert_json_field "$decision" '.decision' "forbidden" "Union/record variant $option loads and matches"
  done
else
  log_skip "codex unavailable; union-token rule parsing not exercised"
fi

log_test "Invalid documentation markers fail before any destination changes"
cp "$fixture/docs/user-guide/configuration.md" "$fixture/valid-docs"
for mode in missing duplicate reversed; do
  case "$mode" in
    missing) sed '/<!-- END GUARD-RULES -->/d' "$fixture/valid-docs" >"$fixture/docs/user-guide/configuration.md" ;;
    duplicate) cat "$fixture/valid-docs" "$fixture/valid-docs" >"$fixture/docs/user-guide/configuration.md" ;;
    reversed) printf '%s\n' '<!-- END GUARD-RULES -->' '<!-- BEGIN GUARD-RULES -->' >"$fixture/docs/user-guide/configuration.md" ;;
  esac
  cp "$fixture/.claude/settings.json" "$fixture/settings-saved"
  if bash "$fixture/scripts/generate-guard.sh"; then
    log_fail "$mode markers must reject generation"
  else
    log_pass "$mode markers rejected"
  fi
  cmp "$fixture/settings-saved" "$fixture/.claude/settings.json"
  log_pass "Settings untouched on $mode markers"
done

print_summary
