# Architect-supporting skills — high-level design

**Status:** Design. Vision + milestone roadmap. Milestone 1 (`review-architecture`) is **done** — designed under [review/design.md](review/design.md), built and verified per [review/tasks.md](review/tasks.md). Milestone 2 (`/kk:model`) is designed in detail under [model/design.md](model/design.md).

**Supersedes discussion in:** [handoff.md](handoff.md) (kept as the discovery record).

**Field input:** field learnings from the first real architect workstream (2026-08-31) — a field-tested output contract for the `model` producer, real-world M1 eval-fixture candidates, and additions to the §6 artifact-homes question — were **consulted during the M2 design session (2026-09-01)** and absorbed, generified, into [model/design.md](model/design.md) §1 (self-contained; the source files stay external/private). Epistemic status: n=1 — the verdicts are encoded as falsifiable defaults citing their motivating failures, not doctrine. First falsification already recorded: the proposed session-close state-rewrite guard was judged a false-positive finding and dropped (see §7).

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

**M2 — `model` producer (designed in detail under [model/](model/design.md); restaged 2026-09-01).** Originally "all three producers"; restaged after the field learnings to a model-first vertical slice: `/kk:model` (the field-tested steady-state kit: glossary + traps pages, not the originally sketched "canonical data model, data flow/lineage"), four shared producer guards in `skills/_shared/`, and additive M1 extensions (`provenance` claim field, composite kit acceptance, Domain Binding dimension) that close the produce→review freshness loop. Rationale: highest-evidence slice; the other producers were staged out rather than built on zero field evidence.

**M2.1 — `decide`.** ADR generation → `docs/adr/`, trade-off/build-vs-buy analysis, **plus the ratification-record design**: nothing today records who flipped a term/rule `proposed → canonical`, when, or why. Candidate homes to evaluate then: glossary-entry metadata (`ratified-by`/`date`) vs. ADRs stretched to cover domain semantics. Reuses the four M2 shared guards unchanged.

**M2.2+ — `decompose`.** Deferred pending **redefinition**: standing C4/deployment-topology artifacts contradict the field verdict that big standing diagrams rot (the field's maintained four-layer stack was dissolved same-day). If built, `decompose` should be an on-demand, per-decision-slice diagram/decomposition producer feeding design docs, not a durable-artifact factory. Seed heuristic from the field: "unify the decision, separate the parameters."

**M3 — the nested flow.** `review-architecture` (M1) + producers (M2.x) + the architecture-implement hand-off that seeds feature-`design`. Formalizes the §4 nesting. Reference prototype: the field workstream's glossary-to-design seam (Map → Delta → Surface → Promote), including its recorded failure mode — running to completion on fabricated input proves a method *executable*, not *grounded*.

**M4 (optional) — architecture as a profile phase.** Profiles contribute an `architecture/` phase and `review-architecture` does profile detection. Decide *after* M1 ships (see [review/design.md](review/design.md) §8 Profiles).

## 6. Artifact homes

- **ADRs:** `docs/adr/NNNN-slug.md` (existing convention, Nygard template). Confirmed.
- **Broader architecture docs / domain-reference kits:** **resolved for `model` (2026-09-01)** — the skill is **home-agnostic** with resolution precedence: (1) brownfield: wherever the existing kit lives; (2) a user-declared home — covers cross-repo domains kept in a dedicated knowledge repo, the third option the field workstream surfaced (single-repo homes don't fit domains spanning repos); (3) otherwise propose `docs/architecture/<context>/` and confirm. The cross-repo question is thus a deployment detail: the org picks the home; the skill asks, never assumes. Whether `decide`/M3 need a firmer answer is re-evaluated at M2.1.

## 7. Standing decisions from the M2 design session (2026-09-01) — inputs to M2.1+

Recorded here so post-`model` milestones inherit them without re-deriving:

- **Freshness model (adopted toolbox-wide for architecture artifacts):** freshness = **re-verification at consumption time** — the consuming agent re-runs `/kk:review-architecture` against a page's Derived-from anchors when loading it. Maintenance social contracts (cross-repo reviewer obligations) are field-falsified (near-zero adoption without CI/PR-template backing) and demoted to optional org policy. The human kickoff habit ("re-read definitions") remains for the business clock only.
- **Register split:** field-protocol *mechanics* migrate into skill workflow steps at their enforcement points (each citing its motivating failure, ADR-0004 pattern); mentor *tone/register* stays project-local CLAUDE.md prose. The toolbox ships no mentor-mode skill.
- **Producer execution model:** producers are main-session skills (they write files and interact mid-flow); the read-only sub-agent pattern stays reviewer-only.
- **Success metric for producers:** a run ends with a decision queue of precise, decidable questions, each tagged with the **role** that can decide it (PO, developer, stakeholder, customer), and artifacts usable as per-audience discussion instruments (definitions → product conversations; bindings → technical conversations). Artifact volume is explicitly not the metric.
- **`provenance` claim-schema extension:** moved from "deferred" into M2 scope — its stated deferral condition (M1 evals green) was met at M1 completion.
- **Process-review skill (review the workstream, not the code):** stays a documented practice, not a skill; revisit if a second workstream demands it.
- **Falsified learnings item:** the session-close state-rewrite guard (from the field's "sedimentary handoff" finding) was judged a false positive by the user and dropped — the first confirmation that the n=1 verdicts are revisable defaults, not doctrine.
- **Shared guard inventory (M2):** requirements-harvesting gate, open-question verification pass, fact-flip propagation, contact-ratio stop — producer-generic, in `skills/_shared/`. Single-consumer content (kit-scope pushback, conventions-bind-author self-check, state→time→invariants archaeology) lives inside `/kk:model` until a second producer needs it. The requirements-harvesting gate is a natural future input to `/kk:design` — out of scope while the seam stays one-directional.

## Assumptions

- The nested-flow model (§4) survives contact with a real architecture review; if M1 shows architecture review does not decompose into produce/review/elaborate, revisit before M2.
- Hand-written ADRs and design-doc architecture sections exist in real projects to review — i.e., M1 has inputs before M2 producers exist.
- (Added 2026-09-01) The field-workstream verdicts generalize beyond n=1; each is encoded to be cheaply falsifiable by workstream #2 (see [model/design.md](model/design.md) §Assumptions for the load-bearing bets).

## Not Doing

- Producer skills beyond `/kk:model` (`decide` → M2.1, `decompose` → M2.2+ pending redefinition) — not this milestone.
- The architecture-implement hand-off and profile `architecture/` phase — M3/M4.
- Any change to `/kk:design` — the seam is one-directional; design stays untouched.
- A role-named mega-skill (`system-architect`) — role is a menu, not an execution unit.
- A session-close/handoff guard — falsified (see §7).

## Rejected Alternatives

- **New upstream phase spliced into the linear dev flow** — blurs two altitudes; makes `design` depend on architecture. Rejected for the nested-flow + one-directional seam (§2, §4).
- **Role-axis skills as the executable unit** — under-scoped, non-gradeable, no eval surface. Rejected; role kept as discovery surface only (§3).
- **Single `architecture` skill with modes** — same under-scoping problem; hides distinct gradeable procedures behind one entry point.
- **Building a producer first** — you would be generating artifacts with no definition of "good." Reviewer-first makes the rubric the spec (§5).
