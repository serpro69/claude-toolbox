# Milestone 1 — `/kk:review-architecture` — detailed design

**Status:** Design. Part of [../design.md](../design.md) (architect-supporting skills). Milestone 1.

**Deliverable:** a `/kk:review-architecture` skill + a read-only `architecture-reviewer` agent that reviews a written architecture artifact against the system it claims to describe, using a claim-driven verification engine that is falsifiable and eval-able throughout.

---

## 1. The altitude line (the organizing principle)

**`review-architecture` verifies the EXISTENCE and TOPOLOGY of declared mechanisms — never their behavioral correctness.**

- Architecture altitude: "is there an idempotency-key column / a circuit breaker targeting dependency D / a Redis client in the read path / a `/v2/` route."
- Behavioral altitude (OUT — belongs to `/kk:review-code`, `/kk:review-spec`): "does the code *use* the key correctly / actually degrade to read-only / actually stay idempotent under retries."

This line is the load-bearing constraint. Without it every dimension silently expands into whole-system reasoning, the LLM hallucinates to fill the gap, and the skill stops being gradeable. With it, each check reduces to *"locate the bounded evidence this claim implicates; confirm the mechanism is present."* The entire rubric, input contract, and eval strategy are consequences of this choice.

**Security architecture is delegated OUT** to the PAL `secaudit` MCP tool (`mcp__pal__secaudit`) — there is no `kk:` security skill. Grading trust boundaries / authN-authZ enforcement / data-classification flow drags the reviewer into runtime/authZ analysis; the skill description states this explicitly and points to the PAL tool for threat modeling.

## 2. Input contract — acceptance vs normalization (two orthogonal questions)

### 2a. Acceptance — what is allowed through the door

`review-architecture` accepts a **committed written artifact that makes falsifiable structural/decision claims**:

- one or more ADRs (`docs/adr/`), or
- a broader architecture doc, or
- the architecture section of a design doc.

Diagrams count **only** when accompanied by prose asserting what they mean. **Verbal or diagram-only proposals are out of scope** until captured as an artifact — that capture is a future M2 *producer* skill's job, not the reviewer's. This mirrors every existing reviewer (code→diff, design→doc, spec→design+impl): each demands claims already committed to text.

M1 only *reads* whatever architecture docs exist; it never writes a broader architecture doc, so the "where do broader docs live" question is deferred to M2 and is **not blocking** here.

### 2b. Normalization — heterogeneous prose → uniform claim-set

An ADR and a loose design-doc section both pass acceptance but express claims in different shapes. The engine needs a consistent list of `{claim, implicated-evidence-location}` tuples.

If extraction were a *hidden* internal step, an eval could not distinguish "reviewer failed to verify a claim" from "extractor never found the claim" — two failure modes collapse into one ungradeable blur, and you grade the extractor's interpretation instead of the artifact.

**Resolution:** extraction is an **explicit, inspectable intermediate artifact** — the derived claim-set is written out and graded on its own. This is **Pass 0**.

## 3. Engine shape — three passes (0 + 6 + 1)

Each pass has its own eval seam so no pass does two jobs:

- **Pass 0** — Claim Extraction (normalize).
- **Pass 1** — Topology Verification (6 dimensions).
- **Pass 2** — Decision Soundness (1 dimension).

## 4. Pass 0 — Claim Extraction

Turns the accepted artifact into the explicit `{claim, implicated-evidence-location}` claim-set. Graded on **three separable sub-metrics** — this separation is what makes the whole engine eval-able:

1. **Precision — "did it invent a claim?"** Self-grounding: every extracted claim cites a span in the artifact; the grader confirms that span actually asserts it. No gold set needed; works in eval and production.
2. **Recall — "did it miss a claim?"** Intrinsically extrinsic.
   - *In evals:* fully gradeable, and **not a new burden** — the oracle is the fixture's expected-claim list, which *is* the `assertions[]` array the eval convention already mandates. Recall-grading = set-difference against that list.
   - *In production:* unprovable (no oracle); a missed claim is silent. This is the **one irreducible limitation** — per fail-loud it is **documented, not hidden**: the reviewer does not certify extraction completeness.
3. **Evidence-location accuracy — "right target per claim?"** Eval-gradeable against expected locations; in production partially self-checking — a claim pointing at a nonexistent path/symbol is a catchable dangling reference.

**Production recall mitigations (raise recall without a gold set):**

- **Structural-slot heuristics per artifact type** — an ADR *must* have decision/options/consequences → assert each slot yielded ≥1 claim; catches gross omissions. (Per-artifact-type catalog is an implementation detail — see §9.)
- **Optional ensemble extraction** — N passes, union claims; a confidence *estimate*, never a completeness *proof*. Worth-the-token-cost is measured during eval (§9).

No circularity: grading is strictly easier than producing — "is this claim in the text" is a bounded lookup, recall-grading is a set-diff, dangling-location detection is a file check.

## 5. Pass 1 — Topology Verification (six dimensions)

Each claim is graded **per-claim** in one of two modes:

- **Reality mode** — evidence exists → locate the bounded evidence the claim implicates, verify.
- **Internal-soundness fallback** — forward-looking/greenfield, no evidence → grade that the claim is well-formed.

"Consistency with reality" is this *mode*, not a separate dimension.

The six dimensions (`claim class → evidence source → greenfield fallback`):

