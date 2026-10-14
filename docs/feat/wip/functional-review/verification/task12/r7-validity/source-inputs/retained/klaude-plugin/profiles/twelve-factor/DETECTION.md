# 12-Factor App — detection

Declares when the `twelve-factor` profile activates. Consumed by `klaude-plugin/skills/_shared/profile-detection.md`. Detection is additive: this profile is expected to co-activate with a domain profile (e.g., `k8s`) on a Kubernetes-shaped service idea.

This is a **design-only** profile. It participates solely in `/kk:design` via the design-token interaction pattern (confirm-gated). It never activates in file-based phases (`review-code`, `review-spec`, `implement`, `test`, `document`) — the three file-signal sections below are intentionally empty.

## Path signals

_None._ The 12-factor methodology has no reliable path signal; code-level factor checks are deferred to a future implement/review-phase adoption and are not part of this profile.

## Filename signals

_None._ No filename identifies a 12-factor app; code-level factor checks are deferred to a future implement/review-phase adoption and are not part of this profile.

## Content signals

_None._ Content inspection cannot distinguish a deployable service from a library or CLI; code-level factor checks are deferred to a future implement/review-phase adoption and are not part of this profile.

## Design signals

display_name: 12-Factor App
tokens:
  - 12-factor
  - twelve-factor
  - SaaS
  - cloud-native app
  - stateless service
  - backing service
  - dev/prod parity
  - horizontally scalable
  - deployable service

Tokens are deliberately narrow. Generic words (`config`, `service`, `deployment`) are excluded to avoid noisy false positives on library, CLI, and tooling ideas. Ambiguous infrastructure ideas that name no specific technology are caught by the shared detection fallback prompt, not by broader tokens here.
