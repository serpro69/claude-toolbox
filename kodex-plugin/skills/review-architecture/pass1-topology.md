# Pass 1 — Topology Verification

Consumes the Pass 0 claim-set ([pass0-extraction.md](pass0-extraction.md)) and assigns **exactly one verdict per claim** routed to a topology dimension (`1`–`7`). Claims routed to `pass2`, `delegated`, or `unrouted` are NOT handled here — they flow straight to the report's Not Reviewed / Pass 2 sections per [output-contract.md](output-contract.md).

## The altitude line (repeat, because it is the whole game)

You verify that a declared mechanism **exists** and is wired into the right **topology** — never that it behaves correctly. "Is there an idempotency-key unique constraint" is Pass 1; "does the code stay idempotent under concurrent retries" is `$kk:review-code`. The instant a dimension starts reasoning about runtime behavior it has left this pass — the check stops being a bounded evidence lookup and the model starts hallucinating to fill the gap. Every dimension below reduces to: *locate the bounded evidence this claim implicates; confirm the mechanism is present with the expected topology.*

## The anchor rule — mode decision (do this per claim, before verifying)

Absence of evidence is ambiguous on its own: a missing mechanism is simultaneously the *violation* signal ("the claimed mechanism isn't there") and the *greenfield* signal ("it isn't built yet"). Leave that ambiguity implicit and the reviewer is either toothless (every absence excused as not-built-yet) or false-positive-prone (every proposed mechanism flagged missing). The day-one input is Accepted ADRs *proposing* mechanisms inside existing repos, so both failure modes are live. The anchor rule resolves it explicitly, per claim:

1. **`tense: future`** (from Pass 0 — Proposed status, prospective wording) → **internal-soundness mode**. A proposal is never graded against the repo; skip straight to the dimension's fallback criteria. Do not resolve an anchor, do not grep the repo.
2. **`tense: present`** → resolve the claim's **anchor** first. The anchor is the *component or boundary the claim names* — a service directory, a module, a manifest — **not the mechanism itself**. (For "the `billing` service must not depend on the order schema", the anchor is the `billing` service, not the dependency edge.)
   - **Anchor exists → reality mode.** Locate the bounded evidence, verify the mechanism. A mechanism absent *inside an anchor that exists* is a **`violated`** verdict — this is the case the reviewer exists to catch.
   - **Anchor does not exist → `dangling-anchor`.** A present-tense claim about a component that is not in the repo is doc drift or a false claim; both are findings. This is its own loud verdict, never a silent fallback to "greenfield." No evidence was inspected, so report the *searched* locations and the conclusion "anchor not found" in the Evidence field (reality mode still owes an evidence line per [output-contract.md](output-contract.md)).

**Determine the claim's polarity before applying "absent ⇒ `violated`".** The rule above is written for *affirmative* claims, where the mechanism is a thing that should be present (a cache, an idempotency key, a circuit breaker). Many claims — especially Dimension 1 boundaries — are **prohibitive**: "X must **not** depend on Y." There the claimed "mechanism" is the *absence* of a forbidden edge, so the polarity inverts: a forbidden edge **present** is the `violated` case, and its **absence** is `verified`. Read the claim's polarity first, then apply "is the claimed condition satisfied inside the existing anchor?" — never a blind "absence ⇒ violated," which would flip every boundary verdict.

**Why the anchor is the component, not the mechanism.** If you resolved the *mechanism* as the anchor, every genuine violation would masquerade as a dangling-anchor ("the circuit breaker isn't there, so I guess the anchor doesn't exist") and the reviewer would never fire. Anchoring on the component the claim names keeps "the component is missing" (drift) distinct from "the component is here but the mechanism inside it is not" (violation).

"Consistency with reality" is this *mode selection*, not a separate dimension.

### Verdict vocabulary (full table in [output-contract.md](output-contract.md))

| Verdict | Mode | When |
| --- | --- | --- |
| `verified` | reality | anchor exists; mechanism present with the expected topology |
| `violated` | reality | anchor exists; mechanism absent or contradicted inside it |
| `dangling-anchor` | reality | present-tense claim; the named component/boundary is not in the repo |
| `internally-sound` | internal-soundness | `future` (or fallback) claim that satisfies its dimension's well-formedness criteria |
| `ill-formed` | internal-soundness¹ | `future` (or fallback) claim missing a required structural element (e.g. a proposed boundary that names no permitted dependency direction) |

