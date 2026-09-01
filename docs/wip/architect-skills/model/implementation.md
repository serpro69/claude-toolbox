# Milestone 2 — `/kk:model` — implementation plan

**Design:** [design.md](design.md). **Umbrella:** [../design.md](../design.md).

Audience: a skilled contributor with **zero context** on this codebase. Read [design.md](design.md) fully first; read root `CLAUDE.md` §Skill & Command Naming Conventions, §Skill workflow ordering, §Skill evaluations, and §Profile Conventions before touching files. `klaude-plugin/` is the canonical source; Codex output is generated.

---

## Orientation — study these existing analogues first

- `klaude-plugin/skills/design/SKILL.md` + `idea-process.md` — the closest analogue: a main-session, file-writing, user-interacting skill with ADR-0004 mandatory ordering and a multi-step interactive workflow. `/kk:model` follows this shape, **not** the reviewer-delegation shape.
- `klaude-plugin/skills/_shared/` + the per-skill `shared-` symlink pattern (root `CLAUDE.md` §Shared instructions) — how the four guard files are wired.
- `klaude-plugin/skills/review-architecture/` — the M1 skill this milestone extends: `pass0-extraction.md` (claim schema), `input-contract.md` (acceptance), `pass1-topology.md` (dimensions + anchor rule), and its `evals/` layout.
- `klaude-plugin/skills/review-code/evals/` and `review-architecture/evals/` — the `evals/<name>/{eval.json,test-files/,oracle/}` layout, `eval.json` schema, and the oracle-staging convention (grader-only `oracle/` sibling).