1. **Structural Boundaries** — "X is isolated from Y at the dependency tier." Evidence: **static dependency manifests** (`go.mod`, `package.json` workspaces, `pom.xml`, module-level imports) — **not** synthesized call graphs (LLM-intractable). Fallback: boundaries + permitted dependency directions are named.
2. **Data Ownership** — "Service A is the sole mutating owner of entity E." Evidence: schema ownership/migrations, mutating route bindings (PUT/POST/DELETE) bound to one service. Fallback: every entity has exactly one named owner; dependents' read paths defined.
3. **NFR Mechanisms** — "System uses mechanism M (cache/CDN/sharding) to meet its NFRs." Evidence: structural presence of the mechanism. Fallback: NFRs are quantified and mapped to a mechanism (the *outcome* "p99<200ms" is statically unverifiable; the *mechanism* is).
4. **Failure Isolation** — "Boundary X survives dependency Y failing." Evidence: timeouts/retries/bulkheads/circuit-breaker topology. Fallback: each boundary enumerates degradation behavior.
5. **State Consistency** — "Mutation on E is safe from duplicates/races." Evidence: idempotency keys, queue dedup config, unique constraints, saga state machines. Fallback: delivery semantics (exactly-once vs at-least-once) declared per mutating crossing.
6. **Evolution & Versioning** — "Boundary X deploys independently of its consumers." Evidence: API version routing, migration tooling (Flyway/Liquibase), expand/contract configs. Fallback: backward-compat/migration strategy stated.

**Design notes:**

- **4 and 5 are kept separate** — failure isolation (availability) and state consistency are opposing physics (CAP); a blended verdict gives muddy eval signal (cannot distinguish "has circuit breakers, no idempotency" from the reverse).
- **Dimension 6 closes a real gap** — strict boundaries (1) + isolated ownership (2) produce a *distributed monolith* unless boundaries can evolve independently.

## 6. Pass 2 — Decision Soundness & Reversibility

**Not a peer of the six topology dimensions — it has no reality branch.** It runs only in internal-soundness mode: it grades the artifact's *reasoning* against the artifact's *own stated context*:

- Are the mechanisms chosen in Pass 1 appropriate **given the constraints the document itself states**? (Doc claims write-heavy but specifies a write-through cache with no stale-read mitigation → fails.)
- Are one-way vs two-way doors identified, and do irreversible decisions carry proportional justification?

Why a separate pass, not a seventh row: Pass 1 is a strict `extract → grep bounded evidence → grade` loop; Pass 2 needs whole-artifact context and has no greppable evidence. Forcing it into Pass 1's schema wrecks the prompt (the model hunting "grep evidence" for a philosophical trade-off). Separation also keeps evals clean: **Pass 1 evals test extraction+verification; Pass 2 evals test judgment.** "Appropriateness" — the highest-value architectural judgment — lives here, scoped to *stated context* because true appropriateness (write-heavy vs read-heavy in reality) needs live profiling the agent cannot do.

## 7. Profiles — optional enrichment, NOT load-bearing

A modern agent can deduce evidence-gathering mechanics ("grep `go.mod` for the forbidden import") from a few short **inline examples** embedded in the skill. Profiles are only warranted where a domain has **non-obvious gotchas** the agent won't infer (e.g., k8s: a Deployment claiming HA needs `podAntiAffinity`, not just `replicas: 3`).

So M1 ships evidence-gathering examples inline. Profile detection in `review-architecture` and a profile `architecture/` phase are **deferred to M4** and are not required for the engine to work.

## 8. Eval strategy

Evals live at `klaude-plugin/skills/review-architecture/evals/<name>/{eval.json,test-files/}` per the toolbox convention (one directory per eval; real fixtures, not inline-in-prompt). Each pass gets its own seam:

- **Pass 0 fixtures** — an artifact + a gold claim-set (the `assertions[]`) → grade precision / recall / location.
- **Pass 1 fixtures** — a fixed claim-set + a `test-files/` codebase slice where some claims hold and some are violated → assert the reviewer catches the false ones, does not flag the true ones, and correctly falls back to internal-soundness where no evidence exists.
- **Pass 2 fixtures** — an artifact with a stated-context/mechanism mismatch → assert the reviewer flags the inappropriate choice.
- **Regression eval** — a clean artifact that should produce no findings.

## 9. Open questions (deferred, documented)

- **Broader-architecture-doc home** (`docs/architecture/` vs `docs/wip/<x>/architecture.md`) — deferred to M2; M1 only reads.
- **Per-artifact-type structural-slot heuristic catalog** (§4) — implementation detail; enumerate as Pass 0 is built.
- **Pass 0 ensemble worth the token cost?** — measure during eval before committing to it.

## Assumptions

- The LLM reliably greps static manifests for topology evidence given inline examples (§7).
- The gold-claim-set-as-`assertions[]` approach makes recall gradeable in evals without extra authoring burden (§4).
- Hand-written ADRs / design-doc architecture sections exist to review on day one (before M2 producers).

## Not Doing (M1)

- Producer skills (`decompose`/`decide`/`model`) — M2.
- The nested architecture flow and architecture-implement hand-off — M3.
- Profile `architecture/` phase and profile detection in `review-architecture` — M4.
- Behavioral / runtime verification — belongs to `/kk:review-code` / `/kk:review-spec`.
- Security architecture — delegated to PAL `secaudit`.
- Writing broader architecture docs — M1 only reads.

## Rejected Alternatives

- **Accept-everything input** (verbal/diagram-only) — ungradeable; forces the reviewer to do extraction *and* evaluation (altitude blur).
- **Role-axis execution units** — under-scoped, no eval surface.
- **Five merged dimensions** (blast-radius + idempotency in one) — muddy eval signal (§5).
- **Hidden extraction step** — collapses two failure modes into one (§2b).
- **Call-graph evidence for boundaries** — LLM-intractable; use static dependency manifests (§5.1).
- **Pass 2 as a peer topology dimension** — breaks the Pass-1 map-reduce contract (§6).
