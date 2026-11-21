#!/usr/bin/env bash
set -euo pipefail

root=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
# shellcheck source=klaude-plugin/scripts/release-plugin.sh
source "$root/scripts/release-plugin.sh"

config=${XDG_CONFIG_HOME:-"$HOME/.config"}/kk/config.json
if [[ -e "$config" || -L "$config" ]]; then
    enabled=$(jq -ers '
        if length != 1 or (.[0] | type) != "object" then error("expected one JSON object")
        else .[0] end
        | if has("claude") then .claude else {} end
        | if type != "object" then error("claude must be an object")
          elif has("instructions") then .instructions else true end
        | if type == "boolean" then tostring else error("claude.instructions must be a boolean") end
    ' "$config") || { printf 'kk: invalid instruction override in %s\n' "$config" >&2; exit 1; }
    [[ "$enabled" == true ]] || exit 0
fi

project=${CLAUDE_PROJECT_DIR:-}
if [[ -z "$project" ]]; then
    project=$(jq -r '.cwd // empty')
    project=${project:-$PWD}
fi
repo=$(git -C "$project" rev-parse --show-toplevel 2>/dev/null) || repo=$project

behavior=/dev/null
root_hint=/dev/null
if [[ ! -f "$project/.claude/CLAUDE.extra.md" && ! -f "$repo/.claude/CLAUDE.extra.md" ]]; then
    behavior=$root/instructions/behavior.md
fi
if ! is_release_plugin "$root" &&
        [[ ! -f "$project/.claude/toolbox/CLAUDE.md" && ! -f "$repo/.claude/toolbox/CLAUDE.md" ]]; then
    root_hint=$root/instructions/plugin-root.md
fi
[[ "$behavior" != /dev/null || "$root_hint" != /dev/null ]] || exit 0

jq -nc --rawfile behavior "$behavior" --rawfile root_hint "$root_hint" '
    {hookSpecificOutput: {hookEventName: "SessionStart",
        additionalContext: ([$behavior, $root_hint] | map(select(length > 0)) | join("\n"))}}'