**Decisions already made (do not relitigate):** main-session skill, no new agent, no command pair in M2 (mirror M1's reasoning — revisit a default/isolated split after the producer is proven); no profile detection in `/kk:model`; M1's architecture frozen, extensions additive only.

## File inventory (all under `klaude-plugin/`, the canonical source)

**Skill** — `klaude-plugin/skills/model/`:

- `SKILL.md` — entry point. Frontmatter `name`/`description` (trigger keywords first: model, domain model, glossary, bounded context, domain reference, information architecture; ≤1024 soft/1536 hard chars). Workflow section with the ADR-0004 mandatory-order directive and the seven-phase summary matching `model-process.md` exactly (no ordering drift between the two).
- `model-process.md` — the detailed seven-phase workflow (design §4): scope intake + mode detection, requirements gate, archaeology, kit drafting, verification, self-check, surface & close.
- `kit-contract.md` — the output contract (design §3): the two page formats, conventions-index content, status markers, freshness banner, homes-resolution precedence, kit-scope pushback, term-count guideline with variance drivers.
- `archaeology.md` — the state → time → invariants reading method and two-clock discipline (single-consumer content; promote to `_shared/` only when a second producer needs it).
- `shared-requirements-harvesting.md`, `shared-open-question-pass.md`, `shared-fact-flip-propagation.md`, `shared-contact-ratio-guard.md` — symlinks to `_shared/`.
- `evals/<name>/{eval.json,test-files/,oracle/}` — five evals per design §7.

**Shared guards** — `klaude-plugin/skills/_shared/`:

- `requirements-harvesting.md`, `open-question-pass.md`, `fact-flip-propagation.md`, `contact-ratio-guard.md` — each opens with the motivating failure (design §1 F-numbers), then the rule as a mandatory workflow step. Written for any producer, not `/kk:model` specifically.

**M1 extensions** — `klaude-plugin/skills/review-architecture/`:

- `pass0-extraction.md` — add the `provenance` field (values, derivation-from-artifact-text rules, repo-blind preserved) and the self-certification check (P2, internal-soundness).
- `input-contract.md` — add the composite domain-reference-kit acceptance clause (glossary + traps pair as one artifact; rationale: hard cross-references).
- `pass1-topology.md` — add dimension 7 (Domain Binding): claim class, evidence (element existence via Grep/Glob), greenfield fallback (`Bindings: none yet` = well-formed `future`), anchor-rule application, altitude-line note (behavior → review-code/review-spec). Inline examples must be domain-disjoint from every fixture, including counterfactual branches.
- `output-contract.md` — extend the verdict/report vocabulary only if dimension 7 or the self-certification check needs it (expected: dimension list mention; no new verdicts).
- `evals/` — three new evals per design §7.

**Tests** — `test/test-plugin-structure.sh`: add `model` to `EXPECTED_SKILLS`; per-skill assertions pick up the new eval dirs and symlinks automatically — verify, don't assume.

**Codex parity** — `make generate-kodex`; CI freshness via `git diff --exit-code kodex-plugin/ .codex/agents/`. Do NOT hand-edit generated output.

**Docs** — `docs/user-guide/skills.md` (+ index count), `make plugin-graph-docs` if the graph doc is regenerated.

## Eval fixtures (build alongside each slice, TDD)

Per design §7. Authoring rules that bit M1 (all indexed in `kk:review-findings`): neutral fixture comments (no verdict/dimension tokens); fixture domains disjoint from procedure inline examples **including their counterfactual branches**; oracles in grader-only `oracle/` siblings, never in `test-files/`; eval prompts mirror real invocations (natural user phrasing, no harness language). The `pass1-domain-binding` fixture is adapted from the field workstream's kit **re-skinned to a fictional domain** — no real project names, tickets, or people.

## Build order (vertical slices — each ends runnable + green)

Each step names its verification.

1. **Guards + skill skeleton** (contract-first: the guard files define the workflow spine). Write the four `_shared/` guard files; create `skills/model/` with SKILL.md (frontmatter, mandatory-order directive, seven-phase summary) + symlinks; add to `EXPECTED_SKILLS`. → *verify:* `bash test/test-plugin-structure.sh` green; `make plugin-graph` link/orphan gate clean; `make generate-kodex` fresh.
2. **Kit contract + kit-format eval.** Write `kit-contract.md`; build `evals/kit-format/`. → *verify:* eval JSON valid; oracle checklist covers every §3 convention; fixture staged under `test-files/` only.
3. **Process + archaeology + requirements-gate & hidden-invariant evals.** Write `model-process.md` + `archaeology.md`; build `evals/requirements-gate/` and `evals/hidden-invariant/`. → *verify:* SKILL.md phase summary matches `model-process.md` (dedup pass per ADR-0004 authoring rule 3); both evals' traps map to F1/F4.
4. **Brownfield mode + brownfield-update eval.** Extend `model-process.md` intake + close phases; build `evals/brownfield-update/` (existing kit + drifted code + ≥2 seeded stale assertions in distinct files). → *verify:* eval asserts all seeded stale assertions are caught (fact-flip), and the no-unilateral-flip assertion is present.
5. **Scope-pushback regression eval.** Build `evals/scope-pushback/`. → *verify:* the prompt asks for a durable ERD/schema mirror naturally; assertions require refusal-with-maintenance-cost, not silent compliance.
6. **M1 extension: provenance + composite acceptance + self-certification check + `pass0-provenance` eval.** → *verify:* Pass 0 stays repo-blind (provenance derives from artifact text only — assert in eval); the properly-labeled twin claim draws no finding.
7. **M1 extension: dimension 7 + `pass1-domain-binding` + `regression-clean-kit` evals; eval-8 re-run.** → *verify:* dimension-7 verdicts discriminate all four outcomes; clean kit yields zero findings; re-run M1 eval 8 and confirm assertions 8.5/8.7 now pass (closing the deliberately-unverified fix from M1).
8. **Final verification.** → *verify:* full `test/test-*.sh` green; `make plugin-graph` clean; `make generate-kodex` fresh + idempotent; `/kk:test`, `/kk:document`, `/kk:review-code`, `/kk:review-spec` run per the tasks file.

## Conventions checklist (do not skip)

- **ADR 0004 ordering** — instructions (SKILL.md + process + guards + kit contract) fully loaded before subject-matter action; the content-read instruction appears exactly once, after instruction-load; SKILL.md phase summary matches the process file.
- **Naming** — `/kk:model` (imperative, no family prefix); `_shared/` bare basenames; `shared-` symlink prefix per consumer.
- **`${TOOLBOX_PLUGIN_ROOT}` rules** — brace form only in plugin-load files (SKILL.md); files read at runtime via `Read` (guards, kit contract, process) must not forward the literal token.
- **Description budget** — trigger keywords first; ≤1024 soft.
- **Generified content** — no real project names, tickets, or people anywhere in skill files or fixtures.
- **Capy** — index only non-obvious rationale as `kk:arch-decisions` after the build stabilizes.

## Assumptions (validate during build)

- Producer evals are gradeable without a harness by asserting on observable output properties (quoted asks, conventions present, pushback text) — if a `kit-format` grader can't decide an assertion, the kit contract needs tightening, not the eval.
- Dimension-7 evidence gathering needs no profile — if the binding eval is flaky across stacks, revisit the M4 profile question sooner.

## Not Doing / Rejected Alternatives

Carried from [design.md](design.md) §Not Doing / §Rejected Alternatives. Notably: no `decide`/`decompose`, no new agent, no command pair, no profile detection, no session-close guard (falsified), no `/kk:design` changes.
