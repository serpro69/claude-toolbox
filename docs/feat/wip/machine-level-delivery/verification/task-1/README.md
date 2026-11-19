# Task 1: Codex vendor probes — results

> Task: [tasks.md, Task 1](../../tasks.md#task-1-codex-vendor-probes) · Design: [Assumptions](../../design.md#assumptions)

Recorded 2026-11-19 on Linux (Pop!_OS 22.04, kernel 7.1.1, x86_64).

| Tool | Version |
|---|---|
| Codex CLI | 0.170.0 (`codex --version`). The design's earlier evidence was taken on 0.169.0 |
| Claude Code | 2.1.296 (not exercised here) |
| tmux | 3.2a |
| Python | 3.10 (`python3 -I` for the harness) |

These results are evidence about Codex 0.170.0. A later Codex release can change any of them.

## Method

- Every probe ran against a scratch `CODEX_HOME` under `~/kkprobe-task1/` (outside `/tmp`, where Codex refuses to create its PATH helpers). The real `~/.codex` was not touched. The maintainer copied credentials into the one scratch home that needed model calls (`r1`).
- A scratch local marketplace `kkprobe` holds `kkprobe-skills` (skills only) and `kkprobe-guard` (a `PreToolUse` hook on `Bash` that logs every call and denies any command containing `KKPROBE_MARKER` with exit 2). Each build carries a *variant* letter in the guard script, so the log and the denial text show which copy ran ([`harness/build-marketplace.sh`](harness/build-marketplace.sh)). [`harness/setup-extra-fixtures.sh`](harness/setup-extra-fixtures.sh) adds the MCP-matcher plugin and MCP server, a user-level sub-agent and the legacy-style project hook; it transcribes steps that were run by hand in the session and has not been re-executed as a whole.
- An *open session* is one long-lived interactive TUI process in a tmux pane. The installation was changed from another shell between two prompts. Each prompt asked the model to run `echo KKPROBE_MARKER <tag>` once ([`harness/tui-send.sh`](harness/tui-send.sh)). Sessions ran with `approval_policy = "never"` and `sandbox_mode = "workspace-write"`, which permit the echo, so a denial can only come from a hook.
- The probe hooks append to `$KKPROBE_ROOT/hook.log`; it is committed as [`raw/hook.jsonl`](raw/hook.jsonl) (cited below as `hook.jsonl:<line>`) because the repository's `.gitignore` drops `*.log*`. A line proves the hook script ran up to its logging line. A step with no line ran no hook script to that point; whether a hook was invoked and failed earlier, as in step 7, is in the pane.
- Probes that need no model are scripts whose full output is in `raw/`: install mechanics ([`probe-cache.sh`](harness/probe-cache.sh)), bundle hash ([`probe-bundle-hash.sh`](harness/probe-bundle-hash.sh)), hook trust reads ([`probe-trust-reader.sh`](harness/probe-trust-reader.sh), using [`app-server-rpc.py`](harness/app-server-rpc.py) and [`hooks-list.py`](harness/hooks-list.py)), Git source ([`probe-git-source.sh`](harness/probe-git-source.sh)), profile precedence ([`probe-profile.sh`](harness/probe-profile.sh)) and developer instructions ([`probe-devinstr.sh`](harness/probe-devinstr.sh)).
- Provenance markers: **[raw]** means a file under `raw/` shows it; **[session]** means it was observed in this session's terminal output and no artifact was kept.

### Live-session steps

All in scratch home `r1`. "Pane" files are tmux captures; the first line of `session-step1.out` is an error from an earlier revision of `tui-send.sh` that read the log before it existed (fixed since).

| Step | Session started in | Action before the prompt | Outcome | Artifact |
|---|---|---|---|---|
| 1 | repo-a | install both plugins, review the hook in the TUI | denied, variant a | `session-step1.out`, `hook.jsonl:1` |
| 2 | same session | re-add `kkprobe-skills` at 1.0.1 | denied, variant a | `session-step2.out`, `hook.jsonl:2` |
| 3a | same session | re-add the unchanged guard 1.0.0 | denied, variant a | `session-step3a.out`, `hook.jsonl:3` |
| 3b | same session | re-add the guard at 1.0.1 with changed bytes (variant b) | "Hook failed — plugin contents changed; hook approval required", command ran | `session-step3b.out` |
| 3c | same session | install the guard as `1.0.1+kk.4a3fddb7eb51` (variant b) | same as 3b | `session-step3c.out` |
| 8i | same session | re-add the guard at 1.0.0 with variant a bytes (newer guard never reviewed) | denied, variant a | `session-step8i.out`, `hook.jsonl:4` |
| 8ii-a | new session, repo-a | install the stamped variant b, choose *Trust all* at startup | denied, variant b | `hook.jsonl:5` |
| 8ii-b | same session | re-add the guard at 1.0.0 with variant a bytes | "Hook failed — plugin contents changed", command ran | `session-step8ii.out` |
| 4 | new session, repo-b/sub1 | *Trust all* at startup; ask for workdir repo-b/sub2 | denied; hook `$PWD` repo-b/sub1, payload `cwd` repo-b/sub2 | `hook.jsonl:6` |
| 4-repo-a | new session, repo-a | none (trust given in repo-b) | no review prompt [session]; denied | `hook.jsonl:7` |
| 5-B | new session, repo-b | repo-b sets `hooks.state.<key>.enabled = false` | denied | `hook.jsonl:8` |
| 5-A | new session, repo-b | repo-b switches both probe guard plugins off ([`raw/repo-b-config-step5-A.toml`](raw/repo-b-config-step5-A.toml)) | command ran, no hook call | `session-step5-project-disables-guard.out` (re-run) |
| 5-disabled | new session, repo-a | switch the hook off in `/hooks` | command ran, no hook call [session] | — |
| 4-git | new session, repo-a | add the `kkprobegit` marketplace over HTTP, install, *Trust all* | denied by both guards (variants a and g) | `hook.jsonl:9-10` |
| mcp1 | new session, repo-a | fixtures as in `setup-extra-fixtures.sh`, *Trust all*, call the MCP tool | matcher fired (`hook.jsonl:11`); "Blocked by hook — kkprobe-mcpguard: denied MCP marker call" in the pane [session] | `hook.jsonl:11` |
| 7 | new session, repo-legacy | *Trust all*; control prompt; move the script out of the repository; prompt again | control denied; then "hook exited with code 127", command ran | `session-step7-legacy-deleted-script.out` (re-run), `hook.jsonl:12-13` |

The panes for steps 2 and 3a were taken by an earlier `tui-send.sh` before Codex printed the turn's closing line (the model's summary is cut off); the denial and its `hook.jsonl` line are in them, and the current script waits for the closing line and a tool outcome. The panes for 5-A and 7 come from re-runs at the end of the task with the same fixtures; the original runs showed the same outcome [session]. "Read-only file system (os error 30)" in some panes is a logging failure inside the sandbox; the model's own summary in the step 5-A pane says so, and the marker's output is printed below it, so the command itself ran [session].

