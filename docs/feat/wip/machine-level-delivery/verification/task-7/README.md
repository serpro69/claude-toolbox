# Codex guard plugin verification

Linux, 2026-11-20. The guard plugin uses the launch workspace for policy and capy registration. Bash and patch operands use the tool’s requested directory. The capy adapter retains capy’s project-relative path conventions.

| Check | Observed result |
| --- | --- |
| `bash test/test-codex-hooks.sh` | Both the template and plugin adapter cases passed. The plugin’s registered commands ran from a workspace subdirectory with operands in a second repository. Only the launch repository supplied the policy and capy registration. A separate case passed outside Git. |
| Structure, generated artifacts and legacy guard | The Codex structure, plugin structure, generator and guard engine suites passed. In an isolated candidate checkout, `make check-guard` regenerated and verified the tracked artifacts. |
| `bash test/test-kk.sh` | 26 tests passed on CPython 3.8.20 (`e714b651-e2b3-4193-9a96-1d79fc6438ad`) and 3.11.13 (`b2b30e55-8e7d-4fcc-b31f-8e95ada86fc4`). The installer rejected a missing fourth directory and a non-object guard manifest. The identity tests covered version-only edits, other manifest bytes, adapter bytes, archive modes, relative paths, and agreement between a checkout and an extracted tag. |
| Repository suites | 16 of 17 passed with Python 3.11 and jq 1.6. The template-sync suite reproduced the previously recorded malformed-base diagnostic assertion. [Baseline](../task-3/README.md) |

## Installed bundle

Codex CLI 0.171.0 registered the checkout as a local marketplace and installed `kk-guard@claude-toolbox` version `0.25.4` in a disposable Codex home. The app-server’s `hooks/list` from `workspace/sub` reported the Bash, patch and capy handlers from the installed plugin. Before review, each was enabled with trust status `untrusted`.

The workspace root contained a `.claude/kk-guard.json` adding the synthetic marker `./**/task7-marker.txt`. Both that marker and a public control file existed in the subdirectory. Directly invoking the Bash command reported by Codex from that subdirectory returned 0 for the control, 2 with the project rule for the marker, and 0 for a second control. The installed bundle hash remained unchanged and no bytecode was created. Capture `4a67c95d-e67f-4361-8ce6-dced9ad08eaf` records that direct check. A separate loopback Responses fixture successfully requested a public control through a real `codex exec` process in a scratch home without plugins.

With the maintainer’s approval, the three installed handlers were reviewed in Codex’s interactive hook dialog in this disposable home. A real `codex --no-daemon exec --ephemeral --json` session ran from `workspace/sub` in a read-only sandbox. A loopback Responses fixture requested `cat ./task7-control.txt` followed by `cat ./task7-marker.txt` in the same turn. The first command returned `TASK7_PUBLIC_CONTROL` with exit 0. Codex blocked the second through `PreToolUse`, and the tool result named the workspace rule `./**/task7-marker.txt`. The marker contents never appeared in the result. The session exited successfully.

Before and after both calls, `hooks/list` reported all three handlers enabled and trusted with the same hashes. The final vendor bundle hash was `sha256:4184dd0b19b74e842bc5c78af0d0d8fac991430936f04d3859e54af5125d1013`. The standalone toolbox identity matched across the checkout and the installed bundle. Capture `f73c83f2-06ee-4263-b3b5-7c5bd3a7a61d` records the live outcomes. The probe used Codex’s normal trust workflow and no account credentials.

## Scope

The required fourth directory takes effect before the first public `kk` tag. The old three-directory development CLI can stage only its own declared layout and refuses a four-directory candidate. The new layout was exercised through a fresh install. Task 10 owns machine-managed guard installation and trust reporting, and Task 12 owns release-time version selection.
