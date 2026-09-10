# Tasks — Milestone 1 `/kk:review-architecture`

> **Design:** [design.md](design.md) · **Implementation:** [implementation.md](implementation.md) · **Umbrella:** [../design.md](../design.md)
> **Status:** done
> **Reflection (M1 complete, 2026-09-01):** The build tracked the plan closely; the recurring surprise was how many ways an eval can leak its own answers — fixture comments (Task 4), procedure inline examples (Task 5), whole-directory oracle staging (Task 4→6), and finally an inline example's *counterfactual* branch (Task 6, caught by isolated review). Each leak class is now guarded: neutral fixture comments, disjoint example/fixture surfaces, the `oracle/` sibling-dir convention with a structure-test assertion, and the counterfactual rule indexed to `kk:review-findings`. One deliberate deviation from design §9: Pass 1 evals are artifact-seeded (eval prompts must mirror real invocations), with the Pass 0/Pass 1 seam preserved via dedicated extraction assertions — recorded in design §9 and `kk:arch-decisions`. Behavioral eval outcomes remain ungraded until a harness exists; the specs are the deliverable, per convention.
> **Live behavioral pass (post-completion, 2026-09-01):** evals 7 and 8 were run manually (fixtures staged to a scratch dir, fresh agent given only `cd` + the eval prompt, output graded by `kk:eval-grader` against the oracle). Eval 7: 6 PASS / 0 FAIL / 2 PARTIAL — zero findings as required; the PARTIALs traced to the main agent summarizing instead of relaying the Claim Set verbatim. Eval 8: 6 PASS / 1 FAIL / 1 PARTIAL — assertion 8.5 failed on the fixture's primary trap (the reviewer classified the guard's own repair cost instead of the guarded decision's door, so the P1→P0 escalation never fired), and 8.7 was PARTIAL (the `pass2`-routed rationale claim was routed correctly but never discussed). Fixes applied: `pass2-soundness.md` now defines which decision a violated claim "rests on" (the decision the mechanism protects, never the enforcement convention), adds escalation-coupling and coverage self-checks, and requires every `pass2`-routed claim to be explicitly accounted for; `SKILL.md`'s Present phase now mandates verbatim relay. **The fixes are unverified by a re-run (deliberately skipped)** — the next eval-8 run should confirm 8.5 and 8.7 pass.
> **Eval-8 re-run (M2 Task 7, 2026-09-03):** re-run per the live-pass procedure (fixtures staged to a scratch dir; the installed plugin cache predates this skill, so the harness injected the working-tree SKILL.md in the production skill-invocation shape — base-directory header + SKILL.md body — with the user prompt still `cd` + the eval prompt; graded by `kk:eval-grader` against the oracle). Result: 7 PASS / 0 FAIL / 1 PARTIAL — **8.5 PASS** (P1→P0 escalation fired on C9/C10/C12, explicitly naming the violated containment claims and the C6/C7 one-way-door classification) and **8.7 PASS** (the trade-off bullet routed `pass2` and was discussed in Pass 2's reversibility grouping). The deliberately-unverified fixes are hereby confirmed. The remaining PARTIAL is 8.8 (not one of the fixed assertions): no manufactured appropriateness finding, but the report never explicitly states Pass 2 opened no source files — inferable, not asserted.
> **Eval-7 re-run (M2 Task 8, 2026-09-03):** re-run per the same live-pass procedure, verifying that the Task 7 Check A "descriptive-artifact" clarification in `pass2-soundness.md` (fire only on decisions the artifact makes or proposes, never on honestly documented divergences — added to stop eval 11's clean-kit false positive) does not under-fire on decision-bearing ADRs. Result: **8 PASS / 0 FAIL / 0 PARTIAL** — 6.3 (P1 write-through-cache appropriateness) and 6.4 (P2 shard-key reversibility) both fired on proposed decisions post-clarification; 6.5 (admission-queue negative control) stayed clean; even the previous run's two PARTIALs (verbatim Claim Set relay, Pass 2 no-files statement) resolved. Graded by `kk:eval-grader` on a sonnet model override (three consecutive 529s on its default pool; mechanical assertion-matching, low substitution risk). The clarification is also now recorded in the M2 design ([../model/design.md](../model/design.md) §6).
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

**Status:** done
**Size:** M
**Depends on:** 1, 2, 3, 4, 5
**Can run in parallel with:** —
**Docs:** [implementation.md — Build order 6 + Conventions checklist](implementation.md)

- [x] Build eval `evals/regression-clean-artifact/` — sound artifact matching its `test-files/`; asserts no findings. (Built as ADR 0015 shipment-tracking: 3 verified present claims + 1 internally-sound future claim + clean Pass 2 with an acknowledged/justified one-way door as the reversibility negative control. Domain and mechanisms deliberately disjoint from every pass-procedure inline example, per the Task 5 instruction-contamination finding.)
- [x] **Pass 2 coverage gap (deferred from Task 5 review).** Covered by the new dedicated fixture `evals/pass2-escalation-one-way-door/` (ADR 0016 device-telemetry wire format + ingest repo slice): (a) a purely rationale trade-off bullet (server CPU for radio bandwidth) that must route `pass2` and yield no finding; (b) the P1→P0 escalation — a `present` decode-path claim `violated` in the repo (diagnostics handler bypasses the shared codec) resting on a one-way-door wire-format decision, which itself is acknowledged + justified (no Check B finding, isolating the escalation).
- [x] **Oracle-staging convention (deferred from Task 4 review).** All 6 pre-existing oracles moved from `test-files/` to sibling grader-only `oracle/` dirs (both new evals ship with `oracle/` from the start); each `eval.json` description and `oracle_note` updated; convention documented in root `CLAUDE.md` §Skill evaluations (layout + Running paragraph); `pass0-extraction.md`, design.md, and implementation.md references updated. Grep confirmed no other references to the old paths.
- [x] Run `make generate-kodex`; confirm `git diff --exit-code kodex-plugin/ .codex/agents/` is clean. (Regenerated + verified idempotent.)
- [x] Run `make plugin-graph` (broken-link/orphan gate) and `bash test/test-plugin-structure.sh` — both green. (Full `test/test-*.sh` suite green.)
- [x] Index non-obvious rationale as `kk:arch-decisions` (skip if self-evident from docs). (Indexed: artifact-seeded Pass 1 evals as a confirmed intentional deviation from design §9's original "fixed claim-set" wording — grounded in the eval-prompt-fidelity rule; design §9 updated to match. Also indexed to `kk:review-findings`: an inline example's counterfactual half contaminates fixtures too — the escalation fixture's door was reworked from a wire-format/payload-% shape, which replayed pass2-soundness Check B's gRPC counterfactual, to a vendor-SDK lock-in justified by capability uniqueness + build cost; the same rework made the violated claim an import-statement violation, aligning it with dim 1's declared evidence source.)
- [x] Delete the build-order HTML comment in `SKILL.md` (Delegation phase) now that all three pass procedures exist.
- [x] Invoke `/kk:test` (full suite), `/kk:document` (update docs), `/kk:review-code` (language: shell/markdown), and `/kk:review-spec` (verify implementation matches [design.md](design.md)/[implementation.md](implementation.md)). (/kk:test: full suite + structural eval checks incl. a new oracle-staging assertion in `test-plugin-structure.sh`. Isolated /kk:review-code: 0×P0/P1, 3×P2 + 2×P3 all fixed — see the eval-8 rework note above, plus implementation.md eval-list completion and a SKILL.md blank-line cleanup; pal codereview corroborated zero issues. Isolated /kk:review-spec: 0×P0/P1; 2×P2 fixed (extraction-completeness disclaimer added to `output-contract.md` report skeleton + Output rules; artifact-seeded Pass 1 evals recorded in design §9 as intentional) + 1×P3 (G9 evidence_class rephrased from "call topology" to mechanism-presence wording) + doc drift fixed (tasks.md header status, implementation.md SKILL.md-directive split description, `oracle/` in both layout strings, escalation fixture bullet in design §9). /kk:document: `docs/user-guide/skills.md` (12 skills + reference row + utility mention), `docs/user-guide/index.md` count, `docs/contributing/architecture.md` agent list, `make plugin-graph-docs` regenerated.)
- [x] **verify:** all tests green; regression eval produces zero findings; review-spec reports no design/impl drift. (All `test/test-*.sh` green; `make plugin-graph` validate clean; `make generate-kodex` fresh + idempotent. The regression eval's zero-findings outcome is a behavioral assertion graded by a reviewer/future harness per the eval convention — its oracle and assertions are in place; no automated harness exists by design. Post-fix review-spec drift items are all resolved.)

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
