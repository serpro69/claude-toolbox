#!/bin/bash

# SessionStart hook — exports TOOLBOX_PLUGIN_ROOT for the session.
#
# A managed release loads in place. Git-marketplace installs need cpr.py
# because the path supplied by the harness can refer to the marketplace.
SCRIPT_DIR=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 1
# shellcheck source=klaude-plugin/scripts/release-plugin.sh
source "$SCRIPT_DIR/release-plugin.sh" || exit 1

# cpr.py resolves the install that applies to the current project, so it needs
# to know which project we are in. $CLAUDE_PROJECT_DIR is the canonical project
# root the harness exposes to hooks; fall back to the cwd when it is unset.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
PLUGIN_ROOT=${SCRIPT_DIR%/*}
if ! is_release_plugin "$PLUGIN_ROOT"; then
  PLUGIN_ROOT=$(python3 -I "$SCRIPT_DIR/cpr.py" kk@agentstakk "$PROJECT_DIR" 2>/dev/null)
  if [ -z "$PLUGIN_ROOT" ] || [ ! -d "$PLUGIN_ROOT" ]; then
    PLUGIN_ROOT="${1:-}"
  fi
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
printf 'export TOOLBOX_PLUGIN_ROOT=%q\n' "$PLUGIN_ROOT" >> "$CLAUDE_ENV_FILE" || true
