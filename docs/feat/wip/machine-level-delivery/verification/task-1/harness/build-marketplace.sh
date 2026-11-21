#!/usr/bin/env bash
# Build (or rebuild) the scratch local Codex marketplace used by the Task 1 probes.
#
# Usage: build-marketplace.sh <marketplace-dir> <skills-version> <guard-version> [guard-variant]
#
# Two plugins:
#   kkprobe-skills  skills only, no hooks
#   kkprobe-guard   a PreToolUse hook on Bash that logs every call and denies any
#                   command containing KKPROBE_MARKER (exit 2, reason on stderr)
#
# guard-variant changes the guard script's bytes (and its denial text) without
# changing anything else, so a probe can tell which copy of the hook ran.
# The hook log is $KKPROBE_ROOT/hook.log, baked into the script at build time.
set -euo pipefail

mkt=${1:?marketplace dir}
skills_version=${2:?skills version}
guard_version=${3:?guard version}
variant=${4:-a}
: "${KKPROBE_ROOT:?set KKPROBE_ROOT}"

mkdir -p "$mkt/.agents/plugins"
cat >"$mkt/.agents/plugins/marketplace.json" <<'JSON'
{
  "name": "kkprobe",
  "interface": { "displayName": "kk probe" },
  "plugins": [
    {
      "name": "kkprobe-skills",
      "source": { "source": "local", "path": "./plugins/kkprobe-skills" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    },
    {
      "name": "kkprobe-guard",
      "source": { "source": "local", "path": "./plugins/kkprobe-guard" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
JSON

s="$mkt/plugins/kkprobe-skills"
mkdir -p "$s/.codex-plugin" "$s/skills/kkprobe-hello"
cat >"$s/.codex-plugin/plugin.json" <<JSON
{
  "name": "kkprobe-skills",
  "version": "$skills_version",
  "description": "Task 1 probe: skills only",
  "skills": "./skills/"
}
JSON
cat >"$s/skills/kkprobe-hello/SKILL.md" <<MD
---
name: kkprobe-hello
description: Probe skill for machine-level-delivery Task 1 (skills version $skills_version). Never invoke.
---

# kkprobe-hello

Skills plugin version $skills_version.
MD

g="$mkt/plugins/kkprobe-guard"
mkdir -p "$g/.codex-plugin" "$g/hooks" "$g/scripts"
cat >"$g/.codex-plugin/plugin.json" <<JSON
{
  "name": "kkprobe-guard",
  "version": "$guard_version",
  "description": "Task 1 probe: guard-like PreToolUse hook"
}
JSON
cat >"$g/hooks/hooks.json" <<'JSON'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash \"$PLUGIN_ROOT/scripts/guard.sh\"" }
        ]
      }
    ]
  }
}
JSON
cat >"$g/scripts/guard.sh" <<SH
#!/usr/bin/env bash
# kkprobe guard, variant $variant, built for guard version $guard_version
payload=\$(cat)
cmd=\$(printf '%s' "\$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)
jq -cn --arg variant "$variant" --arg version "$guard_version" \\
  --arg pid "\$\$" --arg ppid "\$PPID" --arg pwd "\$PWD" \\
  --arg plugin_root "\${PLUGIN_ROOT:-}" --arg script "\${BASH_SOURCE[0]}" \\
  --arg ts "\$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \\
  --argjson payload "\$(printf '%s' "\$payload" | jq -c . 2>/dev/null || echo null)" \\
  '{ts:\$ts, variant:\$variant, version:\$version, pid:\$pid, ppid:\$ppid, hook_pwd:\$pwd,
    plugin_root:\$plugin_root, script:\$script, payload:\$payload}' >>"$KKPROBE_ROOT/hook.log"
case "\$cmd" in
  *KKPROBE_MARKER*)
    echo "kkprobe-guard variant $variant (v$guard_version): denied marker command" >&2
    exit 2 ;;
esac
exit 0
SH
chmod +x "$g/scripts/guard.sh"
echo "built $mkt: kkprobe-skills@$skills_version kkprobe-guard@$guard_version variant=$variant"
