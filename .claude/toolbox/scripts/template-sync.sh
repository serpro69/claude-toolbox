#!/usr/bin/env bash
# Older clients hand control to this file, sometimes from a staged CI tree.
echo "Template sync has retired. Install kk on each machine and run kk migrate in this repository."
for option in "$@"; do
  if [[ $option == --ci && -n ${GITHUB_OUTPUT:-} ]]; then
    printf 'has_changes=false\n' >>"$GITHUB_OUTPUT"
    break
  fi
done

# A released updater delegates its automatic staging cleanup when it execs us.
# Remove only the copied scripts and their empty directories.
handoff_dir=${TEMPLATE_SYNC_HANDOFF_CLEANUP:-}
if [[ ${TEMPLATE_SYNC_NO_HANDOFF:-} == 1 && $handoff_dir =~ ^/tmp/template-sync\.[[:alnum:]]{6}$ &&
      ${BASH_SOURCE[0]} == "$handoff_dir/bin/template-sync.sh" &&
      -O $handoff_dir && ! -L $handoff_dir && -O $handoff_dir/bin && ! -L $handoff_dir/bin ]]; then
  if rm -f -- "$handoff_dir/bin/template-sync.sh" "$handoff_dir/bin/semver-compare.sh"; then
    rmdir -- "$handoff_dir/bin" "$handoff_dir" 2>/dev/null || true
  fi
fi
exit 0
