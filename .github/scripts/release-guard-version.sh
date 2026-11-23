#!/usr/bin/env bash
# Print the guard version for this release. Only --apply writes the manifest.
set -euo pipefail
semver=${1:?expected release version without v}
mode=${2:?expected --preview or --apply}
case "$mode" in
    --preview|--apply) ;;
    *) echo "Expected --preview or --apply, got: $mode" >&2; exit 2 ;;
esac
release_version='^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$'
[[ $semver =~ $release_version ]] || { echo "Invalid release version: $semver" >&2; exit 2; }

root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
source "$root/.github/scripts/semver-compare.sh"

# A pre-release can be on a different branch, including after a squash merge.
# Choose the highest preceding SemVer across all release tags. When build
# metadata gives two tags equal precedence, prefer the most recently tagged.
tags=$(git tag --list 'v[0-9]*' --sort=-creatordate)
previous=''
for tag in $tags; do
    version=${tag#v}
    [[ $version =~ $release_version ]] || continue
    [[ $version != "$semver" && $(compare "$version" "$semver") != gt ]] || continue
    if [[ -z $previous || $(compare "$version" "${previous#v}") == gt ]]; then
        previous=$tag
    fi
done

prior=$(mktemp -d)
trap 'rm -rf -- "$prior"' EXIT
if [[ -n $previous ]]; then
    entry=$(git ls-tree "refs/tags/$previous" -- kodex-guard)
    if [[ -n $entry ]]; then
        git archive "refs/tags/$previous" kodex-guard | tar -x -C "$prior"
    fi
fi

python3 -I -B - "$root/kk/lib" "$prior/kodex-guard" "$semver" "$mode" <<'PY'
import json
from pathlib import Path
import sys

library, previous, version, mode = sys.argv[1:]
sys.path.insert(0, library)
from guard_identity import MANIFEST, guard_identity, with_version

candidate = Path("kodex-guard")
baseline = Path(previous)
identity = guard_identity(candidate)
if baseline.exists() and guard_identity(baseline) == identity:
    version = json.loads((baseline / MANIFEST).read_bytes())["version"]
manifest = candidate / MANIFEST
original = manifest.read_bytes()
if mode == "--apply" and json.loads(original)["version"] != version:
    manifest.write_bytes(with_version(original, version))
print(version)
PY
