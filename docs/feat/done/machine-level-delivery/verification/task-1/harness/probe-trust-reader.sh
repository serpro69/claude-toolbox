#!/usr/bin/env bash
# Probe 1.5 (assumption 7), captured cases: what app-server hooks/list reports for
# the guard handler when it is trusted, switched off by the user, changed since
# review, and switched off by a trusted project in several ways; and whether
# `codex app-server -c …` overrides change the answer. No model call.
#
# Usage: KKPROBE_ROOT=<root of the main scratch home, e.g. ~/kkprobe-task1/r1> \
#        probe-trust-reader.sh <directory for the full RPC exchanges>
# Needs the state the live-session probes left behind: kkprobe-guard@kkprobe
# installed and trusted, repo-a and repo-b trusted projects. The user config, the
# guard bytes and repo-b's project config are restored on exit, including after
# an interruption. Each case's full request/response is written as NN-<case>.json.
set -uo pipefail
: "${KKPROBE_ROOT:?}"
outdir=${1:?directory for the full RPC exchanges}
mkdir -p "$outdir"
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export CODEX_HOME=$KKPROBE_ROOT/home
cfg=$CODEX_HOME/config.toml
guard_src=$KKPROBE_ROOT/mkt/plugins/kkprobe-guard/scripts/guard.sh
projcfg=$KKPROBE_ROOT/repo-b/.codex/config.toml
key='kkprobe-guard@kkprobe:hooks/hooks.json:pre_tool_use:0:0'

backup=$(mktemp -d "$KKPROBE_ROOT/trust-reader-backup.XXXXXX")
cp "$cfg" "$backup/config.toml"
cp "$guard_src" "$backup/guard.sh"
mkdir -p "$KKPROBE_ROOT/repo-b/.codex"
[ -f "$projcfg" ] && mv "$projcfg" "$backup/project-config.toml"
installed_changed=0  # 1 from the moment changed guard bytes may be installed until the original is reinstalled
restore() {
  cp "$backup/config.toml" "$cfg"
  if [ "$installed_changed" = 1 ] || ! cmp -s "$backup/guard.sh" "$guard_src"; then
    cp "$backup/guard.sh" "$guard_src"
    codex plugin add kkprobe-guard@kkprobe >/dev/null 2>&1 && installed_changed=0
  fi
  [ -f "$projcfg" ] && mv -f "$projcfg" "$backup/project-config.probe-case.toml"
  [ -f "$backup/project-config.toml" ] && mv "$backup/project-config.toml" "$projcfg"
}
trap restore EXIT

n=0
failed=0
# One hooks/list read; prints the guard handler's state per workspace, or
# "absent" when the handler is not listed, plus the time the read took. A read
# that does not answer for both workspaces fails the case.
read_state() {
  local label=$1; shift
  local out elapsed file
  n=$((n + 1))
  file=$(printf '%s/%02d-%s.json' "$outdir" "$n" "$(printf '%s' "$label" | tr -cs 'A-Za-z0-9' '-' | cut -c1-60)")
  out=$(python3 -I "$here/app-server-rpc.py" hooks/list \
    "{\"cwds\": [\"$KKPROBE_ROOT/repo-a\", \"$KKPROBE_ROOT/repo-b\"]}" "$@" 2>"$KKPROBE_ROOT/rpc.err")
  printf '%s\n' "$out" >"$file"
  elapsed=$(sed -n 's/^elapsed_seconds=//p' "$KKPROBE_ROOT/rpc.err")
  printf '%s  [%ss]  (%s)\n' "$label" "${elapsed:-?}" "$(basename "$file")"
  if ! printf '%s' "$out" | jq -e '.response.result.data | length == 2 and all(.[]; (.errors | length) == 0)' >/dev/null 2>&1; then
    echo "  FAILED: no error-free answer for both workspaces"; failed=1; return
  fi
  printf '%s' "$out" | jq -r --arg key "$key" '
    .response.result.data[] | . as $e
    | ([.hooks[] | select(.key == $key)] | first) as $h
    | "  \($e.cwd | sub(".*/";"")): " +
      (if $h == null then "absent" else "enabled=\($h.enabled) trustStatus=\($h.trustStatus)" end)'
}

set_user_enabled() {  # true|false for the guard key in the user config; adds the line if missing
  python3 -I - "$cfg" "$key" "$1" <<'PY'
import sys
path, key, value = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(path).read().split("\n")
header = '[hooks.state."%s"]' % key
start = lines.index(header) + 1
end = start
while end < len(lines) and not lines[end].startswith("["):
    end += 1
for i in range(start, end):
    if lines[i].startswith("enabled"):
        lines[i] = "enabled = %s" % value
        break
else:
    lines.insert(start, "enabled = %s" % value)
open(path, "w").write("\n".join(lines))
PY
}

echo "== codex $(codex --version 2>/dev/null)"
read_state "trusted, enabled (baseline)"

set_user_enabled false
read_state "user switched the hook off (hooks.state enabled = false, as /hooks writes it)"
set_user_enabled true

installed_changed=1
printf '\n# modified for the trust-reader probe\n' >>"$guard_src"
codex plugin add kkprobe-guard@kkprobe >/dev/null 2>&1
read_state "guard bytes changed since review (same version re-added)"
cp "$backup/guard.sh" "$guard_src"
codex plugin add kkprobe-guard@kkprobe >/dev/null 2>&1 && installed_changed=0
read_state "original bytes re-added"

for body in \
  '[plugins."kkprobe-guard@kkprobe"]
enabled = false' \
  '[features]
hooks = false' \
  '[features]
plugins = false' \
  "[hooks.state.\"$key\"]
enabled = false"; do
  printf '%s\n' "$body" >"$projcfg"
  read_state "trusted project repo-b sets: $(printf '%s' "$body" | tr '\n' ' ')"
done
mv -f "$projcfg" "$backup/project-config.probe-case.toml"

read_state "app-server -c features.hooks=false" -c features.hooks=false
# Codex splits a -c key on dots and does not treat double quotes as quoting, so
# the quoted spelling names a different, nonexistent key. Both are recorded.
read_state "app-server -c 'plugins.\"kkprobe-guard@kkprobe\".enabled=false' (quoted)" \
  -c 'plugins."kkprobe-guard@kkprobe".enabled=false'
read_state "app-server -c plugins.kkprobe-guard@kkprobe.enabled=false (unquoted)" \
  -c plugins.kkprobe-guard@kkprobe.enabled=false

echo "== does a session honour the same keys? (kkprobe-hello skill mentions in codex debug prompt-input)"
for spelling in none 'plugins."kkprobe-skills@kkprobe".enabled=false' plugins.kkprobe-skills@kkprobe.enabled=false; do
  if [ "$spelling" = none ]; then args=(); else args=(-c "$spelling"); fi
  # A failed or empty prompt render would also count 0: require a valid prompt first.
  if ! prompt=$(cd "$KKPROBE_ROOT/repo-a" && codex "${args[@]}" debug prompt-input hi 2>/dev/null) \
     || ! printf '%s' "$prompt" | jq -e 'length > 0' >/dev/null 2>&1; then
    printf '  -c %s: FAILED (no valid prompt rendered)\n' "$spelling"; failed=1; continue
  fi
  printf '  -c %s: %s\n' "$spelling" "$(printf '%s' "$prompt" | grep -c 'kkprobe-hello')"
done

restore
trap - EXIT
read_state "restored"
exit "$failed"
