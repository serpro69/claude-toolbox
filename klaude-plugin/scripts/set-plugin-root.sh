#!/bin/bash

# SessionStart hook — exports TOOLBOX_PLUGIN_ROOT for the session.
#
# Uses cpr.py (reads installed_plugins.json) as the primary resolver.
# The harness-substituted ${CLAUDE_PLUGIN_ROOT} ($1) is unreliable —
# it resolves to marketplaces/ instead of the versioned cache/ path.
# See anthropics/claude-code#64461

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# cpr.py resolves the install that applies to the current project, so it needs
# to know which project we are in. $CLAUDE_PROJECT_DIR is the canonical project
# root the harness exposes to hooks; fall back to the cwd when it is unset.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
PLUGIN_ROOT=$(python3 "$SCRIPT_DIR/cpr.py" kk "$PROJECT_DIR" 2>/dev/null)

if [ -z "$PLUGIN_ROOT" ] || [ ! -d "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="${1:-}"
fi

if [ -z "$PLUGIN_ROOT" ] || [ ! -d "$PLUGIN_ROOT" ]; then
  exit 0
fi

# Without CLAUDE_ENV_FILE there is nowhere to export to; appending to an empty
# path would be an ambiguous redirect. Nothing to do — exit cleanly.
if [ -z "${CLAUDE_ENV_FILE:-}" ]; then
  exit 0
fi

# `|| true` keeps the hook exit code 0 even if the append fails (e.g. the env
# file is not writable) — a non-zero exit is treated as a hook failure, not a
# no-op.
echo "export TOOLBOX_PLUGIN_ROOT=\"$PLUGIN_ROOT\"" >> "$CLAUDE_ENV_FILE" || true
