# Tasks — Milestone 1 `/kk:review-architecture`

> **Design:** [design.md](design.md) · **Implementation:** [implementation.md](implementation.md) · **Umbrella:** [../design.md](../design.md)
> **Status:** pending
> **Not Doing:** producer skills (decompose/decide/model); nested flow & architecture-implement hand-off; profile `architecture/` phase + profile detection; behavioral/runtime verification; security architecture (→ PAL `secaudit`); writing broader architecture docs; multi-artifact invocations & cross-artifact consistency (single artifact per invocation).

---

## Task 1 — Skill skeleton, acceptance contract, agent stub

**Status:** done
**Size:** M
**Depends on:** —
**Can run in parallel with:** —
**Slicing:** Contract-First (defines the input boundary the rest builds on)
**Docs:** [design.md §2](design.md) · [implementation.md — Build order 1](implementation.md)

- [x] Create `klaude-plugin/skills/review-architecture/SKILL.md` with frontmatter (`name`, trigger-keyword-first `description` ≤1024 soft/1536 hard chars) and a Workflow section carrying the ADR-0004 mandatory-order directive.
- [x] Create `klaude-plugin/skills/review-architecture/input-contract.md` (accepted artifact types; single-artifact-per-invocation rule; diagram-with-prose rule; verbal/diagram-only rejection with actionable message).
- [x] Create `klaude-plugin/skills/review-architecture/output-contract.md` (invocation/scope; report structure — Claim Set, verdicts by dimension, Not Reviewed, Pass 2 findings; verdict vocabulary + severity mapping per design §7).
- [x] Create `klaude-plugin/agents/architecture-reviewer.md` — read-only tools (`Read`/`Grep`/`Glob`/`mcp__capy__capy_search`), role-named, restates instruction-before-action rule, `## Plugin Root` injection.
- [x] Wire the SKILL.md Workflow to actually delegate: an explicit spawn phase for `architecture-reviewer` that resolves `$TOOLBOX_PLUGIN_ROOT`, injects `## Plugin Root`, and enumerates the payload (artifact path + heading, pass-procedure paths, output-contract path). (Added after code review — the hand-off falls between the SKILL and agent, both Task 1; per implementation.md the M1 mode delegates.)
- [x] Add `review-architecture` to `EXPECTED_SKILLS` in `test/test-plugin-structure.sh`. No command pair in M1 (decided — see implementation.md Orientation); `EXPECTED_COMMANDS` untouched. (Also added `architecture-reviewer` to `EXPECTED_AGENTS` in `test/test-codex-structure.sh` and regenerated Codex output via `make generate-kodex` to keep the generation-completeness gate green.)
- [x] **verify:** invoke on a verbal-only input → rejected w/ message; on two ADRs at once → rejected (single-artifact rule); on a real ADR → accepted; `bash test/test-plugin-structure.sh` green. (Automated: all `test/test-*.sh` green + `make plugin-graph` validate clean. Behavioral accept/reject verification is exercised by the Task 2+ evals; the acceptance rules live in `input-contract.md`.)

## Task 2 — Pass 0: claim extraction + recall eval

**Status:** done
**Size:** M
**Depends on:** 1
**Can run in parallel with:** —
**Docs:** [design.md §4](design.md) · [implementation.md — Build order 2](implementation.md)

- [x] Create `pass0-extraction.md` — full claim schema (`id`/`claim`/`source_span`/`dimension`/`tense`/`evidence_class`), repo-blind rule, four sub-metrics (precision/recall/evidence-class/routing), structural-slot heuristics per artifact type. (Added a deontic-wording tense rule and pinned the `dimension` enum to numeric tokens after code review.)
- [x] Build eval `evals/pass0-extraction-recall/` — artifact fixture (Accepted ADR splitting orders/billing) + `gold-claims.json` (G1–G9) in `test-files/`; `assertions[]` (1.1–1.20) reference gold entries. Oracle is grader-only — kept out of `files[]` to avoid leaking answers to the model under test.
- [x] **verify:** JSON valid; all 9 gold `source_span`s are verbatim substrings of the ADR (precision-gradeable); `bash test/test-plugin-structure.sh`, full `test/test-*.sh` suite, and `make plugin-graph` (orphan gate) green; `make generate-kodex` fresh. Regression assertion 1.17 guards against fabricated claims; routing assertions (1.11–1.16, 1.19–1.20) guard `dimension`/`tense`. (No automated eval harness exists — behavioral run is graded by a reviewer/future harness per the eval convention.)

