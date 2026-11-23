# Providers

| Machine installation | Claude Code | Codex |
| --- | --- | --- |
| Start a wrapped session | `kk claude` | `kk codex` |
| Skills | `kk@toolbox`, invoked as `/kk:design` | `kk@toolbox`, invoked as `$kk:design` |
| Guard | Hooks in the Claude plugin | Separate `kk-guard@toolbox` plugin, reviewed in `/hooks` |
| Defaults | Per-launch settings layer and native secret denies | Named profile and owned agent files. Native forbids are an account-wide opt-in. |
| Instructions | Plugin session hook and the project’s `CLAUDE.md` | Profile and project `AGENTS.md`. The launcher supports confirmed imports. |

[Claude Code](claude-code.md) and [Codex](codex.md) describe coverage, configuration precedence and the behavior of unwrapped sessions. For vendor-managed installs, see [plugin-only setup](../getting-started/plugin-only.md).
