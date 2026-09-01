# Pass 1 — Topology Verification

Consumes the Pass 0 claim-set ([pass0-extraction.md](pass0-extraction.md)) and assigns **exactly one verdict per claim** routed to a topology dimension (`1`–`6`). Claims routed to `pass2`, `delegated`, or `unrouted` are NOT handled here — they flow straight to the report's Not Reviewed / Pass 2 sections per [output-contract.md](output-contract.md).

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
| `ill-formed` | internal-soundness | `future` (or fallback) claim missing a required structural element (e.g. a proposed boundary that names no permitted dependency direction) |

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

<!-- Build order (M1): dimensions 4 (Failure Isolation), 5 (State Consistency), and 6 (Evolution & Versioning) land in Task 4, which extends this file. Until then, Pass 0 still routes claims to 4/5/6 (the routing table in pass0-extraction.md is complete), but their verification procedures are not yet specified here. Remove this comment when Task 4 adds the three dimensions. -->

## Output

Feed one verdict per topology-routed claim into the report's **Verdicts by dimension** section, grouped by dimension, each stating its mode and — for reality mode — the resolved evidence path inspected. Apply the verdict→severity mapping from [output-contract.md](output-contract.md) (`violated` P1, `dangling-anchor`/`ill-formed` P2).
