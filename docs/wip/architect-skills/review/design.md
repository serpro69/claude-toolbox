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

`review-architecture` accepts **exactly one committed written artifact per invocation** that makes falsifiable structural/decision claims:

- an ADR (`docs/adr/`), or
- a broader architecture doc, or
- the architecture section of a design doc.

Single-artifact scope is deliberate: Pass 1 verifies claims independently and Pass 2 grades an artifact against its *own* stated context — nothing in the engine detects contradictions *between* artifacts (a superseded ADR contradicting its successor). Accepting artifact sets would silently imply cross-artifact consistency checking the engine does not do. Multi-artifact review is deferred (see §Not Doing).

Diagrams count **only** when accompanied by prose asserting what they mean. **Verbal or diagram-only proposals are out of scope** until captured as an artifact — that capture is a future M2 *producer* skill's job, not the reviewer's. This mirrors every existing reviewer (code→diff, design→doc, spec→design+impl): each demands claims already committed to text.

M1 only *reads* whatever architecture docs exist; it never writes a broader architecture doc, so the "where do broader docs live" question is deferred to M2 and is **not blocking** here.

### 2b. Normalization — heterogeneous prose → uniform claim-set

An ADR and a loose design-doc section both pass acceptance but express claims in different shapes. The engine needs a consistent claim-set (full schema in §4).

If extraction were a *hidden* internal step, an eval could not distinguish "reviewer failed to verify a claim" from "extractor never found the claim" — two failure modes collapse into one ungradeable blur, and you grade the extractor's interpretation instead of the artifact.

**Resolution:** extraction is an **explicit, inspectable intermediate artifact** — the derived claim-set is written out and graded on its own. This is **Pass 0**.

## 3. Engine shape — three passes (0 + 6 + 1)

Each pass has its own eval seam so no pass does two jobs:

- **Pass 0** — Claim Extraction (normalize).
- **Pass 1** — Topology Verification (6 dimensions).
- **Pass 2** — Decision Soundness (1 dimension).

## 4. Pass 0 — Claim Extraction

Turns the accepted artifact into the explicit claim-set. **Pass 0 is repo-blind** — it reads only the artifact, never the codebase. Every field below is derivable from the artifact text alone; this keeps extraction pure normalization and precision grading span-grounded.

**Claim schema** (one entry per extracted claim):

| Field | Content |
| --- | --- |
| `id` | Stable per-review identifier (`C1`, `C2`, …). |
| `claim` | The assertion, tightly paraphrased. |
| `source_span` | The artifact quote (or heading + line) grounding it. |
| `dimension` | One of the six Pass 1 dimensions, `pass2` (decision/trade-off claims), `delegated` (security → PAL `secaudit`), or `unrouted` (fits nothing). `delegated`/`unrouted` claims are never dropped — they surface in the report's Not Reviewed section (§7). |
| `tense` | `present` (describes the system as it is) or `future` (proposed/intended). Derived from artifact metadata (ADR status: Accepted vs Proposed) plus claim wording. Drives the Pass 1 mode decision (§5). |
| `evidence_class` | The *abstract* class of evidence the claim implicates ("dependency manifests of service A", "mutating route bindings for entity E") — never a resolved repo path. Pass 1 resolves classes to concrete paths; Pass 0 stays repo-blind. |

Graded on **four separable sub-metrics** — this separation is what makes the whole engine eval-able:

1. **Precision — "did it invent a claim?"** Self-grounding: every extracted claim cites a span in the artifact; the grader confirms that span actually asserts it. No gold set needed; works in eval and production.
2. **Recall — "did it miss a claim?"** Intrinsically extrinsic.
   - *In evals:* fully gradeable against a structured **`gold-claims.json`** in the eval's `test-files/`; the `assertions[]` bullets reference its entries ("claim G3 is extracted"), so the eval-grader grades each expected claim PASS/FAIL — no free-form set arithmetic.
   - *In production:* unprovable (no oracle); a missed claim is silent. This is the **one irreducible limitation** — per fail-loud it is **documented, not hidden**: the reviewer does not certify extraction completeness.
