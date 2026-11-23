# Tagged retirement release pilot

## Environment and preflight

On 2026-11-23 the pilot first tried a fresh non-root account in Docker Desktop 29.9.3 on Linux ARM64. Codex CLI 0.171.0 returned a completed turn, but the harmless shell read failed before execution because Bubblewrap could not create a namespace. This environment did not qualify for the pilot. Capture `de17010e-16d2-437a-af22-4dbd9a549fb2` contains the failed tool result.

The fallback was a fresh Debian 13 ARM64 VM running kernel `6.12.117+deb13-cloud-arm64` under QEMU with hardware acceleration on macOS. The base image was checked against Debian’s published SHA-512 checksum and booted with a disposable disk overlay. The pilot user had no kk state or installation. It used Claude Code 2.1.296, Codex CLI 0.171.0, and Mike Farah’s yq 4.54.3. The same read in Codex’s normal read-only sandbox returned `Public sandbox control` and tool exit 0 (capture `30353dc9-88be-40e7-96d1-39172415c383`). A loopback model transport selects benign tool calls. The vendor CLIs handle configuration, trust, hook execution and sandboxing.

The guest cloned `serpro69/devex-makefile` at `2e578b419f6f75af63c4fa0e2c486b4658ba8cba`. Before installing kk, the operator inspected its two legacy registrations, trusted the workspace and reviewed the hooks through the normal Codex terminal prompts. That session completed an ordinary text-only turn. The guest could reach the public GitHub API, and its separate recovery network namespace contained only loopback with no external route.

## Publication gate

