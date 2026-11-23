Sync this repository with the last full template from `v0.26.0-rc.4`.

Legacy repositories can sync to the last full template, `v0.26.0-rc.4`. After retirement the compatibility script directs users to `kk migrate`.

Arguments: $ARGUMENTS

## Process

For a legacy checkout, default to the retirement tag. If the user specifies a version, use their version once. Forward other arguments unchanged.

```bash
.claude/toolbox/scripts/template-sync.sh --local --version v0.26.0-rc.4
```

Common usage:

- `/kk:template:sync` — sync to the last full template
- `/kk:template:sync --version v1.0.0` — sync to a specific version
- `/kk:template:sync --dry-run` — preview changes without applying

## Prerequisites

Requires `jq`, `git`, `curl`, and `yq` (mikefarah/yq). If any are missing the script will report which ones to install.

The repository must have a `.github/template-state.json` manifest — created automatically when the repo was set up from the template.

## After sync

Show the user the script output. If changes were applied, suggest reviewing with `git diff` before committing. If it failed, surface the error message from the script.
