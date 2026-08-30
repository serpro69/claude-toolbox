# Handoff — Architect-supporting skills for claude-toolbox

**Status:** Discovery / discussion. No skills written yet. This document lets another session pick up exactly where we left off.

**Date:** 2026-08-28

---

## The ask

The toolbox has a complete end-to-end **agentic dev-work lifecycle** (design → review → implement → test → document), but **nothing supports Architect roles** — system architecture, solution architecture, information architecture. Goal: figure out how to **seamlessly integrate new skills** that support a person doing one or more of those roles.

This is **primarily discussion/discovery** — the user explicitly does **not** want skills written yet. The output of this phase is a shared understanding + a set of decisions, not code.

---

## Background: what the toolbox is and how it's shaped

Read `CLAUDE.md` (root) in full before acting — it is dense and authoritative. Key facts relevant here:

- **Three components:** Claude Code config (`.claude/`), Codex (`.codex/` + `kodex-plugin/`, generated), and the **`klaude-plugin/`** which is the **canonical source of truth** for skills/commands/hooks/agents/profiles.
- **The dev lifecycle skills** (in `klaude-plugin/skills/`): `design`, `review-design`, `implement`, `review-code`, `review-spec`, `test`, `document`, plus utilities (`chain-of-verification`, `dependency-handling`, `diff-skill`, `merge-docs`).
- **Profiles** (`klaude-plugin/profiles/`): `go`, `java`, `js_ts`, `kotlin`, `python`, `k8s`, `k8s-operator`, `skill-md`. A profile injects **per-phase domain content** into the lifecycle. Each profile has `DETECTION.md` (activation rules: path/filename/content/optional design signals) and phase subdirs (`design/`, `review-code/`, `implement/`, `test/`, `document/`, `review-spec/`) each governed by an `index.md` contract (always-load + conditional "Load if:" entries; bidirectional invariant enforced by tests).
- **Reviewer agents** (`klaude-plugin/agents/`): `code-reviewer`, `design-reviewer`, `spec-reviewer`, `eval-grader`, `profile-resolver`. Read-only tool sets. The review skills delegate to these.
- **ADRs already have a home:** `docs/adr/NNNN-slug.md` (Nygard template: Context/Decision/Consequences). **No skill currently produces ADRs.**
- **Per-feature design docs:** `docs/wip/<feature>/{design,implementation,tasks}.md` while active; move to `docs/done/<feature>/` when complete.
- **Conventions that matter for new skills:** imperative-verb names, `/kk:` prefix everywhere, **family prefixes** for grouped skills (`review-design`/`review-spec`/`review-code`), agents named by **role** not by invoking skill, skill description budget (~1024 soft / 1536 hard chars, lead with trigger keywords), **skills load ALL instructions before acting on subject matter** (ADR 0004), and **evals** for skills with non-trivial routing/detection logic (`skills/<skill>/evals/<name>/eval.json` + `test-files/`).
- **`${CLAUDE_PLUGIN_ROOT}` / `${TOOLBOX_PLUGIN_ROOT}` substitution rules** are subtle — see CLAUDE.md "Referencing profile content." Relevant when skills reference profile content at runtime.

### How architecture is handled TODAY (the gap)

Architecture only appears as a **facet**, never as a first-class concern:
- `review-code` flags SOLID violations / "architecture smells" at the code-diff altitude.
- Each profile has an "Architecture in one paragraph" summary (e.g., k8s describes declarative desired-state).
- ADRs are a **doc convention** with no generating skill.

The real gap isn't "missing architect skills" — it's that **architecture lives at a different altitude** than feature work. `/kk:design` assumes a feature slots into an existing system. System/solution/IA work is **upstream and cross-cutting**: it precedes features and spans many of them. Splicing it into `design` would blur two altitudes.

---

## The discussion so far — decisions and reasoning

Four substantive threads were worked through. Each records the reasoning, the user's position, and the current state.

### 1. Position in the flow — "above, but not a dependency"

**Question:** How do architecture skills relate to the existing design→implement flow? (New upstream phase / augment `/kk:design` / standalone toolkit)

**User's position:** Undecided. Sees pros/cons of sitting above `/kk:design`. Wants integration, **but design must NOT depend on architect-produced artifacts.**

**Reasoning / current answer:** "Above" and "not a dependency" are **not in tension**. The toolbox already has the pattern that resolves it: `/kk:design` **conditionally** loads profile `design/` content (present → consume, absent → proceed). Apply the same to architecture — architecture skills **emit artifacts to known homes** (`docs/adr/`, a `docs/architecture/` or `docs/wip/<x>/architecture.md`); feature-`design` **opportunistically reads them if present and degrades gracefully if not.** So architecture sits at a higher altitude and *feeds* design, but design keeps **zero hard dependency** and still works standalone exactly as today. The seam is a **one-directional artifact hand-off, not a call graph.**

**State:** Converging on "higher altitude + optional one-directional artifact hand-off." Not finalized.

### 2. Slicing axis — "role for discovery, artifact for execution"

**Question:** How to slice the skills? (By artifact/action / by role / single skill with modes)

**User's position:** Likes **both** artifact-based and role-based; unsure which yields better AI results.