## Task 3 — Pass 1: engine + dimensions 1–3 (Boundaries, Data Ownership, NFR)

**Status:** done
**Size:** M
**Depends on:** 1, 2
**Can run in parallel with:** —
**Docs:** [design.md §5](design.md) · [implementation.md — Build order 3](implementation.md)

- [x] Create `pass1-topology.md` with the anchor-rule mode decision (tense + anchor existence → reality / internal-soundness / dangling-anchor) and dimensions 1–3, each with inline evidence-gathering examples (profile-substitute). Dimensions 4–6 deferred to Task 4 via a build-order comment. (Post-review hardening: added a **prohibitive-polarity** rule to the anchor decision — for "must not depend" claims the mechanism is the *absence* of a forbidden edge, so absence ⇒ `verified`, not `violated`; dangling-anchor now reports searched locations; dim 2 closes the "owner holds no migrations/routes" case; inline examples phrased as Grep-tool ops, not shell/pipes, since the reviewer agent has no Bash.)
- [x] Build evals `evals/pass1-boundary-violation/` (manifest with a real forbidden dependency), `evals/pass1-greenfield-fallback/` (forward-looking claims, no code), and `evals/pass1-brownfield-proposed/` (existing repo + mixed `future` proposal / `present` violation / dangling-anchor claims). Each ships a grader-only `expected-verdicts.json` (excluded from `files[]`, mirroring Task 2's `gold-claims.json`).
- [x] **verify:** boundary violation caught against a static manifest; greenfield `future` claims fall back to internal-soundness (not flagged as failures); brownfield fixture discriminates violation vs proposal vs dangling-anchor. (Automated gates: JSON valid; `bash test/test-plugin-structure.sh` green (179/0); `make plugin-graph` validate clean; `make generate-kodex` fresh + idempotent. Behavioral eval runs are graded by a reviewer/future harness per the eval convention. Isolated `/kk:review-code` applied: 2×P1 + 1×P2 + supporting findings fixed — see note below; also hardened `pass0-extraction.md` for the Proposed-ADR deontic tense gap the fixtures surfaced.)

## Task 4 — Pass 1: dimensions 4–6 (Failure Isolation, State Consistency, Evolution)

**Status:** done
**Size:** M
**Depends on:** 3
**Can run in parallel with:** 5
**Docs:** [design.md §5](design.md) · [implementation.md — Build order 4](implementation.md)

- [x] Extend `pass1-topology.md` with dimensions 4, 5, 6 (each claim/evidence/fallback + inline examples). (Post-review hardening: dim 5 gained a **placement qualifier** — the unique constraint must cover the key the claimed mutation writes, not any incidental `UNIQUE`; dim 6's accept criterion was tightened from "versioned routes and/or migration tooling" to **consumer-facing version routing OR expand-contract migrations** — a bare `migrations/` dir is insufficient and collides with dim 2's evidence; dim 6 gained the `/kk:review-code` behavioral pointer and a "no dim-6 claim → no dim-6 verdict" scope note; Glob example fixed to match files not dirs.)
- [x] Add a fixture proving 4 and 5 grade **independently** (`evals/pass1-independent-4-5/`: circuit-breaker present → dim 4 `verified`, idempotency absent → dim 5 `violated`). (Post-review: stripped dimension numbers / verdict tokens / behavioral conclusions from the code+SQL fixture comments — they were dictating the graded assertions and the negative fixture's comment text matched the dim-5 Grep pattern, inverting the verdict; renamed the ADR's dimension-named bullet labels ("Failure isolation"/"State consistency") to neutral mechanism-tied framing ("Payments dependency"/"Retry safety") to force routing to be earned from mechanism words and avoid the dim-1 "isolation" keyword collision.)
- [x] **verify:** the fixture scores dim 4 pass / dim 5 fail separately — no blended verdict. (JSON valid; full `test/test-*.sh` suite green (179/0); `make plugin-graph` validate clean; `make generate-kodex` fresh + idempotent. No automated eval harness exists — the behavioral dim-4-pass/dim-5-fail run is graded by a reviewer/future harness per the eval convention. Isolated `/kk:review-code` applied: 1×P1 (fixture verdict-leak) + 3×P2 (dim-5 placement, dim-6 criterion, ADR routing labels) + 3×P3 fixed; see the Task 4 subtask notes above.)

## Task 5 — Pass 2: decision soundness & reversibility

**Status:** done
**Size:** S
**Depends on:** 2
**Can run in parallel with:** 4
**Docs:** [design.md §6](design.md) · [implementation.md — Build order 5](implementation.md)

- [x] Create `pass2-soundness.md` — appropriateness-against-stated-context + one-way/two-way door + proportional-justification procedure; internal-soundness-only (no reality branch). (Made the input scope explicit — Pass 2 grades ALL decision-bearing claims, not only `pass2`-routed ones, per design §6; added the stated-context "no finding without a quotable constraint" guard and the P1→P0 escalation coupling to Pass 1.)
- [x] Build eval `evals/pass2-inappropriate-mechanism/` (write-heavy ADR + write-through cache). Proposed ADR (all `future` → Pass 1 internal-soundness, no repo) so the eval isolates Pass 2 judgment; three decisions — write-through cache (appropriateness P1), shard-key with no reversibility justification (reversibility P2), bounded admission queue (negative control). Grader-only `expected-findings.json` excluded from `files[]`.
- [x] **verify:** the mismatch is flagged; a context-appropriate choice is not. (JSON valid; full `test/test-*.sh` suite green; `make plugin-graph` validate clean; `make generate-kodex` fresh. No automated eval harness — the behavioral flag/no-flag run is graded by a reviewer/future harness per the eval convention. Isolated `/kk:review-code` applied — see Task 5 note.)

## Task 6 — Regression eval, Codex parity, tests, docs (final verification)

**Status:** pending
**Size:** M
**Depends on:** 1, 2, 3, 4, 5
**Can run in parallel with:** —
**Docs:** [implementation.md — Build order 6 + Conventions checklist](implementation.md)

- [ ] Build eval `evals/regression-clean-artifact/` — sound artifact matching its `test-files/`; asserts no findings.
- [ ] **Pass 2 coverage gap (deferred from Task 5 review).** The `pass2-inappropriate-mechanism` fixture exercises appropriateness (F1) and reversibility (F2), but two Pass 2 paths are unexercised: (a) a *purely* rationale/trade-off claim routed to `pass2` (Inputs bullet 2 of `pass2-soundness.md`), and (b) the **P1→P0 escalation** of a Pass 1 `violated` verdict whose decision Pass 2 classifies a one-way door — which needs a repo (a real `violated`) plus a one-way-door decision in the same artifact. Add a dedicated fixture (or extend the regression/brownfield fixtures) to cover both, or explicitly document them as untested in M1.
- [ ] **Oracle-staging convention (deferred from Task 4 review).** Every eval's grader-only oracle (`expected-verdicts.json`, `gold-claims.json`) currently lives *inside* `test-files/` and is only kept out of `eval.json` `files[]`. A harness that stages the whole `test-files/` directory (per the eval-running convention in root `CLAUDE.md` §Skill evaluations) would copy the oracle alongside the artifact, leaking answers to the model under test. Pre-existing across all evals (`pass0-extraction-recall`, `pass1-boundary-violation`, `pass1-greenfield-fallback`, `pass1-brownfield-proposed`, `pass1-independent-4-5`) — not introduced by Task 4. **Fix:** move oracles out of `test-files/` (e.g. a sibling `oracle/` dir) and update the eval convention + each `eval.json` `description`. Confirm nothing references the old path first.
- [ ] Run `make generate-kodex`; confirm `git diff --exit-code kodex-plugin/ .codex/agents/` is clean.
- [ ] Run `make plugin-graph` (broken-link/orphan gate) and `bash test/test-plugin-structure.sh` — both green.
- [ ] Index non-obvious rationale as `kk:arch-decisions` (skip if self-evident from docs).
- [ ] Delete the build-order HTML comment in `SKILL.md` (Delegation phase) now that all three pass procedures exist.
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
