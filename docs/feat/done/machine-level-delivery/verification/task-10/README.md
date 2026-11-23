# Offline Codex recovery

On 2026-11-21, Codex CLI 0.171.0 and Claude Code 2.1.296 installed two local releases in a disposable Linux home. Every upgrade and rollback ran under `unshare -Urn`. The network namespace contained only an inactive loopback interface. Both vendors read the marketplace from disk.

The first install reported all three Codex handlers as untrusted. The operator selected **Trust all and continue** in the normal Codex terminal prompt. Both demonstrations used that one decision. Release B added a comment to A’s shell adapter. Codex reported the following installed versions.

| Release | Skills | Guard |
| --- | --- | --- |
| A | 0.25.4 | 0.25.4+kk.2e86fba86e49 |
| B | 0.25.4 | 0.25.4+kk.59154bf4fc00 |

## Demonstration 2 — interrupted activation

The operator confirmed the changed guard. A fixture wrapper ran the real `codex plugin add kk-guard@toolbox --json`, then exited 79 before the installer received its success response. The journal still named A as active and the candidate as `activating` at `codex-add-kk-guard`. Codex’s inventory already showed B’s guard.

The first offline rollback also encountered the fixture interruption after the vendor restored A’s cache. Removing the interruption and repeating the same rollback completed recovery. The candidate cleared, both vendors reported ready, and the inventory showed A’s guard again. A fresh `kk codex exec` session received this tool result from Codex.

```text
Command blocked by PreToolUse hook: kk guard: destructive — privilege: sudo runs a command as the administrator.
```

## Demonstration 4 — promoted CLI unavailable

A second upgrade promoted B as `local-460a0b6e54ef4f0eb58e0706300025ee`. Codex was awaiting review. The operator left B unreviewed, moved its entire `kk/lib` directory out of the release, and executed the recovery command printed at promotion.

```sh
unshare -Urn "$KK_HOME/releases/local-b6e8ecaba013482ba49a0a379ce683ba/kk/bin/kk" rollback
```

Rollback warned about open sessions, completed without a prompt, and reported `codex: ready`. The journal and both vendor inventories identified A. A new wrapped Codex session received the same guard denial for `sudo --version`.

## Repeat after the review fixes

Both demonstrations passed again with the revised installer. A one-shot fixture interrupted only the upgrade this time. The table records the journal immediately before recovery and the vendor-assigned thread ID for each subsequent denial. Both rollbacks ran in a new network namespace, restored `local-66bbb48c63ff4e74a118171dbab9585b`, cleared the candidate and reported `codex: ready`. Capture `6b35f3e5-c27d-4484-9bfc-9c5f84e0acd7` exited 0.

| Case | State immediately before rollback | Codex thread that received the guard denial |
| --- | --- | --- |
| Interrupted upgrade | Candidate `local-200c23ae65c24898ae28811b6ff31ffc` was activating at `codex-add-kk-guard`. The vendor had installed B. | `01a1fe24-b36c-7311-8092-25b3ad6dfca3` |
| Promoted CLI unavailable | Active `local-94bab92d130145c1ba3dad2c6cd941a8` was awaiting review. Its `kk/lib` directory had been moved. | `01a1fe24-db66-7e31-945a-721f7e41679b` |

On restored A, a separate offline check replayed `-c features.hooks=false` for `exec` and `--disable hooks` for `review`. Both wrapped invocations refused and named the three absent handlers. Machine status reported ready before and after. Capture `3155a354-a5f1-4e9d-bd08-be69507326e0` records the check.

The tag-after-local check fed a local archive of the candidate to the tagged upgrade path, using its manifest version `v0.25.4`. This exercised the local-stamp transition without fetching or publishing a Git tag. After promotion, Codex thread `01a1fe2c-401f-7f41-96da-cd873797e672` returned the guard’s denial. The cached guard manifest had inode 2786712 before activation and after the session. Capture `dfd7a26b-511c-4aac-b6e3-694893a5b3fc` exited 0.

## Evidence boundary

The post-recovery turns used a loopback-only model fixture that requested the read-only version query and recorded Codex’s actual tool response. The fixture supplied model output only. Codex loaded the installed plugin, evaluated its persisted trust, invoked its adapter, and returned the denial. Neither run used a trust override. The capture IDs are `32420740-7e91-420b-9792-03452110d856` for the interrupted upgrade and first rollback attempt, and `3656b3b1-7e1a-4955-b760-ade8ece1df42` for completion and the post-promotion recovery. These results cover fresh sessions on this Linux machine. [Open-session probe results](../task-1/README.md#rollback-across-a-guard-change-assumption-14)