3. **Evidence-class accuracy — "right evidence class per claim?"** Eval-gradeable against the gold set's expected classes. (Resolved-path dangling references are Pass 1's concern — the anchor rule, §5.)
4. **Routing accuracy — "right `dimension` and `tense` per claim?"** Eval-gradeable against the gold set. A misrouted claim sends a verifiable assertion to the wrong verifier or the wrong mode — a distinct failure mode that, ungraded, collapses back into the blur §2b exists to prevent.

**Production recall mitigations (raise recall without a gold set):**

- **Structural-slot heuristics per artifact type** — an ADR *must* have decision/options/consequences → assert each slot yielded ≥1 claim; catches gross omissions. (Per-artifact-type catalog is an implementation detail — see §10.)
- **Optional ensemble extraction** — N passes, union claims; a confidence *estimate*, never a completeness *proof*. Worth-the-token-cost is measured during eval (§10).

No circularity: grading is strictly easier than producing — "is this claim in the text" is a bounded lookup, recall-grading is a per-entry lookup against the gold file, routing-grading is a label comparison.

## 5. Pass 1 — Topology Verification (six dimensions)

Each claim is graded **per-claim** in one of two modes:

- **Reality mode** — locate the bounded evidence the claim implicates, verify.
- **Internal-soundness mode** — grade that the claim is well-formed.

**Mode decision — the anchor rule.** Absence of evidence is ambiguous on its own: it is simultaneously the violation signal ("claimed mechanism missing") and the greenfield signal ("not built yet"). Left implicit, the reviewer is either toothless (every absence excused as greenfield) or false-positive-prone (every proposed mechanism flagged missing — and the day-one input is ADRs *proposing* mechanisms in existing repos). The rule, per claim:

1. `tense: future` (from Pass 0 — Proposed ADR status, forward-looking wording) → **internal-soundness mode**. Proposals are never graded against the repo.
2. `tense: present` → resolve the claim's **anchor** — the component/boundary the claim names (service directory, module, manifest), not the mechanism itself.
   - **Anchor exists → reality mode.** A mechanism absent inside an existing anchor is a **violation** — the case the reviewer exists to catch.
   - **Anchor does not exist → `dangling-anchor`** — its own loud verdict (§7), never a silent fallback. A present-tense claim about a component that is not there is doc drift or a false claim; both are findings.

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

- Are the mechanisms chosen in Pass 1 appropriate **given the constraints the document itself states**? (Doc claims write-heavy but specifies a write-through cache → fails: a read-optimizing cache taxes every write to serve a minority read path. *The original "with no stale-read mitigation" gloss is imprecise — write-through writes cache and store synchronously, so it never serves stale reads; the clash is read-optimizer-vs-write-heavy. The M1 eval builds it that way.*)
- Are one-way vs two-way doors identified, and do irreversible decisions carry proportional justification?

Why a separate pass, not a seventh row: Pass 1 is a strict `extract → grep bounded evidence → grade` loop; Pass 2 needs whole-artifact context and has no greppable evidence. Forcing it into Pass 1's schema wrecks the prompt (the model hunting "grep evidence" for a philosophical trade-off). Separation also keeps evals clean: **Pass 1 evals test extraction+verification; Pass 2 evals test judgment.** "Appropriateness" — the highest-value architectural judgment — lives here, scoped to *stated context* because true appropriateness (write-heavy vs read-heavy in reality) needs live profiling the agent cannot do.

## 7. Output contract

**Invocation:** `/kk:review-architecture <artifact-path>` — exactly one artifact per invocation (§2a); a second path argument is rejected with guidance to run per artifact. For a design doc, an optional heading argument scopes the review to its architecture section. No path given → list candidate artifacts (`docs/adr/`, `docs/wip/*/design.md`) and ask.

**Report** (presented inline, mirroring the review-skill family):

1. **Claim Set** — the full Pass 0 output, verbatim. This *is* the inspectable intermediate artifact (§2b): the read-only reviewer agent has no Write tool, so the report section is the artifact's home.
2. **Verdicts by dimension** — one verdict per claim: `verified` / `violated` / `internally-sound` / `ill-formed` / `dangling-anchor`.
3. **Not Reviewed** — `delegated` claims (with a `secaudit` pointer) and `unrouted` claims, listed explicitly. Fail-loud: extraction happened, review didn't, and the report says so.
4. **Pass 2 findings** — appropriateness / reversibility.

