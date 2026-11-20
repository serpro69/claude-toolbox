# Tasks: Machine-level delivery

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Status: pending — revised after the [design review](./review-design.md); see the [resolution](./review-resolution.md)
> Created: 2026-11-18
> Not Doing: orchestrator features, Go binary or package-manager distribution, built-in unattended upgrades, full parity for IDE/desktop/cloud/CI sessions, merging into user-owned config (migration excepted), general shell-read grants, detection of open Codex sessions, `kk uninstall`, native Windows, per-repository teammate stub, changes to capy's setup, system-level deny fragment (future)

## Task 1: Codex vendor probes
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Slicing:** Risk-First — the central promise and four source-read claims are unprobed
- **Can run in parallel with:** Task 2, Task 5, Task 8
- **Docs:** [implementation.md#codex-vendor-probes](./implementation.md#codex-vendor-probes), [design.md#assumptions](./design.md#assumptions)

### Subtasks
- [x] 1.1 Build a scratch local marketplace with a skills-only plugin and a guard-like plugin whose `PreToolUse` hook denies a marker command and logs every call; install into a scratch `CODEX_HOME` (the maintainer supplies credentials) → verify: a marker command is denied and logged
- [x] 1.2 In a tmux-driven open TUI session, re-add only the skills plugin at a new version and send a marker command → verify: the hook log shows a new denial (assumption 1)
- [x] 1.3 Re-add the unchanged guard plugin, then the guard plugin at a new version with a changed script, each with a session open; then install it once under a digest-stamped version string → verify: record whether the cache directory is replaced, which outcome the open session shows (assumption 2), and which stamped form Codex accepts as a version and cache directory name (assumption 13)
- [x] 1.4 Probe trust scope across two repositories, the hook's launch directory against the payload directory, and a Git-URL marketplace source → verify: results recorded for assumptions 3, 4 and 10
- [x] 1.5 Find how to read hook trust from outside a session (app-server `hooks/list`, then persisted hook state), then disable the trusted hook and read again → verify: the request and response are recorded, with whether a disabled hook shows as disabled, whether the answer depends on the workspace, and how long one read takes; or the absence of a usable mechanism is recorded (assumption 7)
- [x] 1.6 Probe profile precedence against user and trusted project config with every baseline key, user-level sub-agents, and an MCP-tool matcher from a plugin hook → verify: results recorded for assumptions 5 and 6
- [x] 1.7 In a scratch repository, trust a project hook that runs a script from the repository, open a session, delete the script and send a guarded command → verify: record whether the call proceeds unguarded, is blocked or errors (assumption 12)
- [x] 1.8 After the guard upgrade in 1.3, re-add the guard at its earlier version with the earlier bytes → verify: record whether Codex installs an earlier version over a later one and whether the earlier bytes are still trusted or need review again (assumption 14)
- [x] 1.9 (Linux; macOS deferred to 17.1a) Pass `-c developer_instructions=…` with a 64 KiB multi-line value alongside a profile, and in a trusted project that sets its own `developer_instructions` → verify: record the largest value accepted on Linux and macOS and which value the session shows (assumption 15)
- [x] 1.10 Write the results to `verification/task-1/` with tool versions, and update `design.md` Assumptions and any section a result contradicts

### Execution context
- 2026-11-19, observed: local Codex CLI is 0.170.0 (`codex --version`), not the 0.169.0 the design's evidence was taken on; Claude Code 2.1.296. Probe results are labelled with 0.170.0. Source-read claims from `rust-v0.169.0` are re-checked by observation here, not by re-reading source.
- 2026-11-19, observed: `codex` warns and refuses to create its PATH helper binaries when `CODEX_HOME` sits under `/tmp`, so scratch homes for the probes live outside `/tmp` to keep the setup close to a real install.
- 2026-11-19, accepted (maintainer): the maintainer copies Codex credentials into the scratch homes; the implementer does not.
- 2026-11-19, accepted (maintainer): probe 1.9 runs on Linux only in this task; the macOS half is deferred to Task 17 (owner: maintainer, who has the Mac). Next action: run `verification/task-1/harness/probe-devinstr.sh` on macOS and add the result to `verification/task-1/`. Verification condition: the macOS limit is recorded next to the Linux one, and the import size limit in `design.md` is the lower of the two.
- 2026-11-19, observed (supersedes the verification condition of the entry above; the deferral itself is unchanged): once the design fixed an 8 KiB margin, "the lower of the two" no longer gives the cap. The cap rule is in `design.md` §Repository instructions for Codex (122,880 bytes, or the lower measured limit less 8 KiB if that is smaller), and Task 17.1a records the macOS environment size with the limit, because on macOS the limit covers arguments and environment together.
- 2026-11-19, observed: all probes ran; results in [verification/task-1/](./verification/task-1/README.md), raw outputs in `verification/task-1/raw/`. Every Codex assumption held except 14, whose second part fails once the adopter has reviewed the newer guard (Codex keeps one trusted hash per handler). Further findings: a trusted project can switch the guard off for itself and `hooks/list` then omits the handler; a trusted project's `developer_instructions` replaces the profile's; Codex passes unknown keys and invalid enum strings in a profile without error; the trust key embeds the marketplace name.
- 2026-11-19, done: `design.md` updated (evidence, activation state and trust reader, launching Codex, repository-instruction size cap of 122,880 bytes, rollback, guard identity and digest-stamp form `<version>+kk.<12 hex>`, protection guarantee, Assumptions); `implementation.md` §Codex activation and trust step 5 and Task 10.4 now define an absent or `modified` handler as not effective.
- 2026-11-19, proposed (open, owner: maintainer): `design.md` open questions 2 (toolbox instructions in repositories with their own Codex `developer_instructions`; settle before Task 9), 3 (warning or confirmation for open sessions on a rollback across a reviewed guard change; settle before Task 10) and 4 (how `kk` checks Codex overrides; settle before Task 9). Verification condition: each is answered in `design.md` and moved under accepted decisions before the dependent task starts.
- 2026-11-19, verification: Python harness parses under 3.8 grammar; `bash -n` and `shellcheck -S warning` clean after guarding two `cd` calls in `probe-devinstr.sh`; edited `hooks-list.py` re-run against the scratch home (0.16 s, three handlers); 123 relative links and anchors in the four feature docs resolve. No repository suite covers `docs/feat/` (excluded from the docs build), so none was run. Process note: the Python harness was written before the python profile's `implement/` guidance was loaded; it was loaded and applied at verification (stderr pipe in `hooks-list.py` changed to `DEVNULL`).
- 2026-11-19, review round 1 (`/kk:review-code` isolated): code-reviewer sub-agent COMMENT (no P0/P1; 2×P2, 5×P3); Codex via clink (OpenAI, provider assumed from PAL's shipped manifest; receipt unverified because PAL stripped read events) REQUEST_CHANGES (1×P1, 7×P2, 1×P3). Fixed: `raw/hook.log` was gitignored by `*.log*` → renamed `raw/hook.jsonl`; the trust-reader cases subtask 1.5 asks for (disabled, `modified`, absent per workspace, ignored project `hooks.state`, `-c` overrides, timing) captured by `harness/probe-trust-reader.sh`; bundle-hash and Git-source equivalence captured by `probe-bundle-hash.sh` and `probe-git-source.sh`; approval-policy evidence captured in `probe-profile.out`; panes for steps 5-A and 7 re-run and captured; manual fixtures scripted in `setup-extra-fixtures.sh`; README gained a step table and [raw]/[session] provenance markers; `tui-send.sh` reports a timeout as inconclusive; RPC helpers have a 60 s deadline; design wording corrected (rollback precondition, "restarted and reviewed", import cap as measurement vs choice, "All held except the last, which was not probed", A1 evidence, moved paragraphs, "intended trade-off"); implementation.md import report points at the design cap. New finding from the re-capture: the app-server honours `-c features.hooks=false` but ignores `-c plugins."<id>".enabled=false`.
- 2026-11-19, proposed (open, owner: maintainer): `design.md` open question 5 (inputs to the Codex trust reader: workspace for upgrade verification, `-C`, the profile layer the app-server cannot load, `managed`), raised by the review; settle the profile and `-C` parts before Task 9 and the rest before Task 10. Implementation step 5 and Task 10.4 now point at it. Verification condition: answered in `design.md` before the dependent task starts.
- 2026-11-19, review round 2 (same reviewers, continued): code-reviewer APPROVE (4×P3); Codex REQUEST_CHANGES (P2s: exact post-disable RPC exchange, caller-supplied `-c` missing from open question 5, rollback claim ignoring `enabled=false`, cap formula mismatch with 17.1a, no-log-line rule contradicted by step 7, trust-reader script not interruption-safe; P3s: Git probe and fixture script replay hazards). Fixed: `probe-trust-reader.sh` now restores on exit, inserts a missing `enabled` line, fails a case without answers and writes every exchange to `raw/trust-reader/`; `probe-git-source.sh` serves only the bare repository and checks the server and install; `setup-extra-fixtures.sh` refuses a re-run and is labelled a transcription; `tui-send.sh` waits for the tagged turn's outcome; README provenance corrected; design rollback and open questions 3 and 5 reworded; validation statements scoped to the single cases tried; Task 17.1a uses the design's cap rule and records the macOS environment size. Correction of round 1: the code-reviewer's control showed the earlier "app-server ignores `-c plugins.<id>.enabled`" was a quoting artifact; unquoted, `-c plugins.<id>.enabled=false` removes the handler from `hooks/list` and the plugin from a session (`raw/probe-trust-reader.out`).
- 2026-11-19, review round 3 (targeted): code-reviewer APPROVE (N1–N4 resolved; new P3 N5: Task 9 lacked the open-question gates → fixed with a **Blocked until** field on Task 9 and a sentence in implementation.md §Codex baseline and launch). Codex: post-disable exchange, cap rule, fixtures, Git probe, RPC deadlines and the step 5-A request resolved; remaining points fixed by the author and **not independently re-reviewed**: open question 5 notes that replaying a profile key as `-c` inverts its precedence over trusted project config; the Verify step tells the adopter how to handle untrusted/changed, disabled and absent handlers separately; "until restarted" wording replaced by "at least until reviewed" because step 8i suggests open sessions re-check trust (restart necessity not probed); open question 4 scoped to the single cases tried; README A6 denial marked [session], rollback text distinguishes disabled handlers, timing range updated; `probe-trust-reader.sh` tracks an installed guard mutation until reinstall, rejects answers with workspace errors and fails a session control that renders no prompt (re-run, exit 0); `tui-send.sh` requires the tagged turn's closing line and a tool outcome (checked against the saved panes: steps 2 and 3a were captured mid-turn by the old loop, noted in the README). A round-2 change to the accepted macOS-deferral entry's verification condition was reverted to its original wording and superseded by a dated follow-up entry.
- 2026-11-19, done: Task 1's evidence and design updates are complete for Linux on Codex 0.170.0. Open items carried forward with owners: `design.md` open questions 1–5 (maintainer; before Tasks 3.8, 9 and 10), macOS probe 17.1a (maintainer) and its proposed reordering, deletion of `~/kkprobe-task1/` (maintainer; done, see below). Indexed: `kk:test-patterns` (Codex probing technique), `kk:review-findings` (pre-flight readers must match the launched process's configuration), `kk:debug-context` (`-c` key quoting).
- 2026-11-19, proposed (owner: maintainer, unresolved): the code-reviewer noted that Task 17.1a (macOS size limit) runs after the Task 18 pilot, so a lower macOS limit would change the import cap after the retirement release. Next action: decide whether to run 17.1a before Task 18 (for example as part of Task 9). Verification condition: the macOS limit is recorded before the pilot, or the order is confirmed.
- 2026-11-19, observed: scratch state lives in `~/kkprobe-task1/` (scratch `CODEX_HOME`s, one holding a copy of the maintainer's Codex credentials in `r1/home/auth.json`). Owner: maintainer. Next action: delete `~/kkprobe-task1/` when the evidence is accepted (the agent's guard blocks `rm`). Verification condition: the directory no longer exists.
- 2026-11-19, done (maintainer): `~/kkprobe-task1/` deleted, including the copied credentials, after the agent stopped the Codex app-server daemon the probe sessions had started from that home; the review's temporary files under `/tmp` deleted too. Closes the entry above.

## Task 2: Claude vendor probes
- **Status:** done
- **Depends on:** —
- **Size:** S
- **Slicing:** Risk-First — activation depends on in-place loading from a local marketplace
- **Can run in parallel with:** Task 1, Task 5, Task 8
- **Docs:** [implementation.md#claude-vendor-probes](./implementation.md#claude-vendor-probes)

### Subtasks
- [x] 2.1 With the maintainer's agreement, add a uniquely named local-path marketplace whose plugin entry points at a versioned subdirectory; install at user scope → verify: a plugin hook reports its script path and plugin root inside that subdirectory (assumption 8)
- [x] 2.2 Re-point the marketplace entry at a second subdirectory with a session open → verify: the open session keeps the first, a new session uses the second
- [x] 2.3 Probe the flag-layer read deny with hooks disabled in a folder without recorded trust, compare the statusline before and after workspace trust, and set a project-enabled plugin ID to `false` in the layer. The deny and plugin override held. The statusline rendered only in the trusted, hooks-enabled control (assumption 9).
- [ ] 2.4 Optional: route the VS Code extension through a wrapper that adds a settings layer → verify: record whether the layer applies **Skipped** because the VS Code CLI was unavailable.
- [x] 2.5 Remove the scratch marketplace and plugin; write results to `verification/task-2/` and update `design.md`

### Execution context

- 2026-11-20, accepted by the maintainer in this session: install a uniquely named probe in the logged-in Claude user configuration, run the probes in scratch directories and uninstall it afterwards. Baseline: `bd385a6`, Claude Code 2.1.296 on Linux.
- 2026-11-20, observed: assumption 8 held across two overlapping sessions. Use `readFromFolder` to verify the Claude release at first install and after a catalog switch (Tasks 3 and 4). Assumption 9 held for native read denial and the flag-layer plugin override. The statusline was absent at the untrusted prompt and in the trusted control with hooks disabled. [Probe results and reproduction](verification/task-2/README.md)
- 2026-11-20, verified: Claude removed the user plugin and marketplace registrations. The maintainer removed both scratch directories and the vendor-marked orphan cache. All three paths were checked absent.
- 2026-11-20, verified and reviewed: Bash syntax, ShellCheck, the recorded session comparisons and a symlinked fixture directory passed (captures `3578d1a2-84d4-44d7-80b2-dffdfb34b443` and `c4737db2-4505-4313-939c-f0381615c657`). The isolated code reviewer approved the revised task. The external Claude Opus 5.5 reviewer closed its five findings on provenance, activation verification, hook registration coverage, reload behavior and reproducibility. Both reviewed the saved evidence.
- 2026-11-20, review housekeeping: automatic approval rejected recursive deletion of `/tmp/kk-task2-review-9rDg8SDN` and `/tmp/kk-review-instructions-8bbx6buc`. These hold review inputs and a synthetic fixture. The maintainer can remove both directories and confirm the paths are absent.

## Task 3: First install for Claude
- **Status:** done
- **Depends on:** Task 2
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7, Task 8
- **Docs:** [implementation.md#kk-foundation](./implementation.md#kk-foundation), [design.md#upgrade-flow](./design.md#upgrade-flow)

- **Parts:** 3a — 3.2 to 3.4, stage and validate a release as far as *staged*; 3b — 3.1 and 3.5 to 3.8, first install. The tests in 3.7 grow with each part.
### Subtasks
- [x] 3.1 Create `kk/bin/kk` (entry point: resolve the toolbox home, read the active release, the rollback target and the candidate's phase with `jq`; for `rollback` run the CLI of the release being restored, which is the active release when a candidate is pending in *activating* and the rollback target otherwise; for everything else run the active release's; all under isolated Python) and `kk/payload.json` (layout version and required directories)
- [x] 3.2 Create the state module in `kk/lib/`: a format version, one active release, per-tool state, rollback target with its fallback to the previously active release, candidate phase, the time each release stopped being active, the installed-paths record (a path is recorded before it is written), atomic read-modify-write that keeps unknown fields, and the exclusive writer lock on `$KK_HOME/lock` → verify: a failed rename leaves the previous state file intact; a second writer exits at once and changes nothing; an unknown field survives a rewrite; a higher format version is refused and the file left untouched
- [x] 3.3 Create the payload module: fetch from a tag archive or a local checkout, extract only payload directories, reject absolute paths, parent traversal and escaping symlinks → verify: crafted archives are rejected; the plugin's relative symlinks survive
- [x] 3.4 Create `kk/selftest/guard-cases.json` and the validation module: payload completeness, guard self-test against the candidate engine, one event through the Claude guard handler as the staged `hooks/hooks.json` registers it, `claude plugin validate` → verify: a candidate with a broken engine fails and the state file is unchanged; so does one whose hook registration names a script missing from the payload
- [x] 3.5 Create Claude activation: write the local marketplace manifest, add the marketplace, install the plugin at user scope, verify that `readFromFolder` on the matching user-scope `claude plugin list --json` entry resolves to the candidate plugin directory; stop without replacing anything when `~/.local/bin/kk` exists and is not in the installed-paths record; keep the local marketplace's name in one constant (working value `toolbox`)
- [x] 3.6 Add `kk upgrade` for the first-install path, `kk status`, and `install.sh` at the repository root; running the installer again after an interrupted first install resumes from the journaled phase or starts over; the installer warns in one line when `kk` on `PATH` resolves to something other than its own symlink
- [x] 3.7 Add `test/kk/` and `test/test-kk.sh` with stub vendor CLIs covering first install, an interrupted first install completed by a second installer run, failed validation, a colliding symlink and two overlapping writers → verify: the suite passes under isolated Python 3.8 syntax checks
- [ ] 3.8 Do not tag a release that ships `kk` until the maintainer has settled the local marketplace's name ([design.md#open-questions](./design.md#open-questions)); change the constant then **Open pre-tag decision.**

### Execution context

- 2026-11-20, accepted by the maintainer: Task 3 requires `kk/`, `klaude-plugin/` and `kodex-plugin/`. Task 7 adds `kodex-guard/` to the required payload when it introduces the plugin. This makes first install testable from the current checkout. The final release requires all four directories.
- 2026-11-20, implemented on base `60661249`: a standalone installer and checkout entry point, private staging, guard and dispatcher preflight, an atomic journal with a nonblocking writer lock, user-scope Claude activation, path ownership checks and recovery after interruption. A different explicit source can replace a pending candidate. A retained tag directory belonging to another source is a collision.
- 2026-11-20, verified on Linux: all 18 first-install tests passed on CPython 3.10.12 and 3.8.20. Claude Code 2.1.296 installed from this checkout in a disposable configuration, then recovered the same release after a deliberately interrupted vendor operation. [Verification record](verification/task-3/README.md)
- 2026-11-20, reviewed: the isolated code reviewer approved the recovery changes. External review closed its recovery and housekeeping findings on the corrected worktree. The final review diff includes the same-tag collision guard. The marketplace name remains open for the first tag that ships `kk`.
- Review scratch remains at `/tmp/kk-review-first-install-iEg4yT1x`, containing review diffs and the baseline checkout. The temporary mount does not support Trash and automatic approval rejected permanent deletion. The maintainer can remove this directory and verify its absence.
- 2026-11-20, baseline issue (unassigned): 16 of 17 repository suites passed using Python 3.11 for the TOML checks. The template-sync suite’s “Rejected base is logged” assertion also failed on unmodified `60661249` with jq 1.6. Investigate the malformed-base logging case in `test/test-template-sync.sh` separately and verify the expected diagnostic on that jq version.

## Task 4: Upgrade, rollback and recovery for Claude
- **Status:** done
- **Depends on:** Task 3
- **Size:** M
- **Can run in parallel with:** Task 5, Task 7, Task 8
- **Docs:** [implementation.md#kk-foundation](./implementation.md#kk-foundation), [design.md#rollback-and-interrupted-upgrades](./design.md#rollback-and-interrupted-upgrades)

Task 4 pruning must account for unpromoted directories retained under `releases/` after an interrupted first install was superseded. A session may have loaded that directory. Preserve the 14-day support window before removing it and check the launch symlink’s destination as well as its ownership record before replacing it.

Task 4 must distinguish interpreter-generated guard bytecode from a changed release when checking a previously placed candidate. The first-install fingerprint covers the full tree. A second interpreter writing its cache can therefore trigger a conservative rebuild on retry. Verify the policy with an open session before extending it to active-release upgrades.

### Subtasks
- [x] 4.1 Implement the hand-off: fetch, staging and validation from the active release's code; activation and verification from the candidate's; rollback from the code of the release it restores (the active release after an interrupted upgrade, the rollback target otherwise); status and resumption from the active release
- [x] 4.2 Journal the candidate's phase before each activation step and implement resumption of an interrupted upgrade
- [x] 4.3 Implement `kk rollback` to the rollback target, the recovery command `kk upgrade` prints, and pruning of releases that are not active, not the rollback target, and stopped being active more than 14 days ago
- [x] 4.4 Extend the stub-based suite: upgrade, interruption at each activation step followed by resume and by rollback, pruning with a release that was active for a month and superseded yesterday → verify: after every interruption case `kk status` reports the mixed state and both ways out work; the month-old release is kept
- [x] 4.5 Add the post-promotion case: promote a release, make its `kk/lib` unreadable, then break the stable entry point too → verify: the previous release is restored through the stable entry point in the first state and through the copy inside the rollback target in the second

### Execution context

- 2026-11-20, baseline `fecd2a3e`. Task 3 provides the three-directory Claude payload, first-install journal and dispatcher. This task adds the active-release writer paths and retains the first-install contracts. The Codex guard and the first public tag remain later work.
- 2026-11-20, implemented: the active release owns preparation and resumption. The selected candidate or rollback target owns activation. The journal names each step before its side effects, including the target of an interrupted rollback. Successfully verified releases and abandoned tagged candidates retain their source and digest. Pruning uses the time a release stopped serving new sessions.
- 2026-11-20, verified: 25 tests passed on CPython 3.8.20 and 3.10.12. In a disposable Claude Code 2.1.296 session, a second interpreter generated guard bytecode without invalidating the candidate. The same session successfully ran its read hook before resumption, after promotion and after rollback. [Verification record](verification/task-4/README.md)
- 2026-11-20, reviewed: the isolated code reviewer and external Claude reviewer closed the tagged retry and dispatcher recovery findings. Final tests cover interruptions before and after dispatcher publication, restoration through a damaged stable symlink, and validation against the journaled dispatcher digest. The template-sync assertion remains the previously recorded repository-wide failure.

## Task 5: Claude plugin instructions, statusline and plugin root
- **Status:** done
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 7, Task 8
- **Docs:** [implementation.md#claude-plugin-changes](./implementation.md#claude-plugin-changes), [design.md#plugins](./design.md#plugins)

### Subtasks
- [x] 5.1 Create `klaude-plugin/instructions/behavior.md` from `.claude/CLAUDE.extra.md`; make the latter a generated copy with a freshness check → verify: `test/test-claude-extra.sh` passes and the copy is byte-identical
- [x] 5.2 Move the plugin-root override text from `.claude/toolbox/CLAUDE.md` into a plugin instruction file used only for plugin-only installs
- [x] 5.3 Add a `SessionStart` hook script and its registration in `klaude-plugin/hooks/hooks.json` for start, resume, clear and compaction; skip behavioural instructions when the project has `.claude/CLAUDE.extra.md`; honour the override file's switch → verify: `test/test-hooks.sh` covers both the legacy-file and the clean-project fixture
- [x] 5.4 Move the statusline scripts to `klaude-plugin/statusline/`; keep the `.claude/toolbox/scripts/` copies identical until retirement
- [x] 5.5 In `klaude-plugin/scripts/set-plugin-root.sh`, use the script's parent directory when it sits under the toolbox home's `releases/` → verify: `test/test-cpr.sh` passes with a new case for that branch
- [x] 5.6 Run `make generate-kodex` and `test/test-plugin-structure.sh`

### Execution context

- Baseline `6c315da9`. Use the running hook’s physical plugin directory to identify a managed release. Preserve template imports during coexistence. The hook reads the boolean `claude.instructions` switch from the adopter’s override file. An absent switch enables plugin-supplied context.
- 2026-11-20, verified on Linux: the generator, structure, graph and focused shell checks passed. The real Claude Code 2.1.296 startup probe confirmed full instruction receipt and the exported plugin root in four cases. The repository-wide run had the same single template-sync failure documented in Task 3. [Verification record](verification/task-5/README.md)
- Review closed the custom-home, asset graph, exit-status and path portability findings. When documenting the first release in Task 15, call out that plugin-only users now receive the behavioral instructions by default and can disable the hook through `claude.instructions`.

## Task 6: Claude launch layer and overrides
- **Status:** pending
- **Depends on:** Task 3, Task 5
- **Size:** M
- **Can run in parallel with:** Task 7, Task 8, Task 9
- **Docs:** [implementation.md#claude-launch-layer](./implementation.md#claude-launch-layer), [design.md#launching-claude](./design.md#launching-claude)

### Subtasks
- [ ] 6.1 Create `kk/baseline/claude.json`: preferences from the template's adopter defaults as `.github/scripts/template-cleanup.sh` renders them with no options (no `model` key, `effortLevel: high`), environment variables from `.claude/settings.json`, statusline path, default allow entries, opt-in catalogue; do not copy this repository's pinned model or `xhigh`
- [ ] 6.2 Add `kk/baseline/claude/deny.json` as a target in `scripts/generate-guard.sh` and in every freshness list
- [ ] 6.3 Implement layer composition: yield per key and per environment variable to the user, project and local settings; always include denies, which nothing composed later can remove; add default allows; disable the Git-marketplace plugin ID only where it is enabled
- [ ] 6.4 Implement the override file: schema, named settings file, default switches, opt-in grants; overrides set or replace preference keys and add to permission lists; a malformed file stops the launch with a message
- [ ] 6.5 Implement `kk claude` with `--print-layer`; when the adopter supplies `--settings` as a path or inline JSON, compose it as the top of the layer and pass the one composed file; stop the launch when it cannot be read or parsed
- [ ] 6.6 Unit tests for yielding, list composition, each override, the adopter's `--settings` in both forms with the denies intact, an override that tries to empty the deny list, and a malformed override → verify: on a real machine a wrapped session uses the baseline effort level when none is set and the user's when one is; with hooks disabled, a wrapped session started with the adopter's own `--settings` refuses to read a decoy secret

## Task 7: Codex guard plugin with workspace anchoring
- **Status:** pending
- **Depends on:** Task 1
- **Size:** M
- **Can run in parallel with:** Task 3, Task 4, Task 5, Task 6, Task 8
- **Docs:** [implementation.md#codex-guard-plugin](./implementation.md#codex-guard-plugin), [design.md#guard-changes](./design.md#guard-changes)

### Subtasks
- [ ] 7.1 Create `kodex-guard/` with a manifest named `kk-guard`, `hooks/hooks.json` with the matchers from `.codex/hooks.json`, and the three adapters ported from `.codex/scripts/`. Add the directory to `kk/payload.json` and test that a payload missing it is rejected (Task 3 decision).
- [ ] 7.2 Anchor policy to the hook's launch directory (git top level, else the directory); use the payload directory for operands only; read the capy registration from the workspace
- [ ] 7.3 Add the engine copy `kodex-guard/scripts/guard/` and `kk/baseline/codex/kk.rules` as targets in `scripts/generate-guard.sh`; update the Makefile, `generated-check.yml`, `release.yml`, `test/test-generate-guard.sh` and the generated-files text in `AGENTS.md`
- [ ] 7.4 Add a `kk-guard` entry to `.agents/plugins/marketplace.json`
- [ ] 7.5 Port the adapter cases in `test/test-codex-hooks.sh` to the new adapters and add cross-repository anchoring cases; update `test/test-codex-structure.sh` → verify: a live run from a subdirectory enforces a rule from the workspace's `.claude/kk-guard.json`
- [ ] 7.6 Add `kk/lib/guard_identity.py`, a standalone module: SHA-256 over the sorted path, mode and bytes of every file in a guard bundle, leaving out the manifest's `version` field → verify: bundles differing only in version share an identity; a one-byte change or a changed executable bit changes it

## Task 8: Protect toolbox-owned paths in the guard
- **Status:** pending
- **Depends on:** —
- **Size:** S
- **Can run in parallel with:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 7
- **Docs:** [implementation.md#codex-guard-plugin](./implementation.md#codex-guard-plugin), [design.md#guard-changes](./design.md#guard-changes)

### Subtasks
- [ ] 8.1 Add path tokens for the toolbox home, the override directory and the Codex home to `klaude-plugin/scripts/guard/guard.py`, following the temp-directory token
- [ ] 8.2 Add the toolbox home, the override file, the owned files under the Codex home and Codex's plugin cache to `selfmod` in `guard-rules.json`
- [ ] 8.3 Add cases to `test/guard/test_guard.py` for each new path, including a non-default home → verify: an agent edit to each path is denied and a read is not
- [ ] 8.4 Run `make generate-guard` and confirm the documentation table updates

## Task 9: Codex baseline, owned files and `kk codex`
- **Status:** pending
- **Depends on:** Task 1, Task 4
- **Size:** M
- **Can run in parallel with:** Task 6, Task 7, Task 8
- **Docs:** [implementation.md#codex-baseline-and-launch](./implementation.md#codex-baseline-and-launch), [design.md#launching-codex](./design.md#launching-codex)
- **Blocked until:** `design.md` open questions 2 and 4, and the profile and `-C` parts of open question 5, are settled (9.4, 9.7 and 9.9 depend on them)

- **Parts:** 9a — 9.1, 9.3, 9.4, the profile in 9.5, and 9.7: the profile and `kk codex`; 9b — 9.2, the rest of 9.5, 9.6 and 9.8: sub-agents, opt-in rules and `kk apply`; 9c — 9.9, repository instruction imports. The tests in 9.10 grow with each part.
### Subtasks
- [ ] 9.1 Create `kk/baseline/codex.json` from `.codex/config.toml` (no MCP entries; `approval_policy`, `approvals_reviewer` and `sandbox_mode` in the opt-in catalogue, not the defaults) and `kk/baseline/codex/bootstrap.md` from the tool-name mapping in `.codex/scripts/session-start.sh`
- [ ] 9.2 Make generated sub-agents available at `kk/baseline/codex/agents/` through the generator, with a freshness check; keep `.codex/agents/`
- [ ] 9.3 Write the JSON-to-TOML serialiser for the baseline's value shapes → verify: output parses back to the input where a TOML parser is available
- [ ] 9.4 Compose the profile from baseline keys, the opt-in keys the override file switched on, Codex overrides and developer instructions (behavioural instructions, bootstrap text, protected-files advisory); write the composed developer instructions to `$KK_HOME/codex-instructions.md` whenever the profile is written
- [ ] 9.5 Install owned files: the profile, the `kk-` sub-agent files, and the rules file only when the override file switches the native forbids on; check every destination against the installed-paths record at staging and stop on a collision; record each path before writing it and prune by the record, never by prefix; remove the rules file when the switch is turned off; print the account-wide effect the first time the rules file is installed
- [ ] 9.6 Validate the rules file in two steps with `codex execpolicy check`: the candidate alone forbids every command it must, then the candidate with the remaining rules files still loads
- [ ] 9.7 Implement `kk codex`: add the profile, pass through when the adopter names one, refuse per the recorded state table, treat `exec` and `review` as non-interactive (the trust re-read before a non-interactive run arrives with the trust reader in Task 10)
- [ ] 9.8 Implement `kk apply`: rewrite the owned Codex files for the active release from the current override file through the same function as 9.5 and 9.6, under the writer lock, offline, without touching the plugins; record a hash of the override file in the state file at every write; make `kk codex` and `kk status` print one line when the override file no longer matches, without writing anything
- [ ] 9.9 Implement repository instruction imports in `kk codex`: collect `@path` lines from the workspace root's `AGENTS.md` (outside code fences, real path inside the root, no nested imports); ask once per repository and import list on an interactive terminal, default no, storing the answer in one file per repository under `$KK_HOME/imports/`; with a stored yes pass `-c developer_instructions=` built from `codex-instructions.md` plus each file under a heading naming its path; name skipped imports in one line; show the stored answer in `kk status`
- [ ] 9.10 Unit tests for composition with the opt-in keys off and on, serialisation, each refusal, import resolution with an escaping path, a fenced line and a nested import, the confirmation asked once and again when the list changes and never without a terminal, the injected value, `kk apply` installing and removing the rules file as the switch changes with no network, the notice appearing after an override edit and disappearing after `kk apply`, a pre-existing `kk.config.toml` that stops the install untouched, an adopter's `kk-notes.toml` that survives pruning, and a candidate rules file missing a forbid another file supplies → verify: `codex --profile kk debug prompt-input` shows the instructions as a developer message

## Task 10: Codex activation, trust and rollback
- **Status:** pending
- **Depends on:** Task 7, Task 9
- **Size:** M
- **Can run in parallel with:** Task 6
- **Docs:** [implementation.md#codex-activation-and-trust](./implementation.md#codex-activation-and-trust), [design.md#activation-state](./design.md#activation-state)

- **Parts:** 10a — 10.1 to 10.3, activation and guard identity; 10b — 10.4, 10.5, 10.7 and 10.8: trust reader, rollback and the two demonstrations. The tests in 10.6 grow with each part.
### Subtasks
- [ ] 10.1 Write the local Codex marketplace manifest with both plugins; add the marketplace and plugins on first install; compare the tree at the reported install path with the release
- [ ] 10.2 At staging, compute the candidate guard's identity, set a local-checkout guard's staged version from its identity (the installed guard's version when the identities match, otherwise a digest stamp in the form Task 1 found), and fail a tagged candidate that carries the installed version with a different identity; send one event through each staged Codex adapter as its `hooks/hooks.json` registers it; on upgrade re-add the skills plugin when its version differs and the guard plugin only when its identity differs
- [ ] 10.3 Implement the guard-change confirmation, keyed on identity, defaulting to no without a terminal
- [ ] 10.4 Implement the trust reader with the mechanism from Task 1, after [open question 5](./design.md#open-questions) is settled: trust and enablement per guard handler, for a given workspace when the mechanism takes one; record *awaiting review* while any is not effective (untrusted, modified, disabled, or absent for the workspace); without a mechanism, the adopter's acknowledgement gives *unverified*, never *ready*; surface both in `kk status`; make `kk codex` call the reader before a non-interactive run, refuse when a handler is not effective, and warn in one line when the state is *unverified*
- [ ] 10.5 Implement Codex rollback and resumption, including a guard that differs between the two releases; the rollback target skips a release whose guard never got past *awaiting review*, and falls back to the previously active release, naming the unreviewed tool, when no retained release has every tool verified
- [ ] 10.6 Stub-based tests for each activation path; a local checkout whose guard changed under an unchanged manifest version, and one whose guard is unchanged and left alone; a hook disabled after *ready*, which makes `kk codex exec` refuse; the mixed case of Codex *awaiting review* on B, C activated, `kk rollback` restores A with B still on disk; and Codex never reviewed on A or B, where `kk rollback` still restores A and says Codex is unreviewed
- [ ] 10.7 Record demonstration 2 in `verification/task-10/`: interrupt during activation, roll back offline, show a guarded action denied by the restored guard without a trust bypass
- [ ] 10.8 Record demonstration 4 in `verification/task-10/`: promote a release, make its `kk/lib` unavailable, restore the previous release offline through the entry point inside the rollback target, show a guarded action denied by the restored guard

## Task 11: Launch notice, mixed installs and live check
- **Status:** pending
- **Depends on:** Task 6, Task 10
- **Size:** M
- **Can run in parallel with:** Task 12, Task 13
- **Docs:** [implementation.md#notice-mixed-installs-and-live-check](./implementation.md#notice-mixed-installs-and-live-check), [design.md#install-modes](./design.md#install-modes)

### Subtasks
- [ ] 11.1 Implement the launch notice: background check, one-day cache, terminal-only output, silent offline, switchable off → verify: a launch with the network blocked is not delayed and prints nothing
- [ ] 11.2 Detect Git-marketplace installs of the plugin for both tools in `kk status`; offer removal of user-scope installs through the vendor CLIs after confirmation; block *ready* while active hooks are ambiguous
- [ ] 11.3 Implement `kk status --live`: start the session in a scratch directory with the decoy secret inside it, so the workspace-anchored secret patterns match and no legacy guard can produce the same denial → verify: the output contains the guard's own denial text for each tool
- [ ] 11.4 Tests for the cache, the terminal check and mixed-install detection

## Task 12: CI gate and release workflow
- **Status:** pending
- **Depends on:** Task 4, Task 7
- **Size:** S
- **Can run in parallel with:** Task 9, Task 10, Task 11
- **Docs:** [implementation.md#ci-gate-and-release-workflow](./implementation.md#ci-gate-and-release-workflow), [design.md#release-safety](./design.md#release-safety)

### Subtasks
- [ ] 12.1 Add a CI job running the guard engine suite, the `kk` suite, the Codex adapter suite and the self-test cases on the oldest and newest available Python
- [ ] 12.2 Make `release.yml` and `pre-release.yml` run that gate before tagging
- [ ] 12.3 Add the guard plugin version rule to `release.yml` and `pre-release.yml`, comparing identity from `kk/lib/guard_identity.py` with the nearest earlier tag of any kind → verify: a dry run on a skills-only change leaves `kodex-guard`'s manifest untouched; a release candidate with a guard change bumps it; the stable release that follows with the same bytes keeps the candidate's version

## Task 13: Retirement migration in the sync script
- **Status:** pending
- **Depends on:** Task 10
- **Size:** M
- **Can run in parallel with:** Task 11, Task 12
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#removal-rules](./design.md#removal-rules), [design.md#ordinary-sync-and-the-tombstone](./design.md#ordinary-sync-and-the-tombstone)

- **Parts:** 13a — 13.1 to 13.6 and 13.8, the retirement mode with its rules and fixtures; 13b — 13.7, the tombstone, which is independent of 13a.
### Subtasks
- [ ] 13.1 Add a `--retire` mode to `.claude/toolbox/scripts/template-sync.sh` (`parse_arguments` and a separate path in `main`, `--version` naming the retirement tag), previewing with `--dry-run`; it fetches the template at that tag and renders it as a first-time sync does, with nothing merged in from the repository; do not add a `needs_*` / `run_*` migration and do not call the removal functions from `apply_changes`; every existing mode prints one notice naming `kk migrate` → verify: one fixture run through `--local`, a staged `--apply` and `--retire`; only `--retire` removes guard files or hook registrations
- [ ] 13.2 Add the `TEMPLATE_SYNC_MERGE_DENY=1` switch to `apply_substitutions`: leave `permissions.deny` out of `owned_paths` and skip the post-merge assignment of the upstream deny list → verify: with the switch a sync keeps a repository-added deny and removes one the template retired since the base; without it nothing changes
- [ ] 13.3 Remove toolbox hook handlers one at a time by exact command string against the rendered template; drop emptied groups and events; keep all others
- [ ] 13.4 Remove template-supplied entries from the settings file and the Codex config by a removal-only comparison with the rendered template, without the three-way merge: deny entries only when the template has them; keep and report the Codex `sandbox_mode`, `approval_policy` and `approvals_reviewer` whatever their values; keep and report manifest-selected `model`, `effortLevel`, `permissions.defaultMode` and Codex `model` unless the manifest holds the built-in default; remove `statusLine` and report the choice; remove the Git-marketplace enablement and registration
- [ ] 13.5 Remove synced files identical to the rendered template; report and keep files that still differ; remove the two exact import lines; skip and list everything under `sync_exclusions`; stop without removing anything when the template cannot be fetched; remove the sync infrastructure last
- [ ] 13.6 State the team-wide effect in the report; list the kept Codex sandbox and approval settings with the three lines to delete to hand them over to the machine; list the kept manifest choices; list every custom `.claude/CLAUDE.<name>.md` and say Codex stops receiving it without an `@` line in `AGENTS.md`
- [ ] 13.7 Write the tombstone script (accepts every existing option, sources nothing, changes nothing, prints migration guidance, exits successfully, writes `has_changes=false` with `--ci`) and keep it beside the tests until Task 16 installs it → verify: the previous release's script run with `--local`, and with a staged `--apply`, against a fixture upstream holding the tombstone leaves the working tree unchanged apart from the manifest fields that script backfills before handing over
- [ ] 13.8 Add fixtures and cases to `test/test-template-sync.sh` that run the sync step with the deny switch and then `--retire`: capy hooks, an adopter hook, a customised settings file, a deny entry the template never shipped, a manifest selecting a Claude model and a Codex model, a Codex config holding the template's sandbox and approval settings (kept), an edited synced file (overwritten by the sync step and shown in its preview), an edited file under `sync_exclusions` (untouched), and a repository several releases behind that must end in the same state as an up-to-date one → verify: every non-toolbox entry survives byte for byte

## Task 14: `kk migrate` and the migration demonstration
- **Status:** pending
- **Depends on:** Task 11, Task 13
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#migration](./implementation.md#migration), [design.md#verification](./design.md#verification)

### Subtasks
- [ ] 14.1 Implement the guard check in `kk migrate`: for each tool the repository uses, call the trust reader from Task 10, for this repository when the mechanism takes a workspace, and run `kk status --live` unchanged in its scratch workspace; refuse unless the guard's own denial is seen
- [ ] 14.2 Implement the preliminaries: check for `curl` and Mike Farah's `yq` with a message that they are needed for this step only; warn about Codex sessions opened before `kk` was installed, worded from the Task 1 deleted-script result, and ask, default no; fetch `template-sync.sh` and `semver-compare.sh` from the retirement tag into a temporary directory, the tag being a constant in `kk` with a `--retirement-version` override
- [ ] 14.3 Implement the two steps, both with `TEMPLATE_SYNC_NO_HANDOFF=1`: the sync step (`TEMPLATE_SYNC_MERGE_DENY=1`, `--dry-run --version <tag>`; when it reports changes, show them, ask, run `--local --version <tag>`), then the removal step (`--retire --dry-run --version <tag>`, ask, `--retire --version <tag>`); leave the changes uncommitted
- [ ] 14.4 Tests for the refusal when the trust reader reports a disabled hook despite a recorded *ready*, when the tool is *unverified* and the live check fails, for a missing `yq`, for a sync step with nothing to do, and for each declined confirmation, including a declined removal step that leaves the repository synced and guarded
- [ ] 14.5 Record demonstration 3 in `verification/task-14/` on one of the maintainer's repositories, with a Codex session opened before `kk` was installed: a guard is active at every point for sessions started after `kk` became ready, what the older session does is recorded, and the diff shows the team-wide effect

## Task 15: Documentation and ADR
- **Status:** pending
- **Depends on:** Task 11, Task 14
- **Size:** M
- **Can run in parallel with:** Task 18
- **Docs:** [implementation.md#documentation-and-adr](./implementation.md#documentation-and-adr), [design.md#parity-ledger](./design.md#parity-ledger)

### Subtasks
- [ ] 15.1 Write `docs/adr/0014-machine-level-delivery.md` and add it to the ADR table in `docs/contributing/architecture.md`
- [ ] 15.2 Rewrite `docs/getting-started/` around the install command; keep plugin-only as a mode; turn `docs/user-guide/template-sync.md` into a migration guide that covers the two steps of `kk migrate` (the sync step overwrites edits to synced files as any sync does), ordinary sync never retiring, the tombstone, the 14-day supported session lifetime, and not syncing past the retirement release from a script older than v0.21.0
- [ ] 15.3 Update `docs/user-guide/configuration.md`: launcher layer, overrides and when they take effect (the next Claude launch; `kk apply` for Codex), parity exceptions, `Skill(kk:*)` as standing authorisation including future skills, the two Codex opt-ins and the account-wide effect of the native forbids
- [ ] 15.4 Update `docs/providers/codex.md` (guard plugin, hook review, profile precedence, opt-in approval and sandbox defaults, opt-in native forbids, both open-session caveats, `@` imports in `AGENTS.md` with their one-time confirmation, capy guidance from capy's own hooks or an import) and `docs/providers/claude-code.md` (unwrapped-session exception; no coverage for cloud sessions and fresh CI runners from a user-level install)
- [ ] 15.5 Document PAL's Claude client entry in `docs/user-guide/mcp-servers.md`: it runs `kk claude` and keeps the scoped temp-directory read grant → verify: a review launched through the documented entry reads both its criteria and its diff
- [ ] 15.6 Update `README.md`, `AGENTS.md`, `docs/contributing/architecture.md`, `docs/contributing/testing.md`, the plugin READMEs and `mkdocs.yml`; record in the architecture page how to patch the retirement script after retirement (patch tag from a branch at the retirement tag, `kk`'s constant moved to it) → verify: `make docs-build` succeeds

## Task 18: Pilot the tagged release
_Runs before Task 16. It was added after the design review and is numbered 18 so that existing references to Tasks 16 and 17 stay valid._
- **Status:** pending
- **Depends on:** Task 12, Task 14
- **Size:** S
- **Slicing:** Risk-First — retirement is not cheaply undone, and scratch plugins are not what adopters install
- **Can run in parallel with:** Task 15
- **Docs:** [implementation.md#pilot-the-tagged-release](./implementation.md#pilot-the-tagged-release), [design.md#verification](./design.md#verification)

### Subtasks
- [ ] 18.1 Tag a release candidate of the retirement release through the pre-release workflow
- [ ] 18.2 On a machine or user account with no toolbox state, run the installer at the candidate version → verify: every parity-ledger row marked kept or moved is observed, with both Codex opt-ins switched on and off
- [ ] 18.3 In one legacy repository, open a Codex session, then install and review the hooks, then run an ordinary `--local` sync against the candidate → verify: the legacy guard files and hook registrations are intact
- [ ] 18.4 Run `kk migrate --retirement-version <candidate>` in that repository → verify: a new session is guarded throughout; what the older session does is recorded
- [ ] 18.5 Repeat demonstrations 1, 2 and 4 with the shipped guard plugin and the real marketplace names
- [ ] 18.6 Write the results to `verification/pilot/` with tool versions; fix and re-pilot with a new candidate anything the pilot contradicts before the stable retirement release is tagged

## Task 16: Retire the template in this repository
- **Status:** pending
- **Depends on:** Task 15, Task 18
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#retire-the-template](./implementation.md#retire-the-template), [design.md#retiring-the-template](./design.md#retiring-the-template)
- **Blocked until:** the pilot is recorded and the stable retirement release is tagged

### Subtasks
- [ ] 16.1 Move the current `semver-compare.sh` to `.github/scripts/semver-compare.sh`, replacing the stale copy there, and point `release.yml`, `pre-release.yml` and `test/test-semver-compare.sh` at it → verify: a dry run of the release workflow passes its version check
- [ ] 16.2 Replace the sync script with the tombstone from Task 13 and keep its test; remove the sync workflow, the template cleanup script and workflow, the bootstrap script, the example state file and their tests
- [ ] 16.3 Remove the legacy generator targets and the transition copies (`.claude/CLAUDE.extra.md`, `.claude/toolbox/` except the tombstone, `.codex/scripts/`, `.codex/rules/default.rules`, `.codex/agents/`) and update every freshness list
- [ ] 16.4 Reduce this repository's `.claude/` and `.codex/` to an adopter's footprint and run it on `kk` → verify: all suites pass and a wrapped session in this repository shows the guard and the instructions
- [ ] 16.5 The maintainer turns off the repository's template flag

## Task 17: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15, Task 16, Task 18
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 17.1 Run `/kk:test` for the shell and Python suites, the Go tool tests and generated-output freshness; confirm the four demonstrations and the pilot are recorded with tool versions; broaden if a probe contradicted the design after dependent tasks finished or a vendor release changed hook, plugin or settings behaviour
- [ ] 17.1a Run the Task 1 probe 1.9 (`-c developer_instructions=…` size limit) on macOS, deferred from Task 1 by the maintainer on 2026-11-19 → verify: the macOS limit is recorded in `verification/task-1/` beside the Linux one, with the environment size at the time (on macOS the limit covers arguments and environment together), and the import cap in `design.md` follows its rule: 122,880 bytes, or the lower measured limit less 8 KiB if that is smaller
- [ ] 17.2 Confirm the pilot record covers every parity-ledger row marked kept or moved, and observe again any row touched by a change made after the pilot
- [ ] 17.3 Run `/kk:document` to update any remaining docs
- [ ] 17.4 Run `/kk:review-code` with bash and python as the language input
- [ ] 17.5 Run `/kk:review-spec` to verify the implementation matches the design and implementation docs
- [ ] 17.6 If any non-blocking items remain, ask the maintainer how to follow up, for example with GitHub issues
- [ ] 17.7 Move the feature docs from `docs/feat/wip/` to `docs/feat/done/` and update markdown references

## Dependency Graph

```
Task 1 ─┬─→ Task 7 ─┬─→ Task 10 ─┬─→ Task 11 ─→ Task 14 ─┬─→ Task 15 ─┬─→ Task 16 ─→ Task 17
        │           └─→ Task 12  └─→ Task 13 ─→ Task 14  └─→ Task 18 ─┘
        └─→ Task 9 ─→ Task 10
Task 2 ─→ Task 3 ─→ Task 4 ─┬─→ Task 9
                   │        └─→ Task 12 ─→ Task 18
                   └─→ Task 6 ─→ Task 11
Task 5 ─→ Task 6
Task 8 (independent) ─→ Task 17
```
