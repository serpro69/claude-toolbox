# Pass 0 — Claim Extraction

Turns the accepted artifact into an explicit, inspectable **claim-set**: the normalized intermediate the rest of the engine consumes. This pass is the reason the whole skill is gradeable — extraction is surfaced as its own artifact and graded on its own, so "the reviewer missed a claim" stays distinguishable from "the extractor never found the claim."

## The repo-blind rule (load-bearing)

**Pass 0 reads only the artifact. Never the codebase.** Every field below is derivable from the artifact text alone.

Why this matters: the moment extraction consults the repo, precision grading stops being span-grounded — a "claim" could be sourced from code the artifact never asserts, and the grader can no longer confirm the claim against a quote in the artifact. Repo-blindness keeps extraction pure normalization. Resolving an evidence class to a concrete file path is **Pass 1's** job; here you name only the *abstract* class.

## Claim schema

One entry per extracted claim. Every field comes from the artifact text.

| Field | Content |
| --- | --- |
| `id` | Stable per-review identifier — `C1`, `C2`, … Assign in reading order; never reuse or renumber mid-review. |
| `claim` | The assertion, tightly paraphrased. One verifiable proposition per entry — split conjunctions ("A is isolated *and* owns E") into separate claims so each routes and verifies independently. |
| `source_span` | The artifact quote grounding the claim, or `heading + line` locating it. This is what precision grading checks against — it must actually assert the claim. |
| `dimension` | Exactly one of the tokens `1`, `2`, `3`, `4`, `5`, `6` (the six Pass 1 dimensions below), `pass2`, `delegated`, or `unrouted`. Emit the numeric id for a topology dimension, never its name — downstream grading matches the token. See §Routing. |
| `tense` | `present` (describes the system as it is) or `future` (proposed/intended). Drives the Pass 1 anchor-rule mode decision. See §Tense. |
| `provenance` | Where the claim's content came from, per the artifact's own text: `harvested` / `reverse-engineered` / `fabricated-labeled`. Orthogonal to `tense`. Pass 0 only records it; the consistency check runs in Pass 2. See §Provenance. |
| `evidence_class` | The **abstract class** of evidence the claim implicates — e.g. "dependency manifests of service A", "mutating route bindings for entity E". Never a resolved repo path. |

### Dimension routing

Route each claim to exactly one target. The six Pass 1 dimensions:

| # | Dimension | Route here when the claim is about… |
| --- | --- | --- |
| 1 | **Structural Boundaries** | isolation / permitted dependency direction between components ("X must not depend on Y"). |
| 2 | **Data Ownership** | which component is the sole mutating owner of an entity; read-vs-write paths. |
| 3 | **NFR Mechanisms** | a structural mechanism (cache, CDN, shard, replica) introduced to meet a non-functional requirement. |
| 4 | **Failure Isolation** | surviving a dependency failure — timeouts, retries, bulkheads, circuit breakers, degradation. |
| 5 | **State Consistency** | duplicate/race safety — idempotency keys, dedup, unique constraints, delivery semantics, sagas. |
| 6 | **Evolution & Versioning** | independent deployability — API version routing, migration tooling, expand/contract. |

