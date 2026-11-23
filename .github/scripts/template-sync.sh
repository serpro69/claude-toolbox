#!/usr/bin/env bash
# Workflows from v0.5.0 through v0.15.x download and invoke this file directly.
echo "Template sync has retired. Install kk on each machine and run kk migrate in this repository."
for option in "$@"; do
  if [[ $option == --ci && -n ${GITHUB_OUTPUT:-} ]]; then
    printf 'has_changes=false\n' >>"$GITHUB_OUTPUT"
    break
  fi
done
exit 0
