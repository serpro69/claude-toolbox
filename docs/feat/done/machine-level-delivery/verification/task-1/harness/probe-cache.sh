#!/usr/bin/env bash
# Probe 1.3 / 1.8 (install mechanics only, no session): what `codex plugin add`
# does to the guard plugin's cache directory on a same-version re-add, a version
# upgrade, digest-stamped version strings, and a downgrade.
#
# Usage: KKPROBE_ROOT=<fresh dir> probe-cache.sh
set -uo pipefail
: "${KKPROBE_ROOT:?set KKPROBE_ROOT to a fresh directory}"
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export CODEX_HOME=$KKPROBE_ROOT/home
mkdir -p "$CODEX_HOME"
mkt=$KKPROBE_ROOT/mkt
cache=$CODEX_HOME/plugins/cache/kkprobe/kkprobe-guard

snapshot() {
  echo "-- cache after: $1"
  if [ -d "$cache" ]; then
    for d in "$cache"/*/; do
      d=${d%/}
      printf '  %s  dir_inode=%s  script_inode=%s  variant=%s\n' "$(basename "$d")" \
        "$(stat -c %i "$d")" "$(stat -c %i "$d/scripts/guard.sh" 2>/dev/null || echo -)" \
        "$(sed -n 's/^# kkprobe guard, variant \([a-z]*\).*/\1/p' "$d/scripts/guard.sh" 2>/dev/null)"
    done
  else
    echo "  (no cache dir)"
  fi
}

add_guard() {
  echo "\$ codex plugin add kkprobe-guard@kkprobe --json"
  codex plugin add kkprobe-guard@kkprobe --json 2>&1 | grep -v '^WARNING'
  echo "exit=${PIPESTATUS[0]}"
}

echo "== codex $(codex --version 2>/dev/null)"
"$here/build-marketplace.sh" "$mkt" 1.0.0 1.0.0 a
codex plugin marketplace add "$mkt" --json >/dev/null 2>&1
add_guard; snapshot "first install 1.0.0 (variant a)"

echo; echo "== same version, same bytes, re-added"
add_guard; snapshot "re-add unchanged 1.0.0"

echo; echo "== same version, changed bytes (variant b), re-added"
"$here/build-marketplace.sh" "$mkt" 1.0.0 1.0.0 b >/dev/null
add_guard; snapshot "re-add 1.0.0 with variant b bytes"

echo; echo "== upgrade to 1.0.1 (variant c)"
"$here/build-marketplace.sh" "$mkt" 1.0.0 1.0.1 c >/dev/null
add_guard; snapshot "upgrade to 1.0.1"

digest=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
short=${digest:0:12}
for v in "1.0.1+kk.$short" "1.0.1-kk.$short" "0.0.0-dev.$short" "$digest" "sha256-$short" "local-$short"; do
  echo; echo "== digest-stamped version: $v"
  "$here/build-marketplace.sh" "$mkt" 1.0.0 "$v" d >/dev/null
  add_guard; snapshot "install $v"
done

echo; echo "== downgrade: re-add 1.0.0 with the original variant a bytes"
"$here/build-marketplace.sh" "$mkt" 1.0.0 1.0.0 a >/dev/null
add_guard; snapshot "downgrade to 1.0.0"
echo; echo "== config.toml plugin entries"
grep -A1 'plugins\.' "$CODEX_HOME/config.toml"