Non-dimension targets (never dropped — they surface in the report's Not Reviewed section):

- `pass2` — a decision, trade-off, or reversibility claim (why a mechanism was chosen; one-way vs two-way door). Graded by Pass 2, not verified for topology.
- `delegated` — security architecture (trust boundaries, authN/authZ enforcement, data-classification flow). Delegated OUT to PAL `secaudit` (`mcp__pal__secaudit`); do not attempt to verify.
- `unrouted` — a genuine assertion that fits none of the above. Keep it; do not force-fit it into a dimension. A misrouted claim is worse than an honest `unrouted`.

**4 and 5 are distinct on purpose.** Failure isolation (availability) and state consistency are opposing physics (CAP). A claim about circuit breakers routes to 4; a claim about idempotency routes to 5 — never blend them, or the downstream verdict loses signal.

### Tense

`tense` records whether the claim describes reality or intent, because Pass 1 grades the two modes differently (a proposal is never failed for being absent from the repo).

- `future` — proposed/intended. Signals: ADR status **Proposed**; prospective wording like "will", "we propose", "the target design".
- `present` — describes the system as built. Signals: ADR status **Accepted**; wording like "is", "uses", "owns", present-tense assertions of fact.

Derive from artifact metadata first (ADR status), then claim wording. When metadata and wording conflict (an Accepted ADR whose clause says "we *will* introduce"), the clause wording wins for that claim — status sets the default, individual claims can override it.

**Deontic wording is `present`, not `future` — in an artifact that asserts the system as built.** "must", "must not", "shall" assert an *invariant* the artifact places on the system, not an intention to build something later — in an Accepted ADR, treat a deontic clause (e.g. "billing *must not* depend on the order schema") as `present`. Only genuinely prospective wording ("will", "we propose", "the target design") overrides an Accepted default to `future`. This matters because most boundary and isolation claims are phrased deontically; misreading them as `future` would send real, checkable invariants into internal-soundness mode and silently excuse violations.

**But the deontic⇒`present` shortcut presupposes a present-default artifact.** In a **Proposed** ADR — or any artifact whose tense default is `future` — a deontic clause states the *intended* invariant of the not-yet-built system; it stays `future` unless the clause asserts state that already exists. Do not let "must not" drag a proposal into reality mode against an empty or partial repo. Concretely: in a Proposed ADR, "the write side must not import the read-model package" is `future` (the read model is not built yet), not a present invariant to grade against the repo.

### Provenance

`provenance` records where the claim's *content* came from — who or what asserted it — per the artifact's own text. It is orthogonal to `tense`: tense asks whether the described mechanism/behavior exists; provenance asks where the assertion's authority comes from.

- `harvested` — from a cited stakeholder/product source (a ticket, a named decision record, a named decider), or asserted first-hand by the artifact's authors as their own decision or requirement. An ADR's Decision section is its authors' own record — the artifact itself is the source.
- `reverse-engineered` — derived from code or system inspection. Requires an explicit derivation signal in the text: a provenance banner ("the rules below are reverse-engineered"), derivation wording ("derived from reading X", "observed in the implementation", "recovered from the enforcement code").
- `fabricated-labeled` — explicitly marked invented input ("invented placeholder", "assumed pending real data", "no real input exists yet").

Derivation rules:

- **Artifact text only — the repo-blind rule applies unchanged.** Provenance derives from status markers, provenance banners, source citations, and derivation wording in the artifact. Never open the repo to decide provenance; whether code *agrees* with a claim is irrelevant to where the claim came from.
- **Default is `harvested`.** `reverse-engineered` and `fabricated-labeled` each require their explicit textual signal; a claim with neither is its authors' first-hand assertion. The default is deliberately conservative: the downstream self-certification check (Pass 2's provenance-consistency check) fires only on non-default provenance (`reverse-engineered` / `fabricated-labeled` presented as settled), so an ordinary ADR with no derivation wording never draws a provenance finding.
- **Per-claim signals override section-level banners.** A section banner ("the rules below were recovered from code") sets the default for the claims under it; a per-claim cited source (a named decision record, ticket, or decider) overrides the banner for that claim → `harvested`. Precedence: per-claim citation > per-claim derivation wording > section banner > artifact default.
- **Per-claim ratification markers do not set tense.** An artifact-level Status (ADR **Proposed** / **Accepted**) still sets the tense default per §Tense. But a per-claim ratification marker (`proposed` / `canonical` on a rule entry) speaks to the provenance axis — whether a human has ratified the *intent* — not to whether the behavior exists. A rule reverse-engineered from a currently-enforced validator is `tense: present` (the behavior is built) even while its ratification status is `proposed` (the intent is unratified). Do not let a `proposed` marker drag tense to `future`, or a `canonical` marker drag provenance to `harvested`.
- **Record only, here.** Pass 0 stays single-purpose normalization: it records provenance per claim and moves on. Checking that a claim's *presentation* (settled/`canonical`) is consistent with its provenance is Pass 2's provenance-consistency check.

