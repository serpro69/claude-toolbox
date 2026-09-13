# Tasks: 12-Factor design-phase profile

> Design: [./design.md](./design.md)
> Implementation: [./implementation.md](./implementation.md)
> Issue: [serpro69/claude-toolbox#101](https://github.com/serpro69/claude-toolbox/issues/101)
> Status: pending
> Created: 2026-09-13
> Scope: Phase 1 — design-phase adoption only. Issue #101 remains open; approach B is the tracked follow-up.
> Not Doing: code-level factor checks (approach B, deferred), skill-file edits, the *Beyond the Twelve-Factor App* 15-factor extension (API First / Telemetry / Security) and the `twelve-factor/twelve-factor` `next` branch, review-architecture changes

## Task 1: Author the twelve-factor profile
- **Status:** pending
- **Depends on:** —
- **Size:** M
- **Can run in parallel with:** —
- **Docs:** [implementation.md#build-order](./implementation.md#build-order)

### Subtasks
- [ ] 1.1 Create `klaude-plugin/profiles/twelve-factor/DETECTION.md` — three signal headings (`## Path signals`, `## Filename signals`, `## Content signals`) left empty, each with a one-line note that this profile does no file-based detection (code-level checks deferred to approach B); populated `## Design signals` with `display_name: 12-Factor App` and the narrow token list from design.md
- [ ] 1.2 Create `klaude-plugin/profiles/twelve-factor/overview.md` — coverage (classic 12 factors, design-phase lens), activation rules (design-token match, confirm-gated; never file-based phases), a compact enumeration of the 12 factors. Note: required by convention and for humans/authoring; the design flow does NOT load overview.md, so factor content the flow uses lives in questions.md/sections.md
- [ ] 1.3 Create `klaude-plugin/profiles/twelve-factor/design/questions.md` — refinement-question pool, one entry per factor cluster (design.md §questions.md); MUST open with the skip-preamble (skip questions already answered by user / codebase / prior decisions / existing design.md / another active profile) and defer to co-active domain profiles (e.g. k8s) the factors they already cover. Factor-accurate phrasing: III = environment variables (or named justified deviation); IX = graceful SIGTERM drain AND sudden-death robustness + reentrant/idempotent jobs; II = exact/version-pinned + isolated dependencies
- [ ] 1.4 Create `klaude-plugin/profiles/twelve-factor/design/sections.md` — four grouped required sections + the one-line codebase/dependencies (I/II) preamble + the "omit none / justify N/A" rule + the co-active merge/cross-reference rule (cover an overlapping factor once, cross-reference the domain profile's section) (design.md §sections.md)
- [ ] 1.5 Create `klaude-plugin/profiles/twelve-factor/design/index.md` — list `questions.md` and `sections.md` under **Always load** (link + one-line description each)
- [ ] 1.6 Verify locally: `DETECTION.md` has all four headings; `questions.md` contains the skip-preamble and `sections.md` the I/II preamble; every `design/index.md` link resolves and no `design/*.md` is orphaned

## Task 2: Register the profile
- **Status:** pending
- **Depends on:** Task 1
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#4-register-in-known-profiles](./implementation.md#4-register-in-known-profiles)

### Subtasks
- [ ] 2.1 Append `- twelve-factor` to the **Known profiles** list in `klaude-plugin/skills/_shared/profile-detection.md`
- [ ] 2.2 Append `twelve-factor` to `EXPECTED_PROFILES` in `test/test-plugin-structure.sh`
- [ ] 2.3 Run `bash test/test-plugin-structure.sh` → green (structure, DETECTION headings, presence-conditional index, bidirectional invariant)

## Task 3: Regenerate codex output and validate the graph
- **Status:** pending
- **Depends on:** Task 2
- **Size:** S
- **Can run in parallel with:** —
- **Docs:** [implementation.md#6-regenerate-codex-output](./implementation.md#6-regenerate-codex-output)

### Subtasks
- [ ] 3.1 Run `make generate-kodex`; commit the generated `kodex-plugin/profiles/twelve-factor/`
- [ ] 3.2 Verify `make generate-kodex && git diff --exit-code kodex-plugin/ .codex/agents/` produces no diff (CI freshness gate)
- [ ] 3.3 Run `make plugin-graph` → `plugin-graph validate` passes with no new broken links or orphans

## Task 4: Detection dry run
- **Status:** pending
- **Depends on:** Task 2
- **Size:** S
- **Can run in parallel with:** Task 3
- **Docs:** [design.md#detectionmd--design-signals](./design.md#detectionmd--design-signals)

### Subtasks
- [ ] 4.1 Confirm a service-shaped idea prose (e.g. containing "stateless service" / "backing service") surfaces the confirm prompt to activate the `twelve-factor` profile in `/kk:design`
- [ ] 4.2 Confirm a pure library/CLI/tooling idea does NOT activate it (no false positive)
- [ ] 4.3 Confirm a file-based run (e.g. `/kk:review-code`) never activates the profile (empty file signals)

## Task 5: Author /kk:design detection evals
- **Status:** pending
- **Depends on:** Task 1, Task 2
- **Size:** M
- **Can run in parallel with:** Task 3, Task 4
- **Docs:** [design.md#assumptions](./design.md#assumptions); `AGENTS.md` §Skill evaluations

### Subtasks
- [ ] 5.1 Add `klaude-plugin/skills/design/evals/twelve-factor-activation/` — positive service-shaped prompt; assert `twelve-factor` activates AND the produced design covers every required profile section
- [ ] 5.2 Add `.../twelve-factor-regression-library/` — library/CLI prompt; assert the profile does NOT activate (regression)
- [ ] 5.3 Add `.../twelve-factor-ambiguous-fallback/` — infra prompt naming no technology; assert the shared fallback prompt fires
- [ ] 5.4 Add `.../twelve-factor-k8s-coactivation/` — Kubernetes SaaS prompt; assert both profiles activate and overlapping factors (rollback, graceful shutdown, logs, config) are asked/required once, not duplicated
- [ ] 5.5 Each eval is self-contained (`eval.json` + `test-files/`; oracles in a sibling `oracle/`, never inside `test-files/`)

## Task 6: Final verification
- **Status:** pending
- **Depends on:** Task 1, Task 2, Task 3, Task 4, Task 5
- **Size:** S
- **Can run in parallel with:** —

### Subtasks
- [ ] 6.1 Run `/kk:test` to verify the full test suite (`test/test-*.sh`, `make generate-kodex`, `make plugin-graph`)
- [ ] 6.2 Run `/kk:document` to update any relevant docs (e.g. an entry noting the new profile if a profile index exists)
- [ ] 6.3 Run `/kk:review-code` to review the changes
- [ ] 6.4 Run `/kk:review-spec` to verify the implementation matches design.md and implementation.md

## Deferred (not tasks — recorded so the gap is visible)

Approach B (code-level 12-factor checks in implement/review phases) is deferred
pending resolution of the deployability-gate question and exploration of
alternatives. See [design.md §Deferred / Future Work](./design.md#deferred--future-work).
Do not open B tasks until the gate design is settled.

## Dependency Graph

```
Task 1 ─→ Task 2 ─┬─→ Task 3 ─→ Task 6
                  ├─→ Task 4 ─→ Task 6
                  └─→ Task 5 ─→ Task 6
```
