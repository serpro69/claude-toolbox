# 12-Factor App — required design sections

Every `design.md` for a feature with the `twelve-factor` profile active must include the four grouped sections below. Omit none; if a section genuinely does not apply, state so explicitly with a one-line justification — silent omissions hide scope gaps, and a reviewer (or `/kk:review-spec`) cannot tell absence-by-intent from absence-by-oversight.

Section order is not mandated; the sections must all be present. Each section names the factors it covers (Roman numerals per [12factor.net](https://12factor.net/)) so a reviewer can trace every factor to a place in the document.

**Deployment-context preamble (I, II).** Open the first 12-factor section (or the document's context section) with one line stating the codebase and dependency posture: one codebase in version control with N deploys, and dependencies explicitly declared (exact, version-pinned) and isolated from system-wide packages. Codebase and dependencies fold into this preamble rather than a standalone section; expand only if the idea deviates (e.g., multiple apps sharing a codebase, or reliance on host-installed tools).

**Co-active domain profiles — merge, don't duplicate.** When another profile (e.g., `k8s`) is active and its required sections already cover an overlapping concern — disposability / graceful shutdown, config and secrets, rollout and rollback, logs — cover the factor **once**: write it in the domain profile's section and, in the corresponding 12-factor section below, cross-reference that section by name instead of restating it. Every factor must still be visibly addressed somewhere in the document; a cross-reference counts, a silent gap does not. For `k8s` specifically: graceful shutdown (IX) and rollout/rollback (V) belong in its **Reliability posture** and **Failure-mode narrative**; the secrets source (the secrets half of III) in its **Security posture**. `k8s` has no required logs/observability section, so logs (XI) stay owned by **Parity & observability** below even under co-activation. The 12-factor sections then reference the `k8s` sections and add only what `k8s` leaves uncovered (env-var config strategy, backing-service swappability, statelessness, sudden-death/idempotency, dev/prod parity, admin processes, logs).

## Config & backing services (III, IV)

- Config-source strategy — environment variables as the default; if a deviation is used (secret manager, mounted config, config service), name it and justify it. State how strict separation of config from code is preserved and where per-environment config lives.
- Attached resources — enumerate every backing service (database, cache, queue, object store, SMTP, third-party APIs). For each: how it is attached (URL/credentials in config) and confirmation that it is swappable between local and managed instances via config alone, with no code change.

## Process model & concurrency (VI, VIII, VII)

- Statelessness — the process is share-nothing; name where session/user state lives (a backing service with expiration), and confirm nothing correctness-critical lives in process memory or on local disk across requests.
- Process types — enumerate them (web, worker, cron/scheduler) and state that each scales horizontally by adding processes/replicas. Call out any singleton constraint and how it is enforced.
- Port binding — the service is self-contained and exports its protocol by binding to a configured port; no runtime-injected webserver dependency.

## Release & disposability (V, IX, XII)

- Build / release / run separation — how a release is uniquely identified (immutable version), and the guarantee that a release is never mutated after creation.
- Rollback — to which artifact, triggered by whom, and the observable signal that confirms success.
- Disposability — startup time and what gates readiness; graceful shutdown on SIGTERM (web: stop accepting, drain in-flight; worker: return or finish the current job); robustness against sudden death, with worker jobs reentrant / idempotent so an interrupted job can be safely retried.
- Admin / one-off processes — how migrations, scripts, and console sessions run in the same release artifact, environment, and config as the long-running processes.

## Parity & observability (X, XI)

- Dev / prod parity — the concrete gaps between development and production (time, personnel, tools), why each exists, and which parity risks are accepted (e.g., a lighter local substitute for a backing service).
- Logs as event streams — the app writes unbuffered to stdout; the execution environment owns routing, aggregation, and retention. Name the collector/pipeline if known, or state that it is the platform's concern.
