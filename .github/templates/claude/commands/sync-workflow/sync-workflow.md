Update the local template-sync workflow and script from the upstream template repository.

Arguments: $ARGUMENTS

Run the sync script, passing `$ARGUMENTS` as the version (defaults to `latest` if empty):

```bash
bash .claude/scripts/sync-workflow.sh $ARGUMENTS
```

Supported versions: `latest` (default, resolves the most recent tag), `master`, or a specific tag (e.g. `v0.3.0`).

After the script completes, show the user the output. If it failed, suggest they check network connectivity or try a specific version tag.
