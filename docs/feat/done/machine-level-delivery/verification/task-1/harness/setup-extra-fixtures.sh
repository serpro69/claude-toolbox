#!/usr/bin/env bash
# Fixtures for probes 1.6 and 1.7 that live-session steps mcp1, agents and 7 used,
# added to the main scratch home after build-marketplace.sh and the first install:
#   - kkprobe-mcpguard: a plugin whose PreToolUse hook matches an MCP tool with the
#     same regex style as capy's registrations, logs every call, and denies a call
#     carrying KKPROBE_MARKER;
#   - mcp_servers.kkprobe: mcp-echo-server.py, offering the tool kkprobe_echo;
#   - $CODEX_HOME/agents/kk-probe-agent.toml: a user-level sub-agent;
#   - repo-legacy: a trusted project whose hook runs a script from the repository,
#     the way the legacy registrations in .codex/hooks.json do; it switches both
#     probe guard plugins off for itself so only the legacy hook can deny.
#
# Usage: KKPROBE_ROOT=<root of the main scratch home> setup-extra-fixtures.sh
set -euo pipefail
: "${KKPROBE_ROOT:?}"
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export CODEX_HOME=$KKPROBE_ROOT/home
R=$KKPROBE_ROOT

# Appending twice would duplicate TOML tables, which Codex rejects: refuse a re-run.
if grep -q '^\[mcp_servers\.kkprobe\]' "$CODEX_HOME/config.toml" 2>/dev/null || [ -d "$R/mkt/plugins/kkprobe-mcpguard" ]; then
  echo "fixtures already present in $R; not adding them again" >&2; exit 1
fi

m=$R/mkt/plugins/kkprobe-mcpguard
mkdir -p "$m/.codex-plugin" "$m/hooks" "$m/scripts"
cat >"$m/.codex-plugin/plugin.json" <<'EOF'
{ "name": "kkprobe-mcpguard", "version": "1.0.0", "description": "Task 1 probe: PreToolUse hook on an MCP tool" }
EOF
cat >"$m/hooks/hooks.json" <<'EOF'
{ "hooks": { "PreToolUse": [ { "matcher": "^mcp__[^[:space:]]+__kkprobe_echo$",
  "hooks": [ { "type": "command", "command": "bash \"$PLUGIN_ROOT/scripts/guard.sh\"" } ] } ] } }
EOF
cat >"$m/scripts/guard.sh" <<EOF
#!/usr/bin/env bash
payload=\$(cat)
printf '%s\n' "\$payload" | jq -c '{mcpguard: true, tool_name, tool_input}' >> $R/hook.log
case "\$payload" in *KKPROBE_MARKER*) echo "kkprobe-mcpguard: denied MCP marker call" >&2; exit 2;; esac
exit 0
EOF
chmod +x "$m/scripts/guard.sh"
jq '.plugins += [{"name":"kkprobe-mcpguard","source":{"source":"local","path":"./plugins/kkprobe-mcpguard"},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"Productivity"}]' \
  "$R/mkt/.agents/plugins/marketplace.json" >"$R/mkt/m.tmp" && mv "$R/mkt/m.tmp" "$R/mkt/.agents/plugins/marketplace.json"
codex plugin add kkprobe-mcpguard@kkprobe --json 2>/dev/null | jq -c '{pluginId, version}'
printf '\n[mcp_servers.kkprobe]\ncommand = "python3"\nargs = ["-I", "%s/mcp-echo-server.py"]\n' "$here" >>"$CODEX_HOME/config.toml"

mkdir -p "$CODEX_HOME/agents"
cat >"$CODEX_HOME/agents/kk-probe-agent.toml" <<'EOF'
name = "kk-probe-agent"
description = "KKPROBE sub-agent placed in CODEX_HOME/agents for machine-level-delivery Task 1. Replies with the word KKPROBE-AGENT-OK and nothing else."
sandbox_mode = "read-only"
developer_instructions = """
Reply with exactly KKPROBE-AGENT-OK and nothing else.
"""
EOF

p=$R/repo-legacy
mkdir -p "$p/.codex/scripts"
(cd "$p" && git init -q)
cat >"$p/.codex/hooks.json" <<'EOF'
{ "hooks": { "PreToolUse": [ { "matcher": "Bash",
  "hooks": [ { "type": "command", "command": "bash \"$(git rev-parse --show-toplevel)/.codex/scripts/guard.sh\"" } ] } ] } }
EOF
cat >"$p/.codex/scripts/guard.sh" <<EOF
#!/usr/bin/env bash
payload=\$(cat)
printf '%s\n' "\$payload" | jq -c '{legacy: true, cmd: .tool_input.command}' >> $R/hook.log
case "\$payload" in *KKPROBE_LEGACY*) echo "legacy project guard: denied" >&2; exit 2;; esac
exit 0
EOF
printf '[plugins."kkprobe-guard@kkprobe"]\nenabled = false\n\n[plugins."kkprobe-guard@kkprobegit"]\nenabled = false\n' >"$p/.codex/config.toml"
printf '\n[projects."%s"]\ntrust_level = "trusted"\n' "$p" >>"$CODEX_HOME/config.toml"
echo "fixtures ready; review the new hooks in the next TUI session"
