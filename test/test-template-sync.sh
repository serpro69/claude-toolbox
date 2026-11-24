#!/usr/bin/env bash
# A supported legacy client must hand off without applying the retired template.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
sync=.claude/toolbox/scripts/template-sync.sh
old_ci_sync=.github/scripts/template-sync.sh
fixture=$(mktemp -d)
trap 'rm -rf -- "$fixture"' EXIT
cd "$fixture"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_AUTHOR_NAME=Fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

# The installed notice also works in shallow checkouts with no release tags.
GITHUB_OUTPUT="$fixture/output" bash "$root/$sync" --apply --ci --version latest | grep -F 'kk migrate'
test "$(cat "$fixture/output")" = has_changes=false

# Workflows from v0.5.0 through v0.15.x fetch and invoke the old path directly.
# They can download just this one script, so exercise it without siblings.
mkdir -p .github/scripts
cp "$root/$old_ci_sync" "$old_ci_sync"
chmod +x "$old_ci_sync"
GITHUB_OUTPUT="$fixture/old-ci-output" "$old_ci_sync" --version latest --ci --output-dir .github/sync-staging | grep -F 'kk migrate'
test "$(cat "$fixture/old-ci-output")" = has_changes=false
test ! -e .github/sync-staging

python3 -I -B "$root/kk/lib/run.py" migrate --help | grep -F 'v0.26.0+retirement.1'

# Exercise handoff from the original released updater, as installed downstream.
tag=v0.26.0-rc.4
if ! git -C "$root" rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "Skipped released-client handoff: fetch tag $tag to exercise it." >&2
  exit 0
fi

git init -q upstream
mkdir -p "upstream/$(dirname "$sync")"
cp "$root/$sync" "upstream/$sync"
git -C upstream add .
git -C upstream commit -qm 'Retired template'
git -C upstream tag v0.26.0
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="url.file://$fixture/upstream.insteadOf"
export GIT_CONFIG_VALUE_0=https://github.com/example/toolbox.git

git init -q downstream
cd downstream
mkdir -p .github "$(dirname "$sync")"
git -C "$root" show "$tag:.github/template-state.example.json" |
  jq '.upstream_repo = "example/toolbox"' > .github/template-state.json
for file in template-sync.sh semver-compare.sh; do
  git -C "$root" show "$tag:${sync%/*}/$file" > "${sync%/*}/$file"
done
echo 'adopter settings' > keep.txt
git add .
git commit -qm 'Existing template checkout'

notice=$(bash "$sync" --local --version v0.26.0)
printf '%s\n' "$notice" | grep -F 'kk migrate'
handoff_dir=$(awk '$1 == "Staging" && $2 == "dir:" { print $3 }' <<<"$notice")
[[ $handoff_dir =~ ^/tmp/template-sync\.[[:alnum:]]{6}$ ]]
test ! -e "$handoff_dir"
test -z "$(git status --porcelain)"
stage="$fixture/stage"
mkdir -p "$stage/substituted/claude/toolbox/scripts"
cp "$root/$sync" "$stage/substituted/claude/toolbox/scripts/"
printf 'caller-owned\n' > "$stage/keep.txt"
GITHUB_OUTPUT="$fixture/handoff-output" bash "$sync" --apply --ci --version v0.26.0 --output-dir "$stage" | grep -F 'kk migrate'
test "$(cat "$fixture/handoff-output")" = has_changes=false
test "$(cat "$stage/keep.txt")" = caller-owned
test -f "$stage/bin/template-sync.sh"
test -z "$(git status --porcelain)"
echo 'Released client handed off in local and staged CI modes.'
