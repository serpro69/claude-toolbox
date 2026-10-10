#!/usr/bin/env bash
# Reuse declared matching baseline pairs only when the caller selects candidate.
set -euo pipefail
TASK12_C4="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK12_PYTHON=/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin/python3.12
[[ $# == 2 || $# == 3 ]] || { echo 'usage: run-batch.sh CASE MODE [baseline|candidate]' >&2; exit 2; }
sides=(baseline candidate)
if [[ $# == 3 ]]; then
  [[ "$3" == baseline || "$3" == candidate ]] || exit 2
  sides=("$3")
fi
for side in "${sides[@]}"; do
  snapshot=/tmp/fr-task12-baseline-20261010
  [[ "$side" != candidate ]] || snapshot=/tmp/fr-task12-candidate4-20261010
  for repetition in 1 2; do
    run_id="claude-${side}-$1-$2-${repetition}"
    evidence="$TASK12_C4/runs/$run_id"
    workspace="/tmp/fr-task12-c4-$run_id"
    "$TASK12_PYTHON" -B "$TASK12_C4/../candidate4_controller.py" prepare "$side" "$1" "$2" \
      "$snapshot" "$workspace" "$evidence" "$TASK12_C4/freeze.json"
    "$TASK12_PYTHON" -B "$TASK12_C4/../candidate4_controller.py" run "$evidence" "$TASK12_C4/freeze.json"
  done
done
