#!/usr/bin/env bash
# Runs the kk guard engine tests (test/guard/test_guard.py) under the
# isolated interpreter the hook itself uses. The Python suite owns the
# assertions; this wrapper only exists so `for t in test/test-*.sh` picks it up.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${KK_GUARD_TEST_PYTHON:-python3}"

echo "=== kk guard engine tests ($("$PYTHON" --version 2>&1)) ==="
exec "$PYTHON" -I "$SCRIPT_DIR/guard/test_guard.py"
