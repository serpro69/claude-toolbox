# Design Review: clarify-docs

> Historical review of the initial design. Its finding is assessed as A1 in
> [the combined assessment](review-assessment.md); the original report follows unchanged.

**Date:** 2026-09-29
**Mode:** Standard `/kk:review-design`
**Scope:** [design.md](design.md), [implementation.md](implementation.md), [tasks.md](tasks.md)
**Overall assessment:** CONCERNS_FOUND
**Summary:** 1 finding: 0 critical, 0 high, 1 medium, 0 low.

## Findings

### P0 — Critical

(none)

### P1 — High

(none)

### P2 — Medium

#### F1 — INCONSISTENT: automatic implementation coverage is broader than the existing call chain

- **Section:** design.md:43–46 and 124–129; implementation.md:93–99; tasks.md:48.
- **Confidence:** 9/10 — the existing completion step explicitly applies only to plan mode, while the design's integration table names `/kk:implement` without that qualification.
- **Description:** A standalone bug fix or issue implementation follows `/kk:implement` without reaching a prescribed `/kk:document` step. Adding the editor to `/kk:document` therefore cannot guarantee the advertised automatic coverage across both implementation modes. An agent might invoke documentation independently, but that is not the existing call-chain guarantee claimed here.
- **Evidence:** [implement/SKILL.md](../../../../klaude-plugin/skills/implement/SKILL.md), Step 5, is titled “Complete (plan mode only).” Its [plan-mode.md](../../../../klaude-plugin/skills/implement/plan-mode.md) completion procedure invokes `/kk:document`. [standalone-mode.md](../../../../klaude-plugin/skills/implement/standalone-mode.md) returns to the shared execution steps and adds no documentation completion procedure. The proposed implementation explicitly retains this call chain.
- **Recommendation:** Qualify the design and implementation claims as **plan-mode completion**, and make that scope explicit in the integration eval and user guidance. If standalone coverage is intended, instead add an explicit completion change and corresponding eval; that expands the currently planned integration scope.
- **Follow-up:** Open; owner: feature author/implementer. Next step: resolve the coverage wording before implementation. Design documents were not revised because this invocation requested review only.

### P3 — Low

(none)

## Clean Areas

- The standalone skill and shared procedure fit the repository's symlink, generation and plugin self-containment conventions.
- Instruction loading, post-draft execution, bounded editing and no-op behavior are specified consistently across the proposed consumers.
- Evidence grounding distinguishes requirements, implementation and unresolved disagreements; PR drafts have clear local-output and audience boundaries.
- Evals separate comprehension from fidelity, isolate oracles and require recorded execution evidence.
- Tasks have verification steps, size and parallel markers, explicit dependencies, exclusions and a dependency graph. Shared-file coordination is acknowledged.

## Verification and limits

Read all three feature documents; checked existing consumers, task conventions, generation configuration, structure checks and eval layout; read issue #156 and searched prior architecture/review knowledge. No implementation or behavioral evals were run: this is a pre-implementation document review.
