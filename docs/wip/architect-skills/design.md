# Architect-supporting skills — high-level design

**Status:** Design. Vision + milestone roadmap. Milestone 1 (`review-architecture`) is designed in detail under [review/design.md](review/design.md).

**Supersedes discussion in:** [handoff.md](handoff.md) (kept as the discovery record).

---

## 1. The gap

The toolbox has a complete end-to-end dev-work lifecycle — `/kk:design` → `/kk:review-design` → `/kk:implement` → `/kk:review-code` → `/kk:test` → `/kk:document` — but **nothing supports architect roles** (system / solution / information architecture). Architecture appears only as a *facet*: `/kk:review-code` flags SOLID/architecture smells at code-diff altitude; profiles carry a one-paragraph "architecture" summary; ADRs are a doc convention (`docs/adr/NNNN-slug.md`) with **no generating or reviewing skill**.

The real gap is **altitude**. `/kk:design` assumes a feature slots into an existing system. System/solution/IA work is *upstream and cross-cutting* — it precedes features and spans many of them. Splicing it into `design` would blur two altitudes.

## 2. Positioning — higher altitude, one-directional artifact hand-off

Architecture sits **above** `/kk:design` but imposes **zero hard dependency** on it. This is the pattern the toolbox already uses for profiles: `/kk:design` *conditionally* consumes profile `design/` content (present → consume, absent → proceed). Applied here:

- Architecture skills **emit artifacts to known homes** (`docs/adr/`, broader architecture docs — home TBD, see §6).
- Feature-`/kk:design` **opportunistically reads them if present, degrades gracefully if not.**

The seam is a **one-directional artifact hand-off, not a call graph.** Architecture *feeds* design; design never *calls* architecture and still works standalone exactly as today.

## 3. Slicing — role for discovery, artifact for execution

Two axes were considered (see §Rejected Alternatives). Resolution: **role = discovery/routing surface; artifact = executable unit.**

- **Artifact-axis wins for AI output quality.** "Do system architecture" is an under-scoped space the model wanders in and you cannot write evals for. "Produce an ADR for this decision," "review this architecture doc," "decompose into C4 containers" have crisp inputs/outputs and are gradeable — which the toolbox's eval convention requires.
- **Role is not wasted** — it becomes the menu layer. A human thinking "I'm doing solution architecture today" dispatches to the relevant artifact procedures. No sprawling `system-architect` mega-skill.

## 4. Architecture owns its own flow (fractal of the dev flow)

Architecture is the dev flow one altitude up, with the two flows **nested** and joined at exactly one seam:

- architecture **design** → *produce* it (decompose / decide / model)
- architecture **review** → `review-architecture` skill + `architecture-reviewer` agent
- architecture **implement** → *elaborate / hand-off*: turn architecture into buildable specs + ADR-constraints that **seed** feature `/kk:design`

Architecture-implement's output = feature-design's *optional* input. This reuses every existing convention (family prefixes, read-only reviewer agents, profiles, evals, `docs/wip` staging) instead of splicing architecture into the linear flow.

## 5. Milestone roadmap

**M1 — `review-architecture` (this design; detailed under `review/`).** Start with the reviewer, deliberately:

- A reviewer forces you to define **what "good architecture" looks like** — the rubric. That rubric is the hardest, most reusable asset, and it becomes **the spec the future producer skills target.** Build the evaluation criteria before the producer.
- Reuses the proven read-only reviewer-agent pattern.
- Delivers day-one value: people hand-write ADRs today; reviewing those is real value before any producer exists.

**M2 — artifact producers.** `decompose` (C4 context/containers, deployment topology), `decide` (ADR generation → `docs/adr/`, trade-off/build-vs-buy analysis), `model` (canonical data model, data flow/lineage). Each targets the rubric spine from M1.

**M3 — the nested flow.** `review-architecture` (M1) + producers (M2) + the architecture-implement hand-off that seeds feature-`design`. Formalizes the §4 nesting.

**M4 (optional) — architecture as a profile phase.** Profiles contribute an `architecture/` phase and `review-architecture` does profile detection. Decide *after* M1 ships (see [review/design.md](review/design.md) §8 Profiles).

## 6. Artifact homes

- **ADRs:** `docs/adr/NNNN-slug.md` (existing convention, Nygard template). Confirmed.
- **Broader architecture docs:** **OPEN** — `docs/architecture/` (durable, system-of-record) vs `docs/wip/<x>/architecture.md` (per-effort). This choice defines the hand-off seam to feature-`design`. Deferred to M2/M3 when a producer first needs to *write* one; M1 only *reads* whatever exists, so it is not blocking.

## Assumptions

- The nested-flow model (§4) survives contact with a real architecture review; if M1 shows architecture review does not decompose into produce/review/elaborate, revisit before M2.
- Hand-written ADRs and design-doc architecture sections exist in real projects to review — i.e., M1 has inputs before M2 producers exist.

## Not Doing

- Producer skills (`decompose`/`decide`/`model`) — M2, not this design.
- The architecture-implement hand-off and profile `architecture/` phase — M3/M4.
- Any change to `/kk:design` — the seam is one-directional; design stays untouched.
- A role-named mega-skill (`system-architect`) — role is a menu, not an execution unit.

## Rejected Alternatives

- **New upstream phase spliced into the linear dev flow** — blurs two altitudes; makes `design` depend on architecture. Rejected for the nested-flow + one-directional seam (§2, §4).
- **Role-axis skills as the executable unit** — under-scoped, non-gradeable, no eval surface. Rejected; role kept as discovery surface only (§3).
- **Single `architecture` skill with modes** — same under-scoping problem; hides distinct gradeable procedures behind one entry point.
- **Building a producer first** — you would be generating artifacts with no definition of "good." Reviewer-first makes the rubric the spec (§5).