**Reasoning / current answer:** For **AI output quality**, **artifact-axis wins decisively.** "Do system architecture" is an enormous under-scoped space — the model wanders and you can't write evals for it. "Produce an ADR for this decision," "decompose this into C4 containers," "define this canonical data model" have **crisp inputs, crisp outputs, and are gradeable** (the toolbox's eval convention needs that). Narrow artifact-shaped procedures are where LLM skills perform.

Role isn't wasted — it becomes the **routing/menu layer**: a human thinks "I'm doing solution architecture today," and that framing dispatches to the relevant artifact procedures. **Resolution: role as the entry surface, artifact as the executable unit** — you get both without a sprawling "system-architect" mega-skill.

Candidate artifact-shaped units surfaced so far:
- **decompose** — component/service boundaries, C4 context+container, deployment topology
- **decide** — ADR generation (Nygard → `docs/adr/`), trade-off/option analysis, build-vs-buy
- **model** — information/data architecture: canonical schemas, data flow/lineage, taxonomies
- **NFRs/constraints** — scalability, availability, security posture, cost as first-class requirements that design consumes

Each maps to all three architect roles — which is *why* the role axis is a bad unit of execution but a fine unit of discovery.

**State:** Converging on "artifact = executable unit, role = discovery/routing surface." Not finalized.

### 3. Architecture owns its own flow (the strongest insight)

**User's insight:** Don't force a 1-to-1 fit into the dev-flow skills. Maybe **design, review, implement fit *within* an architecture flow** of their own.

**Reasoning / current answer:** Strongly agree — architecture is a **fractal of the dev flow, one altitude up**:
- architecture **design** → *produce* it (decompose / decide / model)
- architecture **review** → `review-architecture` skill + `architecture-reviewer` agent
- architecture **implement** → *elaborate / hand-off*: turn the architecture into buildable specs and ADR-constraints that **seed** feature `/kk:design`

The two flows **nest**, joined at exactly **one seam**: architecture-implement's output = feature-design's *optional* input (ties back to thread 1). This is cleaner than splicing architecture into the existing linear flow and reuses every existing convention (family prefixes, reviewer agents, profiles, evals, `docs/wip` staging).

**State:** Adopted as the leading structural model.

### 4. First step — start with the reviewer

**Question:** Where should the first skill land? (ADR + trade-off / review-architecture + agent / full family upfront)

**User's position:** **Reviewer architect is a good start.** Also: don't necessarily need a 1-to-1 fit with dev-flow skills (led to thread 3).

**Reasoning / current answer:** Starting with the reviewer is **strategically** right, not just pragmatically:
- A reviewer forces you to define **what "good architecture" looks like** — the **rubric**. That rubric is the hardest, most reusable asset, and it later becomes **the spec the generator skills target.** Build the evaluation criteria before the producer.
- Reuses the proven read-only reviewer-agent pattern (`architecture-reviewer` agent mirroring `code-reviewer`/`design-reviewer`/`spec-reviewer`).

**Caveat raised (must resolve before building):** a reviewer needs a defined **input contract.** Architecture artifacts today are **heterogeneous** — an ADR, a design doc's prose, a diagram, a verbal proposal. Nail down **what `review-architecture` accepts** before building it, or it won't be gradeable.

**State:** Agreed to start with `review-architecture` + `architecture-reviewer`. Blocked on defining the input contract + rubric.

---

## Open threads (pick up here)

1. **`review-architecture` input contract** — what heterogeneous inputs does it accept, and how are they normalized so the review is gradeable? (Immediate next topic; the last message ended by offering to dig into this.)
2. **The architecture rubric** — what dimensions define "good architecture"? (Coupling/cohesion, boundary clarity, NFR coverage, trade-off explicitness, reversibility of decisions, data-ownership clarity, failure modes, etc.) This rubric is the reusable core asset.
3. **Architecture as a profile phase?** — should profiles contribute an `architecture/` phase (k8s → deployment topology; a language profile → framework constraints), and should `review-architecture` do **profile detection** like `review-code` does? Decide *after* the input contract is set.
4. **Naming** — likely a family: `/kk:review-architecture` (mirrors review triad) and, later, artifact producers under an architecture family. Confirm against the naming-convention section in CLAUDE.md (imperative verbs, family prefixes, `/kk:` everywhere).
5. **Where artifacts live** — confirm homes: ADRs → `docs/adr/`; broader architecture docs → `docs/architecture/` vs `docs/wip/<x>/architecture.md`. This choice defines the hand-off seam to feature-`design`.
6. **Codex parity** — anything added to `klaude-plugin/` must regenerate via `make generate-kodex`; new profiles/skills touch `test/test-plugin-structure.sh` (`EXPECTED_SKILLS`, `EXPECTED_PROFILES`, etc.). Keep in mind but not blocking during discovery.

---

## How to resume

The user wants **discussion, not implementation.** Continue the Socratic/opinionated mode (see `.claude/CLAUDE.extra.md` — be direct, push back with reasoning, surface blind spots). The natural next move is **thread 1 above: define `review-architecture`'s input contract and start sketching the rubric (thread 2)**. Do not write skills until the user explicitly asks.
