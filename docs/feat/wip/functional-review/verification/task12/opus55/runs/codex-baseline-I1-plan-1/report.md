I’ll use `kk:implement` for task 1 of `settings-receipts`, starting with the plan and repository instructions.


Task 1 has conflicting requirements:

- [design.md](/tmp/fr-opus55-matrix-20261011/codex-baseline-I1-plan-1/docs/feat/wip/settings-receipts/design.md) requires ordinary saves to succeed with the current provider, including when `enhanced_settings` is false.
- [implementation.md](/tmp/fr-opus55-matrix-20261011/codex-baseline-I1-plan-1/docs/feat/wip/settings-receipts/implementation.md) requires rejecting responses without `applied=true`, but defers provider receipts to task 2.

That would report failure for successfully applied saves. Disabling the enhanced UI does not resolve the unconditional client requirement.

Should task 1 preserve legacy-provider success and enforce receipts only when supported?

No files changed or tests run. I paused because [kk:implement](/home/sergio/.codex/plugins/cache/fr-opus55-c2d28c9e-20261011/kk/0.23.0/skills/implement/SKILL.md) requires stopping when the “Plan has critical gaps preventing starting.”