## Grading — four separable sub-metrics

Pass 0 is graded on four independent axes. This separation is what makes the engine eval-able — each axis has its own failure mode and its own oracle.

1. **Precision — "did it invent a claim?"** Every extracted claim cites a `source_span`; the grader confirms that span actually asserts the claim. Self-grounding — no gold set required, works in eval **and** production.
2. **Recall — "did it miss a claim?"** Intrinsically extrinsic.
   - *In evals:* gradeable against a structured `gold-claims.json` in the eval's grader-only `oracle/` directory (a sibling of `test-files/`, so staging fixtures never leaks it); the `assertions[]` bullets reference gold entries ("claim G3 is extracted"), so each expected claim is graded PASS/FAIL individually — no free-form set arithmetic.
   - *In production:* unprovable — there is no oracle, so a missed claim is silent. This is the **one irreducible limitation.** Per fail-loud, it is documented, not hidden: **the reviewer does not certify extraction completeness.** State this in the report rather than implying the claim-set is exhaustive.
3. **Evidence-class accuracy — "right evidence class per claim?"** Gradeable against the gold set's expected classes. (Dangling *resolved-path* references are Pass 1's anchor-rule concern, not this.)
4. **Routing accuracy — "right `dimension`, `tense`, and `provenance` per claim?"** Gradeable against the gold set. A misrouted claim sends a verifiable assertion to the wrong verifier or the wrong mode — a distinct failure that, ungraded, collapses back into the precision/recall blur this pass exists to prevent. (Provenance is additive: gold sets that predate the field simply don't grade it.)

Grading is strictly easier than producing: "is this claim in the text" is a bounded lookup, recall-grading is a per-entry lookup against the gold file, routing-grading is a label comparison. No circularity.

## Production recall mitigations

Recall has no production oracle, but two techniques raise it without a gold set:

### Structural-slot heuristics per artifact type

Each artifact type has mandatory *slots* that should each yield at least one claim. After extracting, assert each slot is non-empty; an empty mandatory slot is a gross-omission signal worth a second read of that section. This catches "the extractor skipped the Consequences section entirely," which precision grading (which only checks what *was* extracted) cannot.

| Artifact type | Mandatory slots (each should yield ≥1 claim) |
| --- | --- |
| **ADR** (Nygard) | **Context** (constraints/forces → often `pass2` or `future`), **Decision** (the chosen mechanism → a dimension claim), **Consequences** (resulting boundaries/trade-offs → dimension or `pass2`). Also mine **Status** for the tense default. |
| **Broader architecture doc** | Each named **component/boundary** (→ dimension 1/2), each stated **NFR** (→ dimension 3, with its mechanism), each **cross-component data flow** (→ dimension 2/5). |
| **Design-doc architecture section** | The **component decomposition**, the **data-ownership** statement, and any **failure/consistency/versioning** subsection present. Scope strictly to the heading passed on invocation — do not extract from unrelated design sections. |

Treat the catalog as a floor, not a ceiling: an artifact can assert claims outside these slots, and those must still be extracted. The slots exist to catch omissions, not to cap the claim-set.

### Optional ensemble extraction

Run extraction N times and union the claims. This is a confidence *estimate* (more passes → fewer misses), never a completeness *proof*. Whether it is worth the token cost is measured during eval — do not enable it by default until the eval shows it recovers claims a single pass misses.

## Output

Emit the claim-set as the report's **Claim Set** section, verbatim (one row per claim, all seven fields). This *is* the inspectable intermediate artifact — the read-only agent has no Write tool, so the report section is its only home. Do not summarize, merge, or omit claims; `delegated` and `unrouted` claims stay in the set. Pass 1 and Pass 2 consume this exact set.