## Results by assumption

| # | Assumption | Result on 0.170.0 |
|---|---|---|
| 1 | Guard keeps trust and stays loaded when only the skills plugin is re-added | **Holds.** The guard plugin was not re-added, and the open session kept denying (step 2) [raw] |
| 2 | An open session loses the guard after a guard-plugin upgrade | **Holds, unguarded outcome.** Steps 3b and 3c [raw] |
| 3 | One hook review covers every repository | **Holds.** Trust is keyed by plugin ID and handler, with no repository path (`hooks-list-*.json`, `config-after-probes.toml`) [raw]. Reviewed in repo-b, the hook ran in repo-a (`hook.jsonl:7`) [raw] without a review prompt [session]. `hooks/list` reports *trusted* in an untrusted-project directory too [session] |
| 4 | Hook process starts in the session's directory; the payload carries the tool's directory | **Holds.** `hook.jsonl:6`: hook `$PWD` repo-b/sub1 (a subdirectory, not the git top level), `payload.cwd` repo-b/sub2 [raw]. The payload has no workspace-root field (its keys are in the same line) |
| 5 | `--profile` ranks below trusted project config; the profile accepts every baseline key | **Precedence holds; acceptance is partly unverifiable.** See [profile precedence](#profile-precedence-assumption-5) |
| 6 | Sub-agents load from `$CODEX_HOME/agents/`; an MCP-tool matcher fires from a plugin hook | **Holds.** The agent is listed among the spawn tool's roles ([`raw/prompt-input-agent-roles.out`](raw/prompt-input-agent-roles.out)); a plugin hook matching `^mcp__[^[:space:]]+__kkprobe_echo$` fired for `mcp__kkprobe__kkprobe_echo` (`hook.jsonl:11`) [raw] and the call was blocked [session]. A sub-agent was not spawned live |
| 7 | Hook trust and enablement can be read from outside a session, fast, and reflect a later disable | **Holds, with two gaps.** See [reading hook trust](#reading-hook-trust-assumption-7) |
| 10 | A Git-marketplace source behaves like the local one for hook trust | **Holds.** Same key format and the same bundle hash as the same tree from a local path ([`raw/probe-git-source.out`](raw/probe-git-source.out)); the hook runs after one review (`hook.jsonl:10`) [raw]; kept after a no-op `marketplace upgrade` [session] |
| 12 | When a project hook's script disappears under an open session, the call proceeds unguarded | **Holds.** Step 7 [raw] |
| 13 | Codex accepts a digest-stamped version string as version and cache directory name | **Holds for every form tried.** See [install mechanics](#install-mechanics-assumptions-13-and-14) |
| 14 | Codex re-adds an earlier version over a later one; trust in earlier bytes survives another bundle in between | **First part holds. Second part fails once the adopter has reviewed the newer guard.** See [rollback](#rollback-across-a-guard-change-assumption-14) |
| 15 | `-c developer_instructions=…` accepts ≥ 64 KiB multi-line and replaces a trusted project's value | **Holds on Linux.** macOS deferred to Task 17 by the maintainer. See [developer instructions](#developer-instructions-assumption-15) |

### Reading hook trust (assumption 7)

The mechanism is the app-server's `hooks/list` method, over stdio JSON-RPC:

```
codex app-server
→ {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"kkprobe","version":"0.0.0"}}}
→ {"jsonrpc":"2.0","method":"initialized"}
→ {"jsonrpc":"2.0","id":2,"method":"hooks/list","params":{"cwds":["/path/to/workspace"]}}
```

Response, one entry per requested `cwd` (abridged from [`raw/hooks-list-untrusted.json`](raw/hooks-list-untrusted.json)):

```json
{"cwd": "/…/repo-a", "warnings": [], "errors": [], "hooks": [{
  "key": "kkprobe-guard@kkprobe:hooks/hooks.json:pre_tool_use:0:0",
  "eventName": "preToolUse", "matcher": "Bash", "source": "plugin",
  "pluginId": "kkprobe-guard@kkprobe",
  "sourcePath": "<CODEX_HOME>/plugins/cache/kkprobe/kkprobe-guard/1.0.0/hooks/hooks.json",
  "enabled": true, "trustStatus": "untrusted",
  "currentHash": "sha256:<declaration>/sha256:<bundle>"}]}
```

What the guard handler reads as, from [`raw/probe-trust-reader.out`](raw/probe-trust-reader.out) unless marked. The full request and response of every case is in [`raw/trust-reader/`](raw/trust-reader/) (for example `02-user-switched-the-hook-off-…json` for the disabled hook):

| State | `hooks/list` for the workspace |
|---|---|
| Never reviewed | `trustStatus: untrusted` ([`raw/hooks-list-untrusted.json`](raw/hooks-list-untrusted.json)) |
| Reviewed | `trustStatus: trusted`, in every requested workspace |
| Switched off by the user (`hooks.state."<key>".enabled = false` in the user config, the line `/hooks` writes) | `enabled: false, trustStatus: trusted` |
| Bytes changed since review | `trustStatus: modified` |
| A trusted project sets `plugins."<guard>".enabled = false`, `features.hooks = false` or `features.plugins = false` | handler **absent** for that workspace only; other workspaces unaffected |
| A trusted project sets `hooks.state."<key>".enabled = false` | ignored: `enabled: true, trusted`; a live session denied (`hook.jsonl:8`) |
| `codex app-server -c features.hooks=false` | handler absent everywhere |
| `codex app-server -c 'plugins."<guard>".enabled=false'` (key quoted) | no effect: still `enabled: true, trusted`. Codex splits a `-c` key on dots and does not treat the quotes as quoting, so this names another key |
| `codex app-server -c plugins.<guard>.enabled=false` (unquoted) | handler absent everywhere |

- Possible `trustStatus` values per the protocol schema (`codex app-server generate-json-schema`, not kept) [session]: `managed`, `untrusted`, `trusted`, `modified`. `managed` was not produced in these probes.
- A session honours the same `-c` spellings the same way: `-c plugins.kkprobe-skills@kkprobe.enabled=false` removes the probe skill from `codex debug prompt-input`, the quoted spelling does not (end of `probe-trust-reader.out`).
- One read, starting the app-server process included, took 0.165–0.191 s in the captured run; the first, cold reads took up to 0.44 s [session].
- Trust lives in the user config as `[hooks.state."<key>"]` with `trusted_hash` (declaration) and `trusted_content_hash` (bundle), plus `enabled` once the hook has been toggled in `/hooks` ([`raw/config-after-probes.toml`](raw/config-after-probes.toml), the complete scratch config after the probes; it holds no credentials). There is no app-server method that writes trust; it is granted in the TUI's `/hooks` view or its startup "Hooks need review" prompt [session].
- **Gap 1: the profile layer.** The app-server rejects `--profile`, so `hooks/list` cannot see a hook, plugin or feature key that the `kk` profile sets. It does honour `-c` for `features.hooks` and, in the unquoted spelling, `plugins.<id>.enabled`, so a reader can mirror such profile keys, and the adopter's own `-c` arguments, by passing them as `-c`. Other keys that could affect hooks were not tried.
- **Gap 2: which workspace.** The answer is per workspace, and a trusted project can remove the guard for itself. A reader must ask for the workspace the session will actually use.

### What the bundle hash covers

From [`raw/probe-bundle-hash.out`](raw/probe-bundle-hash.out). The declaration half of `currentHash` stayed the same throughout. The bundle half:

| Change to the plugin source, then re-add | Bundle hash |
|---|---|
| identical rebuild | unchanged |
| manifest `version` only (directory becomes `9.9.9`) | changed |
| manifest `description` only | changed |
| an extra file | changed |
| guard script content | changed |
| guard script executable bit removed | unchanged (and the cached copy is not executable either) |

Identical bytes produced the identical hash in another `CODEX_HOME` and from a Git source ([`raw/probe-git-source.out`](raw/probe-git-source.out)).

Consequence: the same guard code republished under a new version string needs a new review. `kk` keeps the guard's version unchanged while its content identity is unchanged, which is what keeps trust across releases; that rule is load-bearing.

### Install mechanics (assumptions 13 and 14)

From [`raw/probe-cache.out`](raw/probe-cache.out) (no session):

- A same-version re-add **replaces the cache directory**, even with identical bytes: a new directory inode each time (inode numbers get reused, so an unchanged number alone would not prove the directory was kept). With identical bytes the path and hash do not change, so trust holds and an open session kept enforcing (step 3a).
- An upgrade leaves only the new version's directory; the old one is deleted.
- Every stamped string tried was accepted as version and directory name: `1.0.1+kk.<12 hex>`, `1.0.1-kk.<12 hex>`, `0.0.0-dev.<12 hex>`, a bare 64-hex digest, `sha256-<12 hex>`, `local-<12 hex>`. Codex does not compare versions. The `+kk.` form also ran live (`hook.jsonl:5`).
- A downgrade (`1.0.0` over a later version) installs.
- `codex plugin marketplace add` rejects a `file://` URL; a plain `http://` Git URL works ([`raw/probe-git-source.out`](raw/probe-git-source.out)).

### Rollback across a guard change (assumption 14)

Trust is a single slot per handler key, holding one hash; a restored guard is trusted only if its hash is the one in that slot.

- **Restored guard was the last one reviewed** (the newer guard was never reviewed). Re-adding the earlier version with the earlier bytes left the stored hash matching: the session that had been open since before the upgrade, and had loaded those bytes when they were trusted, enforced again (step 8i). The handler was enabled; a handler the adopter switched off stays off whatever its trust.
- **The newer guard was reviewed after it.** That review overwrote `trusted_content_hash`. Re-adding the earlier bytes then read `modified` (the mechanism is in `probe-trust-reader.out`), and the open session's hook failed while the marker ran (step 8ii-b).
- **The restored guard was never reviewed** (neither guard was): nothing becomes trusted by restoring it. Not probed separately; it follows from the first row of the trust table.

So a rollback restores enforcement only when the restored guard's bytes are the last ones the adopter reviewed and its handlers are enabled. When the bytes do not match, the rollback is itself a guard change: open sessions run unguarded (step 8ii-b), new sessions show "Hooks need review", and the rolled-back guard needs review before it counts as recovery. Whether an open session enforces again after that review without a restart was not probed. A handler the adopter switched off needs switching back on, not review.

### Profile precedence (assumption 5)

From [`raw/probe-profile.out`](raw/probe-profile.out). The app-server rejects `--profile` (`--profile only applies to runtime commands…`) and a legacy `profile = "…"` key is now an error, so values were read from the header `codex exec` prints before its model call, and from `codex debug prompt-input`.

| Workspace | model / effort / sandbox / developer_instructions come from |
|---|---|
| plain directory, no profile | user config |
| plain directory, `--profile kkp` | profile |
| untrusted project with its own `.codex/config.toml`, `--profile kkp` | profile (project config not loaded) |
| trusted project with its own `.codex/config.toml`, `--profile kkp` | project for every key it sets |

Approval policy: `codex exec` reports `approval: never` in every case. In the interactive prompt, the user config's `never` produces "Approval policy is currently never"; with the profile's `on-request` that sentence is gone and the prompt instead explains how to request approval for commands that need escalated privileges. That is the prompt Codex builds for `on-request`, observed in the prompt, not in an approval dialog.

Acceptance: the profile carrying every baseline key and the three opt-in keys loads without error. That is weak evidence on its own. A type error is rejected (`[agents] max_threads = "six"` → exit 1), but an unknown key (appended to the file, so inside its `[tui]` table) loaded silently and an invalid `model_reasoning_effort = "bogus"` was passed through (`reasoning effort: bogus`). These are one case each, not a survey. Effects were observed for `model`, `model_reasoning_effort`, `sandbox_mode`, the approval policy (in the prompt) and `developer_instructions`; the `agents`, `tui`, `features.hooks`, context-limit and `project_doc_max_bytes` keys are type-checked but their effect was not observed. How `kk` should handle this is [open question 4](../../design.md#open-questions).

**Contradiction.** A trusted project that sets its own `developer_instructions` replaces the profile's, so in that repository a wrapped session receives none of the toolbox's Codex instructions unless the launcher passes `-c developer_instructions=…` ([open question 2](../../design.md#open-questions)).

### Developer instructions (assumption 15)

From [`raw/probe-devinstr.out`](raw/probe-devinstr.out), with `--profile kkp` in a trusted project that sets its own `developer_instructions`:

- A 130,682-byte `developer_instructions=<serialised TOML string>` argument (126 KiB of text) was accepted and shown in full; a 131,719-byte one failed in `execve` with "Argument list too long". Codex added no limit of its own below that. The boundary lies between those two sizes, which is consistent with Linux's fixed per-argument cap (`MAX_ARG_STRLEN`, 32 pages = 131,072 bytes on 4 KiB pages); the exact byte was not bisected. The limit applies to the serialised value, so escaping counts.
- `-c developer_instructions=…` replaced both the profile's and the trusted project's value.
- macOS not probed; deferred to Task 17 (17.1a) by the maintainer. There the limit is the total `ARG_MAX` for arguments and environment rather than a per-argument cap.

### Other observations

- On first start with an unreviewed hook, the TUI shows "Hooks need review" with *Review hooks*, *Trust all and continue* and *Continue without trusting (hooks won't run)* [session]. A restarted session after a guard change therefore stays unguarded if the adopter continues without trusting.
- Two copies of the same plugin name from two marketplaces (`kkprobe-guard@kkprobe`, `kkprobe-guard@kkprobegit`) both load and both fire (`hook.jsonl:9-10`).
- The trust key embeds the marketplace name. Renaming the local marketplace after release changes the plugin ID and therefore requires every adopter to review the guard again (bears on [open question 1](../../design.md#open-questions)).

## Not covered

- macOS for probe 1.9 (deferred, Task 17.1a).
- Git marketplace over HTTPS or SSH from a real host; the probe used plain HTTP on 127.0.0.1, which exercises the same Git-source path but not authentication.
- Effects of the `agents`, `tui`, `features.hooks`, context-limit and `project_doc_max_bytes` profile keys (type-checked only).
- The `managed` trust status.
- A live sub-agent spawn; the agent's presence in the spawn tool's role list was observed.
- A rules-file parse failure on the app-server path (still read from source).
