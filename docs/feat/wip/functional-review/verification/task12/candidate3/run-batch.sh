#!/usr/bin/env bash
# Isolated/implementation captures are serialized to avoid shared /tmp artifacts.
set -euo pipefail
TASK12_C3="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK12_PYTHON=/home/sergio/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/bin/python3.12
[[ $# == 2 ]] || { echo 'usage: run-batch.sh CASE MODE' >&2; exit 2; }
for side in baseline candidate; do
  snapshot=/tmp/fr-task12-baseline-20261010
  [[ "$side" != candidate ]] || snapshot=/tmp/fr-task12-candidate3-20261010
  for repetition in 1 2; do
    run_id="claude-${side}-$1-$2-${repetition}"
    evidence="$TASK12_C3/runs/$run_id"
    workspace="/tmp/fr-task12-c3-$run_id"
    "$TASK12_PYTHON" -B "$TASK12_C3/../candidate3_controller.py" prepare "$side" "$1" "$2" \
      "$snapshot" "$workspace" "$evidence" "$TASK12_C3/freeze.json"
    "$TASK12_PYTHON" -B "$TASK12_C3/../candidate3_controller.py" run "$evidence" "$TASK12_C3/freeze.json"
  done
done
