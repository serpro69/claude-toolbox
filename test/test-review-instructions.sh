#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"
log_test "Review instruction packet contract"
if python3 -B "$SCRIPT_DIR/review_instructions_test.py"; then
  log_pass "Instruction packet tests passed"
else
  log_fail "Instruction packet tests failed"
fi
print_summary
