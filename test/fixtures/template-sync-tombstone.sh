#!/usr/bin/env bash
# Older clients hand control to this file, sometimes from a staged CI tree.
echo "Template sync has retired. Install kk on each machine and run kk migrate in this repository."
for option in "$@"; do
  if [[ $option == --ci && -n ${GITHUB_OUTPUT:-} ]]; then
    printf 'has_changes=false\n' >>"$GITHUB_OUTPUT"
    break
  fi
done
exit 0
