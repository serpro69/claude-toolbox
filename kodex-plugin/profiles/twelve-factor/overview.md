# 12-Factor App profile

## What this profile covers

The classic twelve factors from [12factor.net](https://12factor.net/) — a cross-cutting methodology for building deployable, scalable, portable services — applied through a **design-phase lens**. The profile raises the factors where architectural decisions are made (config strategy, backing services, statelessness, disposability, dev/prod parity), when they are cheap to change. It does not verify that resulting code is factor-aligned; that is a separate, deferred concern.

Adjacent-but-out-of-scope: the *Beyond the Twelve-Factor App* extensions (API First, Telemetry, Security/Authentication & Authorization), any language- or platform-specific implementation checks, and architecture-level review of existing systems.

## When it activates

Only in `$kk:design`, via the design-token interaction pattern, and only after the user confirms. The idea prose must match one of the tokens declared under `## Design signals` in [DETECTION.md](DETECTION.md) (e.g., `stateless service`, `backing service`, `SaaS`, `12-factor`). Ambiguous infrastructure ideas that name no technology reach this profile through the shared fallback prompt.

It **never** activates in file-based phases (`review-code`, `review-spec`, `implement`, `test`, `document`): all three file-signal sections in `DETECTION.md` are empty by design. Libraries, CLIs, and tooling therefore never receive service-only questions.

Activation is additive. On a Kubernetes-shaped SaaS idea both `k8s` and `twelve-factor` activate; the design content below defers overlapping factors to the domain profile so each factor is asked and documented once.

## Populated phases

- `design/` — idea-refinement question pool ([design/questions.md](design/questions.md)) and required design-doc sections ([design/sections.md](design/sections.md)), loaded via [design/index.md](design/index.md).

No other phase is populated.

**Authoring note.** This file is a human/authoring reference required by profile convention. The design flow does **not** load it — it reads `DETECTION.md` for tokens and the `design/index.md` always-load entries. Any factor content the flow must act on lives in `design/questions.md` and `design/sections.md`, not here.

## The twelve factors in one screen

| #    | Factor              | One-line statement                                                                              |
| ---- | ------------------- | ----------------------------------------------------------------------------------------------- |
| I    | Codebase            | One codebase tracked in version control, many deploys.                                          |
| II   | Dependencies        | Explicitly declare (exact, version-pinned) and isolate dependencies; no reliance on system-wide packages. |
| III  | Config              | Store config in environment variables; strict separation of config from code.                   |
| IV   | Backing services    | Treat backing services (DB, cache, queue, SMTP, object store) as attached resources swappable via config. |
| V    | Build, release, run | Strictly separate build and run stages; releases are immutable and uniquely identified.        |
| VI   | Processes           | Execute the app as one or more stateless, share-nothing processes; persist state in backing services. |
| VII  | Port binding        | Export services via port binding; the app is self-contained and does not rely on runtime injection of a webserver. |
| VIII | Concurrency         | Scale out via the process model — process types (web, worker, cron) scaled horizontally.        |
| IX   | Disposability       | Fast startup, graceful shutdown on SIGTERM, robustness against sudden death; jobs are reentrant/idempotent. |
| X    | Dev/prod parity     | Keep development, staging, and production as similar as possible (time, personnel, tools gaps). |
| XI   | Logs                | Treat logs as event streams written unbuffered to stdout; routing/storage is the environment's job. |
| XII  | Admin processes     | Run admin/management tasks as one-off processes in the same release and environment as the app. |

## Looking up dependencies

This profile introduces no dependencies of its own. For the primary methodology text, the canonical source is [12factor.net](https://12factor.net/) (mirrored at the `twelve-factor/twelve-factor` GitHub repository). When a design decision under this profile requires a concrete library or platform choice (a config loader, a queue client, a process manager), follow the `$kk:dependency-handling` skill's cascade under the co-active language or platform profile — this profile does not carry per-technology lookup targets.
