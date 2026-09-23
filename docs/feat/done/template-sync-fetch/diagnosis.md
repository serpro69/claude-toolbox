# Template sync fetch stall

Investigated on 2026-09-23 with Git 2.55.0 against
`serpro69/claude-toolbox` at `b7636162dfc732792c1d1930a5a7e3eb7b8bf2c6`.

## Evidence

- The reported downstream sync was canceled by the user; it did not complete.
- The sync script is byte-identical between the downstream manifest version
  `9a164f2bb677120464e47de51c8807997db81528` and the target commit.
- A separate diagnostic clone using `--depth 1 --filter=blob:none` downloaded
  metadata, then stalled for minutes during the checkout's lazy blob fetch.
  That diagnostic clone eventually exited successfully.
- A plain shallow clone without the blob filter completed promptly, downloading
  approximately 1.72 MiB of packed objects. A later plain-clone control stalled
  and was terminated at the diagnostic's 45-second limit. Removing the filter
  is therefore not a reliable workaround.
- A filtered clone with `-c http.version=HTTP/1.1` also completed promptly.
  Both filtered diagnostics set `http.lowSpeedLimit=1024` and
  `http.lowSpeedTime=30`; the slow default-transport clone still completed later.
  The user's subsequent full sync with HTTP/1.1 also stalled; the protocol
  override is not a reliable workaround.
- The user successfully synced `latest` (`v0.21.1`) in 19 seconds, including
  two fetches due to the script handoff, then reproduced the stall with `master`.
  Those versions have identical fetch implementations; their sync scripts differ
  only in two default-model strings. Both initially clone the default branch
  before fetching the requested version.
- Inspection of the restarted `master` run found it inside that initial clone,
  specifically the lazy fetch of 749 blobs. It had not reached the script's
  explicit fetch of the requested SHA. A one-second sample of `git-remote-https`
  found its main thread in `post_rpc` / `run_active_slot` / `__select` throughout.
- [GitHub Status](https://www.githubstatus.com/) reported Git Operations as
  operational at investigation time. This does not rule out a localized problem.

These observations point to an intermittent Git/HTTPS transfer problem, rather
than a recent sync-script regression or a master-specific fetch path. They do
not distinguish a GitHub backend problem from a local client or network problem.
Neither HTTP/1.1 nor removing the partial-clone filter reliably avoids it.

## Alternating version comparison

The user reports that `latest` succeeds consistently while `master` stalls.
To test that observation, the unchanged script's `resolve_version` and
`fetch_upstream_templates` functions were run in alternating order, using fresh
temporary directories, Git Trace2 event logs, and a 30-second timeout per run.
These tests cover resolution and fetch, not the full downstream apply flow.

| Working directory | Requested version | Result |
| --- | --- | --- |
| claude-toolbox | latest, first run | Timed out at 30 seconds |
| claude-toolbox | master, first run | Completed in 7.77 seconds |
| claude-toolbox | latest, second run | Timed out at 30 seconds |
| claude-toolbox | master, second run | Completed in 6.94 seconds |
| wlcm-payments | latest | Completed in 8.43 seconds |
| wlcm-payments | master | Timed out at 30.01 seconds |

The downstream-directory pair reproduced the user's split, while the earlier
pairs produced the reverse. This is evidence that the version label alone does
not explain the outcome, but the cause of the user's consistent pattern remains
unresolved. Do not present network intermittency as a proven root cause.

The downstream `master` trace stopped inside the initial clone's lazy fetch of
749 blobs, before the explicit target-SHA fetch. The second failed `latest`
trace stopped in that same lazy-fetch operation. The first failed `latest` run
spent approximately 26 seconds receiving the initial metadata pack, then reached
clone checkout hooks just before its timeout. Thus slow progress and stalled
blob download can both appear as the same silent "Fetching templates" message.

Trace directories (temporary, on the investigation machine):
`/tmp/template-sync-compare.iqmOnF` and
`/tmp/template-sync-downstream-compare.5AMl8y`.

## Workaround

Use one persistent, complete local checkout as the source for multiple downstream
projects. A full dry run from `wlcm-payments`, using the local `claude-toolbox`
checkout below, exited successfully and reported eight files to update. This
bypasses HTTPS and does not require a separate download for each project.

Run this from each downstream project's root:

```bash
GIT_CONFIG_COUNT=1 \
GIT_CONFIG_KEY_0=url.file:///Users/sergio/Projects/personal/claude-toolbox.insteadOf \
GIT_CONFIG_VALUE_0=https://github.com/serpro69/claude-toolbox.git \
.claude/toolbox/scripts/template-sync.sh --local \
  --version b7636162dfc732792c1d1930a5a7e3eb7b8bf2c6 --dry-run
```

After reviewing the dry run, the same invocation without `--dry-run` applies
the pinned version. Only the dry run was executed by the agent. Update the shared
checkout once before a future batch and use the desired commit SHA for every
project in that batch. The checkout must contain the required objects locally;
uncommitted edits are not included. This leaves global Git configuration unchanged.
If the shell already supplies
`GIT_CONFIG_COUNT` entries, append the override to those entries instead of
replacing them.

At the final follow-up, no live sync process remained and the downstream manifest
recorded `b7636162dfc732792c1d1930a5a7e3eb7b8bf2c6`. The working tree contained the
eight template updates plus the manifest change. This is consistent with the
previously running user-initiated sync completing; its exit status was not
captured by the agent. The user also reported that the issue seemed network-related.

## Deferred script improvements

Implementation is deferred because this investigation diagnoses the reported
stall; it does not establish a permanent transport-policy change.

- Expose clone/fetch progress and preserve failure diagnostics. Currently
  `--quiet 2>/dev/null` hides the stage and any underlying error.
- Bound stalled operations: the retry loop only advances after Git exits.
  Validate any timeout against a deliberately stalled transfer.
- Configure sparse checkout before materializing files, or evaluate using a
  plain shallow clone. Currently clone checks out the entire tree before sparse
  checkout is configured, triggering a second download despite the blob filter.
  Verify required template paths and pinned-version behavior before changing it.
- Fix the sparse-checkout invocations: `git sparse-checkout init` and `set` do
  not accept `--quiet` on Git 2.55.0. These explain the warnings after successful
  downloads, not the network stall. Also validate the file-level selections
  against cone-mode directory requirements when correcting those commands.

## Consumer documentation

The reusable workaround is documented in the published
[Template Sync guide](../../../user-guide/template-sync.md#sync-stalls-at-fetching-templates).
It covers source prerequisites, a pinned commit, preview and apply, reuse across
projects, configuration scope, and optional timeout behavior.

The new section passes standalone Markdownlint checks (heading levels adjusted
for extraction), its shell examples pass `bash -n`, and `git diff --check` passes.
The full guide had 38 default Markdownlint findings before this edit, including
long lines and mixed code-block styles from MkDocs tabs. Formatting cleanup was
deferred to keep this change focused: establish a MkDocs-aware lint configuration
and address the existing guide formatting in a separate change.