**Severity mapping** (reuses the review family's P0–P3 scale):

| Verdict | Severity |
| --- | --- |
| `violated` | P1 — escalates to P0 when Pass 2 marks the underlying decision a one-way door |
| `dangling-anchor` | P2 |
| `ill-formed` (internal-soundness claim missing required elements) | P2 |
| Pass 2 inappropriate-mechanism / missing reversibility justification | P1 / P2 |
| `unrouted` / `delegated` | informational |

## 8. Profiles — optional enrichment, NOT load-bearing

A modern agent can deduce evidence-gathering mechanics ("grep `go.mod` for the forbidden import") from a few short **inline examples** embedded in the skill. Profiles are only warranted where a domain has **non-obvious gotchas** the agent won't infer (e.g., k8s: a Deployment claiming HA needs `podAntiAffinity`, not just `replicas: 3`).

So M1 ships evidence-gathering examples inline. Profile detection in `review-architecture` and a profile `architecture/` phase are **deferred to M4** and are not required for the engine to work.

## 9. Eval strategy

Evals live at `klaude-plugin/skills/review-architecture/evals/<name>/{eval.json,test-files/}` per the toolbox convention (one directory per eval; real fixtures, not inline-in-prompt). Each pass gets its own seam:

- **Pass 0 fixtures** — an artifact + a structured `gold-claims.json` in `test-files/`; `assertions[]` bullets reference gold entries → grade precision / recall / evidence-class / routing per entry.
- **Pass 1 fixtures** — a fixed claim-set + a `test-files/` codebase slice where some claims hold and some are violated → assert the reviewer catches the false ones, does not flag the true ones, and applies the anchor rule correctly.
- **Anchor-rule fixture** — an existing codebase slice + a claim-set mixing a `future` proposal, a `present` violated claim, and a `present` claim naming a nonexistent component → assert internal-soundness / violation / dangling-anchor respectively (all three outcomes discriminated).
- **Pass 2 fixtures** — an artifact with a stated-context/mechanism mismatch → assert the reviewer flags the inappropriate choice.
- **Regression eval** — a clean artifact that should produce no findings.

## 10. Open questions (deferred, documented)

- **Broader-architecture-doc home** (`docs/architecture/` vs `docs/wip/<x>/architecture.md`) — deferred to M2; M1 only reads.
- **Per-artifact-type structural-slot heuristic catalog** (§4) — implementation detail; enumerate as Pass 0 is built.
- **Pass 0 ensemble worth the token cost?** — measure during eval before committing to it.

## Assumptions

- The LLM reliably greps static manifests for topology evidence given inline examples (§7).
- A per-eval `gold-claims.json` oracle makes recall/routing gradeable in evals without disproportionate authoring burden (§4).
- Hand-written ADRs / design-doc architecture sections exist to review on day one (before M2 producers).

## Not Doing (M1)

- Producer skills (`decompose`/`decide`/`model`) — M2.
- The nested architecture flow and architecture-implement hand-off — M3.
- Profile `architecture/` phase and profile detection in `review-architecture` — M4.
- Behavioral / runtime verification — belongs to `/kk:review-code` / `/kk:review-spec`.
- Security architecture — delegated to PAL `secaudit`.
- Writing broader architecture docs — M1 only reads.
- Multi-artifact invocations and cross-artifact consistency (contradicting/superseded ADRs) — single artifact per invocation (§2a); revisit at M2 when producers create artifact families.

## Rejected Alternatives

- **Accept-everything input** (verbal/diagram-only) — ungradeable; forces the reviewer to do extraction *and* evaluation (altitude blur).
- **Role-axis execution units** — under-scoped, no eval surface.
- **Five merged dimensions** (blast-radius + idempotency in one) — muddy eval signal (§5).
- **Hidden extraction step** — collapses two failure modes into one (§2b).
- **Call-graph evidence for boundaries** — LLM-intractable; use static dependency manifests (§5, dimension 1).
- **Absence-of-evidence as an implicit mode signal** — treating a missing mechanism as greenfield excuses every violation; treating it as a violation flags every proposal. Replaced by the explicit anchor rule (§5).
- **Pass 2 as a peer topology dimension** — breaks the Pass-1 map-reduce contract (§6).