The first workflow run on `03060c82` stopped before tagging. Both Python jobs failed the same trust-reader test: the host’s `PATH` lacked Codex, so executable discovery failed before the mocked hook responses were used. The test now uses its own fixture environment. With the host Codex excluded it failed before the correction and passed afterwards (captures `0d99adb2-f78f-45b6-ac93-b1f6da1ecdce` and `7d79f8c7-1983-491f-9654-f2e6583af539`). The correction is `4db31c5d`. [First workflow run](https://github.com/serpro69/claude-toolbox/actions/runs/45151071618)

## RC1

The hosted workflow on `4db31c5d` passed and published `v0.26.0-rc.1` at `44b087d1db83bd4b66ec6cc30fcf25e79d9a4c93`. In the clean guest, the downloaded installer matched the script in that tag. Installing with `--version v0.26.0-rc.1` recorded the public repository and the requested tag in the journal. Claude was ready. Codex listed three untrusted handlers (capture `a31b4256-696f-4c2b-8dbe-a3d80bdb5909`). [Release](https://github.com/serpro69/claude-toolbox/releases/tag/v0.26.0-rc.1) · [Successful workflow](https://github.com/serpro69/claude-toolbox/actions/runs/45155624701)

### Codex hook review scope

The published setup guide directed the adopter to review hooks in `kk codex`. On Codex 0.171.0 that selects the named `kk` profile as the vendor’s write target. After selecting **Trust all and continue** for the three managed handlers, only `kk.config.toml` changed. It acquired three `hooks.state` entries. The account’s `config.toml` retained its previous digest. `kk status` still reported three untrusted handlers, and `kk apply` regenerated the owned profile and removed its entries. The scratch check refused Codex and verified Claude (capture `61a24787-21e7-4c9e-aad1-e3bd57364b99`).

Repeating the review in plain `codex` with no named profile wrote the three decisions into the account configuration. Both tools then reported ready. The decision survived `kk apply` and both scratch sessions returned the installed guard’s own denial (capture `68286581-3c73-4575-b220-da94780a8f6b`). This second path allowed the remaining RC1 checks to run. The published onboarding path still requires correction and a new candidate pilot.

### Settings, session continuity and migration

- The released Claude launcher supplied its native deny list, high effort, declared environment, statusline path, skill wildcard and read grant. An additional settings layer selected low effort and retained the denies. Individual project preferences took precedence. In a trusted wrapped terminal the released statusline displayed the model, context, project and Git branch. The named Codex profile loaded with its declared model, reasoning, limits, instructions and TUI, and its owned agent files matched the release. The approval/sandbox defaults and native rules were absent initially, took effect after opt-in and `kk apply`, and were removed on opt-out. The vendor policy evaluator returned `forbidden` for its public sample (capture `68286581-3c73-4575-b220-da94780a8f6b`).
- The loopback transport observed behavioral instructions on actual Claude and Codex model requests. After an interactive confirmation, the wrapped Codex request also contained the marker from the repository import. Capture `a9b50a52-b4cc-4da8-9a97-b8eed7abd24e`.
- The repository’s existing sync script ran `--local --version v0.26.0-rc.1`. The two original registrations and their scripts remained present. A Codex session opened after readiness received the guard’s denial for a repository-local public canary before and after sync (capture `fac5c19a-6dd4-48f0-8aa0-080be5e82fab`).
- The pre-install terminal was closed before confirming retirement. Its earlier text-only turn completed normally. The behavior of a legacy-only session left open after removal was observed separately in Task 1. In the post-readiness thread `01a207fc-3ac1-7c01-879b-69c71de387a6`, the same canary remained denied after retirement. Both fresh scratch sessions also returned their own guard denials. The legacy clone had 21 changed tracked files, two insertions, 4,204 deletions and no staged changes (capture `28546c34-fceb-45f1-8083-79f6ad0e7f10`).

The two wrapped workspaces actually sent different Codex models to the loopback transport: `gpt-6.2-astra` in the control, and the retained project choice `gpt-6-astra` in the legacy clone (capture `73378cb6-4d38-4a64-be0d-ab995212bd4b`). Trusted Claude terminals displayed the released statusline. Its default Catppuccin and requested Nord palettes produced different output bytes on identical input (capture `32b300d3-d0af-482f-bb9e-c852bb68f4eb`).

### Open-session upgrade and offline recovery

| Demonstration | RC1 observation |
| --- | --- |
| 1. Skills-only upgrade | The local checkout of the tagged payload added an inert marker to a skill. The real skills cache contained the update, the guard manifest retained its device, inode and SHA-256, and thread `01a207fc-3ac1-7c01-879b-69c71de387a6` again received the guard denial. |
| 2. Interrupted activation | An inert package note changed the local candidate’s guard bundle identity while retaining the released handler/runtime bytes. After the actual vendor registered it, the fixture interrupted acknowledgement. The journal still named RC1 as active and recorded `activating / codex-add-kk-guard`. Offline rollback restored RC1, cleared the candidate and both scratch sessions returned guard denials. |
| 4. Promoted command unavailable | After promoting the skills-only variant, the fixture moved its `kk/lib` directory aside. The recovery command from the retained RC1 dispatcher ran offline. RC1 returned to ready, both live probes received guard denials, and the journal had no pending candidate. |

The offline checks ran as the ordinary pilot user in a network namespace containing only loopback. Local model fixtures served the public canaries. Demonstrations 1 and 4 used capture `5c0f05c8-039d-4dbb-8099-68ca6bb06c48`. In the first attempt at demonstration 2, the confirmation input arrived early and the candidate stayed staged. The retry waited for the confirmation prompt and reached the intended vendor checkpoint (capture `fdcfa207-d2ef-402e-af65-7ccc0dc25b19`).

### RC1 disposition

RC1 is unsuitable for stable promotion. The maintainer chose account-level review in plain `codex`. A separate new-project control also confirmed that accepting folder trust from the wrapped TUI changed the generated profile and blocked the next wrapped batch launch (capture `f4ca638d-a222-4000-8425-62abf6577b3c`). The next candidate must exercise the corrected onboarding from a clean account.

## RC2

Correction `ad7e7f13` directs persistent hook and folder decisions to plain Codex and explains how to recover a modified generated profile. The three focused diagnostic tests passed, the full `test/test-kk.sh` suite passed 79 tests, and the strict documentation build passed (captures `3d0727de-abd3-479f-87d7-43dd5bbed2be`, `34830d0f-f1a7-46d5-84ab-d7905dbd73d6` and `fe78c8fd-66c9-412d-9c7b-a6f953eb5462`). [RC2 publication workflow](https://github.com/serpro69/claude-toolbox/actions/runs/45159643630)

The repeat uses a fresh disposable Debian disk, the same vendor binaries and the same legacy Git revision. The pre-install terminal completed a text-only turn in thread `01a20807-fa9a-7e21-b9ec-9c3da007ed18`. The harmless shell control returned its expected contents under the normal Codex sandbox. The account had no kk installation or journal (captures `1a7ed424-8e7f-48a0-8922-45900c3fc5a8` and `82569d03-4197-4afa-8df3-211f1531dc4c`).

The workflow passed both Python gates and published `v0.26.0-rc.2` at `373fbc0b99ae2eb4ae3d9193de9b5d90b36d429c`. The public installer matched the tag. Review in plain Codex saved all three managed hook decisions and both tested workspace decisions in the account configuration. The generated profile was byte-identical before and after these reviews, and both live scratch checks passed.

**RC2 is unsuitable for stable promotion.** The next ordinary `kk codex` TUI launch in an already trusted workspace persisted its model-tip counter in the named profile. Parsing the before/after TOML found one added integer at `tui.model_availability_nux."gpt-6.1-sol"`. Codex also reformatted the inline TUI table. The account config remained intact, but a wrapped batch command refused the regenerated-profile mismatch (capture `15f39659-0de0-49e3-8c42-5aae81cb3681`). Repeating account-level review would not repair that routine UI write.

A local trial changed the serialization to put the TUI table last. The same Codex binary appended only the numeric tip table, preserving every preceding byte. With the matching preflight correction, the first wrapped batch shell read returned the public control file and both actual guards denied the live canaries (capture `fe1e7059-c0e2-4c9b-87fb-f99aa76ab1c8`). A new tagged clean-account pilot is required.

The final checker accepts distinct model keys with unsigned 32-bit counters only. A local TUI-to-batch repeat, both live guards, opt-in parity and confirmed imports all passed (capture `4eab332f-1035-4696-9374-828b97f8e54d`). The 80-test kk suite passed, as did the focused counter-bound regression and strict docs build (captures `859ec0c3-41de-419f-9ccf-e3346391468e`, `baf54348-dadf-4d67-b569-36dd3a46daf6` and `41046138-680a-4182-8ffc-fb7225aa034f`). [Codex configuration schema](https://developers.openai.com/codex/config-schema.json)
