#!/usr/bin/env bash
# Codex Edit|Write aliases deliver the canonical apply_patch payload unchanged.
set -Eeuo pipefail

fail_closed() {
  trap - ERR
  printf '%s\n' 'kk guard: failure — Codex patch adapter could not run; nothing was executed; repair the hook' >&2
  exit 2
}
trap fail_closed ERR HUP INT TERM
exec 3<&0 || fail_closed

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=kodex-guard/scripts/workspace.sh
source "$SCRIPT_DIR/workspace.sh"
REPO_ROOT=$(guard_workspace) || fail_closed
export KK_GUARD_PROJECT_ROOT="$REPO_ROOT"
if bash "$SCRIPT_DIR/guard/guard.sh" --no-bytecode <&3; then
  exit 0
else
  status=$?
  # Exit 2 is a guard denial, already explained on stdout and stderr.
  if [[ "$status" == 2 ]]; then
    exit 2
  fi
  fail_closed
fi
