# Tasks — Milestone 2 `/kk:model`

> **Design:** [design.md](design.md) · **Implementation:** [implementation.md](implementation.md) · **Umbrella:** [../design.md](../design.md)
> **Status:** pending
> **Not Doing:** decide producer (M2.1); decompose producer (M2.2+); M3 hand-off; process-review skill; profile `architecture/` phase (M4); /kk:design changes; freshness CI; session-close guard (falsified).

---

## Task 1 — Shared guards + `/kk:model` skeleton

**Status:** done
**Size:** M
**Depends on:** —
**Can run in parallel with:** 6
**Slicing:** Contract-First (the guard files define the producer workflow spine every later task builds on)
**Docs:** [design.md §5](design.md) · [implementation.md — Build order 1](implementation.md)

- [x] Create `klaude-plugin/skills/_shared/requirements-harvesting.md`, `open-question-pass.md`, `fact-flip-propagation.md`, `contact-ratio-guard.md` — each opens with its motivating failure (design §1 F1/F4/F2/F5), then the rule as a mandatory workflow step, written producer-generic (consumable by `decide` later without edits).
- [x] Create `klaude-plugin/skills/model/SKILL.md` — frontmatter (`name: model`, trigger-keyword-first description ≤1024 soft), ADR-0004 mandatory-order directive, seven-phase Workflow summary (placeholder links to files landing in Tasks 2–4 are acceptable only if `make plugin-graph` stays green — otherwise stub the files in this task). *(Stubbed `model-process.md`, `kit-contract.md`, `archaeology.md` to keep the link/orphan gate green; populated in Tasks 2–4.)*
- [x] Create the five `shared-` symlinks in `klaude-plugin/skills/model/` (`ln -s ../_shared/<name>.md shared-<name>.md`): the four new guards plus the existing `capy-knowledge-protocol.md`.
- [x] Add `model` to `EXPECTED_SKILLS` in `test/test-plugin-structure.sh`; run `make generate-kodex`.
- [x] **verify:** `bash test/test-plugin-structure.sh` green; `make plugin-graph` link/orphan gate clean; `git diff --exit-code kodex-plugin/` clean after regen. *(`make generate-kodex`'s bundled `test-codex-structure.sh` reports 7 pre-existing TOML failures — this env has Python 3.10 with no `tomllib`/`tomli`; unrelated to this change, `.codex/` regen is idempotent.)*

## Task 2 — Kit output contract + kit-format eval

**Status:** pending
**Size:** M
**Depends on:** 1
**Can run in parallel with:** 6
**Docs:** [design.md §3](design.md) · [implementation.md — Build order 2](implementation.md)

- [ ] Create `klaude-plugin/skills/model/kit-contract.md` — glossary page format (dual-audience entry fields, status markers, rules table + provenance banner, one conceptual-altitude diagram, Derived-from footer, no line numbers, ticket-note retirement discipline, 10–20 term guideline with variance drivers), traps page format (P#/D# stable numbering, no schema mirror, self-limiting entries), conventions-index content (once per home), freshness banner (proposed-until-reviewed + re-verification via `/kk:review-architecture`), homes-resolution precedence, kit-scope pushback.
- [ ] Build `evals/kit-format/` — small fictional-domain code slice in `test-files/`; oracle checklist in `oracle/` covering every kit convention; assertions per convention (all intent claims `proposed`; no line numbers; footer complete; exactly one diagram; no schema mirror in traps).
- [ ] **verify:** eval JSON valid; every design-§3 convention has a corresponding assertion; structure tests + plugin-graph green.

## Task 3 — Production workflow + requirements-gate & hidden-invariant evals

**Status:** pending
**Size:** M
**Depends on:** 2
**Can run in parallel with:** 6
**Docs:** [design.md §4](design.md) · [implementation.md — Build order 3](implementation.md)

- [ ] Create `klaude-plugin/skills/model/model-process.md` — the seven phases (greenfield path): scope intake + forcing question + capy search per the shared protocol (`kk:arch-decisions`, `kk:project-conventions`), requirements gate (invokes the shared guard), archaeology (links `archaeology.md`), kit drafting (links `kit-contract.md`), verification (confirm-pass + open-question pass via shared guard), conventions-bind-author self-check, surface & close (RQ queue with role deciders, appended to the feature's `docs/wip/<feature>/design.md` **Open Questions** section when the feature dir exists; contact-ratio guard; capy indexing of non-obvious rationale).
- [ ] Create `klaude-plugin/skills/model/archaeology.md` — state → time → invariants reading order; two-clock discipline; model-in-service-of-the-decision scoping.
- [ ] Sync the SKILL.md phase summary with `model-process.md`; run the ADR-0004 dedup pass (no repeated content-read instructions).
- [ ] Build `evals/requirements-gate/` (ticket files present; trap: modelling without quoting the asks / inventing a brief) and `evals/hidden-invariant/` (code slice hiding a single-result-lookup-class cross-file trap; trap: confirm-only verification missing it).
- [ ] **verify:** phase summary and process file agree; both evals' traps map to F1/F4; assertions decidable from output text alone; all gates green.

## Task 4 — Brownfield mode + brownfield-update eval

**Status:** pending
**Size:** M
**Depends on:** 3
**Can run in parallel with:** 6, 7
**Docs:** [design.md §4 (intake, close)](design.md) · [implementation.md — Build order 4](implementation.md)

- [ ] Extend `model-process.md`: brownfield intake (read existing kit in full first; baseline + deltas; never flip status markers unilaterally) and brownfield close (fact-flip propagation on contradicted recorded facts).
- [ ] Build `evals/brownfield-update/` — existing fictional-domain kit + drifted code slice; ≥2 seeded stale assertions in distinct files; a `proposed` entry a naive run would "promote".
- [ ] **verify:** assertions cover (a) every seeded stale assertion caught, (b) no unilateral `proposed → canonical` flip, (c) delta update rather than full rewrite; all gates green.

## Task 5 — Scope-pushback regression eval + description tuning

**Status:** pending
**Size:** S
**Depends on:** 3
**Can run in parallel with:** 4, 6, 7
**Docs:** [design.md §7](design.md) · [implementation.md — Build order 5](implementation.md)

- [ ] Build `evals/scope-pushback/` — natural prompt asking `/kk:model` for a durable full ERD / schema-mirror page; assertions require pushback naming the maintenance cost (and offering the kit or a disposable per-feature diagram instead), not silent compliance.
- [ ] Re-check the SKILL.md description against the trigger list and budget now that all skill content exists.
- [ ] **verify:** eval JSON valid; assertions decidable; description ≤1024 chars with triggers front-loaded.

## Task 6 — M1 extension: provenance + composite acceptance + self-certification check

**Status:** pending
**Size:** M
**Depends on:** —
**Can run in parallel with:** 1, 2, 3, 4, 5
**Docs:** [design.md §6.1–6.2](design.md) · [implementation.md — Build order 6](implementation.md)

- [ ] Extend `klaude-plugin/skills/review-architecture/pass0-extraction.md` — `provenance` field (`harvested` / `reverse-engineered` / `fabricated-labeled`; derived from artifact text only; repo-blind preserved) + the self-certification check (canonical-status + reverse-engineered provenance + no ratification source → P2, internal-soundness).
- [ ] Extend `input-contract.md` — composite domain-reference-kit acceptance with invocation mechanics per design §6.2: either page's path invokes the pair (sibling naming convention `<context>.md` ↔ `<context>-traps.md`, cross-link fallback); two explicit paths still rejected, rejection message gains the kit clause; single-page kits accepted solo with an unresolvable-cross-references note.
- [ ] Extend `pass2-soundness.md` — the provenance-consistency check as Pass 2's third check: `canonical`/ratified status + `reverse-engineered` provenance + no cited ratification record → P2.
- [ ] Update `output-contract.md` — **Provenance** subsection under Pass 2 findings, the self-certification severity row (P2), composite-kit invocation/acceptance wording.
- [ ] Update `review-architecture/SKILL.md` (description: domain-reference-kit artifact type + glossary/domain-kit trigger keywords + dimension enumeration, ≤1024 recheck; Phase 1 + Invocation composite wording) and `klaude-plugin/agents/architecture-reviewer.md` (description artifact types; "single accepted artifact" payload line).
- [ ] Build `evals/pass0-provenance/` — canonical-by-decree artifact + properly-labeled twin claim (negative control); oracle with expected provenance per claim + the expected finding (Pass 2 Provenance subsection); assertions split the Pass 0 field-assignment seam from the Pass 2 finding seam.
- [ ] **verify:** the P2 finding fires only for the decree claim, in the Provenance subsection; existing M1 evals' gold files unaffected (provenance is additive — confirm no gold-claims schema break); SKILL.md description within budget; all gates green (incl. kodex regen for the agent file).

## Task 7 — M1 extension: dimension 7 + binding evals + eval-8 re-run

**Status:** pending
**Size:** M
**Depends on:** 6
**Can run in parallel with:** 4, 5
**Docs:** [design.md §6.3](design.md) · [implementation.md — Build order 7](implementation.md)

- [ ] Extend `pass0-extraction.md` — the dimension-7 routing set: `dimension` token enum → `7`, Domain Binding row in §Dimension routing, domain-reference-kit row in the artifact-type mining table (per-term Bindings + rules-table enforcement pointers → dim 7; rule intent → provenance-labeled, not truth-verified).
- [ ] Extend `pass1-topology.md` — dimension 7 (Domain Binding): claim class, existence-only evidence via Grep/Glob, anchor-rule application, both fallback outcomes (`Bindings: none yet` → `internally-sound`; future binding naming no code-element kind → `ill-formed`), altitude-line note. Inline examples domain-disjoint from all fixtures **including counterfactual branches**.
- [ ] Build `evals/pass1-domain-binding/` — fictional-domain two-page kit (re-skinned from the field kit's trap structure) + code slice; prompt passes one page's path (counterpart auto-discovered); assertions cover extraction routing (binding claims → dim 7, none `unrouted`) and verdicts: `verified`, `violated` (missing symbol in existing anchor), `dangling-anchor` (nonexistent file), `internally-sound` (`future`), `ill-formed` negative control.
- [ ] Build `evals/regression-clean-kit/` — sound kit matching its slice; zero findings.
- [ ] Re-run M1 eval 8 (`pass2-escalation-one-way-door`) per the M1 live-pass procedure; confirm assertions 8.5 and 8.7 pass post-fix.
- [ ] **verify:** binding claims route to token 7 with no `unrouted` leakage; all dimension-7 verdict outcomes discriminated; clean kit zero findings; eval-8 assertions 8.5/8.7 PASS recorded in [../review/tasks.md](../review/tasks.md); all gates green.

## Task 8 — Final verification

**Status:** pending
**Size:** M
**Depends on:** 1, 2, 3, 4, 5, 6, 7
**Can run in parallel with:** —
**Docs:** [implementation.md — Build order 8 + Conventions checklist](implementation.md)

- [ ] Full `test/test-*.sh` suite; `make plugin-graph`; `make generate-kodex` fresh + idempotent.
- [ ] Grep all new skill files and fixtures for real project names, tickets, or people — must be zero (generified-content rule).
- [ ] Update `docs/user-guide/skills.md` (+ index count) and regenerate `make plugin-graph-docs` if applicable.
- [ ] Index non-obvious rationale to `kk:arch-decisions` (composite-artifact acceptance rationale; provenance-orthogonal-to-tense; falsified session-close guard as the first learnings revision).
- [ ] Invoke `/kk:test` (full suite), `/kk:document` (docs), `/kk:review-code` (language: shell/markdown), `/kk:review-spec` (implementation vs [design.md](design.md)/[implementation.md](implementation.md)).
- [ ] **verify:** all suites green; review-spec reports no drift; user-guide counts match.

## Dependency Graph

```
1 ──> 2 ──> 3 ──> 4 ─┐
             │        ├─> 8
             └──> 5 ──┤
6 ──────────> 7 ──────┘
(6 ∥ 1–5; 7 ∥ 4–5; 8 depends on all)
```
