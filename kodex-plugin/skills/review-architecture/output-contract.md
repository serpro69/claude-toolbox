# Output Contract — Invocation, Scope & Report

## Invocation & scope

```
$kk:review-architecture <artifact-path> [heading]
```

- **Exactly one artifact per invocation** (see [input-contract.md](input-contract.md)). A second path argument is rejected with guidance to run the review once per artifact.
- **Domain-reference kit.** Pass either kit page's path (`<context>.md` or `<context>-traps.md`); the counterpart is auto-discovered (sibling naming convention, cross-link fallback) and the pair is reviewed as **one composite artifact**. Two explicit paths are still rejected. An unresolvable counterpart → the page is reviewed solo with a loud report note.
- **Design-doc scoping.** For a design doc, an optional heading argument scopes the review to that architecture section — extract and verify only claims under the named heading.
- **No path given** → list candidate artifacts (`docs/adr/*.md`, `docs/wip/*/design.md`) and ask; do not guess.

## Verdict vocabulary

Each Pass 1 claim resolves to exactly one verdict:

| Verdict | Meaning |
| --- | --- |
| `verified` | Reality mode: the claimed mechanism exists in the expected evidence with the expected topology. |
| `violated` | Reality mode: the anchor (the component/boundary the claim names) exists, but the claimed mechanism is absent or contradicted inside it. The case the reviewer exists to catch. |
| `internally-sound` | Internal-soundness mode: a `future`/proposed claim (or a fallback claim with no reality branch) is well-formed — names its boundaries, owners, degradation, etc. |
| `ill-formed` | Internal-soundness mode: the claim is missing required structural elements (e.g., a proposed boundary with no permitted-dependency direction stated). Also graded — regardless of mode — for a kit enforcement pointer citing an entry in a missing or unresolvable counterpart page (see the dimension-7 cross-page-pointer rule). |
| `dangling-anchor` | Reality mode: a `present`-tense claim names a component/boundary that does not exist in the repo. Doc drift or a false claim — always a finding. |

Pass 2 produces separate findings (appropriateness / reversibility), not per-claim topology verdicts.

## Report structure

The report is presented inline, mirroring the review-skill family. The `architecture-reviewer` agent is read-only (no Write tool), so the report section — not a file — is the home of the inspectable claim-set.

1. **Claim Set** — the full Pass 0 output, **verbatim**. This *is* the inspectable intermediate artifact (each claim's `id`/`claim`/`source_span`/`dimension`/`tense`/`provenance`/`evidence_class`). Presenting it verbatim keeps "reviewer missed a claim" distinguishable from "extractor never found the claim." The section header carries the extraction-completeness disclaimer (see Output rules) — recall has no production oracle, so the set is never certified complete.
2. **Verdicts by dimension** — one verdict per claim (vocabulary above), grouped by the seven Pass 1 dimensions.
3. **Not Reviewed** — `delegated` claims (with a `secaudit` pointer: security architecture → `mcp__pal__secaudit`) and `unrouted` claims, listed explicitly. Fail-loud: extraction happened, Pass 1 verification did not, and the report says so. (Pass 2's provenance-consistency check is routing-independent, so a settled-presented `unrouted` claim can appear both here and under the Provenance subsection.) These claims are never silently dropped.
4. **Pass 2 findings** — appropriateness (mechanism vs the artifact's own stated context), reversibility (one-way vs two-way doors; proportional justification for irreversible decisions), and provenance (self-certification: claims presented as settled whose provenance is `reverse-engineered`/`fabricated-labeled` with no cited ratification record).

## Severity mapping

Reuses the review family's P0–P3 scale:

| Verdict / finding | Severity |
| --- | --- |
| `violated` | **P1** — escalates to **P0** when Pass 2 marks the underlying decision a one-way (irreversible) door |
| `dangling-anchor` | **P2** |
| `ill-formed` (internal-soundness claim missing required elements) | **P2** |
| Pass 2 inappropriate-mechanism / missing reversibility justification | **P1** / **P2** |
| Pass 2 self-certification (`canonical` by decree: settled presentation, `reverse-engineered`/`fabricated-labeled` provenance, no cited ratification record) | **P2** |
| `unrouted` / `delegated` | **informational** |

## Report skeleton

```markdown
## Architecture Review — {artifact path}

**Artifact type**: {ADR | architecture doc | design-doc architecture section | domain-reference kit (composite | solo page)}
**Scope**: {full artifact | heading: <name> | kit pages: <glossary> + <traps>}
**Overall assessment**: [SOUND / VIOLATIONS_FOUND / DRIFT_FOUND]

---

### Claim Set (Pass 0 — verbatim)

> Extraction is graded on precision (every claim is span-grounded) but recall has
> no production oracle — this claim-set is not certified complete; a claim the
> extractor missed is silently absent.

| id | claim | source_span | dimension | tense | provenance | evidence_class |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | … | … | … | … | … | … |

---

### Verdicts by dimension (Pass 1)

#### 1. Structural Boundaries
- **C1** — `verified` / `violated` / `internally-sound` / `ill-formed` / `dangling-anchor`
  - Mode: {reality | internal-soundness}
  - Evidence: {resolved path(s) inspected, or "n/a — internal-soundness"}
  - Finding: {what was confirmed or what was missing}

#### 2. Data Ownership
#### 3. NFR Mechanisms
#### 4. Failure Isolation
#### 5. State Consistency
#### 6. Evolution & Versioning
#### 7. Domain Binding

---

### Not Reviewed

- **Delegated (security → `mcp__pal__secaudit`)**: {claim ids + one-line each}
- **Unrouted**: {claim ids + one-line each}

---

### Pass 2 — Decision Soundness & Reversibility

- **Appropriateness**: {mechanism-vs-stated-context findings, or "no mismatch found"}
- **Reversibility**: {one-way/two-way door findings + proportional-justification, or "n/a"}
- **Provenance**: {self-certification findings — settled presentation + `reverse-engineered`/`fabricated-labeled` provenance + no cited ratification record (P2), each quoting the presentation and the derivation signal — or "no provenance inconsistency found"}
```

### Output rules

- Present the Claim Set verbatim — do not summarize or omit claims.
- State the extraction-completeness disclaimer with the Claim Set (fail-loud, per the Pass 0 procedure): the reviewer does not certify that every claim in the artifact was extracted.
- Every verdict states its mode (reality vs internal-soundness) and, for reality mode, the resolved evidence path inspected.
- `delegated` and `unrouted` claims always appear under Not Reviewed — never dropped.
- Use `(none)` under any empty section.
