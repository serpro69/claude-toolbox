#!/usr/bin/env bash
# Run one declared case/mode with two fresh sessions on each side.
# Child processes have disjoint actor/evidence directories; wait for every job.
set -euo pipefail
TASK12_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK12_PYTHON=/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin/python3.12
if [[ $# != 3 ]]; then
  echo 'usage: run-claude-batch.sh CASE MODE FREEZE' >&2
  exit 2
fi
case_id="$1"
mode="$2"
freeze="$3"
pids=()
for side in baseline candidate; do
  snapshot=/tmp/fr-task12-baseline-20261010
  [[ "$side" != candidate ]] || snapshot=/tmp/fr-task12-candidate1-20261010
  for repetition in 1 2; do
    run_id="claude-${side}-${case_id}-${mode}-${repetition}"
    evidence="$TASK12_DIR/runs/$run_id"
    workspace="/tmp/fr-task12-$run_id"
    "$TASK12_PYTHON" -B "$TASK12_DIR/controller.py" prepare "$side" "$case_id" "$mode" \
      "$snapshot" "$workspace" "$evidence" "$freeze"
    "$TASK12_PYTHON" -B "$TASK12_DIR/controller.py" run "$evidence" "$freeze" &
    pids+=("$!")
  done
done
failed=0
for pid in "${pids[@]}"; do
  if ! wait "$pid"; then
    failed=1
  fi
done
exit "$failed"
