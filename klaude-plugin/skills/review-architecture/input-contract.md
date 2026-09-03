# Input Contract — Acceptance

This file governs **acceptance**: what is allowed through the door. Normalization (heterogeneous prose → a uniform claim-set) is a separate, orthogonal question handled by Pass 0 (`pass0-extraction.md`). Acceptance is applied first, on the invocation path(s) alone, before any artifact content is read — with one bounded exception, the composite-kit cross-link fallback (§The composite-kit amendment), which may open the invoked page to locate its counterpart: shape, not claims.

## Accepted artifacts

`review-architecture` accepts **exactly one committed written artifact per invocation** that makes falsifiable structural or decision claims:

- an **ADR** (`docs/adr/NNNN-slug.md`), or
- a **broader architecture doc**, or
- the **architecture section of a design doc** (e.g., `docs/wip/<feature>/design.md`, optionally scoped by a heading argument), or
- a **domain-reference kit** — the glossary page (`<context>.md`) and its divergences/traps page (`<context>-traps.md`), reviewed together as **one composite artifact** (see §The composite-kit amendment).

"Committed written artifact" means the claims are already captured as prose in a file. The reviewer reads whatever architecture docs exist; in M1 it never writes one.

## The single-artifact rule

**Exactly one artifact per invocation.** A second path argument is rejected.

This is deliberate, not a limitation to paper over: Pass 1 verifies claims independently and Pass 2 grades an artifact against its *own* stated context. Nothing in the engine detects contradictions *between* artifacts (e.g., a superseded ADR contradicting its successor). Accepting an artifact set would silently imply cross-artifact consistency checking the engine does not perform. Multi-artifact review is deferred.

**Rejection message (multi-artifact):**

> `review-architecture` reviews one artifact per invocation. It verifies each artifact against its own stated context and does not check consistency *between* artifacts. Run it once per artifact:
> `/kk:review-architecture <path-1>` then `/kk:review-architecture <path-2>`.
> For a domain-reference kit, pass just one page's path — the glossary/traps counterpart is auto-discovered and reviewed with it.

## The composite-kit amendment

A domain-reference kit's glossary and traps pages are authored as one unit with hard cross-references — the glossary's rules table cites `P#`/`D#` entries that live in the traps page. Reviewing one page alone would sever claims from their cited divergences, so the pair is accepted as **one composite artifact**. This is a deliberate, bounded amendment to the single-artifact rule, not a general artifact-set feature: nothing else may be paired, and the engine still performs no cross-artifact consistency checking beyond the kit's own internal cross-references.

**Invocation mechanics:**

- The user passes **either page's path** — one path, the same CLI shape as every other artifact.
- The counterpart is resolved by the **sibling naming convention**: `<context>.md` ↔ `<context>-traps.md` in the same directory.
- **Cross-link fallback.** When no sibling matches the naming convention (brownfield kits that predate it), open the invoked page only far enough to follow its explicit cross-link to the companion page — locate the link by pattern match (e.g. Grep the page for a sibling `.md` markdown link), not by reading the page's prose. This is the one bounded exception to path-only acceptance — a shape-level lookup that locates the counterpart, not a reading of claims.
- **Two explicit paths are still rejected** — even when they are the two pages of one kit. Pass one page; the counterpart is auto-discovered (rejection message above).
- **Single-page kit.** When no counterpart resolves by either mechanism, accept the invoked page **solo**, and state loudly in the report that cross-page references are unresolvable. A rules-table enforcement pointer citing an entry in the missing counterpart is graded `ill-formed` — its required supporting element is absent — never silently skipped.

## The diagram-with-prose rule

Diagrams count **only** when accompanied by prose asserting what they mean. A diagram alone is not a set of falsifiable claims — the reviewer cannot verify "X is isolated from Y" from boxes and arrows without prose stating the isolation and its intent.

## Verbal / diagram-only rejection

**Verbal or diagram-only proposals are out of scope** until captured as a written artifact. Capturing a verbal or diagram-only proposal as an artifact is a future *producer* skill's job, not the reviewer's. This mirrors every existing reviewer in the family (`/kk:review-code` → diff, `/kk:review-spec` → design + implementation): each demands claims already committed to text.

**Rejection message (verbal / diagram-only):**

> `review-architecture` reviews a *written* artifact that makes falsifiable claims — an ADR, an architecture doc, or the architecture section of a design doc. A verbal description or a diagram without accompanying prose has nothing to verify against. Capture the proposal as a written artifact first (e.g., an ADR under `docs/adr/`), then re-run: `/kk:review-architecture <path>`.

## No path given

If no path is provided, do **not** guess. List candidate artifacts (`docs/adr/*.md`, `docs/wip/*/design.md`) and ask which one to review.

## Acceptance decision (summary)

| Input | Decision |
| --- | --- |
| One committed ADR / architecture doc / design-doc architecture section | **Accept** → Pass 0 |
| One diagram **with** asserting prose | **Accept** → Pass 0 |
| One kit page with a resolvable counterpart (sibling naming or cross-link) | **Accept the pair** as one composite artifact → Pass 0 |
| One kit page, counterpart unresolvable | **Accept solo** — report notes cross-page references are unresolvable; pointers into the missing page grade `ill-formed` |
| Two or more artifact paths (kit pages included) | **Reject** — single-artifact rule; guide to run per artifact / pass one kit page |
| Verbal description, or diagram-only (no prose) | **Reject** — capture as an artifact first |
| No path | **Ask** — list candidates |
