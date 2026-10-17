# 12-Factor App — design question bank

Questions used during idea refinement when the `twelve-factor` profile is active. Ask one per message, per the skill's rule. Order is risk-first — config and backing services usually constrain the most downstream choices.

**Skip any question already answered.** Before asking, check: the user's idea prose and prior answers in this session; the codebase; prior decisions (`kk:arch-decisions`, `kk:project-conventions`); any existing `design.md`; **and any other active profile's question bank**. A question answered anywhere in that set is not asked again.

**Defer to co-active domain profiles.** When a domain profile (e.g., `k8s`) is active alongside this one, it owns the factors it already covers — do not re-ask them here. Concretely, when `k8s` is active it already asks the rollback trigger (factor V), the graceful-shutdown window — `terminationGracePeriodSeconds` / `preStop` / drain (factor IX), structured logs to stdout and the log collector (factor XI), and the **secrets** source — ESO / Sealed Secrets / Vault / native / workload identity (the secrets half of factor III). It does **not** ask whether non-secret config lives in environment variables versus committed files, so the env-var config-strategy question under III is still asked here. Ask only the twelve-factor questions the domain profile leaves uncovered (for `k8s`, typically: env-var config strategy under III, sudden-death robustness and job idempotency under IX, backing-service swappability under IV, statelessness and state location under VI, dev/prod parity gaps under X, and admin/one-off processes under XII). Extend the same reasoning to any other co-active profile by comparing its question bank against the list below.

## Config (III)

- Is config stored in **environment variables** — the strict factor-III form — rather than in committed config files or constants? Config here means everything that varies between deploys: backing-service handles, credentials, per-deploy hostnames.
- If a deviation is used (secret manager, mounted config file, config service), name it and justify it — what does it buy over env vars, and how is the strict separation of config from code preserved?
- Where does config live per environment (dev / staging / prod), and who owns changes to it?

## Backing services (IV)

- Which backing services attach — database, cache, queue, object store, SMTP, third-party APIs? Enumerate them.
- Is every one of them swappable via config alone, with no code change, between a local instance and a managed/third-party instance (e.g., local Postgres ↔ RDS, local Redis ↔ managed Redis)?

## Build, release, run (V)

- How is a release uniquely identified (immutable version — timestamp, incrementing number, commit SHA + config hash)? Can a release be mutated after creation, and if so how is that prevented?
- How do you roll back — to which artifact, triggered by whom, and what observable signal confirms rollback succeeded?

## Processes / statelessness (VI)

- Is the process share-nothing? Does any correctness-critical state live in process memory or on local disk across requests?
- Where does session/user state live — a backing service with time-expiration (e.g., Redis), never sticky sessions or local files?

## Concurrency (VIII)

- What is the scale-out model — which process types exist (web, worker, cron/scheduler), and is each scaled horizontally by adding processes/replicas rather than by growing a single process?
- Does anything require exactly one instance (a singleton scheduler, a leader)? If so, how is that constraint enforced and what happens on failover?

## Disposability (IX)

- Startup — how fast does a process go from launch to ready, and what blocks readiness (migrations, cache warm-up, connection pools)?
- Graceful shutdown — on SIGTERM, does the web process stop accepting new requests and drain in-flight ones? Does the worker return the current job to the queue (or finish it) before exiting?
- Sudden death — is the design robust against an abrupt exit (crash-only design)? Are worker jobs **reentrant / idempotent** so a job interrupted mid-flight can be safely retried after the process dies?

## Dev / prod parity (X)

- What differs between dev and prod, and why — across the time gap (how long code sits before deploy), the personnel gap (who writes vs. who deploys), and the tools gap (SQLite vs. Postgres, local queue vs. managed queue)?
- Are the same backing-service types and versions used in development as in production, or is a lighter substitute used locally? If substituted, what parity risk is accepted?

## Admin processes (XII)

- How are one-off tasks (schema migrations, data fixes, REPL/console sessions, scripts) run? Do they ship in the same release artifact and run against the same environment and config as the long-running processes?

## Port binding (VII) and logs (XI)

- Is the service self-contained, exporting HTTP (or another protocol) by binding to a port, with no reliance on a runtime-injected webserver? How is the port supplied (config, env)?
- Are logs written as an unbuffered event stream to stdout, with routing, aggregation, and retention handled by the execution environment rather than by the app (no log files managed by the app)?

## Codebase and dependencies (I / II)

Usually a given; ask only when the idea leaves them unclear.

- One codebase tracked in version control, deployed many times — or does the idea imply multiple apps sharing code (which should be factored into libraries)?
- Are dependencies **explicitly and exactly declared** (version-pinned lockfile/manifest) **and isolated** (no reliance on system-wide packages or implicit tools such as `curl` or `ImageMagick` on the host)?
