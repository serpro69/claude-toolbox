# Architecture Decision Records

Architecture decisions that span more than one feature are recorded as ADRs using [Michael Nygard's template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](../adr/0001-profile-detection-model.md) | Profile Detection Model | Accepted |
| [0002](../adr/0002-profile-content-organization.md) | Profile Content Organization | Accepted |
| [0003](../adr/0003-plugin-root-referenced-content.md) | Plugin Root Referenced Content | Accepted |
| [0004](../adr/0004-skill-workflow-ordering.md) | Skill Workflow Ordering | Accepted |
| [0005](../adr/0005-codex-hook-enforcement-gap.md) | Codex Hook Enforcement Gap | Superseded by 0013 |
| [0006](../adr/0006-composite-artifact-acceptance.md) | Composite-Artifact Acceptance for Domain-Reference Kits | Accepted |
| [0007](../adr/0007-failure-citing-defaults.md) | Producer Rules Are Failure-Citing, Falsifiable Defaults | Accepted |
| [0010](../adr/0010-proportionate-verification.md) | Proportionate Verification and Agent Evaluation | Accepted |
| [0012](../adr/0012-permission-guard-single-declaration.md) | Single Declaration for the Permission Guard | Accepted |
| [0013](../adr/0013-codex-file-access-through-hooked-tools.md) | Codex File Access Runs Through Hooked Tools | Accepted |
| [0014](../adr/0014-machine-level-delivery.md) | Deliver the toolbox per machine | Accepted; Codex profile superseded by 0015 |
| [0015](../adr/0015-codex-launch-overrides.md) | Pass Codex settings as launch flags | Accepted |
| [0016](../adr/0016-python-runtime.md) | Keep machine delivery and the guard in Python | Accepted |

## Location

- Cross-feature ADRs: `docs/adr/NNNN-slug.md`
- Per-feature design docs: `docs/feat/wip/<feature>/` (active) → `docs/feat/done/<feature>/` (completed)
