# Input Contract — Acceptance

This file governs **acceptance**: what is allowed through the door. Normalization (heterogeneous prose → a uniform claim-set) is a separate, orthogonal question handled by Pass 0 (`pass0-extraction.md`). Acceptance is applied first, on the invocation path(s) alone, before any artifact content is read.

## Accepted artifacts

`review-architecture` accepts **exactly one committed written artifact per invocation** that makes falsifiable structural or decision claims:

- an **ADR** (`docs/adr/NNNN-slug.md`), or
- a **broader architecture doc**, or
- the **architecture section of a design doc** (e.g., `docs/wip/<feature>/design.md`, optionally scoped by a heading argument).

"Committed written artifact" means the claims are already captured as prose in a file. The reviewer reads whatever architecture docs exist; in M1 it never writes one.

## The single-artifact rule

**Exactly one artifact per invocation.** A second path argument is rejected.

This is deliberate, not a limitation to paper over: Pass 1 verifies claims independently and Pass 2 grades an artifact against its *own* stated context. Nothing in the engine detects contradictions *between* artifacts (e.g., a superseded ADR contradicting its successor). Accepting an artifact set would silently imply cross-artifact consistency checking the engine does not perform. Multi-artifact review is deferred.

**Rejection message (multi-artifact):**

> `review-architecture` reviews one artifact per invocation. It verifies each artifact against its own stated context and does not check consistency *between* artifacts. Run it once per artifact:
> `/kk:review-architecture <path-1>` then `/kk:review-architecture <path-2>`.

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
| Two or more artifact paths | **Reject** — single-artifact rule; guide to run per artifact |
| Verbal description, or diagram-only (no prose) | **Reject** — capture as an artifact first |
| No path | **Ask** — list candidates |
