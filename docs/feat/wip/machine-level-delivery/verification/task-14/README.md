# Repository migration on macOS

On 2026-11-23, a disposable clone of the maintainer’s `devex-makefile` at `2e578b419f6f75af63c4fa0e2c486b4658ba8cba` went through both steps of `kk migrate`. One Codex session opened after the machine guard became ready stayed open throughout. It received a guard denial in all three phases.

The host ran Claude Code 2.1.296, Codex CLI 0.171.0, Bash 5.3.15 and Mike Farah’s yq 4.54.3 on Apple silicon. Both vendors used a disposable home. The maintainer signed into Codex and reviewed its hooks. Codex reported five trusted, enabled registrations in the clone. Two came from the repository and three from `kk-guard@toolbox`.

## What ran

The active local `kk` release was `local-95b8c46b39504319b9db7be04bc7dc54`. The repository’s starting template revision was `c2d28c9e3064a0a71a0e5ac3748a9616c794eb61`. The retirement scripts and template came from the local test tag `v0.26.0-task14.2` at `cc6325d99e3dd0461234d1fd8fb13bfabed7314d`. A local transport served the two script downloads from those Git blobs and redirected the template fetch to the same repository. The hosted release candidate is covered by Task 18.

The final sync-script revision also fixes nested MCP tables when a server registration needs regeneration. The full sync suite exercised that case after the local tag was cut.

| Phase | Observation |
| --- | --- |
| Before sync | Both vendors reported ready. Their scratch probes returned the installed guard’s denial for separate public canaries. A Codex thread in the repository also received the guard’s denial for a repository-local public canary. |
| After sync | The first migration accepted the sync and declined retirement. The manifest named the new tag and the legacy adapter remained on disk. The same Codex thread again received the guard denial. |
| After retirement | The second migration found no sync changes and asked only for the initial and retirement confirmations. The legacy registrations and scripts were removed. The same thread received the guard denial again, and fresh Claude and Codex scratch sessions independently returned their guard denials. |

Codex thread `01a2079f-de96-7803-840c-3b006b8690e1` remained in a single app-server process. Its router attributed all three denials to the PreToolUse hook and named the exact public canary rule. Both vendors used loopback model responses during migration. The fixtures selected the benign read. The vendor processes loaded their installed plugins, evaluated trust, ran the hooks and reported the results. An earlier attempt using the hosted Codex model timed out in the live check after 90 seconds. The migration stopped before sync and the old manifest remained in place.

An older Codex terminal was opened in the clone before installation and had already exited by removal. Task 1 separately observed that an older legacy-only session could continue without its guard. That observation is the basis for the default-no warning. On 2026-11-23, the maintainer accepted it as sufficient evidence for the older-session part of Task 14.5. [Task 1 vendor evidence](../task-1/README.md)

## Team-wide diff

The clone kept its original `HEAD` and had no staged changes. Its tracked diff contained 21 changed files, one insertion and 4,196 deletions. The source checkout remained clean.

```text
$ git diff --name-status -- .claude/settings.json .codex/config.toml .codex/hooks.json .codex/rules/default.rules .github/template-state.json .github/workflows/template-sync.yml
M       .claude/settings.json
M       .codex/config.toml
D       .codex/hooks.json
D       .codex/rules/default.rules
D       .github/template-state.json
D       .github/workflows/template-sync.yml
```

| Change in the clone | Effect if committed |
| --- | --- |
| Removed `.codex/hooks.json`, project adapters and `.codex/rules/default.rules` | Collaborators need the machine guard to replace the repository guard. Restoring the native forbids requires enabling the account-wide rules file. |
| Removed template deny entries, Git-marketplace enablement and the legacy statusline from `.claude/settings.json` | A fresh cloud or CI checkout can no longer rely on the committed plugin enablement. Unwrapped Claude sessions lose the template’s native denies. Four adopter deny entries and the selected Claude model survived. |
| Kept the Codex model, MCP registrations, `sandbox_mode = "read-only"`, `approval_policy = "on-request"` and `approvals_reviewer = "user"` | The retained repository settings continue to take precedence over machine defaults. |
| Removed the sync workflow, manifest and toolbox instruction imports | The repository no longer syncs the template. Its existing `@.capy/AGENTS.md` import survived. |

## Capture references

| Evidence | Capy run |
| --- | --- |
| Scratch guard checks before migration | `66eb9660-214a-4b9f-a4c9-9be7bb7de502` |
| Live-check timeout before any sync | `1bd46d14-e2a5-4d0f-9b76-3541f3c3351c` |
| Sync applied, retirement declined | `fdefc9b0-cb6b-4b08-a217-02063db3344a` |
| No-change sync preview, retirement applied | `84e00f2f-ccb3-4f8d-adce-7f2b2894f1b7` |
| One Codex thread across all three phases | `d16e95e9-113d-421d-b8b1-95902e11676b` |
| Fresh scratch guard checks after retirement | `8c7d57c1-2098-4f48-bfbb-63b8d29999ea` |
