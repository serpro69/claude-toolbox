# Tasks — Milestone 1 `/kk:review-architecture`

> **Design:** [design.md](design.md) · **Implementation:** [implementation.md](implementation.md) · **Umbrella:** [../design.md](../design.md)
> **Status:** pending
> **Not Doing:** producer skills (decompose/decide/model); nested flow & architecture-implement hand-off; profile `architecture/` phase + profile detection; behavioral/runtime verification; security architecture (→ PAL `secaudit`); writing broader architecture docs.

---

## Task 1 — Skill skeleton, acceptance contract, agent stub

**Status:** pending
**Size:** M
**Depends on:** —
**Can run in parallel with:** —
**Slicing:** Contract-First (defines the input boundary the rest builds on)
**Docs:** [design.md §2](design.md) · [implementation.md — Build order 1](implementation.md)

- [ ] Create `klaude-plugin/skills/review-architecture/SKILL.md` with frontmatter (`name`, trigger-keyword-first `description` ≤1024 soft/1536 hard chars) and a Workflow section carrying the ADR-0004 mandatory-order directive.
- [ ] Create `klaude-plugin/skills/review-architecture/input-contract.md` (accepted artifact types; diagram-with-prose rule; verbal/diagram-only rejection with actionable message).
- [ ] Create `klaude-plugin/agents/architecture-reviewer.md` — read-only tools (`Read`/`Grep`/`Glob`/`mcp__capy__capy_search`), role-named, restates instruction-before-action rule, `## Plugin Root` injection.
- [ ] Add `review-architecture` to `EXPECTED_SKILLS` in `test/test-plugin-structure.sh`; decide on `commands/` pair by mirroring existing review skills, updating `EXPECTED_COMMANDS` if added.
- [ ] **verify:** invoke on a verbal-only input → rejected w/ message; on a real ADR → accepted; `bash test/test-plugin-structure.sh` green.

## Task 2 — Pass 0: claim extraction + recall eval

**Status:** pending
**Size:** M
**Depends on:** 1
**Can run in parallel with:** —
**Docs:** [design.md §4](design.md) · [implementation.md — Build order 2](implementation.md)

- [ ] Create `pass0-extraction.md` — `{claim, implicated-evidence-location}` schema, three sub-metrics (precision/recall/location), structural-slot heuristics per artifact type.
- [ ] Build eval `evals/pass0-extraction-recall/` — artifact fixture + gold claim-set in `assertions[]`.
- [ ] **verify:** run the eval; extractor emits a claim-set; grader set-diffs against gold; precision/recall/location reported. Regression check: a fabricated claim is caught by precision grading.

## Task 3 — Pass 1: engine + dimensions 1–3 (Boundaries, Data Ownership, NFR)

**Status:** pending
**Size:** M
**Depends on:** 1, 2
**Can run in parallel with:** —
**Docs:** [design.md §5](design.md) · [implementation.md — Build order 3](implementation.md)

- [ ] Create `pass1-topology.md` with the reality-mode vs internal-soundness-mode decision and dimensions 1–3, each with inline evidence-gathering examples (profile-substitute).
- [ ] Build evals `evals/pass1-boundary-violation/` (manifest with a real forbidden dependency) and `evals/pass1-greenfield-fallback/` (forward-looking claims, no code).
- [ ] **verify:** boundary violation caught against a static manifest; greenfield claims fall back to internal-soundness (not flagged as failures).

## Task 4 — Pass 1: dimensions 4–6 (Failure Isolation, State Consistency, Evolution)

**Status:** pending
**Size:** M
**Depends on:** 3
**Can run in parallel with:** 5
**Docs:** [design.md §5](design.md) · [implementation.md — Build order 4](implementation.md)

- [ ] Extend `pass1-topology.md` with dimensions 4, 5, 6 (each claim/evidence/fallback + inline examples).
- [ ] Add a fixture proving 4 and 5 grade **independently** (circuit-breaker present, idempotency absent).
- [ ] **verify:** the fixture scores dim 4 pass / dim 5 fail separately — no blended verdict.

## Task 5 — Pass 2: decision soundness & reversibility

**Status:** pending
**Size:** S
**Depends on:** 2
**Can run in parallel with:** 4
**Docs:** [design.md §6](design.md) · [implementation.md — Build order 5](implementation.md)

- [ ] Create `pass2-soundness.md` — appropriateness-against-stated-context + one-way/two-way door + proportional-justification procedure; internal-soundness-only (no reality branch).
- [ ] Build eval `evals/pass2-inappropriate-mechanism/` (write-heavy + write-through cache, no stale-read mitigation).
- [ ] **verify:** the mismatch is flagged; a context-appropriate choice is not.

## Task 6 — Regression eval, Codex parity, tests, docs (final verification)

**Status:** pending
**Size:** M
**Depends on:** 1, 2, 3, 4, 5
**Can run in parallel with:** —
**Docs:** [implementation.md — Build order 6 + Conventions checklist](implementation.md)

- [ ] Build eval `evals/regression-clean-artifact/` — sound artifact matching its `test-files/`; asserts no findings.
- [ ] Run `make generate-kodex`; confirm `git diff --exit-code kodex-plugin/ .codex/agents/` is clean.
- [ ] Run `make plugin-graph` (broken-link/orphan gate) and `bash test/test-plugin-structure.sh` — both green.
- [ ] Index non-obvious rationale as `kk:arch-decisions` (skip if self-evident from docs).
- [ ] Invoke `/kk:test` (full suite), `/kk:document` (update docs), `/kk:review-code` (language: shell/markdown), and `/kk:review-spec` (verify implementation matches [design.md](design.md)/[implementation.md](implementation.md)).
- [ ] **verify:** all tests green; regression eval produces zero findings; review-spec reports no design/impl drift.

## Dependency Graph

```
1 ─┬─> 2 ─┬─> 3 ──> 4 ─┐
   │      │            ├─> 6
   │      └─> 5 ───────┘
   └──────────────────────> (1 also feeds 6 via skill/agent structure)

3 blocks 4 (sequential Pass-1 build)
4 ∥ 5 (independent passes; both depend on 2)
6 depends on all
```
