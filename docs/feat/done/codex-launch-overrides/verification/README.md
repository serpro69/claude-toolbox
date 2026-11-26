# Real-Codex verification

Linux, 2026-11-26. Codex CLI 0.172.0, the maintainer's real `~/.codex` (`CODEX_HOME` unset), Python 3.10.12. kk was upgraded twice from the `feat/codex_overrides` checkout with `kk upgrade --local .`: first at 98cc863e (release `local-4aea9136…`), then from the same commit plus the two changes this verification led to (release `local-bf96292a…`, see [Changes made](#changes-made)). The previous release was `v0.26.1`.

The maintainer drove every interactive Codex step. The agent ran the upgrades, the batch launches and the configuration reads. Raw command output stayed in `~/.cache/kk-task6/` on that machine and is not part of the repository; the lines that matter are quoted here.

## Results

| Check | Observed result |
| --- | --- |
| Upgrade removes the managed profile (6.1) | `kk upgrade --local .` exited 0 and printed once: `kk: removed the managed Codex profile /home/sergio/.codex/kk.config.toml; kk codex now passes its settings as launch flags. A model or hook approval Codex saved in that profile no longer applies: choose it again in plain codex, or set it in config.toml.` The file is gone, `state.json` lists it in neither `codex_paths` nor `installed_paths`, `config.toml` was byte-identical before and after, and the guard needed no new review (same guard identity). The profile was in its generated form, so no saved choice was lost. The second upgrade printed no notice. |
| #206 reproduction (6.2) | In a scratch repository with a new `SessionStart` hook: interactive `kk codex`, trust the project, approve the hook, switch `/model` to `gpt-6-sol` with high effort, exit. Without `kk apply`, `kk codex exec "echo ok"` exited 0 and `kk status --live` reported `codex live: ok (guard denied the canary read)` and `claude live: ok (guard denied the canary read)`. Both were repeated on the second release with the same result. |
| The saved model is the one a batch run uses (success criterion 3) | The `exec` header showed `model: gpt-6-sol` and `reasoning effort: high`. |
| Where choices are saved (6.3, assumption 3) | All in `~/.codex/config.toml`: `model` and `model_reasoning_effort` at the top level, a `[projects."<repository>"]` table with `trust_level = "trusted"`, and a `[hooks.state."<repository>/.codex/hooks.json:session_start:0:0"]` table with a `trusted_hash`. Nothing was session-only, and `kk.config.toml` was not recreated. A wrapped session therefore saves hook trust where plain Codex keeps it. |
| A disabled guard handler blocks a batch launch (6.4, assumption 1) | With the guard's `Bash` handler switched off in plain `codex` `/hooks`: `kk codex exec "echo ok"` exited 1 before any session started, with `kk: Codex guard awaiting review for "…/hook-repo": Bash: disabled; enable it in /hooks in plain codex (without --profile)`; `kk status` reported `codex: awaiting review`. After re-enabling it the same command exited 0 and the `PreToolUse` hook ran. Codex records the toggle as an `enabled` line in the handler's `[hooks.state]` table in `config.toml`. |
| Origin lookup time (6.5, assumption 2) | `config/read` through `codex_app.layers`, six runs each: 0.19–0.30 s with the agentstakk repository as the directory (192 origin keys), 0.15–0.16 s in `/tmp` (184 keys). Four `hooks/list` reads took 0.17–0.18 s. Within the assumed 0.2–0.4 s. |

On this machine `config.toml` already sets the model group and every `tui` value kk has a default for, so kk passed three flags: `project_doc_max_bytes`, `agents` and `developer_instructions`. The run exercised yielding more than passing; the passing side rests on the Task 2 and Task 4 probes and tests.

## Other observations

**Flag order across `exec`.** Root-level and `exec`-level `-c` flags form one ordered list, and `app-server` given the same flags in the same order agrees (scratch `CODEX_HOME`, no credentials). `codex -c sandbox_workspace_write.network_access=true exec -c 'sandbox_workspace_write={writable_roots=["/opt"]}'` ran without network access and `config/read` reported `network_access: false`; with the flags swapped, both reported it enabled. The sandbox table was used because the `exec` header prints it. `features.hooks` against a `features` inline table was not observed in `exec` directly.

**Shared background server.** Codex 0.172 attaches the session TUI to a shared background `app-server`. With `-c` flags it starts a server of its own and warns: `Running without the shared background server: command-line configuration overrides (-c, --enable, --disable, or --search) requires embedded mode.` The managed profile caused the same warning with `--profile` as the reason ([#205](https://github.com/serpro69/agentstakk/issues/205)), so this limitation is not new. The maintainer observed that `codex --no-daemon -c …` and `kk codex --no-daemon` start without the warning. In a scratch home `--no-daemon` was accepted before every command tried, including `exec`; given twice it is a usage error; with `--remote` Codex refuses to start. Read from the binary's strings and not run: `remote-control` and `queue` refuse it as well. Not probed: whether `kk codex queue` and `kk codex agents` work at all with kk's flags.

**Managed layer.** A system `managed_config.toml` outranks `-c`. With `/etc/codex/managed_config.toml` containing `project_doc_max_bytes = 12345` (created and removed by the maintainer), `config/read` reported 12345 with origin `legacyManagedConfigTomlFromFile` with and without `-c project_doc_max_bytes=65536`, in the real home and in an empty one. Only a key without an alias was tried. `kk apply` was not run with the file present; a test with the fake Codex reproduced the refusal the name check gave before the change below (`does not report project_doc_max_bytes … it reported no other name instead`).

## Changes made

Both were decided by the maintainer during this verification and are recorded in design.md and in the Task 6 execution context.

- Session launches that carry kk flags now start with `--no-daemon`, and the apply-time `debug prompt-input` run includes it. kk tells a session launch from other commands by a list of Codex 0.172 subcommands; `execpolicy` and `responses-api-proxy`, which `codex --help` does not list, were found by trying names and added after the review, so the installed second release does not have them yet (`execpolicy` accepts the flag anyway). The second upgrade validated with the real Codex, and `kk codex --version` and `kk codex login status` work through the new launcher. The maintainer then started interactive `kk codex` from the second release in the scratch repository: the warning no longer appears.
- The apply-time name check accepts a setting that Codex reports under kk's name from any layer, so a managed pin no longer stops `kk apply`.

## Limits

- One machine, one Codex version, one account. The `kk migrate` live check was not run; it calls the same `live.run` as `kk status --live`.
- No upgrade was run from a `v0.26.1` profile that Codex had written to; the drifted case is covered by `test_apply_removes_the_profile_an_earlier_release_owned` and the Task 4 one-off run.
- Rollback to `v0.26.1` was not exercised here.
- The untrusted-handler case of assumption 1 was not run against the real Codex, only the disabled one.
- Python 3.8 was not run locally.
