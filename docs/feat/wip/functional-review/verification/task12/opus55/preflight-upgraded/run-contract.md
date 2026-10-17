# Opus 5.5 runtime preflight after CLI upgrade

Declared 2026-10-11 before fresh probes. The user upgraded Claude Code and
requested a retry. Claude Code is now **2.1.296**; all other identities,
permissions, evidence requirements and scope in
[the initial declaration](../preflight/run-contract.md) remain unchanged.
The original 2.1.272 network-enabled probe failed before actor execution with
`claude_code_version_too_old`: the API required 2.1.280 or newer.
The first restricted-network attempt was interrupted and has no completed seal.
Neither attempt is a measured result or a successful binding.

Use new workspaces and evidence destinations. Freeze this declaration with the
existing reviewed successor runner before probing. Main and forced subagent
remain `claude-opus-5-5`/high. PAL remains explicitly deferred. These probes
establish runtime and instruction binding only; measured matrix execution needs
its own final controller freeze. Preserve all prior attempts.
