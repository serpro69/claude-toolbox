#!/usr/bin/env bash
# Prepare an empty scratch directory. This script does not modify Claude's configuration.
set -euo pipefail
umask 077
root=$(cd "${1:?pass an empty directory created by mktemp -d}" && pwd -P)
[[ -z $(ls -A "$root") ]] || { echo "Scratch directory must be empty" >&2; exit 1; }

market=$(basename "$root" | tr '[:upper:]' '[:lower:]')
plugin='release-marker'
id="$plugin@$market"
catalog="$root/catalog/.claude-plugin"
mkdir -p "$catalog" "$root/trusted/.claude" "$root/untrusted"
for version in 1.0.0 2.0.0; do
    release="$root/catalog/releases/$version"
    mkdir -p "$release/.claude-plugin" "$release/hooks"
    jq -n --arg name "$plugin" --arg version "$version" \
        '{name: $name, version: $version, description: "Local release marker"}' \
        > "$release/.claude-plugin/plugin.json"
    jq -n --arg cmd 'bash "${CLAUDE_PLUGIN_ROOT}/record.sh"' \
        '{hooks: (["SessionStart", "UserPromptSubmit", "SessionEnd"] | map({
            key: ., value: [{hooks: [{type: "command", command: $cmd}]}]
        }) | from_entries)}' > "$release/hooks/hooks.json"
    {
        printf 'probe_root=%q\n' "$root"
        cat <<'HOOK'
set -eu
[[ "$(pwd -P)" == "$probe_root/trusted" ]] || exit 0
jq -c --arg script "$(realpath "$0")" --arg root "$CLAUDE_PLUGIN_ROOT" \
    '{session_id, hook_event_name, script: $script, root: $root}' >> "$probe_root/events.jsonl"
HOOK
    } > "$release/record.sh"
    jq -n --arg name "$market" --arg plugin "$plugin" --arg source "./releases/$version" \
        '{name: $name, owner: {name: "Task 2 probe"}, plugins: [{name: $plugin, source: $source}]}' \
        > "$root/marketplace-$version.json"
done
cp "$root/marketplace-1.0.0.json" "$catalog/marketplace.json"
jq -n --arg id "$id" '{enabledPlugins: {($id): true}}' > "$root/project-enabled.json"
jq -n --arg id "$id" '{enabledPlugins: {($id): false}}' > "$root/plugin-off.json"
jq -n '{disableAllHooks: true, permissions: {deny: ["Read(./denied-marker.txt)"]},
    statusLine: {type: "command", command: "echo KK-TASK2-STATUS"}}' > "$root/layer.json"
jq 'del(.disableAllHooks)' "$root/layer.json" > "$root/status-layer.json"
# Sibling control and denied file are equally readable by the OS and contain only test data.
printf '%s\n' 'public control mint' > "$root/untrusted/control-marker.txt"
printf '%s\n' 'public fixture coral' > "$root/untrusted/denied-marker.txt"
printf 'Marketplace: %s\nPlugin: %s\n' "$market" "$id"
