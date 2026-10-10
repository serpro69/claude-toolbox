#!/usr/bin/env bash
set -euo pipefail
TASK12_C2="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK12_PYTHON=/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin/python3.12
[[ $# == 2 ]] || { echo 'usage: run-batch.sh CASE MODE' >&2; exit 2; }
pids=()
for side in baseline candidate; do
  snapshot=/tmp/fr-task12-baseline-20261010
  [[ "$side" != candidate ]] || snapshot=/tmp/fr-task12-candidate2-20261010
  for repetition in 1 2; do
    run_id="claude-${side}-$1-$2-${repetition}"
    evidence="$TASK12_C2/runs/$run_id"
    workspace="/tmp/fr-task12-c2-$run_id"
    "$TASK12_PYTHON" -B "$TASK12_C2/../candidate2_controller.py" prepare "$side" "$1" "$2" \
      "$snapshot" "$workspace" "$evidence" "$TASK12_C2/freeze.json"
    "$TASK12_PYTHON" -B "$TASK12_C2/../candidate2_controller.py" run "$evidence" "$TASK12_C2/freeze.json" &
    pids+=("$!")
  done
done
failed=0
for pid in "${pids[@]}"; do
  if ! wait "$pid"; then failed=1; fi
done
exit "$failed"
