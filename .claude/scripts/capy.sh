#!/usr/bin/env bash

set -euo pipefail

for p in "$(command -v capy 2>/dev/null || true)" "$HOME/.local/bin/capy" "/opt/homebrew/bin/capy" "/usr/local/bin/capy" "$HOME/go/bin/capy" "capy"; do
  [ -n "$p" ] && [ -x "$p" ] && exec "$p" "$@"
done

echo 'capy not found' >&2
exit 1
