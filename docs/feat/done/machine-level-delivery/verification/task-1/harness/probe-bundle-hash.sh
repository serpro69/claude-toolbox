#!/usr/bin/env bash
# Probe: which changes to a plugin bundle change the bundle half of Codex's hook
# trust hash (`currentHash` = <declaration hash>/<bundle hash> in hooks/list).
# Each case starts from the same freshly built guard, changes one thing in the
# marketplace source, re-adds the plugin and reads the hash. No model call.
#
# Usage: KKPROBE_ROOT=<fresh dir> probe-bundle-hash.sh
set -uo pipefail
: "${KKPROBE_ROOT:?set KKPROBE_ROOT to a fresh directory}"
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export CODEX_HOME=$KKPROBE_ROOT/home
mkdir -p "$CODEX_HOME" "$KKPROBE_ROOT/w"
mkt=$KKPROBE_ROOT/mkt
g=$mkt/plugins/kkprobe-guard

fresh() { mv -f "$g/README.md" "$KKPROBE_ROOT/README.removed" 2>/dev/null; "$here/build-marketplace.sh" "$mkt" 1.0.0 1.0.0 a >/dev/null; }
hash_now() {
  codex plugin add kkprobe-guard@kkprobe >/dev/null 2>&1
  python3 -I "$here/hooks-list.py" "$KKPROBE_ROOT/w" 2>/dev/null \
    | jq -r '.response.result.data[0].hooks[] | select(.pluginId == "kkprobe-guard@kkprobe")
             | "\(.currentHash | sub("/.*";"") | .[7:19])… / \(.currentHash | sub(".*/";"") | .[7:19])…  (cache dir \(.sourcePath | sub(".*/kkprobe-guard/";"") | sub("/hooks.*";"")))"'
}
case_() { printf '%-58s ' "$1"; hash_now; }

echo "== codex $(codex --version 2>/dev/null)"
fresh; codex plugin marketplace add "$mkt" >/dev/null 2>&1
case_ "baseline (version 1.0.0)"
fresh; case_ "identical rebuild"
fresh; jq '.version = "9.9.9"' "$g/.codex-plugin/plugin.json" >"$g/p.tmp" && mv "$g/p.tmp" "$g/.codex-plugin/plugin.json"
case_ "manifest version only -> 9.9.9"
fresh; jq '.description = "changed"' "$g/.codex-plugin/plugin.json" >"$g/p.tmp" && mv "$g/p.tmp" "$g/.codex-plugin/plugin.json"
case_ "manifest description only"
fresh; echo extra >"$g/README.md"
case_ "extra file README.md"
fresh; printf '\n# one more line\n' >>"$g/scripts/guard.sh"
case_ "guard script content"
fresh; chmod -x "$g/scripts/guard.sh"
case_ "guard script executable bit removed (source)"
echo "  cache mode after that re-add: $(stat -c %A "$CODEX_HOME"/plugins/cache/kkprobe/kkprobe-guard/1.0.0/scripts/guard.sh)"
fresh; case_ "identical rebuild again"
