#!/usr/bin/env bash
# Probe 1.4 (assumption 10), install side: the same guard tree installed from a
# Git marketplace and from a local-path marketplace gets the same plugin ID shape,
# trust key and bundle hash. The Git repository is served over plain HTTP on
# 127.0.0.1 for the duration of the probe (`file://` URLs are rejected). No model
# call. The live-session half (hook runs after one review) is in raw/hook.jsonl.
#
# Usage: KKPROBE_ROOT=<fresh dir> probe-git-source.sh
set -uo pipefail
: "${KKPROBE_ROOT:?set KKPROBE_ROOT to a fresh directory}"
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
port=18766
export GIT_CONFIG_PARAMETERS="'commit.gpgsign=false' 'tag.gpgsign=false'"

src=$KKPROBE_ROOT/gitmkt
"$here/build-marketplace.sh" "$src" 1.0.0 1.0.0 g >/dev/null
jq '.name = "kkprobegit"' "$src/.agents/plugins/marketplace.json" >"$src/m.tmp" \
  && mv "$src/m.tmp" "$src/.agents/plugins/marketplace.json"
(cd "$src" && git init -q -b main && git add -A \
  && git -c user.name=probe -c user.email=probe@example.invalid commit -qm probe)
# Serve a directory that holds only the bare repository, never a CODEX_HOME.
served=$KKPROBE_ROOT/served
mkdir -p "$served"
git clone -q --bare "$src" "$served/gitmkt.git"
(cd "$served/gitmkt.git" && git update-server-info)
python3 -I -m http.server "$port" --bind 127.0.0.1 --directory "$served" >/dev/null 2>&1 &
server=$!
trap 'kill "$server" 2>/dev/null' EXIT
sleep 1
if ! git ls-remote "http://127.0.0.1:$port/gitmkt.git" >/dev/null 2>&1; then
  echo "FAILED: the local HTTP server is not serving the repository" >&2; exit 1
fi

show() {
  python3 -I "$here/hooks-list.py" "$KKPROBE_ROOT/w" 2>/dev/null \
    | jq -r '.response.result.data[0].hooks[] | "  key=\(.key)\n  trustStatus=\(.trustStatus) currentHash=\(.currentHash)"'
}
mkdir -p "$KKPROBE_ROOT/w"

echo "== codex $(codex --version 2>/dev/null)"
for u in "file://$served/gitmkt.git" "http://127.0.0.1:$port/gitmkt.git"; do
  export CODEX_HOME=$KKPROBE_ROOT/home-git; mkdir -p "$CODEX_HOME"
  printf '== marketplace add %s\n  ' "$u"
  codex plugin marketplace add "$u" 2>&1 | grep -v '^WARNING' | tr '\n' ' '; echo
done
if ! codex plugin add kkprobe-guard@kkprobegit --json 2>/dev/null | jq -ce '{pluginId, version}'; then
  echo "FAILED: install from the Git marketplace" >&2; exit 1
fi
show

echo "== same tree from a local path, separate CODEX_HOME"
export CODEX_HOME=$KKPROBE_ROOT/home-local; mkdir -p "$CODEX_HOME"
codex plugin marketplace add "$src" >/dev/null 2>&1
codex plugin add kkprobe-guard@kkprobegit --json 2>/dev/null | jq -c '{pluginId, version}'
show