¹ With one mode-independent exception: a kit enforcement pointer citing an entry in an unresolvable or missing counterpart page grades `ill-formed` **regardless of mode** — see Dimension 7's cross-page-pointer rule.

Internal-soundness mode is **not a rubber stamp**: a proposal still earns `ill-formed` when it omits the structural element its dimension requires. The mode changes *what* you check (well-formedness of the claim vs presence in the repo), not *whether* you check.

### Self-check before emitting a reality-mode finding

Re-read the evidence behind every `violated` / `dangling-anchor` verdict before reporting it. Drop any you cannot substantiate on re-inspection — a false `violated` is more damaging than a missed one, because it trains the reader to distrust the reviewer.

## Dimensions 1–3

Each dimension below gives its **claim class → evidence source → greenfield fallback**, plus an **inline evidence-gathering example** (the profile substitute — a modern agent can generalize the grep from one worked case; profiles are deferred to M4).

### Dimension 1 — Structural Boundaries

- **Claim class:** "X is isolated from Y at the dependency tier" / "X must not depend on Y."
- **Evidence source — static dependency manifests, NOT synthesized call graphs.** `go.mod` / `require` + import statements, `package.json` workspace deps, `pom.xml` `<dependency>`, module-level `import`/`use`. Synthesizing a call graph to prove isolation is LLM-intractable and drifts into behavioral reasoning; a forbidden edge in a *static manifest or import list* is bounded and checkable. That is the only evidence this dimension trusts.
- **Reality mode:** resolve the anchor (X's module/service directory). Inspect its manifest and imports for a dependency on Y. A forbidden edge present → **`violated`**. Absent → **`verified`**.
- **Greenfield fallback (internal-soundness):** the claim names the boundaries *and* the permitted dependency direction. A proposal that says "X and Y are strictly isolated at the dependency tier" — an isolation claim with no stated direction of which side may depend on which — is **`ill-formed`**; one that states "billing may call the orders API; orders never imports billing" is **`internally-sound`**. (A vaguer "keep them loosely coupled" often has no dimension keyword at all and is dropped to `unrouted` back in Pass 0 before it ever reaches this fallback.)

> **Inline example.** Claim: "`billing` must not depend on the order schema module" (`present`, prohibitive, anchor = `billing` service). Resolve the anchor: confirm `services/billing/` exists. Then use the **Grep tool** (the reviewer has no shell — Grep/Glob/Read only) with pattern `orders/schema` scoped to path `services/billing/` (it covers `go.mod` and the `*.go` imports). A hit (e.g. `import "github.com/acme/orders/schema"`) is a forbidden static edge → `violated`; no hit → `verified` — prohibitive polarity, so the *absence* of the forbidden edge is the passing case.

### Dimension 2 — Data Ownership

- **Claim class:** "Service A is the sole mutating owner of entity E" (readers reach E only through A's API).
- **Evidence source:** schema ownership and migrations (which service's migration directory defines/alters E's table), and **mutating route bindings** — `POST`/`PUT`/`PATCH`/`DELETE` handlers for E bound to exactly one service. A *second* service holding migrations or mutating routes for E contradicts sole ownership.
- **Reality mode:** resolve the anchor (owner service A). Confirm A holds E's migrations/mutating routes. Then check that no other service does. Another writer found → **`violated`**. A exists and is the only writer → **`verified`**. A exists but holds *no* migrations or mutating routes for E — even when nobody else does either → **`violated`**: the claimed ownership mechanism is absent inside an existing anchor (a vacuous "sole owner" that owns nothing is still a false ownership claim). (If A itself is absent → `dangling-anchor`.)
- **Greenfield fallback (internal-soundness):** every named entity has exactly one named owner, and dependents' read paths are defined (API, read replica, event stream). A proposal that leaves an entity with two owners, or a reader with no stated read path, is **`ill-formed`**.

> **Inline example.** Claim: "the `orders` service is the sole mutating owner of the Order entity" (`present`, anchor = `orders`). Confirm the owner: Grep for the `orders`-table definition under `services/orders/migrations/`. Then hunt for *other* writers in two Grep-tool steps (the tool has no pipe): (1) Grep pattern `(POST|PUT|PATCH|DELETE).*/orders` across path `services/` with glob `*.go`; (2) from those hits, discard any file under `services/orders/`. A surviving mutating `orders` route — or an `orders`-table migration in another service — → `violated`; none → `verified`.

### Dimension 3 — NFR Mechanisms

- **Claim class:** "the system uses mechanism M (cache / CDN / shard / replica) to meet an NFR."
- **Evidence source — structural presence of the mechanism, never the NFR outcome.** The *outcome* ("p99 < 200ms") is statically unverifiable — you cannot confirm a latency target by reading code, and trying to drags you across the altitude line. The *mechanism* is: a Redis/Memcached client in the read path, a CDN/`Cache-Control` config, a shard key, a read-replica connection string. Verify the mechanism's existence and placement; the NFR number itself is out of scope.
- **Reality mode:** resolve the anchor (the service/path the NFR governs). Confirm the mechanism is present and sits in the right place (a read-through cache must be *in the read path*, not merely a dependency somewhere). Mechanism absent inside the existing anchor → **`violated`**. Present and correctly placed → **`verified`**.
- **Greenfield fallback (internal-soundness):** the NFR is quantified *and* mapped to a named mechanism — both halves are required. "It'll be fast" (neither) and "we'll add a cache to keep it responsive" (mechanism named, target unquantified) are both **`ill-formed`**; "p99 < 200ms via a Redis read-through cache on the orders read API" is **`internally-sound`** (you are grading that the claim names a checkable mechanism *and* a quantified target, not that 200ms is achievable).

> **Inline example.** Claim: "a Redis read-through cache fronts the orders read API to meet p99 < 200ms" (`present`, anchor = `orders` read path). Grep the read path for the mechanism: pattern `redis|go-redis|cache` scoped to path `services/orders/read/`. A Redis client wired into the read handler → `verified`; the read path hitting the DB directly with no cache client → `violated`. Do **not** attempt to confirm the 200ms figure — that is the unverifiable outcome, not the mechanism.

## Dimensions 4–6

Same shape as 1–3 (**claim class → evidence source → greenfield fallback**, plus an inline Grep-tool example). Dimensions 4 and 5 sit on opposite sides of the CAP trade-off — failure isolation buys *availability*, state consistency buys *correctness under concurrency* — so they are **graded independently, never blended**. A service can ship a circuit breaker (dim 4 `verified`) and still have no idempotency guard on its mutations (dim 5 `violated`); a single "is it resilient" verdict would hide exactly that gap. Resolve each dimension's evidence on its own and emit its own verdict.

### Dimension 4 — Failure Isolation

- **Claim class:** "Boundary X survives dependency Y failing" / "X degrades gracefully when Y is down."
- **Evidence source — the failure-handling topology wrapping the cross-boundary call, never the runtime behavior.** Whether X *actually* degrades correctly when Y dies is behavioral (`$kk:review-code`). What is checkable here is the *presence and placement* of an isolation mechanism around the call to Y: a circuit breaker or timeout wrapping the client, a bulkhead pool, a declared fallback path. A raw call to Y with no guard is the absence this dimension catches.
- **Reality mode:** resolve the anchor (X's service/module). Find the call site to Y and confirm it is wrapped in a failure-isolation mechanism (breaker / timeout / bulkhead / fallback). An unguarded call to Y inside the existing anchor → **`violated`**. Wrapped → **`verified`**.
- **Greenfield fallback (internal-soundness):** the claim enumerates degradation behavior for each named dependency (fail fast, serve stale, queue-and-retry). A proposal that asserts a boundary "survives" a dependency without naming *how* it degrades is **`ill-formed`**; one stating "when payments is down, order creation queues and returns 202" is **`internally-sound`**.

> **Inline example.** Claim: "the `orders` service survives `payments` failing — every payments call is wrapped in a circuit breaker" (`present`, anchor = `orders`). Grep path `services/orders/` with pattern `gobreaker|CircuitBreaker|hystrix|breaker|Timeout` to locate the mechanism, then confirm it actually wraps the payments client call (a breaker declared but never applied to the call is not placed correctly). A breaker around `paymentsClient` → `verified`; a direct `paymentsClient.Charge(...)` with no breaker/timeout in the path → `violated`. Do **not** reason about whether the fallback returns *correct* data — presence and placement of the mechanism is the check.

### Dimension 5 — State Consistency

- **Claim class:** "Mutation on E is safe from duplicates/races" / "writes to E are idempotent / exactly-once."
- **Evidence source — the structural consistency mechanism on the mutating path, never race-freedom at runtime.** Whether the code stays correct under concurrent retries is behavioral (`$kk:review-code`). What is checkable: an idempotency key with a **unique constraint**, a DB unique index, queue/consumer dedup config, an optimistic-lock version column, a saga/state-machine definition. Absence of any such mechanism on a mutating path is the finding.
- **Reality mode:** resolve the anchor (the owner service / mutation path). Confirm a consistency mechanism is present on that path — a `UNIQUE` index on the idempotency/request key in a migration, a dedup setting on the consumer, a version column. A mutating path with no such mechanism inside the existing anchor → **`violated`**. Present → **`verified`**. **Placement matters as much as presence** (as in dims 3 and 4): the mechanism must cover *the key the claimed mutation writes* — a `UNIQUE` index on an unrelated column (say `users.email`) is not evidence for a claim about create-order dedup. Match the constraint/column to the entity and operation the claim names before accepting a bare token hit as `verified`.
- **Greenfield fallback (internal-soundness):** delivery semantics (exactly-once vs at-least-once) are declared per mutating crossing *and* a dedup/idempotency strategy is named. A proposal that asserts "writes are safe" with neither declared semantics nor a named mechanism is **`ill-formed`**.

> **Inline example.** Claim: "order creation is idempotent — the create-order mutation is guarded by an idempotency key with a unique constraint" (`present`, anchor = `orders`). Grep the mutating path in two scopes: pattern `idempotency|UNIQUE|unique index|request_id|dedup` across path `services/orders/migrations/` and the create handler. A `UNIQUE` constraint on an `idempotency_key` column → `verified`; a create-order `INSERT` with no unique/idempotency guard → `violated`. **A present circuit breaker (dim 4) does not satisfy this** — grade the state-consistency mechanism on its own evidence, independently of the availability mechanism.

### Dimension 6 — Evolution & Versioning

- **Claim class:** "Boundary X deploys/evolves independently of its consumers."
- **Evidence source — the compatibility mechanism that lets X change without breaking consumers, never a claim about zero-downtime rollout.** Whether a deploy is *actually* zero-downtime is behavioral (`$kk:review-code`). What is checkable: API version routing (`/v1/`, `/v2/` route prefixes, versioned proto/package names), and migration tooling that carries expand/contract evidence (additive/nullable columns, a paired backfill-then-contract migration). Strict boundaries (dim 1) plus isolated ownership (dim 2) with **no** evolution mechanism is a distributed monolith — this dimension closes that gap **when the artifact asserts independent evolution**; absent a dim-6 claim, emit no dim-6 verdict (Pass 1 emits one verdict per *extracted* claim, never a synthesized one).
- **Reality mode:** resolve the anchor (X's service). Confirm a compatibility mechanism that *decouples X's changes from its consumers* — not merely that some migration machinery exists. A bare `migrations/` directory is **not** sufficient: nearly every service has one, and it is also dimension 2's evidence source, so its presence proves nothing about independent evolution. Accept **consumer-facing version routing** (versioned routes / proto packages) **or** migration tooling bearing **expand-contract** shape → **`verified`**. A single unversioned route mutated in place with no compatibility mechanism, under a claim of independent evolution → **`violated`**.
- **Greenfield fallback (internal-soundness):** a backward-compat / migration strategy is stated (versioning scheme, expand-contract, deprecation window). A proposal claiming independent deployability with no stated compatibility strategy is **`ill-formed`**.

> **Inline example.** Claim: "the `orders` API evolves independently of its consumers via versioned routes" (`present`, anchor = `orders`). Grep `services/orders/` with pattern `/v1/|/v2/|apiVersion` at route registration; if the claim instead rests on migrations, Glob pattern `services/orders/migrations/*` (Glob matches files, not directories) and read the latest migration for expand-contract shape — additive/nullable columns, not a destructive in-place `ALTER`/`DROP`. Consumer-facing versioned route prefixes, or expand-contract migrations → `verified`; a single unversioned `/orders` route mutated in place → `violated`. A bare `migrations/` directory whose latest migration is a destructive in-place alter is **not** evidence of independent evolution.

## Dimension 7 — Domain Binding

The domain-reference kit's dimension ([pass0-extraction.md](pass0-extraction.md) routes a kit's per-term **Bindings** lines and rules-table **enforcement pointers** here). Same shape as every dimension: claim class → evidence source → fallback outcomes.

- **Claim class:** "domain concept X is bound to code element Y" — Y naming a **code-element kind**: a directory, a collection/constant, a field, or a symbol. A rules-table enforcement pointer ("L3 is enforced at `<file>` `<symbol>`") is the same claim class with the rule as the concept.
- **Evidence source — existence only, via Grep/Glob.** The named element exists at the cited location: the directory is there (Glob), the symbol/field/constant is declared in the cited file (Grep). This is pure existence-and-topology. **The altitude line holds:** whether the code's *behavior* matches the term's definition — whether the symbol does what the glossary says the concept means — is `$kk:review-code` / `$kk:review-spec` territory, never this dimension. Likewise a rule's *intent-truth* is never verified here: the enforcement pointer's existence is dimension-7 evidence; whether the rule is desired business policy is exactly what its provenance label defers to humans (Pass 2, Check C).
- **Reality mode (anchor rule applied):** the **anchor is the cited location** — the directory or file the binding names; the **mechanism is the named element inside it**. Cited file/directory absent from the repo → **`dangling-anchor`** (the kit cites a location that is not there — doc drift). Location exists but the named symbol/field/constant is not declared in it → **`violated`** (the binding's mechanism is absent inside an existing anchor). All named elements present at their cited locations → **`verified`**.
- **Greenfield fallback (internal-soundness) — both outcomes:** a `future` term carrying **`Bindings: none yet`** is **`internally-sound`** (the kit says outright that no binding exists; nothing to grade against the repo). A binding claim that **names no code-element kind at all** (e.g. "will be represented in code" — neither an element kind nor a location class) is **`ill-formed`** — regardless of tense: with no named location there is no anchor to resolve and no element to check, so the claim has no checkable shape in either mode.
- **Cross-page pointers (mode-independent).** An enforcement pointer may cite a traps-page entry instead of code ("see traps `D2` — declared, not enforced"). Resolve it against the counterpart page: the cited `D#`/`P#` entry **present** → **`verified`**, with the counterpart entry as the evidence (a documented divergence is the kit doing its job, **not** a finding — emit the verdict, never a re-report of the divergence). The cited entry **absent** — or the counterpart page itself unresolvable (single-page kit, per [input-contract.md](input-contract.md)) — → **`ill-formed`**: the claim's required supporting element is missing. This is the one place `ill-formed` fires **regardless of mode** — never silently skip a pointer whose target page is missing.

> **Inline example.** Claim: "the Voucher concept is bound to `services/orders/vouchers/`, symbol `Voucher.Code`" (`present`, anchor = the cited location `services/orders/vouchers/`). Glob pattern `services/orders/vouchers/*` to confirm the directory exists, then Grep pattern `type Voucher|Code` scoped to that path. Directory present and a `Voucher` type with a `Code` field declared → `verified`; directory present but no `Voucher` declaration anywhere in it → `violated`; no `services/orders/vouchers/` in the repo at all → `dangling-anchor`. Do **not** check whether voucher codes are validated correctly — element existence at the cited location is the whole check.

## Output

Feed one verdict per topology-routed claim into the report's **Verdicts by dimension** section, grouped by dimension, each stating its mode and — for reality mode — the resolved evidence path inspected. Apply the verdict→severity mapping from [output-contract.md](output-contract.md) (`violated` P1, `dangling-anchor`/`ill-formed` P2).
