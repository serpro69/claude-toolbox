#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"
TOOLS_PYTHON="${FUNCTIONAL_REVIEW_PYTHON:-python3}"
command -v "$TOOLS_PYTHON" >/dev/null || { echo "Missing interpreter: $TOOLS_PYTHON" >&2; exit 1; }
"$TOOLS_PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Functional-review tools require Python 3.11+")'
COPY_ROOT="$(mktemp -d)"
trap 'rm -rf "$COPY_ROOT"' EXIT
cp -R "$SCRIPT_DIR/../scripts/functional-review-evals" "$COPY_ROOT/tools"
log_test "Functional-review tools work outside repository and evidence tree"
if (cd "$COPY_ROOT" && "$TOOLS_PYTHON" -I -B -m unittest discover -s tools/tests -v); then
  log_pass "Portable tooling tests passed"
else
  log_fail "Portable tooling tests failed"
fi
print_summary
